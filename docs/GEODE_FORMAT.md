# GEOS Executable Format Notes

`pcgeos1/geode.py` is a bounds-checked reader for the GEOS 1.x and 2.x executable layouts encountered during this work. It is not a loader.

## GEOS 1.x

The known 1.x geodes use signature bytes:

```text
C7 45 CF 53
```

The executable header starts at byte 200. Resource file positions are absolute.

## GEOS 2.x

The observed 2.x files use:

```text
C7 45 C1 53
```

The executable header starts at byte 256, and stored resource positions require the 256-byte header origin adjustment.

## Tables

The parser reads:

- imported libraries
- exported entry table
- resource size table
- resource file-position table
- relocation-size table
- resource flags
- relocation records

It verifies duplicate count fields, resource bounds, overlap, import indices and relocation target bounds.

## Relocation records

Each observed relocation record is four bytes:

```text
info, extra, target_offset
```

The upper nibble of `info` identifies the source class; the lower nibble identifies the relocation type. SDK 0.1 emits kernel far-call and resource relocations needed by its runtime.

## Packer strategy

The SDK starts from a known native 1.x application skeleton, preserves its import table and compatible resources, replaces dgroup/code/UI resources, appends a private engine resource, and rewrites the resource descriptor table and payload positions.

This is safer than manufacturing every undocumented header field from zero in the first SDK release.


## Open relocation special cases (2026-11-04)

A static comparison of native GeoWorks 1.x `ELVISBYE.GEO`, `EXPRSRTL.GEO` and `SENDFAX2.GEO` found single four-byte resource-10 relocation records with info bytes `DDh`, `63h` and `23h`, respectively. The meanings of `DDh` and `63h` are not established. Both files also contain 68 repeated little-endian words in initialized resource data that match the respective relocation offset word (`02DDh` / `0263h`). This correlation is documented but its runtime meaning remains open.

Do not broaden the parser's accepted relocation types based on these two examples, and do not label the values invalid without tracing the original 1.x loader. See [the dedicated audit](GEODE_RELOCATION_SPECIAL_CASES_ELVISBYE_EXPRSRTL_2026-11-04.md). No original GEO file or parser code was modified.

## Relocation stream alignment and current reassessment (2026-11-08)

For the current GEOS 1.x reader, the relocation stream for a resource begins at `resource_file_offset + align16(resource_size)`, where `align16(n) = (n + 15) & ~15`. A four-byte relocation record is decoded as `<BBH>`: `info`, `extra`, and a little-endian 16-bit target offset. The upper nibble of `info` is the source class and the lower nibble is the relocation type. Do not combine the first two bytes into a WORD or infer a Big-Endian variant from records read at an unaligned stream position.

The 2026-11-08 reassessment rechecks NOTEPAD, GROBJ, SPLAY and NPLAYGCM against the repository parser. It confirms the current model for several native 1.x files and records DOCUMENT/SPLAY and root NPLAYGCM as unresolved compatibility exceptions. It does not change parser acceptance rules or claim runtime-loader validation. See [the reassessment dossier](GEODE_RELOCATION_REASSESSMENT_2026-11-08.md) and the [2026-11-04 alignment audit](GEODE_RELOCATION_ALIGNMENT_AUDIT_2026-11-04.md).
