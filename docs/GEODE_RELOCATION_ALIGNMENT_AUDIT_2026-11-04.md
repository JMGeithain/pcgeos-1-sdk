# PC/GEOS 1.x GEODE relocation-alignment audit

Date: 2026-11-04. Scope: read-only inspection of the supplied GEOWORKS(4).zip and GNU Chess 8086 source archive. No GEO binary was modified and no SDK parser source was changed.

## Finding

The GNU Chess archive's native 1.x helper SOURCE/port1/audit/geo1.py calculates relocation data at resource_position + resource_size. This is not correct for every native PC/GEOS 1.x file examined. The unmodified GeoWorks 1.x SPLAY.GEO contains paragraph padding between initialized resource bytes and relocation records. Its relocation stream begins at resource_position + ((resource_size + 15) & ~15).

This matches the current SDK parser's align16(size) calculation for the tested 1.x file. Do not remove paragraph alignment from pcgeos1/geode.py on the basis of the GNU Chess helper. The accompanying GNU Chess audit note claiming that relocation bytes follow initialized data without padding is contradicted by the raw SPLAY bytes. Treat that statement and the helper's relocation offset as an audit-script/documentation defect until clarified.

## Reproducible SPLAY evidence

File: GEOWORKS/SPLAY.GEO; identical duplicate: GEOWORKS/WORLD/SPLAY.GEO. Size: 31,390 bytes. SHA-256: 98cacf83465e6dbe2225f44bfb1a0de04dc04aeca6f8ad453397521ce9a4a646. Signature: C7 45 CF 53 (GEOS 1.x).

Resource 2:

| Field | Value |
|---|---:|
| Resource position | 0x05C2 |
| Initialized size | 1250 (0x04E2) |
| Relocation byte count | 296 (74 records) |
| Immediately after data | 0x0AA4 |
| Paragraph-aligned relocation start | 0x0AB2 |
| Padding | 14 bytes |

At 0x0AA4, the bytes are padding zeros followed by the beginning of the relocation stream. Interpreting this as the stream start produces invalid record fields, including relocation kind 0xF and source class 3. At 0x0AB2, all 74 four-byte records satisfy the current parser's bounded checks: source class 0–2, kind 0–5, and target within the resource.

Resource 3 independently confirms the same rule:

| Field | Value |
|---|---:|
| Resource position | 0x0BDA |
| Initialized size | 6479 (0x194F) |
| Relocation byte count | 988 (247 records) |
| Immediately after data | 0x2529 |
| Paragraph-aligned relocation start | 0x252A |
| Padding | 1 byte |

The aligned start yields 247 records passing the same bounded checks. Starting at 0x2529 shifts the four-byte record boundaries and produces invalid target offsets.

## Archive-wide inventory

A signature-only inventory of GEOWORKS(4).zip found 260 .GEO files with the GEOS 1.x signature. Three paths contain resource sizes that are not multiples of 16:

- GEOWORKS/SPLAY.GEO
- GEOWORKS/WORLD/SPLAY.GEO (byte-identical duplicate)
- GEOWORKS/SYSAPPL/NPLAYGCM.GEO

The inventory shows that paragraph rounding is not a vacuous case. At least two resources in SPLAY require nonzero padding before relocation records. Other files, including the distinct DOCUMENT/SPLAY.GEO variant, need separate review before broader claims are made.

## Cross-check against GNU Chess source

The 8086 release's application writer reads its GEOS 2.x engine source with rp = pos + align16(size), and pads each emitted resource to a 16-byte boundary before writing relocation records. Its generated GEOS 1.x outputs also have paragraph-rounded resource sizes, so those outputs alone cannot distinguish direct from aligned relocation placement.

By contrast, the archive's small native 1.x audit helper uses p + size for relocation streams. That helper is unsafe for native 1.x resources whose initialized sizes are not paragraph multiples. Its resource-data extraction p:p+size is separate and remains appropriate; only relocation-stream positioning is implicated.

## SDK consequences

- Keep the current align16(size) relocation offset in the GEOS 1.x parser for now.
- Do not treat GNU Chess geo1.py relocation offsets as authoritative for non-paragraph-sized native 1.x resources.
- Add a regression fixture with a deliberately non-16-byte resource size and nonzero padding bytes, with relocation records at the paragraph boundary.
- Add an optional read-only parser sweep over a known, hash-bound native GeoWorks archive; record exceptions individually rather than weakening validation to force all files through.
- Keep GEOS 2.x handling separate. This audit establishes no new GEOS 2.x rule.
- Do not alter original GEO files or claim runtime-loader validation from static byte analysis.

## Method and limits

The ZIP was CRC-tested. Header/resource table values and raw bytes were read directly from archived GEO members. Record alignment was tested by decoding four-byte little-endian records at both candidate offsets and checking source, type, and target bounds. This is a static structural check, not execution by the GeoManager loader. The result is strong evidence for the tested SPLAY file, not a complete specification of every PC/GEOS 1.x variant.


## Cross-validation against seven native donor files

A second read-only pass applied the current SDK parser's structural checks (header count consistency, resource bounds, paragraph-aligned relocation starts, four-byte relocation records, source/type limits, import bounds, and target bounds) to seven available GEOS 1.x donor files. All seven passed this bounded check:

| File | Bytes | Resources | Relocation records |
|---|---:|---:|---:|
| NOTEPAD.GEO | 8,070 | 15 | 105 |
| VIEWER.GEO | 59,984 | 37 | 877 |
| TERM.GEO | 63,718 | 32 | 1,240 |
| SPINTEXT.GEO | 3,764 | 11 | 58 |
| SYSTEM/SVGA8004.GEO | 18,950 | 3 | 50 |
| WORLD/BOUNCE.GEO | 3,572 | 11 | 46 |
| SPLAY.GEO | 31,390 | 14 | 389 |

The check was an independent script reproducing the current parser's structural rules, not a call to the repository's Python module and not a GeoManager load. The four user-supplied application files are known local inputs; SPINTEXT.GEO contains local demo/site strings and is not a pristine stock donor. BOUNCE and SVGA8004 came from the supplied GeoWorks archive. These results support the paragraph-aligned relocation offset for this bounded donor set; they do not prove every legacy relocation source/type is covered.

A wider inventory also surfaced exceptional files whose relocation records do not satisfy the parser's current source/type restrictions (including a distinct DOCUMENT/SPLAY.GEO variant and some CD-player geodes). Do not broaden or weaken the accepted relocation source/type range without identifying the semantics of those records. Record these as separate compatibility cases, not as evidence against the SPLAY alignment result.
