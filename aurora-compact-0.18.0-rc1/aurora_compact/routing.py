"""In-memory P2P reference: the network is a dictionary one scale higher."""

from __future__ import annotations

from dataclasses import dataclass, replace

from aurora_compact import aurora, control, deduction


@dataclass(frozen=True)
class Node:
    node_id: str
    names: tuple[aurora.Triplet, ...]
    dictionary: aurora.AuroraDictionary = aurora.AuroraDictionary()

    def __post_init__(self) -> None:
        if not self.node_id:
            raise aurora.AuroraError("node_id cannot be empty")
        if not self.names:
            raise aurora.AuroraError("a node needs at least one tensor name")
        object.__setattr__(self, "names",
                           tuple(aurora.triplet(name) for name in self.names))

    def search(self, query: deduction.DeductiveQuery) -> tuple[aurora.Relation, ...]:
        return self.dictionary.search(
            query.result,
            anchor_ds=query.anchor,
            mode_ds=query.mode,
        )


@dataclass(frozen=True)
class Route:
    tensor: aurora.Triplet
    node_id: str
    successful_uses: int = 0
    last_success: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "tensor", aurora.triplet(self.tensor))


@dataclass(frozen=True)
class Resolution:
    scope: control.SearchScope
    matches: tuple[aurora.Relation, ...]
    network: Network
    node_id: str | None = None
    learned_route: bool = False
    stopped: bool = False


@dataclass(frozen=True)
class Network:
    nodes: tuple[Node, ...]
    routes: tuple[Route, ...] = ()

    def __post_init__(self) -> None:
        ids = tuple(node.node_id for node in self.nodes)
        if len(ids) != len(set(ids)):
            raise aurora.AuroraError("node ids must be unique")

    def node(self, node_id: str) -> Node:
        try:
            return next(node for node in self.nodes if node.node_id == node_id)
        except StopIteration as error:
            raise aurora.AuroraError(f"unknown node {node_id!r}") from error

    def _route_matches(
        self, query: deduction.DeductiveQuery
    ) -> tuple[deduction.DeductiveMatch, ...]:
        candidates = (
            deduction.TensorCandidate(
                route.tensor,
                route,
                route.successful_uses,
                route.last_success,
            )
            for route in self.routes
        )
        return deduction.search(query, candidates)

    def _named_nodes(
        self, source_id: str, query: deduction.DeductiveQuery
    ) -> tuple[tuple[Node, aurora.Triplet], ...]:
        candidates = [
            deduction.TensorCandidate(name, (node, name))
            for node in self.nodes if node.node_id != source_id
            for name in node.names
        ]
        return tuple(match.candidate.payload for match in deduction.search(
            query, candidates
        ))

    def _promote(self, selected: Route, tick: int) -> Network:
        routes = list(self.routes)
        index = routes.index(selected)
        routes[index] = replace(
            selected,
            successful_uses=selected.successful_uses + 1,
            last_success=tick,
        )
        return Network(self.nodes, tuple(routes))

    def _learn(self, tensor: aurora.Triplet, node_id: str, tick: int) -> Network:
        for route in self.routes:
            if route.tensor == tensor and route.node_id == node_id:
                return self._promote(route, tick)
        return Network(self.nodes, self.routes + (
            Route(tensor, node_id, successful_uses=1, last_success=tick),
        ))

    def resolve(
        self,
        source_id: str,
        query: deduction.DeductiveQuery,
        scope: control.SearchScope,
        tick: int = 0,
    ) -> Resolution:
        """Apply R(HDO): local=0, network=1, stop=2."""
        scope = control.SearchScope(scope)
        source = self.node(source_id)
        if scope is control.SearchScope.STOP:
            return Resolution(scope, (), self, stopped=True)
        if scope is control.SearchScope.LOCAL:
            return Resolution(scope, source.search(query), self, source_id)

        for match in self._route_matches(query):
            route = match.candidate.payload
            node = self.node(route.node_id)
            found = node.search(query)
            if found:
                updated = self._promote(route, tick)
                return Resolution(scope, found, updated, node.node_id)

        for node, name in self._named_nodes(source_id, query):
            found = node.search(query)
            if found:
                updated = self._learn(name, node.node_id, tick)
                return Resolution(scope, found, updated, node.node_id, True)
        return Resolution(scope, (), self)


__all__ = ["Network", "Node", "Resolution", "Route"]
