"""Reproducible downward-selection experiment for Aurora 0.11."""

from __future__ import annotations

from dataclasses import dataclass

from . import context_experiment, growth, training


COMBINED_PROBE = " cama gesto soy "


@dataclass(frozen=True)
class PruningProbe:
    """Cost and semantic-equivalence record for one unlabelled text."""

    text: str
    total_readings: int
    evaluated_readings: int
    pruned_readings: int
    routes: int
    closed_positions: tuple[int, ...]
    selected_senses: tuple[tuple[int, str], ...] | None
    exhaustive_senses: tuple[tuple[int, str], ...] | None

    @property
    def equivalent(self) -> bool:
        return self.selected_senses == self.exhaustive_senses


@dataclass(frozen=True)
class DownwardExperiment:
    """Trained memory plus independent and combined selection probes."""

    training: training.CorpusTraining
    probes: tuple[PruningProbe, ...]


def _senses(result: growth.ContextualTextGrowth) -> tuple[tuple[int, str], ...] | None:
    return None if result.selected is None else result.selected.senses


def run() -> DownwardExperiment:
    """Compare selected execution with the exhaustive 0.10 baseline."""
    trained = context_experiment.run()
    texts = tuple(text for text, _ in context_experiment.PROBES) + (COMBINED_PROBE,)
    probes: list[PruningProbe] = []
    for text in texts:
        selected = training.evaluate_text(trained.state, text)
        exhaustive = training.evaluate_text(
            trained.state,
            text,
            downward=False,
        )
        probes.append(PruningProbe(
            text,
            selected.total_readings,
            selected.evaluated_readings,
            selected.pruned_readings,
            len(selected.selection.routes),
            selected.selection.closed_positions,
            _senses(selected),
            _senses(exhaustive),
        ))
    return DownwardExperiment(trained, tuple(probes))


def main() -> None:
    experiment = run()
    print("Aurora downward-selection experiment 0.11")
    print(f"observations={experiment.training.state.observation_count}")
    print(f"relations={len(experiment.training.state.dictionary.entries)}")
    for probe in experiment.probes:
        print(
            f"probe={probe.text!r} total={probe.total_readings} "
            f"evaluated={probe.evaluated_readings} pruned={probe.pruned_readings} "
            f"closed={probe.closed_positions!r} "
            f"selected={probe.selected_senses!r} "
            f"equivalent={probe.equivalent}"
        )


if __name__ == "__main__":
    main()
