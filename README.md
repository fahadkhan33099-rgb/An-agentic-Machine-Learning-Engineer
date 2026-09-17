# Free Local Video Shot & Transition Analyzer

A modular Python 3.10+ application for local video shot analysis. It writes zero-based, exact frame boundaries; shot ranges; detector evidence; JSON/CSV; full-resolution boundary frames; a timeline; and a boundary contact sheet. It does **not** call OpenAI, Gemini, Twelve Labs, or any paid cloud video API.

## Install

Install FFmpeg/FFprobe (on Ubuntu: `sudo apt install ffmpeg`), then create an environment:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Install PyTorch appropriate for the local CPU/CUDA platform from [pytorch.org](https://pytorch.org/get-started/locally/). Install OmniShotCut v1.5 locally and configure its command as described in [`models/README.md`](models/README.md). The application intentionally fails with an actionable message if its configured primary detector is absent; it never silently replaces it with frame differencing or an inferior detector.

## Usage

```bash
python -m app.cli analyze input.mp4 \
  --output ./output \
  --device auto \
  --omnishotcut-command 'python /opt/omnishotcut/run.py --input {video} --json-stdout' \
  --verify --extract-frames --timeline --seed 7
```

`--verify` enables optional TransNet V2 (configure with `--transnet-command`) and PySceneDetect. Detector adapters receive and return a normalized `Boundary`; model-specific JSON parsing stays in the adapter. The ensemble clusters candidates within `--boundary-tolerance` (default ±2 frames), preserves agreement, and reports a heuristic agreement score—not a calibrated probability.

## Frame semantics and outputs

All frame numbers are **zero-based**. A boundary at frame `N` means the first frame of the next shot: its extracted pair is `N - 1` (`before`) and `N` (`after`). This keeps exact decoded frame identity instead of converting timestamps back to frames, which is ambiguous for variable-frame-rate sources.

Outputs in `--output` are:

- `shots.json`, `shots.csv`, and `boundaries.json` (including model/version/evidence data)
- `boundary_frames/boundary_###_before.jpg` and `_after.jpg`
- `shot_frames/shot_###_start.jpg` and `_end.jpg`
- `timeline.png` and `boundaries.jpg`

## Transition classification and limits

Classification analyzes a temporal window (default 15 frames) using luminance, spatial mixture, and temporal progression. It conservatively emits `CUT`, `FADE` (`Fade Black`/`Fade White`), `DISSOLVE`, `WIPE` (direction only when supported), or `UNKNOWN`. Fade detection requires both an extreme uniform region and surrounding luminance change to reduce dark/bright-scene false positives. Cut subtype mapping is modular in `app/classifiers/cut_subtype.py`; without supported MovieCuts evidence, the app does not fabricate cinematic labels.

Camera pans, zooms, dolly/handheld movement, and subject motion are not primary detection signals: boundaries come from the model detectors and verification ensemble, never simple frame-difference thresholding. Results remain dependent on local model quality and should be reviewed with the contact sheet.
