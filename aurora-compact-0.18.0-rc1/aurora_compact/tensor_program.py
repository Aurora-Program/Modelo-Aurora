"""Homoiconic nine-triplet programs for the Aurora relational executor.

The 0.12 executor reads its operation from a tensor but still receives cell
connections as Python strings.  This module moves that remaining topology into
Aurora data.  One :class:`ProgramTensor` contains exactly nine ordinary units:

``three input addresses | three output addresses | DO, DE, DS instruction``

The compiler is deliberately mechanical.  It gives no meaning to a cell and
contains no growth, carry, pruning, lexical or recurrence action.  Changing
only the nine triplets changes which signals are presented, where the three
channels are published, and which direction/phase the frozen face executes.

Program hypotheses also compete without counters.  Three aligned code tensors
are presented position by position to the same Aurora face.  Two compatible
copies can synthesize a re-executable program; an impossible emergent address
remains non-executable while all three hypotheses are preserved.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Mapping, Sequence

from . import aurora, relational


CODE_TRIPLETS = 9
PHASE_ATOM = 6
CLOSED: aurora.Triplet = (1, 1, 1)


def _literal_address(value: Sequence[aurora.Trit]) -> bool:
    """Whether a triplet can be used as a closed relational address."""

    ordered = aurora.order_triplet(value)
    return ordered.valid or ordered.original == aurora.OPEN


def _address_name(value: Sequence[aurora.Trit]) -> str:
    address = aurora.triplet(value)
    return "cell:" + "".join(str(item) for item in address)


def _address_value(name: str) -> aurora.Triplet:
    """Recover the triplet carried literally by one relational address."""

    if not name.startswith("cell:") or len(name) != 8:
        raise aurora.AuroraError("tensor-program provenance has a foreign address")
    try:
        return aurora.triplet(int(item) for item in name[5:])
    except ValueError as error:
        raise aurora.AuroraError(
            "tensor-program provenance has a foreign address"
        ) from error


def _unit_payload(unit: aurora.Unit) -> dict[str, object]:
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
    raw_state = payload["state"]
    if not isinstance(raw_state, Mapping):
        raise aurora.AuroraError("program unit state must be a mapping")
    children_payload = payload.get("children", ())
    if not isinstance(children_payload, list):
        raise aurora.AuroraError("program unit children must be a list")
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
        raise aurora.AuroraError("serialized program provenance does not re-execute")
    return unit


@dataclass(frozen=True)
class ProgramTensor:
    """Nine Aurora units whose positions form an executable relation."""

    atoms: tuple[aurora.Unit, ...]

    def __post_init__(self) -> None:
        if len(self.atoms) != CODE_TRIPLETS:
            raise aurora.AuroraError("a tensor program needs exactly nine triplets")
        if not all(aurora.reexecute(atom) for atom in self.atoms):
            raise aurora.AuroraError("every tensor-program atom must re-execute")

    @classmethod
    def author(
        cls,
        inputs: Sequence[Sequence[aurora.Trit]],
        outputs: Sequence[Sequence[aurora.Trit]],
        direction: aurora.Direction,
        phase: Sequence[aurora.Trit] = aurora.OPEN,
    ) -> ProgramTensor:
        """Author education as data; the runtime never calls this helper."""

        if len(inputs) != 3 or len(outputs) != 3:
            raise aurora.AuroraError("a tensor program needs three inputs and outputs")
        c = aurora.Direction(direction).value
        values = (
            *(aurora.triplet(item) for item in inputs),
            *(aurora.triplet(item) for item in outputs),
            aurora.triplet(phase),
            CLOSED,
            (c, c, c),
        )
        return cls(tuple(aurora.Unit.leaf(value) for value in values))

    @classmethod
    def from_seed(cls, seed: relational.OperationalSeed) -> ProgramTensor:
        """Reflect executed educational provenance back into tensor code."""

        if len(seed.provenance) != CODE_TRIPLETS:
            raise aurora.AuroraError(
                "operational seed does not preserve a complete tensor program"
            )
        program = cls(seed.provenance)
        reflected_inputs = tuple(_address_value(name) for name in seed.inputs)
        reflected_outputs = tuple(_address_value(name) for name in seed.outputs)
        if program.inputs != reflected_inputs or program.outputs != reflected_outputs:
            raise aurora.AuroraError(
                "tensor-program provenance does not match executed routing"
            )
        if (
            program.phase != seed.tensor.state.do
            or program.de != seed.tensor.state.de
            or program.signature != seed.tensor.state.ds
        ):
            raise aurora.AuroraError(
                "tensor-program provenance does not match executed instruction"
            )
        return program

    @classmethod
    def from_firing(cls, firing: relational.Firing) -> ProgramTensor:
        """Recover code exclusively from one re-executable causal firing."""

        if not firing.reexecutes:
            raise aurora.AuroraError("cannot reflect a firing that does not re-execute")
        return cls.from_seed(firing.seed)

    @property
    def values(self) -> tuple[aurora.Triplet, ...]:
        return tuple(atom.value for atom in self.atoms)

    @property
    def inputs(self) -> tuple[aurora.Triplet, aurora.Triplet, aurora.Triplet]:
        return self.values[:3]  # type: ignore[return-value]

    @property
    def outputs(self) -> tuple[aurora.Triplet, aurora.Triplet, aurora.Triplet]:
        return self.values[3:6]  # type: ignore[return-value]

    @property
    def phase(self) -> aurora.Triplet:
        return self.values[6]

    @property
    def de(self) -> aurora.Triplet:
        return self.values[7]

    @property
    def signature(self) -> aurora.Triplet:
        return self.values[8]

    @property
    def direction(self) -> aurora.Direction:
        if len(set(self.signature)) != 1:
            raise aurora.AuroraError("tensor-program direction is still open")
        return aurora.Direction(self.signature[0])

    @property
    def executable(self) -> bool:
        try:
            self.compile("probe")
        except aurora.AuroraError:
            return False
        return True

    @property
    def all_reexecute(self) -> bool:
        return all(aurora.reexecute(atom) for atom in self.atoms)

    def compile(self, name: str) -> relational.OperationalSeed:
        """Decode tensor positions into the universal executor's six ports."""

        if not all(_literal_address(value) for value in (*self.inputs, *self.outputs)):
            raise aurora.AuroraError("tensor program contains an open address")
        if self.de != CLOSED:
            raise aurora.AuroraError("tensor-program instruction has not closed")
        direction = self.direction
        instruction = aurora.Unit(aurora.Knowledge(
            self.phase, self.de, self.signature
        ))
        if direction != aurora.Direction(aurora.majority3(*instruction.value)):
            raise aurora.AuroraError("tensor-program direction is inconsistent")
        return relational.OperationalSeed.from_tensor(
            name,
            tuple(_address_name(item) for item in self.inputs),
            tuple(_address_name(item) for item in self.outputs),
            instruction,
            self.atoms,
        )

    def to_json(self, *, indent: int | None = 2) -> str:
        return json.dumps(
            {
                "schema": "aurora-tensor-program-v1",
                "atoms": [_unit_payload(atom) for atom in self.atoms],
            },
            indent=indent,
            sort_keys=True,
        )

    @classmethod
    def from_json(cls, document: str) -> ProgramTensor:
        payload = json.loads(document)
        if payload.get("schema") != "aurora-tensor-program-v1":
            raise aurora.AuroraError("unknown tensor-program schema")
        return cls(tuple(_unit_from_payload(item) for item in payload["atoms"]))


@dataclass(frozen=True)
class ProgramInduction:
    """Three preserved hypotheses and the code tensor their faces produced."""

    candidates: tuple[ProgramTensor, ProgramTensor, ProgramTensor]
    emergent: ProgramTensor
    direction: aurora.Direction = aurora.Direction.INFER_R
    phase: aurora.Triplet = aurora.OPEN

    def __post_init__(self) -> None:
        object.__setattr__(self, "direction", aurora.Direction(self.direction))
        object.__setattr__(self, "phase", aurora.triplet(self.phase))

    @property
    def all_reexecute(self) -> bool:
        expected = tuple(
            aurora.synthesize(
                tuple(candidate.atoms[index] for candidate in self.candidates),
                self.direction,
                self.phase,
            )
            for index in range(CODE_TRIPLETS)
        )
        return self.emergent.atoms == expected and self.emergent.all_reexecute


def induce(
    candidates: Sequence[ProgramTensor],
    phase: Sequence[aurora.Trit] = aurora.OPEN,
    *,
    direction: aurora.Direction = aurora.Direction.INFER_R,
) -> ProgramInduction:
    """Present three complete programs through nine ordinary Aurora faces."""

    if len(candidates) != 3:
        raise aurora.AuroraError("program induction needs exactly three hypotheses")
    triple = tuple(candidates)
    phase = aurora.triplet(phase)
    direction = aurora.Direction(direction)
    atoms = tuple(
        aurora.synthesize(
            tuple(candidate.atoms[index] for candidate in triple),
            direction,
            phase,
        )
        for index in range(CODE_TRIPLETS)
    )
    return ProgramInduction(  # type: ignore[arg-type]
        triple, ProgramTensor(atoms), direction, phase
    )


@dataclass(frozen=True)
class ProgramExecution:
    """Address-preserving view of the unchanged relational execution."""

    programs: tuple[ProgramTensor, ...]
    execution: relational.Execution

    def values(self, address: Sequence[aurora.Trit]) -> tuple[aurora.Triplet, ...]:
        return self.execution.values(_address_name(address))

    @property
    def all_reexecute(self) -> bool:
        return (
            all(program.all_reexecute for program in self.programs)
            and self.execution.all_reexecute
    )


@dataclass(frozen=True)
class ProgramReflection:
    """A code tensor recovered from one firing rather than authored again."""

    execution_number: int
    firing: relational.Firing
    program: ProgramTensor

    @property
    def window(self) -> tuple[tuple[object, ...], ...]:
        return tuple(signal.fingerprint for signal in self.firing.inputs)

    @property
    def reexecutes(self) -> bool:
        return self.firing.reexecutes and self.program.all_reexecute


@dataclass(frozen=True)
class ProvenanceInduction:
    """Three causal experiences presented to the unchanged induction faces."""

    reflections: tuple[ProgramReflection, ProgramReflection, ProgramReflection]
    induction: ProgramInduction

    @property
    def emergent(self) -> ProgramTensor:
        return self.induction.emergent

    @property
    def all_reexecute(self) -> bool:
        return (
            all(reflection.reexecutes for reflection in self.reflections)
            and self.induction.all_reexecute
        )


def induce_from_provenance(
    executions: Sequence[relational.Execution],
) -> tuple[ProvenanceInduction, ...]:
    """Let exact causal windows present their own tensor-program hypotheses.

    Code-bearing firings are grouped only when their three input fingerprints
    are identical.  The event order supplies ordinary sliding windows of three;
    each window is passed to :func:`induce`, the same nine Aurora faces used by
    explicit 0.13 experiments.  The host neither authors candidate programs nor
    scores them.
    """

    grouped: dict[
        tuple[tuple[object, ...], ...], list[ProgramReflection]
    ] = {}
    for execution_number, execution in enumerate(executions):
        for firing in execution.firings:
            if not firing.seed.provenance:
                continue
            reflection = ProgramReflection(
                execution_number,
                firing,
                ProgramTensor.from_firing(firing),
            )
            grouped.setdefault(reflection.window, []).append(reflection)

    learned: list[ProvenanceInduction] = []
    for reflections in grouped.values():
        for index in range(len(reflections) - 2):
            window = tuple(reflections[index:index + 3])
            induction = induce(tuple(item.program for item in window))
            learned.append(ProvenanceInduction(window, induction))  # type: ignore[arg-type]
    return tuple(learned)


def execute(
    programs: Sequence[ProgramTensor],
    initial: Mapping[
        aurora.Triplet,
        Sequence[aurora.Trit] | relational.Signal | Sequence[relational.Signal],
    ],
    *,
    budget: int = 729,
) -> ProgramExecution:
    """Execute code tensors without a Python-authored presentation graph."""

    unique = tuple(dict.fromkeys(programs))
    seeds = tuple(
        program.compile(f"tensor-program-{index}")
        for index, program in enumerate(unique)
    )
    encoded_initial = {
        _address_name(address): value for address, value in initial.items()
    }
    result = relational.execute(relational.Education(seeds), encoded_initial, budget=budget)
    return ProgramExecution(unique, result)


__all__ = [
    "CODE_TRIPLETS",
    "CLOSED",
    "PHASE_ATOM",
    "ProgramExecution",
    "ProgramInduction",
    "ProgramReflection",
    "ProgramTensor",
    "ProvenanceInduction",
    "execute",
    "induce",
    "induce_from_provenance",
]
