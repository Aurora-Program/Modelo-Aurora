"""Reproducible experiment: Aurora tensors synthesized and executed as code."""

from __future__ import annotations

from . import aurora, tensor_program


P0 = (0, 0, 0)
P1 = (0, 0, 1)
P2 = (0, 0, 2)
P3 = (1, 0, 1)
P4 = (1, 1, 0)
P5 = (1, 1, 1)
P6 = (1, 1, 2)


def route(output_ds=P5) -> tensor_program.ProgramTensor:
    return tensor_program.ProgramTensor.author(
        (P0, P1, P2),
        (P3, P4, output_ds),
        aurora.Direction.INFER_R,
    )


def run() -> dict[str, object]:
    recurrent = route(P5)
    alternative = route(P6)
    learned = tensor_program.induce((recurrent, recurrent, alternative))
    execution = tensor_program.execute(
        (learned.emergent,), {P0: P0, P1: P0, P2: P0}
    )

    incompatible = tensor_program.induce((route(P0), route(P3), route(P6)))
    deduction = tensor_program.ProgramTensor.author(
        (P0, P1, P2),
        (P3, P4, P5),
        aurora.Direction.DEDUCE_B,
    )

    return {
        "schema": "aurora-tensor-program-experiment-v1",
        "code_triplets": tensor_program.CODE_TRIPLETS,
        "runtime_action_table": [],
        "recurrent_induction": {
            "hypotheses_preserved": len(learned.candidates),
            "uses_external_score": False,
            "emergent_equals_recurrent": learned.emergent.values == recurrent.values,
            "emergent_executable": learned.emergent.executable,
            "emergent_ds_address": list(learned.emergent.outputs[2]),
            "executed_ds": [list(value) for value in execution.values(P5)],
        },
        "incompatible_induction": {
            "hypotheses_preserved": len(incompatible.candidates),
            "emergent_ds_address": list(incompatible.emergent.outputs[2]),
            "emergent_executable": incompatible.emergent.executable,
        },
        "deduction_instruction": {
            "de": list(deduction.de),
            "ds": list(deduction.signature),
            "direction": deduction.direction.name,
            "executable": deduction.executable,
        },
        "all_reexecute": (
            learned.all_reexecute
            and incompatible.all_reexecute
            and execution.all_reexecute
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
