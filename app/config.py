from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class DetectorConfig:
    omnishotcut: bool = True
    transnet: bool = True
    pyscenedetect: bool = True

@dataclass
class AnalyzerConfig:
    device: str = "auto"
    detectors: DetectorConfig = field(default_factory=DetectorConfig)
    boundary_tolerance_frames: int = 2
    transition_window_frames: int = 15
    extract_boundary_frames: bool = True
    generate_timeline: bool = True
    generate_contact_sheet: bool = True
    seed: int | None = None
    # Executables let users install model projects independently without binding
    # the app to their unstable Python APIs.
    omnishotcut_command: str | None = None
    transnet_command: str | None = None
