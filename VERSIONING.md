# Version management

1. Work only on a new branch for a strategy change.
2. Copy the current `solution/` into `versions/vX.Y/solution/` before editing.
3. Record the change, evidence, test result and unresolved hypotheses in that version's review report.
4. Run offline checks before changing the active `solution/`.
5. Commit the snapshot and tag it (`v0.3.3`, `v0.4-experiment`, etc.).
6. Never commit `.env`, API keys, databases, framework sessions, raw emulator logs or large transcripts.
7. To roll back, copy the selected snapshot's `solution/` into the active `solution/`, verify `versions/MANIFEST.json`, then perform the separately approved runtime deployment/reload.

The active version is recorded in `versions/MANIFEST.json`. A failed experiment remains available under its own snapshot and report; it is not silently merged into the active strategy.
