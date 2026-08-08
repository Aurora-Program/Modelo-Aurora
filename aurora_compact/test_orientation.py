import itertools
import unittest

from aurora_compact import (
    aurora, control, orientation, orientation_experiment, relational,
    tensor_program,
)


class TripletOrientationTests(unittest.TestCase):
    def test_o_selects_es_for_every_resolved_triplet_and_phase(self):
        resolved = 0
        for values in itertools.product(range(3), repeat=3):
            for phase in range(3):
                result = orientation.orient_triplet(values, phase)
                if not result.resolved:
                    continue
                resolved += 1
                self.assertEqual(result.es, values[result.o])
                indices = (
                    result.ordering.o,
                    result.ordering.fn_index,
                    result.ordering.fo_index,
                )
                self.assertEqual(set(indices), {0, 1, 2})
        self.assertGreater(resolved, 0)

    def test_superior_o_inherits_es_from_the_selected_lower_relation(self):
        children = ((0, 0, 2), (1, 1, 2), (0, 0, 0))
        for upper_o in range(3):
            result = orientation.inherit_es(children, upper_o)
            self.assertEqual(result.selected, children[upper_o])
            if result.lower.resolved:
                self.assertEqual(result.es, result.selected[result.lower.o])


class FractalOrientationTests(unittest.TestCase):
    def test_same_complete_unit_accepts_three_orientations_without_rebuild(self):
        unit = aurora.Unit(aurora.Knowledge(
            (0, 1, 2), (1, 1, 1), (0, 0, 0)
        ))
        presentations = tuple(orientation.present(unit, c) for c in range(3))
        self.assertTrue(all(step.unit is unit for step in presentations))
        self.assertEqual(tuple(step.outgoing for step in presentations), (0, 1, 2))

    def test_emitted_o_feeds_the_next_c_without_translation(self):
        units = (
            aurora.Unit(aurora.Knowledge((1, 2, 0), (1, 1, 1), (0, 0, 0))),
            aurora.Unit(aurora.Knowledge((2, 0, 1), (1, 1, 1), (0, 0, 1))),
            aurora.Unit(aurora.Knowledge((0, 1, 2), (1, 1, 1), (0, 0, 2))),
        )
        trace = orientation.chain(units, 0)
        self.assertEqual(tuple(step.incoming for step in trace), (0, 1, 0))
        self.assertEqual(tuple(step.outgoing for step in trace), (1, 0, 0))

    def test_so_and_tensor_program_expose_the_same_complete_instruction_k(self):
        program = tensor_program.ProgramTensor.author(
            ((0, 0, 0), (0, 0, 1), (0, 0, 2)),
            ((1, 0, 1), (1, 1, 0), (1, 1, 1)),
            aurora.Direction.INFER_R,
            (0, 1, 2),
        )
        seed = program.compile("orientation")
        direct = relational.instruction_tensor(
            aurora.Direction.INFER_R, (0, 1, 2)
        )
        self.assertEqual(seed.tensor, direct)
        self.assertEqual(seed.phase, seed.tensor.state.do)
        self.assertEqual(int(seed.direction), aurora.majority3(*seed.tensor.value))

    def test_window_carry_is_the_full_reexecutable_k_unit(self):
        result = aurora.resolve_window((aurora.OPEN,) * 3)
        self.assertIsNotNone(result.carry)
        self.assertEqual(result.carry.unit.state, result.knowledge)
        self.assertEqual(len(result.carry.unit.children), 3)
        self.assertTrue(result.carry.reexecutes)

    def test_control_is_projected_back_into_one_complete_k(self):
        unit = aurora.Unit.leaf((1, 0, 0))
        result = control.control_faces(unit, unit, aurora.Unit.leaf(aurora.OPEN))
        packets = result.hds.packet, result.hde.packet, result.hdo.packet
        self.assertEqual(result.knowledge.do, tuple(packet.o for packet in packets))
        self.assertEqual(result.knowledge.de, tuple(packet.e for packet in packets))
        self.assertEqual(result.knowledge.ds, tuple(packet.r for packet in packets))
        self.assertEqual(result.unit.state.ds, (
            int(result.operation), int(result.coherence), int(result.scope)
        ))
        self.assertTrue(result.reexecutes)

    def test_reproducible_orientation_experiment(self):
        result = orientation_experiment.run()
        self.assertTrue(result["triplet"]["es_is_value_at_o"])
        self.assertTrue(result["operational_seed"]["same_instruction"])
        self.assertTrue(result["window"]["reexecutes"])
        self.assertTrue(result["control"]["ds_is_control_triplet"])
        self.assertTrue(result["control"]["reexecutes"])
        self.assertTrue(
            result["same_unit_three_orientations"]["identity_preserved"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
