"""One ternary orientation propagated through every Aurora scale.

The module adds no movement table.  It only makes two existing invariants
executable: ``O`` selects ``ES`` inside a triplet, and the selected ``DO`` trit
of a complete unit can be presented unchanged as ``C`` to the next relation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from . import aurora


@dataclass(frozen=True)
class TripletOrientation:
    """The ordinary triplet ordering exposed as an orientation result."""

    ordering: aurora.Ordering

    @property
    def resolved(self) -> bool:
        return self.ordering.valid

    @property
    def o(self) -> aurora.Trit | None:
        return self.ordering.o if self.resolved else None

    @property
    def es(self) -> aurora.Trit | None:
        return self.ordering.es if self.resolved else None


def orient_triplet(
    values: Sequence[aurora.Trit], phase: aurora.Trit = 2,
) -> TripletOrientation:
    """Determine ``O`` and therefore ``ES`` with the frozen ordering rule."""

    return TripletOrientation(aurora.order_triplet(values, phase))


@dataclass(frozen=True)
class VerticalInheritance:
    """One application of ``ES↑ = ES[O↑]``."""

    upper_o: aurora.Trit
    selected: aurora.Triplet
    lower: TripletOrientation

    @property
    def es(self) -> aurora.Trit | None:
        return self.lower.es


def inherit_es(
    children: Sequence[Sequence[aurora.Trit]],
    upper_o: aurora.Trit,
    phases: Sequence[aurora.Trit] = aurora.OPEN,
) -> VerticalInheritance:
    """Select one lower relation by superior ``O`` and retain its ``ES``."""

    if len(children) != 3:
        raise aurora.AuroraError("vertical orientation needs three children")
    index = aurora.trit(upper_o)
    phase = aurora.triplet(phases)[index]
    selected = aurora.triplet(children[index])
    return VerticalInheritance(index, selected, orient_triplet(selected, phase))


@dataclass(frozen=True)
class Presentation:
    """One full unit read at an index without changing or rebuilding it."""

    unit: aurora.Unit
    incoming: aurora.Trit
    outgoing: aurora.Trit

    def __post_init__(self) -> None:
        if not aurora.reexecute(self.unit):
            raise aurora.AuroraError("an oriented unit must re-execute")
        if self.outgoing != self.unit.state.do[self.incoming]:
            raise aurora.AuroraError("outgoing orientation must come from unit DO")


def present(unit: aurora.Unit, incoming: aurora.Trit) -> Presentation:
    """Apply ``C[t+1] = DO[t][C[t]]`` without translating the tensor."""

    incoming = aurora.trit(incoming)
    return Presentation(unit, incoming, unit.state.do[incoming])


def chain(
    units: Sequence[aurora.Unit], initial: aurora.Trit,
) -> tuple[Presentation, ...]:
    """Feed each emitted orientation directly into the next full unit."""

    current = aurora.trit(initial)
    trace = []
    for unit in units:
        step = present(unit, current)
        trace.append(step)
        current = step.outgoing
    return tuple(trace)


__all__ = [
    "Presentation",
    "TripletOrientation",
    "VerticalInheritance",
    "chain",
    "inherit_es",
    "orient_triplet",
    "present",
]
