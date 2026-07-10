# astropy.units

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.units` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `Unit`, `Quantity`, `CompositeUnit`
- Unit systems: SI, CGS, astrophys, photometric, imperial
- Format parsers: `fits`, `cds`, `vounit`, `ogip`, `latex`, etc.
- Equivalencies, decorators (`@quantity_input`), structured units

## Current backend

Pure Python unit registry and parsing; Cython lexer tables for CDS format.

## Siderust coverage today

Siderust uses its own typed quantities (`qtty::Degrees`, `Meters`, etc.) at the
Rust boundary. There is no bridge to Astropy's unit system.

## Gap list

Entire unit parsing, conversion, formatting, and `Quantity` arithmetic layer.
Unit conversion at the Siderust boundary is explicit: Python converts to plain
`float64` with documented units before calling Rust.

## Proposed kernel names

None planned.

## Blockers

Astropy units are the public API facade; they must remain in Python.

## Fallback behavior

All unit handling uses upstream Astropy. Siderust kernels receive pre-converted
numerical arrays only.
