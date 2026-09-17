from __future__ import annotations
import cv2, numpy as np
def wipe_subtype(before: np.ndarray, after: np.ndarray, middle: np.ndarray) -> str | None:
    # A conservative spatial-mixture test; direction is only reported when dominant.
    a=cv2.cvtColor(before,cv2.COLOR_BGR2GRAY).astype(float); b=cv2.cvtColor(after,cv2.COLOR_BGR2GRAY).astype(float); m=cv2.cvtColor(middle,cv2.COLOR_BGR2GRAY).astype(float)
    da=np.abs(m-a); db=np.abs(m-b); mask=da < db
    row=mask.mean(1); col=mask.mean(0)
    if max(row.mean(), col.mean()) and np.std(col) > .32: return "Wipe Left" if col[0] > col[-1] else "Wipe Right"
    if np.std(row) > .32: return "Wipe Up" if row[0] > row[-1] else "Wipe Down"
    return None
