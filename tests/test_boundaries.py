from app.detectors.ensemble import BoundaryEnsemble
from app.models import Boundary
from app.shots import build_shots

def b(frame, source): return Boundary(frame, frame/25, source, .8)
def test_clusters_duplicates_and_preserves_sources():
    merged=BoundaryEnsemble(2).merge([b(100,"omnishotcut")],[b(102,"transnet")],[b(101,"pyscenedetect")])
    assert len(merged)==1 and merged[0].frame==100 and set(merged[0].detectors)=={"omnishotcut","transnet","pyscenedetect"}
def test_build_shots_is_zero_based_and_inclusive():
    boundary=Boundary(3,.12,"ensemble",.9,("omnishotcut",))
    shots=build_shots(8,25,[boundary],{})
    assert [(s.start_frame,s.end_frame) for s in shots]==[(0,2),(3,7)]
