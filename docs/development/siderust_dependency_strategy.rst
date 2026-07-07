.. _siderust-dependency-strategy:

Siderust Dependency Strategy
===========================

The native extension currently builds only the local PyO3 skeleton in
``crates/astropy-siderust``. It does not depend on the real Siderust crate yet.
When scientific kernels are added, the Python package should consume Siderust
from a deterministic Rust dependency.

Default source
--------------

CI and release builds should use a pinned Siderust git revision until Siderust
has a released crate suitable for this package. The pin belongs in
``crates/astropy-siderust/Cargo.toml`` and the resolved dependency graph belongs
in ``Cargo.lock`` once the real Siderust dependency is introduced.

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

    [patch."https://github.com/VPRamon/siderust"]
    siderust = { path = "../siderust" }

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
