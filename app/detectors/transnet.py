from __future__ import annotations
from app.detectors.command_adapter import run_json_detector
class TransNetDetector:
    """TransNet V2 adapter for a local JSON-emitting inference command."""
    source = "transnet"
    def __init__(self, fps: float, command: str | None = None, device: str = "auto"):
        self.fps, self.command, self.device = fps, command, device
    def detect(self, video_path: str): return run_json_detector(self.command, video_path, self.source, self.fps)
