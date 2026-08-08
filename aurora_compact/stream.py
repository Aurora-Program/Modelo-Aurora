"""Sequential learning probes built only from the Aurora compact kernel."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Sequence

from aurora_compact import aurora


def surface(unit: aurora.Unit) -> tuple[aurora.Triplet, ...]:
    """Return the ordered simple-token provenance of a fractal unit."""
    if not unit.children:
        return (unit.value,)
    return tuple(value for child in unit.children for value in surface(child))


def reexecute_local(unit: aurora.Unit) -> bool:
    """Verify one stored face while trusting already verified descendants."""
    if not unit.children:
        return True
    result = aurora.face(
        tuple(child.value for child in unit.children),
        unit.direction,
        unit.do_before,
    )
    return result.knowledge == unit.state


def _priority(memory: aurora.AuroraDictionary, unit: aurora.Unit) -> tuple[int, int]:
    uses = ((relation.successful_uses, relation.last_success)
            for relation in memory.entries
            if relation.input == unit or relation.output == unit)
    return max(uses, default=(0, 0))


@dataclass(frozen=True)
class SequenceResult:
    fractal: aurora.FractalResult
    lexicalized: bool
    candidates_tried: int

    @property
    def logical_cost(self) -> int:
        return self.candidates_tried + sum(
            len(step.trace) for step in self.fractal.trace
        )


def process_sequence(
    tokens: Sequence[Sequence[aurora.Trit]],
    dictionary: aurora.AuroraDictionary | None = None,
    do_route: Sequence[Sequence[aurora.Trit]] = (aurora.OPEN,),
    tick: int = 0,
) -> SequenceResult:
    """Reuse an exact stored tensor or construct it fractally from simple tokens.

    This first lexical profile recognizes only a tensor spanning the complete
    sequence. Partial segmentation and backtracking remain deliberately open.
    """
    values = tuple(aurora.triplet(token) for token in tokens)
    if not values or len(values) % 3:
        raise aurora.AuroraError("a sequence needs a non-empty multiple of three")
    memory = aurora.AuroraDictionary() if dictionary is None else dictionary
    candidates = [unit for unit in memory.lexicon
                  if unit.children and surface(unit) == values]
    candidates.sort(key=lambda unit: _priority(memory, unit), reverse=True)
    for number, unit in enumerate(candidates, 1):
        if reexecute_local(unit):
            leaves = tuple(aurora.Unit.leaf(value) for value in values)
            result = aurora.FractalResult(
                unit, memory, (leaves, (unit,)), (),
            )
            return SequenceResult(result, True, number)
    result = aurora.process_fractal(values, memory, do_route, tick)
    return SequenceResult(result, False, len(candidates))


@dataclass(frozen=True)
class Observation:
    index: int
    lexicalized: bool
    logical_cost: int
    candidates_tried: int
    transformations: int
    learned: int
    reused: int
    rejected: int
    new_relations: int
    dictionary_size: int


@dataclass(frozen=True)
class StreamResult:
    dictionary: aurora.AuroraDictionary
    observations: tuple[Observation, ...]


def learn_stream(
    sequences: Sequence[Sequence[Sequence[aurora.Trit]]],
    dictionary: aurora.AuroraDictionary | None = None,
    do_route: Sequence[Sequence[aurora.Trit]] = (aurora.OPEN,),
) -> StreamResult:
    """Process successive token sequences while preserving one dictionary."""
    memory = aurora.AuroraDictionary() if dictionary is None else dictionary
    observations: list[Observation] = []
    for index, tokens in enumerate(sequences):
        before = len(memory.entries)
        result = process_sequence(tokens, memory, do_route, index + 1)
        memory = result.fractal.dictionary
        actions = Counter(attempt.action for step in result.fractal.trace
                          for attempt in step.trace)
        observations.append(Observation(
            index=index,
            lexicalized=result.lexicalized,
            logical_cost=result.logical_cost,
            candidates_tried=result.candidates_tried,
            transformations=len(result.fractal.trace),
            learned=actions[aurora.AttemptAction.LEARN_KNOWLEDGE],
            reused=actions[aurora.AttemptAction.REUSE_OUTPUT],
            rejected=actions[aurora.AttemptAction.REJECT],
            new_relations=len(memory.entries) - before,
            dictionary_size=len(memory.entries),
        ))
    return StreamResult(memory, tuple(observations))
