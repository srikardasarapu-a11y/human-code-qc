# Dataset Safety

- The original dataset `C:\HumanCodeDataset\original\test-human-code.zip` is strictly IMMUTABLE.
- NEVER modify, rewrite, delete, rename, normalize in place, or extract over it.
- All derived outputs, reports, and repaired files MUST go to an external directory (e.g. `audit/`, `repaired/`).
- Treat all original data as READ-ONLY and stop operations before any path pointing to the original archive is written to.
