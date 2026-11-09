#!/usr/bin/env python3
"""Create a temporary SDK target archive from the verified German GeoWorks 1.2.8 set.

The input archive is never modified. Only the four native SDK template geodes are
copied to the member paths expected by pcgeos1/target.py. This profile is pinned
to the exact SHA-256 values recorded in docs/GEOTEST_DEVELOPMENT_LOG.md.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

SOURCES = {
    "GEOWORKS/WORLD/PROGRAMM.E/SPINTEXT.GEO": "GEOWORKS/WORLD/EXTRAS/SPINTEXT.GEO",
    "GEOWORKS/WORLD/NOTEPAD.GEO": "GEOWORKS/WORLD/NOTEPAD.GEO",
    "GEOWORKS/WORLD/VIEWER.GEO": "GEOWORKS/WORLD/VIEWER.GEO",
    "GEOWORKS/WORLD/TERM.GEO": "GEOWORKS/WORLD/TERM.GEO",
}
EXPECTED = {
    "GEOWORKS/WORLD/PROGRAMM.E/SPINTEXT.GEO": "18f2075c9d61fe7231b1dacae8c171e68c2028ef2fca6d40a6694158fdfcb9fd",
    "GEOWORKS/WORLD/NOTEPAD.GEO": "a1ebd0cb84712a126b1f67f5fd1ca6b57f8bda2e9038e9224ba16ebc008f9ea9",
    "GEOWORKS/WORLD/VIEWER.GEO": "c884b76cdc4f9119d4794f7830d5438e0abcc1d92d3cc248aa912bde85ed43e7",
    "GEOWORKS/WORLD/TERM.GEO": "a62ebc0fb3c01acb4b59c8172d20d520653822a6d42f0bec4831dfdb93e1cf3a",
}

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path, help="original GEOWORKS.zip")
    p.add_argument("output", type=Path, help="new normalized temporary target ZIP")
    args = p.parse_args()
    if args.input.resolve() == args.output.resolve():
        p.error("input and output must be different files; the original is never overwritten")
    manifest = {}
    with zipfile.ZipFile(args.input, "r") as zin:
        names = set(zin.namelist())
        selected = {}
        for source, target in SOURCES.items():
            if source not in names:
                raise SystemExit(f"Missing required archive member: {source}")
            data = zin.read(source)
            actual = digest(data)
            expected = EXPECTED[source]
            if actual != expected:
                raise SystemExit(f"Unexpected SHA-256 for {source}: {actual}; expected {expected}")
            selected[target] = data
            manifest[target] = {"source": source, "bytes": len(data), "sha256": actual}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for target, data in selected.items():
            zout.writestr(target, data)
    print(json.dumps({"profile": "geoworks-1.2.8-de", "input": str(args.input),
                      "output": str(args.output), "original_modified": False,
                      "templates": manifest}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
