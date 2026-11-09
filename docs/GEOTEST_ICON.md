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
