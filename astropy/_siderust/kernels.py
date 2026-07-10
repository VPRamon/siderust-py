# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Python wrappers for Siderust-backed native kernels."""

from __future__ import annotations

import numpy as np

from . import _load_core


def tai_jd_to_tt_jd(jd1, jd2):
    """Convert TAI split Julian dates to TT split Julian dates."""

    core = _load_core()
    if core is None:
        raise RuntimeError("Siderust native extension is not importable")

    jd1_array = np.asarray(jd1, dtype=np.float64)
    jd2_array = np.asarray(jd2, dtype=np.float64)
    shape = np.broadcast_shapes(jd1_array.shape, jd2_array.shape)
    jd1_broadcast = np.broadcast_to(jd1_array, shape)
    jd2_broadcast = np.broadcast_to(jd2_array, shape)

    out1, out2 = core.tai_jd_to_tt_jd(
        jd1_broadcast.ravel().tolist(),
        jd2_broadcast.ravel().tolist(),
    )
    out1 = np.asarray(out1, dtype=np.float64).reshape(shape)
    out2 = np.asarray(out2, dtype=np.float64).reshape(shape)

    if shape == ():
        return out1[()], out2[()]
    return out1, out2


def utc_jd_to_tai_jd(jd1, jd2):
    """Convert UTC split Julian dates to TAI Julian dates.

    Blocked until Siderust exposes a public UTC/TAI leap-second API.
    """

    core = _load_core()
    if core is None:
        raise RuntimeError("Siderust native extension is not importable")

    jd1_array = np.asarray(jd1, dtype=np.float64)
    jd2_array = np.asarray(jd2, dtype=np.float64)
    shape = np.broadcast_shapes(jd1_array.shape, jd2_array.shape)
    jd1_broadcast = np.broadcast_to(jd1_array, shape)
    jd2_broadcast = np.broadcast_to(jd2_array, shape)

    out = core.utc_jd_to_tai_jd(
        jd1_broadcast.ravel().tolist(),
        jd2_broadcast.ravel().tolist(),
    )
    out = np.asarray(out, dtype=np.float64).reshape(shape)

    if shape == ():
        return out[()]
    return out


def icrs_to_altaz_unit_spherical(
    ra,
    dec,
    obstime_tt_jd,
    longitude,
    latitude,
    height,
):
    """Transform unit-spherical ICRS coordinates to no-refraction AltAz."""

    core = _load_core()
    if core is None:
        raise RuntimeError("Siderust native extension is not importable")

    inputs = [
        np.asarray(value, dtype=np.float64)
        for value in (ra, dec, obstime_tt_jd, longitude, latitude, height)
    ]
    shape = np.broadcast_shapes(*(value.shape for value in inputs))
    broadcast = [np.broadcast_to(value, shape) for value in inputs]

    az, alt = core.icrs_to_altaz_unit_spherical(
        *(value.ravel().tolist() for value in broadcast)
    )
    az = np.asarray(az, dtype=np.float64).reshape(shape)
    alt = np.asarray(alt, dtype=np.float64).reshape(shape)

    if shape == ():
        return az[()], alt[()]
    return az, alt
