import argparse
import sys
import os
from .discovery import DatasetReader
from .audit import QCPipeline
from .llm.client import LLMRepairEngine

def main():
    parser = argparse.ArgumentParser(description="Human Code Quality Control Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Run the pipeline without making any actual repairs or file changes.", default=False)
    parser.add_argument("--limit", type=int, default=10, help="Limit the number of files to process for testing.")
    args = parser.parse_args()

    print(f"Starting Human Code QC Pipeline (Phase 2) - Dry Run: {args.dry_run}")
    
    try:
        reader = DatasetReader()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
        
    qc = QCPipeline()
    repair = LLMRepairEngine(enable_repair=not args.dry_run)
    
    processed = 0
    issues_found = 0
    
    output_dir = "repaired/llm_assisted"
    if not args.dry_run:
        os.makedirs(output_dir, exist_ok=True)
    
    for prefix, py_content, meta_content in reader.iter_dataset():
        if processed >= args.limit:
            break
            
        print(f"\nProcessing: {prefix}")
        results = qc.run_checks(py_content, meta_content)
        
        if results["needs_repair"]:
            issues_found += 1
            print(f"  [!] Issues found: {', '.join(results['issues'])}")
            
            repaired_code, was_repaired = repair.attempt_repair(py_content, meta_content, results["issues"])
            
            if was_repaired:
                print("  [+] Code repaired by LLM.")
                if not args.dry_run:
                    filename = os.path.basename(prefix) + ".py"
                    output_path = os.path.join(output_dir, filename)
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(repaired_code)
                    print(f"  [+] Saved repaired code to {output_path}")
        else:
            print("  [+] QC Passed.")
            
        processed += 1
        
    print(f"\nPipeline finished. Processed: {processed}, Issues found: {issues_found}")

if __name__ == "__main__":
    main()
