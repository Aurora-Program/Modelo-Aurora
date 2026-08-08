import inspect
import unittest

from aurora_compact import aurora, fractal_kernel, release_candidate_experiment


CHILDREN = ((0, 0, 0), (1, 0, 1), aurora.OPEN)
CURRENT = fractal_kernel.FractalAddress((0, 0, 0), (0, 1, 0))
UPPER = fractal_kernel.FractalAddress((0, 0, 1), (0, 1, 0))
TOPOLOGY = fractal_kernel.FractalTopology(
    ((CURRENT,), (UPPER,), (CURRENT, UPPER))
)


def emergent_unit():
    return aurora.synthesize(
        tuple(aurora.Unit.leaf(value) for value in CHILDREN),
        aurora.Direction.LEARN_M,
    )


class ThreeIndexDictionaryTests(unittest.TestCase):
    def test_one_k_is_reconstructed_from_each_of_its_three_indices(self):
        unit = emergent_unit()
        memory = fractal_kernel.FractalTensorDictionary().remember(unit)
        self.assertEqual(len(memory.nodes), 1)

        lookups = tuple(
            memory.search(unit.state.channels[index], aurora.Direction(index))
            for index in range(3)
        )
        self.assertEqual(tuple(lookup.state for lookup in lookups), (1, 1, 1))
        self.assertTrue(all(lookup.selected is unit for lookup in lookups))
        self.assertTrue(all(lookup.selected.state == unit.state for lookup in lookups))
        self.assertEqual(
            tuple(lookup.outgoing[0] for lookup in lookups), unit.state.do
        )

    def test_shared_index_remains_open_and_preserves_full_units(self):
        shared_do = (0, 1, 2)
        first = aurora.Unit(aurora.Knowledge(shared_do, (1, 1, 1), (0, 0, 0)))
        second = aurora.Unit(aurora.Knowledge(shared_do, (0, 0, 0), (1, 1, 1)))
        memory = (
            fractal_kernel.FractalTensorDictionary()
            .remember(first)
            .remember(second)
        )
        result = memory.search(shared_do, aurora.Direction.LEARN_M)
        self.assertEqual(result.state, 2)
        self.assertEqual(result.alternatives, (first, second))

    def test_missing_index_is_determined_absence(self):
        unit = emergent_unit()
        memory = fractal_kernel.FractalTensorDictionary().remember(unit)
        result = memory.search((1, 1, 1), aurora.Direction.DEDUCE_B)
        self.assertEqual(result.state, 0)
        self.assertIsNone(result.selected)

    def test_nine_complete_units_promote_to_one_three_index_root(self):
        unit = emergent_unit()
        memory = fractal_kernel.FractalTensorDictionary()
        for _ in range(9):
            memory = memory.remember(unit)
        root = memory.root
        self.assertIsNotNone(root)
        self.assertEqual([len(level) for level in memory.levels], [0, 0, 1])
        self.assertEqual(root.leaf_count, 9)
        self.assertTrue(root.all_reexecute)
        for index in range(3):
            result = memory.search(
                root.unit.state.channels[index], aurora.Direction(index)
            )
            self.assertEqual(result.state, 1)
            self.assertIs(result.selected, root.unit)


class FractalPassageTests(unittest.TestCase):
    def test_orientation_alone_selects_same_upper_or_open_destination(self):
        unit = emergent_unit()
        self.assertEqual(unit.state.do, (2, 1, 0))
        window = fractal_kernel.OrientedBoundary(TOPOLOGY)

        open_passage = window.pass_unit(unit, aurora.Direction.LEARN_M)
        upper_passage = window.pass_unit(unit, aurora.Direction.INFER_R)
        current_passage = window.pass_unit(unit, aurora.Direction.DEDUCE_B)

        self.assertEqual(open_passage.destinations, (CURRENT, UPPER))
        self.assertEqual(upper_passage.destinations, (UPPER,))
        self.assertEqual(current_passage.destinations, (CURRENT,))
        self.assertTrue(all(
            passage.unit is unit
            for passage in (open_passage, upper_passage, current_passage)
        ))
        self.assertEqual(
            tuple(int(passage.next_c) for passage in (
                open_passage, upper_passage, current_passage
            )),
            unit.state.do,
        )

    def test_de_does_not_change_the_selected_connection(self):
        first = aurora.Unit(aurora.Knowledge((0, 1, 2), (1, 1, 1), (0, 0, 0)))
        second = aurora.Unit(aurora.Knowledge((0, 1, 2), (0, 0, 0), (1, 1, 1)))
        window = fractal_kernel.OrientedBoundary(TOPOLOGY)
        for incoming in aurora.Direction:
            left = window.pass_unit(first, incoming)
            right = window.pass_unit(second, incoming)
            self.assertEqual(left.outgoing, right.outgoing)
            self.assertEqual(left.destinations, right.destinations)

    def test_window_is_the_boundary_and_preserves_the_emergent_unit(self):
        children = tuple(aurora.Unit.leaf(value) for value in CHILDREN)
        window = fractal_kernel.OrientedBoundary(TOPOLOGY)
        passage = window.resolve(children, aurora.Direction.LEARN_M)
        expected = aurora.synthesize(children, aurora.Direction.LEARN_M)
        self.assertEqual(passage.unit, expected)
        self.assertTrue(aurora.reexecute(passage.unit))
        self.assertTrue(all(unit is passage.unit for _, unit in passage.deliveries))

    def test_triplet_uses_its_own_ordering_and_open_preserves_ports(self):
        resolved = fractal_kernel.pass_triplet((1, 1, 2), TOPOLOGY)
        ordering = aurora.order_triplet((1, 1, 2))
        self.assertEqual(resolved.orientations, (ordering.o,))
        self.assertEqual(resolved.destinations, TOPOLOGY.ports[ordering.o])

        opened = fractal_kernel.pass_triplet(aurora.OPEN, TOPOLOGY)
        self.assertFalse(opened.resolved)
        self.assertEqual(set(opened.destinations), {CURRENT, UPPER})

    def test_release_candidate_kernel_contains_no_semantic_action_dispatch(self):
        source = inspect.getsource(fractal_kernel).lower()
        for forbidden in (
            "classify_de(", "growthaction", "outputaction", "unit.state.de",
            "ascend =", "carry =", "sorted(",
        ):
            self.assertNotIn(forbidden, source)

    def test_reproducible_release_candidate_experiment(self):
        result = release_candidate_experiment.run()
        self.assertTrue(result["emergent_unit"]["reexecutes"])
        self.assertEqual(result["three_index_dictionary"]["states"], [1, 1, 1])
        self.assertTrue(result["three_index_dictionary"]["same_identity"])
        self.assertTrue(result["window_boundary"]["same_identity"])
        self.assertTrue(result["window_boundary"]["open_preserves_both"])
        self.assertTrue(result["window_boundary"]["upper_selected"])
        self.assertTrue(result["window_boundary"]["current_selected"])
        self.assertEqual(result["promotion"]["levels"], [0, 0, 1])
        self.assertEqual(result["promotion"]["root_leaves"], 9)
        self.assertTrue(result["promotion"]["same_root"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
