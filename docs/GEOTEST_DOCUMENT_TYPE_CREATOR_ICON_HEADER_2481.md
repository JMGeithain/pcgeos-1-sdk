# GEOTEST – GeoWorks document header: type token, creator token and icon mapping (Investigation 2481)

**Date:** 2026-11-12  
**Scope:** GeoWorks / PC/GEOS 1.x only

## 1. Goal

Determine which fields in native GeoWorks 1.x document files identify the document type and creating application, and prepare the first GEOTEST document prototype without inventing an unverified header layout or token.

## 2. Sources

Read-only sources from the user's GEOWORKS.zip:
- GEOWORKS/DOCUMENT/NEUES_DO.000 — 2,352 bytes
- GEOWORKS/DOCUMENT/TESTWRIT.000 — 2,752 bytes
- GEOWORKS/ICONS/DOS_ICON.TXT
- GEOWORKS/ICONS/ICONINST.TXT
- GEOWORKS/SYSTEM/TOKEN.DB
- GEOWORKS/SYSTEM/TOKENDB.ALT/TOKEN.DB
- GEOWORKS/BUCH/TOKEN.DB

Both sample documents begin with the GeoWorks 1.x signature C7 45 CF 53. No source files were modified.

## 3. Document-header fields

The supplied DOS_ICON.TXT identifies:
- offset 0x14: Type — four-byte document-type token;
- offset 0x1A: Creator — four-byte token for the application that created the file;
- offset 0x20: long filename.

The actual bytes in the two native documents confirm this:

| File | Type at 0x14 | Creator at 0x1A | Long name at 0x20 |
|---|---|---|---|
| NEUES_DO.000 | WDAT | WP00 | Neues Dokument |
| TESTWRIT.000 | WDAT | WP00 | testwrite |

This directly confirms that Type and Creator are separate four-byte fields.

## 4. Inventory of document files

A byte-level inventory found 426 files under GEOWORKS/DOCUMENT/ with the GEODE 1.x signature and a .000 suffix. Their Type/Creator pairs at offsets 0x14/0x1A are:

| Type | Creator | Count |
|---|---|---:|
| WDAT | WP00 | 198 |
| DDAT | DP00 | 154 |
| scbk | Scrp | 54 |
| adbk | ADBK | 8 |
| Icon | GEOS | 6 |
| plnr | PLNR | 2 |
| TMPL | null bytes | 2 |
| jmgn | GEOS | 1 |
| TOOL | Scrp | 1 |

The frequent WDAT/WP00 and DDAT/DP00 pairs agree with the token list in DOS_ICON.TXT, which lists WDAT as the GeoWrite data-file icon and DDAT as the GeoDraw data-file icon. This is an archive inventory, not a live test of all 426 files.

## 5. Token database collision check

The three archived TOKEN.DB files were searched for the four-byte sequences GTD1 and GTS1:
- GTD1: no hit in the three TOKEN.DB files.
- GTS1: no hit in the three TOKEN.DB files.
- WDAT, WP00, DDAT, and DP00 are present.

The complete GEOWORKS.zip was also searched for GTD1; no hit was found. GTD1 is therefore a possible unused four-character candidate within this archive, not a globally guaranteed unique token and not yet approved as the final GEOTEST document type. It must be checked in the actual target installation and given a corresponding document-icon token entry before use.

## 6. Distinguish filename rules from native file type

ICONINST.TXT describes [fileManager] filenameTokens in GEOS.INI. Those rules assign icons by DOS filename pattern or extension (for example *.BAT). DOS_ICON.TXT separately describes the Type field in the GEOS file header and lists WDAT/DDAT as native data-file icons.

These mechanisms must not be conflated:
- filenameTokens: mapping by filename pattern;
- Type token in the GEOS file header: native file-type identifier.

For the GEOTEST document, the Type-token path is the relevant research target. No change to the production GEOS.INI is proposed for the first test.

## 7. Implications for GEOTEST

The existing GEOTEST application token is GTS1. Native GeoWrite/GeoDraw files show that a document carries a separate Type token and Creator token.

A concrete prototype plan is now:
1. Select a four-character document Type token and check it against the target TOKEN.DB.
2. Use GTS1 as Creator only after confirming the native GeoManager/document-launch path accepts the app token in that role.
3. Generate a structurally valid minimal GEOS document. NEUES_DO.000 and TESTWRIT.000 are comparison inputs; their GeoWrite content structure must not be copied as if it were already a GEOTEST format.
4. Create a document-icon entry for the new Type token through the verified GeoWorks 1.x token mechanism.
5. Test the Type/Creator association and icon display in GeoManager.

The Creator assignment and exact icon resolution for a new Type token still require a GeoWorks 1.2 runtime test. They are not claimed as tested.

## 8. When can the new GEO be built?

The existing GEOTEST base application (window, view, keyboard/mouse callbacks and Help) has already been built and launched in GeoWorks 1.2 on 2026-11-09. That base can be rebuilt from the current SDK project; the complete GEODE loader analysis is not a prerequisite.

A new version with document creation and its own document icon can be built only after the document-creation path and Type/icon association are implemented. The header fields are now confirmed, but file creation, the native GEOS document payload and the new token-database entry are not yet integrated. MiniCalc's file-service adapter is a possible implementation reference, but it does not by itself prove a valid native GEOS document format.

## 9. Change and test status

- Original archive files were read only.
- No TOKEN.DB or GEOS.INI was modified.
- No new GEOTEST.GEO was built in this investigation.
- No GeoWorks runtime test was performed.
- No final document Type token was selected.
- No new document icon was registered.

## 10. Version boundary

All findings use GeoWorks 1.x files and documentation from the user's archive. PC/GEOS 2.x / FreeGEOS implementations were not used as evidence.
