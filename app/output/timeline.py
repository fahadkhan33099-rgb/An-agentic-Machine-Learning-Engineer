from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
from app.models import Boundary
def create_timeline(output_path: str | Path, duration: float, boundaries: list[Boundary], labels: dict[int,str]) -> None:
    fig,ax=plt.subplots(figsize=(12,2.8)); ax.hlines(0,0,max(duration,.1),color="black")
    for i,b in enumerate(boundaries):
        ax.vlines(b.timestamp,0,.55,color="#d62728"); ax.text(b.timestamp,.65+(i%2)*.22,f"{labels.get(b.frame,'UNKNOWN')}\nF{b.frame} · {b.timestamp:.2f}s",ha="center",fontsize=7,rotation=25)
    ax.set(xlim=(0,max(duration,.1)),ylim=(-.2,1.35),yticks=[],xlabel="Time (seconds)"); ax.spines[["left","right","top"]].set_visible(False); fig.tight_layout(); fig.savefig(output_path,dpi=160); plt.close(fig)
