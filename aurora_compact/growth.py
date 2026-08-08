"""Horizontal carry and vertical synthesis for Aurora fractal streams.

The module adds no segmentation rule.  Every window contains three units and
is resolved by :func:`aurora.synthesize`, the same face used by the rest of the
kernel.  ``DE`` alone selects the movement:

* ``111`` closes and the relation ascends as one unit;
* ``000`` rejects the current grouping and slides the window;
* every open or transient value becomes a carry and joins the next two units.

A carry remains at the current semantic level even though it preserves the
three units that produced it.  A closed unit becomes an element of the next
level.  This is the horizontal/vertical distinction described by Aurora.

The historical :func:`grow_level` follows one left-to-right branch.
:func:`compete_level` starts that same operation at every source position,
keeps every closed relation, and lets all compatible non-overlapping
segmentations compete by recurrent dictionary priority.  Exact ties remain
explicit branches; there is no segmentation threshold or external grammar.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from itertools import product
from math import prod
from typing import Mapping, Sequence

from aurora_compact import aurora, characters


class GrowthAction(Enum):
    """The only three movements available to a sequence window."""

    ASCEND = "ascend"
    CARRY = "carry"
    SHIFT = "shift"


@dataclass(frozen=True)
class GrowthNode:
    """One unit at the current level and the source positions it preserves."""

    unit: aurora.Unit
    source_positions: tuple[int, ...]
    open: bool = False

    def __post_init__(self) -> None:
        if not self.source_positions:
            raise aurora.AuroraError("a growth node needs source positions")
        if tuple(sorted(set(self.source_positions))) != self.source_positions:
            raise aurora.AuroraError(
                "source positions must be unique and strictly ordered"
            )

    @classmethod
    def seed(cls, unit: aurora.Unit, position: int) -> GrowthNode:
        if position < 0:
            raise aurora.AuroraError("source positions cannot be negative")
        return cls(unit, (position,))

    @classmethod
    def combine(
        cls,
        unit: aurora.Unit,
        children: Sequence[GrowthNode],
        *,
        open: bool,
    ) -> GrowthNode:
        positions = tuple(
            position for child in children for position in child.source_positions
        )
        return cls(unit, positions, open)

    @property
    def span(self) -> tuple[int, int]:
        return self.source_positions[0], self.source_positions[-1] + 1

    @property
    def width(self) -> int:
        return len(self.source_positions)


@dataclass(frozen=True)
class WindowAttempt:
    """One re-executable decision over three nodes of the same level."""

    number: int
    inputs: tuple[GrowthNode, GrowthNode, GrowthNode]
    candidate: GrowthNode
    state: aurora.RelationState
    action: GrowthAction
    lexicalized: bool = False
    support: int = 0


@dataclass(frozen=True)
class LevelGrowth:
    """Result of moving once across a single semantic level."""

    level: int
    inputs: tuple[GrowthNode, ...]
    emerged: tuple[GrowthNode, ...]
    residual: tuple[GrowthNode, ...]
    attempts: tuple[WindowAttempt, ...]
    dictionary: aurora.AuroraDictionary

    @property
    def complete(self) -> bool:
        return not self.residual


@dataclass(frozen=True)
class FractalGrowth:
    """Repeated level growth until one root or an unresolved frontier remains."""

    initial: tuple[GrowthNode, ...]
    levels: tuple[LevelGrowth, ...]
    frontier: tuple[GrowthNode, ...]
    dictionary: aurora.AuroraDictionary

    @property
    def complete(self) -> bool:
        return len(self.frontier) == 1 and not self.frontier[0].open

    @property
    def root(self) -> GrowthNode | None:
        return self.frontier[0] if self.complete else None


@dataclass(frozen=True)
class TextGrowth:
    """The explicit character readings and their resulting fractal growth."""

    text: str
    readings: tuple[characters.CharacterTensor, ...]
    growth: FractalGrowth


@dataclass(frozen=True)
class ClosureCandidate:
    """One closed branch discovered from an overlapping source position.

    ``start`` and ``stop`` address units at the current level.  The complete
    character or token provenance remains in ``node.source_positions``.  A
    candidate's support is the support of its exact re-executable relation
    after every overlapping branch in the current observation has run.
    """

    number: int
    start: int
    stop: int
    node: GrowthNode
    attempts: tuple[WindowAttempt, ...]
    support: int = 0
    last_success: int = 0
    lexicalized: bool = False

    def __post_init__(self) -> None:
        if self.number < 1:
            raise aurora.AuroraError("candidate numbers start at one")
        if self.start < 0 or self.stop <= self.start:
            raise aurora.AuroraError("a closure needs a positive source interval")
        if not self.attempts:
            raise aurora.AuroraError("a closure needs a re-executable attempt trace")
        if self.attempts[-1].action is not GrowthAction.ASCEND:
            raise aurora.AuroraError("a closure trace must end by ascending")

    @property
    def item_width(self) -> int:
        return self.stop - self.start

    @property
    def source_width(self) -> int:
        return self.node.width

    @property
    def priority(self) -> tuple[int, int]:
        """Structural priority, without a weighted score or threshold."""
        return self.support, self.source_width


@dataclass(frozen=True)
class SegmentationHypothesis:
    """A compatible set of closures plus the units it leaves unresolved."""

    segments: tuple[ClosureCandidate, ...]
    residual: tuple[GrowthNode, ...]

    @property
    def emerged(self) -> tuple[GrowthNode, ...]:
        return tuple(segment.node for segment in self.segments)

    @property
    def complete(self) -> bool:
        return not self.residual

    @property
    def frontier(self) -> tuple[GrowthNode, ...]:
        return tuple(sorted((*self.emerged, *self.residual),
                            key=lambda node: node.span))

    @property
    def priority(self) -> tuple[tuple[tuple[int, int], ...], int]:
        """Compare recurrence first, then global structural compression.

        Candidate priorities are compared as an ordered multiset.  Thus one
        genuinely more recurrent closure outranks any number of accidental
        lower-priority closures.  Equal recurrence prefers the hypothesis
        that closes more source positions.  Exact ties stay tied; observation
        order is deliberately not a semantic tiebreaker.
        """
        priorities = tuple(sorted(
            (segment.priority for segment in self.segments), reverse=True
        ))
        coverage = sum(segment.source_width for segment in self.segments)
        return priorities, coverage


@dataclass(frozen=True)
class SegmentationCompetition:
    """Exhaustive overlapping candidates and the undominated hypotheses."""

    level: int
    inputs: tuple[GrowthNode, ...]
    candidates: tuple[ClosureCandidate, ...]
    winners: tuple[SegmentationHypothesis, ...]
    hypothesis_count: int
    attempts: tuple[WindowAttempt, ...]
    dictionary: aurora.AuroraDictionary

    @property
    def resolved(self) -> bool:
        return len(self.winners) == 1

    @property
    def selected(self) -> SegmentationHypothesis | None:
        return self.winners[0] if self.resolved else None

    @property
    def frontiers(self) -> tuple[tuple[GrowthNode, ...], ...]:
        return tuple(winner.frontier for winner in self.winners)


@dataclass(frozen=True)
class CompetitiveFractalGrowth:
    """Repeat overlapping competition while one complete branch wins."""

    initial: tuple[GrowthNode, ...]
    levels: tuple[SegmentationCompetition, ...]
    frontiers: tuple[tuple[GrowthNode, ...], ...]
    dictionary: aurora.AuroraDictionary

    @property
    def complete(self) -> bool:
        return (
            len(self.frontiers) == 1
            and len(self.frontiers[0]) == 1
            and not self.frontiers[0][0].open
        )

    @property
    def root(self) -> GrowthNode | None:
        return self.frontiers[0][0] if self.complete else None


@dataclass(frozen=True)
class CompetitiveTextGrowth:
    """Character readings and their overlapping fractal competition."""

    text: str
    readings: tuple[characters.CharacterTensor, ...]
    growth: CompetitiveFractalGrowth


@dataclass(frozen=True)
class ReadingHypothesis:
    """One complete assignment of character readings using ordinary growth.

    A reading is not scored by a separate classifier.  Its priority begins
    with active closures that contain each ambiguous source position, then
    uses the ordered segmentation priorities produced at every fractal level.
    Recurrence therefore acts before compression, a deeper closed level acts
    only after lower context ties, and exact ties remain genuinely ambiguous.
    """

    senses: tuple[tuple[int, str], ...]
    result: CompetitiveTextGrowth

    @property
    def readings(self) -> tuple[characters.CharacterTensor, ...]:
        return self.result.readings

    @property
    def growth(self) -> CompetitiveFractalGrowth:
        return self.result.growth

    @property
    def priority(
        self,
    ) -> tuple[
        tuple[tuple[tuple[int, int], ...], ...],
        tuple[tuple[tuple[tuple[int, int], ...], int], ...],
        int,
    ]:
        contextual_profiles: list[tuple[tuple[int, int], ...]] = []
        for position, _sense in self.senses:
            seen: set[tuple[int, int, int]] = set()
            priorities: list[tuple[int, int]] = []
            for level in self.growth.levels:
                for winner in level.winners:
                    for segment in winner.segments:
                        if position not in segment.node.source_positions:
                            continue
                        identity = (level.level, segment.start, segment.stop)
                        if identity in seen:
                            continue
                        seen.add(identity)
                        priorities.append(segment.priority)
            contextual_profiles.append(tuple(sorted(priorities, reverse=True)))

        levels = tuple(
            max(winner.priority for winner in level.winners)
            for level in self.growth.levels
            if level.winners
        )
        return (
            tuple(sorted(contextual_profiles, reverse=True)),
            levels,
            int(self.growth.complete),
        )


@dataclass(frozen=True)
class ContextualTextGrowth:
    """Competition between readings selected by the same fractal memory.

    ``selection`` records the downward pass that occurred before the surviving
    readings entered ordinary upward growth.  It is deliberately audit data,
    not a second score: its routes are exact re-executable dictionary closures.
    """

    text: str
    hypotheses: tuple[ReadingHypothesis, ...]
    winners: tuple[ReadingHypothesis, ...]
    selection: DownwardSelection

    def __post_init__(self) -> None:
        if not self.hypotheses:
            raise aurora.AuroraError("contextual growth needs a reading hypothesis")
        if not self.winners:
            raise aurora.AuroraError("contextual growth needs an active reading")
        if any(item not in self.hypotheses for item in self.winners):
            raise aurora.AuroraError("a reading winner must be a known hypothesis")

    @property
    def resolved(self) -> bool:
        return len(self.winners) == 1

    @property
    def selected(self) -> ReadingHypothesis | None:
        return self.winners[0] if self.resolved else None

    @property
    def growth(self) -> CompetitiveFractalGrowth:
        """Compatibility projection for a single available/selected reading."""
        selected = self.selected
        if selected is None:
            raise aurora.AuroraError(
                "contextual character readings remain ambiguous"
            )
        return selected.growth

    @property
    def readings(self) -> tuple[characters.CharacterTensor, ...]:
        selected = self.selected
        if selected is None:
            raise aurora.AuroraError(
                "contextual character readings remain ambiguous"
            )
        return selected.readings

    @property
    def winner_senses(self) -> tuple[tuple[tuple[int, str], ...], ...]:
        return tuple(item.senses for item in self.winners)

    @property
    def total_readings(self) -> int:
        return self.selection.total_readings

    @property
    def evaluated_readings(self) -> int:
        return len(self.hypotheses)

    @property
    def pruned_readings(self) -> int:
        return self.total_readings - self.evaluated_readings


DownwardPriority = tuple[tuple[tuple[int, int], ...], ...]


@dataclass(frozen=True)
class DownwardRoute:
    """One superior closure that selects compatible character descendants.

    The route is recovered from a relation's own fractal provenance.  Surface
    text and training evidence are absent: ``constraints`` contains only
    source positions and the senses whose stored tensors equal the relation's
    leaves at those positions.
    """

    start: int
    stop: int
    unit: aurora.Unit
    support: int
    last_success: int
    constraints: tuple[tuple[int, tuple[str, ...]], ...]

    def __post_init__(self) -> None:
        if self.start < 0 or self.stop <= self.start:
            raise aurora.AuroraError("a downward route needs a positive span")
        if self.support < 1:
            raise aurora.AuroraError("a downward route needs positive support")
        if not self.constraints:
            raise aurora.AuroraError(
                "a downward route must constrain an ambiguous descendant"
            )

    @property
    def source_width(self) -> int:
        return self.stop - self.start

    @property
    def priority(self) -> tuple[int, int]:
        """Reuse the same recurrence/width order as upward competition."""
        return self.support, self.source_width


@dataclass(frozen=True)
class DownwardAssignment:
    """One compatible assignment inside a connected contextual component."""

    senses: tuple[tuple[int, str], ...]
    priority: DownwardPriority


@dataclass(frozen=True)
class DownwardComponent:
    """Ambiguous positions connected by one or more superior closures."""

    positions: tuple[int, ...]
    options: tuple[tuple[int, tuple[str, ...]], ...]
    routes: tuple[DownwardRoute, ...]
    assignment_count: int
    winners: tuple[DownwardAssignment, ...]

    def __post_init__(self) -> None:
        if not self.positions or not self.winners:
            raise aurora.AuroraError(
                "a downward component needs positions and active assignments"
            )
        if self.assignment_count < len(self.winners):
            raise aurora.AuroraError(
                "active assignments cannot exceed the available component"
            )

    @property
    def closed(self) -> bool:
        return len(self.winners) < self.assignment_count

    @property
    def pruned_assignments(self) -> int:
        return self.assignment_count - len(self.winners)

    def active_senses(self, position: int) -> tuple[str, ...]:
        available = dict(self.options).get(position)
        if available is None:
            raise aurora.AuroraError(
                f"position {position} is outside the downward component"
            )
        active = {
            sense
            for winner in self.winners
            for current, sense in winner.senses
            if current == position
        }
        return tuple(sense for sense in available if sense in active)

    def position_closed(self, position: int) -> bool:
        return len(self.active_senses(position)) < len(dict(self.options)[position])


@dataclass(frozen=True)
class DownwardSelection:
    """Auditable selection from superior closures to inferior readings."""

    total_readings: int
    active_readings: int
    routes: tuple[DownwardRoute, ...]
    components: tuple[DownwardComponent, ...]
    enabled: bool = True

    def __post_init__(self) -> None:
        if self.total_readings < 1 or self.active_readings < 1:
            raise aurora.AuroraError("a reading space cannot be empty")
        if self.active_readings > self.total_readings:
            raise aurora.AuroraError(
                "active readings cannot exceed the complete reading space"
            )

    @property
    def pruned_readings(self) -> int:
        return self.total_readings - self.active_readings

    @property
    def activation_rate(self) -> float:
        return self.active_readings / self.total_readings

    @property
    def closed_positions(self) -> tuple[int, ...]:
        return tuple(
            position
            for component in self.components
            for position in component.positions
            if component.position_closed(position)
        )

    @property
    def open_positions(self) -> tuple[int, ...]:
        return tuple(
            position
            for component in self.components
            for position in component.positions
            if not component.position_closed(position)
        )


def _nodes(items: Sequence[aurora.Unit | GrowthNode]) -> tuple[GrowthNode, ...]:
    result: list[GrowthNode] = []
    for position, item in enumerate(items):
        result.append(
            item if isinstance(item, GrowthNode) else GrowthNode.seed(item, position)
        )
    positions = tuple(
        position for node in result for position in node.source_positions
    )
    if tuple(sorted(set(positions))) != positions:
        raise aurora.AuroraError("growth nodes must preserve source order")
    return tuple(result)


def _remember_closure(
    dictionary: aurora.AuroraDictionary,
    candidate: aurora.Unit,
    direction: aurora.Direction,
    do_t: aurora.Triplet,
    tick: int,
) -> tuple[aurora.AuroraDictionary, aurora.Unit, bool, int]:
    """Learn one re-executable closure or promote its existing relation.

    ``support`` counts successful observations, including genesis.  The
    underlying relation keeps the kernel convention in which
    ``successful_uses`` counts reuse after genesis.
    """
    known = next((
        relation for relation in dictionary.entries
        if relation.input == candidate
        and relation.output == candidate
        and relation.direction == direction
        and relation.reexecutes_for(candidate)
    ), None)
    if known is not None:
        updated = dictionary.promote(known, tick)
        return updated, known.output, True, known.successful_uses + 2

    knowledge = aurora.derive_knowledge(candidate, candidate, do_t)
    learned = aurora.Relation(candidate, knowledge, candidate, direction)
    return dictionary.add(learned), candidate, False, 1


def _closure_relation(
    dictionary: aurora.AuroraDictionary,
    candidate: aurora.Unit,
    direction: aurora.Direction,
) -> aurora.Relation:
    """Return the exact closure branch, never a colliding ``DS`` summary."""
    matches = tuple(
        relation for relation in dictionary.entries
        if relation.input == candidate
        and relation.output == candidate
        and relation.direction == direction
        and relation.reexecutes_for(candidate)
    )
    if len(matches) != 1:
        raise aurora.AuroraError(
            f"expected one exact closure relation; found {len(matches)}"
        )
    return matches[0]


def grow_level(
    items: Sequence[aurora.Unit | GrowthNode],
    dictionary: aurora.AuroraDictionary | None = None,
    *,
    level: int = 0,
    direction: aurora.Direction = aurora.Direction.INFER_R,
    do_t: Sequence[aurora.Trit] = aurora.OPEN,
    tick: int = 0,
) -> LevelGrowth:
    """Resolve consecutive ternary windows at one level.

    A carry replaces its three inputs at the front of the queue, so the next
    attempt is exactly ``(carry, next, next)``.  A contradiction removes only
    the first element from the active hypothesis and therefore slides the
    window without losing source provenance.
    """
    if level < 0:
        raise aurora.AuroraError("a fractal level cannot be negative")
    original = _nodes(items)
    queue = list(original)
    held: list[GrowthNode] = []
    emerged: list[GrowthNode] = []
    attempts: list[WindowAttempt] = []
    memory = aurora.AuroraDictionary() if dictionary is None else dictionary
    direction = aurora.Direction(direction)
    do_t = aurora.triplet(do_t)

    while len(queue) >= 3:
        window = tuple(queue[:3])
        units = tuple(node.unit for node in window)
        candidate_unit = aurora.synthesize(units, direction, do_t)
        state = aurora.classify_de(candidate_unit.state.de)

        if state is aurora.RelationState.CLOSED:
            memory, selected, lexicalized, support = _remember_closure(
                memory,
                candidate_unit,
                direction,
                do_t,
                tick + len(attempts) + 1,
            )
            candidate = GrowthNode.combine(
                selected,
                window,
                open=False,
            )
            emerged.append(candidate)
            del queue[:3]
            action = GrowthAction.ASCEND
        elif state is aurora.RelationState.CONTRADICTION:
            candidate = GrowthNode.combine(candidate_unit, window, open=True)
            held.append(queue.pop(0))
            lexicalized = False
            support = 0
            action = GrowthAction.SHIFT
        else:
            candidate = GrowthNode.combine(candidate_unit, window, open=True)
            queue[:3] = [candidate]
            lexicalized = False
            support = 0
            action = GrowthAction.CARRY

        attempts.append(WindowAttempt(
            len(attempts) + 1,
            window,  # type: ignore[arg-type]
            candidate,
            state,
            action,
            lexicalized,
            support,
        ))

    residual = tuple(sorted((*held, *queue), key=lambda node: node.span))
    return LevelGrowth(
        level,
        original,
        tuple(emerged),
        residual,
        tuple(attempts),
        memory,
    )


def _overlapping_closures(
    original: tuple[GrowthNode, ...],
    dictionary: aurora.AuroraDictionary,
    direction: aurora.Direction,
    do_t: aurora.Triplet,
    tick: int,
) -> tuple[
    tuple[ClosureCandidate, ...],
    tuple[WindowAttempt, ...],
    aurora.AuroraDictionary,
]:
    """Try every source start, extending only open branches by carry."""
    memory = dictionary
    candidates: list[ClosureCandidate] = []
    all_attempts: list[WindowAttempt] = []

    for start in range(max(0, len(original) - 2)):
        stop = start + 3
        window: tuple[GrowthNode, GrowthNode, GrowthNode] = (
            original[start], original[start + 1], original[start + 2]
        )
        branch_attempts: list[WindowAttempt] = []

        while True:
            candidate_unit = aurora.synthesize(
                tuple(node.unit for node in window), direction, do_t
            )
            state = aurora.classify_de(candidate_unit.state.de)
            candidate_node = GrowthNode.combine(
                candidate_unit,
                window,
                open=state is not aurora.RelationState.CLOSED,
            )

            if state is aurora.RelationState.CLOSED:
                memory, selected, lexicalized, support = _remember_closure(
                    memory,
                    candidate_unit,
                    direction,
                    do_t,
                    tick + len(all_attempts) + 1,
                )
                candidate_node = GrowthNode.combine(selected, window, open=False)
                action = GrowthAction.ASCEND
            elif state is aurora.RelationState.CONTRADICTION:
                lexicalized, support = False, 0
                action = GrowthAction.SHIFT
            else:
                lexicalized, support = False, 0
                action = GrowthAction.CARRY

            attempt = WindowAttempt(
                len(all_attempts) + 1,
                window,
                candidate_node,
                state,
                action,
                lexicalized,
                support,
            )
            branch_attempts.append(attempt)
            all_attempts.append(attempt)

            if action is GrowthAction.ASCEND:
                candidates.append(ClosureCandidate(
                    len(candidates) + 1,
                    start,
                    stop,
                    candidate_node,
                    tuple(branch_attempts),
                    support,
                    0,
                    lexicalized,
                ))
                break
            if action is GrowthAction.SHIFT or stop + 2 > len(original):
                break

            window = (
                candidate_node,
                original[stop],
                original[stop + 1],
            )
            stop += 2

    # Every occurrence of one relation competes with its final support for this
    # observation.  Recency remains audit data and never breaks a semantic tie.
    finalized: list[ClosureCandidate] = []
    for candidate in candidates:
        relation = _closure_relation(memory, candidate.node.unit, direction)
        finalized.append(replace(
            candidate,
            support=relation.successful_uses + 1,
            last_success=relation.last_success,
        ))
    return tuple(finalized), tuple(all_attempts), memory


def _competing_hypotheses(
    original: tuple[GrowthNode, ...],
    candidates: tuple[ClosureCandidate, ...],
) -> tuple[tuple[SegmentationHypothesis, ...], int]:
    """Select every best non-overlapping path through the candidate DAG.

    The dynamic program evaluates both possibilities at every source unit:
    preserve it as residual, or take any closure beginning there.  Only
    dominated complete paths are discarded; exact ties remain explicit.
    ``hypothesis_count`` records how many compatible paths were compared.
    """
    by_start: dict[int, list[ClosureCandidate]] = {}
    for candidate in candidates:
        by_start.setdefault(candidate.start, []).append(candidate)

    size = len(original)
    winners: list[tuple[SegmentationHypothesis, ...]] = [tuple()] * (size + 1)
    counts = [0] * (size + 1)
    winners[size] = (SegmentationHypothesis((), ()),)
    counts[size] = 1

    for position in range(size - 1, -1, -1):
        options: list[SegmentationHypothesis] = []
        counts[position] = counts[position + 1]

        for suffix in winners[position + 1]:
            options.append(SegmentationHypothesis(
                suffix.segments,
                (original[position], *suffix.residual),
            ))

        for candidate in by_start.get(position, ()):  # type: ignore[arg-type]
            counts[position] += counts[candidate.stop]
            for suffix in winners[candidate.stop]:
                options.append(SegmentationHypothesis(
                    (candidate, *suffix.segments),
                    suffix.residual,
                ))

        best = max(option.priority for option in options)
        winners[position] = tuple(
            option for option in options if option.priority == best
        )

    return winners[0], counts[0]


def compete_level(
    items: Sequence[aurora.Unit | GrowthNode],
    dictionary: aurora.AuroraDictionary | None = None,
    *,
    level: int = 0,
    direction: aurora.Direction = aurora.Direction.INFER_R,
    do_t: Sequence[aurora.Trit] = aurora.OPEN,
    tick: int = 0,
) -> SegmentationCompetition:
    """Learn all overlapping closures and let compatible paths compete.

    No candidate is deleted when it loses.  The dictionary preserves every
    exact branch, while the returned winners identify only the structure that
    may currently ascend.  Multiple winners mean contextual ambiguity.
    """
    if level < 0:
        raise aurora.AuroraError("a fractal level cannot be negative")
    original = _nodes(items)
    memory = aurora.AuroraDictionary() if dictionary is None else dictionary
    direction = aurora.Direction(direction)
    do_t = aurora.triplet(do_t)
    candidates, attempts, memory = _overlapping_closures(
        original, memory, direction, do_t, tick
    )
    winners, hypothesis_count = _competing_hypotheses(original, candidates)
    return SegmentationCompetition(
        level,
        original,
        candidates,
        winners,
        hypothesis_count,
        attempts,
        memory,
    )


def compete_fractal(
    items: Sequence[aurora.Unit | GrowthNode],
    dictionary: aurora.AuroraDictionary | None = None,
    *,
    direction: aurora.Direction = aurora.Direction.INFER_R,
    do_t: Sequence[aurora.Trit] = aurora.OPEN,
    tick: int = 0,
) -> CompetitiveFractalGrowth:
    """Ascend only while competition yields one complete segmentation."""
    initial = _nodes(items)
    current = initial
    memory = aurora.AuroraDictionary() if dictionary is None else dictionary
    levels: list[SegmentationCompetition] = []
    level = 0

    while len(current) >= 3:
        result = compete_level(
            current,
            memory,
            level=level,
            direction=direction,
            do_t=do_t,
            tick=tick + sum(len(previous.attempts) for previous in levels),
        )
        levels.append(result)
        memory = result.dictionary
        selected = result.selected
        if selected is None or not selected.complete:
            return CompetitiveFractalGrowth(
                initial, tuple(levels), result.frontiers, memory
            )
        current = selected.emerged
        level += 1

    return CompetitiveFractalGrowth(
        initial, tuple(levels), (current,), memory
    )


def grow_fractal(
    items: Sequence[aurora.Unit | GrowthNode],
    dictionary: aurora.AuroraDictionary | None = None,
    *,
    direction: aurora.Direction = aurora.Direction.INFER_R,
    do_t: Sequence[aurora.Trit] = aurora.OPEN,
    tick: int = 0,
) -> FractalGrowth:
    """Repeat :func:`grow_level` while the whole frontier can ascend.

    Aurora does not combine across an unresolved gap.  If a level leaves a
    residual, growth pauses with that mixed frontier; more context or another
    learned candidate may resume it later.
    """
    initial = _nodes(items)
    current = initial
    memory = aurora.AuroraDictionary() if dictionary is None else dictionary
    levels: list[LevelGrowth] = []
    level = 0

    while len(current) >= 3:
        result = grow_level(
            current,
            memory,
            level=level,
            direction=direction,
            do_t=do_t,
            tick=tick + sum(len(previous.attempts) for previous in levels),
        )
        levels.append(result)
        memory = result.dictionary
        if result.residual:
            frontier = tuple(sorted(
                (*result.emerged, *result.residual), key=lambda node: node.span
            ))
            return FractalGrowth(initial, tuple(levels), frontier, memory)
        current = result.emerged
        level += 1

    return FractalGrowth(initial, tuple(levels), current, memory)


def character_options(
    text: str,
    lexicon: characters.CharacterLexicon | None = None,
    senses: Mapping[int, str] | None = None,
) -> tuple[tuple[characters.CharacterTensor, ...], ...]:
    """Return every admissible tensor reading at every source position.

    An explicit sense restricts one position to validated experience.  Without
    one, all registered alternatives remain available; insertion order never
    acts as an implicit interpretation.
    """
    lexicon = characters.spanish_character_lexicon() if lexicon is None else lexicon
    senses = {} if senses is None else senses
    options_by_position: list[tuple[characters.CharacterTensor, ...]] = []
    for position, symbol in enumerate(text):
        options = lexicon.lookup(symbol)
        if not options:
            raise aurora.AuroraError(
                f"no character tensor is registered for {symbol!r} at {position}"
            )
        requested = senses.get(position)
        if requested is not None:
            options = tuple(item for item in options if item.sense == requested)
            if not options:
                raise aurora.AuroraError(
                    f"sense {requested!r} is not registered for {symbol!r} "
                    f"at {position}"
                )
        options_by_position.append(options)
    return tuple(options_by_position)


def character_readings(
    text: str,
    lexicon: characters.CharacterLexicon | None = None,
    senses: Mapping[int, str] | None = None,
) -> tuple[characters.CharacterTensor, ...]:
    """Resolve one explicit tensor reading for every character.

    This compatibility entry point remains strict.  Use
    :func:`compete_contextual_text` to let all readings enter Aurora's ordinary
    fractal competition.
    """
    options_by_position = character_options(text, lexicon, senses)
    readings: list[characters.CharacterTensor] = []
    for position, options in enumerate(options_by_position):
        if len(options) != 1:
            available = ", ".join(sorted(item.sense for item in options))
            raise aurora.AuroraError(
                f"character {text[position]!r} at {position} remains ambiguous: "
                f"{available}"
            )
        readings.append(options[0])
    return tuple(readings)


def grow_text(
    text: str,
    lexicon: characters.CharacterLexicon | None = None,
    senses: Mapping[int, str] | None = None,
    dictionary: aurora.AuroraDictionary | None = None,
    *,
    tick: int = 0,
) -> TextGrowth:
    """Materialize character tensors and grow them with the ordinary window."""
    readings = character_readings(text, lexicon, senses)
    nodes = tuple(GrowthNode.seed(item.unit, position)
                  for position, item in enumerate(readings))
    return TextGrowth(text, readings, grow_fractal(nodes, dictionary, tick=tick))


def compete_text(
    text: str,
    lexicon: characters.CharacterLexicon | None = None,
    senses: Mapping[int, str] | None = None,
    dictionary: aurora.AuroraDictionary | None = None,
    *,
    tick: int = 0,
) -> CompetitiveTextGrowth:
    """Materialize a text and run overlapping competition at every level."""
    readings = character_readings(text, lexicon, senses)
    nodes = tuple(GrowthNode.seed(item.unit, position)
                  for position, item in enumerate(readings))
    return CompetitiveTextGrowth(
        text,
        readings,
        compete_fractal(nodes, dictionary, tick=tick),
    )


def _character_leaves(
    unit: aurora.Unit,
    lexical_units: frozenset[aurora.Unit],
) -> tuple[aurora.Unit, ...] | None:
    """Descend one learned unit until registered character tensors are found."""
    if unit in lexical_units:
        return (unit,)
    if not unit.children:
        return None
    leaves: list[aurora.Unit] = []
    for child in unit.children:
        branch = _character_leaves(child, lexical_units)
        if branch is None:
            return None
        leaves.extend(branch)
    return tuple(leaves)


def _downward_routes(
    options_by_position: tuple[tuple[characters.CharacterTensor, ...], ...],
    dictionary: aurora.AuroraDictionary,
    lexicon: characters.CharacterLexicon,
) -> tuple[DownwardRoute, ...]:
    """Match re-executable superior closures against open inferior tensors.

    Matching uses unit identity and provenance only.  A relation may span a
    three-character face, an extended carry, or a higher fractal closure; the
    descent treats all of them identically after recovering their character
    leaves.
    """
    ambiguous = frozenset(
        position for position, options in enumerate(options_by_position)
        if len(options) > 1
    )
    if not ambiguous:
        return ()
    lexical_units = frozenset(item.unit for item in lexicon.entries)
    routes: list[DownwardRoute] = []
    size = len(options_by_position)
    for relation in dictionary.entries:
        if (
            relation.direction is not aurora.Direction.INFER_R
            or relation.input != relation.output
            or not relation.reexecutes_for(relation.input)
        ):
            continue
        leaves = _character_leaves(relation.input, lexical_units)
        if not leaves or len(leaves) > size:
            continue
        width = len(leaves)
        for start in range(size - width + 1):
            if any(
                all(option.unit != leaf for option in options_by_position[start + offset])
                for offset, leaf in enumerate(leaves)
            ):
                continue
            constraints: list[tuple[int, tuple[str, ...]]] = []
            for offset, leaf in enumerate(leaves):
                position = start + offset
                if position not in ambiguous:
                    continue
                senses = tuple(
                    option.sense
                    for option in options_by_position[position]
                    if option.unit == leaf
                )
                if senses:
                    constraints.append((position, senses))
            if constraints:
                routes.append(DownwardRoute(
                    start,
                    start + width,
                    relation.input,
                    relation.successful_uses + 1,
                    relation.last_success,
                    tuple(constraints),
                ))
    return tuple(routes)


def _position_components(
    ambiguous: tuple[int, ...],
    routes: tuple[DownwardRoute, ...],
) -> tuple[tuple[int, ...], ...]:
    """Return connected ambiguous positions without building a global product."""
    parent = {position: position for position in ambiguous}

    def find(position: int) -> int:
        while parent[position] != position:
            parent[position] = parent[parent[position]]
            position = parent[position]
        return position

    def union(left: int, right: int) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for route in routes:
        positions = tuple(position for position, _ in route.constraints)
        for position in positions[1:]:
            union(positions[0], position)

    grouped: dict[int, list[int]] = {}
    for position in ambiguous:
        grouped.setdefault(find(position), []).append(position)
    return tuple(
        tuple(positions)
        for _, positions in sorted(grouped.items(), key=lambda item: item[1][0])
    )


def _route_accepts(
    route: DownwardRoute,
    assignment: Mapping[int, characters.CharacterTensor],
) -> bool:
    return all(
        assignment[position].sense in senses
        for position, senses in route.constraints
    )


def _downward_component(
    positions: tuple[int, ...],
    options_by_position: tuple[tuple[characters.CharacterTensor, ...], ...],
    routes: tuple[DownwardRoute, ...],
) -> DownwardComponent:
    component_routes = tuple(
        route for route in routes
        if any(position in positions for position, _ in route.constraints)
    )
    assignments: list[DownwardAssignment] = []
    for choices in product(*(options_by_position[position] for position in positions)):
        assignment = dict(zip(positions, choices))
        compatible = tuple(
            route for route in component_routes
            if _route_accepts(route, assignment)
        )
        contextual_profiles = tuple(
            tuple(sorted(
                (
                    route.priority for route in compatible
                    if any(current == position
                           for current, _ in route.constraints)
                ),
                reverse=True,
            ))
            for position in positions
        )
        priority: DownwardPriority = tuple(
            sorted(contextual_profiles, reverse=True)
        )
        assignments.append(DownwardAssignment(
            tuple((position, assignment[position].sense)
                  for position in positions),
            priority,
        ))

    best = max(item.priority for item in assignments)
    winners = tuple(item for item in assignments if item.priority == best)
    options = tuple(
        (position, tuple(item.sense for item in options_by_position[position]))
        for position in positions
    )
    return DownwardComponent(
        positions,
        options,
        component_routes,
        len(assignments),
        winners,
    )


def _selected_readings(
    options_by_position: tuple[tuple[characters.CharacterTensor, ...], ...],
    routes: tuple[DownwardRoute, ...],
) -> tuple[
    tuple[DownwardComponent, ...],
    tuple[tuple[characters.CharacterTensor, ...], ...],
]:
    ambiguous = tuple(
        position for position, options in enumerate(options_by_position)
        if len(options) > 1
    )
    components = tuple(
        _downward_component(positions, options_by_position, routes)
        for positions in _position_components(ambiguous, routes)
    )
    if not components:
        return (), (tuple(options[0] for options in options_by_position),)

    readings: list[tuple[characters.CharacterTensor, ...]] = []
    for component_choices in product(*(item.winners for item in components)):
        selected_senses = {
            position: sense
            for choice in component_choices
            for position, sense in choice.senses
        }
        reading: list[characters.CharacterTensor] = []
        for position, options in enumerate(options_by_position):
            selected = selected_senses.get(position)
            if selected is None:
                reading.append(options[0])
                continue
            matches = tuple(item for item in options if item.sense == selected)
            if len(matches) != 1:
                raise aurora.AuroraError(
                    f"downward selection did not identify one tensor at {position}"
                )
            reading.append(matches[0])
        readings.append(tuple(reading))
    return components, tuple(readings)


def compete_contextual_text(
    text: str,
    lexicon: characters.CharacterLexicon | None = None,
    senses: Mapping[int, str] | None = None,
    dictionary: aurora.AuroraDictionary | None = None,
    *,
    tick: int = 0,
    downward: bool = True,
) -> ContextualTextGrowth:
    """Select downward, then let active readings repeat ordinary upward growth.

    Stored superior closures are first descended to their character tensors.
    They connect only the ambiguous positions they actually contain, so
    independent regions never require a global Cartesian product.  Exact ties
    remain active.  The surviving branches then start from the same immutable
    dictionary and execute :func:`compete_fractal` unchanged.

    ``downward=False`` retains the exhaustive 0.10 path for audits.  It must
    produce the same winners whenever the learned closures determine a unique
    route, but it intentionally performs every complete reading.
    """
    lexicon = characters.spanish_character_lexicon() if lexicon is None else lexicon
    options_by_position = character_options(text, lexicon, senses)
    ambiguous_positions = tuple(
        position for position, options in enumerate(options_by_position)
        if len(options) > 1
    )
    memory = aurora.AuroraDictionary() if dictionary is None else dictionary
    total_readings = prod(len(options) for options in options_by_position)
    routes = (
        _downward_routes(options_by_position, memory, lexicon)
        if downward else ()
    )
    components, active_readings = _selected_readings(
        options_by_position, routes
    )
    selection = DownwardSelection(
        total_readings,
        len(active_readings),
        routes,
        components,
        downward,
    )
    hypotheses: list[ReadingHypothesis] = []
    for readings in active_readings:
        nodes = tuple(
            GrowthNode.seed(item.unit, position)
            for position, item in enumerate(readings)
        )
        result = CompetitiveTextGrowth(
            text,
            tuple(readings),
            compete_fractal(nodes, memory, tick=tick),
        )
        hypotheses.append(ReadingHypothesis(
            tuple((position, readings[position].sense)
                  for position in ambiguous_positions),
            result,
        ))

    best = max(item.priority for item in hypotheses)
    winners = tuple(item for item in hypotheses if item.priority == best)
    return ContextualTextGrowth(
        text,
        tuple(hypotheses),
        winners,
        selection,
    )


__all__ = [
    "ClosureCandidate",
    "CompetitiveFractalGrowth",
    "CompetitiveTextGrowth",
    "ContextualTextGrowth",
    "DownwardAssignment",
    "DownwardComponent",
    "DownwardRoute",
    "DownwardSelection",
    "FractalGrowth",
    "GrowthAction",
    "GrowthNode",
    "LevelGrowth",
    "SegmentationCompetition",
    "SegmentationHypothesis",
    "ReadingHypothesis",
    "TextGrowth",
    "WindowAttempt",
    "character_options",
    "character_readings",
    "compete_contextual_text",
    "compete_fractal",
    "compete_level",
    "compete_text",
    "grow_fractal",
    "grow_level",
    "grow_text",
]
