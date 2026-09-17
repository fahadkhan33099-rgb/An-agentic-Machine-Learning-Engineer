from __future__ import annotations
from app.models import Boundary, Shot

def build_shots(frame_count: int, fps: float, boundaries: list[Boundary], transitions: dict[int, object]) -> list[Shot]:
    """Create inclusive zero-based shot ranges from first-frame-of-new-shot boundaries."""
    starts=sorted({0, *(b.frame for b in boundaries if 0 < b.frame < frame_count)})
    shots=[]
    for i,start in enumerate(starts):
        end=starts[i+1]-1 if i+1<len(starts) else frame_count-1
        boundary=next((b for b in boundaries if b.frame==start),None); result=transitions.get(start)
        shots.append(Shot(i+1,start,end,start/fps,end/fps,getattr(result,"transition_type",None),getattr(result,"subtype",None),boundary.confidence if boundary else None,boundary.detectors if boundary else ()))
    return shots
