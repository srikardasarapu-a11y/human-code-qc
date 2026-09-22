# Current State

## Existing Files & Directory Tree
The repository contains work generated prior to the 59-phase master specification:
- `.git/` and `.gitignore`
- `.env` and `.env.example`
- `requirements.txt`
- `AGENTS.md` and `.agents/`
- `config/litellm.yaml`
- `docs/architecture.md`, `docs/implementation_plan.md`
- `src/main.py`, `src/config/`, `src/core/`

## Existing Architecture & Scripts
- A naive reading layer in `src/core/dataset_reader.py` (yields parsed python and meta json pairs).
- A basic linting placeholder in `src/core/qc_pipeline.py`.
- A litellm hook for repair in `src/core/llm_repair.py`.
- The entrypoint in `src/main.py` does not use Hermes, directly hooks up LiteLLM.

## Environment & Configuration
- LiteLLM is configured in `config/litellm.yaml` pointing to `ollama/deepseek-coder:6.7b` at `http://localhost:11434`.
- **Conflict**: Local powershell returned Python `3.14.6` for `python` instead of the required `.venv`'s `3.12.4` environment. Shell must be properly scoped to the virtual environment for python tool usage.
- Docker is available (`29.0.1`), Git is available (`2.52.0`), Ollama is available (`0.32.14`).

## Dataset Preflight Statistics
- Path: `C:\HumanCodeDataset\original\test-human-code.zip`
- Total entries: 18,461
- Metadata files (`.json`): 9,215
- Code files: Python (`.py`): 1,843, Java (`.java`): 1,843, C (`.c`): 1,843, C++ (`.cpp`): 1,843, JS (`.js`): 1,843
- Directories: 31

## Gaps & Conflicts with Master Specification
- **Architecture**: `src/core/` and `src/config/` must be moved into the `src/human_code_qc/` package structure defined by Phase 2.
- **Data Models**: Missing Pydantic models (Phase 3).
- **Validation Rules**: Missing the rigorous classification of errors and severities (Phases 7-18).
- **Repair Engine**: Exists but does not distinguish between deterministic and LLM-assisted, nor does it enforce the verification phases (Phases 20-31).
- **Configuration**: Missing `audit.yaml`, `repair.yaml`, `verification.yaml`, etc.

## Proposed Migration
No files will be deleted yet. In Phase 2, `src/core/` and `src/main.py` will be migrated into `src/human_code_qc/` and expanded into the appropriate modular structure, deprecating the naive `core/` package.
