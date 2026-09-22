# Coding Standards

- The environment is strictly Python 3.12.4 mapped to the `.venv\Scripts\python.exe` interpreter. Do not use the global interpreter (3.14+).
- Use Pydantic models for strongly typed data representations.
- Abstractions must be used for providers (e.g., LiteLLM is the gateway, do not hardcode model providers in audit layers).
- Maintain deterministic output schemas.
