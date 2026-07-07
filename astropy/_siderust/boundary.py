# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Private Python/Rust boundary helpers for future Siderust kernels."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class BoundaryArray:
    """Plain numerical array plus the unit expected by a native kernel."""

    name: str
    data: np.ndarray
    unit: str
    optional: bool = False


@dataclass(frozen=True)
class BoundaryValue:
    """Name and unit metadata for one native-kernel value."""

    name: str
    unit: str
    optional: bool = False


@dataclass(frozen=True)
class KernelSpec:
    """Boundary contract for one planned or supported native kernel."""

    name: str
    inputs: tuple[BoundaryValue, ...]
    outputs: tuple[BoundaryValue, ...]
    supported: bool = False


PLANNED_KERNELS = (
    KernelSpec(
        name="time.utc_jd_to_tai_jd",
        inputs=(
            BoundaryValue("jd1", "day"),
            BoundaryValue("jd2", "day"),
        ),
        outputs=(BoundaryValue("tai_jd", "day"),),
    ),
    KernelSpec(
        name="time.tai_jd_to_tt_jd",
        inputs=(
            BoundaryValue("jd1", "day"),
            BoundaryValue("jd2", "day"),
        ),
        outputs=(
            BoundaryValue("tt_jd1", "day"),
            BoundaryValue("tt_jd2", "day"),
        ),
        supported=True,
    ),
    KernelSpec(
        name="coordinates.icrs_to_altaz",
        inputs=(
            BoundaryValue("ra", "radian"),
            BoundaryValue("dec", "radian"),
            BoundaryValue("obstime_tt_jd", "TT Julian date day"),
            BoundaryValue("longitude", "radian"),
            BoundaryValue("latitude", "radian"),
            BoundaryValue("height", "meter", optional=True),
        ),
        outputs=(
            BoundaryValue("az", "radian"),
            BoundaryValue("alt", "radian"),
        ),
        supported=True,
    ),
)

SUPPORTED_KERNELS = tuple(kernel for kernel in PLANNED_KERNELS if kernel.supported)


def _is_astropy_object(value: Any) -> bool:
    return hasattr(value, "unit") or hasattr(value, "to_value")


def as_boundary_array(
    name: str,
    value: Any,
    unit: str,
    *,
    optional: bool = False,
    dtype: np.dtype | type = np.float64,
) -> BoundaryArray | None:
    """Normalize a scalar or array-like value for the native boundary."""

    if value is None:
        if optional:
            return None
        raise ValueError(f"{name} is required")

    if _is_astropy_object(value):
        raise TypeError(
            f"{name} must be converted to a plain value in {unit} before "
            "crossing the Siderust boundary"
        )

    data = np.asarray(value, dtype=dtype)
    if data.dtype.kind == "O":
        raise TypeError(f"{name} must be a numeric scalar or array")

    return BoundaryArray(name=name, data=data, unit=unit, optional=optional)


def broadcast_boundary_shape(*arrays: BoundaryArray | None) -> tuple[int, ...]:
    """Return the shared shape for scalar, vector, and optional inputs."""

    shapes = [array.data.shape for array in arrays if array is not None]
    if not shapes:
        return ()
    return np.broadcast_shapes(*shapes)
