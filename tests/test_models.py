import pytest
from pydantic import ValidationError
from src.human_code_qc.models import (
    AuditIssue, IssueCode, Severity, EvidenceType, 
    SolutionRecord, AuditResult, AuditStatus, RepairJob, RepairClass, RepairStatus
)

def test_audit_issue_valid():
    issue = AuditIssue(
        issue_code=IssueCode.CODE_FILE_MISSING,
        severity=Severity.CRITICAL,
        reason="File not found in archive",
        confidence=1.0,
        evidence_type=EvidenceType.STATIC_ANALYSIS,
        evidence="{}",
        validator="structure.py",
        validator_version="1.0.0",
        created_at="2026-09-22T00:00:00Z"
    )
    assert issue.issue_code == IssueCode.CODE_FILE_MISSING

def test_audit_issue_invalid_confidence():
    with pytest.raises(ValidationError):
        AuditIssue(
            issue_code=IssueCode.CODE_FILE_MISSING,
            severity=Severity.CRITICAL,
            reason="Bad confidence",
            confidence=1.5,  # Out of range!
            evidence_type=EvidenceType.STATIC_ANALYSIS,
            evidence="{}",
            validator="structure.py",
            validator_version="1.0.0",
            created_at="2026-09-22"
        )

def test_legacy_solution_record_conversion():
    legacy_data = {
        "solutionId": "SOL_123",
        "problemId": "PROB_123",
        "language": "Python",
        "problem": {"problemId": "PROB_123", "title": "Test"}
    }
    record = SolutionRecord.from_legacy_dict(legacy_data)
    assert record.solutionId == "SOL_123"
    assert record.language == "Python"
    assert record.problem.title == "Test"
    assert record.repository is None

def test_repair_job_hash_validation():
    # Valid hash length 64 hex
    valid_hash = "a" * 64
    job = RepairJob(
        job_id="job_1",
        solution_id="sol_1",
        problem_id="prob_1",
        original_code_path="path/to/code",
        original_metadata_path="path/to/meta",
        original_code_sha256=valid_hash,
        original_metadata_sha256=valid_hash,
        recommended_action="none",
        repair_class=RepairClass.SAFE_DETERMINISTIC_REPAIR,
        repair_allowed=True,
        verification_required=True,
        status=RepairStatus.PENDING,
        pipeline_version="1.0",
        created_at="now"
    )
    assert job.original_code_sha256 == valid_hash
    
    with pytest.raises(ValidationError):
        # Invalid hash length
        invalid_hash = "a" * 63
        RepairJob(
            job_id="job_1",
            solution_id="sol_1",
            problem_id="prob_1",
            original_code_path="path/to/code",
            original_metadata_path="path/to/meta",
            original_code_sha256=invalid_hash,
            original_metadata_sha256=valid_hash,
            recommended_action="none",
            repair_class=RepairClass.SAFE_DETERMINISTIC_REPAIR,
            repair_allowed=True,
            verification_required=True,
            status=RepairStatus.PENDING,
            pipeline_version="1.0",
            created_at="now"
        )
