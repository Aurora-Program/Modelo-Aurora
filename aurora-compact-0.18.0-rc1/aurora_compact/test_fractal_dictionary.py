import inspect
import unittest

from aurora_compact import (
    aurora, fractal_dictionary, fractal_dictionary_experiment, tensor_program,
)


P0 = (0, 0, 0)
P1 = (0, 0, 1)
P2 = (0, 0, 2)
P3 = (1, 0, 1)
P4 = (1, 1, 0)
OUTPUTS = fractal_dictionary_experiment.OUTPUTS


def program(output, phase=(1, 1, 1)):
    return tensor_program.ProgramTensor.author(
        (P0, P1, P2),
        (P3, P4, output),
        aurora.Direction.INFER_R,
        phase,
    )


def remember(programs):
    memory = fractal_dictionary.FractalProgramDictionary()
    for item in programs:
        memory = memory.remember(item)
    return memory


class ModeIndexedDictionaryTests(unittest.TestCase):
    def setUp(self):
        self.programs = tuple(program(output) for output in OUTPUTS)
        self.memory = remember(self.programs)

    def test_nine_programs_form_three_nodes_and_one_root(self):
        root = self.memory.complete_root
        self.assertIsNotNone(root)
        self.assertEqual([len(level) for level in self.memory.levels], [0, 0, 1])
        self.assertEqual(root.level, 2)
        self.assertEqual(root.leaf_count, 9)
        self.assertEqual(tuple(leaf.program for leaf in root.leaves), self.programs)
        self.assertTrue(root.all_reexecute)

    def test_learning_and_inference_are_different_fractal_indices(self):
        learning = self.memory.route(aurora.Direction.LEARN_M)
        inference = self.memory.route(aurora.Direction.INFER_R)
        self.assertEqual(learning.indices, (0, 0))
        self.assertEqual(inference.indices, (1, 1))
        self.assertEqual(learning.selected, self.programs[0])
        self.assertEqual(inference.selected, self.programs[4])

    def test_deduction_defers_its_open_index_to_dictionary_order(self):
        first = self.memory.route(
            aurora.Direction.DEDUCE_B, (0, 0, 0)
        )
        second = self.memory.route(
            aurora.Direction.DEDUCE_B, aurora.OPEN
        )
        self.assertEqual(first.indices, (0, 2))
        self.assertEqual(second.indices, (2, 2))
        self.assertEqual(first.selected, self.programs[2])
        self.assertEqual(second.selected, self.programs[8])

    def test_open_dictionary_order_preserves_every_alternative(self):
        open_memory = remember(
            tuple(program(output, aurora.OPEN) for output in OUTPUTS)
        )
        result = open_memory.route(aurora.Direction.DEDUCE_B)
        self.assertFalse(result.resolved)
        self.assertIsNone(result.selected)
        self.assertEqual(result.indices, ())
        self.assertEqual(result.alternatives, tuple(
            program(output, aurora.OPEN) for output in OUTPUTS
        ))

    def test_dictionary_order_is_the_existing_program_do_atom(self):
        root = self.memory.complete_root
        self.assertIs(root.order_unit, root.program.atoms[tensor_program.PHASE_ATOM])
        self.assertEqual(root.order_unit.value, (1, 1, 1))
        self.assertEqual(len(root.order_unit.children), 3)
        self.assertTrue(aurora.reexecute(root.order_unit))


class FractalFeedbackTests(unittest.TestCase):
    def test_observed_code_feeds_itself_from_nine_to_three_to_one(self):
        recurrent = program(OUTPUTS[0], aurora.OPEN)
        alternative = program(OUTPUTS[1], aurora.OPEN)
        observed = (
            recurrent, recurrent, alternative,
            recurrent, alternative, recurrent,
            alternative, recurrent, recurrent,
        )
        memory = fractal_dictionary.FractalProgramDictionary()
        for item in observed:
            execution = tensor_program.execute(
                (item,), {P0: P0, P1: P0, P2: P0}
            ).execution
            memory = memory.observe(execution)

        root = memory.complete_root
        self.assertIsNotNone(root)
        self.assertEqual(root.level, 2)
        self.assertEqual(root.leaf_count, 9)
        self.assertEqual(root.program.values, recurrent.values)
        self.assertTrue(root.all_reexecute)

        replay = memory.execute_root({P0: P0, P1: P0, P2: P0})
        self.assertEqual(replay.values(OUTPUTS[0]), (P0,))
        self.assertTrue(replay.all_reexecute)

    def test_fractal_dictionary_has_no_scalar_priority_or_sort(self):
        source = inspect.getsource(fractal_dictionary).lower()
        for forbidden in (
            "sorted(", "max(", "support", "counter", "weight",
            "threshold", "successful_uses", "last_success", "reorder",
        ):
            self.assertNotIn(forbidden, source)

    def test_reproducible_dictionary_experiment(self):
        result = fractal_dictionary_experiment.run()
        self.assertTrue(result["all_reexecute"])
        self.assertEqual(result["mode_routes"]["learning"]["indices"], [0, 0])
        self.assertEqual(result["mode_routes"]["inference"]["indices"], [1, 1])
        self.assertEqual(result["mode_routes"]["deduction_o0"]["indices"], [0, 2])
        self.assertEqual(result["mode_routes"]["deduction_o2"]["indices"], [2, 2])
        self.assertFalse(result["open_order"]["resolved"])
        self.assertEqual(result["open_order"]["alternatives"], 9)
        self.assertTrue(result["feedback"]["root_equals_recurrent"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
