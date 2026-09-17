from __future__ import annotations
import json, shlex, subprocess
from pathlib import Path
from app.models import Boundary

class ModelUnavailableError(RuntimeError): pass

def run_json_detector(command: str | None, video_path: str, source: str, fps: float) -> list[Boundary]:
    """Run an installed local model adapter that emits JSON boundary records to stdout.

    Command may contain ``{video}`` and ``{device}`` placeholders. Accepted JSON is
    either a list or ``{"boundaries": [...]}``; items require ``frame`` and can
    optionally include ``confidence``. This deliberately keeps model parsing isolated.
    """
    if not command:
        raise ModelUnavailableError(f"{source} is enabled but no local adapter command is configured. See models/README.md.")
    args = [part.format(video=str(Path(video_path))) for part in shlex.split(command)]
    run = subprocess.run(args, text=True, capture_output=True)
    if run.returncode: raise ModelUnavailableError(f"{source} adapter failed ({run.returncode}): {run.stderr.strip()}")
    try: payload = json.loads(run.stdout); items = payload.get("boundaries", payload) if isinstance(payload, dict) else payload
    except json.JSONDecodeError as exc: raise ModelUnavailableError(f"{source} adapter did not emit JSON: {exc}") from exc
    result=[]
    for item in items:
        frame = int(item["frame"] if isinstance(item, dict) else item)
        confidence = item.get("confidence") if isinstance(item, dict) else None
        result.append(Boundary(frame, frame/fps, source, confidence, evidence={"adapter": source}))
    return result
