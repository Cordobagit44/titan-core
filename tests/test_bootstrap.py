from __future__ import annotations

import titan


def test_package_exposes_version() -> None:
    assert titan.__version__ == "0.1.0"
