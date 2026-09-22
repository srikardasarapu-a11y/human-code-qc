import argparse
import sys
from src.human_code_qc.manifests.verifier import verify_archive_integrity, IntegrityError

def main():
    parser = argparse.ArgumentParser(description="Verify original dataset archive immutability.")
    parser.add_argument("--dataset", required=True, help="Path to original dataset archive")
    parser.add_argument("--baseline", required=True, help="Expected baseline SHA-256 hash")
    
    args = parser.parse_args()
    
    try:
        verify_archive_integrity(args.dataset, args.baseline)
        print("PASS: Dataset archive matches exact baseline hash.")
    except IntegrityError as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
