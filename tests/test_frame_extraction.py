import pytest
cv2 = pytest.importorskip("cv2")
import numpy as np
from app.models import Boundary
from app.extraction.boundary_frames import extract_boundary_frames
def test_beginning_boundary_is_safe(tmp_path):
    path=tmp_path/'v.avi'; out=tmp_path/'out'; w=cv2.VideoWriter(str(path),cv2.VideoWriter_fourcc(*'MJPG'),5,(8,8)); w.write(np.zeros((8,8,3),np.uint8)); w.release()
    rows=extract_boundary_frames(str(path),[Boundary(0,0,'x')],out)
    assert 'before' not in rows[0] and 'after' in rows[0]
