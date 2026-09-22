import argparse
import json
import os
import sys

from src.human_code_qc.discovery import run_discovery
from src.human_code_qc.hashing import hash_file
from src.human_code_qc.manifests.verifier import verify_archive_integrity, IntegrityError

def write_markdown_report(report, path: str):
    md = [
        "# Dataset Discovery Report\n",
        "## Summary",
        f"- **Total Archive Entries:** {report.total_entries}",
        f"- **Directories:** {report.directories}",
        f"- **Code Files:** {report.code_files}",
        f"- **Metadata Files:** {report.metadata_files}",
        f"- **Other Files:** {report.other_files}",
        f"- **Valid Pairs:** {report.valid_pairs}",
        f"- **Orphan Code:** {report.orphan_code}",
        f"- **Orphan Metadata:** {report.orphan_metadata}",
        f"- **Unique Solution IDs:** {report.unique_solution_ids}",
        f"- **Unique Problem IDs:** {report.unique_problem_ids}\n",
        "## Files by Extension"
    ]
    for ext, count in sorted(report.files_by_extension.items()):
        md.append(f"- `{ext}`: {count}")
        
    md.append("\n## Solutions by Language")
    for lang, count in sorted(report.solutions_per_language.items()):
        md.append(f"- **{lang}**: {count}")
        
    md.append("\n## Schema Fingerprints")
    for fp, count in sorted(report.schema_fingerprints.items()):
        md.append(f"- `{fp}`: {count}")
        
    if report.unexpected_paths:
        md.append("\n## Unexpected Paths (Errors)")
        for err in report.unexpected_paths[:20]:
            md.append(f"- {err}")
        if len(report.unexpected_paths) > 20:
            md.append(f"- ... and {len(report.unexpected_paths) - 20} more.")
            
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

def main():
    parser = argparse.ArgumentParser(description="QC Dataset Discovery")
    parser.add_argument("--dataset", required=True, help="Path to original dataset ZIP")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of output records")
    parser.add_argument("--language", help="Filter by language (ignored in this read-only full-sweep script)")
    parser.add_argument("--problem-id", help="Filter by problem-id (ignored in this read-only full-sweep script)")
    parser.add_argument("--workers", type=int, default=1, help="Number of workers (ignored for zip streaming)")
    parser.add_argument("--output", default="audit/", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Perform discovery without writing outputs")
    
    args = parser.parse_args()
    
    print(f"Starting discovery on {args.dataset}")
    baseline = hash_file(args.dataset)
    print(f"Pre-execution Baseline Hash: {baseline}")
    
    records, report = run_discovery(args.dataset, limit=args.limit)
    
    post_hash = hash_file(args.dataset)
    print(f"Post-execution Hash: {post_hash}")
    
    if baseline != post_hash:
        print("ERROR: ORIGINAL_DATASET_INTEGRITY_FAILURE")
        sys.exit(1)
        
    print("Integrity check passed.")
    
    if not args.dry_run:
        os.makedirs(args.output, exist_ok=True)
        jsonl_path = os.path.join(args.output, "discovery_records.jsonl")
        json_path = os.path.join(args.output, "discovery_report.json")
        md_path = os.path.join(args.output, "discovery_report.md")
        
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for rec in records:
                f.write(rec.model_dump_json() + "\n")
                
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json.loads(report.model_dump_json()), f, indent=2, sort_keys=True)
            
        write_markdown_report(report, md_path)
        print(f"Outputs written to {args.output}")

if __name__ == "__main__":
    main()
