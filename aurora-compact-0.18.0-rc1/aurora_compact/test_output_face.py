import inspect
import unittest

from aurora_compact import (
    aurora, fractal_dictionary, fractal_dictionary_experiment, output_face,
    output_face_experiment, tensor_program,
)


P0 = fractal_dictionary_experiment.P0
P1 = fractal_dictionary_experiment.P1
P2 = fractal_dictionary_experiment.P2
P3 = fractal_dictionary_experiment.P3
P4 = fractal_dictionary_experiment.P4


def program(output, phase=(1, 1, 1)):
    return tensor_program.ProgramTensor.author(
        (P0, P1, P2), (P3, P4, output),
        aurora.Direction.INFER_R, phase,
    )


def memory_for(programs):
    memory = fractal_dictionary.FractalProgramDictionary()
    for item in programs:
        memory = memory.remember(item)
    return memory


class ParallelOutputFaceTests(unittest.TestCase):
    def setUp(self):
        self.programs = tuple(
            program(output) for output in fractal_dictionary_experiment.OUTPUTS
        )
        self.memory = memory_for(self.programs)
        self.known = (self.programs[0], self.programs[4], self.programs[8])
        self.new = program((2, 1, 0))

    def test_each_output_searches_from_its_own_index(self):
        result = output_face.resolve(self.memory, self.known)
        self.assertEqual(
            tuple(int(lane.direction) for lane in result.lanes), (0, 1, 2)
        )
        self.assertEqual(
            tuple(lane.index for lane in result.lanes), (0, 1, 2)
        )
        self.assertEqual(result.states, (1, 1, 1))
        self.assertIs(result.action, output_face.OutputAction.CONTINUE)
        self.assertTrue(result.can_advance)
        self.assertEqual(result.memory_after, self.memory)

    def test_two_found_crystallize_only_the_absent_output(self):
        result = output_face.resolve(
            self.memory, (self.known[0], self.known[1], self.new)
        )
        self.assertEqual(result.states, (1, 1, 0))
        self.assertIs(result.action, output_face.OutputAction.CRYSTALLIZE)
        self.assertEqual(result.crystallized_index, 2)
        self.assertEqual(result.crystallized, self.new)
        self.assertEqual(result.post_states, (1, 1, 1))
        self.assertTrue(result.can_advance)
        self.assertEqual(
            result.memory_after.search(
                self.new, aurora.Direction.DEDUCE_B
            ).state,
            1,
        )
        self.assertEqual([len(level) for level in result.memory_after.levels], [1, 0, 1])

    def test_the_single_absence_can_occupy_any_output_index(self):
        cases = (
            ((self.new, self.known[1], self.known[2]), (0, 1, 1), 0),
            ((self.known[0], self.new, self.known[2]), (1, 0, 1), 1),
            ((self.known[0], self.known[1], self.new), (1, 1, 0), 2),
        )
        for requirements, states, missing in cases:
            with self.subTest(missing=missing):
                result = output_face.resolve(self.memory, requirements)
                self.assertEqual(result.states, states)
                self.assertEqual(result.crystallized_index, missing)
                self.assertEqual(result.post_states, (1, 1, 1))
                self.assertEqual(
                    result.memory_after.search(
                        self.new, aurora.Direction(missing)
                    ).state,
                    1,
                )

    def test_two_absences_make_path_impossible_and_return_outputs(self):
        second = program((2, 2, 0))
        requirements = (self.known[0], self.new, second)
        result = output_face.resolve(self.memory, requirements)
        self.assertEqual(result.states, (1, 0, 0))
        self.assertIs(result.action, output_face.OutputAction.RETURN)
        self.assertFalse(result.can_advance)
        self.assertEqual(result.returned, requirements)
        self.assertEqual(result.memory_after, self.memory)
        self.assertIsNone(result.crystallized)

    def test_three_absences_return_outputs_without_writing(self):
        empty = fractal_dictionary.FractalProgramDictionary()
        requirements = (
            self.new, program((2, 2, 0)), program((2, 2, 1))
        )
        result = output_face.resolve(empty, requirements)
        self.assertEqual(result.states, (0, 0, 0))
        self.assertIs(result.action, output_face.OutputAction.RETURN)
        self.assertEqual(result.returned, requirements)
        self.assertEqual(result.memory_after, empty)

    def test_open_search_is_not_treated_as_absence(self):
        open_programs = tuple(
            program(output, aurora.OPEN)
            for output in fractal_dictionary_experiment.OUTPUTS
        )
        open_memory = memory_for(open_programs)
        result = output_face.resolve(
            open_memory, (open_programs[0], open_programs[4], open_programs[8])
        )
        self.assertEqual(result.states, (1, 1, 2))
        self.assertIs(result.action, output_face.OutputAction.OPEN)
        self.assertEqual(result.memory_after, open_memory)
        self.assertEqual(len(result.lanes[2].search.alternatives), 9)

    def test_incoherent_absence_is_never_written(self):
        atoms = list(self.new.atoms)
        atoms[8] = aurora.Unit.leaf((1, 0, 2))
        impossible = tensor_program.ProgramTensor(tuple(atoms))
        result = output_face.resolve(
            self.memory, (self.known[0], self.known[1], impossible)
        )
        self.assertEqual(result.states, (1, 1, 0))
        self.assertFalse(impossible.executable)
        self.assertIs(result.action, output_face.OutputAction.RETURN)
        self.assertEqual(result.memory_after, self.memory)

    def test_output_runtime_neither_authors_nor_scores_candidates(self):
        source = inspect.getsource(output_face).lower()
        for forbidden in (
            ".author(", "sorted(", "max(", "support", "counter",
            "weight", "threshold", "successful_uses", "last_success",
            "reorder",
        ):
            self.assertNotIn(forbidden, source)

    def test_reproducible_output_face_experiment(self):
        result = output_face_experiment.run()
        self.assertEqual(result["all_found"]["states"], [1, 1, 1])
        self.assertEqual(result["one_absent"]["states"], [1, 1, 0])
        self.assertEqual(result["one_absent"]["post_states"], [1, 1, 1])
        self.assertEqual(result["two_absent"]["states"], [1, 0, 0])
        self.assertEqual(result["two_absent"]["returned"], 3)
        self.assertEqual(result["open"]["states"], [1, 1, 2])
        self.assertTrue(result["all_reexecute"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
