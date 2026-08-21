from __future__ import annotations

import ast
from pathlib import Path

APPLICATION_PATH = Path("src/titan/application")

DIRECT_REPOSITORY_MODULES = {
    "titan.application.domain_event_repository",
    "titan.application.investigation_repository",
}

ALLOWED_DIRECT_REPOSITORY_DEPENDENCIES = {
    "domain_event_repository.py",
    "get_investigation.py",
    "in_memory_domain_event_repository.py",
    "in_memory_investigation_repository.py",
    "investigation_repository.py",
    "list_investigations.py",
    "persist_domain_events.py",
    "unit_of_work.py",
}


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(
        path.read_text(encoding="utf-8"),
        filename=str(path),
    )
    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)

    return modules


def test_application_repository_dependencies_are_explicit() -> None:
    violations: dict[str, list[str]] = {}

    for path in APPLICATION_PATH.glob("*.py"):
        if path.name in ALLOWED_DIRECT_REPOSITORY_DEPENDENCIES:
            continue

        forbidden = sorted(imported_modules(path) & DIRECT_REPOSITORY_MODULES)

        if forbidden:
            violations[str(path)] = forbidden

    assert violations == {}
