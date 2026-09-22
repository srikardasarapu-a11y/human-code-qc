import argparse
import sys
from src.human_code_qc.manifests.builder import ManifestBuilder
from src.human_code_qc.normalization import NormalizationMode

def main():
    parser = argparse.ArgumentParser(description="Build QC dataset manifest without modification.")
    parser.add_argument("--dataset", required=True, help="Path to original dataset archive")
    parser.add_argument("--output", default="manifests/manifest.json", help="Output path for manifest JSON")
    
    args = parser.parse_args()
    
    print(f"Building manifest for {args.dataset}")
    builder = ManifestBuilder(args.dataset, NormalizationMode.LINE_ENDING_NORMALIZED)
    entries = builder.build_manifest()
    
    import os
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    builder.serialize_manifest(entries, args.output)
    
    print(f"Successfully generated deterministic manifest at {args.output}")

if __name__ == "__main__":
    main()
