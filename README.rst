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
primarily an Astropy fork. A minimal native extension now exists under
``astropy._siderust`` and pins the published ``siderust`` crate at ``0.11.0``.
The first supported kernels route TAI split-Julian-date to TT split-Julian-date
conversion and a limited ICRS-to-AltAz coordinate transform through the native
extension when the Siderust backend is enabled.

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

Missing-feature inventory
=========================

Each Astropy subpackage has a missing-feature document under
``docs/siderust/missing/``. See ``docs/siderust/missing/README.md`` for the
index and status legend. Accelerated paths and known gaps for ``astropy.time``
and ``astropy.coordinates`` are documented in detail; other subpackages
describe why they remain on the upstream Astropy implementation path.

Inspect the live backend with:

.. code-block:: bash

    python -m astropy._siderust

Native extension development
============================

The private native extension is exposed as ``astropy._siderust._core`` and is
built through ``setuptools-rust`` using the PyO3 crate in
``crates/astropy-siderust``. The extension is intentionally small: it proves
that the repository can build, install, import, and call a native module from
the Astropy package tree, and it exposes the first time-scale and coordinate
kernels.

Development builds that include this native extension require a Rust toolchain.
The Python build dependency on ``setuptools-rust`` is declared in
``pyproject.toml``, so a normal editable install builds the extension:

.. code-block:: bash

    python -m pip install -e .

After installation, the native extension can be inspected with:

.. code-block:: bash

    python -c "import astropy._siderust._core as core; print(core.version())"
    python -c "from astropy._siderust import backend_info; print(backend_info())"
    python -c "from astropy._siderust import backend_status; print(backend_status())"

The top-level ``astropy`` import does not import the private native module
eagerly. The ``astropy._siderust`` helpers load ``astropy._siderust._core`` only
when diagnostics are requested.

Runtime backend selection is controlled by
``astropy._siderust.conf.backend_mode``. The accepted values are ``"auto"``,
``"off"``, and ``"on"``. Unsupported operations continue to use the existing
Astropy implementation.

The currently supported time kernel is ``time.tai_jd_to_tt_jd``. It is used by
``Time(..., scale="tai").tt`` for unmasked times when
``astropy._siderust.conf.backend_mode`` is ``"auto"`` or ``"on"`` and the
native extension is importable. The planned ``time.utc_jd_to_tai_jd`` kernel
remains unsupported until Siderust exposes a public UTC/TAI leap-second
conversion surface suitable for Astropy split Julian dates.

The currently supported coordinate kernel is ``coordinates.icrs_to_altaz``. It
is used for unit-spherical ICRS coordinates transformed to ``AltAz`` when
``pressure`` is zero, ``obstime`` and ``location`` are present, no coordinate
distance or differentials are attached, and the backend is ``"auto"`` or
``"on"``. Unsupported coordinate cases continue through Astropy's existing
ERFA-backed path. The first validation tests require agreement with current
Astropy behavior within 30 arcseconds for this narrow no-refraction route; the
tolerance must be tightened before presenting the transform as a high-precision
replacement.

The matching upstream FFI crate lives under ``siderust-ffi`` in
``Siderust/siderust.git`` and will be pinned when the first FFI-backed kernel
lands. The Python/Rust boundary contract is documented in
``docs/development/siderust_boundary.rst``. The Siderust pinning and local
override policy is documented in
``docs/development/siderust_dependency_strategy.rst``.

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

For siderust-py development, clone this repository and use the editable install
workflow described in `Native extension development`_.

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
