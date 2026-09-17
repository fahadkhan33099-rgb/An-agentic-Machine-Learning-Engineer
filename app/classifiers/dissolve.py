from __future__ import annotations
import cv2, numpy as np
def looks_like_dissolve(frames: list[np.ndarray]) -> bool:
    if len(frames) < 5: return False
    means=np.array([cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).mean() for f in frames]); steps=np.abs(np.diff(means))
    return bool(np.count_nonzero(steps > 1) >= max(3, len(steps)//2) and steps.max() < 35)
