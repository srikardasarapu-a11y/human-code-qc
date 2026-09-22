# Legacy main entrypoint
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print("Legacy entrypoint.")

if __name__ == "__main__":
    main()
