"""Deductive tensor lookup built from the Aurora TriGate itself."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, TypeVar

from aurora_compact import aurora

Payload = TypeVar("Payload")


@dataclass(frozen=True)
class DeductiveQuery:
    """A, M and R are known; every compatible B is a search result."""

    anchor: aurora.Triplet
    mode: aurora.Triplet
    result: aurora.Triplet

    def __post_init__(self) -> None:
        object.__setattr__(self, "anchor", aurora.triplet(self.anchor))
        object.__setattr__(self, "mode", aurora.triplet(self.mode))
        object.__setattr__(self, "result", aurora.triplet(self.result))

    @classmethod
    def for_tensor(cls, tensor: Sequence[aurora.Trit]) -> DeductiveQuery:
        """Canonical lookup: A=R=query and M=222.

        For query coordinates 0 or 1, B must equal the query.  Query 2 leaves
        B open, so a tensor can be extended without a separate similarity
        metric.
        """
        value = aurora.triplet(tensor)
        return cls(value, aurora.OPEN, value)

    @classmethod
    def for_exact_tensor(cls, tensor: Sequence[aurora.Trit]) -> DeductiveQuery:
        """Deduce one literal B, including a literal 2, without equality.

        A query 2 with M=2 is intentionally open.  When the caller needs the
        literal trit 2 instead, the complementary pair A=0, M=1 makes B=2 the
        sole value capable of producing R=2.
        """
        value = aurora.triplet(tensor)
        anchor = tuple(v if v != 2 else 0 for v in value)
        mode = tuple(2 if v != 2 else 1 for v in value)
        return cls(anchor, mode, value)

    @property
    def domains(self) -> tuple[frozenset[aurora.Trit], ...]:
        return tuple(
            aurora.candidate_domain(a, 2, m, r, aurora.Direction.DEDUCE_B)
            for a, m, r in zip(self.anchor, self.mode, self.result)
        )

    def accepts(self, candidate: Sequence[aurora.Trit]) -> bool:
        value = aurora.triplet(candidate)
        return all(v in domain for v, domain in zip(value, self.domains))

    def ambiguity(self, candidate: Sequence[aurora.Trit]) -> int:
        if not self.accepts(candidate):
            raise aurora.AuroraError("candidate does not close the query")
        return sum(len(domain) - 1 for domain in self.domains)


@dataclass(frozen=True)
class TensorCandidate:
    tensor: aurora.Triplet
    payload: object
    successful_uses: int = 0
    last_success: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "tensor", aurora.triplet(self.tensor))


@dataclass(frozen=True)
class DeductiveMatch:
    candidate: TensorCandidate
    domains: tuple[frozenset[aurora.Trit], ...]

    @property
    def ambiguity(self) -> int:
        return sum(len(domain) - 1 for domain in self.domains)


def search(
    query: DeductiveQuery,
    candidates: Iterable[TensorCandidate],
) -> tuple[DeductiveMatch, ...]:
    """Return every B that closes Majority3(A,B,M)=R.

    Ranking uses only structural openness and recorded successful reuse.  It
    introduces no geometric distance, embedding similarity or threshold.
    """
    matches = [
        DeductiveMatch(candidate, query.domains)
        for candidate in candidates
        if query.accepts(candidate.tensor)
    ]
    return tuple(sorted(
        matches,
        key=lambda match: (
            -match.ambiguity,
            match.candidate.successful_uses,
            match.candidate.last_success,
        ),
        reverse=True,
    ))


__all__ = ["DeductiveMatch", "DeductiveQuery", "TensorCandidate", "search"]
