from __future__ import annotations
import cv2, numpy as np
def fade_subtype(frames: list[np.ndarray]) -> str | None:
    if len(frames) < 5: return None
    gray=np.array([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).mean() for f in frames])
    # Center must be uniform extreme and both sides materially differ: dark scenes alone fail.
    middle=frames[len(frames)//2]; uniform=float(cv2.cvtColor(middle,cv2.COLOR_BGR2GRAY).std()) < 12
    if uniform and gray.min() < 18 and gray.max()-gray.min() > 45: return "Fade Black"
    if uniform and gray.max() > 237 and gray.max()-gray.min() > 45: return "Fade White"
    return None
