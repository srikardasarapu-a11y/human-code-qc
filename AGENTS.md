# Antigravity Agents Workspace Customizations

This workspace adheres strictly to the **Human Code QC** Master Specification.

## Rules
- Dataset Safety ([dataset-safety.md](.agents/rules/dataset-safety.md)): The original dataset is IMMUTABLE.
- Research Integrity ([research-integrity.md](.agents/rules/research-integrity.md)): Preserve uncertainty and factual provenance.
- Coding Standards ([coding-standards.md](.agents/rules/coding-standards.md)): Use Python 3.12.4 via `.venv`, Pydantic models, robust abstractions.
- Testing ([testing.md](.agents/rules/testing.md)): pytest for all validators, synthetic fixtures preferred.
- Security ([security.md](.agents/rules/security.md)): No secrets committed, untrusted code requires Docker.
- LLM Repair ([llm-repair.md](.agents/rules/llm-repair.md)): Use LiteLLM abstraction, disable by default, repair vs reconstruction.
