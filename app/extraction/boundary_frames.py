from __future__ import annotations
from pathlib import Path
from app.video.frames import FrameReader, write_jpeg
from app.models import Boundary, Shot
def extract_boundary_frames(video_path: str, boundaries: list[Boundary], output_dir: str | Path) -> list[dict]:
    out=Path(output_dir); records=[]
    with FrameReader(video_path) as reader:
        for number,boundary in enumerate(boundaries, 1):
            record={"boundary":number,"frame":boundary.frame}
            for label,index in (("before",boundary.frame-1),("after",boundary.frame)):
                frame=reader.get(index)
                if frame is not None:
                    path=out/f"boundary_{number:03d}_{label}.jpg"; write_jpeg(path,frame); record[label]=str(path)
            records.append(record)
    return records
def extract_shot_endpoint_frames(video_path: str, shots: list[Shot], output_dir: str | Path) -> None:
    with FrameReader(video_path) as reader:
        for shot in shots:
            for label,index in (("start",shot.start_frame),("end",shot.end_frame)):
                if (frame:=reader.get(index)) is not None: write_jpeg(Path(output_dir)/f"shot_{shot.shot_id:03d}_{label}.jpg",frame)
