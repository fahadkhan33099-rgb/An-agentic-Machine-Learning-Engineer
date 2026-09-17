from __future__ import annotations
from collections import defaultdict
from app.models import Boundary
class BoundaryEnsemble:
    def __init__(self, tolerance_frames: int = 2, primary_source: str = "omnishotcut"):
        self.tolerance_frames, self.primary_source = tolerance_frames, primary_source
    def merge(self, omnishotcut_boundaries=(), transnet_boundaries=(), pyscenedetect_boundaries=()) -> list[Boundary]:
        candidates = sorted([*omnishotcut_boundaries, *transnet_boundaries, *pyscenedetect_boundaries], key=lambda b:b.frame)
        clusters=[]
        for candidate in candidates:
            if candidate.frame <= 0: continue
            if clusters and candidate.frame - clusters[-1][-1].frame <= self.tolerance_frames: clusters[-1].append(candidate)
            else: clusters.append([candidate])
        merged=[]
        for group in clusters:
            sources=tuple(sorted({b.source for b in group})); primary=[b for b in group if b.source == self.primary_source]
            representative=max(primary or group, key=lambda b: b.confidence if b.confidence is not None else 0)
            supplied=[b.confidence for b in group if b.confidence is not None]
            # Agreement score is explicitly heuristic, not calibrated probability.
            agreement=len(sources)/3; model_score=sum(supplied)/len(supplied) if supplied else 0.5
            confidence=round(0.65*agreement + 0.35*model_score, 3)
            merged.append(Boundary(representative.frame, representative.timestamp, "ensemble", confidence, sources, {"candidates":[{"frame":b.frame,"source":b.source,"confidence":b.confidence} for b in group]}))
        return merged
