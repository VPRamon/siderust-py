# astropy.io

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.io` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

Subpackages and major I/O surfaces:

- `astropy.io.fits` — FITS file read/write, headers, compression, tables
- `astropy.io.ascii` — ASCII table formats (IPAC, CDS, LaTeX, etc.)
- `astropy.io.votable` — VOTable XML
- `astropy.io.misc` — ECSV, HDF5, Parquet, YAML, ASDF hooks
- `astropy.io.registry` — unified I/O registration

## Current backend

- FITS: bundled `cfitsio` C library (`cextern/cfitsio`) + Python wrappers
- VOTable: pure Python XML parsing
- ASCII: pure Python readers/writers
- Compression: C extensions for Rice, HCOMPRESS, etc.

## Siderust coverage today

Siderust includes format parsers (`formats::spice`, `formats::ccsds`, etc.) for
mission data, but none match Astropy's FITS/VOTable/ASCII APIs.

## Gap list

All file-format I/O, registry, and serialization for astronomical tables and
images.

## Proposed kernel names

None planned (explicit README non-goal).

## Blockers

FITS/WCS I/O is a separate domain from Siderust observation-geometry kernels.

## Fallback behavior

All I/O uses upstream Astropy implementations unchanged.
