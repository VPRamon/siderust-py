# astropy.&lt;subpackage&gt;

| Field | Value |
|-------|-------|
| **Status** | `not_in_siderust` |
| **Astropy module** | `astropy.&lt;subpackage&gt;` |
| **Siderust pin** | `0.11.0` |

## Astropy surface area

Key classes, functions, and user-facing APIs in this subpackage.

## Current backend

How Astropy implements this today (ERFA, Cython, C, pure Python).

## Siderust coverage today

What the pinned `siderust` crate provides that could back this subpackage, if anything.

## Gap list

Specific operations or APIs not available in Siderust.

## Proposed kernel names

Kernel identifiers matching `astropy._siderust.boundary.KernelSpec.name` naming
(`module.operation`), if applicable.

## Blockers

Upstream Siderust APIs, features, or validation work required before integration.

## Fallback behavior

What siderust-py users experience when no Siderust kernel is available for a
given operation.
