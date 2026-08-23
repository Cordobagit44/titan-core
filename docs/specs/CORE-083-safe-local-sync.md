# CORE-083 — Add Safe Local Synchronization

## Status

In Progress

## Context

GitHub is TITAN's durable source of truth, while development also happens from a local
VS Code checkout. A blind or scheduled `git pull` could produce confusing repository
state when the local checkout has uncommitted work, is on a feature branch, or has
commits that diverge from `origin/main`.

## Goal

Provide an explicit, one-click synchronization workflow that updates a clean local
`main` branch only when Git can do so with a fast-forward.

## Behavior

`scripts/sync-titan.ps1` must:

- require Git to be available;
- require execution from within a Git repository;
- stop when tracked or untracked local changes exist;
- stop when the current branch is not `main`;
- verify that `origin` exists;
- fetch `origin/main` with pruning;
- stop when local `main` has commits absent from `origin/main`;
- update only through `git merge --ff-only origin/main`;
- optionally run the complete TITAN quality gates.

VS Code tasks must expose:

- a safe synchronization task;
- a safe synchronization and validation task.

## Acceptance Criteria

- No periodic or background pull is introduced.
- No local changes are stashed, discarded, reset, or overwritten.
- No branch is switched automatically.
- Diverged or locally-ahead history requires manual review.
- Remote-only commits are applied with fast-forward only.
- The validation option runs dependency synchronization, Ruff lint, Ruff format,
  mypy, and pytest.
- Existing production and test behavior remains unchanged.

## Out of Scope

CORE-083 does not introduce:

- automatic commits or pushes;
- automatic branch switching;
- automatic conflict resolution;
- scheduled synchronization;
- destructive resets;
- production domain, application, or persistence changes.
