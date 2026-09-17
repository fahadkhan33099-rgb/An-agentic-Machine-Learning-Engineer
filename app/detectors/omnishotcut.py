from __future__ import annotations
from app.detectors.command_adapter import run_json_detector
class OmniShotCutDetector:
    """OmniShotCut v1.5 adapter. Model-specific output parsing is kept here."""
    source = "omnishotcut"
    def __init__(self, fps: float, command: str | None = None, device: str = "auto"):
        self.fps, self.command, self.device = fps, command, device
    def detect(self, video_path: str): return run_json_detector(self.command, video_path, self.source, self.fps)
