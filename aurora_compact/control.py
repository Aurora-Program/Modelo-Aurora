"""Emergent Aurora control: C4-C6 and the HDS/HDE/HDO projections."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Sequence

from aurora_compact import aurora


class Coherence(IntEnum):
    INCOHERENT = 0
    COHERENT = 1
    AMBIGUOUS = 2


class SearchScope(IntEnum):
    LOCAL = 0
    NETWORK = 1
    STOP = 2


@dataclass(frozen=True)
class ChannelControl:
    """Three lower R values form H; one more TriGate produces R(H)."""

    signature: aurora.Triplet
    lower: tuple[aurora.Packet, aurora.Packet, aurora.Packet]
    packet: aurora.Packet


@dataclass(frozen=True)
class ControlResult:
    c4: aurora.FaceResult
    c5: aurora.FaceResult
    c6: aurora.FaceResult
    hds: ChannelControl
    hde: ChannelControl
    hdo: ChannelControl

    @property
    def knowledge(self) -> aurora.Knowledge:
        """Project control as the same complete ``K`` emitted by every face.

        HDS, HDE and HDO are the three homologous groups at control scale.
        Their packets therefore project R, E and O back into DS, DE and DO;
        operation, coherence and scope are readings of this tensor rather than
        three externally stored control fields.
        """

        packets = self.hds.packet, self.hde.packet, self.hdo.packet
        return aurora.Knowledge(
            tuple(packet.o for packet in packets),
            tuple(packet.e for packet in packets),
            tuple(packet.r for packet in packets),
        )

    @property
    def unit(self) -> aurora.Unit:
        """The complete control tensor, reusable as an ordinary Aurora unit."""

        return aurora.Unit(self.knowledge)

    @property
    def reexecutes(self) -> bool:
        """Rebuild both control stages from their preserved face inputs."""

        original = self.c4, self.c5, self.c6
        faces = tuple(
            aurora.face(face.inputs, face.direction, face.do_before)
            for face in original
        )
        return (
            faces == original
            and _channel(faces, "ds") == self.hds
            and _channel(faces, "de") == self.hde
            and _channel(faces, "do") == self.hdo
        )

    @property
    def operation(self) -> aurora.Direction:
        return aurora.Direction(self.hds.packet.r)

    @property
    def coherence(self) -> Coherence:
        return Coherence(self.hde.packet.r)

    @property
    def scope(self) -> SearchScope:
        return SearchScope(self.hdo.packet.r)


def _channel(
    faces: tuple[aurora.FaceResult, aurora.FaceResult, aurora.FaceResult],
    name: str,
) -> ChannelControl:
    lower = tuple(
        aurora.trigate(
            *getattr(result.knowledge, name),
            direction=aurora.Direction.INFER_R,
        )
        for result in faces
    )
    signature = aurora.triplet(packet.r for packet in lower)
    packet = aurora.trigate(*signature, direction=aurora.Direction.INFER_R)
    return ChannelControl(signature, lower, packet)


def interpret(
    hds: Sequence[aurora.Trit],
    hde: Sequence[aurora.Trit],
    hdo: Sequence[aurora.Trit],
) -> tuple[aurora.Direction, Coherence, SearchScope]:
    """Read the three emergent control signatures without external ideals."""
    ds = aurora.trigate(*aurora.triplet(hds)).r
    de = aurora.trigate(*aurora.triplet(hde)).r
    do = aurora.trigate(*aurora.triplet(hdo)).r
    return aurora.Direction(ds), Coherence(de), SearchScope(do)


def control_faces(
    input_unit: aurora.Unit,
    knowledge_unit: aurora.Unit,
    output_unit: aurora.Unit,
    direction: aurora.Direction = aurora.Direction.INFER_R,
    do_t: Sequence[aurora.Trit] = aurora.OPEN,
) -> ControlResult:
    """Use ordinary faces at both sides of the autosimilar boundary."""
    do_t = aurora.triplet(do_t)
    direction = aurora.Direction(direction)
    units = input_unit, knowledge_unit, output_unit
    c4 = aurora.face(tuple(unit.state.ds for unit in units), direction, do_t)
    c5 = aurora.face(tuple(unit.state.de for unit in units), direction, do_t)
    c6 = aurora.face(tuple(unit.state.do for unit in units), direction, do_t)
    faces = c4, c5, c6
    return ControlResult(
        c4,
        c5,
        c6,
        _channel(faces, "ds"),
        _channel(faces, "de"),
        _channel(faces, "do"),
    )


__all__ = [
    "ChannelControl",
    "Coherence",
    "ControlResult",
    "SearchScope",
    "control_faces",
    "interpret",
]
