# Implementation Plan (Master Roadmap)

Following the 59-phase specification:

1. **Phase 0 & 1: Inspection & Preflight** (Completed): Inspected repository, preflighted dataset.
2. **Phase 2: Project Architecture**: Reorganize existing `src/` to `src/human_code_qc/` with all defined subpackages. Create `pyproject.toml`, `config/*.yaml` files, `schemas/`, `prompts/`, and `tests/`.
3. **Phase 3-5: Models & Hashing**: Implement Pydantic models and SHA-256 hashers.
4. **Phase 6-18: Validation & Discovery**: Build validators for metadata, structural checks, provenance, generated code suspected, duplicates, syntax (per language), matching.
5. **Phase 19-31: Repair Pipeline**: Implement CLI for auditing, deterministic repairs, and carefully bounded LLM repairs via LiteLLM. Introduce Docker sandboxes for verification.
6. **Phase 32-58: Scale & Reporting**: Manifest generation, Reproducibility layers, Staged execution (10 -> 50 -> 500 -> full).

*Note: Execution will strictly follow the Staged Execution guidelines (Phase 53 & 54) and halt at each milestone for human review.*
