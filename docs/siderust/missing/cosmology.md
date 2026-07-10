# astropy.cosmology

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.cosmology` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `Cosmology`, `FLRW`, `LambdaCDM`, `FlatLambdaCDM`, `wCDM`, etc.
- Distance and age calculations: `luminosity_distance`, `comoving_distance`,
  `lookback_time`, `H`, `inv_efunc`
- I/O: mapping, YAML, MRT, LaTeX, cosmology registry

## Current backend

Pure Python with SciPy integration for integrals; no native extensions.

## Siderust coverage today

None.

## Gap list

Cosmological distance integrals, parameter sets, and cosmology registry I/O.

## Proposed kernel names

None planned.

## Blockers

Cosmology is outside Siderust's solar-system / observation geometry focus.

## Fallback behavior

Full upstream Astropy cosmology implementation.
