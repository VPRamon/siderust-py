# astropy.constants

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.constants` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- CODATA/IAU physical and astronomical constants (`c`, `G`, `h`, `au`, `pc`, etc.)
- Versioned constant sets (`astropyconst13`, `astropyconst20`, `astropyconst40`)
- `Constant`, `EMConstant` with units

## Current backend

Static Python `Quantity` objects; no runtime computation.

## Siderust coverage today

Siderust defines physical constants internally (`qtty`, mission modules) but
does not expose a constants registry matching Astropy's API.

## Gap list

Entire subpackage — constant lookup, versioning, and unit attachment.

## Proposed kernel names

None planned.

## Blockers

Astropy constants are declarative data, not compute kernels. Delegation would
add coupling without performance benefit.

## Fallback behavior

All constant access uses upstream Astropy definitions.
