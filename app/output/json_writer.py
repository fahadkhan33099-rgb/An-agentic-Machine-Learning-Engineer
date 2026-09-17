from __future__ import annotations
import json
from dataclasses import asdict
from pathlib import Path
from app.models import VideoMetadata, Boundary, Shot
def write_outputs(output_dir: str | Path, video_path: str, metadata: VideoMetadata, shots: list[Shot], boundaries: list[Boundary], models: dict) -> None:
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    video={"path":str(video_path), **asdict(metadata)}
    (out/"shots.json").write_text(json.dumps({"software_version":"0.1.0","models":models,"video":video,"shots":[_shot(s) for s in shots]},indent=2))
    (out/"boundaries.json").write_text(json.dumps({"software_version":"0.1.0","video":video,"boundaries":[asdict(b) for b in boundaries]},indent=2))
def _shot(shot: Shot):
    value=asdict(shot); value["transition"]=value.pop("transition_type"); value["subtype"]=value.pop("transition_subtype"); return value
