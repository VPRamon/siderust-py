# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Contains the transformation functions for getting to "observed" systems from ICRS.
"""

import erfa
import numpy as np

from astropy import units as u
from astropy.coordinates.baseframe import frame_transform_graph
from astropy.coordinates.builtin_frames.utils import atciqz, aticq
from astropy.coordinates.erfa_astrom import erfa_astrom
from astropy.coordinates.representation import (
    CartesianRepresentation,
    SphericalRepresentation,
    UnitSphericalRepresentation,
)
from astropy.coordinates.transformations import FunctionTransformWithFiniteDifference

from .altaz import AltAz
from .hadec import HADec
from .icrs import ICRS
from .utils import PIOVER2


def _has_mask(value):
    try:
        masked = getattr(value, "masked", False)
    except ValueError:
        return False
    return masked is not False


def _try_siderust_icrs_to_altaz(icrs_coo, observed_frame, is_unitspherical):
    if not is_unitspherical or not isinstance(observed_frame, AltAz):
        return None

    from astropy import _siderust

    if not _siderust.should_use_siderust("coordinates.icrs_to_altaz"):
        return None
    if _has_mask(icrs_coo) or _has_mask(observed_frame):
        return None
    if getattr(icrs_coo.data, "differentials", None):
        return None
    if observed_frame.location is None or observed_frame.obstime is None:
        return None

    pressure = observed_frame.pressure.to_value(u.hPa)
    if np.any(np.asarray(pressure) != 0.0):
        return None

    from astropy._siderust.kernels import icrs_to_altaz_unit_spherical

    usrepr = icrs_coo.represent_as(UnitSphericalRepresentation)
    location = observed_frame.location
    ra = usrepr.lon.to_value(u.radian)
    dec = usrepr.lat.to_value(u.radian)
    obstime_tt_jd = observed_frame.obstime.tt.jd
    longitude = location.lon.to_value(u.radian)
    latitude = location.lat.to_value(u.radian)
    height = location.height.to_value(u.m)

    if any(
        np.any(~np.isfinite(np.asarray(value, dtype=np.float64)))
        for value in (ra, dec, obstime_tt_jd, longitude, latitude, height)
    ):
        return None

    az, alt = icrs_to_altaz_unit_spherical(
        ra,
        dec,
        obstime_tt_jd,
        longitude,
        latitude,
        height,
    )
    obs_srepr = UnitSphericalRepresentation(
        az << u.radian, alt << u.radian, copy=False
    )
    return observed_frame.realize_frame(obs_srepr)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, ICRS, AltAz)
@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, ICRS, HADec)
def icrs_to_observed(icrs_coo, observed_frame):
    # if the data are UnitSphericalRepresentation, we can skip the distance calculations
    is_unitspherical = (
        isinstance(icrs_coo.data, UnitSphericalRepresentation)
        or icrs_coo.cartesian.x.unit == u.one
    )
    siderust_result = _try_siderust_icrs_to_altaz(
        icrs_coo, observed_frame, is_unitspherical
    )
    if siderust_result is not None:
        return siderust_result

    # first set up the astrometry context for ICRS<->observed
    astrom = erfa_astrom.get().apco(observed_frame)

    # correct for parallax to find BCRS direction from observer (as in erfa.pmpx)
    if is_unitspherical:
        srepr = icrs_coo.spherical
    else:
        observer_icrs = CartesianRepresentation(
            astrom["eb"], unit=u.au, xyz_axis=-1, copy=None
        )
        srepr = (icrs_coo.cartesian - observer_icrs).represent_as(
            SphericalRepresentation
        )

    # convert to topocentric CIRS
    cirs_ra, cirs_dec = atciqz(srepr, astrom)

    # now perform observed conversion
    if isinstance(observed_frame, AltAz):
        lon, zen, _, _, _ = erfa.atioq(cirs_ra, cirs_dec, astrom)
        lat = PIOVER2 - zen
    else:
        _, _, lon, lat, _ = erfa.atioq(cirs_ra, cirs_dec, astrom)

    if is_unitspherical:
        obs_srepr = UnitSphericalRepresentation(
            lon << u.radian, lat << u.radian, copy=False
        )
    else:
        obs_srepr = SphericalRepresentation(
            lon << u.radian, lat << u.radian, srepr.distance, copy=False
        )
    return observed_frame.realize_frame(obs_srepr)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, AltAz, ICRS)
@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, HADec, ICRS)
def observed_to_icrs(observed_coo, icrs_frame):
    # if the data are UnitSphericalRepresentation, we can skip the distance calculations
    is_unitspherical = (
        isinstance(observed_coo.data, UnitSphericalRepresentation)
        or observed_coo.cartesian.x.unit == u.one
    )

    usrepr = observed_coo.represent_as(UnitSphericalRepresentation)
    lon = usrepr.lon.to_value(u.radian)
    lat = usrepr.lat.to_value(u.radian)

    if isinstance(observed_coo, AltAz):
        # the 'A' indicates zen/az inputs
        coord_type = "A"
        lat = PIOVER2 - lat
    else:
        coord_type = "H"

    # first set up the astrometry context for ICRS<->CIRS at the observed_coo time
    astrom = erfa_astrom.get().apco(observed_coo)

    # Topocentric CIRS
    cirs_ra, cirs_dec = erfa.atoiq(coord_type, lon, lat, astrom) << u.radian
    if is_unitspherical:
        srepr = SphericalRepresentation(cirs_ra, cirs_dec, 1, copy=None)
    else:
        srepr = SphericalRepresentation(
            lon=cirs_ra,
            lat=cirs_dec,
            distance=observed_coo.distance,
            copy=None,
        )

    # BCRS (Astrometric) direction to source
    bcrs_ra, bcrs_dec = aticq(srepr, astrom) << u.radian

    # Correct for parallax to get ICRS representation
    if is_unitspherical:
        icrs_srepr = UnitSphericalRepresentation(bcrs_ra, bcrs_dec, copy=None)
    else:
        icrs_srepr = SphericalRepresentation(
            lon=bcrs_ra,
            lat=bcrs_dec,
            distance=observed_coo.distance,
            copy=None,
        )
        observer_icrs = CartesianRepresentation(
            astrom["eb"], unit=u.au, xyz_axis=-1, copy=None
        )
        newrepr = icrs_srepr.to_cartesian() + observer_icrs
        icrs_srepr = newrepr.represent_as(SphericalRepresentation)

    return icrs_frame.realize_frame(icrs_srepr)


# Create loopback transformations
frame_transform_graph._add_merged_transform(AltAz, ICRS, AltAz)
frame_transform_graph._add_merged_transform(HADec, ICRS, HADec)
# for now we just implement this through ICRS to make sure we get everything
# covered
# Before, this was using CIRS as intermediate frame, however this is much
# slower than the direct observed<->ICRS transform added in 4.3
# due to how the frame attribute broadcasting works, see
# https://github.com/astropy/astropy/pull/10994#issuecomment-722617041
