Siderust kernel boundary contract
=================================

Status
------

This document defines the private Python/Rust boundary contract for
``siderust-py``. It implements the ownership rules in
`project-charter.rst <project-charter.rst>`_.

The boundary is not a public user API. Public users interact with facade objects
that follow the declared Astropy-compatible profile, such as ``Time``,
``SkyCoord``, ``EarthLocation``, and frame objects. Python converts object
structure into compact buffers and metadata; public Rust APIs own the complete
scientific operation.

Goals
-----

The boundary is designed to:

* avoid passing Python or Astropy objects into Rust;
* minimize Python object churn in hot paths;
* support scalar, vector, multidimensional, and broadcast inputs;
* make units, frames, scales, models, and data contexts explicit;
* represent optional astronomical data without confusing ``missing`` with a
  physical zero;
* execute one Rust batch operation per logical facade operation;
* keep shape, mask, status, and error behaviour predictable;
* prevent a silent production fallback for APIs declared supported.

Non-goals
---------

This contract does not define scientific formulas, scientific model selection,
or a stable public Python API. It also does not authorize the binding crate to
reimplement science that belongs in ``Siderust/qtty``, ``Siderust/tempoch``,
``Siderust/siderust``, or another owning Rust crate.

Private names may change while these ownership and transport rules remain
stable.

Data model
----------

Native kernels receive compact primitive buffers and explicit metadata:

* ``float64`` NumPy-compatible arrays for continuous values;
* integer arrays or scalar tags for closed identifiers such as time scales,
  frames, units, models, and status codes;
* boolean masks or status arrays when missing/invalid state cannot be represented
  safely by a numeric sentinel;
* immutable or safely shared context handles for scientific datasets;
* no ``Time``, ``SkyCoord``, ``Quantity``, frame, table, or unit Python objects.

The Python adapter extracts facade object structure and passes it through the
native boundary. Unit conversion, time interpretation, frame transformation,
model selection, and other scientific semantics are performed by public Rust
APIs. Python reconstructs the declared compatible result objects.

Array layout
------------

The boundary accepts NumPy-compatible buffers with an explicit dtype, shape, and
stride/contiguity contract.

The initial implementation may normalize supported floating-point inputs to
C-contiguous ``float64`` arrays. Scalars are represented as zero-dimensional
arrays on the Python side and may be flattened with shape metadata for the
native call.

Native code must not rely on Python object iteration, Python dtype inference, or
Python-owned scientific conversion logic.

Shape and broadcasting rules
----------------------------

The facade follows the broadcasting behaviour declared by the active
compatibility profile.

* Every input has a shape. A scalar has shape ``()``.
* The logical batch shape is computed from the declared broadcasting rules.
* Inputs are exposed to Rust as validated views or normalized buffers.
* Outputs use the logical batch shape unless the kernel documents an additional
  component axis.
* Incompatible shapes fail before scientific execution.
* A kernel must not silently zip arrays of unrelated lengths.
* Python must call the Rust batch API once per logical operation, not once per
  scalar element.

Examples:

* scalar time with vector coordinates broadcasts to the coordinate shape;
* vector time with scalar observer location broadcasts to the time shape;
* target shape ``(n_targets, 1)`` with time shape ``(n_times,)`` broadcasts to
  ``(n_targets, n_times)``;
* shape ``(2,)`` with shape ``(3,)`` is invalid unless the public API declares a
  different combination rule.

Optional and invalid data
-------------------------

Missing values, masks, and scientific failures are distinct concepts.

* A Python mask is transported explicitly when the compatibility profile
  supports masked input.
* Physical zero remains ``0.0`` and is never treated as missing.
* ``NaN`` may be used only where the kernel contract explicitly defines it as a
  missing or invalid sentinel.
* Per-element scientific status is returned through a documented status buffer
  when partial batch success is supported.
* Whole-operation errors return no partial result.
* Unknown, unavailable, stale, and out-of-range scientific data have distinct
  structured error/status semantics.

Error handling
--------------

Python validates facade-level concerns before entering Rust:

* required Python attributes and arguments are present;
* inputs can be exposed through the declared buffer/dtype protocol;
* shapes are structurally compatible;
* masks and optional values use supported representations;
* public identifiers are syntactically valid.

Rust validates scientific concerns:

* units and dimensions are compatible;
* frames, scales, centers, and model combinations are valid;
* physical domains are valid;
* required scientific data is available and in range;
* numerical methods converge.

Rust returns structured errors that Python maps to stable exception classes.
Rust panics must not cross the language boundary.

Initial kernel contracts
------------------------

The following families describe the first intended boundary shapes. They are
private transport contracts, not permission to implement the corresponding
science in Python or PyO3.

Time scale conversion
~~~~~~~~~~~~~~~~~~~~~

Purpose:
    Convert a batch of precision-preserving split Julian dates between supported
    time scales through a public ``Siderust/tempoch`` API.

Inputs:
    ``jd1_days``
        ``float64`` array. First part of the input Julian date, in days.
    ``jd2_days``
        ``float64`` array. Second part of the input Julian date, in days.
    ``input_scale``
        Stable scale identifier.
    ``output_scale``
        Stable scale identifier.
    ``time_context``
        Explicit context identifier/handle for leap-second and EOP data when
        required.

Outputs:
    ``out_jd1_days``
        ``float64`` array, same logical batch shape.
    ``out_jd2_days``
        ``float64`` array, same logical batch shape.
    ``status``
        Optional per-element status according to the profile contract.

Observed-coordinate batch
~~~~~~~~~~~~~~~~~~~~~~~~~

Purpose:
    Compute a target/time/observer batch through public Siderust coordinate and
    observed-astrometry APIs.

Inputs include:

* target direction or position buffers with explicit frame metadata;
* precision-preserving observation-time buffers and time-scale identifiers;
* observer location buffers with an explicit terrestrial model;
* optional motion/distance/radial-velocity buffers and masks;
* explicit Earth-orientation, ephemeris, atmosphere, and model contexts.

Outputs include:

* coordinate component buffers in the requested output frame;
* explicit output metadata;
* optional per-element status according to the profile contract.

Python/Rust responsibility split
--------------------------------

Python responsibilities:

* accept and expose the declared facade objects;
* validate Python-level structure and buffer compatibility;
* compute or validate the declared logical broadcast shape;
* expose masks, identifiers, and contiguous/strided buffers safely;
* call one native batch function per logical operation;
* reconstruct compatible result objects;
* map structured Rust errors to stable Python exceptions.

Rust responsibilities:

* validate scientific units, domains, frames, scales, centers, models, and data;
* perform all unit conversion and scientific computation;
* execute scalar and batch algorithms;
* reuse prepared scientific contexts across batches;
* return primitive/typed result buffers, metadata, status, and structured errors;
* remain independently usable and tested from Rust.

Testing rule
------------

Every supported boundary operation includes tests for:

* scalar, vector, and multidimensional input;
* mixed scalar/array broadcasting;
* incompatible shape and dtype validation;
* masks, missing values, physical zero, and partial-status behaviour;
* error and panic isolation;
* explicit unit, frame, scale, model, and data-context metadata;
* scalar-versus-batch scientific equivalence;
* proof that the facade makes one Rust call per logical batch;
* proof that no supported production path imports or calls Astropy/ERFA as a
  fallback.
