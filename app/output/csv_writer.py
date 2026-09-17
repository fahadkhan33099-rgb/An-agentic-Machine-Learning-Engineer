from __future__ import annotations
import csv
from pathlib import Path
from app.models import Shot
def write_shots_csv(output_dir: str | Path, shots: list[Shot]) -> None:
    fields="shot_id start_frame end_frame start_time end_time duration transition subtype confidence detectors".split()
    with (Path(output_dir)/"shots.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader()
        for s in shots: writer.writerow({"shot_id":s.shot_id,"start_frame":s.start_frame,"end_frame":s.end_frame,"start_time":s.start_time,"end_time":s.end_time,"duration":s.end_time-s.start_time,"transition":s.transition_type,"subtype":s.transition_subtype,"confidence":s.confidence,"detectors":";".join(s.detectors)})
