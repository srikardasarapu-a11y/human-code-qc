import os
import json
from src.human_code_qc.models import AuditIssue, AuditResult, RepairJob, RepairResult, VerificationResult, ManifestEntry

def generate_schemas():
    schema_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "schemas"))
    os.makedirs(schema_dir, exist_ok=True)
    
    mapping = {
        "audit_issue.schema.json": AuditIssue,
        "audit_result.schema.json": AuditResult,
        "repair_job.schema.json": RepairJob,
        "repair_result.schema.json": RepairResult,
        "verification_result.schema.json": VerificationResult,
        "manifest.schema.json": ManifestEntry
    }
    
    for filename, model in mapping.items():
        schema_path = os.path.join(schema_dir, filename)
        with open(schema_path, "w", encoding="utf-8") as f:
            json.dump(model.model_json_schema(), f, indent=2)
            
    print(f"Generated {len(mapping)} schemas to {schema_dir}")

if __name__ == "__main__":
    generate_schemas()
