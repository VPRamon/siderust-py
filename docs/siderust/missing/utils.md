# astropy.utils

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.utils` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

Major utilities used across Astropy:

- `iers` — IERS Earth-orientation and leap-second tables
- `data` — remote data download and cache
- `masked` — masked array/quantity support
- `xml`, `metadata`, `shapes`, `parsing`, `console`, `diff`

## Current backend

Pure Python; IERS table parsing; optional downloads from network mirrors.

## Siderust coverage today

Siderust maintains its own EOP/leap-second data paths internally (`tempoch`,
`astro::eop`) but does not replace Astropy's `iers` module for Python users.

## Gap list

IERS table management, data caching, XML helpers, masked array utilities, and
miscellaneous shared helpers.

## Proposed kernel names

None planned. Leap-second **data** for `time.utc_jd_to_tai_jd` must come from a
Siderust public API, not by replacing `astropy.utils.iers` wholesale.

## Blockers

`astropy.utils.iers` is tightly coupled to Astropy `Time` UTC handling.

## Fallback behavior

Full upstream utils implementation.
