"""Reproducible contextual-reading experiment for Aurora 0.10."""

from __future__ import annotations

from . import growth, training


GROUNDED_CORPUS = (
    training.TrainingSample.from_text(" casa", {1: "velar"}),
    training.TrainingSample.from_text(" cena", {1: "coronal"}),
    training.TrainingSample.from_text(" gato", {1: "voiced"}),
    training.TrainingSample.from_text(" gente", {1: "fricative"}),
    training.TrainingSample.from_text(" hoy ", {3: "vowel"}),
    training.TrainingSample.from_text(" ya ", {1: "consonant"}),
)


PROBES = (
    (" cama", ((1, "velar"),)),
    (" cero", ((1, "coronal"),)),
    (" gana", ((1, "voiced"),)),
    (" gesto", ((1, "fricative"),)),
    (" soy ", ((3, "vowel"),)),
    (" ya ", ((1, "consonant"),)),
)


def run(epochs: int = 4) -> training.CorpusTraining:
    """Ground six closures; probes themselves remain unlabelled."""
    return training.train_corpus(GROUNDED_CORPUS, epochs=epochs)


def selected_senses(
    result: growth.ContextualTextGrowth,
) -> tuple[tuple[int, str], ...] | None:
    selected = result.selected
    return None if selected is None else selected.senses


def main() -> None:
    empty = training.TrainingState()
    trained = run()
    print("Aurora contextual experiment 0.10")
    print(f"observations={trained.state.observation_count}")
    print(f"relations={len(trained.state.dictionary.entries)}")
    for text, expected in PROBES:
        before = training.evaluate_text(empty, text)
        after = training.evaluate_text(trained.state, text)
        print(
            f"probe={text!r} winners_before={len(before.winners)} "
            f"winners_after={len(after.winners)} "
            f"selected={selected_senses(after)!r} expected={expected!r}"
        )


if __name__ == "__main__":
    main()
