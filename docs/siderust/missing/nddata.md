# astropy.nddata

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.nddata` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `NDData`, `NDDataRef`, `CCDData`
- Uncertainty propagation (`StdDevUncertainty`, `VarianceUncertainty`, etc.)
- `NDArithmeticMixin` — arithmetic with masks and WCS
- Bit flags, slicing, unit-aware operations

## Current backend

Pure Python built on NumPy arrays and `astropy.units`.

## Siderust coverage today

None.

## Gap list

N-dimensional masked array containers, arithmetic, and uncertainty attachment.

## Proposed kernel names

None planned.

## Blockers

NDData is a data-container abstraction, not an astronomy kernel surface.

## Fallback behavior

Full upstream Astropy nddata implementation.
