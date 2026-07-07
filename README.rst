siderust-py
===========

siderust-py is an experimental fork of Astropy intended to keep the familiar
Astropy Python API while selectively delegating performance-sensitive numerical
astronomy kernels to Siderust through native Python bindings.

The project goal is not to rewrite all of Astropy. The goal is to preserve the
Astropy-facing user experience for APIs such as ``Time``, ``SkyCoord``,
``EarthLocation``, and ``AltAz``, while making selected internal computation
paths available through Siderust when they are scientifically validated and
measurably beneficial.

Current status
==============

This repository is at the planning and integration-bootstrap stage. It is still
primarily an Astropy fork. Siderust-backed execution paths are not yet part of
the public runtime behavior unless explicitly introduced by later changes.

Compatibility policy
====================

siderust-py should remain compatible with Astropy's public Python API unless a
compatibility difference is explicitly documented.

The intended dispatch model is:

* keep Astropy-compatible public objects and call patterns;
* normalize selected numerical workloads into a low-overhead Python/Rust
  boundary;
* execute supported kernels through Siderust when the backend is enabled;
* fall back to the existing Astropy implementation for unsupported operations;
* report both numerical agreement and performance impact before enabling a new
  accelerated path by default.

Users should not need to pass Siderust-specific objects into standard Astropy
APIs. Native kernels should receive simple numerical inputs such as arrays,
scalars, and explicitly documented units at the internal boundary.

Initial acceleration scope
==========================

The first development phase focuses on a narrow set of astronomy-computation
surfaces where Siderust can plausibly provide value without destabilizing the
full Astropy package:

* ``astropy.time``: selected time-scale and Julian-date-style conversions;
* ``astropy.coordinates``: selected high-value coordinate transforms, starting
  with planning-oriented paths such as ICRS to AltAz if supported by Siderust;
* scheduling-oriented workflows: batch target/time/location calculations where
  Python object churn and repeated transformations can dominate runtime;
* backend diagnostics: tools to determine whether Siderust is available,
  enabled, and used for a given supported path;
* correctness and performance evidence: parity tests and benchmarks that report
  both runtime and numerical deltas.

Initial non-goals
=================

The first iteration does not attempt to accelerate or replace all of Astropy.
In particular, the following areas are outside the initial Siderust-backed
scope unless a later ticket explicitly expands the plan:

* FITS I/O;
* WCS;
* tables;
* modeling and fitting;
* visualization;
* general file/network I/O;
* broad replacement of ERFA/pyerfa-backed behavior before scientific parity is
  demonstrated;
* claims of universal speedup, especially for scalar or Python-object-heavy
  workloads.

Development direction
=====================

The expected implementation path is incremental:

1. document the fork identity and compatibility policy;
2. add a minimal native Siderust extension that can be imported from Python;
3. define the Python/Rust kernel boundary using arrays and explicit units;
4. add backend selection and diagnostics;
5. route one time kernel and one coordinate kernel through Siderust;
6. add parity tests against the existing Astropy behavior;
7. add facade-level benchmarks using normal Astropy-style code;
8. document supported accelerated paths and fallbacks.

Upstream Astropy attribution
============================

This repository is derived from Astropy. Astropy is a community project that
develops a core astronomy package for Python and promotes interoperability
between astronomy packages.

Useful upstream resources:

* `Astropy website <https://astropy.org/>`_
* `Astropy documentation <https://docs.astropy.org/>`_
* `Astropy contribution guide <https://www.astropy.org/contribute.html>`_
* `Astropy developer documentation <https://docs.astropy.org/en/latest/index_dev.html>`_
* `Astropy AI Policy <https://github.com/astropy/astropy-project/blob/main/policies/ai-policy.md>`_

License
=======

Astropy is licensed under a 3-clause BSD style license. This fork preserves the
upstream license; see `LICENSE.rst <LICENSE.rst>`_ and the files under
``licenses/``.

Installation
============

This fork is not yet presented as a stable public replacement for Astropy. For
normal Astropy usage, install upstream Astropy from PyPI:

.. code-block:: bash

    pip install astropy

For siderust-py development, clone this repository and use the development
installation workflow described by the project once the native Siderust build
skeleton is introduced.

Contributing
============

Contributions should follow the fork's compatibility policy above and preserve
upstream Astropy attribution. For Siderust-specific work, prefer small pull
requests tied to the planning tickets in this repository.

Security note
=============

Do not accept code, patches, or build artifacts through ZIP files or opaque
attachments in issues. Proposed changes should arrive through normal pull
requests with source diffs, tests, and reviewable explanations.
