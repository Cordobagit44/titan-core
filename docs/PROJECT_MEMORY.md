# TITAN Core – Project Memory

## Vision

TITAN Core is the domain engine for TITAN.

The project prioritizes correctness, maintainability, and long-term evolution over implementation speed.

## Architecture

The project follows:

- Domain-Driven Design (DDD)
- Clean Architecture
- Vertical Slice Architecture
- Test-Driven Development (TDD)
- Repository Pattern
- Domain Events

## Technology Stack

- Python 3.13
- uv
- pytest
- Ruff
- mypy
- SQLite (development persistence)

## Development Workflow

Every story follows the same workflow:

1. RED
2. GREEN
3. REFACTOR
4. Run all tests
5. Run Ruff
6. Run mypy
7. Commit
8. Push

No story is considered complete until every quality gate passes.

## Development Rules

- The domain never depends on infrastructure.
- Infrastructure adapts the domain.
- Tests define the expected behaviour.
- Every story implements a single functional capability.
- One file is reviewed at a time.
- All code is written in English.
- Conversation is in Spanish.
- Every completed story leaves the project in a green state.

## Current Status

Latest completed story:

- CORE-037 — Record Investigation Closure

Current quality gates:

- pytest ✅
- Ruff ✅
- mypy ✅

## Repository Structure

- `src/` — Application source code
- `tests/` — Automated tests
- `docs/specs/` — Functional specifications
- `docs/PROJECT_MEMORY.md` — Project memory
- `docs/CHANGELOG.md` — Functional history

## Next Story

- CORE-038
