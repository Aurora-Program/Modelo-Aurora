"""Incremental, auditable corpus training for Aurora fractal growth.

Training does not add labels, expected boundaries, a similarity function, or a
second segmentation algorithm.  Every observation is still processed by
``growth.compete_contextual_text``.  Re-executable superior closures first
select compatible inferior readings; every active reading then repeats the
ordinary fractal competition.  This module commits the returned immutable
memory, advances its logical clock, and records enough evidence to inspect
which exact closures became recurrent and how much reading space was avoided.

Text forms are audit evidence.  They never participate in closure, dictionary
search, competition, or ranking inside the Aurora kernel.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from . import aurora, characters, growth


CHECKPOINT_SCHEMA = "aurora-training-state-v1"


@dataclass(frozen=True)
class CountedForm:
    """One observable surface form associated with an exact closed unit."""

    text: str
    count: int = 1

    def __post_init__(self) -> None:
        if not self.text:
            raise aurora.AuroraError("closure evidence cannot contain an empty form")
        if self.count < 1:
            raise aurora.AuroraError("closure evidence counts must be positive")


@dataclass(frozen=True)
class CountedLevel:
    """Number of times one exact unit closed at a fractal level."""

    level: int
    count: int = 1

    def __post_init__(self) -> None:
        if self.level < 0:
            raise aurora.AuroraError("a fractal level cannot be negative")
        if self.count < 1:
            raise aurora.AuroraError("closure evidence counts must be positive")


@dataclass(frozen=True)
class ClosureEvidence:
    """Human-readable evidence for one exact dictionary relation.

    The unit and direction are the operational identity.  Forms, levels and
    observation numbers explain where that relation was seen; they do not feed
    back into the model.
    """

    unit: aurora.Unit
    direction: aurora.Direction
    forms: tuple[CountedForm, ...] = ()
    levels: tuple[CountedLevel, ...] = ()
    observations: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "direction", aurora.Direction(self.direction))
        if tuple(sorted(set(self.observations))) != self.observations:
            raise aurora.AuroraError(
                "evidence observations must be unique and strictly ordered"
            )

    @property
    def occurrences(self) -> int:
        return sum(item.count for item in self.forms)


@dataclass(frozen=True)
class TrainingState:
    """Committed Aurora memory after zero or more text observations."""

    dictionary: aurora.AuroraDictionary = field(
        default_factory=aurora.AuroraDictionary
    )
    tick: int = 0
    observation_count: int = 0
    evidence: tuple[ClosureEvidence, ...] = ()

    def __post_init__(self) -> None:
        if self.tick < 0 or self.observation_count < 0:
            raise aurora.AuroraError("training counters cannot be negative")


@dataclass(frozen=True)
class TrainingSample:
    """Raw text plus optional validated readings for contextual graphemes.

    A validated reading is grounding evidence, not a permanent lookup rule.
    Samples without it execute every available reading and let contextual
    closures in the ordinary dictionary decide which branches remain active.
    """

    text: str
    senses: tuple[tuple[int, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.text:
            raise aurora.AuroraError("a training sample cannot be empty")
        positions = tuple(position for position, _ in self.senses)
        if tuple(sorted(set(positions))) != positions:
            raise aurora.AuroraError(
                "sample senses must use unique positions in source order"
            )
        if any(position < 0 or position >= len(self.text)
               for position in positions):
            raise aurora.AuroraError("a sample sense position is outside its text")
        if any(not sense for _, sense in self.senses):
            raise aurora.AuroraError("a requested character sense cannot be empty")

    @classmethod
    def from_text(
        cls,
        text: str,
        senses: Mapping[int, str] | None = None,
    ) -> TrainingSample:
        return cls(text, tuple(sorted((senses or {}).items())))

    @property
    def sense_map(self) -> dict[int, str]:
        return dict(self.senses)


@dataclass(frozen=True)
class ObservationLevel:
    """Compact audit record for one competitive fractal level."""

    level: int
    candidates: int
    hypotheses: int
    winners: int
    resolved: bool
    complete: bool
    selected_forms: tuple[str, ...] = ()


@dataclass(frozen=True)
class TrainingObservation:
    """What changed when one unlabelled character stream was committed."""

    number: int
    text: str
    tick_start: int
    tick_stop: int
    levels: tuple[ObservationLevel, ...]
    closure_events: int
    new_relations: int
    reused_events: int
    relations_before: int
    relations_after: int
    complete: bool
    reading_hypotheses: int = 1
    reading_winners: int = 1
    reading_resolved: bool = True
    winning_senses: tuple[tuple[tuple[int, str], ...], ...] = ((),)
    reading_space: int = 1
    reading_pruned: int = 0
    downward_routes: int = 0
    downward_closed_positions: tuple[int, ...] = ()


@dataclass(frozen=True)
class TrainingStep:
    """Committed state plus the full re-executable result of one observation."""

    state: TrainingState
    observation: TrainingObservation
    result: growth.ContextualTextGrowth


@dataclass(frozen=True)
class CorpusTraining:
    """A deterministic sequence of committed observations."""

    initial_state: TrainingState
    state: TrainingState
    samples: tuple[TrainingSample, ...]
    epochs: int
    observations: tuple[TrainingObservation, ...]


@dataclass(frozen=True)
class LearnedClosure:
    """Display projection of a re-executable dictionary closure."""

    unit: aurora.Unit
    direction: aurora.Direction
    support: int
    last_success: int
    forms: tuple[CountedForm, ...]
    levels: tuple[CountedLevel, ...]
    observation_count: int

    @property
    def primary_form(self) -> str | None:
        return self.forms[0].text if self.forms else None


def _surface_form(text: str, node: growth.GrowthNode) -> str:
    positions = node.source_positions
    contiguous = tuple(range(positions[0], positions[-1] + 1))
    if positions == contiguous:
        return text[positions[0]:positions[-1] + 1]
    return "".join(text[position] for position in positions)


def _increment_form(
    forms: tuple[CountedForm, ...],
    text: str,
) -> tuple[CountedForm, ...]:
    counts = {item.text: item.count for item in forms}
    counts[text] = counts.get(text, 0) + 1
    return tuple(
        CountedForm(form, count)
        for form, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    )


def _increment_level(
    levels: tuple[CountedLevel, ...],
    level: int,
) -> tuple[CountedLevel, ...]:
    counts = {item.level: item.count for item in levels}
    counts[level] = counts.get(level, 0) + 1
    return tuple(CountedLevel(key, counts[key]) for key in sorted(counts))


RelationKey = tuple[
    aurora.Unit,
    aurora.Unit,
    aurora.Unit,
    aurora.Direction,
]


def _relation_key(relation: aurora.Relation) -> RelationKey:
    return (
        relation.input,
        relation.knowledge,
        relation.output,
        relation.direction,
    )


def _branch_relation(
    branch: growth.ReadingHypothesis,
    candidate: growth.ClosureCandidate,
) -> aurora.Relation:
    matches = tuple(
        relation for relation in branch.growth.dictionary.entries
        if relation.input == candidate.node.unit
        and relation.output == candidate.node.unit
        and relation.direction is aurora.Direction.INFER_R
        and relation.reexecutes_for(candidate.node.unit)
    )
    if len(matches) != 1:
        raise aurora.AuroraError(
            f"expected one contextual closure relation; found {len(matches)}"
        )
    return matches[0]


def _contextual_events(
    base: aurora.AuroraDictionary,
    result: growth.ContextualTextGrowth,
) -> tuple[
    tuple[growth.ClosureCandidate, int, growth.ReadingHypothesis], ...
]:
    """Return committed closure events without duplicating shared branches.

    Active reading winners confirm every closure they used.  A losing reading
    contributes only relations that are genuinely new, preserving alternatives
    without promoting a branch that the current context did not select.
    """
    known = {_relation_key(item) for item in base.entries}
    winners = set(result.winners)
    events: list[tuple[growth.ClosureCandidate, int, growth.ReadingHypothesis]] = []
    seen: set[tuple[RelationKey, int, tuple[int, ...]]] = set()
    for branch in result.hypotheses:
        active = branch in winners
        for level in branch.growth.levels:
            for candidate in level.candidates:
                relation = _branch_relation(branch, candidate)
                key = _relation_key(relation)
                if not active and key in known:
                    continue
                event_key = (
                    (key, level.level, candidate.node.source_positions)
                    if active else (key, -1, ())
                )
                if event_key in seen:
                    continue
                seen.add(event_key)
                events.append((candidate, level.level, branch))
    return tuple(events)


def _merge_contextual_dictionary(
    base: aurora.AuroraDictionary,
    result: growth.ContextualTextGrowth,
) -> aurora.AuroraDictionary:
    """Commit reading branches without letting enumeration order vote.

    For an active winner, the largest per-branch support delta is committed;
    using ``max`` avoids counting one shared closure once per mutually exclusive
    reading.  Losing alternatives enter memory once but do not accumulate use.
    """
    base_by_key = {_relation_key(item): item for item in base.entries}
    branch_maps = tuple(
        {
            _relation_key(relation): relation
            for relation in branch.growth.dictionary.entries
        }
        for branch in result.hypotheses
    )
    winner_indexes = tuple(
        index for index, branch in enumerate(result.hypotheses)
        if branch in result.winners
    )

    ordered_keys = list(base_by_key)
    for branch_map in branch_maps:
        for key in branch_map:
            if key not in ordered_keys:
                ordered_keys.append(key)

    merged: list[aurora.Relation] = []
    for key in ordered_keys:
        original = base_by_key.get(key)
        winner_versions = tuple(
            branch_maps[index][key]
            for index in winner_indexes
            if key in branch_maps[index]
        )
        if winner_versions:
            base_uses = 0 if original is None else original.successful_uses
            deltas = tuple(
                max(0, item.successful_uses - base_uses)
                for item in winner_versions
            )
            template = winner_versions[0]
            merged.append(aurora.Relation(
                template.input,
                template.knowledge,
                template.output,
                template.direction,
                base_uses + max(deltas),
                max(
                    (0 if original is None else original.last_success),
                    *(item.last_success for item in winner_versions),
                ),
            ))
        elif original is not None:
            merged.append(original)
        else:
            # The branch was explored but did not win.  Preserve the candidate
            # at genesis support without recording a successful reuse.
            template = next(
                branch_map[key] for branch_map in branch_maps if key in branch_map
            )
            merged.append(aurora.Relation(
                template.input,
                template.knowledge,
                template.output,
                template.direction,
            ))

    lexicon = list(base.lexicon)
    for branch in result.hypotheses:
        for unit in branch.growth.dictionary.lexicon:
            if unit not in lexicon:
                lexicon.append(unit)
    return aurora.AuroraDictionary(tuple(merged), tuple(lexicon))


def _record_evidence(
    evidence: tuple[ClosureEvidence, ...],
    text: str,
    events: Sequence[
        tuple[growth.ClosureCandidate, int, growth.ReadingHypothesis]
    ],
    observation_number: int,
) -> tuple[ClosureEvidence, ...]:
    records = {
        (item.unit, item.direction): item
        for item in evidence
    }
    for candidate, level, _branch in events:
        key = (candidate.node.unit, aurora.Direction.INFER_R)
        current = records.get(
            key,
            ClosureEvidence(candidate.node.unit, aurora.Direction.INFER_R),
        )
        observations = current.observations
        if observation_number not in observations:
            observations = (*observations, observation_number)
        records[key] = ClosureEvidence(
            current.unit,
            current.direction,
            _increment_form(
                current.forms,
                _surface_form(text, candidate.node),
            ),
            _increment_level(current.levels, level),
            observations,
        )
    return tuple(records.values())


def _observation_levels(
    text: str,
    result: growth.CompetitiveTextGrowth,
) -> tuple[ObservationLevel, ...]:
    records: list[ObservationLevel] = []
    for level in result.growth.levels:
        selected = level.selected
        records.append(ObservationLevel(
            level.level,
            len(level.candidates),
            level.hypothesis_count,
            len(level.winners),
            level.resolved,
            bool(selected and selected.complete),
            (() if selected is None else tuple(
                _surface_form(text, candidate.node)
                for candidate in selected.segments
            )),
        ))
    return tuple(records)


def evaluate_text(
    state: TrainingState,
    text: str,
    *,
    lexicon: characters.CharacterLexicon | None = None,
    senses: Mapping[int, str] | None = None,
    downward: bool = True,
) -> growth.ContextualTextGrowth:
    """Run selected readings without committing returned memory.

    ``downward=False`` exposes the exhaustive 0.10 baseline for equivalence
    and cost audits.
    """
    if not text:
        raise aurora.AuroraError("an evaluation text cannot be empty")
    return growth.compete_contextual_text(
        text,
        lexicon=lexicon,
        senses=senses,
        dictionary=state.dictionary,
        tick=state.tick,
        downward=downward,
    )


def observe_text(
    state: TrainingState,
    text: str,
    *,
    lexicon: characters.CharacterLexicon | None = None,
    senses: Mapping[int, str] | None = None,
) -> TrainingStep:
    """Commit one raw character stream using the ordinary competition cycle."""
    result = evaluate_text(
        state,
        text,
        lexicon=lexicon,
        senses=senses,
    )
    representative = result.winners[0].result
    levels = _observation_levels(text, representative)
    attempt_count = sum(
        len(level.attempts)
        for branch in result.hypotheses
        for level in branch.growth.levels
    )
    events = _contextual_events(state.dictionary, result)
    closure_events = len(events)
    before = len(state.dictionary.entries)
    dictionary = _merge_contextual_dictionary(state.dictionary, result)
    source_options = growth.character_options(text, lexicon, senses)
    dictionary = dictionary.register(*(
        item.unit for options in source_options for item in options
    ))
    after = len(dictionary.entries)
    new_relations = after - before
    observation_number = state.observation_count + 1
    tick_stop = state.tick + attempt_count + 1
    evidence = _record_evidence(
        state.evidence,
        text,
        events,
        observation_number,
    )
    committed = TrainingState(
        dictionary,
        tick_stop,
        observation_number,
        evidence,
    )
    observation = TrainingObservation(
        observation_number,
        text,
        state.tick,
        tick_stop,
        levels,
        closure_events,
        new_relations,
        closure_events - new_relations,
        before,
        after,
        bool(result.selected and result.selected.growth.complete),
        len(result.hypotheses),
        len(result.winners),
        result.resolved,
        result.winner_senses,
        result.total_readings,
        result.pruned_readings,
        len(result.selection.routes),
        result.selection.closed_positions,
    )
    return TrainingStep(committed, observation, result)


def _sample(item: str | TrainingSample) -> TrainingSample:
    return item if isinstance(item, TrainingSample) else TrainingSample(item)


def train_corpus(
    samples: Iterable[str | TrainingSample],
    *,
    epochs: int = 1,
    state: TrainingState | None = None,
    lexicon: characters.CharacterLexicon | None = None,
) -> CorpusTraining:
    """Observe raw samples in stable order for a reproducible number of epochs."""
    if epochs < 1:
        raise aurora.AuroraError("training requires at least one epoch")
    prepared = tuple(_sample(item) for item in samples)
    if not prepared:
        raise aurora.AuroraError("training requires at least one sample")
    initial = TrainingState() if state is None else state
    current = initial
    observations: list[TrainingObservation] = []
    for _ in range(epochs):
        for sample in prepared:
            step = observe_text(
                current,
                sample.text,
                lexicon=lexicon,
                senses=sample.sense_map,
            )
            current = step.state
            observations.append(step.observation)
    return CorpusTraining(
        initial,
        current,
        prepared,
        epochs,
        tuple(observations),
    )


def ranked_closures(state: TrainingState) -> tuple[LearnedClosure, ...]:
    """Project every exact closure in dictionary-support order.

    Sorting is only a reporting view.  It does not modify the dictionary and
    is not used by segmentation competition.
    """
    evidence = {
        (item.unit, item.direction): item
        for item in state.evidence
    }
    learned: list[LearnedClosure] = []
    for relation in state.dictionary.entries:
        if relation.input != relation.output:
            continue
        key = (relation.input, relation.direction)
        audit = evidence.get(key)
        learned.append(LearnedClosure(
            relation.input,
            relation.direction,
            relation.successful_uses + 1,
            relation.last_success,
            () if audit is None else audit.forms,
            () if audit is None else audit.levels,
            0 if audit is None else len(audit.observations),
        ))
    return tuple(sorted(
        learned,
        key=lambda item: (
            -item.support,
            -item.observation_count,
            -(item.forms[0].count if item.forms else 0),
            item.primary_form or "",
            repr(item.unit),
        ),
    ))


def _knowledge_data(knowledge: aurora.Knowledge) -> dict[str, list[int]]:
    return {
        "do": list(knowledge.do),
        "de": list(knowledge.de),
        "ds": list(knowledge.ds),
    }


def _knowledge_from_data(data: Mapping[str, object]) -> aurora.Knowledge:
    return aurora.Knowledge(data["do"], data["de"], data["ds"])  # type: ignore[arg-type]


def _unit_data(unit: aurora.Unit) -> dict[str, object]:
    return {
        "state": _knowledge_data(unit.state),
        "children": [_unit_data(child) for child in unit.children],
        "direction": int(unit.direction),
        "do_before": list(unit.do_before),
    }


def _unit_from_data(data: Mapping[str, object]) -> aurora.Unit:
    children = tuple(
        _unit_from_data(child)  # type: ignore[arg-type]
        for child in data.get("children", [])  # type: ignore[union-attr]
    )
    return aurora.Unit(
        _knowledge_from_data(data["state"]),  # type: ignore[arg-type]
        children,
        aurora.Direction(data["direction"]),  # type: ignore[arg-type]
        aurora.triplet(data["do_before"]),  # type: ignore[arg-type]
    )


def state_to_data(state: TrainingState) -> dict[str, object]:
    """Return a JSON-compatible, versioned checkpoint representation."""
    return {
        "schema": CHECKPOINT_SCHEMA,
        "tick": state.tick,
        "observation_count": state.observation_count,
        "dictionary": {
            "entries": [
                {
                    "input": _unit_data(relation.input),
                    "knowledge": _unit_data(relation.knowledge),
                    "output": _unit_data(relation.output),
                    "direction": int(relation.direction),
                    "successful_uses": relation.successful_uses,
                    "last_success": relation.last_success,
                }
                for relation in state.dictionary.entries
            ],
            "lexicon": [_unit_data(unit) for unit in state.dictionary.lexicon],
        },
        "evidence": [
            {
                "unit": _unit_data(item.unit),
                "direction": int(item.direction),
                "forms": [
                    {"text": form.text, "count": form.count}
                    for form in item.forms
                ],
                "levels": [
                    {"level": level.level, "count": level.count}
                    for level in item.levels
                ],
                "observations": list(item.observations),
            }
            for item in state.evidence
        ],
    }


def state_from_data(data: Mapping[str, object]) -> TrainingState:
    """Reconstruct a training state from a versioned checkpoint mapping."""
    if data.get("schema") != CHECKPOINT_SCHEMA:
        raise aurora.AuroraError("unsupported Aurora training checkpoint schema")
    dictionary_data = data["dictionary"]  # type: ignore[assignment]
    entries = tuple(
        aurora.Relation(
            _unit_from_data(item["input"]),
            _unit_from_data(item["knowledge"]),
            _unit_from_data(item["output"]),
            aurora.Direction(item["direction"]),
            int(item["successful_uses"]),
            int(item["last_success"]),
        )
        for item in dictionary_data["entries"]  # type: ignore[index,union-attr]
    )
    lexicon = tuple(
        _unit_from_data(item)
        for item in dictionary_data["lexicon"]  # type: ignore[index,union-attr]
    )
    evidence = tuple(
        ClosureEvidence(
            _unit_from_data(item["unit"]),
            aurora.Direction(item["direction"]),
            tuple(CountedForm(form["text"], int(form["count"]))
                  for form in item["forms"]),
            tuple(CountedLevel(int(level["level"]), int(level["count"]))
                  for level in item["levels"]),
            tuple(int(number) for number in item["observations"]),
        )
        for item in data["evidence"]  # type: ignore[index]
    )
    return TrainingState(
        aurora.AuroraDictionary(entries, lexicon),
        int(data["tick"]),  # type: ignore[arg-type]
        int(data["observation_count"]),  # type: ignore[arg-type]
        evidence,
    )


def save_state(state: TrainingState, path: str | Path) -> Path:
    """Write a deterministic UTF-8 JSON checkpoint and return its path."""
    destination = Path(path)
    destination.write_text(
        json.dumps(state_to_data(state), ensure_ascii=False,
                   separators=(",", ":"), sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination


def load_state(path: str | Path) -> TrainingState:
    """Load a JSON checkpoint produced by :func:`save_state`."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise aurora.AuroraError("an Aurora checkpoint must contain an object")
    return state_from_data(data)


__all__ = [
    "CHECKPOINT_SCHEMA",
    "ClosureEvidence",
    "CorpusTraining",
    "CountedForm",
    "CountedLevel",
    "LearnedClosure",
    "ObservationLevel",
    "TrainingObservation",
    "TrainingSample",
    "TrainingState",
    "TrainingStep",
    "evaluate_text",
    "load_state",
    "observe_text",
    "ranked_closures",
    "save_state",
    "state_from_data",
    "state_to_data",
    "train_corpus",
]
