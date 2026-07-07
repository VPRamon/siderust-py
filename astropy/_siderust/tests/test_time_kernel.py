# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest
import erfa

from astropy import _siderust
from astropy._siderust import conf
from astropy._siderust.kernels import tai_jd_to_tt_jd
from astropy.time import Time


def test_native_tai_jd_to_tt_jd_scalar_matches_erfa():
    jd1, jd2 = tai_jd_to_tt_jd(2451545.0, 0.25)
    expected1, expected2 = erfa.taitt(2451545.0, 0.25)

    assert jd1 == pytest.approx(expected1)
    assert jd2 == pytest.approx(expected2)


def test_native_tai_jd_to_tt_jd_vector_matches_erfa():
    jd1 = np.array([2451545.0, 2451546.0])
    jd2 = np.array([0.25, -0.125])

    out1, out2 = tai_jd_to_tt_jd(jd1, jd2)
    expected1, expected2 = erfa.taitt(jd1, jd2)

    assert np.allclose(out1, expected1)
    assert np.allclose(out2, expected2)


def test_time_tai_to_tt_dispatches_to_siderust(monkeypatch):
    calls = []

    def fake_should_use_siderust(kernel_name):
        return kernel_name == "time.tai_jd_to_tt_jd"

    def fake_tai_jd_to_tt_jd(jd1, jd2):
        calls.append((np.shape(jd1), np.shape(jd2)))
        return erfa.taitt(jd1, jd2)

    monkeypatch.setattr(_siderust, "should_use_siderust", fake_should_use_siderust)
    monkeypatch.setattr(
        "astropy._siderust.kernels.tai_jd_to_tt_jd",
        fake_tai_jd_to_tt_jd,
    )

    result = Time([2451545.0, 2451546.0], format="jd", scale="tai").tt

    assert calls == [((2,), (2,))]
    assert result.scale == "tt"


def test_time_tai_to_tt_matches_existing_path_when_backend_enabled():
    with conf.set_temp("backend_mode", "off"):
        expected = Time([2451545.0, 2451546.0], format="jd", scale="tai").tt

    with conf.set_temp("backend_mode", "on"):
        result = Time([2451545.0, 2451546.0], format="jd", scale="tai").tt

    assert result.scale == "tt"
    assert np.allclose(result.jd1, expected.jd1)
    assert np.allclose(result.jd2, expected.jd2)


def test_unsupported_time_conversion_uses_existing_path(monkeypatch):
    calls = []

    def fake_should_use_siderust(kernel_name):
        calls.append(kernel_name)
        return False

    monkeypatch.setattr(_siderust, "should_use_siderust", fake_should_use_siderust)

    result = Time(2451545.0, format="jd", scale="tt").tai

    assert result.scale == "tai"
    assert calls == []
