"""First reproducible Aurora experiment over unlabelled Spanish character streams."""

from __future__ import annotations

from . import growth, training


CORPUS = (
    "la luna sale.",
    "mi luna brilla.",
    "una luna sube.",
    "esa luna brilla.",
    "la luna alta.",
    "la luna rota.",
    "sale la luna.",
    "el sol sale.",
    "sale el sol.",
    "mi mama sale.",
    "la rosa sale.",
    "la mesa alta.",
)


def selected_forms(
    result: growth.CompetitiveTextGrowth,
    text: str,
) -> tuple[str, ...]:
    level = result.growth.levels[0]
    selected = level.selected
    if selected is None:
        return ()
    return tuple(
        text[candidate.node.span[0]:candidate.node.span[1]]
        for candidate in selected.segments
    )


def run(epochs: int = 3) -> training.CorpusTraining:
    return training.train_corpus(CORPUS, epochs=epochs)


def main() -> None:
    probe = "luna"
    before = training.evaluate_text(training.TrainingState(), probe)
    trained = run()
    after = training.evaluate_text(trained.state, probe)

    print("Aurora corpus experiment 0.9")
    print(f"observations={trained.state.observation_count}")
    print(f"relations={len(trained.state.dictionary.entries)}")
    print(
        f"probe={probe!r} winners_before="
        f"{len(before.growth.levels[0].winners)} "
        f"winners_after={len(after.growth.levels[0].winners)}"
    )
    print(f"selected_after={selected_forms(after, probe)!r}")
    print("top recurrent closures:")
    for closure in training.ranked_closures(trained.state)[:12]:
        forms = ", ".join(
            f"{item.text!r}:{item.count}" for item in closure.forms[:3]
        )
        print(
            f"  support={closure.support:>3} "
            f"observations={closure.observation_count:>2} forms={forms}"
        )


if __name__ == "__main__":
    main()
