# astropy.modeling

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.modeling` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `Model`, `FittableModel`, compound models, parameter sets
- Functional models (Gaussians, polynomials, power laws, etc.)
- `fitting` — Levenberg-Marquardt and other optimizers
- Splines, convolutions, model I/O

## Current backend

Pure Python with optional SciPy optimizers; no Siderust-relevant native code.

## Siderust coverage today

None.

## Gap list

Model evaluation, fitting, parameter constraints, and compound model algebra.

## Proposed kernel names

None planned.

## Blockers

Modeling/fitting is outside initial Siderust acceleration scope.

## Fallback behavior

Full upstream Astropy modeling stack.
