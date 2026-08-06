"""Reproducible orientation audit from triplet to emergent control."""

from __future__ import annotations

from . import aurora, control, orientation, relational, tensor_program


P0 = (0, 0, 0)
P1 = (0, 0, 1)
P2 = (0, 0, 2)
P3 = (1, 0, 1)
P4 = (1, 1, 0)


def _channels(unit: aurora.Unit) -> list[list[int]]:
    return [list(channel) for channel in unit.state.channels]


def run() -> dict[str, object]:
    ordered = orientation.orient_triplet((1, 1, 2), 2)
    inherited = orientation.inherit_es(
        ((0, 0, 2), (1, 1, 2), (0, 0, 0)), 1
    )

    instruction = relational.instruction_tensor(
        aurora.Direction.INFER_R, (0, 1, 2)
    )
    program = tensor_program.ProgramTensor.author(
        (P0, P1, P2), (P3, P4, (1, 1, 1)),
        aurora.Direction.INFER_R, (0, 1, 2),
    )
    compiled = program.compile("orientation")

    window = aurora.resolve_window((aurora.OPEN,) * 3)
    if window.carry is None:
        raise aurora.AuroraError("orientation audit expected an open carry")
    input_unit = aurora.Unit.leaf((1, 0, 0))
    controlled = control.control_faces(
        input_unit, input_unit, aurora.Unit.leaf(aurora.OPEN)
    )

    same = aurora.Unit(aurora.Knowledge(
        (0, 1, 2), (1, 1, 1), (0, 0, 0)
    ))
    presentations = tuple(orientation.present(same, index) for index in range(3))
    chain_units = (
        aurora.Unit(aurora.Knowledge((1, 2, 0), (1, 1, 1), P0)),
        aurora.Unit(aurora.Knowledge((2, 0, 1), (1, 1, 1), P1)),
        aurora.Unit(aurora.Knowledge((0, 1, 2), (1, 1, 1), P2)),
    )
    linked = orientation.chain(chain_units, 0)

    return {
        "schema": "aurora-fractal-orientation-experiment-v1",
        "triplet": {
            "value": [1, 1, 2],
            "phase": 2,
            "o": ordered.o,
            "es": ordered.es,
            "es_is_value_at_o": (
                ordered.o is not None
                and ordered.es == ordered.ordering.original[ordered.o]
            ),
        },
        "vertical": {
            "upper_o": inherited.upper_o,
            "selected": list(inherited.selected),
            "es": inherited.es,
        },
        "operational_seed": {
            "c": int(compiled.direction),
            "k": _channels(compiled.tensor),
            "same_instruction": compiled.tensor == instruction,
        },
        "window": {
            "k": _channels(window.carry.unit),
            "children": len(window.carry.unit.children),
            "reexecutes": window.carry.reexecutes,
        },
        "control": {
            "k": _channels(controlled.unit),
            "ds_readings": [
                int(controlled.operation), int(controlled.coherence),
                int(controlled.scope),
            ],
            "ds_is_control_triplet": controlled.unit.state.ds == (
                int(controlled.operation), int(controlled.coherence),
                int(controlled.scope),
            ),
            "reexecutes": controlled.reexecutes,
        },
        "same_unit_three_orientations": {
            "incoming": [step.incoming for step in presentations],
            "outgoing": [step.outgoing for step in presentations],
            "identity_preserved": all(step.unit is same for step in presentations),
        },
        "c_o_chain": {
            "incoming": [step.incoming for step in linked],
            "outgoing": [step.outgoing for step in linked],
            "all_reexecute": all(aurora.reexecute(step.unit) for step in linked),
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
