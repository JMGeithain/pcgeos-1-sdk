# GEOTEST 1.x – program icon and document-icon research

## Application icon

The GEOTEST application carries token `GTS1` and manufacturer ID `0` in its GEODE header. Its program icon is handled through the GeoWorks 1.x token mechanism; it is not a PCX file appended to the executable.

The user's original 48×30, 16-color PCX was converted with ICONMAKE in a separate test setup. A fresh TOKEN.DB displayed the newly generated icon. An older TOKEN.DB continued to show its cached icon, demonstrating that token database state affects the visible result. Do not delete or replace a production TOKEN.DB without a backup.

## Separate test-document icon concept

Two matching 48×30 test-document graphics were prepared: a color version and a monochrome version. The motif is a test-screen monitor on a symbolic stack of two sheets. They are design inputs, not yet verified native GeoWorks VisMonikers or a complete document-type implementation.

The intended separation is:
- `GTS1`: GEOTEST application token, manufacturer ID 0.
- a future document/icon-provider token: not yet selected or validated.
- a future GEOS document file type: not yet selected or validated.

Do not assume that `GTD1` or the extension `.GTD` is correct. The original GeoWorks archive documents a historical icon-provider mechanism; see [the archive audit](ICONDB1.TXT).

## Findings from the original GeoWorks 1.2 archive

The user's supplied `GEOWORKS.zip` contains:
- `GEOWORKS/ICONS/ICONINST.TXT`
- `GEOWORKS/ICONS/DOS_ICON.TXT`
- icon-provider applications `PAPR.000`, `GDOC.000`, and `NBAT.000`
- GEOS data files named `TESTICON.000`

The original `ICONINST.TXT` explains that the icon-provider files are small PC/GEOS applications and that their four-character filename stem is the token name. The supplied provider mappings use manufacturer ID 255. Existing system tokens in the same example use manufacturer ID 0.

The original `DOS_ICON.TXT` identifies the GEOS header fields:
- file type at offset `0x14`;
- creator at offset `0x1A`;
- long filename beginning at offset `0x20`.

The actual sample headers confirm that `PAPR.000`, `GDOC.000`, and `NBAT.000` are provider applications with creator `GEOS`, while `TESTICON.000` is a data file with type `Icon` and creator `GEOS`. These are distinct mechanisms.

## Current status

- Application token `GTS1`: established.
- Original provider-token mechanism: documented by the supplied GeoWorks 1.2 files.
- Candidate document token `GTD1`: unverified; not adopted.
- Candidate file extension `.GTD`: unverified; not adopted.
- Color and monochrome document artwork: prepared as 48×30 PNG/PCX test inputs in the working conversation, but not yet verified by ICONMAKE and GeoManager as a native document token.
- No changes to `GEOTEST.GEO`, `TOKEN.DB`, or the user's original GeoWorks installation were made in this audit.

## Next steps

1. Inspect the complete provider application structure in `PAPR.000` and `GDOC.000`, without redistributing those copyrighted binaries.
2. Determine the required provider token filename and manufacturer ID behavior for a GEOTEST-specific test.
3. Inspect how a true GEOS data file type is declared and associated with a token; do not infer this from the filename alone.
4. Convert the new color and monochrome artwork using the actual GeoWorks 1.x ICONMAKE utility and inspect its output.
5. Test only in a disposable GeoWorks 1.2 environment with a separate TOKEN.DB.
6. Record the exact test setup, token mapping, and GeoManager result before calling the document icon complete.


## Static analysis of the GEOTEST.GEO resources (2026-11-10)

The supplied GEOTEST.GEO was checked against the build report:
- Size: 70,794 bytes
- SHA-256: `9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b`

The resource table has 12 entries. Its table start is `0x12E`; the resource positions are DWORD entries beginning at `0x146`. Resource 4 is a 336-byte LMem resource with five local chunks. Resources 5–10 are separate resource-table entries, each with two local chunks.

The 48×30 candidate pair is resource 7 / resource 8:
- R7 starts `41 30 00 1E 00 1A`
- R8 starts `46 30 00 1E 00 1A`

The 64×40 candidate pair is resource 9 / resource 10:
- R9 starts `41 40 00 28 00 1A`
- R10 starts `46 40 00 28 00 1A`

Resources 5 and 6 start with `61 30 00 0E 00 1A` and `61 40 00 12 00 1A`, respectively. These byte prefixes and dimension-like values are measurements only. The semantic VisMoniker field definitions are not yet independently established for this exact GeoWorks 1.x target. In particular, the interpretation `0x41 = color` and `0x46 = monochrome` remains unproven.

### Resource 4: local LMem references

Resource 4 has chunk handles `0x20`, `0x22`, `0x24`, `0x26`, and `0x28`. Its 44-byte chunk at handle `0x24` contains six little-endian occurrences of `0x0022`. These are local LMem chunk handles in resource 4: handle `0x22` points to that same resource's 200-byte chunk at resource-relative offset `0x36`. They are not resource IDs 5–10 and do not establish a cross-resource icon-selection chain.

The final chunk (handle `0x28`) contains the ASCII text `GeoWorks 1.x Test`. The remaining fields in the 44-byte chunk are kept uninterpreted pending a matching GeoWorks 1.x structure definition or controlled native comparison.

### Current evidence boundary

- Resource 4's five chunks and their offsets/lengths are recorded in [investigation 2362](GEOTEST_UNTERSUCHUNG_2362.TXT).
- Resource table and moniker-candidate comparisons are recorded in [investigation 2361](GEOTEST_UNTERSUCHUNG_2361.TXT).
- The ICONMAKE-side lookup chain is recorded in [investigation 2360](ICONMAKE_RESOURCE_BLOCK_LOOKUP_2360.TXT).
- No proven chain yet connects the ICONMAKE provider lookup indices to GEOTEST resources 5–10.
- The color/monochrome meaning of the leading bytes, actual icon-selection path, and runtime display context remain open.
- GEOTEST.GEO, source files, TOKEN.DB, and the original GeoWorks installation were not modified by these static investigations. The proprietary GEO binary is not stored in this public repository.


## ICONMAKE provider variant mapping (investigation 2363)

The previously extracted PAPR and GDOC providers provide an independent correlation between the leading payload bytes and the three classic icon variants:

| Provider resource | Payload prefix | Dimensions | Extracted PCX format | Correlated variant |
|---|---|---:|---|---|
| R4 | `0x61` | 48×14 | 1-bit monochrome | CGA |
| R5 | `0x41` | 48×30 | 1-bit monochrome | HGC |
| R6 | `0x46` | 48×30 | 4-bit paletted | EGA |

The PAPR and GDOC extraction reports independently agree on these dimensions and formats. Thus, within the examined GeoWorks 1.x provider payloads, the correlation `0x61=CGA`, `0x41=HGC`, and `0x46=EGA` is now strongly supported. This is still a header/format correlation, not a complete pixel-for-pixel native payload decode.

ICONMAKE's six-byte records pass table indices 6, 5, and 4 (with additional offset `0x0022`) to its block loader. The mapping of those indices to CGA/HGC/EGA is consistent with provider resources R4/R5/R6, but the absolute 32-bit table entries and exact loaded file offsets have not yet been recalculated in this step. See [investigation 2363](ICONMAKE_PROVIDER_VARIANT_MAPPING_2363.TXT).

Important number-space distinction:
- GEODE resource indices are not ICONMAKE context-table indices.
- LMem chunk handles (for example `0x22`) are local to one resource.
- These values must not be equated based only on similar numbers.

The provider mapping does not by itself classify GEOTEST resources 5–10. Those GEOTEST payloads require their own GeoWorks 1.x VisMoniker decoding or a verified native comparison. Absolute ICONMAKE offsets, full native pixel decoding, and GeoWorks 1.2 runtime validation remain open.


## PCX input audit and transparency-index finding (investigation 2364)

A byte/pixel-level audit of the supplied icon input archives found that both new document-icon PCX files (GTS1DOC_COLOR_48x30_M14_4PLANE.PCX and GTS1DOC_MONO_48x30_M14_4PLANE.PCX) are 48×30, 1 bit per plane, four planes, and all four corner pixels use palette index 14. Their input pixels are therefore consistent with the documented ICONMAKE M14 choice, although actual ICONMAKE and GeoManager behavior has not yet been tested.

A discrepancy exists in the older GTS1ICON.PCX: its four corner pixels are palette index 13, while ERZEUGE.BAT invokes ICONMAKE M14. The README describes the exterior as palette index 13 and says it becomes transparent. The PCX bytes therefore do not support that explanation: index 13 and index 14 are distinct palette entries. Do not modify the original asset automatically; verify the exact M14 behavior with ICONMAKE 1.x on a backed-up test copy first.

The separate GEOTEST_EGA.PCX is 8 bpp / one plane, unlike the four-plane assets, and has non-uniform corner indices (7 and 9). It is described as an opaque M0 input and must not be conflated with the M14 assets.

See [investigation 2364](GEOTEST_ICON_INPUT_AUDIT_2364.TXT) for hashes, header fields, pixel counts, and test boundaries. No token was generated, no GEO or PCX file was modified, and no runtime test was performed.


## Transparency-index discrepancy (investigation 2365)

A fresh RLE decode of the uploaded PCX files found that all four corner pixels of `GTS1ICON.PCX` are palette index 13, while its batch file invokes `ICONMAKE M14`. Its README says index 13 is transparent. Those statements are internally inconsistent if M14 selects index 14, as the same README claims. The two separate document PCX files have all four corner pixels at index 14 and are structurally consistent with M14 at the file-data level.

This is not proof of ICONMAKE's actual transparency behavior. The original ICONMAKE executable is still unavailable in the current workspace, so no native output or GeoManager test was performed. Do not alter the PCX, batch file, or README until the original GeoWorks 1.x ICONMAKE test resolves the discrepancy.

See [investigation 2365](GEOTEST_ICON_TRANSPARENZ_WIDERSPRUCH_2365.TXT). No GEO, PCX, token, or TOKEN.DB file was modified.


## Exact ICONMAKE provider blocks and transparency parameter (investigation 2366)

The original `ICONMAKE.EXE`, `PAPR.000`, and `GDOC.000` were extracted again from the user's `GEOWORKS.zip`. The executable hash matches the previously analyzed binary. Its context builder at 164Ch reads the provider resource count and table; its block loader at 1758h resolves the DWORD resource position, adds offset `0x22`, reads the pointer `0x2A`, obtains the block length at base+`0x28`, and reads the block from base+`0x2A`.

The exact provider table bases are:
- PAPR indices 4/5/6: `0x3F4`, `0x498`, `0x5AC`.
- GDOC indices 4/5/6: `0x3F4`, `0x498`, `0x59C`.

The six extracted blocks confirm the mapping index 4 = CGA (prefix `0x61`), index 5 = HGC (prefix `0x41`), and index 6 = EGA (prefix `0x46`). Exact offsets, lengths, and block hashes are in [investigation 2366](ICONMAKE_PROVIDER_EXACT_BLOCKS_2366.TXT).

The same disassembly confirms that the `m[<transp_color>]` mode parses the decimal suffix, defaults to 14 when omitted, and passes the selected value into icon-variant creation. The uploaded `GTS1ICON.PCX` has corner pixels at index 13, while `ERZEUGE.BAT` calls `ICONMAKE M14`. Therefore that command does not select the actual corner index. `M13` is the matching parameter for this input file. This is a static conclusion; no ICONMAKE execution or GeoWorks 1.2 display test has yet been performed. The batch file and README have deliberately not been changed.


## Audit of generated GTS1 token output (investigation 2367)

The user supplied `GTS10000.000` (1,760 bytes; SHA-256 `7ea8625f66868038b3c1e7c99cc11c5134b8fa2b211b9b84c23767dd6e03b54f`). Its header contains token `GTS1`, manufacturer ID 0, creator `GEOS`, and seven resources. The resource table is structurally in-bounds. Resources 4, 5, and 6 contain leading variant signatures `0x61`, `0x41`, and `0x46`, respectively, matching the CGA/HGC/EGA provider signatures established in investigation 2366.

The file does not contain an identified explicit marker stating whether it was generated with M13 or M14. A single output therefore cannot establish which transparency parameter was used or prove the rendered transparency. The second output from the other test folder and confirmation of this file's origin (M13 or M14) are required for a controlled byte comparison. Resources 4 and 5 are only 0x30 bytes each; do not describe them as fully decoded pixel bitmaps based on their signatures alone.

See [investigation 2367](ICONMAKE_TOKEN_OUTPUT_AUDIT_2367.TXT). No source or generated file was modified.
