# Target Compatibility

SDK 0.1 uses explicit, hash-pinned target profiles. The default remains the original GeoWorks Pro 1.2 reference set.

## Required native interface

- GEOS 1.x executable format
- kernel protocol: `622.3`
- UI library protocol: `693.0`
- basic application skeleton: `SPINTEXT.GEO`

## Exact template hashes

| File | SHA-256 |
|---|---|
| SPINTEXT.GEO | `848f5afb43a2184b01d2a4ad3231957b6ab9936006b23b4b2a260d1224d44370` |
| NOTEPAD.GEO | `edc48848ff4b9d2880e715bbb29532f14b3b54293c45159c467e33e2af841d1b` |
| VIEWER.GEO | `3d433a39c455a9cea242763dad0e3f681b4196fb7b1a75a08ca47e1aa8aa4a30` |
| TERM.GEO | `2d66ac2ff9fd24c4591303b2cba7cec6f40f0d52b4f3d75d9e0cdaa5fc1be542` |

The generic basic-view build currently requires all four hashes even though it directly consumes only SPINTEXT and VIEWER. This is intentional: the target set is treated as a coherent known distribution.

## Registered profiles

The default project profile is `geoworks-pro-1.2`; projects without `target_profile` retain the original strict hash set. The experimental German GeoWorks 1.2.8 profile is selected explicitly with `target_profile: geoworks-1.2.8-de` and verifies these four hashes before compilation:

| File | SHA-256 |
|---|---|
| SPINTEXT.GEO | `18f2075c9d61fe7231b1dacae8c171e68c2028ef2fca6d40a6694158fdfcb9fd` |
| NOTEPAD.GEO | `a1ebd0cb84712a126b1f67f5fd1ca6b57f8bda2e9038e9224ba16ebc008f9ea9` |
| VIEWER.GEO | `c884b76cdc4f9119d4794f7830d5438e0abcc1d92d3cc248aa912bde85ed43e7` |
| TERM.GEO | `a62ebc0fb3c01acb4b59c8172d20d520653822a6d42f0bec4831dfdb93e1cf3a` |

The former `allow_unknown_target=true` bypass is rejected. Projects select a named profile; they cannot supply arbitrary trusted hashes.

## Adding another target

To add a target properly:

1. scan every geode and record kernel/UI protocols;
2. identify native applications that contain the required object types;
3. recover exact object chunks and hints;
4. verify superclass/message behavior;
5. add target-specific hashes and tests;
6. keep target profiles separate if layouts differ.
