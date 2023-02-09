import os
from pathlib import Path
from xml.dom import ValidationErr
import pytest 
from models import FileImportModel

@pytest.fixture(
    params=[
        os.path.sep.join([p, file_name])
        for p, m, files in os.walk(os.path.dirname('examples/'))
        for file_name in files
        if file_name.casefold().endswith('.json')
    ]
)
def json_config_file(request: pytest.FixtureRequest) -> Path:
    assert isinstance(request.param, str), 'fixture param is not a string'
    path = Path(request.param)
    assert path.is_file(), f'param is not a file {path}'
    return path


def test_all_example_json_files(json_config_file: Path) -> None:
    FileImportModel.parse_file(json_config_file)
