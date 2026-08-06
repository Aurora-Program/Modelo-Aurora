import unittest

from aurora_compact import aurora, characters


class FractalCharacterTensorTests(unittest.TestCase):
    def test_character_materializes_one_three_nine(self):
        tensor = characters.vowel_tensor("a")
        self.assertEqual(len(tensor.triplets), 13)
        self.assertEqual(len(tensor.trits), 39)
        self.assertEqual(len(tensor.unit.children), 3)
        self.assertTrue(all(len(branch.children) == 3
                            for branch in tensor.unit.children))
        self.assertTrue(tensor.reexecutes)

    def test_lower_schema_is_inherited_from_family(self):
        vowel = characters.vowel_tensor("a")
        consonant = characters.consonant_tensor(
            "b",
            place=characters.predicates(1, 0, 0),
            manner=aurora.OPEN,
            phonation=characters.one_of(1),
        )
        symbol = characters.symbol_tensor(
            ".",
            boundary=characters.one_of(2),
            pairing=characters.one_of(0),
            pause=characters.one_of(2),
            contour=characters.one_of(2),
        )

        self.assertEqual(
            tuple(prop.name for prop in vowel.branch(
                characters.SemanticRole.STRUCTURE).properties),
            ("family", "height", "position"),
        )
        self.assertEqual(
            tuple(prop.name for prop in consonant.branch(
                characters.SemanticRole.STRUCTURE).properties),
            ("family", "place", "manner"),
        )
        self.assertEqual(
            tuple(prop.name for prop in symbol.branch(
                characters.SemanticRole.FUNCTION).properties),
            ("pause", "contour", "force"),
        )

    def test_role_binding_is_not_a_physical_position(self):
        tensor = characters.vowel_tensor("i")
        rotated = tensor.reordered((
            characters.SemanticRole.FORM,
            characters.SemanticRole.STRUCTURE,
            characters.SemanticRole.FUNCTION,
        ))
        self.assertEqual(
            rotated.physical_roles,
            (characters.SemanticRole.FORM,
             characters.SemanticRole.STRUCTURE,
             characters.SemanticRole.FUNCTION),
        )
        self.assertEqual(
            rotated.get_property(characters.SemanticRole.STRUCTURE, "height").value,
            tensor.get_property(characters.SemanticRole.STRUCTURE, "height").value,
        )
        self.assertTrue(rotated.reexecutes)

    def test_two_characters_can_share_a_tensor_pattern(self):
        lexicon = characters.spanish_character_lexicon()
        b = lexicon.lookup("b")[0]
        v = lexicon.lookup("v")[0]
        self.assertEqual(b.leaf_values, v.leaf_values)
        self.assertNotEqual(b.text, v.text)

    def test_root_summary_does_not_replace_fractal_identity(self):
        a = characters.vowel_tensor("a")
        e = characters.vowel_tensor("e")
        self.assertEqual(a.unit.value, e.unit.value)
        self.assertNotEqual(a.triplets, e.triplets)


class CharacterDeductionTests(unittest.TestCase):
    def test_search_reuses_trigate_deduction(self):
        lexicon = characters.spanish_character_lexicon()
        query = characters.CharacterQuery(
            characters.CharacterFamily.VOWEL,
            ((characters.SemanticRole.STRUCTURE,
              "height", characters.one_of(0)),),
        )
        found = {item.text for item in lexicon.search(query)}
        self.assertTrue({"i", "u", "í", "ú", "ü"}.issubset(found))
        self.assertNotIn("a", found)

    def test_open_property_pattern_accepts_every_value(self):
        lexicon = characters.spanish_character_lexicon()
        query = characters.CharacterQuery(
            constraints=((characters.SemanticRole.STRUCTURE,
                          "family", aurora.OPEN),),
        )
        self.assertEqual(len(lexicon.search(query)), len(lexicon.entries))

    def test_contextual_graphemes_keep_competing_senses(self):
        lexicon = characters.spanish_character_lexicon()
        self.assertEqual({item.sense for item in lexicon.lookup("c")},
                         {"velar", "coronal"})
        self.assertEqual({item.family for item in lexicon.lookup("y")},
                         {characters.CharacterFamily.VOWEL,
                          characters.CharacterFamily.CONSONANT})

    def test_every_seed_is_a_reexecutable_39_trit_tensor(self):
        lexicon = characters.spanish_character_lexicon()
        self.assertGreater(len(lexicon.entries), 60)
        for item in lexicon.entries:
            with self.subTest(text=item.text, sense=item.sense):
                self.assertEqual(len(item.trits), 39)
                self.assertTrue(item.reexecutes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
