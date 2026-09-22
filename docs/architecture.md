# Architecture

The pipeline consists of a deterministic auditor and an optional LLM-assisted repair and verification subsystem.

## Core Components
- **CLI layer**: `scripts/*` targeting `src/human_code_qc/cli.py`
- **Validators**: Highly modular `src/human_code_qc/validators/*`
- **Models**: Strongly typed Pydantic models.
- **Repair Engine**: Divides into `deterministic.py` and `llm.py` via `policy.py`.
- **LLM Gateway**: `LiteLLM` pointing to `code-repair` model.
- **Sandbox**: Docker-based execution runners in `src/human_code_qc/sandbox/*`.

## Storage Directories
- **audit/**: Reports, queue lists, review lists.
- **repaired/**: Output for repairs (subdivided into deterministic, llm_assisted, reconstructed, rejected, uncertain).
- **verified/**: Verified dataset files.
- **manifests/**: Output dataset manifests.

*The original dataset archive (`C:\HumanCodeDataset\original\test-human-code.zip`) is strictly read-only and immutable.*
