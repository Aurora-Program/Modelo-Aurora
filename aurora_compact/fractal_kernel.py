"""Release-candidate fractal passage and three-index Aurora memory.

The module freezes one rule for every scale:

``C -> read K[C] -> O=DO[C] -> C(next)``

``K`` is never reduced or rebuilt while it moves.  A topology contains three
ordinary output ports indexed by ``O``.  Selecting a port can therefore place
the same unit in a same-scale cell, an upper-scale cell, or preserve several
destinations while the orientation remains open.  The runtime does not carry
an action table for those interpretations.

The dictionary stores each complete ``Unit(K)`` once.  ``C`` selects one of
its three existing projections -- ``DO``, ``DE`` or ``DS`` -- as the lookup
index.  A successful lookup returns the complete unit, so orientation,
closure knowledge and synthesized information are three entrances to the same
causal object rather than three duplicated dictionaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from . import aurora, deduction, relational


@dataclass(frozen=True)
class FractalAddress:
    """One tensor-native destination in the presentation graph."""

    scale: aurora.Triplet
    cell: aurora.Triplet

    def __post_init__(self) -> None:
        object.__setattr__(self, "scale", aurora.triplet(self.scale))
        object.__setattr__(self, "cell", aurora.triplet(self.cell))


@dataclass(frozen=True)
class FractalTopology:
    """Three output ports selected directly by an Aurora orientation."""

    ports: tuple[
        tuple[FractalAddress, ...],
        tuple[FractalAddress, ...],
        tuple[FractalAddress, ...],
    ]

    def __post_init__(self) -> None:
        if len(self.ports) != 3 or any(not port for port in self.ports):
            raise aurora.AuroraError(
                "a fractal topology needs three non-empty orientation ports"
            )
        for port in self.ports:
            if len(tuple(dict.fromkeys(port))) != len(port):
                raise aurora.AuroraError(
                    "one orientation port cannot duplicate a destination"
                )

    def destinations(self, orientations: Sequence[aurora.Trit]) -> tuple[FractalAddress, ...]:
        """Return every destination retained by the supplied orientations."""

        selected = tuple(
            address
            for orientation in orientations
            for address in self.ports[aurora.trit(orientation)]
        )
        return tuple(dict.fromkeys(selected))


@dataclass(frozen=True)
class TripletPassage:
    """One triplet routed by the same ``O`` that determines its ``ES``."""

    value: aurora.Triplet
    phase: aurora.Trit
    orientations: tuple[aurora.Trit, ...]
    destinations: tuple[FractalAddress, ...]

    @property
    def resolved(self) -> bool:
        return len(self.orientations) == 1


def pass_triplet(
    value: Sequence[aurora.Trit],
    topology: FractalTopology,
    phase: aurora.Trit = 2,
) -> TripletPassage:
    """Route a triplet without adding a second movement classifier."""

    value = aurora.triplet(value)
    phase = aurora.trit(phase)
    ordering = aurora.order_triplet(value, phase)
    orientations = (
        (ordering.o,)
        if ordering.valid
        else tuple(aurora.operation_orientations(value))
    )
    return TripletPassage(
        value,
        phase,
        orientations,
        topology.destinations(orientations),
    )


@dataclass(frozen=True)
class UnitPassage:
    """The same complete unit presented to destinations selected by ``C-O``."""

    unit: aurora.Unit
    incoming: aurora.Direction
    outgoing: aurora.Trit
    destinations: tuple[FractalAddress, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "incoming", aurora.Direction(self.incoming))
        object.__setattr__(self, "outgoing", aurora.trit(self.outgoing))
        if not aurora.reexecute(self.unit):
            raise aurora.AuroraError("a passed Aurora unit must re-execute")
        if self.outgoing != self.unit.state.do[int(self.incoming)]:
            raise aurora.AuroraError("the outgoing orientation must be DO[C]")
        if not self.destinations:
            raise aurora.AuroraError("a unit passage must retain a destination")

    @property
    def next_c(self) -> aurora.Direction:
        """``O`` becomes the incoming ``C`` of the next presentation."""

        return aurora.Direction(self.outgoing)

    @property
    def resolved(self) -> bool:
        return len(self.destinations) == 1

    @property
    def deliveries(self) -> tuple[tuple[FractalAddress, aurora.Unit], ...]:
        """Preserve object identity across every still-valid destination."""

        return tuple((destination, self.unit) for destination in self.destinations)


@dataclass(frozen=True)
class OrientedBoundary:
    """The rc1 scale boundary that presents one complete unit through ``C-O``.

    ``FractalWindow`` below supersedes this three-closed-input prototype.  The
    boundary remains available because its identity-preserving ``C -> O``
    passage is still a useful primitive and an rc1 regression.
    """

    topology: FractalTopology
    phase: aurora.Triplet = aurora.OPEN

    def __post_init__(self) -> None:
        object.__setattr__(self, "phase", aurora.triplet(self.phase))

    def pass_unit(
        self,
        unit: aurora.Unit,
        incoming: aurora.Direction,
    ) -> UnitPassage:
        incoming = aurora.Direction(incoming)
        outgoing = unit.state.do[int(incoming)]
        return UnitPassage(
            unit,
            incoming,
            outgoing,
            self.topology.destinations((outgoing,)),
        )

    def resolve(
        self,
        children: Sequence[aurora.Unit],
        incoming: aurora.Direction,
    ) -> UnitPassage:
        """Synthesize three children, then pass that same unit at the boundary."""

        incoming = aurora.Direction(incoming)
        unit = aurora.synthesize(children, incoming, self.phase)
        return self.pass_unit(unit, incoming)


def open_unit() -> aurora.Unit:
    """Return a fresh complete tensor ``2``: ``K=(222,222,222)``."""

    return aurora.Unit(aurora.EMPTY_KNOWLEDGE)


@dataclass(frozen=True)
class FractalWindow:
    """One TriGate-shaped tensor window ``(A, B, 2)``.

    ``A`` and ``B`` are the two available tensors.  ``result`` is a fresh
    complete open tensor and occupies the result position that the ordinary
    Aurora face must evolve.  The evolved result may continue as carry.  It
    is not the superior unit: on closure a second application of the same
    face makes the complete relation ``(A,B,result_evolved)`` emerge.
    """

    a: aurora.Unit
    b: aurora.Unit
    result: aurora.Unit
    phase: aurora.Triplet = aurora.OPEN

    def __post_init__(self) -> None:
        object.__setattr__(self, "phase", aurora.triplet(self.phase))
        if not all(aurora.reexecute(unit) for unit in (self.a, self.b, self.result)):
            raise aurora.AuroraError("every tensor-window slot must re-execute")
        if self.result.state != aurora.EMPTY_KNOWLEDGE or self.result.children:
            raise aurora.AuroraError(
                "the result position of a new tensor window must be a leaf tensor 2"
            )

    @classmethod
    def open(
        cls,
        a: aurora.Unit,
        b: aurora.Unit,
        phase: Sequence[aurora.Trit] = aurora.OPEN,
    ) -> FractalWindow:
        """Open a new result position for two tensors at the same scale."""

        return cls(a, b, open_unit(), aurora.triplet(phase))

    @property
    def slots(self) -> tuple[aurora.Unit, aurora.Unit, aurora.Unit]:
        return self.a, self.b, self.result

    def deduce(self) -> WindowResolution:
        """Evolve tensor ``2`` and apply the three autosimilar outcomes."""

        evolved = aurora.synthesize(
            self.slots,
            aurora.Direction.INFER_R,
            self.phase,
        )
        closure = aurora.majority3(*evolved.state.de)

        # At every scale R=2 remains open.  Its E trits retain residual
        # information and therefore must not be mistaken for contradiction.
        if evolved.value == aurora.OPEN:
            state = aurora.RelationState.OPEN
        elif not aurora.order_triplet(evolved.value).valid:
            # A determined but non-orderable result (such as 012 or 102) cannot
            # become a superior tensor even if DE carries a positive vote.
            state = aurora.RelationState.CONTRADICTION
        elif closure == 1:
            state = aurora.RelationState.CLOSED
        elif closure == 0:
            state = aurora.RelationState.CONTRADICTION
        else:
            state = aurora.RelationState.OPEN

        emergent = None
        if state is aurora.RelationState.CLOSED:
            # The evolved tensor is the completed third position.  The unit
            # promoted above is the relation of A, B and that completed
            # position, not the completed position by itself.
            emergent = aurora.synthesize(
                (self.a, self.b, evolved),
                aurora.Direction.INFER_R,
                evolved.state.do,
            )
        return WindowResolution(self, evolved, state, emergent)


@dataclass(frozen=True)
class WindowResolution:
    """Structural consequence of evolving tensor ``2`` in ``(A,B,2)``.

    On closure the superior unit is the emergence of ``(A,B,2_evolved)``.
    When ambiguity remains, ``2_evolved`` itself is retained for the next
    same-scale window.  On contradiction ``A`` is already the coherent unit
    and ``B`` is retained.  No reduced carry type is created.
    """

    window: FractalWindow
    evolved: aurora.Unit
    state: aurora.RelationState
    emergent: aurora.Unit | None = None

    def __post_init__(self) -> None:
        if self.state not in (
            aurora.RelationState.CLOSED,
            aurora.RelationState.OPEN,
            aurora.RelationState.CONTRADICTION,
        ):
            raise aurora.AuroraError("a tensor window has only three stable outcomes")
        if self.evolved.children != self.window.slots:
            raise aurora.AuroraError("evolved tensor 2 must preserve A, B and tensor 2")
        if not aurora.reexecute(self.evolved):
            raise aurora.AuroraError("an evolved tensor 2 must re-execute")
        if self.state is aurora.RelationState.CLOSED:
            if self.emergent is None:
                raise aurora.AuroraError("a coherent window must produce an emergence")
            if self.emergent.children != (
                self.window.a,
                self.window.b,
                self.evolved,
            ):
                raise aurora.AuroraError(
                    "window emergence must preserve A, B and evolved tensor 2"
                )
            if not aurora.reexecute(self.emergent):
                raise aurora.AuroraError("a superior window emergence must re-execute")
        elif self.emergent is not None:
            raise aurora.AuroraError(
                "an open or incoherent window cannot publish a relation emergence"
            )

    @property
    def superior(self) -> aurora.Unit | None:
        if self.state is aurora.RelationState.CLOSED:
            return self.emergent
        if self.state is aurora.RelationState.CONTRADICTION:
            return self.window.a
        return None

    @property
    def carry(self) -> aurora.Unit | None:
        if self.state is aurora.RelationState.OPEN:
            return self.evolved
        if self.state is aurora.RelationState.CONTRADICTION:
            return self.window.b
        return None

    def continue_with(self, following: aurora.Unit) -> FractalWindow:
        """Build ``(carry, following, new 2)`` and inherit the carry's ``O``."""

        if self.carry is None:
            raise aurora.AuroraError(
                "a closed tensor window starts afresh from two following tensors"
            )
        return FractalWindow.open(self.carry, following, self.carry.state.do)


@dataclass(frozen=True)
class WindowLevel:
    """One left-to-right application of the corrected window law."""

    inputs: tuple[aurora.Unit, ...]
    superior: tuple[aurora.Unit, ...]
    residual: tuple[aurora.Unit, ...]
    attempts: tuple[WindowResolution, ...]

    @property
    def complete(self) -> bool:
        return not self.residual


def resolve_level(
    items: Sequence[aurora.Unit],
    phase: Sequence[aurora.Trit] = aurora.OPEN,
) -> WindowLevel:
    """Resolve a stream using only ``(A,B,2)`` windows.

    Closure consumes ``A`` and ``B`` and publishes the emergence of
    ``(A,B,2_evolved)`` above.  Openness retains the complete evolved tensor
    ``2`` as carry.  Contradiction publishes ``A`` and retains ``B``.  A
    continuation consumes exactly one new source tensor because its third
    position is always a fresh tensor ``2``.
    """

    original = tuple(items)
    if not all(aurora.reexecute(unit) for unit in original):
        raise aurora.AuroraError("a tensor-window stream must be re-executable")
    pending = list(original)
    retained: aurora.Unit | None = None
    superior: list[aurora.Unit] = []
    attempts: list[WindowResolution] = []
    phase = aurora.triplet(phase)

    while True:
        if retained is None:
            if len(pending) < 2:
                break
            a, b = pending.pop(0), pending.pop(0)
            window_phase = phase
        else:
            if not pending:
                break
            a, b = retained, pending.pop(0)
            window_phase = retained.state.do
            retained = None

        attempt = FractalWindow.open(a, b, window_phase).deduce()
        attempts.append(attempt)
        if attempt.superior is not None:
            superior.append(attempt.superior)
        retained = attempt.carry

    residual = (() if retained is None else (retained,)) + tuple(pending)
    return WindowLevel(original, tuple(superior), residual, tuple(attempts))


@dataclass(frozen=True)
class TensorNode:
    """One complete Aurora unit and the three units that promoted it."""

    unit: aurora.Unit
    level: int = 0
    children: tuple[TensorNode, ...] = ()

    def __post_init__(self) -> None:
        if self.level < 0:
            raise aurora.AuroraError("a tensor dictionary level cannot be negative")
        if not aurora.reexecute(self.unit):
            raise aurora.AuroraError("a tensor dictionary unit must re-execute")
        if not self.children:
            if self.level:
                raise aurora.AuroraError("a tensor leaf must occupy level zero")
            return
        if len(self.children) != 3:
            raise aurora.AuroraError("a promoted tensor node needs three children")
        if any(child.level != self.level - 1 for child in self.children):
            raise aurora.AuroraError("promoted tensor children must share one level")
        expected = aurora.synthesize(
            tuple(child.unit for child in self.children),
            self.unit.direction,
            self.unit.do_before,
        )
        if expected != self.unit:
            raise aurora.AuroraError("a promoted tensor node must reexecute its origin")

    @classmethod
    def combine(
        cls,
        children: Sequence[TensorNode],
        direction: aurora.Direction,
        phase: Sequence[aurora.Trit],
    ) -> TensorNode:
        if len(children) != 3:
            raise aurora.AuroraError("tensor promotion needs exactly three nodes")
        triple = tuple(children)
        if len({child.level for child in triple}) != 1:
            raise aurora.AuroraError("tensor promotion cannot mix levels")
        unit = aurora.synthesize(
            tuple(child.unit for child in triple), direction, phase
        )
        return cls(unit, triple[0].level + 1, triple)

    @property
    def leaf_count(self) -> int:
        return 1 if not self.children else sum(child.leaf_count for child in self.children)

    @property
    def all_reexecute(self) -> bool:
        return aurora.reexecute(self.unit) and all(
            child.all_reexecute for child in self.children
        )

    def walk(self) -> tuple[TensorNode, ...]:
        return (self,) + tuple(
            descendant
            for child in self.children
            for descendant in child.walk()
        )


@dataclass(frozen=True)
class TensorLookup:
    """A lookup through one of the three channels of the same stored ``K``."""

    requirement: aurora.Triplet
    direction: aurora.Direction
    state: aurora.Trit
    nodes: tuple[TensorNode, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "requirement", aurora.triplet(self.requirement))
        object.__setattr__(self, "direction", aurora.Direction(self.direction))
        object.__setattr__(self, "state", aurora.trit(self.state))
        if self.state == 0 and self.nodes:
            raise aurora.AuroraError("an absent lookup cannot expose candidates")
        if self.state == 1 and len(self.nodes) != 1:
            raise aurora.AuroraError("a closed lookup must expose exactly one unit")
        if self.state == 2 and len(self.nodes) < 2:
            raise aurora.AuroraError("an open lookup must preserve alternatives")

    @property
    def channel(self) -> relational.Channel:
        return relational.Channel(int(self.direction))

    @property
    def selected(self) -> aurora.Unit | None:
        return self.nodes[0].unit if self.state == 1 else None

    @property
    def alternatives(self) -> tuple[aurora.Unit, ...]:
        return tuple(node.unit for node in self.nodes) if self.state == 2 else ()

    @property
    def outgoing(self) -> tuple[aurora.Trit, ...]:
        """Every retained candidate emits its own next ``O`` from ``DO[C]``."""

        index = int(self.direction)
        return tuple(node.unit.state.do[index] for node in self.nodes)


@dataclass(frozen=True)
class FractalTensorDictionary:
    """Immutable 1-3-9 memory, indexed by the three projections of one ``K``."""

    promotion_direction: aurora.Direction = aurora.Direction.INFER_R
    phase: aurora.Triplet = aurora.OPEN
    levels: tuple[tuple[TensorNode, ...], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "promotion_direction", aurora.Direction(self.promotion_direction)
        )
        object.__setattr__(self, "phase", aurora.triplet(self.phase))
        if any(len(nodes) > 2 for nodes in self.levels):
            raise aurora.AuroraError(
                "a normalized tensor dictionary retains fewer than three frontiers"
            )
        for level, nodes in enumerate(self.levels):
            if any(node.level != level for node in nodes):
                raise aurora.AuroraError("a tensor node is stored at the wrong level")

    def remember(self, unit: aurora.Unit) -> FractalTensorDictionary:
        """Store one complete ``K`` and promote every completed ternary group."""

        if not aurora.reexecute(unit):
            raise aurora.AuroraError("the dictionary cannot store a causal failure")
        buckets = [list(nodes) for nodes in self.levels]
        promoted = TensorNode(unit)
        level = 0
        while True:
            if level == len(buckets):
                buckets.append([])
            buckets[level].append(promoted)
            if len(buckets[level]) < 3:
                break
            children = tuple(buckets[level])
            buckets[level].clear()
            promoted = TensorNode.combine(
                children, self.promotion_direction, self.phase
            )
            level += 1
        return FractalTensorDictionary(
            self.promotion_direction,
            self.phase,
            tuple(tuple(nodes) for nodes in buckets),
        )

    @property
    def frontier(self) -> tuple[TensorNode, ...]:
        return tuple(node for level in self.levels for node in level)

    @property
    def root(self) -> TensorNode | None:
        frontier = self.frontier
        if len(frontier) == 1 and frontier[0].level > 0:
            return frontier[0]
        return None

    @property
    def nodes(self) -> tuple[TensorNode, ...]:
        """All causal nodes, highest scale first, without three index copies."""

        discovered = tuple(
            node
            for frontier in self.frontier
            for node in frontier.walk()
        )
        unique = tuple(dict.fromkeys(discovered))
        return tuple(
            node
            for level in range(len(self.levels) - 1, -1, -1)
            for node in unique
            if node.level == level
        )

    def search(
        self,
        requirement: Sequence[aurora.Trit],
        direction: aurora.Direction,
        *,
        exact: bool = True,
    ) -> TensorLookup:
        """Read ``K[C]`` and return the complete unit at the highest matching scale."""

        requirement = aurora.triplet(requirement)
        direction = aurora.Direction(direction)
        query = (
            deduction.DeductiveQuery.for_exact_tensor(requirement)
            if exact
            else deduction.DeductiveQuery.for_tensor(requirement)
        )
        index = int(direction)
        levels = tuple(dict.fromkeys(node.level for node in self.nodes))
        for level in levels:
            matches = tuple(
                node
                for node in self.nodes
                if node.level == level
                and query.accepts(node.unit.state.channels[index])
            )
            matches = tuple(dict.fromkeys(matches))
            if not matches:
                continue
            state = 1 if len(matches) == 1 else 2
            return TensorLookup(requirement, direction, state, matches)
        return TensorLookup(requirement, direction, 0)


__all__ = [
    "FractalAddress",
    "FractalTensorDictionary",
    "FractalTopology",
    "FractalWindow",
    "OrientedBoundary",
    "TensorLookup",
    "TensorNode",
    "TripletPassage",
    "UnitPassage",
    "WindowLevel",
    "WindowResolution",
    "open_unit",
    "pass_triplet",
    "resolve_level",
]
