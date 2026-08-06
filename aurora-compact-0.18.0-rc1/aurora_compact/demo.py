"""Run Aurora's genesis, reuse and fractal dialogue."""

from __future__ import annotations

import json

from aurora_compact import (
    aurora, characters, control, deduction, growth, routing, tokens, training,
)


def run() -> dict[str, object]:
    context = (0, 0, 0)
    input_unit = aurora.Unit.leaf(context)
    genesis = aurora.transcend(input_unit, aurora.AuroraDictionary())
    known_output = aurora.Unit.leaf((1, 1, 1))
    memory = aurora.AuroraDictionary().register(known_output)
    learned = aurora.transcend(
        input_unit, memory, initial_output=known_output,
    )
    reused = aurora.transcend(
        input_unit, learned.dictionary, initial_output=input_unit, tick=20,
    )
    fractal = aurora.process_fractal(
        (context,) * 9, do_route=(aurora.OPEN, (1, 1, 1)),
    )
    expert_value = (1, 1, 1)
    expert_unit = aurora.Unit.leaf(expert_value)
    expert_memory = aurora.transcend(
        expert_unit, aurora.AuroraDictionary()
    ).dictionary
    network = routing.Network((
        routing.Node("local", (context,), genesis.dictionary),
        routing.Node("expert", (expert_value,), expert_memory),
    ))
    query = deduction.DeductiveQuery.for_exact_tensor(expert_value)
    remote = network.resolve(
        "local", query, control.SearchScope.NETWORK, tick=1,
    )
    number_names = tokens.numeric_lexicon(("cero", "uno", "dos", "tres"))
    character_lexicon = characters.spanish_character_lexicon()
    vowel_a = character_lexicon.lookup("a")[0]
    period = character_lexicon.lookup(".")[0]
    character_growth = growth.grow_text("aaaaaaaaa", character_lexicon)
    a = aurora.Unit.leaf((0, 0, 0))
    b = aurora.Unit.leaf((0, 0, 1))
    competition = growth.compete_level((a, a, b) * 3)
    selected = competition.selected
    before_training = training.evaluate_text(training.TrainingState(), "luna")
    trained = training.observe_text(
        training.TrainingState(), "una luna."
    ).state
    after_training = training.evaluate_text(trained, "luna")
    return {
        "genesis": {
            "input": input_unit.value,
            "output": genesis.output.value,
            "knowledge": genesis.knowledge.value,
            "action": genesis.trace[0].action.value,
        },
        "reuse": {
            "output_before": reused.trace[0].output_before.value,
            "output_after": reused.output.value,
            "action": reused.trace[0].action.value,
        },
        "fractal_levels": [len(level) for level in fractal.levels],
        "fractal_relations": len(fractal.dictionary.entries),
        "control_table": {
            "hds_112": control.interpret(
                (1, 1, 2), (1, 1, 2), (0, 0, 0)
            )[0].name,
            "hde_112": control.interpret(
                (1, 1, 2), (1, 1, 2), (0, 0, 0)
            )[1].name,
            "hdo_000": control.interpret(
                (1, 1, 2), (1, 1, 2), (0, 0, 0)
            )[2].name,
        },
        "network": {
            "resolved_by": remote.node_id,
            "route_learned": remote.learned_route,
            "route_tensor": remote.network.routes[0].tensor,
        },
        "simple_token": {
            "text": "tres",
            "tensor": number_names.lookup("tres")[0].ds,
        },
        "character_tensor": {
            "text": vowel_a.text,
            "family": vowel_a.family.value,
            "levels": (1, 3, 9),
            "triplets": len(vowel_a.triplets),
            "trits": len(vowel_a.trits),
            "reexecutes": vowel_a.reexecutes,
            "period_pause": period.get_property(
                characters.SemanticRole.FUNCTION, "pause"
            ).value,
        },
        "character_growth": {
            "levels": [len(level.emerged)
                       for level in character_growth.growth.levels],
            "complete": character_growth.growth.complete,
            "root_width": character_growth.growth.root.width,
            "relations": len(character_growth.growth.dictionary.entries),
        },
        "segmentation_competition": {
            "overlapping_candidates": len(competition.candidates),
            "compatible_hypotheses": competition.hypothesis_count,
            "winners": len(competition.winners),
            "selected_spans": [
                (candidate.start, candidate.stop)
                for candidate in selected.segments
            ] if selected is not None else [],
            "selected_support": [
                candidate.support for candidate in selected.segments
            ] if selected is not None else [],
        },
        "incremental_training": {
            "probe": "luna",
            "winners_before": len(before_training.growth.levels[0].winners),
            "winners_after": len(after_training.growth.levels[0].winners),
            "relations": len(trained.dictionary.entries),
            "observations": trained.observation_count,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
