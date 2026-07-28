# TITAN Core – Changelog

This document summarizes the functional evolution of TITAN Core.

It complements the Git history and the functional specifications by providing a concise overview of completed stories.

---

## CORE-037 — Record Investigation Closure

### Added

- `Investigation.closed_at`
- `InvestigationClosed` domain event
- `close()` records the closure timestamp
- `close()` publishes the `InvestigationClosed` domain event
- `reopen()` clears `closed_at`
- SQLite persistence for `closed_at`
- SQLite restoration of `closed_at`

### Validation

- pytest ✅
- Ruff ✅
- mypy ✅
