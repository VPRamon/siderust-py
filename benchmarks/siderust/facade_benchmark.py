#!/usr/bin/env python3
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Facade-level benchmarks for Siderust-backed Astropy code paths.

Run from the repository root after an editable install:

    python benchmarks/siderust/facade_benchmark.py
"""

from __future__ import annotations

import timeit
from pathlib import Path

import numpy as np

from astropy import units as u
from astropy._siderust import conf
from astropy.coordinates import AltAz, EarthLocation, ICRS
from astropy.time import Time
from astropy.utils import iers

REPEAT = 5
NUMBER = 20

iers.conf.auto_download = False


def _location() -> EarthLocation:
    return EarthLocation(lon=-17.8925 * u.deg, lat=28.7543 * u.deg, height=2396 * u.m)


def bench_tai_to_tt() -> None:
    times = Time(np.linspace(2_456_000.0, 2_460_000.0, 10_000), format="jd", scale="tai")

    def run_off() -> None:
        with conf.set_temp("backend_mode", "off"):
            _ = times.tt

    def run_on() -> None:
        with conf.set_temp("backend_mode", "on"):
            _ = times.tt

    off = min(timeit.repeat(run_off, repeat=REPEAT, number=NUMBER))
    on = min(timeit.repeat(run_on, repeat=REPEAT, number=NUMBER))
    print(f"time.tai_to_tt  backend=off  {off:.4f}s")
    print(f"time.tai_to_tt  backend=on   {on:.4f}s  (ratio {on / off:.2f}x)")


def bench_icrs_to_altaz() -> None:
    location = _location()
    obstime = Time(np.linspace(2_458_000.0, 2_459_000.0, 1_000), format="jd", scale="utc")
    coord = ICRS(
        ra=np.linspace(0.0, 360.0, 1_000) * u.deg,
        dec=np.linspace(-30.0, 60.0, 1_000) * u.deg,
    )
    frame = AltAz(obstime=obstime, location=location, pressure=0 * u.hPa)

    def run_off() -> None:
        with conf.set_temp("backend_mode", "off"):
            _ = coord.transform_to(frame)

    def run_on() -> None:
        with conf.set_temp("backend_mode", "on"):
            _ = coord.transform_to(frame)

    off = min(timeit.repeat(run_off, repeat=REPEAT, number=NUMBER))
    on = min(timeit.repeat(run_on, repeat=REPEAT, number=NUMBER))
    print(f"coords.icrs_altaz  backend=off  {off:.4f}s")
    print(f"coords.icrs_altaz  backend=on   {on:.4f}s  (ratio {on / off:.2f}x)")


def main() -> None:
    if not Path(__file__).is_file():
        raise SystemExit("Run this script from the siderust-py repository.")

    print("siderust-py facade benchmarks")
    print(f"repeat={REPEAT} number={NUMBER}")
    bench_tai_to_tt()
    bench_icrs_to_altaz()


if __name__ == "__main__":
    main()
