# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Private Siderust backend integration helpers.

This package exposes private diagnostics and dispatch helpers for native
Siderust-backed kernels.
"""

from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Any

from astropy import config as _config

_CORE_MODULE = "astropy._siderust._core"
BACKEND_MODES = ["auto", "off", "on"]


class Conf(_config.ConfigNamespace):
    """
    Configuration parameters for `astropy._siderust`.
    """

    backend_mode = _config.ConfigItem(
        BACKEND_MODES,
        "Siderust backend mode. Use 'off' to force existing Astropy behavior, "
        "'on' to request Siderust when a supported kernel exists, or 'auto' to "
        "use Siderust only when it is available and supported.",
    )


conf = Conf()


def _load_core() -> ModuleType | None:
    try:
        return import_module(_CORE_MODULE)
    except ImportError:
        return None


def is_available() -> bool:
    """Return whether the native Siderust extension can be imported."""

    return _load_core() is not None


def _supported_kernel_names() -> list[str]:
    from .boundary import SUPPORTED_KERNELS

    return [kernel.name for kernel in SUPPORTED_KERNELS]


def _planned_kernel_names() -> list[str]:
    from .boundary import PLANNED_KERNELS

    return [kernel.name for kernel in PLANNED_KERNELS]


def backend_status() -> dict[str, Any]:
    """Return Siderust backend mode, availability, and kernel diagnostics."""

    core = _load_core()
    mode = conf.backend_mode
    extension_available = core is not None
    enabled = mode != "off" and extension_available

    status = {
        "mode": mode,
        "enabled": enabled,
        "available": extension_available,
        "extension_available": extension_available,
        "module": _CORE_MODULE,
        "supported_kernels": _supported_kernel_names(),
        "planned_kernels": _planned_kernel_names(),
    }

    if core is None:
        status["reason"] = "native extension is not importable"
        return status

    status.update(
        {
            "name": core.backend_name(),
            "version": core.version(),
            "skeleton": core.is_skeleton(),
            "dependencies": core.dependency_info(),
        }
    )
    if mode == "off":
        status["reason"] = "backend disabled by configuration"
    elif not status["supported_kernels"]:
        status["reason"] = "native extension available; no kernels are registered yet"

    return status


def backend_info() -> dict[str, Any]:
    """Return diagnostic information about the native Siderust extension."""

    return backend_status()


def should_use_siderust(kernel_name: str) -> bool:
    """Return whether a named internal kernel should use Siderust."""

    status = backend_status()
    return status["enabled"] and kernel_name in status["supported_kernels"]


__all__ = [
    "BACKEND_MODES",
    "Conf",
    "backend_info",
    "backend_status",
    "conf",
    "is_available",
    "should_use_siderust",
]
