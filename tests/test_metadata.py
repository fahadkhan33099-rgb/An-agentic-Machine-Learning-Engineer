import pytest
cv2 = pytest.importorskip("cv2")
import numpy as np
from app.video.metadata import read_metadata
def test_metadata_duration_and_dimensions(tmp_path):
    path=tmp_path/'tiny.avi'; writer=cv2.VideoWriter(str(path),cv2.VideoWriter_fourcc(*'MJPG'),10,(16,8))
    for _ in range(5): writer.write(np.zeros((8,16,3),np.uint8))
    writer.release(); meta=read_metadata(path)
    assert (meta.frame_count,meta.width,meta.height)==(5,16,8)
    assert meta.duration_seconds==.5
