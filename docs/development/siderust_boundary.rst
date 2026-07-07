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

Kernel contracts
----------------

The first supported Siderust kernels are:

``time.tai_jd_to_tt_jd``
    Inputs: ``jd1`` in days and ``jd2`` in days. Outputs: ``tt_jd1`` and
    ``tt_jd2`` in days. This kernel backs ``Time(..., scale="tai").tt`` for
    unmasked times when the Siderust backend is enabled.

``coordinates.icrs_to_altaz``
    Inputs: ``ra`` in radians, ``dec`` in radians, ``obstime_tt_jd`` as a TT
    Julian-date day, ``longitude`` in radians, ``latitude`` in radians, and
    optional ``height`` in meters. Outputs: ``az`` in radians and ``alt`` in
    radians. This kernel backs unit-spherical ICRS to no-refraction ``AltAz``
    transforms when the coordinate has no distance or differentials and the
    target frame has both ``obstime`` and ``location``.

Unsupported coordinate variants fall back to the existing Astropy path. The
first coordinate validation tolerance is 30 arcseconds against current Astropy
behavior for the supported no-refraction route. This is a bootstrap tolerance,
not a precision target for future high-accuracy coordinate kernels.

The first planned contract is:

``time.utc_jd_to_tai_jd``
    Inputs: ``jd1`` in days and ``jd2`` in days. Output: ``tai_jd`` in days.

Error handling
--------------

Python wrappers validate object types, units, missing required values, and
broadcast shapes before calling Rust. Rust kernels should return structured
errors for numerical domain failures or unsupported modes. Python wrappers are
responsible for converting those errors into the same exception style as the
existing Astropy path for that operation.
