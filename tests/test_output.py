import json
from app.models import VideoMetadata, Shot, Boundary
from app.output.json_writer import write_outputs
from app.output.csv_writer import write_shots_csv
def test_json_schema_and_csv(tmp_path):
    shot=Shot(1,0,2,0,.2,None,None,None,())
    write_outputs(tmp_path,'x.mp4',VideoMetadata(10,3,.3,4,4),[shot],[Boundary(1,.1,'x')],{})
    write_shots_csv(tmp_path,[shot]); data=json.loads((tmp_path/'shots.json').read_text())
    assert data['shots'][0]['start_frame']==0 and (tmp_path/'shots.csv').read_text().startswith('shot_id,')
