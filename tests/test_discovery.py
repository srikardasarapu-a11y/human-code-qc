import pytest
import zipfile
import json
import os
from src.human_code_qc.discovery import DatasetReader

@pytest.fixture
def mock_dataset(tmp_path):
    zip_path = tmp_path / "mock.zip"
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr("test/P001/PY_001.py", "print('hello')")
        zf.writestr("test/P001/PY_001.meta.json", json.dumps({"test": "data"}))
    return zip_path

def test_dataset_reader_yields_pairs(mock_dataset):
    reader = DatasetReader(dataset_path=str(mock_dataset))
    entries = list(reader.iter_dataset())
    
    assert len(entries) == 1
    prefix, py_content, meta_content = entries[0]
    
    assert prefix == "test/P001/PY_001"
    assert "print('hello')" in py_content
    assert meta_content["test"] == "data"
