# Security

- NEVER request, print, commit, or hard-code secrets (`GITHUB_TOKEN`, `LITELLM_MASTER_KEY`).
- Do not bypass Windows permission boundaries or access controls.
- Untrusted code must only be executed in a Docker sandbox. If Docker is unavailable, fail gracefully with `SANDBOX_UNAVAILABLE`.
- Secure against path traversal and malicious zip archives.
