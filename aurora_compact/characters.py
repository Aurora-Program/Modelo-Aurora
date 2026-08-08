"""Operational 1-3-9 fractal tensors for character tokens.

The root identifies one character tensor.  Its three children are the
structure, function and form branches for the current lexical context.  Every
branch owns three lower properties, so the complete materialized tensor has
1 + 3 + 9 triplets (39 trits).

The meaning of the lower properties is inherited from the character family.
Vowels expose vowel phonetics, consonants expose consonant phonetics and
symbols expose boundary, pause and intonation properties.  Role names are
attached to branches rather than hard-coded to physical tuple positions.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
import unicodedata
from typing import Iterable, Sequence

from aurora_compact import aurora, deduction


class SemanticRole(Enum):
    STRUCTURE = "structure"
    FUNCTION = "function"
    FORM = "form"


class CharacterFamily(Enum):
    VOWEL = "vowel"
    CONSONANT = "consonant"
    SYMBOL = "symbol"


ROLE_ORDER = (
    SemanticRole.STRUCTURE,
    SemanticRole.FUNCTION,
    SemanticRole.FORM,
)


def predicates(*values: bool | None | int) -> aurora.Triplet:
    """Build three yes/no/open predicates without using 2 as a category.

    ``False`` is 0, ``True`` is 1 and ``None`` is the open trit 2.  Integers
    are accepted when they are already valid trits.
    """
    if len(values) != 3:
        raise aurora.AuroraError("a property requires exactly three predicates")
    encoded = tuple(2 if value is None else int(value) for value in values)
    return aurora.triplet(encoded)


def one_of(index: int) -> aurora.Triplet:
    """Encode one selected predicate among three using only 0 and 1."""
    if index not in range(3):
        raise aurora.AuroraError("a ternary property choice must be 0, 1 or 2")
    return aurora.triplet(1 if position == index else 0 for position in range(3))


@dataclass(frozen=True)
class CharacterProperty:
    """One lower property and the meanings of its three trit positions."""

    name: str
    labels: tuple[str, str, str]
    value: aurora.Triplet

    def __post_init__(self) -> None:
        if not self.name:
            raise aurora.AuroraError("a character property needs a name")
        if len(self.labels) != 3 or any(not label for label in self.labels):
            raise aurora.AuroraError("a property needs three non-empty labels")
        if len(set(self.labels)) != 3:
            raise aurora.AuroraError("property labels must be distinct")
        object.__setattr__(self, "value", aurora.triplet(self.value))

    @property
    def unit(self) -> aurora.Unit:
        return aurora.Unit.leaf(self.value)


@dataclass(frozen=True)
class PropertyBranch:
    """A role-bound system made from exactly three inherited properties."""

    role: SemanticRole
    properties: tuple[CharacterProperty, CharacterProperty, CharacterProperty]

    def __post_init__(self) -> None:
        object.__setattr__(self, "role", SemanticRole(self.role))
        if len(self.properties) != 3:
            raise aurora.AuroraError("a fractal branch requires three properties")
        if len({prop.name for prop in self.properties}) != 3:
            raise aurora.AuroraError("property names must be unique in a branch")

    @property
    def unit(self) -> aurora.Unit:
        return aurora.synthesize(tuple(prop.unit for prop in self.properties))

    def property(self, name: str) -> CharacterProperty:
        for item in self.properties:
            if item.name == name:
                return item
        raise KeyError(name)


@dataclass(frozen=True)
class CharacterTensor:
    """A re-executable character tensor with one root, three branches and nine leaves."""

    text: str
    family: CharacterFamily
    branches: tuple[PropertyBranch, PropertyBranch, PropertyBranch]
    sense: str = "default"

    def __post_init__(self) -> None:
        if len(self.text) != 1:
            raise aurora.AuroraError("a character tensor must contain one character")
        if not self.sense:
            raise aurora.AuroraError("a character tensor needs a sense")
        object.__setattr__(self, "family", CharacterFamily(self.family))
        if len(self.branches) != 3:
            raise aurora.AuroraError("a character tensor requires three branches")
        if {branch.role for branch in self.branches} != set(ROLE_ORDER):
            raise aurora.AuroraError(
                "the three branches must bind structure, function and form"
            )

    def branch(self, role: SemanticRole) -> PropertyBranch:
        wanted = SemanticRole(role)
        for item in self.branches:
            if item.role is wanted:
                return item
        raise KeyError(wanted)

    def get_property(self, role: SemanticRole, name: str) -> CharacterProperty:
        return self.branch(role).property(name)

    @property
    def physical_roles(self) -> tuple[SemanticRole, SemanticRole, SemanticRole]:
        return tuple(branch.role for branch in self.branches)  # type: ignore[return-value]

    def reordered(self, roles: Sequence[SemanticRole]) -> CharacterTensor:
        """Return the same semantic tensor in another physical role order."""
        order = tuple(SemanticRole(role) for role in roles)
        if len(order) != 3 or set(order) != set(ROLE_ORDER):
            raise aurora.AuroraError("a role order must be a permutation of ES/FN/FO")
        return replace(self, branches=tuple(self.branch(role) for role in order))

    @property
    def unit(self) -> aurora.Unit:
        return aurora.synthesize(tuple(branch.unit for branch in self.branches))

    @property
    def triplets(self) -> tuple[aurora.Triplet, ...]:
        """Materialize the canonical 1-3-9 tree as thirteen triplets."""
        root = self.unit
        branch_units = root.children
        leaves = tuple(
            leaf.value for branch in branch_units for leaf in branch.children
        )
        return (root.value,) + tuple(branch.value for branch in branch_units) + leaves

    @property
    def trits(self) -> tuple[aurora.Trit, ...]:
        return tuple(value for triplet in self.triplets for value in triplet)

    @property
    def leaf_values(self) -> tuple[aurora.Triplet, ...]:
        return tuple(
            prop.value for branch in self.branches for prop in branch.properties
        )

    @property
    def reexecutes(self) -> bool:
        return aurora.reexecute(self.unit)


@dataclass(frozen=True)
class CharacterQuery:
    """A semantic path selection whose values are matched by TriGate deduction."""

    family: CharacterFamily | None = None
    constraints: tuple[tuple[SemanticRole, str, aurora.Triplet], ...] = ()

    def __post_init__(self) -> None:
        if self.family is not None:
            object.__setattr__(self, "family", CharacterFamily(self.family))
        normalized = tuple(
            (SemanticRole(role), name, aurora.triplet(value))
            for role, name, value in self.constraints
        )
        object.__setattr__(self, "constraints", normalized)

    def accepts(self, candidate: CharacterTensor) -> bool:
        if self.family is not None and candidate.family is not self.family:
            return False
        for role, name, pattern in self.constraints:
            try:
                value = candidate.get_property(role, name).value
            except KeyError:
                return False
            if not deduction.DeductiveQuery.for_tensor(pattern).accepts(value):
                return False
        return True


@dataclass(frozen=True)
class CharacterLexicon:
    entries: tuple[CharacterTensor, ...] = ()

    def bind(self, tensor: CharacterTensor) -> CharacterLexicon:
        if any(
            item.text == tensor.text and item.sense == tensor.sense
            for item in self.entries
        ):
            raise aurora.AuroraError("that character sense is already bound")
        return CharacterLexicon(self.entries + (tensor,))

    def extend(self, tensors: Iterable[CharacterTensor]) -> CharacterLexicon:
        result = self
        for tensor in tensors:
            result = result.bind(tensor)
        return result

    def lookup(self, text: str) -> tuple[CharacterTensor, ...]:
        return tuple(item for item in self.entries if item.text == text)

    def search(self, query: CharacterQuery) -> tuple[CharacterTensor, ...]:
        return tuple(item for item in self.entries if query.accepts(item))


def _property(
    name: str,
    labels: tuple[str, str, str],
    value: Sequence[aurora.Trit],
) -> CharacterProperty:
    return CharacterProperty(name, labels, aurora.triplet(value))


def _branch(
    role: SemanticRole,
    definitions: Sequence[
        tuple[str, tuple[str, str, str], Sequence[aurora.Trit]]
    ],
) -> PropertyBranch:
    if len(definitions) != 3:
        raise aurora.AuroraError("a branch schema requires three definitions")
    properties = tuple(_property(*definition) for definition in definitions)
    return PropertyBranch(role, properties)  # type: ignore[arg-type]


def _base_letter(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


_FAMILY_LABELS = ("vowel", "consonant", "symbol")
_CASE_LABELS = ("lower", "upper", "uncased")
_MARK_LABELS = ("plain", "acute", "diaeresis")
_COMPOSITION_LABELS = ("single", "combined", "contextual")


def vowel_tensor(text: str, sense: str = "default") -> CharacterTensor:
    """Create a Spanish-vowel seed whose descendants are vowel properties."""
    base = _base_letter(text)
    height = {"i": 0, "u": 0, "e": 1, "o": 1, "a": 2}.get(base)
    position = {"i": 0, "e": 0, "a": 1, "o": 2, "u": 2}.get(base)
    if height is None or position is None:
        raise aurora.AuroraError(f"{text!r} is not a supported vowel seed")
    rounded = 1 if base in "ou" else 0
    lowered = text.lower()
    mark = 1 if lowered in "áéíóú" else 2 if lowered == "ü" else 0
    case = 1 if text.isupper() else 0
    syllabicity = 2 if base in "iu" else 1
    stress = 2 if mark == 1 else 1

    branches = (
        _branch(SemanticRole.STRUCTURE, (
            ("family", _FAMILY_LABELS, one_of(0)),
            ("height", ("high", "mid", "low"), one_of(height)),
            ("position", ("front", "central", "back"), one_of(position)),
        )),
        _branch(SemanticRole.FUNCTION, (
            ("rounding", ("unrounded", "rounded", "variable"), one_of(rounded)),
            ("syllabicity", ("non_syllabic", "syllabic", "contextual"), one_of(syllabicity)),
            ("stress", ("unstressed", "stress_capable", "marked"), one_of(stress)),
        )),
        _branch(SemanticRole.FORM, (
            ("case", _CASE_LABELS, one_of(case)),
            ("mark", _MARK_LABELS, one_of(mark)),
            ("composition", _COMPOSITION_LABELS, one_of(0)),
        )),
    )
    return CharacterTensor(text, CharacterFamily.VOWEL, branches, sense)


def consonant_tensor(
    text: str,
    *,
    place: Sequence[aurora.Trit],
    manner: Sequence[aurora.Trit],
    phonation: Sequence[aurora.Trit],
    stability: Sequence[aurora.Trit] = one_of(0),
    realization: Sequence[aurora.Trit] = one_of(0),
    mark: Sequence[aurora.Trit] | None = None,
    composition: Sequence[aurora.Trit] = one_of(0),
    sense: str = "default",
) -> CharacterTensor:
    """Create a consonant seed from coarse, explicitly ternary phonetics."""
    case = one_of(1 if text.isupper() else 0)
    if mark is None:
        mark = one_of(1 if text.lower() == "ñ" else 0)
    branches = (
        _branch(SemanticRole.STRUCTURE, (
            ("family", _FAMILY_LABELS, one_of(1)),
            ("place", ("labial", "coronal", "dorsal"), place),
            ("manner", ("occlusive", "continuous", "nasal"), manner),
        )),
        _branch(SemanticRole.FUNCTION, (
            ("phonation", ("voiceless", "voiced", "variable"), phonation),
            ("stability", ("stable", "contextual", "composite"), stability),
            ("realization", ("pronounced", "silent", "variable"), realization),
        )),
        _branch(SemanticRole.FORM, (
            ("case", _CASE_LABELS, case),
            ("mark", ("plain", "diacritic", "foreign"), mark),
            ("composition", ("single", "multigraph", "contextual"), composition),
        )),
    )
    return CharacterTensor(text, CharacterFamily.CONSONANT, branches, sense)


def symbol_tensor(
    text: str,
    *,
    boundary: Sequence[aurora.Trit],
    pairing: Sequence[aurora.Trit],
    pause: Sequence[aurora.Trit],
    contour: Sequence[aurora.Trit],
    force: Sequence[aurora.Trit] = (0, 0, 0),
    spacing: Sequence[aurora.Trit] = one_of(0),
    repetition: Sequence[aurora.Trit] = one_of(0),
    visibility: Sequence[aurora.Trit] = one_of(0),
    sense: str = "default",
) -> CharacterTensor:
    """Create a symbol seed whose inherited function includes pause."""
    branches = (
        _branch(SemanticRole.STRUCTURE, (
            ("family", _FAMILY_LABELS, one_of(2)),
            ("boundary", ("word", "clause", "sentence"), boundary),
            ("pairing", ("unpaired", "opening", "closing"), pairing),
        )),
        _branch(SemanticRole.FUNCTION, (
            ("pause", ("short", "medium", "long"), pause),
            ("contour", ("neutral", "rising", "falling"), contour),
            ("force", ("declarative", "interrogative", "exclamative"), force),
        )),
        _branch(SemanticRole.FORM, (
            ("spacing", ("attached", "blank", "linebreak"), spacing),
            ("repetition", ("single", "repeatable", "paired"), repetition),
            ("visibility", ("visible", "blank", "control"), visibility),
        )),
    )
    return CharacterTensor(text, CharacterFamily.SYMBOL, branches, sense)


def spanish_character_lexicon() -> CharacterLexicon:
    """Return a small auditable Spanish seed alphabet and punctuation set.

    Context-dependent graphemes keep competing senses instead of collapsing
    them into one average tensor.  The inventory is intentionally phonetic and
    coarse: later learning may add alternatives under the same character.
    """
    lexicon = CharacterLexicon()

    for text in "aeiouáéíóúüAEIOUÁÉÍÓÚÜ":
        lexicon = lexicon.bind(vowel_tensor(text))

    # place=(labial, coronal, dorsal), manner=(occlusive, continuous, nasal)
    # phonation=(voiceless, voiced, variable)
    seeds = (
        ("b", "default", predicates(1, 0, 0), aurora.OPEN, one_of(1), one_of(1), one_of(0), one_of(0)),
        ("c", "velar", predicates(0, 0, 1), one_of(0), one_of(0), one_of(1), one_of(0), one_of(0)),
        ("c", "coronal", predicates(0, 1, 0), one_of(1), one_of(0), one_of(1), one_of(0), one_of(0)),
        ("d", "default", predicates(0, 1, 0), aurora.OPEN, one_of(1), one_of(1), one_of(0), one_of(0)),
        ("f", "default", predicates(1, 0, 0), one_of(1), one_of(0), one_of(0), one_of(0), one_of(0)),
        ("g", "voiced", predicates(0, 0, 1), aurora.OPEN, one_of(1), one_of(1), one_of(0), one_of(0)),
        ("g", "fricative", predicates(0, 0, 1), one_of(1), one_of(0), one_of(1), one_of(0), one_of(0)),
        ("h", "silent", aurora.OPEN, aurora.OPEN, aurora.OPEN, one_of(0), one_of(1), one_of(0)),
        ("j", "default", predicates(0, 0, 1), one_of(1), one_of(0), one_of(0), one_of(0), one_of(0)),
        ("k", "default", predicates(0, 0, 1), one_of(0), one_of(0), one_of(0), one_of(0), one_of(0)),
        ("l", "default", predicates(0, 1, 0), one_of(1), one_of(1), one_of(0), one_of(0), one_of(0)),
        ("m", "default", predicates(1, 0, 0), one_of(2), one_of(1), one_of(0), one_of(0), one_of(0)),
        ("n", "default", predicates(0, 1, 0), one_of(2), one_of(1), one_of(0), one_of(0), one_of(0)),
        ("ñ", "default", predicates(0, 1, 1), one_of(2), one_of(1), one_of(0), one_of(0), one_of(0)),
        ("p", "default", predicates(1, 0, 0), one_of(0), one_of(0), one_of(0), one_of(0), one_of(0)),
        ("q", "default", predicates(0, 0, 1), one_of(0), one_of(0), one_of(1), one_of(0), one_of(1)),
        ("r", "default", predicates(0, 1, 0), one_of(1), one_of(1), one_of(1), one_of(0), one_of(2)),
        ("s", "default", predicates(0, 1, 0), one_of(1), one_of(0), one_of(0), one_of(0), one_of(0)),
        ("t", "default", predicates(0, 1, 0), one_of(0), one_of(0), one_of(0), one_of(0), one_of(0)),
        ("v", "default", predicates(1, 0, 0), aurora.OPEN, one_of(1), one_of(1), one_of(0), one_of(0)),
        ("w", "default", predicates(1, 0, 1), one_of(1), one_of(1), one_of(1), one_of(0), one_of(2)),
        ("x", "default", predicates(0, 1, 1), predicates(1, 1, 0), one_of(0), one_of(2), one_of(0), one_of(2)),
        ("y", "consonant", predicates(0, 1, 1), one_of(1), one_of(1), one_of(1), one_of(0), one_of(2)),
        ("z", "default", predicates(0, 1, 0), one_of(1), one_of(0), one_of(0), one_of(0), one_of(0)),
    )
    for text, sense, place, manner, phonation, stability, realization, composition in seeds:
        for variant in (text, text.upper()):
            lexicon = lexicon.bind(consonant_tensor(
                variant,
                place=place,
                manner=manner,
                phonation=phonation,
                stability=stability,
                realization=realization,
                composition=composition,
                sense=sense,
            ))

    # Y may operate as a vowel in conjunctional or syllabic contexts.
    for variant in ("y", "Y"):
        vowel_y = vowel_tensor("i" if variant == "y" else "I", "vowel")
        lexicon = lexicon.bind(replace(vowel_y, text=variant))

    symbols = (
        symbol_tensor(" ", boundary=one_of(0), pairing=one_of(0),
                      pause=(0, 0, 0), contour=one_of(0),
                      spacing=one_of(1), visibility=one_of(1)),
        symbol_tensor("\n", boundary=one_of(2), pairing=one_of(0),
                      pause=one_of(2), contour=one_of(0),
                      spacing=one_of(2), visibility=one_of(2)),
        symbol_tensor(",", boundary=one_of(1), pairing=one_of(0),
                      pause=one_of(0), contour=one_of(0)),
        symbol_tensor(";", boundary=one_of(1), pairing=one_of(0),
                      pause=one_of(1), contour=one_of(0)),
        symbol_tensor(":", boundary=one_of(1), pairing=one_of(0),
                      pause=one_of(1), contour=one_of(0)),
        symbol_tensor(".", boundary=one_of(2), pairing=one_of(0),
                      pause=one_of(2), contour=one_of(2), force=one_of(0)),
        symbol_tensor("¿", boundary=one_of(2), pairing=one_of(1),
                      pause=one_of(2), contour=one_of(1), force=one_of(1),
                      repetition=one_of(2)),
        symbol_tensor("?", boundary=one_of(2), pairing=one_of(2),
                      pause=one_of(2), contour=one_of(1), force=one_of(1),
                      repetition=one_of(2)),
        symbol_tensor("¡", boundary=one_of(2), pairing=one_of(1),
                      pause=one_of(2), contour=one_of(2), force=one_of(2),
                      repetition=one_of(2)),
        symbol_tensor("!", boundary=one_of(2), pairing=one_of(2),
                      pause=one_of(2), contour=one_of(2), force=one_of(2),
                      repetition=one_of(2)),
        symbol_tensor("(", boundary=one_of(1), pairing=one_of(1),
                      pause=(0, 0, 0), contour=one_of(0),
                      repetition=one_of(2)),
        symbol_tensor(")", boundary=one_of(1), pairing=one_of(2),
                      pause=(0, 0, 0), contour=one_of(0),
                      repetition=one_of(2)),
        symbol_tensor("-", boundary=one_of(0), pairing=one_of(0),
                      pause=(0, 0, 0), contour=one_of(0),
                      repetition=one_of(1)),
    )
    return lexicon.extend(symbols)


__all__ = [
    "CharacterFamily",
    "CharacterLexicon",
    "CharacterProperty",
    "CharacterQuery",
    "CharacterTensor",
    "PropertyBranch",
    "ROLE_ORDER",
    "SemanticRole",
    "consonant_tensor",
    "one_of",
    "predicates",
    "spanish_character_lexicon",
    "symbol_tensor",
    "vowel_tensor",
]
