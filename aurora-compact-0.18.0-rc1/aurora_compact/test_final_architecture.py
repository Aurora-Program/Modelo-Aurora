import itertools
import unittest

from aurora_compact import aurora, control, deduction, routing, tokens


class FinalDirectionTests(unittest.TestCase):
    def test_direction_values_are_the_emergent_hds_values(self):
        self.assertEqual(aurora.Direction.LEARN_M.value, 0)
        self.assertEqual(aurora.Direction.INFER_R.value, 1)
        self.assertEqual(aurora.Direction.DEDUCE_B.value, 2)

    def test_dictionary_query_is_trigate_deduction(self):
        query = deduction.DeductiveQuery((1, 1, 1), aurora.OPEN, (1, 1, 1))
        self.assertEqual(query.domains, (frozenset((1,)),) * 3)
        self.assertTrue(query.accepts((1, 1, 1)))
        self.assertFalse(query.accepts((1, 1, 0)))

    def test_unknown_result_with_open_mode_keeps_b_open(self):
        query = deduction.DeductiveQuery((2, 2, 2), aurora.OPEN, aurora.OPEN)
        self.assertEqual(query.domains, (frozenset((0, 1, 2)),) * 3)
        for candidate in itertools.product(range(3), repeat=3):
            self.assertTrue(query.accepts(candidate))

    def test_literal_two_can_also_be_deduced_uniquely(self):
        query = deduction.DeductiveQuery.for_exact_tensor((0, 1, 2))
        self.assertEqual(query.domains, (
            frozenset((0,)), frozenset((1,)), frozenset((2,)),
        ))
        self.assertTrue(query.accepts((0, 1, 2)))


class EmergentControlTests(unittest.TestCase):
    def test_hds_hde_hdo_tables(self):
        self.assertEqual(
            control.interpret((0, 0, 0), (0, 0, 0), (0, 0, 0)),
            (aurora.Direction.LEARN_M,
             control.Coherence.INCOHERENT,
             control.SearchScope.LOCAL),
        )
        self.assertEqual(
            control.interpret((1, 1, 2), (1, 1, 2), (1, 1, 2)),
            (aurora.Direction.INFER_R,
             control.Coherence.COHERENT,
             control.SearchScope.NETWORK),
        )
        self.assertEqual(
            control.interpret(aurora.OPEN, aurora.OPEN, aurora.OPEN),
            (aurora.Direction.DEDUCE_B,
             control.Coherence.AMBIGUOUS,
             control.SearchScope.STOP),
        )


class TokenTensorTests(unittest.TestCase):
    def test_simple_token_has_open_do_de_and_its_ds(self):
        token = tokens.SimpleToken("uno", (0, 0, 1))
        self.assertEqual(token.knowledge,
                         aurora.Knowledge(aurora.OPEN, aurora.OPEN, (0, 0, 1)))

    def test_base_three_numeric_tokens_match_their_indices(self):
        names = ("cero", "uno", "dos", "tres", "cuatro")
        lexicon = tokens.numeric_lexicon(names)
        for index, name in enumerate(names):
            value = lexicon.lookup(name)[0].ds
            self.assertEqual(tokens.index_from_tensor(value), index)

    def test_one_token_can_have_more_than_one_tensor(self):
        lexicon = (tokens.TokenLexicon()
                   .bind("banco", (0, 0, 1), "asiento")
                   .bind("banco", (1, 1, 0), "finanzas"))
        self.assertEqual(len(lexicon.lookup("banco")), 2)


class DistributedDictionaryTests(unittest.TestCase):
    @staticmethod
    def learned_dictionary(value):
        unit = aurora.Unit.leaf(value)
        return aurora.transcend(unit, aurora.AuroraDictionary()).dictionary

    def test_hdo_selects_local_network_and_stop(self):
        query = deduction.DeductiveQuery.for_exact_tensor((1, 1, 1))
        local = routing.Node("local", ((0, 0, 0),), self.learned_dictionary((0, 0, 0)))
        expert = routing.Node("expert", ((1, 1, 1),), self.learned_dictionary((1, 1, 1)))
        network = routing.Network((local, expert))

        here = network.resolve("local", query, control.SearchScope.LOCAL)
        self.assertEqual(here.matches, ())

        remote = network.resolve("local", query, control.SearchScope.NETWORK, tick=4)
        self.assertEqual(remote.node_id, "expert")
        self.assertTrue(remote.learned_route)
        self.assertEqual(remote.network.routes[0].tensor, (1, 1, 1))

        reused = remote.network.resolve(
            "local", query, control.SearchScope.NETWORK, tick=5,
        )
        self.assertFalse(reused.learned_route)
        self.assertEqual(reused.network.routes[0].successful_uses, 2)

        stopped = reused.network.resolve("local", query, control.SearchScope.STOP)
        self.assertTrue(stopped.stopped)
        self.assertEqual(stopped.matches, ())


if __name__ == "__main__":
    unittest.main(verbosity=2)
