"""Canonical simple-token tensors for the Aurora compact profile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from aurora_compact import aurora


def tensor_from_index(index: int) -> aurora.Triplet:
    """Encode 0..26 as three base-three trits, most significant first."""
    if not 0 <= index < 27:
        raise aurora.AuroraError("a simple DS index must be between 0 and 26")
    return index // 9, (index // 3) % 3, index % 3


def index_from_tensor(value: Sequence[aurora.Trit]) -> int:
    a, b, c = aurora.triplet(value)
    return 9 * a + 3 * b + c


@dataclass(frozen=True)
class SimpleToken:
    text: str
    ds: aurora.Triplet
    sense: str = "default"

    def __post_init__(self) -> None:
        if not self.text:
            raise aurora.AuroraError("token text cannot be empty")
        if not self.sense:
            raise aurora.AuroraError("token sense cannot be empty")
        object.__setattr__(self, "ds", aurora.triplet(self.ds))

    @property
    def knowledge(self) -> aurora.Knowledge:
        """Every simple token starts as (DO=222, DE=222, DS=token)."""
        return aurora.Knowledge(aurora.OPEN, aurora.OPEN, self.ds)

    @property
    def unit(self) -> aurora.Unit:
        return aurora.Unit(self.knowledge)


@dataclass(frozen=True)
class TokenLexicon:
    entries: tuple[SimpleToken, ...] = ()

    def bind(
        self,
        text: str,
        ds: Sequence[aurora.Trit],
        sense: str = "default",
    ) -> TokenLexicon:
        token = SimpleToken(text, aurora.triplet(ds), sense)
        if any(item.text == text and item.sense == sense for item in self.entries):
            raise aurora.AuroraError("that token sense is already bound")
        if token in self.entries:
            return self
        return TokenLexicon(self.entries + (token,))

    def allocate(self, text: str, sense: str = "default") -> TokenLexicon:
        used = {item.ds for item in self.entries}
        value = next((tensor_from_index(i) for i in range(27)
                      if tensor_from_index(i) not in used), None)
        if value is None:
            raise aurora.AuroraError("the simple triplet namespace is full")
        return self.bind(text, value, sense)

    def lookup(self, text: str) -> tuple[SimpleToken, ...]:
        return tuple(item for item in self.entries if item.text == text)

    def by_tensor(self, ds: Sequence[aurora.Trit]) -> tuple[SimpleToken, ...]:
        value = aurora.triplet(ds)
        return tuple(item for item in self.entries if item.ds == value)


def numeric_lexicon(names: Iterable[str]) -> TokenLexicon:
    """Bind ordered number names to their matching base-three DS values."""
    lexicon = TokenLexicon()
    for index, name in enumerate(names):
        lexicon = lexicon.bind(name, tensor_from_index(index))
    return lexicon


__all__ = [
    "SimpleToken",
    "TokenLexicon",
    "index_from_tensor",
    "numeric_lexicon",
    "tensor_from_index",
]
