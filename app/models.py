"""Stable, detector-independent data objects. Frame indices are zero-based."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class VideoMetadata:
    fps: float
    frame_count: int
    duration_seconds: float
    width: int
    height: int
    codec: str | None = None

@dataclass(frozen=True)
class Boundary:
    frame: int
    timestamp: float
    source: str
    confidence: float | None = None
    detectors: tuple[str, ...] = ()
    evidence: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class TransitionResult:
    transition_type: str
    subtype: str | None
    confidence: float | None

@dataclass(frozen=True)
class Shot:
    shot_id: int
    start_frame: int
    end_frame: int
    start_time: float
    end_time: float
    transition_type: str | None
    transition_subtype: str | None
    confidence: float | None
    detectors: tuple[str, ...] = ()
