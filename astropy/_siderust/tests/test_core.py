# Licensed under a 3-clause BSD style license - see LICENSE.rst

import astropy._siderust._core as core
from astropy import _siderust
from astropy._siderust import (
    backend_info,
    backend_status,
    conf,
    is_available,
    should_use_siderust,
)


def test_core_module_importable():
    assert core.version() == "0.0.0"
    assert core.backend_name() == "siderust-py native extension skeleton"
    assert core.is_skeleton() is True


def test_backend_info_reports_native_extension():
    info = backend_info()

    assert is_available() is True
    assert info["available"] is True
    assert info["module"] == "astropy._siderust._core"
    assert info["name"] == "siderust-py native extension skeleton"
    assert info["version"] == "0.0.0"
    assert info["skeleton"] is True


def test_backend_status_reports_mode_and_kernels():
    info = backend_status()

    assert info["mode"] == "auto"
    assert info["enabled"] is True
    assert info["extension_available"] is True
    assert info["supported_kernels"] == []
    assert info["planned_kernels"] == [
        "time.utc_jd_to_tai_jd",
        "coordinates.icrs_to_altaz",
    ]


def test_backend_can_be_disabled():
    with conf.set_temp("backend_mode", "off"):
        info = backend_status()

        assert info["mode"] == "off"
        assert info["enabled"] is False
        assert should_use_siderust("time.utc_jd_to_tai_jd") is False


def test_backend_on_does_not_route_unsupported_kernels():
    with conf.set_temp("backend_mode", "on"):
        info = backend_status()

        assert info["mode"] == "on"
        assert info["enabled"] is True
        assert should_use_siderust("unsupported.kernel") is False


def test_missing_native_code_is_reported(monkeypatch):
    monkeypatch.setattr(_siderust, "_load_core", lambda: None)

    with conf.set_temp("backend_mode", "on"):
        info = backend_status()

    assert info["available"] is False
    assert info["extension_available"] is False
    assert info["enabled"] is False
    assert info["reason"] == "native extension is not importable"
