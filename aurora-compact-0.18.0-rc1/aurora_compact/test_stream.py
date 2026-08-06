import itertools
import unittest
from dataclasses import replace

from aurora_compact import aurora, experiment, stream


def full_route():
    return (aurora.OPEN,) + tuple(
        value for value in itertools.product(range(3), repeat=3)
        if value != aurora.OPEN
    )


class SequentialLearningTests(unittest.TestCase):
    phrase = ((0, 0, 0), (0, 0, 1), (0, 0, 2)) * 3

    def test_exact_tensor_is_lexicalized_after_first_observation(self):
        first = stream.process_sequence(self.phrase, do_route=full_route())
        second = stream.process_sequence(
            self.phrase, first.fractal.dictionary, full_route(), tick=2,
        )
        self.assertFalse(first.lexicalized)
        self.assertEqual(len(first.fractal.trace), 4)
        self.assertTrue(second.lexicalized)
        self.assertEqual(second.fractal.trace, ())
        self.assertEqual(second.logical_cost, 1)
        self.assertEqual(stream.surface(second.fractal.root), self.phrase)

    def test_exact_fractal_context_precedes_popular_ds_collision(self):
        token = (0, 0, 0)
        lower = aurora.synthesize(tuple(aurora.Unit.leaf(token) for _ in range(3)))
        learned_lower = aurora.transcend(lower, aurora.AuroraDictionary())
        upper = aurora.synthesize((lower, lower, lower))
        learned_upper = aurora.transcend(
            upper, learned_lower.dictionary, do_route=full_route(),
        )
        lower_relation, upper_relation = learned_upper.dictionary.entries
        memory = aurora.AuroraDictionary(
            (replace(lower_relation, successful_uses=99), upper_relation),
            learned_upper.dictionary.lexicon,
        )
        found = memory.search(upper.value, current=upper)
        self.assertEqual(found[0].input, upper)
        result = aurora.transcend(upper, memory, do_route=full_route())
        self.assertEqual(result.trace[0].action,
                         aurora.AttemptAction.REUSE_OUTPUT)

    def test_stream_preserves_memory_and_detects_novelty(self):
        shifted = ((1, 1, 1), (1, 1, 2), (1, 2, 2)) * 3
        result = stream.learn_stream(
            (self.phrase, self.phrase, shifted, shifted),
            do_route=full_route(),
        )
        observations = result.observations
        self.assertEqual([x.lexicalized for x in observations],
                         [False, True, False, True])
        self.assertGreater(observations[0].new_relations, 0)
        self.assertEqual(observations[1].new_relations, 0)
        self.assertGreater(observations[2].new_relations, 0)
        self.assertEqual(observations[3].new_relations, 0)

    def test_600_sequence_experiment_relearns_only_at_shift(self):
        report = experiment.run()
        blocks = {block["range"]: block for block in report["blocks"]}
        self.assertEqual(report["sequences"], 600)
        self.assertEqual(report["vocabulary"], 24)
        self.assertEqual(blocks["100-150"]["new_relations"], 0)
        self.assertGreater(blocks["300-350"]["new_relations"], 0)
        self.assertEqual(blocks["550-600"]["new_relations"], 0)
        self.assertEqual(report["literal_boundary_probe"]["blocked"], 60)
        self.assertEqual(sum(report["genesis_control_after_one_pass"].values()),
                         25)


if __name__ == "__main__":
    unittest.main(verbosity=2)
