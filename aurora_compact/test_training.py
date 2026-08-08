import tempfile
import unittest
from pathlib import Path

from aurora_compact import (
    aurora, context_experiment, downward_experiment, growth, training,
)


class IncrementalTrainingTests(unittest.TestCase):
    def test_ambiguous_real_text_keeps_both_closures(self):
        step = training.observe_text(training.TrainingState(), "luna")
        level = step.result.growth.levels[0]
        self.assertEqual(len(level.winners), 2)
        self.assertEqual(len(step.state.dictionary.entries), 2)
        self.assertEqual(
            {item.text for evidence in step.state.evidence
             for item in evidence.forms},
            {"lun", "una"},
        )
        self.assertEqual(step.observation.new_relations, 2)
        self.assertEqual(step.observation.reused_events, 0)

    def test_repeated_observation_promotes_without_duplication(self):
        first = training.observe_text(training.TrainingState(), "luna")
        second = training.observe_text(first.state, "luna")
        self.assertEqual(len(second.state.dictionary.entries), 2)
        self.assertEqual(second.observation.new_relations, 0)
        self.assertEqual(second.observation.reused_events, 2)
        self.assertEqual(
            sorted(item.support for item in training.ranked_closures(second.state)),
            [2, 2],
        )
        self.assertEqual(second.state.observation_count, 2)
        self.assertGreater(second.state.tick, first.state.tick)

    def test_contextual_recurrence_breaks_a_surface_tie(self):
        empty = training.TrainingState()
        before = training.evaluate_text(empty, "luna")
        self.assertEqual(len(before.growth.levels[0].winners), 2)

        learned = training.observe_text(empty, "una luna.").state
        after = training.evaluate_text(learned, "luna")
        level = after.growth.levels[0]
        self.assertTrue(level.resolved)
        self.assertEqual(
            ["luna"[candidate.node.span[0]:candidate.node.span[1]]
             for candidate in level.selected.segments],
            ["una"],
        )
        self.assertGreater(
            level.selected.segments[0].support,
            next(candidate.support for candidate in level.candidates
                 if candidate.node.span == (0, 3)),
        )

    def test_evaluation_does_not_commit_memory(self):
        state = training.observe_text(training.TrainingState(), "una luna.").state
        before = training.state_to_data(state)
        training.evaluate_text(state, "luna")
        self.assertEqual(training.state_to_data(state), before)

    def test_corpus_training_is_reproducible(self):
        samples = ("una luna.", "la luna sale.")
        first = training.train_corpus(samples, epochs=2)
        second = training.train_corpus(samples, epochs=2)
        self.assertEqual(first.state, second.state)
        self.assertEqual(len(first.observations), 4)
        self.assertEqual(first.state.observation_count, 4)
        self.assertTrue(training.ranked_closures(first.state))

    def test_contextual_grapheme_keeps_all_readings_without_grounding(self):
        first = training.observe_text(training.TrainingState(), " casa")
        self.assertEqual(first.observation.reading_hypotheses, 2)
        self.assertEqual(first.observation.reading_winners, 2)
        self.assertFalse(first.observation.reading_resolved)
        self.assertEqual(
            first.result.winner_senses,
            (((1, "velar"),), ((1, "coronal"),)),
        )
        second = training.observe_text(first.state, " casa")
        self.assertEqual(len(second.result.winners), 2)
        self.assertEqual(len(second.state.dictionary.entries), 5)

    def test_validated_closure_selects_unlabelled_context(self):
        state = training.TrainingState()
        grounded = training.TrainingSample.from_text(" casa", {1: "velar"})
        state = training.train_corpus((grounded,), epochs=3, state=state).state

        exact = training.evaluate_text(state, " casa")
        transfer = training.evaluate_text(state, " cama")
        self.assertTrue(exact.resolved)
        self.assertTrue(transfer.resolved)
        self.assertEqual(exact.selected.senses, ((1, "velar"),))
        self.assertEqual(transfer.selected.senses, ((1, "velar"),))

    def test_pruned_reading_is_preserved_without_false_execution(self):
        grounded = training.TrainingSample.from_text(" casa", {1: "velar"})
        state = training.train_corpus((grounded,), epochs=3).state
        before = {
            (item.input, item.knowledge, item.output, item.direction):
            item.successful_uses
            for item in state.dictionary.entries
        }

        step = training.observe_text(state, " casa")
        self.assertEqual(step.result.selected.senses, ((1, "velar"),))
        after = {
            (item.input, item.knowledge, item.output, item.direction):
            item.successful_uses
            for item in step.state.dictionary.entries
        }
        self.assertTrue(all(after[key] >= uses for key, uses in before.items()))
        self.assertEqual(len(after), len(before))
        self.assertEqual(step.result.pruned_readings, 1)
        self.assertEqual(step.result.selection.closed_positions, (1,))
        self.assertTrue(all(
            item.unit in step.state.dictionary.lexicon
            for item in growth.character_options(" casa")[1]
        ))

    def test_empty_memory_keeps_the_complete_reading_space_open(self):
        result = training.evaluate_text(training.TrainingState(), " casa")
        self.assertEqual(result.total_readings, 2)
        self.assertEqual(result.evaluated_readings, 2)
        self.assertEqual(result.pruned_readings, 0)
        self.assertEqual(result.selection.closed_positions, ())
        self.assertEqual(result.selection.open_positions, (1,))

    def test_superior_closure_prunes_before_upward_execution(self):
        grounded = training.TrainingSample.from_text(" casa", {1: "velar"})
        state = training.train_corpus((grounded,), epochs=3).state
        result = training.evaluate_text(state, " cama")
        self.assertEqual(result.total_readings, 2)
        self.assertEqual(result.evaluated_readings, 1)
        self.assertEqual(result.pruned_readings, 1)
        self.assertEqual(result.selected.senses, ((1, "velar"),))
        self.assertEqual(result.selection.activation_rate, 0.5)

    def test_three_independent_ambiguities_reduce_eight_paths_to_one(self):
        state = context_experiment.run().state
        result = training.evaluate_text(state, " cama gesto soy ")
        self.assertEqual(result.total_readings, 8)
        self.assertEqual(result.evaluated_readings, 1)
        self.assertEqual(result.pruned_readings, 7)
        self.assertEqual(result.selection.closed_positions, (1, 6, 14))
        self.assertEqual(
            result.selected.senses,
            ((1, "velar"), (6, "fricative"), (14, "vowel")),
        )

    def test_one_superior_route_selects_three_connected_descendants(self):
        grounded = training.TrainingSample.from_text(
            "cgy",
            {0: "velar", 1: "voiced", 2: "consonant"},
        )
        state = training.train_corpus((grounded,), epochs=3).state
        result = training.evaluate_text(state, "cgy")
        self.assertEqual(result.total_readings, 8)
        self.assertEqual(result.evaluated_readings, 1)
        self.assertEqual(len(result.selection.components), 1)
        self.assertEqual(result.selection.components[0].positions, (0, 1, 2))
        self.assertEqual(
            result.selected.senses,
            ((0, "velar"), (1, "voiced"), (2, "consonant")),
        )

    def test_downward_and_exhaustive_paths_select_the_same_reading(self):
        state = context_experiment.run().state
        text = " cama gesto soy "
        selected = training.evaluate_text(state, text)
        exhaustive = training.evaluate_text(state, text, downward=False)
        self.assertEqual(selected.winner_senses, exhaustive.winner_senses)
        self.assertEqual(exhaustive.evaluated_readings, 8)
        self.assertEqual(exhaustive.pruned_readings, 0)

    def test_equal_superior_evidence_preserves_both_readings(self):
        samples = (
            training.TrainingSample.from_text(" casa", {1: "velar"}),
            training.TrainingSample.from_text(" casa", {1: "coronal"}),
        )
        state = training.train_corpus(samples, epochs=2).state
        result = training.evaluate_text(state, " casa")
        self.assertEqual(result.total_readings, 2)
        self.assertEqual(result.evaluated_readings, 2)
        self.assertEqual(result.pruned_readings, 0)
        self.assertFalse(result.resolved)

    def test_context_experiment_resolves_c_g_and_y_without_probe_labels(self):
        trained = context_experiment.run()
        for text, expected in context_experiment.PROBES:
            result = training.evaluate_text(trained.state, text)
            self.assertTrue(result.resolved, text)
            self.assertEqual(result.selected.senses, expected)

    def test_downward_experiment_matches_exhaustive_winners(self):
        experiment = downward_experiment.run()
        self.assertTrue(all(probe.equivalent for probe in experiment.probes))
        combined = experiment.probes[-1]
        self.assertEqual(combined.total_readings, 8)
        self.assertEqual(combined.evaluated_readings, 1)
        self.assertEqual(combined.pruned_readings, 7)


class TrainingCheckpointTests(unittest.TestCase):
    def test_checkpoint_round_trip_preserves_exact_state(self):
        state = training.train_corpus(
            ("una luna.", "la luna sale."), epochs=2
        ).state
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aurora-state.json"
            training.save_state(state, path)
            restored = training.load_state(path)
        self.assertEqual(restored, state)
        self.assertTrue(all(
            relation.reexecutes_for(relation.input)
            for relation in restored.dictionary.entries
        ))

    def test_checkpoint_schema_is_rejected_when_unknown(self):
        with self.assertRaisesRegex(aurora.AuroraError, "unsupported"):
            training.state_from_data({"schema": "future"})

    def test_contextual_selection_survives_checkpoint_round_trip(self):
        grounded = training.TrainingSample.from_text(" cena", {1: "coronal"})
        state = training.train_corpus((grounded,), epochs=3).state
        restored = training.state_from_data(training.state_to_data(state))
        result = training.evaluate_text(restored, " cero")
        self.assertTrue(result.resolved)
        self.assertEqual(result.selected.senses, ((1, "coronal"),))


if __name__ == "__main__":
    unittest.main(verbosity=2)
