# Siderust missing-feature inventory

This directory documents Astropy subpackages and operations that are **not yet**
delegated to the [Siderust](https://github.com/Siderust/siderust) crate through
`siderust-py`. Each file corresponds to one top-level `astropy` subpackage.

siderust-py keeps the Astropy public API unchanged. When a feature listed here
is invoked, the existing Astropy, ERFA, Cython, or C implementation runs.

## Status legend

| Status | Meaning |
|--------|---------|
| `supported` | Kernel(s) wired and passing parity tests |
| `partial` | Some paths delegated; most still use Astropy/ERFA |
| `planned` | Siderust API expected; integration designed |
| `blocked` | Waiting on upstream `siderust` API |
| `not_in_siderust` | No Siderust equivalent; Astropy path retained |
| `not_applicable` | Infrastructure; no numerical kernel target |

## Kernel registry cross-reference

Supported and planned kernels are registered in
[`astropy/_siderust/boundary.py`](../../../astropy/_siderust/boundary.py).
Diagnostics: `python -m astropy._siderust`.

## Subpackage index

| File | Subpackage | Status |
|------|------------|--------|
| [config.md](config.md) | `astropy.config` | `not_applicable` |
| [constants.md](constants.md) | `astropy.constants` | `not_in_siderust` |
| [convolution.md](convolution.md) | `astropy.convolution` | `not_in_siderust` |
| [coordinates.md](coordinates.md) | `astropy.coordinates` | `partial` |
| [cosmology.md](cosmology.md) | `astropy.cosmology` | `not_in_siderust` |
| [io.md](io.md) | `astropy.io` | `not_in_siderust` |
| [modeling.md](modeling.md) | `astropy.modeling` | `not_in_siderust` |
| [nddata.md](nddata.md) | `astropy.nddata` | `not_in_siderust` |
| [samp.md](samp.md) | `astropy.samp` | `not_applicable` |
| [stats.md](stats.md) | `astropy.stats` | `not_in_siderust` |
| [table.md](table.md) | `astropy.table` | `not_in_siderust` |
| [time.md](time.md) | `astropy.time` | `partial` |
| [timeseries.md](timeseries.md) | `astropy.timeseries` | `not_in_siderust` |
| [uncertainty.md](uncertainty.md) | `astropy.uncertainty` | `not_in_siderust` |
| [units.md](units.md) | `astropy.units` | `not_in_siderust` |
| [utils.md](utils.md) | `astropy.utils` | `not_in_siderust` |
| [visualization.md](visualization.md) | `astropy.visualization` | `not_in_siderust` |
| [wcs.md](wcs.md) | `astropy.wcs` | `not_in_siderust` |

## Adding a new entry

Copy [`_template.md`](_template.md), fill every section, and add a row to the
index table above. When a kernel moves from `planned` to `supported`, update the
relevant file and `boundary.py` in the same pull request.
