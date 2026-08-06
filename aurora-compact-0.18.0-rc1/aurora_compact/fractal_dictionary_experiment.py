"""Reproducible C-O dictionary orientation and feedback experiment."""

from __future__ import annotations

from . import aurora, fractal_dictionary, tensor_program


P0 = (0, 0, 0)
P1 = (0, 0, 1)
P2 = (0, 0, 2)
P3 = (1, 0, 1)
P4 = (1, 1, 0)
OUTPUTS = (
    (1, 1, 1),
    (1, 1, 2),
    (1, 2, 1),
    (0, 1, 0),
    (1, 2, 0),
    (1, 2, 2),
    (2, 0, 0),
    (2, 0, 1),
    (2, 0, 2),
)


def route(output, phase=(1, 1, 1)) -> tensor_program.ProgramTensor:
    return tensor_program.ProgramTensor.author(
        (P0, P1, P2),
        (P3, P4, output),
        aurora.Direction.INFER_R,
        phase,
    )


def memory_for(programs) -> fractal_dictionary.FractalProgramDictionary:
    memory = fractal_dictionary.FractalProgramDictionary()
    for program in programs:
        memory = memory.remember(program)
    return memory


def run() -> dict[str, object]:
    programs = tuple(route(output) for output in OUTPUTS)
    ordered = memory_for(programs)
    routes = {
        "learning": ordered.route(aurora.Direction.LEARN_M),
        "inference": ordered.route(aurora.Direction.INFER_R),
        "deduction_o0": ordered.route(
            aurora.Direction.DEDUCE_B, (0, 0, 0)
        ),
        "deduction_o2": ordered.route(
            aurora.Direction.DEDUCE_B, aurora.OPEN
        ),
    }

    open_memory = memory_for(
        tuple(route(output, aurora.OPEN) for output in OUTPUTS)
    )
    open_route = open_memory.route(aurora.Direction.DEDUCE_B)

    recurrent = route(OUTPUTS[0], aurora.OPEN)
    alternative = route(OUTPUTS[1], aurora.OPEN)
    observed = (
        recurrent, recurrent, alternative,
        recurrent, alternative, recurrent,
        alternative, recurrent, recurrent,
    )
    feedback = fractal_dictionary.FractalProgramDictionary()
    for program in observed:
        execution = tensor_program.execute(
            (program,), {P0: P0, P1: P0, P2: P0}
        ).execution
        feedback = feedback.observe(execution)
    root = feedback.complete_root
    if root is None:
        raise aurora.AuroraError("feedback experiment did not form a root")
    replay = feedback.execute_root({P0: P0, P1: P0, P2: P0})

    return {
        "schema": "aurora-fractal-dictionary-experiment-v1",
        "runtime_action_table": [],
        "levels": [9, 3, 1],
        "frontier_by_level": [len(nodes) for nodes in ordered.levels],
        "mode_routes": {
            name: {
                "indices": list(result.indices),
                "output_address": list(result.selected.outputs[2])
                if result.selected is not None else None,
            }
            for name, result in routes.items()
        },
        "open_order": {
            "resolved": open_route.resolved,
            "alternatives": len(open_route.alternatives),
        },
        "feedback": {
            "observed_programs": len(observed),
            "root_level": root.level,
            "root_leaves": root.leaf_count,
            "root_equals_recurrent": root.program.values == recurrent.values,
            "root_executable": root.program.executable,
            "replayed_ds": [list(value) for value in replay.values(OUTPUTS[0])],
        },
        "all_reexecute": (
            ordered.complete_root is not None
            and ordered.complete_root.all_reexecute
            and root.all_reexecute
            and replay.all_reexecute
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
