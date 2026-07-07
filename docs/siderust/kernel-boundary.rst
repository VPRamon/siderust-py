Siderust kernel boundary contract
=================================

Status
------

This document defines the first Python/Rust boundary contract for
``siderust-py``. It is an internal implementation contract, not a public user
API. Public users should continue to interact with Astropy-facing objects such
as ``Time``, ``SkyCoord``, ``EarthLocation``, and frame objects. Python is
responsible for normalizing those objects into compact numerical arrays before
calling native Siderust kernels.

Goals
-----

The boundary is designed to:

* avoid passing Astropy objects into Rust;
* minimize Python object churn in hot paths;
* support scalar, vector, and mixed scalar/vector inputs;
* make units explicit at every native entry point;
* represent optional astronomical data without confusing ``missing`` with a
  physical zero;
* allow batch execution over contiguous numerical buffers;
* keep shape and error behavior predictable for facade-level tests.

Non-goals
---------

This contract does not implement scientific kernels. It also does not define a
stable public Python API. Later tickets may revise private names while keeping
these semantic rules intact.

Data model
----------

Native kernels should receive only compact primitive values:

* ``float64`` NumPy-compatible arrays for continuous quantities;
* integer arrays or scalar integer tags for closed enums, such as time scales or
  frame identifiers;
* boolean masks only when a missing-value sentinel is insufficient;
* no ``Time``, ``SkyCoord``, ``Quantity``, frame, table, or unit objects.

Python-side adapter code must convert public Astropy objects into this boundary
format before crossing into Rust. Rust-side code should operate on homogeneous
buffers and return homogeneous buffers. The Python side is responsible for
reconstructing Astropy-compatible result objects.

Array layout
------------

Before calling Rust, Python should coerce floating-point inputs to C-contiguous
``float64`` arrays. Scalars are represented as zero-dimensional arrays on the
Python side and may be flattened with shape metadata for FFI calls. Native code
should not rely on Python object iteration, dtype inference, or unit conversion.

Shape and broadcasting rules
----------------------------

The boundary follows NumPy broadcasting semantics.

* Every input has a shape. A scalar has shape ``()``.
* The kernel batch shape is ``numpy.broadcast_shapes`` over all non-optional or
  explicitly supplied input shapes.
* Inputs are broadcast to the batch shape before crossing the Rust boundary.
* Outputs use the same batch shape unless the kernel explicitly documents an
  extra trailing component axis.
* Incompatible shapes are validation errors and must fail before entering Rust.
* A kernel must not silently zip arrays of different lengths.

Examples:

* scalar time with vector coordinates broadcasts to the coordinate vector shape;
* vector time with scalar observer location broadcasts to the time vector shape;
* target shape ``(n_targets, 1)`` with time shape ``(n_times,)`` broadcasts to
  ``(n_targets, n_times)``;
* shape ``(2,)`` with shape ``(3,)`` is invalid unless one side is explicitly
  reshaped by Python first.

Optional data
-------------

Optional floating-point astronomical data is represented as a ``float64`` array
with the same batch shape as the kernel inputs.

* Missing proper motion, distance, parallax, radial velocity, pressure, or
  wavelength is represented by ``NaN``.
* Physical zero remains ``0.0`` and must not be used as a missing-value marker.
* Optional observer height defaults to ``0.0`` meters only when the public
  Astropy-facing object semantically means geodetic height zero. If the height
  is unknown, use ``NaN`` instead.
* If a later kernel needs to distinguish several missing reasons, add an
  explicit integer status or boolean mask array rather than overloading a
  numeric value.

Error handling
--------------

The Python adapter should validate the following before calling Rust:

* input values are convertible to the required primitive dtype;
* units have been converted to the documented boundary units;
* shapes are broadcast-compatible;
* enum values are known;
* required arrays do not contain unsupported missing values.

Validation failures should raise ``TypeError`` for non-numeric/non-convertible
inputs and ``ValueError`` for invalid shapes, invalid enum values, or invalid
physical domains.

Rust kernels should return structured errors that Python maps to standard
exceptions. A whole-kernel failure should not return partial outputs. Per-element
invalid physical results may be represented by ``NaN`` plus a documented status
array when that is scientifically meaningful.

Initial kernel contracts
------------------------

These are the initial private kernel families the boundary is expected to
support. Names are descriptive placeholders, not final public API.

Time scale conversion kernel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Purpose:
    Convert a batch of split Julian dates between supported time scales.

Inputs:
    ``jd1_days``
        ``float64`` array. First part of the input Julian date, in days.
    ``jd2_days``
        ``float64`` array. Second part of the input Julian date, in days.
    ``input_scale``
        Scalar integer enum. Input time scale.
    ``output_scale``
        Scalar integer enum. Output time scale.
    ``delta_ut1_utc_s``
        Optional ``float64`` array, seconds. Required only for conversions that
        need UT1-UTC.

Outputs:
    ``out_jd1_days``
        ``float64`` array, same batch shape, first part of the output Julian
        date in days.
    ``out_jd2_days``
        ``float64`` array, same batch shape, second part of the output Julian
        date in days.

Coordinate planning kernel
~~~~~~~~~~~~~~~~~~~~~~~~~~

Purpose:
    Compute a batch planning-oriented ICRS-to-observed-horizontal transform for
    a target/time/observer grid after Python has normalized Astropy objects.

Inputs:
    ``ra_rad``
        ``float64`` array. ICRS right ascension, radians.
    ``dec_rad``
        ``float64`` array. ICRS declination, radians.
    ``obstime_jd1_utc_days`` and ``obstime_jd2_utc_days``
        ``float64`` arrays. Observation time as split UTC Julian date, days.
    ``observer_lon_rad_east``
        ``float64`` array. Geodetic longitude, radians, positive east.
    ``observer_lat_rad``
        ``float64`` array. Geodetic latitude, radians.
    ``observer_height_m``
        ``float64`` array. Geodetic height above reference ellipsoid, meters.
    ``pm_ra_cosdec_rad_per_yr``
        Optional ``float64`` array. Proper motion in RA*cos(dec), radians per
        Julian year.
    ``pm_dec_rad_per_yr``
        Optional ``float64`` array. Proper motion in declination, radians per
        Julian year.
    ``distance_m``
        Optional ``float64`` array. Barycentric distance, meters.
    ``radial_velocity_m_per_s``
        Optional ``float64`` array. Radial velocity, meters per second.

Outputs:
    ``az_rad``
        ``float64`` array, same batch shape. Azimuth, radians.
    ``alt_rad``
        ``float64`` array, same batch shape. Altitude, radians.

Python/Rust responsibility split
--------------------------------

Python responsibilities:

* accept Astropy-facing public objects;
* perform unit conversion into documented boundary units;
* compute the broadcast batch shape;
* broadcast and make arrays C-contiguous;
* represent missing optional data consistently;
* call the native function once per batch, not once per scalar element;
* reconstruct Astropy-compatible outputs.

Rust responsibilities:

* assume validated primitive buffers;
* avoid Python object interaction in hot loops;
* compute over the supplied batch shape;
* return primitive buffers and structured errors;
* not silently reinterpret units or shapes.

Testing rule
------------

Any future kernel added to this boundary must include tests that cover:

* scalar-only input;
* vector input;
* mixed scalar/vector broadcasting;
* incompatible-shape validation;
* optional data missing by ``NaN``;
* optional physical zero preserved as ``0.0``;
* explicit input and output units in the test name, fixture, or docstring.
