#!/usr/bin/env python3
"""Verify planned Siderust kernels are referenced in missing-feature docs."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MISSING_DOCS = REPO_ROOT / "docs" / "siderust" / "missing"
BOUNDARY = REPO_ROOT / "astropy" / "_siderust" / "boundary.py"


def _planned_kernel_names() -> list[str]:
    namespace: dict[str, object] = {}
    exec(BOUNDARY.read_text(encoding="utf-8"), namespace)  # noqa: S102
    planned = namespace["PLANNED_KERNELS"]
    return [kernel.name for kernel in planned]


def _doc_corpus() -> str:
    parts = [MISSING_DOCS / "README.md"]
    parts.extend(sorted(MISSING_DOCS.glob("*.md")))
    return "\n".join(path.read_text(encoding="utf-8") for path in parts)


def main() -> int:
    corpus = _doc_corpus()
    missing = [name for name in _planned_kernel_names() if name not in corpus]

    if missing:
        print("Planned kernels not referenced in docs/siderust/missing/:")
        for name in missing:
            print(f"  - {name}")
        return 1

    print("All planned kernels are referenced in missing-feature docs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
