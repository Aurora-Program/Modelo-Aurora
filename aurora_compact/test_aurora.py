import itertools
import pathlib
import unittest
from collections import Counter
from dataclasses import replace

from aurora_compact import aurora


class TriGateTests(unittest.TestCase):
    def test_honest_majority_and_completeness(self):
        self.assertEqual(aurora.majority3(1, 1, 2), 1)
        self.assertEqual(aurora.majority3(1, 2, 2), 2)
        self.assertEqual(aurora.majority3(0, 1, 2), 2)

    def test_majority_is_permutation_invariant(self):
        for values in itertools.product(range(3), repeat=3):
            outputs = {aurora.majority3(*p) for p in itertools.permutations(values)}
            self.assertEqual(len(outputs), 1)

    def test_inverse_domains_preserve_ambiguity(self):
        domain = aurora.candidate_domain(0, 0, 2, 0, aurora.Direction.LEARN_M)
        self.assertEqual(domain, frozenset((0, 1, 2)))
        packet = aurora.trigate(0, 0, 2, 0, aurora.Direction.LEARN_M)
        self.assertEqual(packet.state, aurora.RelationState.AMBIGUOUS)
        self.assertEqual(packet.resolved_target, 2)

    def test_directions_target_the_current_spec_cells(self):
        self.assertEqual(
            aurora.candidate_domain(1, 2, 1, 1, aurora.Direction.DEDUCE_B),
            frozenset((0, 1, 2)),
        )
        self.assertEqual(
            aurora.candidate_domain(1, 0, 2, 0, aurora.Direction.INFER_R),
            frozenset((2,)),
        )
        self.assertEqual(
            aurora.candidate_domain(1, 1, 2, 0, aurora.Direction.LEARN_M),
            frozenset(),
        )

    def test_r2_carries_unique_residual(self):
        for values, residual in [((2, 2, 0), 0), ((2, 1, 2), 1),
                                 ((2, 2, 2), 2), ((0, 1, 2), 2)]:
            self.assertEqual(aurora.trigate(*values).e, residual)

    def test_determined_value_cannot_match_a_unique_open_result(self):
        packet = aurora.trigate(0, 1, 2, r=0,
                                direction=aurora.Direction.INFER_R)
        self.assertEqual(packet.candidates, frozenset((2,)))
        self.assertEqual(packet.state, aurora.RelationState.CONTRADICTION)

    def test_symmetry_meaning(self):
        self.assertEqual(aurora.symmetry((0, 1, 2)), 0)  # completeness
        self.assertEqual(aurora.symmetry((1, 1, 2)), 1)  # duality
        self.assertEqual(aurora.symmetry((2, 2, 2)), 2)  # unity

    def test_exhaustive_trigate_state_fingerprint(self):
        expected = {
            aurora.Direction.DEDUCE_B:
                {"ambiguous": 17, "closed": 16, "contradiction": 46, "open": 2},
            aurora.Direction.INFER_R:
                {"closed": 28, "contradiction": 40, "open": 13},
            aurora.Direction.LEARN_M:
                {"ambiguous": 17, "closed": 16, "contradiction": 46, "open": 2},
        }
        for direction in aurora.Direction:
            states = Counter(
                aurora.trigate(a, b, m, r, direction).state.value
                for a, b, m, r in itertools.product(range(3), repeat=4)
            )
            self.assertEqual(dict(states), expected[direction])


class OrderingTests(unittest.TestCase):
    def test_roles_and_self_reference_exclusion(self):
        order = aurora.order_triplet((1, 1, 2), phase=2)
        self.assertTrue(order.valid)
        self.assertEqual((order.o, order.fn_index, order.fo_index), (0, 1, 2))
        self.assertEqual((order.es, order.fn, order.fo), (1, 1, 2))

    def test_012_is_a_signature_not_literal_closure(self):
        order = aurora.order_triplet((0, 1, 2))
        self.assertFalse(order.valid)
        with self.assertRaises(aurora.AuroraError):
            aurora.face(((0, 1, 2), (1, 1, 2), (0, 0, 2)))

    def test_open_and_heterogeneous_r2_have_distinct_o_domains(self):
        self.assertEqual(aurora.operation_orientations((2, 2, 2)), (2, 0, 1))
        self.assertEqual(aurora.operation_orientations((0, 1, 2)), (1, 2))


class FaceAndFractalTests(unittest.TestCase):
    inputs = ((1, 1, 2), (0, 0, 2), (1, 1, 0))

    def test_triangular_wiring_and_projection(self):
        result = aurora.face(self.inputs)
        fo = tuple(o.fo for o in result.ordered)
        fn = tuple(o.fn for o in result.ordered)
        expected = (
            aurora.majority3(fo[1], fo[2], fn[0]),
            aurora.majority3(fo[2], fo[0], fn[1]),
            aurora.majority3(fo[0], fo[1], fn[2]),
        )
        actual = tuple(p.r for p in (result.triangle[1], result.triangle[2],
                                     result.triangle[0]))
        self.assertEqual(actual, expected)
        self.assertEqual(result.knowledge.ds, tuple(p.r for p in result.groups))
        self.assertEqual(result.knowledge.de, tuple(p.e for p in result.groups))
        self.assertEqual(result.knowledge.do, tuple(p.o for p in result.groups))

    def test_1_3_9_uses_the_same_face_and_keeps_provenance(self):
        leaves = tuple(aurora.Unit.leaf(self.inputs[i % 3]) for i in range(9))
        level3 = aurora.ascend(leaves)
        root = aurora.ascend(level3)[0]
        self.assertEqual(len(level3), 3)
        self.assertEqual(len(root.children), 3)
        self.assertTrue(aurora.reexecute(root))

    def test_control_topology_is_c4_c5_c6_only(self):
        i, k, s = (aurora.Unit.leaf(v) for v in self.inputs)
        control = aurora.control_faces(i, k, s)
        self.assertIsInstance(control.c4, aurora.FaceResult)
        self.assertIsInstance(control.c5, aurora.FaceResult)
        self.assertIsInstance(control.c6, aurora.FaceResult)
        self.assertFalse(hasattr(control, "c7"))


class WindowAndMemoryTests(unittest.TestCase):
    inputs = ((1, 1, 2), (0, 0, 2), (1, 1, 0))

    def test_window_stops_only_at_fixed_point_or_explicit_limit(self):
        result = aurora.resolve_window(self.inputs, max_steps=27)
        if result.fixed_point:
            self.assertEqual(result.trace[-1].knowledge.do,
                             result.trace[-1].do_before)
        else:
            self.assertEqual(result.state, aurora.RelationState.UNRESOLVED)

    def test_open_fixed_point_emits_carry_not_invented_closure(self):
        result = aurora.resolve_window((aurora.OPEN,) * 3)
        self.assertTrue(result.fixed_point)
        self.assertEqual(result.state, aurora.RelationState.OPEN)
        self.assertIsNotNone(result.carry)
        self.assertEqual(result.carry.unit.state, result.knowledge)
        self.assertEqual(result.carry.unit.state.channels,
                         (aurora.OPEN, aurora.OPEN, aurora.OPEN))
        self.assertEqual(len(result.carry.unit.children), 3)
        self.assertTrue(result.carry.reexecutes)

    def test_dictionary_creation_and_search_are_separate(self):
        unit = aurora.Unit.leaf((1, 1, 2))
        relation = aurora.Relation(
            unit, aurora.derive_knowledge(unit, unit), unit,
            successful_uses=1, last_success=10,
        )
        builder = aurora.DictionaryBuilder()
        builder.add(relation)
        frozen = builder.freeze()
        builder.add(replace(relation, successful_uses=2, last_success=20))
        self.assertEqual(len(frozen.search(unit.value, aurora.Direction.INFER_R)), 1)

    def test_sliding_windows_preserve_order(self):
        items = tuple(aurora.Unit.leaf((x, x, 2)) for x in (0, 1, 0, 1))
        found = tuple(aurora.windows(items))
        self.assertEqual(len(found), 2)
        self.assertEqual(found[0], items[:3])
        self.assertEqual(found[1], items[1:])


class BehavioralCycleTests(unittest.TestCase):
    context = (0, 0, 0)

    @staticmethod
    def _unit(*values):
        return aurora.synthesize(tuple(aurora.Unit.leaf(v) for v in values))

    def test_control_emerges_without_an_external_purpose(self):
        i = aurora.Unit.leaf((1, 0, 0))
        control = aurora.control_faces(i, i, aurora.Unit.leaf(aurora.OPEN))
        self.assertEqual(len(control.hds.signature), 3)
        self.assertEqual(len(control.hde.signature), 3)
        self.assertEqual(len(control.hdo.signature), 3)
        self.assertEqual(control.operation.value, control.hds.packet.r)
        self.assertEqual(control.coherence.value, control.hde.packet.r)
        self.assertEqual(control.scope.value, control.hdo.packet.r)
        self.assertFalse(hasattr(control, "blocked_purpose"))

    def test_empty_dictionary_reflects_input_and_learns_knowledge(self):
        input_unit = aurora.Unit.leaf(self.context)
        result = aurora.transcend(input_unit, aurora.AuroraDictionary())
        self.assertEqual(result.state, aurora.RelationState.CLOSED)
        self.assertEqual(result.output, input_unit)
        self.assertNotEqual(result.knowledge.state, aurora.EMPTY_KNOWLEDGE)
        self.assertEqual(result.trace[0].action,
                         aurora.AttemptAction.LEARN_KNOWLEDGE)
        self.assertTrue(result.trace[0].reexecuted)
        self.assertTrue(result.dictionary.knows(input_unit))

    def test_existing_knowledge_changes_output_to_lexicalized_unit(self):
        input_unit = aurora.Unit.leaf(self.context)
        known_output = aurora.Unit.leaf((1, 1, 1))
        dictionary = aurora.AuroraDictionary().register(known_output)
        learned = aurora.transcend(
            input_unit, dictionary, initial_output=known_output,
        )
        reused = aurora.transcend(
            input_unit, learned.dictionary, initial_output=input_unit, tick=7,
        )
        self.assertEqual(reused.output, known_output)
        self.assertEqual(reused.trace[0].action,
                         aurora.AttemptAction.REUSE_OUTPUT)
        self.assertEqual(reused.dictionary.entries[0].successful_uses, 1)
        self.assertEqual(reused.dictionary.entries[0].last_success, 7)

    def test_output_must_be_in_input_or_dictionary(self):
        with self.assertRaises(aurora.AuroraError):
            aurora.transcend(
                aurora.Unit.leaf(self.context), aurora.AuroraDictionary(),
                initial_output=aurora.Unit.leaf((1, 1, 1)),
            )

    def test_failed_knowledge_kept_while_new_branch_competes(self):
        input_unit = aurora.Unit.leaf(self.context)
        bad = aurora.Relation(input_unit, aurora.Unit(aurora.EMPTY_KNOWLEDGE),
                              input_unit, successful_uses=10)
        dictionary = aurora.AuroraDictionary().add(bad)
        result = aurora.transcend(
            input_unit, dictionary, do_route=(aurora.OPEN, (1, 1, 1)),
        )
        self.assertEqual(tuple(a.action for a in result.trace), (
            aurora.AttemptAction.REJECT,
            aurora.AttemptAction.LEARN_KNOWLEDGE,
        ))
        self.assertEqual(len(result.dictionary.entries), 2)
        self.assertEqual(result.output, input_unit)

    def test_same_ds_different_fractal_context_creates_alternative(self):
        lower = self._unit(self.context, self.context, self.context)
        learned = aurora.transcend(lower, aurora.AuroraDictionary())
        upper = aurora.synthesize((lower, lower, lower))
        self.assertEqual(lower.value, upper.value)
        result = aurora.transcend(
            upper, learned.dictionary, do_route=(aurora.OPEN, (1, 1, 1)),
        )
        self.assertEqual(tuple(a.action for a in result.trace), (
            aurora.AttemptAction.REJECT,
            aurora.AttemptAction.LEARN_KNOWLEDGE,
        ))
        self.assertEqual(len(result.dictionary.entries), 2)

    def test_dialogue_repeats_through_complete_1_3_9_tensor(self):
        result = aurora.process_fractal(
            (self.context,) * 9,
            do_route=(aurora.OPEN, (1, 1, 1)),
        )
        self.assertEqual(tuple(len(level) for level in result.levels), (9, 3, 1))
        self.assertEqual(len(result.trace), 4)
        self.assertTrue(aurora.reexecute(result.root))
        self.assertEqual(len(result.dictionary.entries), 2)

    def test_do_budget_never_repeats_a_state(self):
        with self.assertRaises(aurora.AuroraError):
            aurora.transcend(
                aurora.Unit.leaf(self.context), aurora.AuroraDictionary(()),
                do_route=(aurora.OPEN, aurora.OPEN),
            )


class CompactnessTests(unittest.TestCase):
    def test_reference_kernel_stays_compact_after_control_extraction(self):
        path = pathlib.Path(aurora.__file__)
        self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 620)


if __name__ == "__main__":
    unittest.main(verbosity=2)
