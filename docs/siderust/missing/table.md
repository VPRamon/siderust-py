# astropy.table

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.table` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `Table`, `QTable`, `Column`, `Row`, `MaskedColumn`
- Joins, vstack/hstack, grouping, indexing
- Unit-aware columns, mixin columns (coordinates, times)
- Cython column mixins (`_column_mixins.pyx`)

## Current backend

Python table algebra with Cython-accelerated column operations.

## Siderust coverage today

None.

## Gap list

Table storage, manipulation, joins, and serialization.

## Proposed kernel names

None planned (explicit README non-goal).

## Blockers

Tables are a data-structure layer, not Siderust kernel targets.

## Fallback behavior

Full upstream Astropy table implementation.
