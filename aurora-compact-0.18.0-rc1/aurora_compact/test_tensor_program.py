import inspect
import unittest

from aurora_compact import (
    aurora, provenance_experiment, relational, tensor_program,
)


P0 = (0, 0, 0)
P1 = (0, 0, 1)
P2 = (0, 0, 2)
P3 = (1, 0, 1)
P4 = (1, 1, 0)
P5 = (1, 1, 1)
P6 = (1, 1, 2)
P7 = (1, 2, 1)
P8 = (0, 1, 0)


def route_a():
    return tensor_program.ProgramTensor.author(
        (P0, P1, P2), (P3, P4, P5), aurora.Direction.INFER_R
    )


def route_b():
    return tensor_program.ProgramTensor.author(
        (P0, P1, P2), (P3, P4, P6), aurora.Direction.INFER_R
    )


def experience(program, value=P0):
    return tensor_program.execute(
        (program,), {P0: value, P1: value, P2: value}
    ).execution


class TensorInstructionCompletenessTests(unittest.TestCase):
    def test_closed_222_instruction_executes_deduction(self):
        seed = relational.OperationalSeed.from_tensor(
            "deduce",
            ("a", "b", "r"),
            ("o.do", "o.de", "o.ds"),
            relational.instruction_tensor(aurora.Direction.DEDUCE_B),
        )
        self.assertEqual(seed.tensor.state.de, (1, 1, 1))
        self.assertEqual(seed.tensor.value, aurora.OPEN)
        self.assertEqual(seed.direction, aurora.Direction.DEDUCE_B)


class TensorProgramTests(unittest.TestCase):
    def test_nine_triplets_are_the_complete_presentation(self):
        program = route_a()
        self.assertEqual(program.inputs, (P0, P1, P2))
        self.assertEqual(program.outputs, (P3, P4, P5))
        self.assertEqual(program.phase, aurora.OPEN)
        self.assertEqual(program.de, (1, 1, 1))
        self.assertEqual(program.signature, (1, 1, 1))
        self.assertTrue(program.executable)

    def test_changing_only_code_changes_output_routing(self):
        initial = {P0: P0, P1: P0, P2: P0}
        first = tensor_program.execute((route_a(),), initial)
        second = tensor_program.execute((route_b(),), initial)
        self.assertEqual(first.values(P5), (P0,))
        self.assertEqual(second.values(P6), (P0,))
        self.assertEqual(first.execution.firings[0].result,
                         second.execution.firings[0].result)
        self.assertTrue(first.all_reexecute)
        self.assertTrue(second.all_reexecute)

    def test_two_recurrent_programs_synthesize_executable_code(self):
        a = route_a()
        b = route_b()
        learned = tensor_program.induce((a, a, b))
        self.assertEqual(learned.candidates, (a, a, b))
        self.assertEqual(learned.emergent.values, a.values)
        self.assertTrue(learned.emergent.executable)
        self.assertTrue(learned.all_reexecute)

        result = tensor_program.execute(
            (learned.emergent,), {P0: P0, P1: P0, P2: P0}
        )
        self.assertEqual(result.values(P5), (P0,))
        self.assertTrue(result.all_reexecute)

    def test_incompatible_programs_remain_open_without_forced_winner(self):
        def candidate(target):
            return tensor_program.ProgramTensor.author(
                (P0, P1, P2), (P3, P4, target), aurora.Direction.INFER_R
            )

        candidates = (candidate(P8), candidate(P3), candidate(P6))
        learned = tensor_program.induce(candidates)
        self.assertEqual(learned.candidates, candidates)
        self.assertEqual(learned.emergent.outputs[2], (1, 0, 2))
        self.assertFalse(learned.emergent.executable)
        self.assertTrue(learned.all_reexecute)
        with self.assertRaisesRegex(aurora.AuroraError, "open address"):
            tensor_program.execute((learned.emergent,), {})

    def test_emergent_program_round_trips_with_full_provenance(self):
        learned = tensor_program.induce((route_a(), route_a(), route_b()))
        restored = tensor_program.ProgramTensor.from_json(
            learned.emergent.to_json()
        )
        self.assertEqual(restored, learned.emergent)
        self.assertTrue(restored.all_reexecute)
        self.assertTrue(all(len(atom.children) == 3 for atom in restored.atoms))

    def test_induction_has_no_external_recurrence_score(self):
        source = inspect.getsource(tensor_program.induce).lower()
        for forbidden in ("support", "counter", "weight", "threshold", "max("):
            self.assertNotIn(forbidden, source)


class ProvenanceProgramTests(unittest.TestCase):
    def test_reproducible_provenance_experiment(self):
        result = provenance_experiment.run()
        self.assertTrue(result["all_reexecute"])
        self.assertTrue(
            result["same_causal_window"]["emergent_equals_recurrent"]
        )
        self.assertEqual(result["distinct_causal_window"]["inductions"], 0)
        self.assertFalse(
            result["incompatible_window"]["emergent_executable"]
        )

    def test_firing_preserves_and_reflects_the_executed_tensor_program(self):
        original = route_a()
        observed = experience(original)
        self.assertEqual(len(observed.firings), 1)
        firing = observed.firings[0]
        self.assertEqual(firing.seed.provenance, original.atoms)
        self.assertEqual(tensor_program.ProgramTensor.from_firing(firing), original)

    def test_causal_fingerprint_contains_the_executed_program(self):
        first = experience(route_a()).firings[0].emissions[0]
        second = experience(route_b()).firings[0].emissions[0]
        self.assertEqual(first.seed.name, second.seed.name)
        self.assertEqual(first.value, second.value)
        self.assertEqual(first.parents, second.parents)
        self.assertNotEqual(first.fingerprint, second.fingerprint)

    def test_reflection_keeps_learned_code_provenance(self):
        a = route_a()
        learned = tensor_program.induce((a, a, route_b())).emergent
        self.assertTrue(all(len(atom.children) == 3 for atom in learned.atoms))
        reflected = tensor_program.ProgramTensor.from_firing(
            experience(learned).firings[0]
        )
        self.assertEqual(reflected, learned)
        self.assertTrue(all(len(atom.children) == 3 for atom in reflected.atoms))

    def test_three_causal_experiences_present_their_own_programs(self):
        a = route_a()
        b = route_b()
        observed = (experience(a), experience(a), experience(b))
        learned = tensor_program.induce_from_provenance(observed)
        self.assertEqual(len(learned), 1)
        self.assertEqual(learned[0].induction.candidates, (a, a, b))
        self.assertEqual(learned[0].emergent.values, a.values)
        self.assertTrue(learned[0].all_reexecute)

        execution = experience(learned[0].emergent)
        self.assertEqual(execution.values("cell:111"), (P0,))
        self.assertTrue(execution.all_reexecute)

    def test_distinct_causal_windows_are_not_mixed(self):
        observed = (
            experience(route_a(), P0),
            experience(route_a(), P0),
            experience(route_b(), P5),
        )
        self.assertEqual(tensor_program.induce_from_provenance(observed), ())

    def test_incompatible_experiences_preserve_open_code(self):
        def candidate(target):
            return tensor_program.ProgramTensor.author(
                (P0, P1, P2), (P3, P4, target), aurora.Direction.INFER_R
            )

        candidates = (candidate(P8), candidate(P3), candidate(P6))
        learned = tensor_program.induce_from_provenance(
            tuple(experience(program) for program in candidates)
        )
        self.assertEqual(len(learned), 1)
        self.assertEqual(learned[0].induction.candidates, candidates)
        self.assertEqual(learned[0].emergent.outputs[2], (1, 0, 2))
        self.assertFalse(learned[0].emergent.executable)
        self.assertTrue(learned[0].all_reexecute)

    def test_program_education_round_trip_preserves_code_provenance(self):
        program = tensor_program.induce(
            (route_a(), route_a(), route_b())
        ).emergent
        education = relational.Education((program.compile("learned"),))
        restored = relational.Education.from_json(education.to_json())
        self.assertEqual(restored, education)
        self.assertEqual(
            tensor_program.ProgramTensor.from_seed(restored.seeds[0]), program
        )

    def test_provenance_induction_has_no_authored_candidate_or_score(self):
        source = inspect.getsource(
            tensor_program.induce_from_provenance
        ).lower()
        for forbidden in (
            "author(", "support", "counter", "weight", "threshold", "max("
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
