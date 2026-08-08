import inspect
import unittest

from aurora_compact import aurora, education_experiment, relational


class OperationalSeedTests(unittest.TestCase):
    def test_instruction_direction_is_read_from_an_aurora_tensor(self):
        inputs = ("a", "b", "m")
        outputs = ("o.do", "o.de", "o.ds")
        learn = relational.OperationalSeed.from_tensor(
            "learn", inputs, outputs,
            relational.instruction_tensor(aurora.Direction.LEARN_M),
        )
        infer = relational.OperationalSeed.from_tensor(
            "infer", inputs, outputs,
            relational.instruction_tensor(aurora.Direction.INFER_R),
        )
        self.assertEqual(learn.tensor.value, (0, 0, 0))
        self.assertEqual(infer.tensor.value, (1, 1, 1))
        self.assertEqual(learn.direction, aurora.Direction.LEARN_M)
        self.assertEqual(infer.direction, aurora.Direction.INFER_R)

    def test_open_direction_instruction_is_rejected_as_undetermined(self):
        tensor = aurora.Unit(aurora.Knowledge(
            aurora.OPEN, aurora.OPEN, aurora.OPEN
        ))
        with self.assertRaisesRegex(aurora.AuroraError, "determine"):
            relational.OperationalSeed.from_tensor(
                "open", ("a", "b", "c"), ("d", "e", "f"), tensor
            )

    def test_education_round_trips_as_data(self):
        original = education_experiment.vertical_education()
        restored = relational.Education.from_json(original.to_json())
        self.assertEqual(restored, original)


class UniversalExecutionTests(unittest.TestCase):
    def test_tensor_instruction_changes_operation_without_runtime_change(self):
        initial = {"a": (0, 0, 0), "b": (0, 0, 0), "m": (0, 0, 0)}

        def execute(direction):
            seed = relational.OperationalSeed.from_tensor(
                "only",
                ("a", "b", "m"),
                ("out.do", "out.de", "out.ds"),
                relational.instruction_tensor(direction),
            )
            return relational.execute(relational.Education((seed,)), initial)

        learned = execute(aurora.Direction.LEARN_M)
        inferred = execute(aurora.Direction.INFER_R)
        self.assertEqual(learned.values("out.de"), (aurora.OPEN,))
        self.assertEqual(inferred.values("out.de"), ((1, 1, 1),))
        self.assertTrue(learned.all_reexecute)
        self.assertTrue(inferred.all_reexecute)

    def test_outputs_activate_the_next_educated_relation(self):
        result = relational.execute(
            education_experiment.vertical_education(),
            {f"x{index}": (0, 0, 0) for index in range(9)},
        )
        self.assertTrue(result.fixed_point)
        self.assertFalse(result.exhausted)
        self.assertEqual(len(result.firings), 4)
        self.assertEqual(result.values("root.de"), ((1, 1, 1),))
        self.assertEqual(result.values("root.ds"), ((0, 0, 0),))
        self.assertEqual(result.signals("root.ds")[0].depth, 2)
        self.assertTrue(result.all_reexecute)

    def test_open_output_is_represented_with_next_two_by_education(self):
        result = relational.execute(
            education_experiment.open_then_close_education(),
            {
                "x0": (0, 0, 0),
                "x1": (1, 1, 1),
                "x2": aurora.OPEN,
                "x3": (0, 0, 0),
                "x4": (0, 0, 0),
            },
        )
        self.assertEqual(result.values("first.de"), (aurora.OPEN,))
        self.assertEqual(result.values("second.de"), ((1, 1, 1),))
        self.assertEqual(result.values("second.ds"), ((0, 0, 0),))
        self.assertEqual(len(result.firings), 2)
        self.assertTrue(result.all_reexecute)

    def test_exact_alternatives_are_preserved_and_all_propagate(self):
        seed = relational.OperationalSeed.from_tensor(
            "branch",
            ("a", "b", "c"),
            ("out.do", "out.de", "out.ds"),
            relational.instruction_tensor(aurora.Direction.INFER_R),
        )
        alternatives = (
            relational.Signal.leaf((0, 0, 0), "a:zero"),
            relational.Signal.leaf((1, 1, 1), "a:one"),
        )
        result = relational.execute(
            relational.Education((seed,)),
            {"a": alternatives, "b": (0, 0, 0), "c": (0, 0, 0)},
        )
        self.assertEqual(len(result.firings), 2)
        self.assertEqual(len(result.signals("out.ds")), 2)
        self.assertTrue(result.all_reexecute)

    def test_runtime_has_no_semantic_growth_action_table(self):
        source = inspect.getsource(relational.execute).lower()
        for forbidden in ("ascend", "carry", "shift", "syllab", "segment"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
