"""Reproducible Aurora 0.18.0-rc1 autosimilarity experiment."""

from __future__ import annotations

from . import aurora, fractal_kernel


CHILDREN = ((0, 0, 0), (1, 0, 1), aurora.OPEN)
CURRENT = fractal_kernel.FractalAddress((0, 0, 0), (0, 1, 0))
UPPER = fractal_kernel.FractalAddress((0, 0, 1), (0, 1, 0))
TOPOLOGY = fractal_kernel.FractalTopology(
    ((CURRENT,), (UPPER,), (CURRENT, UPPER))
)


def _triplets(unit: aurora.Unit) -> list[list[int]]:
    return [list(channel) for channel in unit.state.channels]


def run() -> dict[str, object]:
    children = tuple(aurora.Unit.leaf(value) for value in CHILDREN)
    unit = aurora.synthesize(children, aurora.Direction.LEARN_M)
    window = fractal_kernel.FractalWindow(TOPOLOGY)

    memory = fractal_kernel.FractalTensorDictionary().remember(unit)
    lookups = tuple(
        memory.search(unit.state.channels[index], aurora.Direction(index))
        for index in range(3)
    )
    passages = tuple(
        window.pass_unit(unit, aurora.Direction(index))
        for index in range(3)
    )
    triplet = fractal_kernel.pass_triplet((1, 1, 2), TOPOLOGY)
    open_triplet = fractal_kernel.pass_triplet(aurora.OPEN, TOPOLOGY)

    promoted = fractal_kernel.FractalTensorDictionary()
    for _ in range(9):
        promoted = promoted.remember(unit)
    root = promoted.root
    if root is None:
        raise aurora.AuroraError("release-candidate experiment needs one root")
    root_reads = tuple(
        promoted.search(root.unit.state.channels[index], aurora.Direction(index))
        for index in range(3)
    )

    return {
        "schema": "aurora-release-candidate-experiment-v1",
        "version": "0.18.0rc1",
        "emergent_unit": {
            "k": _triplets(unit),
            "children": len(unit.children),
            "reexecutes": aurora.reexecute(unit),
        },
        "three_index_dictionary": {
            "states": [lookup.state for lookup in lookups],
            "channels": [lookup.channel.name for lookup in lookups],
            "same_identity": all(lookup.selected is unit for lookup in lookups),
            "full_k": [
                _triplets(lookup.selected)
                for lookup in lookups
                if lookup.selected is not None
            ],
            "outgoing_o": [lookup.outgoing[0] for lookup in lookups],
            "stored_nodes": len(memory.nodes),
        },
        "window_boundary": {
            "incoming_c": [int(passage.incoming) for passage in passages],
            "outgoing_o": [passage.outgoing for passage in passages],
            "next_c": [int(passage.next_c) for passage in passages],
            "destinations": [
                [
                    {"scale": list(address.scale), "cell": list(address.cell)}
                    for address in passage.destinations
                ]
                for passage in passages
            ],
            "same_identity": all(passage.unit is unit for passage in passages),
            "open_preserves_both": len(passages[0].destinations) == 2,
            "upper_selected": passages[1].destinations == (UPPER,),
            "current_selected": passages[2].destinations == (CURRENT,),
        },
        "triplet_passage": {
            "resolved_orientations": list(triplet.orientations),
            "open_orientations": list(open_triplet.orientations),
            "open_destinations": len(open_triplet.destinations),
        },
        "promotion": {
            "levels": [len(level) for level in promoted.levels],
            "root_level": root.level,
            "root_leaves": root.leaf_count,
            "root_reexecutes": root.all_reexecute,
            "three_index_states": [lookup.state for lookup in root_reads],
            "same_root": all(lookup.selected is root.unit for lookup in root_reads),
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
