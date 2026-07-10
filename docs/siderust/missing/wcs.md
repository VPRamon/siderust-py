# astropy.wcs

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.wcs` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `WCS` — World Coordinate System transformations
- FITS WCS header parsing, SIP/distortion, tabular distortions
- `wcslib` bindings for celestial ↔ pixel transforms

## Current backend

Bundled `wcslib` C library (`cextern/wcslib`) with C extension wrappers in
`astropy/wcs/src/`.

## Siderust coverage today

None. Siderust coordinate frames serve observation geometry, not FITS WCS
header semantics.

## Gap list

All WCS parsing, distortion application, and pixel ↔ world transforms.

## Proposed kernel names

None planned (explicit README non-goal).

## Blockers

WCS is a separate standards domain (FITS WCS papers) from Siderust frame
transforms.

## Fallback behavior

Full upstream wcslib-backed implementation.
