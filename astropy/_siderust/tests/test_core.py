# Licensed under a 3-clause BSD style license - see LICENSE.rst

import astropy._siderust._core as core
from astropy._siderust import backend_info, is_available


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
