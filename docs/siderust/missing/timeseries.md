# astropy.timeseries

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.timeseries` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `TimeSeries`, `BinnedTimeSeries`
- `BoxLeastSquares`, Lomb-Scargle periodograms (including multiband)
- Sampled and binned time-series utilities

## Current backend

Python built on `astropy.table`, `astropy.time`, and NumPy/SciPy.

## Siderust coverage today

None for periodogram or time-series container APIs.

## Gap list

Time-series containers, periodogram algorithms, and binning.

## Proposed kernel names

None planned.

## Blockers

Scheduling-oriented batch coordinate/time work may eventually use Siderust
kernels indirectly via `astropy.coordinates` and `astropy.time`, but this
subpackage itself has no delegation targets.

## Fallback behavior

Full upstream Astropy timeseries implementation.
