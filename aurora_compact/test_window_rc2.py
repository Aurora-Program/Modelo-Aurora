import unittest

from aurora_compact import aurora, fractal_kernel, window_experiment


def leaf(value):
    return aurora.Unit.leaf(value)


class TensorWindowTests(unittest.TestCase):
    def test_new_window_is_exactly_a_b_and_a_complete_tensor_two(self):
        a, b = leaf((0, 0, 0)), leaf((0, 0, 0))
        window = fractal_kernel.FractalWindow.open(a, b)
        self.assertEqual(window.slots[:2], (a, b))
        self.assertEqual(window.result.state, aurora.EMPTY_KNOWLEDGE)
        self.assertFalse(window.result.children)

    def test_coherent_relation_emerges_above_evolved_tensor_two(self):
        a, b = leaf((0, 0, 0)), leaf((0, 0, 0))
        result = fractal_kernel.FractalWindow.open(a, b).deduce()
        self.assertIs(result.state, aurora.RelationState.CLOSED)
        self.assertIs(result.superior, result.emergent)
        self.assertIsNot(result.superior, result.evolved)
        self.assertIsNone(result.carry)
        self.assertEqual(result.evolved.children, result.window.slots)
        self.assertEqual(result.emergent.children, (a, b, result.evolved))
        self.assertTrue(aurora.reexecute(result.evolved))
        self.assertTrue(aurora.reexecute(result.emergent))

    def test_tensor_two_carries_whole_c_into_a_b_two_next_window(self):
        a, b, following = leaf((0, 0, 0)), leaf((1, 1, 1)), leaf((0, 1, 1))
        result = fractal_kernel.FractalWindow.open(a, b).deduce()
        self.assertIs(result.state, aurora.RelationState.OPEN)
        self.assertEqual(result.evolved.value, aurora.OPEN)
        self.assertIs(result.carry, result.evolved)
        self.assertIsNone(result.emergent)
        self.assertIsNone(result.superior)

        continued = result.continue_with(following)
        self.assertIs(continued.a, result.evolved)
        self.assertIs(continued.b, following)
        self.assertEqual(continued.result.state, aurora.EMPTY_KNOWLEDGE)
        self.assertIsNot(continued.result, result.window.result)
        self.assertEqual(continued.phase, result.evolved.state.do)

    def test_incoherence_ascends_a_and_carries_b_with_next_c_and_new_two(self):
        a, b, following = leaf((0, 0, 0)), leaf((0, 2, 2)), leaf((1, 1, 1))
        result = fractal_kernel.FractalWindow.open(a, b).deduce()
        self.assertIs(result.state, aurora.RelationState.CONTRADICTION)
        self.assertIs(result.superior, a)
        self.assertIs(result.carry, b)
        self.assertIsNone(result.emergent)

        continued = result.continue_with(following)
        self.assertEqual(continued.slots[:2], (b, following))
        self.assertEqual(continued.result.state, aurora.EMPTY_KNOWLEDGE)
        self.assertIsNot(continued.result, result.window.result)
        self.assertEqual(continued.phase, b.state.do)

    def test_open_c_precedes_residual_e_and_is_not_false_contradiction(self):
        a, b = leaf((0, 0, 1)), leaf((0, 2, 2))
        result = fractal_kernel.FractalWindow.open(a, b).deduce()
        self.assertEqual(result.evolved.value, aurora.OPEN)
        self.assertEqual(result.evolved.state.de, (0, 0, 0))
        self.assertIs(result.state, aurora.RelationState.OPEN)
        self.assertIs(result.carry, result.evolved)

    def test_non_orderable_evolved_result_is_incoherent_despite_de_vote(self):
        cases = (
            ((1, 0, 0), (0, 1, 2)),
            ((1, 0, 1), (1, 0, 2)),
        )
        for leaf_value, evolved_value in cases:
            with self.subTest(evolved_value=evolved_value):
                a, b = leaf(leaf_value), leaf(leaf_value)
                result = fractal_kernel.FractalWindow.open(a, b).deduce()
                self.assertEqual(result.evolved.value, evolved_value)
                self.assertEqual(aurora.majority3(*result.evolved.state.de), 1)
                self.assertFalse(aurora.order_triplet(result.evolved.value).valid)
                self.assertIs(result.state, aurora.RelationState.CONTRADICTION)
                self.assertIs(result.superior, a)
                self.assertIs(result.carry, b)
                self.assertIsNone(result.emergent)

    def test_level_continuations_consume_one_new_tensor_not_two(self):
        units = tuple(leaf(value) for value in (
            (0, 0, 0),
            (1, 1, 1),
            (0, 0, 0),
        ))
        level = fractal_kernel.resolve_level(units)
        self.assertEqual(len(level.attempts), 2)
        first, second = level.attempts
        self.assertIs(first.state, aurora.RelationState.OPEN)
        self.assertIs(second.window.a, first.evolved)
        self.assertIs(second.window.b, units[2])
        self.assertIsNot(second.window.result, first.window.result)
        self.assertEqual(second.window.phase, first.evolved.state.do)

    def test_reproducible_corrected_window_experiment(self):
        result = window_experiment.run()
        self.assertEqual(result["window"], ["A", "B", "2_0"])
        self.assertEqual(result["closed"]["superior"], "U(A,B,2e)")
        self.assertEqual(result["open"]["next_window"], ["2e", "next", "2_0"])
        self.assertEqual(
            result["contradiction"]["next_window"], ["B", "next", "2_0"]
        )
        self.assertEqual(result["contradiction"]["superior"], "A")


if __name__ == "__main__":
    unittest.main(verbosity=2)
