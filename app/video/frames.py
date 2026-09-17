from __future__ import annotations
from pathlib import Path
import cv2
import numpy as np

class FrameReader:
    """Random-access OpenCV reader; all arguments and returned indices are zero-based."""
    def __init__(self, video_path: str):
        self.path = video_path; self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened(): raise RuntimeError(f"Cannot decode video: {video_path}")
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
    def get(self, index: int) -> np.ndarray | None:
        if not 0 <= index < self.frame_count: return None
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index); ok, frame = self.cap.read()
        return frame if ok else None
    def window(self, center: int, radius: int) -> list[np.ndarray]:
        return [f for i in range(max(0, center-radius), min(self.frame_count, center+radius+1)) if (f := self.get(i)) is not None]
    def close(self): self.cap.release()
    def __enter__(self): return self
    def __exit__(self, *_): self.close()

def write_jpeg(path: str | Path, frame: np.ndarray) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(path), frame): raise RuntimeError(f"Could not write image: {path}")
