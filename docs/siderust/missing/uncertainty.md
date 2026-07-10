# astropy.uncertainty

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.uncertainty` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `Distribution` — array of samples representing uncertainty
- Functions: `normal`, `uniform` distribution constructors
- Propagation through unit-aware operations

## Current backend

Pure Python on NumPy.

## Siderust coverage today

None.

## Gap list

Distribution containers and sample-based uncertainty propagation.

## Proposed kernel names

None planned.

## Blockers

Uncertainty propagation is a Python/NumPy concern, not a Siderust kernel.

## Fallback behavior

Full upstream implementation.
