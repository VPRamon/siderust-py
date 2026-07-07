# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest

from astropy._siderust.boundary import (
    PLANNED_KERNELS,
    SUPPORTED_KERNELS,
    as_boundary_array,
    broadcast_boundary_shape,
)


def test_boundary_array_normalizes_scalars_and_arrays():
    scalar = as_boundary_array("jd1", 1.0, "day")
    vector = as_boundary_array("jd2", [1.0, 2.0, 3.0], "day")

    assert scalar.data.shape == ()
    assert vector.data.shape == (3,)
    assert vector.unit == "day"
    assert vector.data.dtype == np.float64


def test_optional_boundary_value_can_be_missing():
    assert as_boundary_array("height", None, "meter", optional=True) is None


def test_required_boundary_value_cannot_be_missing():
    with pytest.raises(ValueError, match="jd1 is required"):
        as_boundary_array("jd1", None, "day")


def test_astropy_objects_must_be_converted_before_boundary():
    class QuantityLike:
        unit = "m"

    with pytest.raises(TypeError, match="plain value in meter"):
        as_boundary_array("height", QuantityLike(), "meter")


def test_boundary_shape_rules_support_scalar_vector_and_mixed_inputs():
    scalar = as_boundary_array("jd1", 1.0, "day")
    vector = as_boundary_array("jd2", [1.0, 2.0, 3.0], "day")
    optional = as_boundary_array("height", None, "meter", optional=True)

    assert broadcast_boundary_shape(scalar) == ()
    assert broadcast_boundary_shape(vector) == (3,)
    assert broadcast_boundary_shape(scalar, vector, optional) == (3,)


def test_boundary_shape_rules_reject_incompatible_shapes():
    ra = as_boundary_array("ra", np.ones((2,)), "radian")
    dec = as_boundary_array("dec", np.ones((3,)), "radian")

    with pytest.raises(ValueError):
        broadcast_boundary_shape(ra, dec)


def test_planned_kernel_contracts_have_explicit_units():
    assert [kernel.name for kernel in SUPPORTED_KERNELS] == [
        "time.tai_jd_to_tt_jd",
        "coordinates.icrs_to_altaz",
    ]
    assert PLANNED_KERNELS

    for kernel in PLANNED_KERNELS:
        for value in kernel.inputs + kernel.outputs:
            assert value.unit
