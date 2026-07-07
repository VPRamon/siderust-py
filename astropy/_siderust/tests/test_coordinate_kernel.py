# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest

from astropy import _siderust
from astropy import units as u
from astropy._siderust import conf
from astropy._siderust.kernels import icrs_to_altaz_unit_spherical
from astropy.coordinates import AltAz, EarthLocation, ICRS
from astropy.coordinates.representation import UnitSphericalRepresentation
from astropy.time import Time
from astropy.utils import iers


MAX_CURRENT_DELTA = 30.0


def setup_module(module):
    iers.conf.auto_download = False


def _location():
    return EarthLocation(lon=-17.8925 * u.deg, lat=28.7543 * u.deg, height=2396 * u.m)


def _assert_current_altaz_tolerance(actual, expected):
    daz = (actual.az - expected.az).wrap_at(180 * u.deg).to_value(u.arcsec)
    dalt = (actual.alt - expected.alt).to_value(u.arcsec)

    assert np.all(np.abs(daz) < MAX_CURRENT_DELTA)
    assert np.all(np.abs(dalt) < MAX_CURRENT_DELTA)


def test_native_icrs_to_altaz_unit_spherical_scalar_matches_current_astropy():
    location = _location()
    obstime = Time("2020-06-01T00:00:00", scale="utc")
    coord = ICRS(ra=101.287 * u.deg, dec=-16.716 * u.deg)
    frame = AltAz(obstime=obstime, location=location, pressure=0 * u.hPa)

    with conf.set_temp("backend_mode", "off"):
        expected = coord.transform_to(frame)

    az, alt = icrs_to_altaz_unit_spherical(
        coord.ra.to_value(u.radian),
        coord.dec.to_value(u.radian),
        obstime.tt.jd,
        location.lon.to_value(u.radian),
        location.lat.to_value(u.radian),
        location.height.to_value(u.m),
    )
    actual = frame.realize_frame(
        UnitSphericalRepresentation(az << u.radian, alt << u.radian)
    )

    _assert_current_altaz_tolerance(actual, expected)


def test_icrs_to_altaz_dispatches_to_siderust_for_unit_spherical_no_refraction(monkeypatch):
    calls = []

    def fake_should_use_siderust(kernel_name):
        return kernel_name == "coordinates.icrs_to_altaz"

    def fake_icrs_to_altaz(ra, dec, obstime_tt_jd, longitude, latitude, height):
        calls.append((np.shape(ra), np.shape(obstime_tt_jd), np.shape(height)))
        return np.zeros_like(np.asarray(ra)), np.zeros_like(np.asarray(dec))

    monkeypatch.setattr(_siderust, "should_use_siderust", fake_should_use_siderust)
    monkeypatch.setattr(
        "astropy._siderust.kernels.icrs_to_altaz_unit_spherical",
        fake_icrs_to_altaz,
    )

    location = _location()
    frame = AltAz(
        obstime=Time(["2020-06-01T00:00:00", "2020-06-01T01:00:00"], scale="utc"),
        location=location,
        pressure=0 * u.hPa,
    )
    coord = ICRS(ra=[101.287, 210.0] * u.deg, dec=[-16.716, 54.0] * u.deg)

    result = coord.transform_to(frame)

    assert calls == [((2,), (2,), ())]
    assert isinstance(result, AltAz)
    assert np.all(result.az == 0 * u.radian)
    assert np.all(result.alt == 0 * u.radian)


def test_icrs_to_altaz_matches_current_astropy_when_backend_enabled():
    location = _location()
    frame = AltAz(
        obstime=Time(["2020-06-01T00:00:00", "2020-12-01T03:00:00"], scale="utc"),
        location=location,
        pressure=0 * u.hPa,
    )
    coord = ICRS(ra=[101.287, 210.0] * u.deg, dec=[-16.716, 54.0] * u.deg)

    with conf.set_temp("backend_mode", "off"):
        expected = coord.transform_to(frame)
    with conf.set_temp("backend_mode", "on"):
        actual = coord.transform_to(frame)

    _assert_current_altaz_tolerance(actual, expected)


def test_icrs_to_altaz_falls_back_for_refraction(monkeypatch):
    def fake_should_use_siderust(kernel_name):
        return kernel_name == "coordinates.icrs_to_altaz"

    def fail_if_called(*args, **kwargs):
        raise AssertionError("Siderust coordinate kernel should not be called")

    monkeypatch.setattr(_siderust, "should_use_siderust", fake_should_use_siderust)
    monkeypatch.setattr(
        "astropy._siderust.kernels.icrs_to_altaz_unit_spherical",
        fail_if_called,
    )

    frame = AltAz(
        obstime=Time("2020-06-01T00:00:00", scale="utc"),
        location=_location(),
        pressure=1013 * u.hPa,
    )
    coord = ICRS(ra=101.287 * u.deg, dec=-16.716 * u.deg)

    result = coord.transform_to(frame)

    assert isinstance(result, AltAz)


def test_icrs_to_altaz_falls_back_for_coordinates_with_distance(monkeypatch):
    def fake_should_use_siderust(kernel_name):
        return kernel_name == "coordinates.icrs_to_altaz"

    def fail_if_called(*args, **kwargs):
        raise AssertionError("Siderust coordinate kernel should not be called")

    monkeypatch.setattr(_siderust, "should_use_siderust", fake_should_use_siderust)
    monkeypatch.setattr(
        "astropy._siderust.kernels.icrs_to_altaz_unit_spherical",
        fail_if_called,
    )

    frame = AltAz(
        obstime=Time("2020-06-01T00:00:00", scale="utc"),
        location=_location(),
        pressure=0 * u.hPa,
    )
    coord = ICRS(ra=101.287 * u.deg, dec=-16.716 * u.deg, distance=10 * u.pc)

    result = coord.transform_to(frame)

    assert isinstance(result, AltAz)


def test_icrs_to_altaz_falls_back_for_nonfinite_inputs(monkeypatch):
    def fake_should_use_siderust(kernel_name):
        return kernel_name == "coordinates.icrs_to_altaz"

    def fail_if_called(*args, **kwargs):
        raise AssertionError("Siderust coordinate kernel should not be called")

    monkeypatch.setattr(_siderust, "should_use_siderust", fake_should_use_siderust)
    monkeypatch.setattr(
        "astropy._siderust.kernels.icrs_to_altaz_unit_spherical",
        fail_if_called,
    )

    frame = AltAz(
        obstime=Time("2020-06-01T00:00:00", scale="utc"),
        location=_location(),
        pressure=0 * u.hPa,
    )
    coord = ICRS(ra=np.nan * u.deg, dec=-16.716 * u.deg)

    with pytest.warns(RuntimeWarning, match="invalid value encountered"):
        result = coord.transform_to(frame)

    assert isinstance(result, AltAz)
