"""Fractal C-O orientation for executable Aurora tensor programs.

The dictionary is a ternary forest rather than a scored list.  Every three
program nodes are presented position by position to the same nine Aurora
faces; their emergent program becomes an ordinary node at the next level.

Lookup repeats one structural rule at every level.  Learning and inference
select their determined C branch (0 and 1).  Deduction keeps C=2 open and lets
the node's tensorial DO atom supply O.  If that atom is also open, all exact
descendants remain alternatives and no branch is fabricated.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from . import aurora, relational, tensor_program


@dataclass(frozen=True)
class ProgramNode:
    """One executable program and the three dictionary nodes that formed it."""

    program: tensor_program.ProgramTensor
    level: int = 0
    children: tuple[ProgramNode, ...] = ()
    induction: tensor_program.ProgramInduction | None = None

    def __post_init__(self) -> None:
        if self.level < 0:
            raise aurora.AuroraError("a dictionary level cannot be negative")
        if not self.children:
            if self.level or self.induction is not None:
                raise aurora.AuroraError("a leaf program must occupy level zero")
            return
        if len(self.children) != 3 or self.induction is None:
            raise aurora.AuroraError(
                "a fractal dictionary node needs three children and one induction"
            )
        if any(child.level != self.level - 1 for child in self.children):
            raise aurora.AuroraError("dictionary children must share the lower level")
        if self.induction.candidates != tuple(
            child.program for child in self.children
        ):
            raise aurora.AuroraError(
                "dictionary induction must preserve its three child programs"
            )
        if self.program != self.induction.emergent:
            raise aurora.AuroraError("dictionary node must contain its emergent code")

    @classmethod
    def combine(
        cls,
        children: Sequence[ProgramNode],
        direction: aurora.Direction,
        phase: Sequence[aurora.Trit],
    ) -> ProgramNode:
        if len(children) != 3:
            raise aurora.AuroraError("dictionary synthesis needs exactly three nodes")
        triple = tuple(children)
        if len({child.level for child in triple}) != 1:
            raise aurora.AuroraError("dictionary synthesis cannot mix levels")
        induction = tensor_program.induce(
            tuple(child.program for child in triple),
            phase,
            direction=direction,
        )
        return cls(induction.emergent, triple[0].level + 1, triple, induction)

    @property
    def order_unit(self) -> aurora.Unit:
        """The ordinary DO-code atom that orients this dictionary node."""

        return self.program.atoms[tensor_program.PHASE_ATOM]

    @property
    def leaf_count(self) -> int:
        return 1 if not self.children else sum(child.leaf_count for child in self.children)

    @property
    def leaves(self) -> tuple[ProgramNode, ...]:
        if not self.children:
            return (self,)
        return tuple(leaf for child in self.children for leaf in child.leaves)

    @property
    def all_reexecute(self) -> bool:
        return (
            self.program.all_reexecute
            and (self.induction is None or self.induction.all_reexecute)
            and all(child.all_reexecute for child in self.children)
        )


@dataclass(frozen=True)
class DictionaryRoute:
    """One C-O descent, or the exact alternatives retained by an open O."""

    direction: aurora.Direction
    do_before: aurora.Triplet
    indices: tuple[int, ...]
    nodes: tuple[ProgramNode, ...]
    selected: ProgramTensor | None
    alternatives: tuple[ProgramTensor, ...] = ()

    @property
    def resolved(self) -> bool:
        return self.selected is not None


@dataclass(frozen=True)
class DictionarySearch:
    """One exact requirement read through the ordered fractal frontier."""

    requirement: tensor_program.ProgramTensor
    direction: aurora.Direction
    do_before: aurora.Triplet
    state: aurora.Trit
    routes: tuple[DictionaryRoute, ...]
    matched: tensor_program.ProgramTensor | None = None
    alternatives: tuple[tensor_program.ProgramTensor, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "direction", aurora.Direction(self.direction))
        object.__setattr__(self, "do_before", aurora.triplet(self.do_before))
        object.__setattr__(self, "state", aurora.trit(self.state))
        if self.state == 1 and self.matched != self.requirement:
            raise aurora.AuroraError("a closed dictionary search must match its requirement")
        if self.state != 1 and self.matched is not None:
            raise aurora.AuroraError("only a closed dictionary search can expose a match")
        if self.state == 2 and not self.alternatives:
            raise aurora.AuroraError("an open dictionary search must preserve alternatives")


@dataclass(frozen=True)
class FractalProgramDictionary:
    """Immutable 1-3-9 program memory with ternary structural promotion."""

    direction: aurora.Direction = aurora.Direction.INFER_R
    do: aurora.Triplet = aurora.OPEN
    levels: tuple[tuple[ProgramNode, ...], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "direction", aurora.Direction(self.direction))
        object.__setattr__(self, "do", aurora.triplet(self.do))
        if any(len(nodes) > 2 for nodes in self.levels):
            raise aurora.AuroraError(
                "a normalized ternary dictionary keeps fewer than three frontier nodes"
            )
        for level, nodes in enumerate(self.levels):
            if any(node.level != level for node in nodes):
                raise aurora.AuroraError("dictionary node stored at the wrong level")

    def remember(self, program: tensor_program.ProgramTensor) -> FractalProgramDictionary:
        """Insert code and let every complete ternary group feed the next level."""

        buckets = [list(nodes) for nodes in self.levels]
        carry = ProgramNode(program)
        level = 0
        while True:
            if level == len(buckets):
                buckets.append([])
            buckets[level].append(carry)
            if len(buckets[level]) < 3:
                break
            children = tuple(buckets[level])
            buckets[level].clear()
            carry = ProgramNode.combine(children, self.direction, self.do)
            level += 1
        return FractalProgramDictionary(
            self.direction,
            self.do,
            tuple(tuple(nodes) for nodes in buckets),
        )

    def observe(self, execution: relational.Execution) -> FractalProgramDictionary:
        """Reflect code-bearing firings and feed them into the same ternary memory."""

        memory = self
        for firing in execution.firings:
            if firing.seed.provenance:
                memory = memory.remember(
                    tensor_program.ProgramTensor.from_firing(firing)
                )
        return memory

    @property
    def frontier(self) -> tuple[ProgramNode, ...]:
        return tuple(node for nodes in self.levels for node in nodes)

    @property
    def complete_root(self) -> ProgramNode | None:
        frontier = self.frontier
        if len(frontier) == 1 and frontier[0].leaf_count > 1:
            return frontier[0]
        return None

    def route(
        self,
        direction: aurora.Direction,
        do_t: Sequence[aurora.Trit] = aurora.OPEN,
    ) -> DictionaryRoute:
        """Descend one complete root by the same C-O rule at every scale.

        C=0 and C=1 are determined indices.  C=2 asks the node's DO atom for O.
        The superior orientation trit selected at one node becomes the phase of
        the next node.  An unordered DO atom leaves every descendant available.
        """

        root = self.complete_root
        if root is None:
            raise aurora.AuroraError("C-O routing needs one complete fractal root")
        return self._route_node(root, direction, do_t)

    @staticmethod
    def _route_node(
        root: ProgramNode,
        direction: aurora.Direction,
        do_t: Sequence[aurora.Trit] = aurora.OPEN,
    ) -> DictionaryRoute:
        """Apply one C-O descent to any frontier node, including one leaf."""

        direction = aurora.Direction(direction)
        do_t = aurora.triplet(do_t)
        phase = do_t[int(direction)]
        node = root
        indices: list[int] = []
        visited = [node]
        while node.children:
            if direction is aurora.Direction.DEDUCE_B:
                ordering = aurora.order_triplet(node.order_unit.value, phase)
                if not ordering.valid:
                    alternatives = tuple(leaf.program for leaf in node.leaves)
                    return DictionaryRoute(
                        direction, do_t, tuple(indices), tuple(visited), None,
                        alternatives,
                    )
                index = ordering.o
            else:
                index = int(direction)
            indices.append(index)
            phase = node.order_unit.state.do[index]
            node = node.children[index]
            visited.append(node)
        return DictionaryRoute(
            direction, do_t, tuple(indices), tuple(visited), node.program
        )

    def search(
        self,
        requirement: tensor_program.ProgramTensor,
        direction: aurora.Direction,
        do_t: Sequence[aurora.Trit] = aurora.OPEN,
    ) -> DictionarySearch:
        """Read one exact program requirement through the fractal forest.

        Higher structural levels are consulted before their later, unfinished
        frontiers.  A determined route that does not re-execute the requested
        program allows the next frontier node to be tried.  An open route does
        not mean absence: it returns trit 2 and preserves every descendant.
        """

        direction = aurora.Direction(direction)
        do_t = aurora.triplet(do_t)
        routes: list[DictionaryRoute] = []
        for level in range(len(self.levels) - 1, -1, -1):
            for node in self.levels[level]:
                route = self._route_node(node, direction, do_t)
                routes.append(route)
                if not route.resolved:
                    return DictionarySearch(
                        requirement, direction, do_t, 2, tuple(routes), None,
                        route.alternatives,
                    )
                if (
                    route.selected == requirement
                    and requirement.executable
                    and requirement.all_reexecute
                ):
                    return DictionarySearch(
                        requirement, direction, do_t, 1, tuple(routes),
                        requirement,
                    )
        return DictionarySearch(
            requirement, direction, do_t, 0, tuple(routes)
        )

    def execute_root(
        self,
        initial: Mapping[
            aurora.Triplet,
            Sequence[aurora.Trit]
            | relational.Signal
            | Sequence[relational.Signal],
        ],
        *,
        budget: int = 729,
    ) -> tensor_program.ProgramExecution:
        """Execute code that reached the root through automatic 3-to-1 feedback."""

        root = self.complete_root
        if root is None:
            raise aurora.AuroraError("the dictionary does not yet have one root")
        if not root.program.executable:
            raise aurora.AuroraError("the emergent dictionary root is still open")
        return tensor_program.execute((root.program,), initial, budget=budget)


__all__ = [
    "DictionarySearch",
    "DictionaryRoute",
    "FractalProgramDictionary",
    "ProgramNode",
]
