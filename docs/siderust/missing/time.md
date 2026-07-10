# astropy.time

| Field | Value |
|-------|-------|
| **Status** | `partial` |
| **Astropy module** | `astropy.time` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

Primary user-facing types and operations:

- `Time` — time instants with scale (`utc`, `tai`, `tt`, `tcb`, `tcg`, `tdb`, `ut1`)
- `TimeDelta` — durations between instants
- Scale conversion via properties (`.tt`, `.utc`, `.tai`, etc.) and `_set_scale`
- Format parsing (`iso`, `jd`, `mjd`, `fits`, etc.)
- Leap-second table management via `astropy.utils.iers`
- Location-aware time (`Time` with `location` for light-travel corrections)

## Current backend

- Scale transforms: ERFA/pyerfa (`erfa.*tt*`, `erfa.*utc*`, etc.) via internal
  transform chains in `astropy/time/core.py`
- Parsing: optional fast C parser; Python fallback
- Leap seconds: IERS tables in `astropy/utils/iers`

## Siderust coverage today

| Operation | Siderust API | siderust-py kernel |
|-----------|--------------|-------------------|
| TAI → TT offset | `siderust::time::constats::TT_MINUS_TAI` | `time.tai_jd_to_tt_jd` (**supported**) |
| UTC → TAI (leap seconds) | Internal to `tempoch`; not exposed for split JD | `time.utc_jd_to_tai_jd` (**blocked**) |
| Other scale chains | Partial via `tempoch` / EOP modules | None |

## Gap list

### Supported (via Siderust)

- `Time(..., scale="tai").tt` for **unmasked** times when
  `astropy._siderust.conf.backend_mode` is `"auto"` or `"on"`

### Blocked on upstream Siderust

- **`time.utc_jd_to_tai_jd`** — UTC to TAI with leap-second handling for Astropy
  split Julian dates (`jd1`, `jd2`). Siderust 0.11.0 delegates leap-second
  history to `tempoch` internally but does not expose a public UTC/TAI
  conversion surface suitable for this boundary contract.

### Not in Siderust (Astropy path retained)

- All other scale conversions (`utc` ↔ `ut1`, `tdb`, `tcb`, `tcg`, etc.)
- `TimeDelta` arithmetic and scale changes
- String format parsing and output formatting
- Masked `Time` scale changes
- Sub-nanosecond precision requirements beyond current kernel scope
- Location-dependent light-time corrections

## Proposed kernel names

| Kernel | Status | Astropy hook |
|--------|--------|--------------|
| `time.tai_jd_to_tt_jd` | **supported** | `Time._set_scale_siderust` in `time/core.py` |
| `time.utc_jd_to_tai_jd` | **blocked** | Future: `Time._set_scale` UTC chain |

## Blockers

### `time.utc_jd_to_tai_jd`

Siderust must expose a stable public API that:

1. Accepts UTC split Julian dates (`jd1`, `jd2` in days)
2. Applies the IERS-compatible leap-second table (or equivalent `tempoch` chain)
3. Returns TAI split Julian dates with documented error semantics

Until then, all UTC-involving scale changes use ERFA via `_check_leapsec()` and
the existing `MULTI_HOPS` transform graph.

## Fallback behavior

| User operation | Siderust used? | Fallback |
|----------------|----------------|----------|
| `tai` → `tt`, unmasked, backend on | Yes | — |
| `tai` → `tt`, masked | No | ERFA |
| Any scale involving `utc` | No | ERFA + leap-second table |
| All other scale pairs | No | ERFA transform chain |
| `backend_mode="off"` | No | Full Astropy/ERFA |

Users see identical `Time` objects and APIs regardless of backend; only internal
computation paths differ.
