# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Private Siderust backend integration helpers.

This package intentionally exposes only minimal diagnostics at this stage.  The
native extension is a build skeleton; scientific kernels are introduced by later
issues.
"""

from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Any

_CORE_MODULE = "astropy._siderust._core"


def _load_core() -> ModuleType | None:
    try:
        return import_module(_CORE_MODULE)
    except ImportError:
        return None


def is_available() -> bool:
    """Return whether the native Siderust extension can be imported."""

    return _load_core() is not None


def backend_info() -> dict[str, Any]:
    """Return diagnostic information about the native Siderust extension."""

    core = _load_core()
    if core is None:
        return {
            "available": False,
            "module": _CORE_MODULE,
            "reason": "native extension is not importable",
        }

    return {
        "available": True,
        "module": _CORE_MODULE,
        "name": core.backend_name(),
        "version": core.version(),
        "skeleton": core.is_skeleton(),
    }


__all__ = ["backend_info", "is_available"]
