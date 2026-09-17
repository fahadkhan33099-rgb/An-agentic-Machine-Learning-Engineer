from __future__ import annotations
import argparse, sys
from app.config import AnalyzerConfig, DetectorConfig

def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description="Analyze local video shot boundaries without cloud APIs.")
    sub=parser.add_subparsers(dest="command",required=True); command=sub.add_parser("analyze")
    command.add_argument("video"); command.add_argument("--output",default="output"); command.add_argument("--device",default="auto",choices=["auto","cpu","cuda"]); command.add_argument("--verify",action="store_true",help="Enable TransNet V2 and PySceneDetect verification.")
    command.add_argument("--extract-frames",action=argparse.BooleanOptionalAction,default=True); command.add_argument("--timeline",action=argparse.BooleanOptionalAction,default=True); command.add_argument("--contact-sheet",action=argparse.BooleanOptionalAction,default=True); command.add_argument("--boundary-tolerance",type=int,default=2); command.add_argument("--transition-window",type=int,default=15); command.add_argument("--seed",type=int); command.add_argument("--omnishotcut-command"); command.add_argument("--transnet-command")
    args=parser.parse_args(argv)
    try:
        from app.pipeline import analyze
        from app.video.metadata import read_metadata
        meta=read_metadata(args.video); print(f"Loading video...\nFPS: {meta.fps:g}\nFrames: {meta.frame_count}\nDuration: {meta.duration_seconds:.2f}s")
        config=AnalyzerConfig(device=args.device,detectors=DetectorConfig(omnishotcut=True,transnet=args.verify,pyscenedetect=args.verify),boundary_tolerance_frames=args.boundary_tolerance,transition_window_frames=args.transition_window,extract_boundary_frames=args.extract_frames,generate_timeline=args.timeline,generate_contact_sheet=args.contact_sheet,seed=args.seed,omnishotcut_command=args.omnishotcut_command,transnet_command=args.transnet_command)
        shots,boundaries=analyze(args.video,args.output,config); print(f"Final boundaries: {len(boundaries)}\nWriting: {args.output}/shots.json, shots.csv, boundaries.json\nDone.")
    except Exception as exc: print(f"ERROR: {exc}",file=sys.stderr); return 2
    return 0
if __name__ == "__main__": raise SystemExit(main())
