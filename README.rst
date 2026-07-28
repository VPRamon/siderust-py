siderust-py
===========

``siderust-py`` is an experimental Python facade project whose long-term goal is
to expose a declared Astropy-compatible API while using the Siderust Rust
ecosystem as the sole scientific implementation for every supported operation.

The project is not an optional acceleration backend for Astropy. Python owns the
compatibility layer; Rust owns the scientific semantics.

Project charter
===============

For an API declared supported, the production execution path is:

1. a user calls an Astropy-compatible Python API;
2. Python validates facade-level behaviour and marshals array/object structure;
3. the PyO3/NumPy boundary passes primitive buffers, identifiers, masks, and
   explicit context metadata into Rust;
4. a public Siderust-ecosystem API performs the complete scientific operation;
5. Python reconstructs the compatible result object.

A supported operation must not silently fall back to Astropy, ERFA, Python,
Cython, or a second scientific implementation in the binding crate. When an API
is outside the active compatibility profile, it must be reported as unsupported
and fail explicitly.

The authoritative product program is tracked in
`GitHub issue #26 <https://github.com/VPRamon/siderust-py/issues/26>`_. The
dependency-ordered implementation plan is tracked in
`GitHub issue #253 <https://github.com/VPRamon/siderust-py/issues/253>`_.

Responsibility split
====================

Python facade responsibilities
------------------------------

Python may own:

* Astropy-compatible import paths, signatures, constructors, and properties;
* facade-level argument normalization and object-shape validation;
* indexing, reshaping, representation, formatting, warnings, and exceptions;
* NumPy/PyO3 marshaling and reconstruction of Python result objects;
* explicit capability and compatibility diagnostics.

Python and the binding crate must not own astronomical formulas, physical-unit
conversion rules, time-scale semantics, coordinate transformations, scientific
model selection, ephemeris interpretation, atmospheric corrections, or
per-element scientific loops.

Rust responsibilities
---------------------

The Siderust Rust ecosystem owns:

* scientific algorithms and numerical models;
* units, quantities, equivalencies, constants, and their provenance;
* time representations, scale conversion, leap seconds, and EOP semantics;
* coordinate representations, frame transformations, Earth orientation,
  ephemerides, atmospheric effects, and planning calculations;
* scalar and batch execution;
* structured scientific errors;
* scientific-data contexts, validity ranges, and provenance;
* authoritative Rust tests and benchmarks.

Scientific capabilities must be exposed through public Rust APIs that remain
useful independently of Python.

Compatibility policy
====================

Compatibility claims are bounded by named, versioned profiles. A profile records
the supported public symbols and their signatures, defaults, result types,
units, shapes, broadcasting, masks, warnings, exceptions, numerical tolerances,
models, and required data.

Each API is classified as one of:

``supported``
    The complete scientific operation is Rust-owned and the facade behaviour is
    covered by the compatibility and validation suites.

``experimental``
    The operation is available for evaluation but is not part of a stable
    compatibility guarantee. It still must not use a silent production fallback.

``unsupported``
    The facade fails explicitly. Unsupported APIs are not delegated to Astropy
    at runtime.

Astropy is a pinned development and conformance oracle. It may be used to
inventory APIs, generate fixtures, compare behaviour, and run benchmarks in
test-only environments. It is not the production scientific backend.

Current status
==============

This repository is still an Astropy-derived compatibility laboratory. A minimal
native-extension skeleton exists under ``astropy._siderust`` and historical
bootstrap work may still contain optional-backend assumptions.

That transitional code does not define the target architecture. New work must
follow the charter above. The copied Astropy tree will be removed from the
supported product after the standalone facade, tests, documentation, and
required compatibility behaviour have been extracted.

The previous optional-backend program is preserved for historical context in
`GitHub issue #1 <https://github.com/VPRamon/siderust-py/issues/1>`_, which is
closed and superseded by issue #26.

Initial product sequence
========================

The first stable product is a core-astrometry compatibility profile. Work is
ordered broadly as follows:

1. freeze the product, compatibility, namespace, and licensing contracts;
2. extract a standalone facade and make Astropy test-only;
3. build the reusable NumPy/PyO3 and public Rust API foundations;
4. deliver units, quantities, constants, ``Time``, and ``TimeDelta``;
5. deliver coordinate representations, frames, ``EarthLocation``, and
   ``SkyCoord``;
6. complete Earth orientation and observed astrometry;
7. publish reproducible core-astrometry wheels with scientific evidence;
8. add solar-system ephemerides and observation-planning profiles;
9. expand into separately scoped domains such as WCS or cosmology.

The ordered milestone gates and their issue dependencies are maintained in
`the roadmap issue <https://github.com/VPRamon/siderust-py/issues/253>`_.

Kernel boundary contract
========================

The private Python/Rust boundary contract is documented in
`docs/siderust/kernel-boundary.rst <docs/siderust/kernel-boundary.rst>`_. The
authoritative ownership and fallback policy is documented in
`docs/siderust/project-charter.rst <docs/siderust/project-charter.rst>`_.

Native extension development
============================

The current private native skeleton is exposed as ``astropy._siderust._core`` and
is built through ``setuptools-rust`` using the PyO3 crate in
``crates/astropy-siderust``. This location is transitional and will be replaced
by the standalone package architecture.

Development builds that include the native skeleton require a Rust toolchain.
The Python build dependency on ``setuptools-rust`` is declared in
``pyproject.toml``, so an editable install builds the extension:

.. code-block:: bash

    python -m pip install -e .

After installation, the current skeleton can be inspected with:

.. code-block:: bash

    python -c "import astropy._siderust._core as core; print(core.version())"
    python -c "from astropy._siderust import backend_info; print(backend_info())"

These commands describe the bootstrap implementation, not the final public
namespace or backend-selection policy.

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

The repository currently contains Astropy-derived code under Astropy's
3-clause BSD-style license; see `LICENSE.rst <LICENSE.rst>`_ and the files under
``licenses/``. The licensing model for the standalone distribution and its
linked Siderust dependencies is a tracked program decision and must be resolved
before public binary releases.

Installation
============

This repository is not yet a stable public replacement for Astropy. For normal
Astropy usage, install upstream Astropy from PyPI:

.. code-block:: bash

    pip install astropy

For ``siderust-py`` development, clone this repository and use the editable
installation workflow described in `Native extension development`_.

Contributing
============

Contributions must follow the project charter and be linked to the roadmap.
Scientific formulas, model choices, data interpretation, and batch loops belong
in the owning Rust repository. Python changes should implement compatibility and
marshaling around an existing public Rust capability.

Small, reviewable pull requests should identify:

* the compatibility-profile effect;
* the owning Rust API or upstream issue;
* scientific references and data dependencies;
* scalar, array, mask, and broadcasting behaviour;
* validation and performance evidence;
* any intentional difference from the pinned Astropy reference.

Security note
=============

Do not accept code, patches, or build artifacts through ZIP files or opaque
attachments in issues. Proposed changes should arrive through normal pull
requests with source diffs, tests, and reviewable explanations.
