import unittest

from aurora_compact import aurora, growth


def leaves(*values):
    return tuple(aurora.Unit.leaf(value) for value in values)


class HorizontalAndVerticalGrowthTests(unittest.TestCase):
    def test_closed_window_ascends_and_is_lexicalized(self):
        result = growth.grow_level(leaves((0, 0, 0), (0, 0, 0), (0, 0, 0)))
        self.assertTrue(result.complete)
        self.assertEqual(len(result.emerged), 1)
        self.assertEqual(result.attempts[0].action, growth.GrowthAction.ASCEND)
        self.assertEqual(result.emerged[0].source_positions, (0, 1, 2))
        self.assertTrue(aurora.reexecute(result.emerged[0].unit))
        self.assertTrue(result.dictionary.knows(result.emerged[0].unit))
        self.assertEqual(len(result.dictionary.entries), 1)
        self.assertTrue(result.dictionary.entries[0].reexecutes_for(
            result.emerged[0].unit
        ))
        self.assertEqual(result.attempts[0].support, 1)

    def test_open_window_becomes_carry_and_joins_next_two(self):
        result = growth.grow_level(leaves(
            (0, 0, 0), (1, 1, 1), aurora.OPEN,
            (0, 0, 0), (0, 0, 0),
        ))
        self.assertEqual(
            [attempt.action for attempt in result.attempts],
            [growth.GrowthAction.CARRY, growth.GrowthAction.ASCEND],
        )
        carry = result.attempts[0].candidate
        self.assertTrue(carry.open)
        self.assertEqual(carry.source_positions, (0, 1, 2))
        self.assertIs(result.attempts[1].inputs[0], carry)
        self.assertEqual(result.emerged[0].source_positions, (0, 1, 2, 3, 4))
        self.assertTrue(result.complete)

    def test_contradiction_slides_without_losing_sources(self):
        result = growth.grow_level(leaves(
            (0, 0, 1), (0, 2, 2), (0, 2, 2),
        ))
        self.assertEqual(result.attempts[0].state,
                         aurora.RelationState.CONTRADICTION)
        self.assertEqual(result.attempts[0].action, growth.GrowthAction.SHIFT)
        self.assertEqual(
            tuple(position for node in result.residual
                  for position in node.source_positions),
            (0, 1, 2),
        )
        self.assertEqual(result.emerged, ())

    def test_nine_closed_units_grow_through_two_levels(self):
        result = growth.grow_fractal(leaves(*(((0, 0, 0),) * 9)))
        self.assertTrue(result.complete)
        self.assertEqual([len(level.emerged) for level in result.levels], [3, 1])
        self.assertEqual(result.root.source_positions, tuple(range(9)))
        self.assertTrue(aurora.reexecute(result.root.unit))

    def test_known_closed_unit_is_reused(self):
        units = leaves((0, 0, 0), (0, 0, 0), (0, 0, 0))
        first = growth.grow_level(units)
        second = growth.grow_level(units, first.dictionary)
        self.assertFalse(first.attempts[0].lexicalized)
        self.assertTrue(second.attempts[0].lexicalized)
        self.assertEqual(first.attempts[0].support, 1)
        self.assertEqual(second.attempts[0].support, 2)
        self.assertEqual(second.dictionary.entries[0].successful_uses, 1)
        self.assertGreater(second.dictionary.entries[0].last_success, 0)


class CharacterGrowthTests(unittest.TestCase):
    def test_strict_character_reader_requires_explicit_sense(self):
        with self.assertRaisesRegex(aurora.AuroraError, "remains ambiguous"):
            growth.character_readings("c")
        reading = growth.character_readings("c", senses={0: "velar"})
        self.assertEqual(reading[0].sense, "velar")

    def test_nine_character_tensors_enter_the_same_growth_cycle(self):
        result = growth.grow_text("aaaaaaaaa")
        self.assertTrue(result.growth.complete)
        self.assertEqual([len(level.emerged) for level in result.growth.levels],
                         [3, 1])
        self.assertEqual(result.growth.root.source_positions, tuple(range(9)))

    def test_recurrence_promotes_closures_without_duplication(self):
        first = growth.grow_text("aaaaaaaaa")
        second = growth.grow_text(
            "aaaaaaaaa", dictionary=first.growth.dictionary, tick=100,
        )
        self.assertEqual(
            [attempt.support for attempt in first.growth.levels[0].attempts],
            [1, 2, 3],
        )
        self.assertEqual(
            [attempt.support for attempt in second.growth.levels[0].attempts],
            [4, 5, 6],
        )
        self.assertEqual(len(first.growth.dictionary.entries), 2)
        self.assertEqual(len(second.growth.dictionary.entries), 2)
        self.assertEqual(
            [relation.successful_uses
             for relation in second.growth.dictionary.entries],
            [5, 1],
        )

    def test_dictionary_ranks_recurrent_closure_above_ds_collisions(self):
        a = growth.grow_text("aaaaaaaaa")
        e1 = growth.grow_text(
            "eeeeeeeee", dictionary=a.growth.dictionary, tick=100,
        )
        e2 = growth.grow_text(
            "eeeeeeeee", dictionary=e1.growth.dictionary, tick=200,
        )
        recurrent = e2.growth.levels[0].emerged[0].unit
        candidates = e2.growth.dictionary.search(recurrent.value)
        self.assertEqual(candidates[0].input, recurrent)
        self.assertGreater(
            candidates[0].successful_uses,
            candidates[1].successful_uses,
        )

    def test_open_character_relation_remains_as_carry(self):
        result = growth.grow_text("hhh")
        self.assertFalse(result.growth.complete)
        attempt = result.growth.levels[0].attempts[0]
        self.assertEqual(attempt.action, growth.GrowthAction.CARRY)
        self.assertEqual(result.growth.frontier[0].source_positions, (0, 1, 2))


class OverlappingCompetitionTests(unittest.TestCase):
    A = aurora.Unit.leaf((0, 0, 0))
    B = aurora.Unit.leaf((0, 0, 1))

    def test_every_overlapping_closure_is_observed_and_kept(self):
        result = growth.compete_level((self.A, self.A, self.B) * 3)
        self.assertEqual(len(result.candidates), 7)
        self.assertEqual(len(result.dictionary.entries), 3)
        self.assertEqual(result.hypothesis_count, 19)
        self.assertEqual(
            [candidate.support for candidate in result.candidates],
            [3, 2, 2, 3, 2, 2, 3],
        )
        self.assertTrue(all(
            relation.reexecutes_for(relation.input)
            for relation in result.dictionary.entries
        ))

    def test_recurrence_selects_a_complete_segmentation(self):
        result = growth.compete_level((self.A, self.A, self.B) * 3)
        self.assertTrue(result.resolved)
        self.assertTrue(result.selected.complete)
        self.assertEqual(
            [(candidate.start, candidate.stop)
             for candidate in result.selected.segments],
            [(0, 3), (3, 6), (6, 9)],
        )
        self.assertEqual(
            [candidate.support for candidate in result.selected.segments],
            [3, 3, 3],
        )

    def test_equal_histories_remain_contextually_ambiguous(self):
        result = growth.compete_level((self.A, self.A, self.B, self.B))
        self.assertFalse(result.resolved)
        self.assertEqual(len(result.winners), 2)
        self.assertEqual(
            {tuple((candidate.start, candidate.stop)
                   for candidate in winner.segments)
             for winner in result.winners},
            {((0, 3),), ((1, 4),)},
        )
        self.assertTrue(all(len(winner.residual) == 1
                            for winner in result.winners))

    def test_prior_context_changes_selection_without_deleting_the_loser(self):
        memory = growth.compete_level((self.A, self.A, self.B)).dictionary
        memory = growth.compete_level(
            (self.A, self.A, self.B), memory, tick=10
        ).dictionary
        result = growth.compete_level(
            (self.A, self.A, self.B, self.B), memory, tick=20
        )
        self.assertTrue(result.resolved)
        self.assertEqual(
            [(candidate.start, candidate.stop, candidate.support)
             for candidate in result.selected.segments],
            [(0, 3, 3)],
        )
        self.assertEqual(len(result.dictionary.entries), 2)
        self.assertEqual(
            sorted(relation.successful_uses + 1
                   for relation in result.dictionary.entries),
            [1, 3],
        )

    def test_open_branch_extends_before_it_competes(self):
        result = growth.compete_level(leaves(
            (0, 0, 0), (1, 1, 1), aurora.OPEN,
            (0, 0, 0), (0, 0, 0),
        ))
        long = result.selected.segments[0]
        self.assertEqual((long.start, long.stop), (0, 5))
        self.assertEqual(
            [attempt.action for attempt in long.attempts],
            [growth.GrowthAction.CARRY, growth.GrowthAction.ASCEND],
        )
        self.assertEqual(long.node.source_positions, (0, 1, 2, 3, 4))

    def test_unique_competition_repeats_at_the_next_fractal_level(self):
        result = growth.compete_fractal((self.A, self.A, self.B) * 3)
        self.assertTrue(result.complete)
        self.assertEqual(len(result.levels), 2)
        self.assertEqual(result.root.source_positions, tuple(range(9)))
        self.assertTrue(aurora.reexecute(result.root.unit))


if __name__ == "__main__":
    unittest.main(verbosity=2)
