"""Compact, auditable reference kernel for the August 2026 Aurora profile."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, IntEnum
from typing import Iterable, Iterator, Sequence

Trit = int
Triplet = tuple[Trit, Trit, Trit]
TRITS = frozenset((0, 1, 2))
OPEN: Triplet = (2, 2, 2)
class AuroraError(ValueError):
    """Invalid input or an operation forbidden by the frozen profile."""
class Direction(IntEnum):
    """The cell transformed while A remains the anchor."""

    LEARN_M = 0
    INFER_R = 1
    DEDUCE_B = 2
class RelationState(Enum):
    CLOSED = "closed"
    CONTRADICTION = "contradiction"
    OPEN = "open"
    AMBIGUOUS = "ambiguous"
    TRANSIENT = "transient"
    UNRESOLVED = "unresolved"
def trit(value: int) -> Trit:
    if value not in TRITS:
        raise AuroraError(f"expected trit 0, 1 or 2; got {value!r}")
    return value
def triplet(values: Iterable[int]) -> Triplet:
    result = tuple(values)
    if len(result) != 3:
        raise AuroraError(f"expected exactly three trits; got {result!r}")
    return trit(result[0]), trit(result[1]), trit(result[2])
def majority3(a: Trit, b: Trit, m: Trit) -> Trit:
    """Honest ternary majority; completeness 0-1-2 remains open as 2."""
    a, b, m = trit(a), trit(b), trit(m)
    if a == b or a == m:
        return a
    if b == m:
        return b
    return 2
def symmetry(values: Sequence[Trit]) -> int:
    """S(DD) = 3 - |unique(DD)|."""
    values = triplet(values)
    return 3 - len(set(values))
def candidate_domain(
    a: Trit, b: Trit, m: Trit, r: Trit, direction: Direction
) -> frozenset[Trit]:
    """All target values compatible with Majority3(A,B,M)=R."""
    cells = [trit(a), trit(b), trit(m), trit(r)]
    target = {Direction.LEARN_M: 2, Direction.INFER_R: 3,
              Direction.DEDUCE_B: 1}[Direction(direction)]
    compatible: set[Trit] = set()
    for value in TRITS:
        probe = cells.copy()
        probe[target] = value
        if majority3(probe[0], probe[1], probe[2]) == probe[3]:
            compatible.add(value)
    return frozenset(compatible)
def _domain_state(domain: frozenset[Trit], observed: Trit) -> RelationState:
    if not domain:
        return RelationState.CONTRADICTION
    if observed == 2:
        if domain == frozenset((2,)):
            return RelationState.OPEN
        determined = domain - {2}
        return RelationState.CLOSED if len(domain) == 1 and determined else RelationState.AMBIGUOUS
    if observed not in domain:
        return RelationState.CONTRADICTION
    if len(domain) == 1:
        return RelationState.OPEN if domain == frozenset((2,)) else RelationState.CLOSED
    return RelationState.AMBIGUOUS
def _state_e(state: RelationState) -> Trit:
    """Current document's C5 convention: 1 closes, 0 rejects, 2 opens."""
    if state is RelationState.CLOSED:
        return 1
    if state is RelationState.CONTRADICTION:
        return 0
    return 2
def _residual_e(operated: Triplet) -> Trit:
    residual = [value for value in operated if value != 2]
    return residual[0] if len(residual) == 1 else 2
@dataclass(frozen=True)
class Ordering:
    original: Triplet
    es: Trit
    fn: Trit
    fo: Trit
    o: Trit
    fn_index: int
    fo_index: int
    candidates: tuple[int, ...]
    valid: bool
def ordering_candidates(values: Sequence[Trit]) -> tuple[int, ...]:
    """Indices holding ES, excluding the ES-position self-reference."""
    values = triplet(values)
    es = majority3(*values)
    return tuple(i for i, value in enumerate(values) if value == es and i != es)
def _pick(candidates: Sequence[int], phase: Trit) -> int:
    if phase in candidates:
        return phase
    return min(candidates, key=lambda i: ((i - phase) % 3, i))
def order_triplet(values: Sequence[Trit], phase: Trit = 2) -> Ordering:
    """Assign ES/FN/FO using the stable phase inherited from DO.

    0-1-2 may emerge as a control signature but is impossible as a literal
    ordered closure.  The all-open triplet uses O=2 as iteration sentinel.
    """
    values, phase = triplet(values), trit(phase)
    es = majority3(*values)
    candidates = ordering_candidates(values)
    if values == OPEN:
        return Ordering(values, 2, 2, 2, 2, 2, 2, (2, 0, 1), False)
    if not candidates:
        return Ordering(values, es, values[es], 2, 2, es, 2, (), False)
    o = _pick(candidates, phase)
    fn_index = es
    fo_index = next(i for i in range(3) if i not in (o, fn_index))
    return Ordering(values, values[o], values[fn_index], values[fo_index],
                    o, fn_index, fo_index, candidates, True)
def operation_orientations(values: Sequence[Trit]) -> tuple[int, ...]:
    """Known O constraints, without inventing the pending global O table."""
    values = triplet(values)
    if values == OPEN:
        return 2, 0, 1
    if set(values) == TRITS:
        return 1, 2  # O=0 is the forbidden self-reference in this case.
    return ordering_candidates(values) or (2,)


@dataclass(frozen=True)
class Packet:
    r: Trit
    e: Trit
    o: Trit
    direction: Direction
    candidates: frozenset[Trit]
    state: RelationState
    resolved_target: Trit
    orientation_candidates: tuple[int, ...]

    @property
    def observable(self) -> Triplet:
        return self.r, self.e, self.o


def trigate(
    a: Trit,
    b: Trit,
    m: Trit,
    r: Trit | None = None,
    direction: Direction = Direction.INFER_R,
    phase: Trit = 2,
) -> Packet:
    """Execute or re-execute one TriGate without discarding inverse domains."""
    a, b, m = trit(a), trit(b), trit(m)
    predicted = majority3(a, b, m)
    r = predicted if r is None else trit(r)
    direction, phase = Direction(direction), trit(phase)
    domain = candidate_domain(a, b, m, r, direction)
    observed = {Direction.DEDUCE_B: b, Direction.INFER_R: r,
                Direction.LEARN_M: m}[direction]
    state = _domain_state(domain, observed)
    resolved = next(iter(domain)) if len(domain) == 1 else observed
    operated = (a, b, m)
    e = _residual_e(operated) if predicted == 2 else _state_e(state)
    orientations = operation_orientations(operated)
    o = _pick(orientations, phase)
    return Packet(predicted, e, o, direction, domain, state, resolved, orientations)


@dataclass(frozen=True)
class Knowledge:
    """The homoiconic knowledge triplet K=(DO,DE,DS)."""

    do: Triplet
    de: Triplet
    ds: Triplet

    def __post_init__(self) -> None:
        object.__setattr__(self, "do", triplet(self.do))
        object.__setattr__(self, "de", triplet(self.de))
        object.__setattr__(self, "ds", triplet(self.ds))

    @property
    def channels(self) -> tuple[Triplet, Triplet, Triplet]:
        return self.do, self.de, self.ds


EMPTY_KNOWLEDGE = Knowledge(OPEN, OPEN, OPEN)


@dataclass(frozen=True)
class FaceResult:
    inputs: tuple[Triplet, Triplet, Triplet]
    ordered: tuple[Ordering, Ordering, Ordering]
    triangle: tuple[Packet, Packet, Packet]
    groups: tuple[Packet, Packet, Packet]
    knowledge: Knowledge
    direction: Direction
    do_before: Triplet


def face(
    inputs: Sequence[Sequence[Trit]],
    direction: Direction = Direction.INFER_R,
    do_t: Sequence[Trit] = OPEN,
) -> FaceResult:
    """Order, triangularly interlace, emerge and project one Aurora face."""
    if len(inputs) != 3:
        raise AuroraError("a face requires exactly three input triplets")
    ps = tuple(triplet(p) for p in inputs)
    do_t, direction = triplet(do_t), Direction(direction)
    ordered = tuple(order_triplet(p, do_t[i]) for i, p in enumerate(ps))
    impossible = [o.original for o in ordered if not o.valid and o.original != OPEN]
    if impossible:
        raise AuroraError(f"literal closure has impossible ordering: {impossible!r}")

    fns = tuple(o.fn for o in ordered)
    fos = tuple(o.fo for o in ordered)
    t1 = trigate(fos[0], fos[1], fns[2], fos[2], direction, do_t[2])
    t2 = trigate(fos[1], fos[2], fns[0], fos[0], direction, do_t[0])
    t3 = trigate(fos[2], fos[0], fns[1], fos[1], direction, do_t[1])
    reconstructed = t2.r, t3.r, t1.r

    channels = (
        tuple(o.es for o in ordered),
        fns,
        reconstructed,
    )
    groups = tuple(
        trigate(*channel, direction=direction, phase=do_t[i])
        for i, channel in enumerate(channels)
    )
    knowledge = Knowledge(
        tuple(p.o for p in groups),
        tuple(p.e for p in groups),
        tuple(p.r for p in groups),
    )
    return FaceResult(ps, ordered, (t1, t2, t3), groups, knowledge,
                      direction, do_t)


def classify_de(de: Sequence[Trit]) -> RelationState:
    de = triplet(de)
    if de == (1, 1, 1):
        return RelationState.CLOSED
    if de == (0, 0, 0):
        return RelationState.CONTRADICTION
    if de == OPEN:
        return RelationState.OPEN
    return RelationState.TRANSIENT


@dataclass(frozen=True)
class Carry:
    """The complete open unit, not a reduced window result."""
    unit: Unit

    @property
    def reexecutes(self) -> bool:
        return reexecute(self.unit)


@dataclass(frozen=True)
class WindowResult:
    state: RelationState
    knowledge: Knowledge
    trace: tuple[FaceResult, ...]
    fixed_point: bool
    carry: Carry | None = None


def resolve_window(
    inputs: Sequence[Sequence[Trit]],
    direction: Direction = Direction.INFER_R,
    initial_do: Sequence[Trit] = OPEN,
    max_steps: int = 27,
) -> WindowResult:
    """Propagate DO snapshots until a fixed point, cycle, or explicit budget.

    This follows emergent DO only.  It intentionally does not fabricate the
    still-unspecified ternary-Fibonacci traversal.
    """
    if max_steps < 1:
        raise AuroraError("max_steps must be positive")
    current = triplet(initial_do)
    visited: set[Triplet] = set()
    trace: list[FaceResult] = []
    for _ in range(max_steps):
        result = face(inputs, direction, current)
        trace.append(result)
        nxt = result.knowledge.do
        if nxt == current:
            state = classify_de(result.knowledge.de)
            carried = Unit(result.knowledge,
                           tuple(Unit.leaf(value) for value in result.inputs),
                           result.direction, result.do_before)
            carry = Carry(carried) if state is RelationState.OPEN else None
            return WindowResult(state, result.knowledge, tuple(trace), True, carry)
        if nxt in visited:
            return WindowResult(RelationState.UNRESOLVED, result.knowledge,
                                tuple(trace), False)
        visited.add(current)
        current = nxt
    return WindowResult(RelationState.UNRESOLVED, trace[-1].knowledge,
                        tuple(trace), False)


@dataclass(frozen=True)
class Unit:
    """A fractal unit: full state plus the three units that produced it."""

    state: Knowledge
    children: tuple[Unit, ...] = ()
    direction: Direction = Direction.INFER_R
    do_before: Triplet = OPEN

    @classmethod
    def leaf(cls, value: Sequence[Trit]) -> Unit:
        return cls(Knowledge(OPEN, OPEN, triplet(value)))

    @property
    def value(self) -> Triplet:
        return self.state.ds


def synthesize(
    children: Sequence[Unit],
    direction: Direction = Direction.INFER_R,
    do_t: Sequence[Trit] = OPEN,
) -> Unit:
    if len(children) != 3:
        raise AuroraError("synthesis requires exactly three children")
    result = face(tuple(child.value for child in children), direction, do_t)
    return Unit(result.knowledge, tuple(children), Direction(direction), triplet(do_t))


def reexecute(unit: Unit) -> bool:
    if not unit.children:
        return True
    result = face(tuple(child.value for child in unit.children),
                  unit.direction, unit.do_before)
    return result.knowledge == unit.state and all(reexecute(c) for c in unit.children)


def ascend(units: Sequence[Unit], **kwargs: object) -> tuple[Unit, ...]:
    """Apply the same synthesis to consecutive groups of three."""
    if len(units) % 3:
        raise AuroraError("a complete fractal level needs a multiple of three units")
    return tuple(synthesize(units[i:i + 3], **kwargs) for i in range(0, len(units), 3))


def control_faces(
    input_unit: Unit,
    knowledge_unit: Unit,
    output_unit: Unit,
    direction: Direction = Direction.INFER_R,
    do_t: Sequence[Trit] = OPEN,
) -> object:
    """Build the emergent C4-C6 control without an external harmonizer."""
    from aurora_compact.control import control_faces as execute_control

    return execute_control(input_unit, knowledge_unit, output_unit,
                           direction, do_t)


@dataclass(frozen=True)
class Relation:
    """One dictionary branch: input, applicable knowledge and output."""

    input: Unit
    knowledge: Unit
    output: Unit
    direction: Direction = Direction.INFER_R
    successful_uses: int = 0
    last_success: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "direction", Direction(self.direction))

    def reexecutes_for(self, current: Unit) -> bool:
        """Verify provenance without assuming unfrozen context equivalence."""
        children = self.knowledge.children
        return (
            current == self.input
            and len(children) == 3
            and children[0] == current
            and children[1].state == EMPTY_KNOWLEDGE
            and children[2].value == self.output.value
            and reexecute(self.knowledge)
            and reexecute(self.output)
        )


@dataclass(frozen=True)
class AuroraDictionary:
    """Static lexicon plus competing input-knowledge-output relations."""

    entries: tuple[Relation, ...] = ()
    lexicon: tuple[Unit, ...] = ()

    def search(
        self,
        result_ds: Sequence[Trit],
        relation_direction: Direction | None = None,
        current: Unit | None = None,
        anchor_ds: Sequence[Trit] | None = None,
        mode_ds: Sequence[Trit] = OPEN,
    ) -> tuple[Relation, ...]:
        """Deduce stored tensors as B; never compare DS by equality.

        The default query uses A=R=result_ds and M=222.  Determined query
        coordinates therefore retrieve the same B value, while a query 2
        keeps that coordinate open.  Contextual validity is decided later by
        reexecution of the complete relation.
        """
        from aurora_compact.deduction import DeductiveQuery

        result_ds = triplet(result_ds)
        query = DeductiveQuery(
            result_ds if anchor_ds is None else triplet(anchor_ds),
            triplet(mode_ds),
            result_ds,
        )
        wanted = (None if relation_direction is None
                  else Direction(relation_direction))
        found = [r for r in self.entries
                 if query.accepts(r.input.value)
                 and (wanted is None or r.direction == wanted)]
        return tuple(sorted(found,
                            key=lambda r: (r.input == current,
                                           r.successful_uses, r.last_success),
                            reverse=True))

    def knows(self, unit: Unit) -> bool:
        return any(known == unit for known in self.lexicon)

    def register(self, *units: Unit) -> AuroraDictionary:
        lexicon = list(self.lexicon)
        lexicon.extend(unit for unit in units if unit not in lexicon)
        return AuroraDictionary(self.entries, tuple(lexicon))

    def add(self, relation: Relation) -> AuroraDictionary:
        return self.register(relation.input, relation.output)._with_relation(relation)

    def _with_relation(self, relation: Relation) -> AuroraDictionary:
        return AuroraDictionary(self.entries + (relation,), self.lexicon)

    def promote(self, selected: Relation, tick: int) -> AuroraDictionary:
        entries = list(self.entries)
        index = entries.index(selected)
        entries[index] = replace(
            selected,
            successful_uses=selected.successful_uses + 1,
            last_success=tick,
        )
        return AuroraDictionary(tuple(entries), self.lexicon)


class DictionaryBuilder:
    """Mutable creation phase; ``freeze`` ends it and yields static search."""

    def __init__(self) -> None:
        self._dictionary = AuroraDictionary()

    def add(self, relation: Relation) -> None:
        self._dictionary = self._dictionary.add(relation)

    def freeze(self) -> AuroraDictionary:
        return self._dictionary


class AttemptAction(Enum):
    REUSE_OUTPUT = "reuse_output"
    LEARN_KNOWLEDGE = "learn_knowledge"
    REJECT = "reject"


@dataclass(frozen=True)
class Attempt:
    number: int
    do: Triplet
    relation: Relation
    output_before: Unit
    output_after: Unit
    action: AttemptAction
    reexecuted: bool
    reason: str = ""


@dataclass(frozen=True)
class TranscendResult:
    state: RelationState
    output: Unit
    knowledge: Unit
    dictionary: AuroraDictionary
    trace: tuple[Attempt, ...]
    relation: Relation | None = None
    exhausted: bool = False


def derive_knowledge(
    input_unit: Unit, output_unit: Unit, do_t: Sequence[Trit] = OPEN
) -> Unit:
    """Resolve empty K through the ordinary face for (I, ⊥, S)."""
    empty = Unit(EMPTY_KNOWLEDGE)
    return synthesize((input_unit, empty, output_unit),
                      Direction.LEARN_M, do_t)


def transcend(
    input_unit: Unit,
    dictionary: AuroraDictionary,
    direction: Direction = Direction.INFER_R,
    initial_output: Unit | None = None,
    do_route: Sequence[Sequence[Trit]] = (OPEN,),
    tick: int = 0,
) -> TranscendResult:
    """Reuse K to change S, or preserve S and create a competing K.

    With no applicable relation the output reflects the input.  Knowledge is
    then derived by the same face used later, stored and verified by
    reexecution.  Every candidate and every new branch consumes one DO state.
    """
    direction = Direction(direction)
    output = input_unit if initial_output is None else initial_output
    route = tuple(triplet(state) for state in do_route)
    if not route or len(set(route)) != len(route):
        raise AuroraError("DO route must contain unique states and cannot be empty")
    from aurora_compact.deduction import DeductiveQuery

    lookup = DeductiveQuery.for_exact_tensor(input_unit.value)
    candidates = dictionary.search(
        lookup.result,
        direction,
        input_unit,
        lookup.anchor,
        lookup.mode,
    )
    attempts: list[Attempt] = []
    for number, (do_t, relation) in enumerate(zip(route, candidates), 1):
        verified = relation.reexecutes_for(input_unit)
        output_known = dictionary.knows(relation.output)
        action = (AttemptAction.REUSE_OUTPUT if verified and output_known
                  else AttemptAction.REJECT)
        attempts.append(Attempt(number, do_t, relation, output,
                                relation.output if action is AttemptAction.REUSE_OUTPUT
                                else output, action, verified,
                                "" if output_known else "output is not lexicalized"))
        if action is AttemptAction.REUSE_OUTPUT:
            updated = dictionary.promote(relation, tick or number)
            return TranscendResult(RelationState.CLOSED, relation.output,
                                   relation.knowledge, updated, tuple(attempts),
                                   relation)
    if len(attempts) >= len(route):
        return TranscendResult(RelationState.UNRESOLVED, output,
                               Unit(EMPTY_KNOWLEDGE), dictionary,
                               tuple(attempts), exhausted=True)
    if output != input_unit and not dictionary.knows(output):
        raise AuroraError("output must already be lexicalized or appear in input")
    do_t, number = route[len(attempts)], len(attempts) + 1
    knowledge = derive_knowledge(input_unit, output, do_t)
    learned = Relation(input_unit, knowledge, output, direction)
    updated = dictionary.add(learned)
    attempts.append(Attempt(number, do_t, learned, output, output,
                            AttemptAction.LEARN_KNOWLEDGE,
                            learned.reexecutes_for(input_unit)))
    return TranscendResult(RelationState.CLOSED, output, knowledge, updated,
                           tuple(attempts), learned)


@dataclass(frozen=True)
class FractalResult:
    root: Unit
    dictionary: AuroraDictionary
    levels: tuple[tuple[Unit, ...], ...]
    trace: tuple[TranscendResult, ...]


def process_fractal(
    tokens: Sequence[Sequence[Trit]], dictionary: AuroraDictionary | None = None,
    do_route: Sequence[Sequence[Trit]] = (OPEN,), tick: int = 0,
) -> FractalResult:
    """Repeat the same input-K-output dialogue at every complete 1-3-9 level."""
    level = tuple(Unit.leaf(value) for value in tokens)
    if not level or len(level) % 3:
        raise AuroraError("fractal processing needs a non-empty multiple of three")
    memory = AuroraDictionary() if dictionary is None else dictionary
    memory = memory.register(*level)
    levels, trace = [level], []
    while len(level) > 1:
        if len(level) % 3:
            raise AuroraError("each complete fractal level must divide by three")
        next_level: list[Unit] = []
        for children in (level[i:i + 3] for i in range(0, len(level), 3)):
            raw = synthesize(children)
            step = transcend(raw, memory, do_route=do_route,
                             tick=tick + len(trace))
            if step.state is not RelationState.CLOSED:
                raise AuroraError("fractal branch exhausted before closure")
            memory, output = step.dictionary, step.output
            next_level.append(output if output.children else raw)
            trace.append(step)
        level = tuple(next_level)
        levels.append(level)
    return FractalResult(level[0], memory, tuple(levels), tuple(trace))


def windows(items: Sequence[Unit]) -> Iterator[tuple[Unit, Unit, Unit]]:
    """Sliding windows of three, preserving level and order."""
    for i in range(len(items) - 2):
        yield items[i], items[i + 1], items[i + 2]


__all__ = [name for name in globals() if not name.startswith("_")]
