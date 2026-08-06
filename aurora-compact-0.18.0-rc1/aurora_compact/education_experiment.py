"""Reproducible probes for the universal relational Aurora executor."""

from __future__ import annotations

from . import aurora, relational


def _seed(name: str, inputs: tuple[str, str, str], prefix: str):
    return relational.OperationalSeed.from_tensor(
        name,
        inputs,
        (f"{prefix}.do", f"{prefix}.de", f"{prefix}.ds"),
        relational.instruction_tensor(aurora.Direction.INFER_R),
    )


def vertical_education() -> relational.Education:
    """Present nine leaves as three faces and re-present their three DS."""

    return relational.Education((
        _seed("lower-0", ("x0", "x1", "x2"), "g0"),
        _seed("lower-1", ("x3", "x4", "x5"), "g1"),
        _seed("lower-2", ("x6", "x7", "x8"), "g2"),
        _seed("upper", ("g0.ds", "g1.ds", "g2.ds"), "root"),
    ))


def open_then_close_education() -> relational.Education:
    """Re-present an open DS with the next two values; no carry action exists."""

    return relational.Education((
        _seed("first", ("x0", "x1", "x2"), "first"),
        _seed("continue", ("first.ds", "x3", "x4"), "second"),
    ))


def run() -> dict[str, object]:
    vertical = relational.execute(
        vertical_education(),
        {f"x{index}": (0, 0, 0) for index in range(9)},
    )
    continued = relational.execute(
        open_then_close_education(),
        {
            "x0": (0, 0, 0),
            "x1": (1, 1, 1),
            "x2": aurora.OPEN,
            "x3": (0, 0, 0),
            "x4": (0, 0, 0),
        },
    )
    return {
        "runtime_actions": [],
        "vertical": {
            "firings": len(vertical.firings),
            "root_ds": list(vertical.values("root.ds")[0]),
            "root_de": list(vertical.values("root.de")[0]),
            "root_depth": vertical.signals("root.ds")[0].depth,
            "fixed_point": vertical.fixed_point,
        },
        "open_then_close": {
            "firings": len(continued.firings),
            "first_de": list(continued.values("first.de")[0]),
            "second_de": list(continued.values("second.de")[0]),
            "second_ds": list(continued.values("second.ds")[0]),
            "fixed_point": continued.fixed_point,
        },
        "all_reexecute": vertical.all_reexecute and continued.all_reexecute,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
