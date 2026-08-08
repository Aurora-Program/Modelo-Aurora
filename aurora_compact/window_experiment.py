"""Reproducible Aurora 0.18.0-rc2 tensor-window experiment."""

from __future__ import annotations

from . import aurora, fractal_kernel


def _leaf(value: aurora.Triplet) -> aurora.Unit:
    return aurora.Unit.leaf(value)


def _channels(unit: aurora.Unit) -> list[list[int]]:
    return [list(channel) for channel in unit.state.channels]


def run() -> dict[str, object]:
    following = _leaf((1, 1, 1))

    closed = fractal_kernel.FractalWindow.open(
        _leaf((0, 0, 0)), _leaf((0, 0, 0))
    ).deduce()
    opened = fractal_kernel.FractalWindow.open(
        _leaf((0, 0, 0)), _leaf((1, 1, 1))
    ).deduce()
    contradicted = fractal_kernel.FractalWindow.open(
        _leaf((0, 0, 0)), _leaf((0, 2, 2))
    ).deduce()

    opened_next = opened.continue_with(following)
    contradicted_next = contradicted.continue_with(following)

    return {
        "schema": "aurora-tensor-window-experiment-v3",
        "version": "0.18.0rc2",
        "window": ["A", "B", "2_0"],
        "tensor_2": _channels(fractal_kernel.open_unit()),
        "closed": {
            "state": closed.state.value,
            "evolved_2": _channels(closed.evolved),
            "emergent": _channels(closed.emergent),
            "emergent_children": ["A", "B", "2e"],
            "superior": (
                "U(A,B,2e)" if closed.superior is closed.emergent else None
            ),
            "carry": None,
            "evolved_reexecutes": aurora.reexecute(closed.evolved),
            "emergent_reexecutes": aurora.reexecute(closed.emergent),
        },
        "open": {
            "state": opened.state.value,
            "evolved_2": _channels(opened.evolved),
            "superior": None,
            "carry": "2e" if opened.carry is opened.evolved else None,
            "next_window": ["2e", "next", "2_0"],
            "new_tensor_2": opened_next.result is not opened.window.result,
            "evolved_reexecutes": aurora.reexecute(opened.evolved),
        },
        "contradiction": {
            "state": contradicted.state.value,
            "evolved_2": _channels(contradicted.evolved),
            "superior": "A" if contradicted.superior is contradicted.window.a else None,
            "carry": "B" if contradicted.carry is contradicted.window.b else None,
            "next_window": ["B", "next", "2_0"],
            "new_tensor_2": (
                contradicted_next.result is not contradicted.window.result
            ),
            "evolved_reexecutes": aurora.reexecute(contradicted.evolved),
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
