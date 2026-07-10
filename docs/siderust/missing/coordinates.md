# astropy.coordinates

| Field | Value |
|-------|-------|
| **Status** | `partial` |
| **Astropy module** | `astropy.coordinates` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

Primary user-facing types and operations:

- `SkyCoord` — high-level coordinate wrapper
- Frame types: `ICRS`, `FK5`, `Galactic`, `AltAz`, `HADec`, `GCRS`, `CIRS`, etc.
- `EarthLocation` — observer geodetic positions
- Frame transform graph (`frame_transform_graph`)
- Representations: spherical, cartesian, unit-spherical, differentials
- Matching, name resolution, solar-system bodies, spectral coordinates

## Current backend

- Coordinate transforms: ERFA/pyerfa via `astropy/coordinates/builtin_frames/`
- Astrometry context: `erfa_astrom` for observed-frame transforms
- Matrix utilities, finite-difference velocity transforms

## Siderust coverage today

Siderust 0.11.0 (`default-features = false`) exposes horizontal-coordinate
helpers under `siderust::event::horizontal`:

| Siderust API | Used by siderust-py? |
|--------------|---------------------|
| `star_horizontal` | Yes — `coordinates.icrs_to_altaz` |
| `star_horizontal_with_policy` | No — planned for precision tuning |
| `equatorial_to_horizontal` | No |
| `equatorial_to_horizontal_true_of_date` | No |
| `geocentric_j2000_to_apparent_topocentric` | No |

Atmospheric refraction lives behind the optional `atmosphere` feature
(`siderust::atmosphere`); not enabled in the current pin.

## Gap list

### Supported (via Siderust)

- **ICRS → AltAz** for unit-spherical coordinates when:
  - `obstime` and `location` are set
  - `pressure == 0` (no refraction)
  - No distance or differentials attached
  - No masked coordinates; all inputs finite
  - Backend mode `"auto"` or `"on"`

Hook: `_try_siderust_icrs_to_altaz` in
`astropy/coordinates/builtin_frames/icrs_observed_transforms.py`.

### Planned

| Gap | Proposed kernel | Siderust notes |
|-----|-----------------|----------------|
| Refraction (`pressure != 0`) | `coordinates.icrs_to_altaz_with_refraction` | Requires `atmosphere` feature + refraction model API |
| ICRS → HADec | `coordinates.icrs_to_hadec` | `equatorial_to_horizontal` may apply; needs HADec mapping |
| AltAz → ICRS reverse | `coordinates.altaz_to_icrs` | No hook today; `observed_to_icrs` is ERFA-only |
| Coordinates with distance | `coordinates.icrs_to_altaz` (extended) | Current kernel is unit-spherical only |
| Proper motion / radial velocity | — | Differentials not supported at boundary |
| Masked coordinates | — | Fall back to ERFA |
| FK5, Galactic, ecliptic, etc. | — | No Siderust frame graph equivalent |
| `SkyCoord` matching, solar system | — | Out of initial scope |

### Performance note (not a user-facing gap)

`icrs_to_altaz_unit_spherical` loops element-wise in Rust. Batch vectorization
depends on future batched APIs in `siderust`.

## Proposed kernel names

| Kernel | Status | Astropy hook |
|--------|--------|--------------|
| `coordinates.icrs_to_altaz` | **supported** | `icrs_to_observed` (AltAz branch) |
| `coordinates.icrs_to_altaz_with_refraction` | **planned** | `icrs_to_observed` (non-zero pressure) |
| `coordinates.icrs_to_hadec` | **planned** | `icrs_to_observed` (HADec branch) |
| `coordinates.altaz_to_icrs` | **planned** | `observed_to_icrs` |

## Blockers

- **Refraction**: Enable and pin `siderust` `atmosphere` feature; validate against
  Astropy refraction model in `AltAz` frame defaults.
- **HADec**: Map Siderust horizontal output to hour-angle / declination convention
  used by Astropy's `HADec` frame.
- **Reverse transform**: Siderust apparent-topocentric pipeline is forward-only
  today; reverse requires invertible API or separate kernel.
- **Parity tightening**: Bootstrap tolerance is 20 arcseconds (see
  `test_coordinate_kernel.py`); must tighten further before claiming
  high-precision replacement.

## Fallback behavior

| User operation | Siderust used? | Fallback |
|----------------|----------------|----------|
| ICRS → AltAz, unit-spherical, P=0 | Yes (if guards pass) | — |
| ICRS → AltAz, refraction | No | ERFA `aticq` / `atciqz` |
| ICRS → HADec | No | ERFA |
| AltAz → ICRS | No | ERFA |
| Any frame not listed above | No | ERFA transform graph |
| `backend_mode="off"` | No | Full Astropy/ERFA |

Users invoke `coord.transform_to(AltAz(...))` as with upstream Astropy; dispatch
is transparent.
