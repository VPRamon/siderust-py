# astropy.visualization

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.visualization` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `ImageNormalize`, interval classes (`MinMaxInterval`, `ZScaleInterval`, etc.)
- `wcsaxes` — WCS-aware Matplotlib axes
- RGB composition, lupton-style stretches, histogram utilities

## Current backend

Python integration with Matplotlib; WCS plotting delegates to `astropy.wcs`.

## Siderust coverage today

None.

## Gap list

Plotting, normalization, stretch functions, and WCSAxes integration.

## Proposed kernel names

None planned (explicit README non-goal).

## Blockers

Visualization is a Matplotlib-facing layer, not a Siderust compute target.

## Fallback behavior

Full upstream visualization implementation.
