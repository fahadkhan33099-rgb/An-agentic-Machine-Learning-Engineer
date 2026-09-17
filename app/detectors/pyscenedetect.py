from __future__ import annotations
from app.models import Boundary
class PySceneDetectDetector:
    source = "pyscenedetect"
    def __init__(self, fps: float, threshold: float = 27.0): self.fps, self.threshold = fps, threshold
    def detect(self, video_path: str) -> list[Boundary]:
        try:
            from scenedetect import detect, ContentDetector
        except ImportError as exc:
            raise RuntimeError("PySceneDetect is enabled but not installed. Install dependencies with pip install -e .") from exc
        scenes = detect(video_path, ContentDetector(threshold=self.threshold))
        # Scene start frame is exactly the first frame of new shot. Ignore frame 0.
        return [Boundary(s[0].get_frames(), s[0].get_seconds(), self.source, None) for s in scenes[1:]]
