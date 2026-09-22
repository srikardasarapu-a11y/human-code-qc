import pytest
import os
import tempfile
from src.human_code_qc.normalization import normalize, NormalizationMode, NORMALIZATION_VERSION
from src.human_code_qc.hashing import hash_text, hash_bytes
from src.human_code_qc.models import ManifestEntry, AuditStatus
from src.human_code_qc.manifests.builder import ManifestBuilder

def test_newline_normalization():
    # 7. Newline normalization
    data = b"line1\r\nline2\r\nline3"
    result = normalize(data, NormalizationMode.LINE_ENDING_NORMALIZED)
    assert result == "line1\nline2\nline3"

def test_whitespace_normalization():
    # 8. Whitespace normalization
    data = b"def foo():  \r\n    return 1 \t \n"
    result = normalize(data, NormalizationMode.WHITESPACE_NORMALIZED)
    assert result == "def foo():\n    return 1\n"

def test_normalization_versioning():
    # 9. Normalization versioning
    assert NORMALIZATION_VERSION == "1.0"

def test_invalid_utf8():
    # 10. Invalid UTF-8
    # 11. Raw hash available when normalized hash is unavailable
    invalid_data = b"\x80\x81\x82"
    # Raw hash succeeds
    raw_hash = hash_bytes(invalid_data)
    assert raw_hash is not None
    
    # Normalized is unavailable
    result = normalize(invalid_data, NormalizationMode.LINE_ENDING_NORMALIZED)
    assert result is None

def test_manifest_serialization():
    # 14. Manifest serialization
    entry = ManifestEntry(
        solution_id="sol_1",
        problem_id="prob_1",
        original_code_path="code.py",
        original_metadata_path="meta.json",
        archive_sha256="a"*64,
        original_code_sha256="b"*64,
        original_metadata_sha256="c"*64,
        raw_code_hash="d"*64,
        normalized_code_hash="e"*64,
        normalization_method="WHITESPACE_NORMALIZED",
        normalization_version="1.0",
        audit_status=AuditStatus.CLEAN,
        pipeline_version="1.0",
        schema_version="1.0",
        config_hash="f"*64
    )
    
    with tempfile.NamedTemporaryFile(delete=False) as f:
        path = f.name
        
    try:
        builder = ManifestBuilder(path, NormalizationMode.RAW)
        builder.serialize_manifest([entry], path)
        assert os.path.exists(path)
        with open(path, "r") as f2:
            content = f2.read()
            assert "sol_1" in content
            assert "WHITESPACE_NORMALIZED" in content
    finally:
        os.remove(path)

def test_reproducibility():
    # 15. Reproducibility
    data = b"int main() { return 0; }"
    h1 = hash_bytes(data)
    h2 = hash_bytes(data)
    assert h1 == h2
    
    n1 = normalize(data, NormalizationMode.LINE_ENDING_NORMALIZED)
    n2 = normalize(data, NormalizationMode.LINE_ENDING_NORMALIZED)
    assert n1 == n2
