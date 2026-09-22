# LLM Repair

- LLM Repair is DISABLED by default (`allow_llm_repair: false`).
- Use the `LiteLLM` abstraction exclusively (`code-repair` model via `http://localhost:4000`).
- Differentiate heavily between REPAIR (bounded fix of existing code) and RECONSTRUCTION (generating missing code from a problem statement).
- Never trust LLM output automatically. It MUST pass independent verification.
