"""Reproducible parallel read-write output dictionary experiment."""

from __future__ import annotations

from . import (
    aurora, fractal_dictionary, fractal_dictionary_experiment, output_face,
    tensor_program,
)


P0 = fractal_dictionary_experiment.P0
P1 = fractal_dictionary_experiment.P1
P2 = fractal_dictionary_experiment.P2
P3 = fractal_dictionary_experiment.P3
P4 = fractal_dictionary_experiment.P4


def program(output, phase=(1, 1, 1)) -> tensor_program.ProgramTensor:
    return tensor_program.ProgramTensor.author(
        (P0, P1, P2),
        (P3, P4, output),
        aurora.Direction.INFER_R,
        phase,
    )


def memory_for(programs) -> fractal_dictionary.FractalProgramDictionary:
    memory = fractal_dictionary.FractalProgramDictionary()
    for item in programs:
        memory = memory.remember(item)
    return memory


def reflected(output) -> tensor_program.ProgramTensor:
    """Produce the output requirement from an actual causal firing."""

    source = program(output)
    execution = tensor_program.execute(
        (source,), {P0: P0, P1: P0, P2: P0}
    ).execution
    return tensor_program.ProgramTensor.from_firing(execution.firings[0])


def run() -> dict[str, object]:
    programs = tuple(
        program(output) for output in fractal_dictionary_experiment.OUTPUTS
    )
    memory = memory_for(programs)
    known = (programs[0], programs[4], programs[8])

    all_found = output_face.resolve(memory, known)

    new = reflected((2, 1, 0))
    one_absent = output_face.resolve(memory, (known[0], known[1], new))
    read_back = one_absent.memory_after.search(
        new, aurora.Direction.DEDUCE_B
    )

    second_absent = reflected((2, 2, 0))
    two_absent = output_face.resolve(
        memory, (known[0], new, second_absent)
    )

    open_programs = tuple(
        program(output, aurora.OPEN)
        for output in fractal_dictionary_experiment.OUTPUTS
    )
    open_memory = memory_for(open_programs)
    open_search = output_face.resolve(
        open_memory, (open_programs[0], open_programs[4], open_programs[8])
    )

    return {
        "schema": "aurora-output-face-experiment-v1",
        "runtime_action_table": [],
        "all_found": {
            "states": list(all_found.states),
            "action": all_found.action.value,
            "advance": all_found.can_advance,
        },
        "one_absent": {
            "states": list(one_absent.states),
            "action": one_absent.action.value,
            "crystallized_index": one_absent.crystallized_index,
            "post_states": list(one_absent.post_states or aurora.OPEN),
            "read_back": read_back.state,
            "frontier_by_level": [
                len(nodes) for nodes in one_absent.memory_after.levels
            ],
        },
        "two_absent": {
            "states": list(two_absent.states),
            "action": two_absent.action.value,
            "advance": two_absent.can_advance,
            "returned": len(two_absent.returned),
            "dictionary_unchanged": two_absent.memory_after == memory,
        },
        "open": {
            "states": list(open_search.states),
            "action": open_search.action.value,
            "dictionary_unchanged": open_search.memory_after == open_memory,
            "alternatives": len(open_search.lanes[2].search.alternatives),
        },
        "all_reexecute": (
            all_found.all_reexecute
            and one_absent.all_reexecute
            and two_absent.all_reexecute
            and open_search.all_reexecute
            and new.all_reexecute
            and read_back.state == 1
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
