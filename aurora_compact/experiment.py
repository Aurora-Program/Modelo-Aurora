"""Reproducible 600-sequence learning and distribution-shift experiment."""

from __future__ import annotations

import json
from collections import Counter
from itertools import product
from statistics import mean

from aurora_compact import aurora, stream


def vocabulary() -> tuple[aurora.Triplet, ...]:
    return tuple(value for value in product(range(3), repeat=3)
                 if value != aurora.OPEN and aurora.order_triplet(value).valid)


def corpus() -> tuple[tuple[aurora.Triplet, ...], ...]:
    words = vocabulary()
    if len(words) != 24:
        raise AssertionError("the frozen ordering profile must expose 24 tokens")

    def templates(offset: int) -> tuple[tuple[aurora.Triplet, ...], ...]:
        half = words[offset:offset + 12]
        return tuple((half[i], half[(i + 1) % 12],
                      half[(i + (5 if offset == 0 and i == 4 else 4)) % 12]) * 3
                     for i in range(12))

    before, after = templates(0), templates(12)
    return tuple(before[i % 12] for i in range(300)) + tuple(
        after[i % 12] for i in range(300)
    )


def route() -> tuple[aurora.Triplet, ...]:
    """Explicit exhaustive route; not the still-unfrozen Fibonacci route."""
    return (aurora.OPEN,) + tuple(
        value for value in product(range(3), repeat=3) if value != aurora.OPEN
    )


def boundary_probe() -> dict[str, object]:
    """Count emergent DS values that cannot become a literal next-level unit."""
    words = vocabulary()
    blocked: Counter[str] = Counter()
    for offset in (0, 12):
        half = words[offset:offset + 12]
        for indices in product(range(12), repeat=3):
            unit = aurora.synthesize(
                tuple(aurora.Unit.leaf(half[index]) for index in indices)
            )
            if (unit.value != aurora.OPEN
                    and not aurora.order_triplet(unit.value).valid):
                blocked["".join(map(str, unit.value))] += 1
    return {
        "faces": 2 * 12 ** 3,
        "blocked": sum(blocked.values()),
        "values": dict(sorted(blocked.items())),
    }


def genesis_control_probe() -> dict[str, int]:
    """Read emergent HDS/HDE/HDO after one ordinary genesis pass."""
    counts: Counter[str] = Counter()
    values = tuple(value for value in product(range(3), repeat=3)
                   if value == aurora.OPEN or aurora.order_triplet(value).valid)
    for value in values:
        unit = aurora.Unit.leaf(value)
        try:
            knowledge = aurora.derive_knowledge(unit, unit)
            control = aurora.control_faces(unit, knowledge, unit)
        except aurora.AuroraError:
            counts["blocked"] += 1
            continue
        key = "/".join((
            control.operation.name,
            control.coherence.name,
            control.scope.name,
        ))
        counts[key] += 1
    return dict(sorted(counts.items()))


def run() -> dict[str, object]:
    result = stream.learn_stream(corpus(), do_route=route())
    observations = result.observations
    ranges = ((0, 50), (100, 150), (250, 300),
              (300, 350), (550, 600))
    blocks = []
    for start, end in ranges:
        block = observations[start:end]
        blocks.append({
            "range": f"{start}-{end}",
            "mean_logical_cost": round(mean(x.logical_cost for x in block), 2),
            "lexicalized": sum(x.lexicalized for x in block),
            "new_relations": sum(x.new_relations for x in block),
            "rejections": sum(x.rejected for x in block),
            "dictionary_size_end": block[-1].dictionary_size,
        })
    return {
        "profile": "aurora-compact-0.6-experiment",
        "sequences": len(observations),
        "tokens_per_sequence": 9,
        "vocabulary": len(vocabulary()),
        "distribution_shift_at": 300,
        "final_dictionary_size": len(result.dictionary.entries),
        "total_new_relations": sum(x.new_relations for x in observations),
        "total_reuses": sum(x.reused for x in observations),
        "total_rejections": sum(x.rejected for x in observations),
        "lexicalized_sequences": sum(x.lexicalized for x in observations),
        "genesis_control_after_one_pass": genesis_control_probe(),
        "literal_boundary_probe": boundary_probe(),
        "blocks": blocks,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
