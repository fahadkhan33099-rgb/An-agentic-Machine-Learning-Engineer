from __future__ import annotations
import shutil
import subprocess
from pathlib import Path
import cv2
from app.models import VideoMetadata

class VideoMetadataError(RuntimeError): pass

def read_metadata(video_path: str | Path) -> VideoMetadata:
    path = Path(video_path)
    if not path.is_file(): raise VideoMetadataError(f"Video does not exist: {path}")
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened(): raise VideoMetadataError(f"OpenCV could not open video: {path}. Check codec or corruption.")
    try:
        fps, count = float(cap.get(cv2.CAP_PROP_FPS)), int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    finally: cap.release()
    if fps <= 0 or count < 0 or width <= 0 or height <= 0: raise VideoMetadataError(f"Invalid metadata in {path}.")
    return VideoMetadata(fps=fps, frame_count=count, duration_seconds=count/fps, width=width, height=height, codec=_codec(path))

def _codec(path: Path) -> str | None:
    if not shutil.which("ffprobe"): return None
    run = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True)
    return run.stdout.strip() or None
