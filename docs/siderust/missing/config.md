# astropy.config

| Field | Value |
|-------|-------|
| **Status** | `not_applicable` |
| **Astropy module** | `astropy.config` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

- `ConfigItem`, `ConfigNamespace` — runtime configuration for Astropy subpackages
- `get_config_dir`, configuration file I/O
- `astropy._siderust.conf.backend_mode` — Siderust dispatch toggle

## Current backend

Pure Python configuration infrastructure.

## Siderust coverage today

None. Siderust backend selection is configured in Python (`astropy._siderust`).

## Gap list

No numerical kernels. Configuration remains entirely in Python.

## Proposed kernel names

None.

## Blockers

None.

## Fallback behavior

N/A — not a computation surface.
