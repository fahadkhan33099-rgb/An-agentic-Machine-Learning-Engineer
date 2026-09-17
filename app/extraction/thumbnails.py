from __future__ import annotations
from pathlib import Path
import cv2, numpy as np
def create_contact_sheet(records: list[dict], output_path: str | Path) -> None:
    tiles=[]
    for record in records:
        images=[]
        for key in ("before","after"):
            image=cv2.imread(record.get(key,"")) if record.get(key) else None
            if image is None: image=np.zeros((180,320,3),np.uint8)
            image=cv2.resize(image,(320,180)); cv2.putText(image,f"{key}: frame {record['frame'] - (key=='before')}",(8,170),cv2.FONT_HERSHEY_SIMPLEX,.45,(255,255,255),1); images.append(image)
        tiles.append(np.hstack(images))
    sheet=np.vstack(tiles) if tiles else np.zeros((180,640,3),np.uint8)
    cv2.imwrite(str(output_path),sheet)
