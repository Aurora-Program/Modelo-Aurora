"""Reproduce the finite-state and behavioral audit for Aurora 0.18.0-rc2."""

from __future__ import annotations

import json
from collections import Counter
from itertools import product

from aurora_compact import (
    aurora, context_experiment, downward_experiment, education_experiment,
    experiment, fractal_dictionary_experiment, fractal_kernel, growth,
    provenance_experiment,
    orientation_experiment, output_face_experiment, tensor_program_experiment,
    release_candidate_experiment, training, window_experiment,
)


def _counts(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def audit() -> dict[str, object]:
    triplets = list(product(range(3), repeat=3))
    processible = [
        p for p in triplets if aurora.order_triplet(p).valid or p == aurora.OPEN
    ]
    report: dict[str, object] = {
        "profile": "aurora-compact-0.18.0rc2",
        "triplets_total": len(triplets),
        "triplets_processible": len(processible),
        "literal_impossible": [list(p) for p in triplets if p not in processible],
        "directions": {},
    }
    directions: dict[str, object] = {}
    for direction in aurora.Direction:
        states: Counter[str] = Counter()
        domains: Counter[int] = Counter()
        for a, b, m, r in product(range(3), repeat=4):
            packet = aurora.trigate(a, b, m, r, direction)
            states[packet.state.value] += 1
            domains[len(packet.candidates)] += 1

        face_states: Counter[str] = Counter()
        window_states: Counter[str] = Counter()
        control_operations: Counter[str] = Counter()
        control_coherences: Counter[str] = Counter()
        control_scopes: Counter[str] = Counter()
        complete_control_tensors = 0
        fixed_points = 0
        max_trace = 0
        for inputs in product(processible, repeat=3):
            face_result = aurora.face(inputs, direction)
            face_states[aurora.classify_de(face_result.knowledge.de).value] += 1
            window = aurora.resolve_window(inputs, direction)
            window_states[window.state.value] += 1
            fixed_points += window.fixed_point
            max_trace = max(max_trace, len(window.trace))
            units = tuple(aurora.Unit.leaf(value) for value in inputs)
            control = aurora.control_faces(*units, direction=direction)
            control_operations[control.operation.name] += 1
            control_coherences[control.coherence.name] += 1
            control_scopes[control.scope.name] += 1
            complete_control_tensors += control.knowledge.ds == (
                int(control.operation), int(control.coherence), int(control.scope)
            )
        directions[direction.name] = {
            "trigate_cases": 81,
            "trigate_states": _counts(states),
            "candidate_domain_sizes": dict(sorted(domains.items())),
            "face_cases": sum(face_states.values()),
            "face_states": _counts(face_states),
            "window_states": _counts(window_states),
            "window_fixed_points": fixed_points,
            "window_max_trace": max_trace,
            "control_operations": _counts(control_operations),
            "control_coherences": _counts(control_coherences),
            "control_scopes": _counts(control_scopes),
            "complete_control_tensors": complete_control_tensors,
        }
    report["directions"] = directions
    tensor_window_states: Counter[str] = Counter()
    tensor_window_reexecutions = 0
    tensor_window_emergences = 0
    tensor_window_emergence_reexecutions = 0
    non_orderable_positive_rejections = 0
    tensor_window_transitions = 0
    for a_value, b_value in product(processible, repeat=2):
        a, b = aurora.Unit.leaf(a_value), aurora.Unit.leaf(b_value)
        resolved = fractal_kernel.FractalWindow.open(a, b).deduce()
        tensor_window_states[resolved.state.value] += 1
        tensor_window_reexecutions += aurora.reexecute(resolved.evolved)
        if resolved.state is aurora.RelationState.CLOSED:
            tensor_window_emergences += 1
            tensor_window_emergence_reexecutions += aurora.reexecute(
                resolved.emergent
            )
            valid = (
                resolved.superior is resolved.emergent
                and resolved.superior is not resolved.evolved
                and resolved.emergent is not None
                and resolved.emergent.children == (a, b, resolved.evolved)
                and aurora.reexecute(resolved.emergent)
                and resolved.carry is None
            )
        elif resolved.state is aurora.RelationState.OPEN:
            valid = (
                resolved.superior is None
                and resolved.emergent is None
                and resolved.carry is resolved.evolved
            )
        else:
            non_orderable_positive_rejections += (
                resolved.evolved.value != aurora.OPEN
                and aurora.majority3(*resolved.evolved.state.de) == 1
                and not aurora.order_triplet(resolved.evolved.value).valid
            )
            valid = (
                resolved.superior is a
                and resolved.emergent is None
                and resolved.carry is b
            )
        tensor_window_transitions += valid
    report["tensor_window_audit"] = {
        "cases": sum(tensor_window_states.values()),
        "states": _counts(tensor_window_states),
        "all_evolved_results_reexecute": (
            tensor_window_reexecutions == sum(tensor_window_states.values())
        ),
        "coherent_emergences": tensor_window_emergences,
        "all_coherent_emergences_reexecute": (
            tensor_window_emergence_reexecutions == tensor_window_emergences
        ),
        "non_orderable_positive_rejections": (
            non_orderable_positive_rejections
        ),
        "all_transitions_preserve_identity": (
            tensor_window_transitions == sum(tensor_window_states.values())
        ),
        "shape": ["A", "B", "2_0"],
    }
    context = (0, 0, 0)
    input_unit = aurora.Unit.leaf(context)
    genesis = aurora.transcend(input_unit, aurora.AuroraDictionary())
    known_output = aurora.Unit.leaf((1, 1, 1))
    memory = aurora.AuroraDictionary().register(known_output)
    learned = aurora.transcend(input_unit, memory, initial_output=known_output)
    behavior = aurora.transcend(input_unit, learned.dictionary,
                                initial_output=input_unit, tick=20)
    bad = aurora.Relation(input_unit, aurora.Unit(aurora.EMPTY_KNOWLEDGE),
                          input_unit, successful_uses=10)
    competition = aurora.transcend(
        input_unit, aurora.AuroraDictionary().add(bad),
        do_route=(aurora.OPEN, (1, 1, 1)),
    )
    fractal = aurora.process_fractal(
        (context,) * 9, do_route=(aurora.OPEN, (1, 1, 1)),
    )
    report["behavioral_probe"] = {
        "genesis_action": genesis.trace[0].action.value,
        "genesis_output_equals_input": genesis.output == input_unit,
        "initial_output": list(behavior.trace[0].output_before.value),
        "actions": [attempt.action.value for attempt in behavior.trace],
        "do_route_consumed": [list(attempt.do) for attempt in behavior.trace],
        "final_state": behavior.state.value,
        "final_output": list(behavior.output.value),
        "winner_promoted_to": behavior.dictionary.entries[0].successful_uses,
        "competition_actions": [a.action.value for a in competition.trace],
        "alternatives_preserved": len(competition.dictionary.entries),
        "fractal_levels": [len(level) for level in fractal.levels],
        "fractal_relations": len(fractal.dictionary.entries),
    }
    report["sequential_probe"] = experiment.run()
    growth_units = tuple(aurora.Unit.leaf(value) for value in (
        (0, 0, 0), (1, 1, 1), aurora.OPEN, (0, 0, 0), (0, 0, 0),
    ))
    growth_result = growth.grow_level(growth_units)
    report["growth_probe"] = {
        "actions": [attempt.action.value for attempt in growth_result.attempts],
        "states": [attempt.state.value for attempt in growth_result.attempts],
        "support": [attempt.support for attempt in growth_result.attempts],
        "emerged_source_widths": [node.width for node in growth_result.emerged],
        "residual": len(growth_result.residual),
        "relations": len(growth_result.dictionary.entries),
    }
    a = aurora.Unit.leaf((0, 0, 0))
    b = aurora.Unit.leaf((0, 0, 1))
    segmentation = growth.compete_level((a, a, b) * 3)
    selected = segmentation.selected
    report["segmentation_probe"] = {
        "overlapping_candidates": len(segmentation.candidates),
        "distinct_relations": len(segmentation.dictionary.entries),
        "compatible_hypotheses": segmentation.hypothesis_count,
        "winners": len(segmentation.winners),
        "selected_spans": [
            [candidate.start, candidate.stop]
            for candidate in selected.segments
        ] if selected is not None else [],
        "selected_support": [
            candidate.support for candidate in selected.segments
        ] if selected is not None else [],
    }
    probe_text = "luna"
    before_training = training.evaluate_text(training.TrainingState(), probe_text)
    trained_state = training.observe_text(
        training.TrainingState(), "una luna."
    ).state
    after_training = training.evaluate_text(trained_state, probe_text)
    after_selected = after_training.growth.levels[0].selected
    report["training_probe"] = {
        "observations": trained_state.observation_count,
        "relations": len(trained_state.dictionary.entries),
        "winners_before": len(before_training.growth.levels[0].winners),
        "winners_after": len(after_training.growth.levels[0].winners),
        "selected_forms": [
            probe_text[candidate.node.span[0]:candidate.node.span[1]]
            for candidate in after_selected.segments
        ] if after_selected is not None else [],
        "all_relations_reexecute": all(
            relation.reexecutes_for(relation.input)
            for relation in trained_state.dictionary.entries
        ),
    }
    contextual = context_experiment.run()
    report["contextual_reading_probe"] = {
        "observations": contextual.state.observation_count,
        "relations": len(contextual.state.dictionary.entries),
        "probes": [
            {
                "text": text,
                "winners_before": len(training.evaluate_text(
                    training.TrainingState(), text
                ).winners),
                "winners_after": len(result.winners),
                "total_readings": result.total_readings,
                "evaluated_readings": result.evaluated_readings,
                "pruned_readings": result.pruned_readings,
                "selected": list(result.selected.senses)
                if result.selected is not None else [],
                "expected": list(expected),
            }
            for text, expected in context_experiment.PROBES
            for result in (training.evaluate_text(contextual.state, text),)
        ],
    }
    downward = downward_experiment.run()
    report["downward_selection_probe"] = {
        "all_equivalent_to_exhaustive": all(
            item.equivalent for item in downward.probes
        ),
        "probes": [
            {
                "text": item.text,
                "total_readings": item.total_readings,
                "evaluated_readings": item.evaluated_readings,
                "pruned_readings": item.pruned_readings,
                "routes": item.routes,
                "closed_positions": list(item.closed_positions),
                "equivalent": item.equivalent,
            }
            for item in downward.probes
        ],
    }
    report["universal_relational_probe"] = education_experiment.run()
    report["tensor_program_probe"] = tensor_program_experiment.run()
    report["provenance_program_probe"] = provenance_experiment.run()
    report["fractal_dictionary_probe"] = fractal_dictionary_experiment.run()
    report["parallel_output_face_probe"] = output_face_experiment.run()
    report["fractal_orientation_probe"] = orientation_experiment.run()
    report["release_candidate_probe"] = release_candidate_experiment.run()
    report["corrected_tensor_window_probe"] = window_experiment.run()
    return report


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
