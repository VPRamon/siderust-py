# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest

from astropy._siderust.boundary import (
    as_float64_c_array,
    broadcast_shape,
    optional_float64_array,
)


def test_broadcast_shape_accepts_scalars_and_vectors():
    assert broadcast_shape(1.0, np.arange(3, dtype=np.float64)) == (3,)


def test_broadcast_shape_accepts_target_time_grid():
    targets = np.zeros((2, 1), dtype=np.float64)
    times = np.zeros(3, dtype=np.float64)

    assert broadcast_shape(targets, times) == (2, 3)


def test_broadcast_shape_rejects_incompatible_vectors():
    with pytest.raises(ValueError, match="not broadcast-compatible"):
        broadcast_shape(np.zeros(2, dtype=np.float64), np.zeros(3, dtype=np.float64))


def test_as_float64_c_array_broadcasts_to_boundary_shape():
    ra_rad = np.array([[1.0], [2.0]])

    array = as_float64_c_array("ra_rad", ra_rad, shape=(2, 3))

    assert array.dtype == np.float64
    assert array.shape == (2, 3)
    assert array.flags.c_contiguous
    np.testing.assert_allclose(array, [[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]])


def test_as_float64_c_array_rejects_non_numeric_values():
    with pytest.raises(TypeError, match="obstime_jd1_utc_days"):
        as_float64_c_array("obstime_jd1_utc_days", "not-a-number")


def test_optional_float64_array_uses_nan_for_missing_values():
    distance_m = optional_float64_array("distance_m", None, shape=(3,))

    assert distance_m.dtype == np.float64
    assert distance_m.shape == (3,)
    assert np.isnan(distance_m).all()


def test_optional_float64_array_preserves_physical_zero():
    radial_velocity_m_per_s = optional_float64_array(
        "radial_velocity_m_per_s",
        0.0,
        shape=(3,),
    )

    assert radial_velocity_m_per_s.dtype == np.float64
    assert radial_velocity_m_per_s.shape == (3,)
    np.testing.assert_array_equal(radial_velocity_m_per_s, np.zeros(3))


def test_optional_observer_height_can_default_to_zero_meters():
    observer_height_m = optional_float64_array(
        "observer_height_m",
        None,
        shape=(2,),
        missing_value=0.0,
    )

    np.testing.assert_array_equal(observer_height_m, np.zeros(2))
