# astropy.stats

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.stats` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `sigma_clip`, `sigma_clipped_stats`, `mad_std`
- Circular statistics (`circmean`, `circstd`, etc.)
- `histogram`, `bayesian_blocks`, Lomb-Scargle (`lombscargle`)
- Robust estimators, jackknife, biweight

## Current backend

- Cython: `astropy/stats/_stats.pyx`
- C: `astropy/stats/src/wirth_select.c`
- Python/SciPy for remaining functions

## Siderust coverage today

None.

## Gap list

Statistical functions, clipping, periodograms, and robust estimators.

## Proposed kernel names

None planned.

## Blockers

General statistics are outside Siderust scope.

## Fallback behavior

Cython/C/Python upstream paths unchanged.
