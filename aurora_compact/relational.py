"""Universal event-driven execution for Aurora operational seeds.

This module deliberately knows nothing about text, syllables, segmentation,
carry, ascent, pruning or recurrence scores.  It implements only the substrate
described by Aurora's relational automata:

``changed cells -> ordinary face -> (DO, DE, DS) -> dependent faces``

What is presented together and where each projected channel is presented next
belongs to :class:`Education`.  The operational instruction is itself an
Aurora :class:`~aurora_compact.aurora.Unit`: its ``DS`` majority selects the
ordinary face direction and its ``DO`` supplies the stable phase.  Changing
that tensor or the educational topology changes behaviour without changing
the executor.

All exact alternatives are preserved.  A seed fires once for every new
combination of three input signals.  Emissions retain their complete
provenance and can be re-executed through the frozen Aurora face.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import IntEnum
from itertools import product
import json
from typing import Iterable, Mapping, Sequence

from . import aurora


class Channel(IntEnum):
    """The three projections published by every ordinary Aurora face."""

    DO = 0
    DE = 1
    DS = 2


@dataclass(frozen=True)
class OperationalSeed:
    """One homoiconic instruction plus its educational presentation graph.

    ``tensor`` is data, not a Python callback.  A determined majority in its
    ``DS`` channel is read as ``C``; its ``DO`` channel is the phase snapshot.
    ``inputs`` and ``outputs`` are cell addresses in the educated relational
    graph.  Their meaning is not interpreted by the executor.
    """

    name: str
    inputs: tuple[str, str, str]
    outputs: tuple[str, str, str]
    tensor: aurora.Unit
    provenance: tuple[aurora.Unit, ...] = ()

    def __post_init__(self) -> None:
        if not self.name:
            raise aurora.AuroraError("an operational seed needs a name")
        if len(self.inputs) != 3 or any(not cell for cell in self.inputs):
            raise aurora.AuroraError("a seed needs three named input cells")
        if len(self.outputs) != 3 or any(not cell for cell in self.outputs):
            raise aurora.AuroraError("a seed needs three named output cells")
        if not aurora.reexecute(self.tensor):
            raise aurora.AuroraError("the operational tensor must re-execute")
        if not all(aurora.reexecute(unit) for unit in self.provenance):
            raise aurora.AuroraError(
                "every educational provenance unit must re-execute"
            )
        signature = self.tensor.value
        direction = aurora.majority3(*signature)
        if set(signature) == aurora.TRITS:
            raise aurora.AuroraError(
                "the seed DS must determine one Aurora direction"
            )
        if signature == aurora.OPEN and self.tensor.state.de != (1, 1, 1):
            raise aurora.AuroraError(
                "cannot determine direction 2 without a closed tensor instruction"
            )

    @property
    def direction(self) -> aurora.Direction:
        return aurora.Direction(aurora.majority3(*self.tensor.value))

    @property
    def phase(self) -> aurora.Triplet:
        return self.tensor.state.do

    @classmethod
    def from_tensor(
        cls,
        name: str,
        inputs: Sequence[str],
        outputs: Sequence[str],
        tensor: aurora.Unit,
        provenance: Sequence[aurora.Unit] = (),
    ) -> OperationalSeed:
        return cls(
            name,
            tuple(inputs),  # type: ignore[arg-type]
            tuple(outputs),  # type: ignore[arg-type]
            tensor,
            tuple(provenance),
        )


def instruction_tensor(
    direction: aurora.Direction,
    phase: Sequence[aurora.Trit] = aurora.OPEN,
) -> aurora.Unit:
    """Create a leaf instruction for educational authoring.

    The executor never calls this helper.  It reads only the resulting tensor.
    Repeating ``C`` three times gives the instruction a determined majority.
    ``DE=111`` marks the instruction itself as closed.  This is essential for
    ``C=2``: its canonical ``DS=222`` is a valid deduction instruction rather
    than an unresolved direction.
    """

    c = aurora.Direction(direction).value
    return aurora.Unit(aurora.Knowledge(
        aurora.triplet(phase), (1, 1, 1), (c, c, c)
    ))


def _unit_payload(unit: aurora.Unit) -> dict[str, object]:
    """Serialize one re-executable unit without interpreting its role."""

    return {
        "state": {
            "do": list(unit.state.do),
            "de": list(unit.state.de),
            "ds": list(unit.state.ds),
        },
        "direction": int(unit.direction),
        "do_before": list(unit.do_before),
        "children": [_unit_payload(child) for child in unit.children],
    }


def _unit_from_payload(payload: Mapping[str, object]) -> aurora.Unit:
    """Restore and verify one unit of educational provenance."""

    raw_state = payload["state"]
    if not isinstance(raw_state, Mapping):
        raise aurora.AuroraError("provenance unit state must be a mapping")
    children_payload = payload.get("children", ())
    if not isinstance(children_payload, list):
        raise aurora.AuroraError("provenance unit children must be a list")
    unit = aurora.Unit(
        aurora.Knowledge(
            raw_state["do"],  # type: ignore[arg-type]
            raw_state["de"],  # type: ignore[arg-type]
            raw_state["ds"],  # type: ignore[arg-type]
        ),
        tuple(_unit_from_payload(item) for item in children_payload),
        aurora.Direction(int(payload.get("direction", 1))),
        aurora.triplet(payload.get("do_before", aurora.OPEN)),  # type: ignore[arg-type]
    )
    if not aurora.reexecute(unit):
        raise aurora.AuroraError("serialized educational provenance does not re-execute")
    return unit


@dataclass(frozen=True)
class Education:
    """An immutable dictionary of operational seeds and cell connections."""

    seeds: tuple[OperationalSeed, ...]

    def __post_init__(self) -> None:
        names = tuple(seed.name for seed in self.seeds)
        if len(names) != len(set(names)):
            raise aurora.AuroraError("operational seed names must be unique")

    @property
    def cells(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(
            cell
            for seed in self.seeds
            for cell in (*seed.inputs, *seed.outputs)
        ))

    def to_json(self, *, indent: int | None = 2) -> str:
        """Serialize the education as data, with no executable callbacks."""

        payload = {
            "schema": "aurora-operational-education-v1",
            "seeds": [
                {
                    "name": seed.name,
                    "inputs": list(seed.inputs),
                    "outputs": list(seed.outputs),
                    "tensor": {
                        "do": list(seed.tensor.state.do),
                        "de": list(seed.tensor.state.de),
                        "ds": list(seed.tensor.state.ds),
                    },
                    "provenance": [
                        _unit_payload(unit) for unit in seed.provenance
                    ],
                }
                for seed in self.seeds
            ],
        }
        return json.dumps(payload, indent=indent, sort_keys=True)

    @classmethod
    def from_json(cls, document: str) -> Education:
        payload = json.loads(document)
        if payload.get("schema") != "aurora-operational-education-v1":
            raise aurora.AuroraError("unknown operational education schema")
        seeds = []
        for item in payload.get("seeds", ()):
            state = item["tensor"]
            tensor = aurora.Unit(aurora.Knowledge(
                state["do"], state["de"], state["ds"]
            ))
            provenance = tuple(
                _unit_from_payload(unit)
                for unit in item.get("provenance", ())
            )
            seeds.append(OperationalSeed.from_tensor(
                item["name"], item["inputs"], item["outputs"], tensor,
                provenance,
            ))
        return cls(tuple(seeds))


@dataclass(frozen=True)
class Signal:
    """One triplet in one cell, with a re-executable causal history."""

    value: aurora.Triplet
    origin: str
    parents: tuple[Signal, ...] = ()
    seed: OperationalSeed | None = None
    channel: Channel | None = None
    knowledge: aurora.Knowledge | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", aurora.triplet(self.value))
        if not self.origin:
            raise aurora.AuroraError("a signal needs an origin")
        emitted = self.seed is not None
        if emitted != bool(self.parents):
            raise aurora.AuroraError(
                "an emitted signal needs both a seed and three parents"
            )
        if emitted and (len(self.parents) != 3
                        or self.channel is None
                        or self.knowledge is None):
            raise aurora.AuroraError(
                "an emitted signal needs channel and knowledge provenance"
            )
        if not emitted and (self.channel is not None or self.knowledge is not None):
            raise aurora.AuroraError("a leaf signal cannot claim face provenance")

    @classmethod
    def leaf(cls, value: Sequence[aurora.Trit], origin: str) -> Signal:
        return cls(aurora.triplet(value), origin)

    @property
    def fingerprint(self) -> tuple[object, ...]:
        if self.seed is None:
            return "leaf", self.origin, self.value
        return (
            "face",
            self.seed.name,
            self.seed.inputs,
            self.seed.outputs,
            self.seed.tensor,
            self.seed.provenance,
            int(self.channel),
            tuple(parent.fingerprint for parent in self.parents),
            self.value,
        )

    @property
    def depth(self) -> int:
        return 0 if not self.parents else 1 + max(p.depth for p in self.parents)

    def reexecutes(self) -> bool:
        if self.seed is None:
            return True
        if not all(parent.reexecutes() for parent in self.parents):
            return False
        result = aurora.face(
            tuple(parent.value for parent in self.parents),
            self.seed.direction,
            self.seed.phase,
        )
        return (
            result.knowledge == self.knowledge
            and self.value == result.knowledge.channels[int(self.channel)]
        )


@dataclass(frozen=True)
class Cell:
    """All exact alternatives currently known at one graph address."""

    name: str
    signals: tuple[Signal, ...] = ()


@dataclass(frozen=True)
class Firing:
    """One application of one seed to one exact input combination."""

    number: int
    seed: OperationalSeed
    inputs: tuple[Signal, Signal, Signal]
    result: aurora.FaceResult
    emissions: tuple[Signal, Signal, Signal]

    @property
    def reexecutes(self) -> bool:
        return all(signal.reexecutes() for signal in self.emissions)


@dataclass(frozen=True)
class Execution:
    """The fixed point or budget frontier of one relational execution."""

    education: Education
    cells: tuple[Cell, ...]
    firings: tuple[Firing, ...]
    fixed_point: bool
    exhausted: bool
    budget: int

    def signals(self, cell: str) -> tuple[Signal, ...]:
        try:
            return next(item.signals for item in self.cells if item.name == cell)
        except StopIteration as error:
            raise aurora.AuroraError(f"unknown relational cell {cell!r}") from error

    def values(self, cell: str) -> tuple[aurora.Triplet, ...]:
        return tuple(signal.value for signal in self.signals(cell))

    @property
    def all_reexecute(self) -> bool:
        return all(firing.reexecutes for firing in self.firings)


def _normalize_initial(
    initial: Mapping[str, Sequence[aurora.Trit] | Signal | Iterable[Signal]],
) -> dict[str, list[Signal]]:
    cells: dict[str, list[Signal]] = {}
    for cell, supplied in initial.items():
        if not cell:
            raise aurora.AuroraError("initial cell names cannot be empty")
        if isinstance(supplied, Signal):
            signals = [supplied]
        else:
            material = tuple(supplied)
            if len(material) == 3 and all(isinstance(value, int) for value in material):
                signals = [Signal.leaf(material, cell)]
            elif all(isinstance(value, Signal) for value in material):
                signals = list(material)  # type: ignore[list-item]
            else:
                raise aurora.AuroraError(
                    "initial values must be one triplet or an iterable of Signals"
                )
        fingerprints = {signal.fingerprint for signal in signals}
        if len(fingerprints) != len(signals):
            raise aurora.AuroraError("initial alternatives must be distinct")
        cells[cell] = signals
    return cells


def execute(
    education: Education,
    initial: Mapping[str, Sequence[aurora.Trit] | Signal | Iterable[Signal]],
    *,
    budget: int = 729,
) -> Execution:
    """Propagate changed cells through ordinary faces until a fixed point.

    The loop has no semantic action table.  It evaluates every newly enabled
    exact presentation, publishes its three channels, and wakes seeds that
    subscribe to changed cells.  A finite budget is the sole hard stop for an
    education containing a productive cycle.
    """

    if budget < 1:
        raise aurora.AuroraError("the relational execution budget must be positive")
    cells = _normalize_initial(initial)
    for name in education.cells:
        cells.setdefault(name, [])

    dependents: dict[str, list[int]] = {name: [] for name in cells}
    for index, seed in enumerate(education.seeds):
        for name in dict.fromkeys(seed.inputs):
            dependents.setdefault(name, []).append(index)

    pending = deque(range(len(education.seeds)))
    queued = set(pending)
    fired: set[tuple[object, ...]] = set()
    firings: list[Firing] = []

    while pending and len(firings) < budget:
        index = pending.popleft()
        queued.discard(index)
        seed = education.seeds[index]
        alternatives = tuple(cells[name] for name in seed.inputs)
        if any(not values for values in alternatives):
            continue
        for inputs in product(*alternatives):
            key = (seed.name, tuple(signal.fingerprint for signal in inputs))
            if key in fired:
                continue
            fired.add(key)
            result = aurora.face(
                tuple(signal.value for signal in inputs),
                seed.direction,
                seed.phase,
            )
            emission_tuple = tuple(
                Signal(
                    value,
                    f"{seed.name}:{channel.name.lower()}",
                    inputs,
                    seed,
                    channel,
                    result.knowledge,
                )
                for channel, value in zip(Channel, result.knowledge.channels)
            )
            firing = Firing(
                len(firings) + 1, seed, inputs, result, emission_tuple
            )
            firings.append(firing)
            for output, signal in zip(seed.outputs, emission_tuple):
                known = {item.fingerprint for item in cells[output]}
                if signal.fingerprint in known:
                    continue
                cells[output].append(signal)
                for dependent in dependents.get(output, ()):  # event fan-out
                    if dependent not in queued:
                        pending.append(dependent)
                        queued.add(dependent)
            if len(firings) >= budget:
                break

    exhausted = bool(pending) and len(firings) >= budget
    frozen_cells = tuple(
        Cell(name, tuple(cells[name]))
        for name in dict.fromkeys((*education.cells, *initial.keys()))
    )
    return Execution(
        education,
        frozen_cells,
        tuple(firings),
        fixed_point=not pending,
        exhausted=exhausted,
        budget=budget,
    )


__all__ = [
    "Cell",
    "Channel",
    "Education",
    "Execution",
    "Firing",
    "OperationalSeed",
    "Signal",
    "execute",
    "instruction_tensor",
]
