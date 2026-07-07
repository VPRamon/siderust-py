.. _siderust-dependency-strategy:

Siderust Dependency Strategy
===========================

The native extension currently builds the local PyO3 crate in
``crates/astropy-siderust`` and pins the published ``siderust`` crate to
``0.11.0``. The extension exposes dependency diagnostics, the first native time
kernel, ``time.tai_jd_to_tt_jd``, and the first native coordinate kernel,
``coordinates.icrs_to_altaz``.

Siderust's C ABI crate lives in the upstream ``Siderust/siderust.git``
repository under ``siderust-ffi``. At the time this policy was written, the
matching ``siderust-ffi`` crate for ``siderust`` ``0.11.0`` is present in that
repository but is not the default published crate used by Cargo. Real
FFI-backed Python kernels should therefore add ``siderust-ffi`` as a pinned git
dependency when the first kernel lands, rather than silently depending on an
older crates.io FFI package.

Default source
--------------

CI and release builds should use the crates.io ``siderust`` ``0.11.0`` release
for Rust API use. FFI use should be pinned to an exact upstream git revision of
``Siderust/siderust.git`` until a matching ``siderust-ffi`` release is available
on crates.io.

The pins belong in ``crates/astropy-siderust/Cargo.toml`` and the resolved
dependency graph belongs in ``Cargo.lock`` once the real Siderust dependency
graph is introduced.

The initial TAI-to-TT time kernel and the limited unit-spherical ICRS-to-AltAz
coordinate kernel use the public ``siderust`` Rust API from crates.io, so they
do not require ``siderust-ffi``. UTC-to-TAI remains planned rather than
supported because the leap-second-aware UTC/TAI conversion data is not currently
exposed through the public ``siderust`` or ``siderust-ffi`` surface in version
``0.11.0``.

The pin must be updated in a normal pull request that includes:

* the Siderust revision change;
* the resulting ``Cargo.lock`` update;
* parity tests for every Python path using Siderust;
* backend diagnostics showing the expected supported kernels.

Local development override
--------------------------

Developers may point Cargo at a sibling Siderust checkout while working on both
projects. Use Cargo's local override mechanism outside committed source files,
for example in ``.cargo/config.toml``:

.. code-block:: toml

    [patch.crates-io]
    siderust = { path = "../siderust" }

If the active work uses ``siderust-ffi`` from the upstream repository, use the
same local checkout for the git dependency:

.. code-block:: toml

    [patch."https://github.com/Siderust/siderust.git"]
    siderust-ffi = { path = "../siderust/siderust-ffi" }

Local overrides are for development only and should not be committed unless a
later repository policy explicitly adopts a workspace layout.

Network and wheel policy
------------------------

Normal CI and release builds should not rely on an unpinned branch or hidden
network state. A future wheel build should use the checked-in lockfile and build
from the pinned Siderust revision, or from a released crate version once that is
available.

Vendoring Siderust into this repository is not the default strategy. A submodule
or workspace member can be reconsidered later if CI reliability, release
process, or upstream Siderust packaging makes the pinned Cargo dependency
unworkable.
