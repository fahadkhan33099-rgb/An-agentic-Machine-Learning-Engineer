from __future__ import annotations
import cv2, numpy as np
from app.models import TransitionResult
from .fade import fade_subtype
from .dissolve import looks_like_dissolve
from .wipe import wipe_subtype
class TransitionClassifier:
    """Conservative local transition classifier. It returns Unknown over unsupported claims."""
    def classify(self, before_frames, transition_frames, after_frames) -> TransitionResult:
        frames=[*before_frames, *transition_frames, *after_frames]
        fade=fade_subtype(frames)
        if fade: return TransitionResult("FADE", fade, .70)
        if len(frames) >= 5:
            wipe=wipe_subtype(frames[0], frames[-1], frames[len(frames)//2])
            if wipe: return TransitionResult("WIPE", wipe, .55)
            if looks_like_dissolve(frames): return TransitionResult("DISSOLVE", None, .55)
        if before_frames and after_frames:
            a=cv2.cvtColor(before_frames[-1],cv2.COLOR_BGR2GRAY); b=cv2.cvtColor(after_frames[0],cv2.COLOR_BGR2GRAY)
            if float(np.mean(cv2.absdiff(a,b))) > 10: return TransitionResult("CUT", None, .60)
        return TransitionResult("UNKNOWN", "Unknown", None)
