from enum import Enum
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class Language(str, Enum):
    C = "C"
    CPP = "C++"
    JAVA = "Java"
    JAVASCRIPT = "JavaScript"
    PYTHON = "Python"

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class IssueCode(str, Enum):
    CODE_FILE_MISSING = "CODE_FILE_MISSING"
    METADATA_FILE_MISSING = "METADATA_FILE_MISSING"
    ORPHAN_CODE_FILE = "ORPHAN_CODE_FILE"
    ORPHAN_METADATA_FILE = "ORPHAN_METADATA_FILE"
    UNEXPECTED_EXTENSION = "UNEXPECTED_EXTENSION"
    UNEXPECTED_PATH = "UNEXPECTED_PATH"
    ENCODING_INVALID = "ENCODING_INVALID"
    BINARY_CONTENT = "BINARY_CONTENT"
    CODE_EMPTY = "CODE_EMPTY"
    CODE_TOO_SMALL = "CODE_TOO_SMALL"
    CODE_SUSPICIOUS_SIZE = "CODE_SUSPICIOUS_SIZE"
    CODE_TRUNCATED = "CODE_TRUNCATED"
    CODE_SYNTAX_INVALID = "CODE_SYNTAX_INVALID"
    CODE_LANGUAGE_MISMATCH = "CODE_LANGUAGE_MISMATCH"
    CODE_COMPILATION_FAILED = "CODE_COMPILATION_FAILED"
    METADATA_MISSING = "METADATA_MISSING"
    METADATA_INVALID = "METADATA_INVALID"
    METADATA_INCONSISTENT = "METADATA_INCONSISTENT"
    METADATA_SCHEMA_INVALID = "METADATA_SCHEMA_INVALID"
    SOURCE_MISSING = "SOURCE_MISSING"
    SOURCE_URL_MALFORMED = "SOURCE_URL_MALFORMED"
    SOURCE_REPOSITORY_MISMATCH = "SOURCE_REPOSITORY_MISMATCH"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    SOURCE_FILE_NOT_FOUND = "SOURCE_FILE_NOT_FOUND"
    SOURCE_CONTENT_MISMATCH = "SOURCE_CONTENT_MISMATCH"
    SOURCE_CHANGED = "SOURCE_CHANGED"
    LICENSE_MISSING = "LICENSE_MISSING"
    LICENSE_UNVERIFIED = "LICENSE_UNVERIFIED"
    LICENSE_UNKNOWN = "LICENSE_UNKNOWN"
    LICENSE_CONFLICT = "LICENSE_CONFLICT"
    PROVENANCE_MISSING = "PROVENANCE_MISSING"
    PROVENANCE_INCOMPLETE = "PROVENANCE_INCOMPLETE"
    AUTHOR_MISSING = "AUTHOR_MISSING"
    AUTHOR_UNVERIFIED = "AUTHOR_UNVERIFIED"
    COMMIT_METADATA_MISSING = "COMMIT_METADATA_MISSING"
    DATE_METADATA_MISSING = "DATE_METADATA_MISSING"
    DUPLICATE_EXACT = "DUPLICATE_EXACT"
    DUPLICATE_NORMALIZED = "DUPLICATE_NORMALIZED"
    DUPLICATE_NEAR = "DUPLICATE_NEAR"
    PROBLEM_SOLUTION_MISMATCH = "PROBLEM_SOLUTION_MISMATCH"
    PROBLEM_MATCH_UNCERTAIN = "PROBLEM_MATCH_UNCERTAIN"
    SOURCE_PROBLEM_MISMATCH = "SOURCE_PROBLEM_MISMATCH"
    GENERATED_MARKER_FOUND = "GENERATED_MARKER_FOUND"
    GENERATED_CODE_SUSPECTED = "GENERATED_CODE_SUSPECTED"

class AuditStatus(str, Enum):
    CLEAN = "CLEAN"
    ISSUES_FOUND = "ISSUES_FOUND"

class RepairClass(str, Enum):
    SAFE_DETERMINISTIC_REPAIR = "SAFE_DETERMINISTIC_REPAIR"
    LLM_ASSISTED_REPAIR = "LLM_ASSISTED_REPAIR"
    SOURCE_REFETCH_REQUIRED = "SOURCE_REFETCH_REQUIRED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    DO_NOT_REPAIR = "DO_NOT_REPAIR"

class RepairStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    PENDING = "PENDING"

class VerificationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_AVAILABLE = "NOT_AVAILABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNCERTAIN = "UNCERTAIN"

class DecisionStatus(str, Enum):
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    UNCERTAIN = "UNCERTAIN"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    NOT_VERIFIED = "NOT_VERIFIED"

class EvidenceType(str, Enum):
    STATIC_ANALYSIS = "STATIC_ANALYSIS"
    NETWORK_FETCH = "NETWORK_FETCH"
    HEURISTIC = "HEURISTIC"
    LLM = "LLM"
    COMPILER = "COMPILER"
    NONE = "NONE"

class ProvenanceStatus(str, Enum):
    VERIFIED = "VERIFIED"
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"

class LicenseStatus(str, Enum):
    VERIFIED = "VERIFIED"
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"
    
class MatchStatus(str, Enum):
    MATCH_CONFIRMED = "MATCH_CONFIRMED"
    MATCH_LIKELY = "MATCH_LIKELY"
    MATCH_UNCERTAIN = "MATCH_UNCERTAIN"
    MATCH_FAILED = "MATCH_FAILED"

class SourceStatus(str, Enum):
    URL_FORMAT_VALID = "URL_FORMAT_VALID"
    URL_ACCESSIBLE = "URL_ACCESSIBLE"
    REPOSITORY_EXISTS = "REPOSITORY_EXISTS"
    SOURCE_FILE_EXISTS = "SOURCE_FILE_EXISTS"
    SOURCE_CONTENT_MATCH = "SOURCE_CONTENT_MATCH"
    SOURCE_CURRENT = "SOURCE_CURRENT"

# ---------------------------------------------------------
# Metadata Models
# ---------------------------------------------------------

class ProblemRecord(BaseModel):
    problemId: str
    title: Optional[str] = None
    problemStatement: Optional[str] = None

class RepositoryRecord(BaseModel):
    url: Optional[str] = None
    owner: Optional[str] = None
    name: Optional[str] = None

class SourceRecord(BaseModel):
    url: Optional[str] = None
    path: Optional[str] = None

class LicenseRecord(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None

class ProvenanceRecord(BaseModel):
    author: Optional[str] = None
    commit_sha: Optional[str] = None
    date: Optional[str] = None

class DeduplicationRecord(BaseModel):
    is_duplicate: bool = False
    duplicate_of: Optional[str] = None

class ValidationRecord(BaseModel):
    syntaxValid: bool = True
    utf8Valid: bool = True

class CollectionRecord(BaseModel):
    collected_at: Optional[str] = None

class MatchingRecord(BaseModel):
    match_status: Optional[MatchStatus] = None

class SolutionRecord(BaseModel):
    solutionId: str
    problemId: str
    language: Optional[Language] = None
    label: Optional[str] = None
    problem: Optional[ProblemRecord] = None
    repository: Optional[RepositoryRecord] = None
    source: Optional[SourceRecord] = None
    matching: Optional[MatchingRecord] = None
    provenance: Optional[ProvenanceRecord] = None
    deduplication: Optional[DeduplicationRecord] = None
    validation: Optional[ValidationRecord] = None
    collection: Optional[CollectionRecord] = None

    @classmethod
    def from_legacy_dict(cls, data: Dict[str, Any]) -> "SolutionRecord":
        """Converts arbitrary legacy metadata dicts into the typed SolutionRecord."""
        # Provides safe fallbacks for missing keys.
        return cls(
            solutionId=data.get("solutionId", "UNKNOWN"),
            problemId=data.get("problemId", "UNKNOWN"),
            language=data.get("language"),
            label=data.get("label"),
            problem=ProblemRecord(**data.get("problem", {})) if data.get("problem") else None,
            repository=RepositoryRecord(**data.get("repository", {})) if data.get("repository") else None,
            source=SourceRecord(**data.get("source", {})) if data.get("source") else None,
            matching=MatchingRecord(**data.get("matching", {})) if data.get("matching") else None,
            provenance=ProvenanceRecord(**data.get("provenance", {})) if data.get("provenance") else None,
            deduplication=DeduplicationRecord(**data.get("deduplication", {})) if data.get("deduplication") else None,
            validation=ValidationRecord(**data.get("validation", {})) if data.get("validation") else None,
            collection=CollectionRecord(**data.get("collection", {})) if data.get("collection") else None,
        )

# ---------------------------------------------------------
# Audit Models
# ---------------------------------------------------------

class AuditIssue(BaseModel):
    issue_code: IssueCode
    severity: Severity
    reason: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence_type: EvidenceType
    evidence: str
    validator: str
    validator_version: str
    created_at: str

class AuditResult(BaseModel):
    run_id: str
    solution_id: str
    problem_id: str
    language: Optional[Language] = None
    issues: List[AuditIssue] = Field(default_factory=list)
    status: AuditStatus
    started_at: str
    completed_at: str
    pipeline_version: str
    config_version: str

# ---------------------------------------------------------
# Repair Models
# ---------------------------------------------------------

class RepairJob(BaseModel):
    job_id: str
    solution_id: str
    problem_id: str
    language: Optional[Language] = None
    
    original_code_path: str
    original_metadata_path: str
    original_code_sha256: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")
    original_metadata_sha256: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")
    
    issues: List[AuditIssue] = Field(default_factory=list)
    recommended_action: str
    
    repair_class: RepairClass
    repair_allowed: bool
    verification_required: bool
    
    status: RepairStatus
    pipeline_version: str
    created_at: str

class RepairCandidate(BaseModel):
    candidate_code: str
    confidence: float = Field(..., ge=0.0, le=1.0)

class RepairResult(BaseModel):
    job_id: str
    repair_status: RepairStatus
    repair_type: RepairClass
    original_hash: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")
    repaired_hash: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")
    changes: str
    warnings: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)

class ModelRun(BaseModel):
    gateway: str
    provider: str
    model_alias: str
    resolved_model: str
    prompt_version: str
    
    input_hash: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")
    output_hash: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")
    
    request_id: str
    timestamp: str
    latency_ms: int
    
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
    retry_count: int
    status: str

# ---------------------------------------------------------
# Verification Models
# ---------------------------------------------------------

class VerificationResult(BaseModel):
    integrity: VerificationStatus = VerificationStatus.NOT_APPLICABLE
    encoding: VerificationStatus = VerificationStatus.NOT_APPLICABLE
    language: VerificationStatus = VerificationStatus.NOT_APPLICABLE
    syntax: VerificationStatus = VerificationStatus.NOT_APPLICABLE
    compilation: VerificationStatus = VerificationStatus.NOT_APPLICABLE
    execution: VerificationStatus = VerificationStatus.NOT_APPLICABLE
    problem_matching: VerificationStatus = VerificationStatus.NOT_APPLICABLE
    metadata: VerificationStatus = VerificationStatus.NOT_APPLICABLE
    provenance: VerificationStatus = VerificationStatus.NOT_APPLICABLE
    diff: VerificationStatus = VerificationStatus.NOT_APPLICABLE
    
    overall_decision: DecisionStatus

class DecisionRecord(BaseModel):
    solution_id: str
    verification_result: VerificationResult
    timestamp: str

# ---------------------------------------------------------
# Manifest Models
# ---------------------------------------------------------

class ManifestEntry(BaseModel):
    solution_id: str
    problem_id: str
    language: Optional[Language] = None
    
    original_code_path: str
    original_metadata_path: str
    archive_sha256: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")
    original_code_sha256: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")
    original_metadata_sha256: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")
    raw_code_hash: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")
    normalized_code_hash: Optional[str] = None
    normalization_method: str
    normalization_version: str
    
    repository: Optional[str] = None
    source_url: Optional[str] = None
    source_path: Optional[str] = None
    
    license: Optional[LicenseStatus] = None
    provenance_status: Optional[ProvenanceStatus] = None
    
    audit_status: AuditStatus
    repair_status: Optional[RepairStatus] = None
    verification_status: Optional[DecisionStatus] = None
    
    pipeline_version: str
    schema_version: str
    config_hash: str
