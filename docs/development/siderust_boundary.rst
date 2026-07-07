.. _siderust-boundary:

Python/Rust Siderust Boundary
=============================

The private ``astropy._siderust`` boundary is the only intended interface
between Astropy-facing Python code and future Siderust kernels. Public Astropy
objects such as ``Time``, ``SkyCoord``, ``Quantity``, frames, locations, and
tables must be converted on the Python side before data crosses into Rust.

Boundary data model
-------------------

Native kernels receive plain NumPy-compatible numerical arrays or scalar values.
Each value has an explicit boundary unit in the kernel contract. Examples
include radians for angles, meters for distances, seconds for durations, and
Julian-date days for time values. Rust kernels must not infer units from Astropy
objects.

Optional inputs are represented as missing values at the boundary. For example,
observer height, distance, proper motion, or radial velocity may be omitted by
passing no array for that field. Missing optional values do not participate in
shape broadcasting.

Shape and broadcasting rules
----------------------------

The boundary follows NumPy broadcasting rules:

* scalar inputs have shape ``()`` and broadcast against arrays;
* vector inputs preserve their NumPy-compatible shape;
* mixed scalar/vector inputs broadcast to the common shape;
* incompatible shapes are rejected before calling Rust;
* optional inputs that are not present do not constrain the output shape.

Kernels should operate on batches. Python wrappers should normalize inputs once,
validate shapes once, and pass contiguous numerical buffers whenever a future
kernel requires that layout.

Initial kernel contracts
------------------------

No scientific Siderust kernel is registered as supported yet. The first planned
contracts are:

``time.utc_jd_to_tai_jd``
    Inputs: ``jd1`` in days and ``jd2`` in days. Output: ``tai_jd`` in days.

``coordinates.icrs_to_altaz``
    Inputs: ``ra`` in radians, ``dec`` in radians, ``obstime`` as Julian-date
    days, ``longitude`` in radians, ``latitude`` in radians, and optional
    ``height`` in meters. Outputs: ``az`` in radians and ``alt`` in radians.

Error handling
--------------

Python wrappers validate object types, units, missing required values, and
broadcast shapes before calling Rust. Rust kernels should return structured
errors for numerical domain failures or unsupported modes. Python wrappers are
responsible for converting those errors into the same exception style as the
existing Astropy path for that operation.
