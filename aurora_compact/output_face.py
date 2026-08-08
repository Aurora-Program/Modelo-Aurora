"""Parallel read-write output face for the fractal Aurora dictionary.

The three output requirements query one shared dictionary from their own
Aurora indices.  Their lookup states remain trits: 1 found, 0 absent and 2
open.  Only a determined two-of-three closure may crystallize the sole absent
output.  The runtime never authors a replacement program and never writes two
unknowns to force a continuation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from . import aurora, fractal_dictionary, tensor_program


class OutputAction(Enum):
    """The four structural outcomes of one parallel output lookup."""

    CONTINUE = "continue"
    CRYSTALLIZE = "crystallize"
    RETURN = "return"
    OPEN = "open"


@dataclass(frozen=True)
class OutputLane:
    """One output requirement and the search made from its own C index."""

    index: int
    direction: aurora.Direction
    search: fractal_dictionary.DictionarySearch

    def __post_init__(self) -> None:
        if self.index not in aurora.TRITS:
            raise aurora.AuroraError("an output lane index must be a trit")
        if int(self.direction) != self.index:
            raise aurora.AuroraError("an output lane must search from its own index")


@dataclass(frozen=True)
class OutputResolution:
    """Immutable result of the ternary read-write decision."""

    requirements: tuple[
        tensor_program.ProgramTensor,
        tensor_program.ProgramTensor,
        tensor_program.ProgramTensor,
    ]
    lanes: tuple[OutputLane, OutputLane, OutputLane]
    states: aurora.Triplet
    action: OutputAction
    memory_before: fractal_dictionary.FractalProgramDictionary
    memory_after: fractal_dictionary.FractalProgramDictionary
    crystallized_index: int | None = None
    crystallized: tensor_program.ProgramTensor | None = None
    post_states: aurora.Triplet | None = None

    @property
    def can_advance(self) -> bool:
        return self.action in (OutputAction.CONTINUE, OutputAction.CRYSTALLIZE)

    @property
    def returned(self) -> tuple[tensor_program.ProgramTensor, ...]:
        """The unchanged output tensors retained when the path cannot advance."""

        return self.requirements if self.action is OutputAction.RETURN else ()

    @property
    def all_reexecute(self) -> bool:
        return all(program.all_reexecute for program in self.requirements)


def _parallel_search(
    memory: fractal_dictionary.FractalProgramDictionary,
    requirements: tuple[
        tensor_program.ProgramTensor,
        tensor_program.ProgramTensor,
        tensor_program.ProgramTensor,
    ],
    do_t: aurora.Triplet,
) -> tuple[OutputLane, OutputLane, OutputLane]:
    lanes = tuple(
        OutputLane(
            index,
            aurora.Direction(index),
            memory.search(requirement, aurora.Direction(index), do_t),
        )
        for index, requirement in enumerate(requirements)
    )
    return lanes  # type: ignore[return-value]


def resolve(
    memory: fractal_dictionary.FractalProgramDictionary,
    requirements: Sequence[tensor_program.ProgramTensor],
    do_t: Sequence[aurora.Trit] = aurora.OPEN,
) -> OutputResolution:
    """Read three outputs, crystallize one absence, or return them unchanged."""

    if len(requirements) != 3:
        raise aurora.AuroraError("an output face requires exactly three tensors")
    triple = tuple(requirements)
    do_t = aurora.triplet(do_t)
    lanes = _parallel_search(memory, triple, do_t)  # type: ignore[arg-type]
    states = aurora.triplet(lane.search.state for lane in lanes)

    if 2 in states:
        return OutputResolution(
            triple, lanes, states, OutputAction.OPEN, memory, memory
        )  # type: ignore[arg-type]

    closure = aurora.majority3(*states)
    if closure == 0:
        return OutputResolution(
            triple, lanes, states, OutputAction.RETURN, memory, memory
        )  # type: ignore[arg-type]

    if states == (1, 1, 1):
        return OutputResolution(
            triple, lanes, states, OutputAction.CONTINUE, memory, memory,
            post_states=states,
        )  # type: ignore[arg-type]

    missing = states.index(0)
    candidate = triple[missing]
    if not candidate.executable or not candidate.all_reexecute:
        return OutputResolution(
            triple, lanes, states, OutputAction.RETURN, memory, memory
        )  # type: ignore[arg-type]

    updated = memory.remember(candidate)
    verification = updated.search(candidate, aurora.Direction(missing), do_t)
    if verification.state != 1:
        raise aurora.AuroraError("a crystallized output must close when read back")
    post_states = tuple(
        1 if index == missing else state
        for index, state in enumerate(states)
    )
    return OutputResolution(
        triple,
        lanes,
        states,
        OutputAction.CRYSTALLIZE,
        memory,
        updated,
        missing,
        candidate,
        aurora.triplet(post_states),
    )  # type: ignore[arg-type]


__all__ = [
    "OutputAction",
    "OutputLane",
    "OutputResolution",
    "resolve",
]
