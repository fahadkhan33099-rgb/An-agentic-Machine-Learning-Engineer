"""Utilities for generating deterministic regression clips when OpenCV is installed.

They cover hard cuts, fades, dissolves, wipes, and continuous pan/zoom clips. The
latter two have no true boundary and protect against adding frame-difference
based detectors to the primary path.
"""
from __future__ import annotations
import numpy as np

def solid(color, size=(64,96)): return np.full((*size,3),color,np.uint8)
def hard_cut(): return [solid((0,0,255))]*10 + [solid((255,0,0))]*10
def fade(to_white=False):
    end=255 if to_white else 0
    return [np.full((64,96,3),int(128+(end-128)*i/9),np.uint8) for i in range(10)]
def dissolve(): return [np.full((64,96,3),int(255*i/9),np.uint8) for i in range(10)]
def wipe():
    frames=[]
    for i in range(10):
        frame=solid((255,0,0)); frame[:,:int(96*i/9)]=((0,0,255)); frames.append(frame)
    return frames
def continuous_pan():
    image=np.tile(np.arange(160,dtype=np.uint8),(64,1)); return [np.dstack([image[:,i:i+96]]*3) for i in range(20)]
def continuous_zoom():
    image=np.tile(np.arange(96,dtype=np.uint8),(64,1)); return [np.dstack([image]*3) for _ in range(20)]
