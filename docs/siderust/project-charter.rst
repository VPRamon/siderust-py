Project charter
===============

Status
------

This document is the authoritative architecture charter for ``siderust-py``.
The product program is tracked in
`issue #26 <https://github.com/VPRamon/siderust-py/issues/26>`_, and its ordered
milestones are tracked in
`issue #253 <https://github.com/VPRamon/siderust-py/issues/253>`_.

Goal
----

Build a production-quality Python package that exposes a declared,
versioned Astropy-compatible API while delegating every supported scientific
operation to public APIs in the Siderust Rust ecosystem.

``siderust-py`` is not an Astropy fork with an optional Rust accelerator.
Python owns compatibility behaviour. Rust owns scientific behaviour.

Required execution path
-----------------------

For every operation declared ``supported``:

1. the user calls an Astropy-compatible Python API;
2. the facade validates Python-level structure and marshals inputs;
3. PyO3 passes primitive buffers and explicit metadata into Rust;
4. a public Rust API performs the complete scientific operation;
5. the facade reconstructs the compatible Python result.

The production path must not silently execute Astropy, ERFA, Cython, Python
scientific code, or an independent scientific implementation in the PyO3 crate.

Unsupported operations fail explicitly. They are not rescued by a hidden
fallback.

Ownership boundaries
--------------------

Python facade
~~~~~~~~~~~~~

Python may own:

* public import paths and signatures;
* constructors, properties, indexing, reshaping, formatting, and representation;
* facade-level type and shape validation;
* warnings and stable Python exception classes;
* NumPy/PyO3 marshaling;
* result-object construction;
* compatibility and capability diagnostics.

Python must not own:

* astronomical or physical formulas;
* unit conversion or equivalency rules;
* time-scale or leap-second semantics;
* coordinate or reference-frame transformations;
* model selection;
* ephemeris, Earth-orientation, or atmospheric interpretation;
* per-element scientific execution loops.

PyO3 boundary
~~~~~~~~~~~~~

The binding layer may own language interoperation only:

* safe buffer access;
* dtype, shape, and mask transport;
* stable identifier mapping;
* GIL and thread-safety management;
* conversion between structured Rust errors and Python exceptions.

The binding layer must call public Rust APIs. It must not become a second
scientific library.

Rust ecosystem
~~~~~~~~~~~~~~

The owning Rust repositories implement and validate the science:

* ``Siderust/qtty`` owns units, quantities, equivalencies, and constants;
* ``Siderust/tempoch`` owns time representations, time-scale conversion, leap
  seconds, EOP-backed time semantics, and duration arithmetic;
* ``Siderust/siderust`` owns astronomy orchestration, coordinates, frames,
  Earth orientation, ephemerides, atmospheric effects, and planning;
* future specialized Rust crates may own bounded domains such as WCS or
  cosmology.

A public Rust capability must remain useful and tested independently of Python.

Compatibility contract
----------------------

Compatibility is defined by named, versioned profiles rather than a blanket
claim of complete Astropy replacement.

The canonical profile manifest records, at minimum:

* symbol and import path;
* signature and defaults;
* accepted inputs and result objects;
* units, shapes, broadcasting, masks, and dtypes;
* exceptions, warnings, and unsupported conditions;
* Rust implementation owner and kernel identifier;
* numerical tolerance and approved model differences;
* scientific-data requirements and validity ranges.

An operation cannot be marked supported until its Rust implementation,
Rust-side scientific validation, facade conformance tests, and documentation are
complete.

Astropy policy
--------------

Astropy is a pinned test-only conformance oracle. It may be used to:

* inventory the selected reference API;
* generate or compare fixtures;
* run differential behaviour tests;
* benchmark equivalent public workflows;
* identify API drift in later Astropy releases.

Astropy is not a production dependency or fallback for supported operations.

Migration policy
----------------

The repository currently contains an Astropy-derived tree and bootstrap code
built around optional backend dispatch. That code is transitional.

During migration:

* legacy code may remain temporarily while behaviour and tests are extracted;
* legacy paths must not be promoted as the target architecture;
* new supported capabilities follow this charter;
* copied Astropy modules are removed after their required facade behaviour,
  tests, and documentation are preserved;
* historical bootstrap issues remain linked for traceability.

The original optional-backend story is preserved in
`issue #1 <https://github.com/VPRamon/siderust-py/issues/1>`_. It is closed and
superseded by the product program in issue #26.

Non-goals
---------

This charter does not require:

* implementing every Astropy module in the first release;
* rewriting non-scientific Python infrastructure in Rust for language purity;
* claiming exact numerical identity when an approved, documented scientific
  model differs;
* preserving Astropy private internals;
* hiding unsupported APIs behind fallback behaviour.

Enforcement
-----------

Architecture and conformance tests should prevent:

* production imports of Astropy or ERFA from supported paths;
* scientific formulas in Python or PyO3 code;
* Python loops invoking scalar Rust kernels for logical batches;
* manifest entries marked supported without a compiled Rust capability;
* undocumented model, data, or numerical changes.

Pull requests that add supported behaviour must identify the owning Rust API,
compatibility-profile change, validation evidence, and any intentional
difference from the pinned Astropy reference.
