"""Reproducible experiment: causal firings propose tensor programs."""

from __future__ import annotations

from . import aurora, relational, tensor_program


P0 = (0, 0, 0)
P1 = (0, 0, 1)
P2 = (0, 0, 2)
P3 = (1, 0, 1)
P4 = (1, 1, 0)
P5 = (1, 1, 1)
P6 = (1, 1, 2)
P8 = (0, 1, 0)


def route(output_ds=P5) -> tensor_program.ProgramTensor:
    return tensor_program.ProgramTensor.author(
        (P0, P1, P2),
        (P3, P4, output_ds),
        aurora.Direction.INFER_R,
    )


def observe(
    program: tensor_program.ProgramTensor,
    value=P0,
) -> relational.Execution:
    return tensor_program.execute(
        (program,), {P0: value, P1: value, P2: value}
    ).execution


def run() -> dict[str, object]:
    recurrent = route(P5)
    alternative = route(P6)
    experiences = (
        observe(recurrent),
        observe(recurrent),
        observe(alternative),
    )
    learned = tensor_program.induce_from_provenance(experiences)[0]
    replay = observe(learned.emergent)

    incompatible_programs = (route(P8), route(P3), route(P6))
    incompatible = tensor_program.induce_from_provenance(
        tuple(observe(program) for program in incompatible_programs)
    )[0]
    separated = tensor_program.induce_from_provenance((
        observe(recurrent, P0),
        observe(recurrent, P0),
        observe(alternative, P5),
    ))

    education = relational.Education((learned.emergent.compile("learned"),))
    restored = relational.Education.from_json(education.to_json())
    restored_program = tensor_program.ProgramTensor.from_seed(restored.seeds[0])

    return {
        "schema": "aurora-provenance-program-experiment-v1",
        "runtime_action_table": [],
        "same_causal_window": {
            "experiences": len(experiences),
            "candidate_values": [
                [list(value) for value in program.values]
                for program in learned.induction.candidates
            ],
            "candidate_programs_authored_by_runtime": False,
            "emergent_equals_recurrent": (
                learned.emergent.values == recurrent.values
            ),
            "emergent_executable": learned.emergent.executable,
            "executed_ds": [
                list(value) for value in replay.values("cell:111")
            ],
            "reflected_program_atoms": len(learned.emergent.atoms),
        },
        "distinct_causal_window": {
            "inductions": len(separated),
        },
        "incompatible_window": {
            "hypotheses_preserved": len(incompatible.induction.candidates),
            "emergent_ds_address": list(incompatible.emergent.outputs[2]),
            "emergent_executable": incompatible.emergent.executable,
        },
        "serialization": {
            "education_round_trip": restored == education,
            "program_round_trip": restored_program == learned.emergent,
        },
        "all_reexecute": (
            learned.all_reexecute
            and incompatible.all_reexecute
            and replay.all_reexecute
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
