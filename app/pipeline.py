from __future__ import annotations
import random, numpy as np
from pathlib import Path
from app.config import AnalyzerConfig
from app.models import Boundary, Shot
from app.video.metadata import read_metadata
from app.video.frames import FrameReader
from app.detectors.omnishotcut import OmniShotCutDetector
from app.detectors.transnet import TransNetDetector
from app.detectors.pyscenedetect import PySceneDetectDetector
from app.detectors.ensemble import BoundaryEnsemble
from app.detectors.command_adapter import ModelUnavailableError
from app.classifiers.transition import TransitionClassifier
from app.extraction.boundary_frames import extract_boundary_frames, extract_shot_endpoint_frames
from app.extraction.thumbnails import create_contact_sheet
from app.output.json_writer import write_outputs
from app.output.csv_writer import write_shots_csv
from app.output.timeline import create_timeline

from app.shots import build_shots
def analyze(video_path: str, output_dir: str | Path, config: AnalyzerConfig) -> tuple[list[Shot],list[Boundary]]:
    if config.seed is not None: random.seed(config.seed); np.random.seed(config.seed)
    meta=read_metadata(video_path); results={"omnishotcut":[],"transnet":[],"pyscenedetect":[]}; unavailable=[]
    detector_specs=[("omnishotcut",config.detectors.omnishotcut,OmniShotCutDetector(meta.fps,config.omnishotcut_command,config.device)),("transnet",config.detectors.transnet,TransNetDetector(meta.fps,config.transnet_command,config.device)),("pyscenedetect",config.detectors.pyscenedetect,PySceneDetectDetector(meta.fps))]
    for name,enabled,detector in detector_specs:
        if not enabled: continue
        try: results[name]=detector.detect(video_path)
        except (ModelUnavailableError,RuntimeError) as exc: unavailable.append(str(exc))
    if config.detectors.omnishotcut and not results["omnishotcut"]:
        raise RuntimeError("Primary OmniShotCut produced no usable boundaries. " + " ".join(unavailable))
    boundaries=BoundaryEnsemble(config.boundary_tolerance_frames).merge(**{f"{k}_boundaries":v for k,v in results.items()})
    classifier=TransitionClassifier(); transitions={}
    with FrameReader(video_path) as reader:
        for boundary in boundaries:
            frames=reader.window(boundary.frame,config.transition_window_frames); pivot=min(config.transition_window_frames,len(frames)//2); transitions[boundary.frame]=classifier.classify(frames[:pivot],frames[pivot:pivot+1],frames[pivot+1:])
    shots=build_shots(meta.frame_count,meta.fps,boundaries,transitions); out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    write_outputs(out,video_path,meta,shots,boundaries,{"omnishotcut":"v1.5 local adapter","transnet":"v2 local adapter","pyscenedetect":"installed optional"}); write_shots_csv(out,shots)
    if config.extract_boundary_frames:
        records=extract_boundary_frames(video_path,boundaries,out/"boundary_frames"); extract_shot_endpoint_frames(video_path,shots,out/"shot_frames")
        if config.generate_contact_sheet: create_contact_sheet(records,out/"boundaries.jpg")
    if config.generate_timeline: create_timeline(out/"timeline.png",meta.duration_seconds,boundaries,{f:t.transition_type for f,t in transitions.items()})
    return shots,boundaries
