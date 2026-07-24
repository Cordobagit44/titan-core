from __future__ import annotations

import ast
from pathlib import Path

CORE_PATH = Path("src/titan/core")
FORBIDDEN_ROOT_IMPORTS = {"anthropic", "fastapi", "openai", "pydantic", "requests", "sqlalchemy"}


def imported_root_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".", maxsplit=1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", maxsplit=1)[0])
    return roots


def test_core_has_no_forbidden_framework_dependencies() -> None:
    violations: dict[str, list[str]] = {}
    for path in CORE_PATH.rglob("*.py"):
        forbidden = sorted(imported_root_modules(path) & FORBIDDEN_ROOT_IMPORTS)
        if forbidden:
            violations[str(path)] = forbidden
    assert violations == {}
