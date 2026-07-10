# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Command-line backend diagnostics for the Siderust integration."""

from __future__ import annotations

import json
import sys

from astropy._siderust import backend_status


def main(argv: list[str] | None = None) -> int:
    """Print Siderust backend status as JSON."""

    if argv is None:
        argv = sys.argv[1:]

    if argv not in ([], ["--help"], ["-h"]):
        print("usage: python -m astropy._siderust", file=sys.stderr)
        return 2

    if argv:
        print("Print Siderust backend diagnostics as JSON.")
        return 0

    print(json.dumps(backend_status(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
