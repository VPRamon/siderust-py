# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Private helpers for the Siderust kernel boundary contract.

These helpers are intentionally small and Python-only.  They codify the shape,
dtype, contiguity, and optional-value rules documented for the private native
boundary without implementing any scientific kernels.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def broadcast_shape(*values: Any) -> tuple[int, ...]:
    """Return the NumPy broadcast shape for supplied boundary values.

    ``None`` values are ignored because missing optional arrays are expanded only
    after the required batch shape is known.
    """

    shapes = [np.shape(value) for value in values if value is not None]
    if not shapes:
        return ()

    try:
        return np.broadcast_shapes(*shapes)
    except ValueError as exc:
        joined = ", ".join(str(shape) for shape in shapes)
        raise ValueError(f"boundary inputs are not broadcast-compatible: {joined}") from exc


def as_float64_c_array(
    name: str,
    value: Any,
    shape: tuple[int, ...] | None = None,
) -> np.ndarray:
    """Convert a boundary value to a C-contiguous ``float64`` array.

    If ``shape`` is provided, the value is broadcast to that shape first.
    """

    try:
        array = np.asarray(value, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be convertible to float64") from exc

    if shape is not None:
        try:
            array = np.broadcast_to(array, shape)
        except ValueError as exc:
            raise ValueError(
                f"{name} with shape {array.shape} cannot broadcast to boundary "
                f"shape {shape}"
            ) from exc

    return np.ascontiguousarray(array, dtype=np.float64)


def optional_float64_array(
    name: str,
    value: Any | None,
    shape: tuple[int, ...],
    *,
    missing_value: float = np.nan,
) -> np.ndarray:
    """Return an optional boundary array with missing values expanded.

    ``None`` means missing and is filled with ``missing_value``.  Explicit values,
    including physical zero, are preserved after broadcasting.
    """

    if value is None:
        return np.full(shape, missing_value, dtype=np.float64)

    return as_float64_c_array(name, value, shape)
