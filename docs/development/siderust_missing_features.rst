.. _siderust-missing-features:

Siderust missing-feature inventory
==================================

siderust-py documents Astropy subpackages and operations that are not yet
delegated to the Siderust crate. The inventory lives in Markdown under
``docs/siderust/missing/``.

Start with the index:

* `docs/siderust/missing/README.md <../siderust/missing/README.md>`_

Detailed coverage for accelerated areas:

* `time.md <../siderust/missing/time.md>`_ — time-scale kernels and UTC/TAI blockers
* `coordinates.md <../siderust/missing/coordinates.md>`_ — frame transforms and planned paths

Each Astropy top-level subpackage has one file. Status values are documented in
the index README.

Kernel names in the inventory match ``KernelSpec.name`` entries in
``astropy/_siderust/boundary.py``. Run ``python -m astropy._siderust`` for live
backend diagnostics.
