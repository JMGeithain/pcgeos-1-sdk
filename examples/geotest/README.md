# GEOTEST – German GeoWorks 1.2.8 target profile

This source-only example is an experimental first application for the German GeoWorks 1.2.8 installation. It is pinned to the four template hashes recorded in the development dossier.

## Prepare the target archive

From the SDK repository root:

```sh
python3 tools/prepare_geoworks_1_2_8_de.py /path/to/GEOWORKS.zip /tmp/GWP2-geoworks-1.2.8-de.zip
```

The script verifies the exact source members and SHA-256 hashes, writes a new temporary ZIP with the member paths expected by SDK 0.1, and never modifies the original archive.

## Build

```sh
./bin/pcgeos1 build examples/geotest/project.json --gwp /tmp/GWP2-geoworks-1.2.8-de.zip --toolchain gnu
```

`allow_unknown_target` is intentionally enabled only for this explicitly pinned experimental profile because the complete GEODE file hashes differ from the SDK 0.1 reference set. Do not use arbitrary target files with this project. The preparation script is the required gate.

The generated `.GEO` is derived from the user's GeoWorks templates. Do not redistribute it without checking the original software license. A successful host build does not prove that GeoWorks 1.2 will load or run the application; runtime testing in a disposable installation is still required.
