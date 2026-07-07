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
primarily an Astropy fork. A minimal native-extension skeleton now exists under
``astropy._siderust`` so later issues can add real Siderust-backed kernels.

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

Kernel boundary contract
========================

The private Python/Rust boundary contract is documented in
`docs/siderust/kernel-boundary.rst <docs/siderust/kernel-boundary.rst>`_. The
contract defines the initial array data model, explicit units, optional-data
representation, error mapping, and NumPy broadcasting rules that Siderust-backed
kernels must follow.

Native extension development
============================

The private native skeleton is exposed as ``astropy._siderust._core`` and is
built through ``setuptools-rust`` using the PyO3 crate in
``crates/astropy-siderust``. This skeleton is intentionally small: it only
proves that the repository can build, install, import, and call a native module
from the Astropy package tree.

Development builds that include this native skeleton require a Rust toolchain.
The Python build dependency on ``setuptools-rust`` is declared in
``pyproject.toml``, so a normal editable install builds the extension:

.. code-block:: bash

    python -m pip install -e .

After installation, the native skeleton can be inspected with:

.. code-block:: bash

    python -c "import astropy._siderust._core as core; print(core.version())"
    python -c "from astropy._siderust import backend_info; print(backend_info())"

The top-level ``astropy`` import does not import the private native module
eagerly. The ``astropy._siderust`` helpers load ``astropy._siderust._core`` only
when diagnostics are requested.

The skeleton does not yet call the real Siderust library. That dependency and
the first scientific kernels are intentionally left to later tickets.

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
