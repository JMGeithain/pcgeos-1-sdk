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

## Original GeoWorks 1.x kernel loader investigation (2026-11-08)

The current static investigation of the original German `KERNEL.OLD` and the separately patched `KERNEL.EXE` is documented in [GEODE_RELOCATION_REASSESSMENT_2026-11-08.md](GEODE_RELOCATION_REASSESSMENT_2026-11-08.md), sections 2051–2060. The MZ DOS relocation table is explicitly distinguished from GEODE resource relocation streams. The DOS entry path and a kernel bootstrap self-relocation routine have been disassembled, but the GEODE relocation-processing routine has **not yet been identified**. No parser or binary changes follow from this work.

## Loader-confirmed relocation decoding (2026-11-08)

The original German `KERNEL.OLD` contains the GEODE loader path at load-image offset `0x1970`; its relocation reader is at `0x20FE` and dispatches each four-byte record to `0x2153`. The reader loads the first WORD into AX and the final WORD into BX; `BX` is used as an offset into the target resource (`ES:[BX]`). The dispatcher splits the first byte: its low nibble (`byte0 & 0x0F`) selects an operation, while its high nibble (`byte0 & 0xF0`) selects a processing class. The second byte is used as an index in at least the `0x10` class branch. Therefore `<BBH>` remains a useful storage representation, but the earlier interpretation of byte 0 as one complete type and byte 1 as a generic auxiliary field is superseded. See sections 2071–2080 in [the reassessment dossier](GEODE_RELOCATION_REASSESSMENT_2026-11-08.md). This is static disassembly; no runtime loader test has yet been performed.

## Dispatcher branch map (Investigation 2081–2090)

Static disassembly of the original German `KERNEL.OLD` at the correctly aligned entry `0x2153` confirms: byte 0 high nibble selects a class path; byte 0 low nibble selects an operation. Class `0x00` obtains a table segment through `CS:[0x2151]`; class `0x10` uses byte 1 as a WORD index into the segment table based at `DS:[0x0036]`; other classes enter a path using a table based at `DS:[0x003A]`. The resource WORD at `ES:[BX]` is read before dispatch. The common operation code has distinct paths for low-nibble values 0–3, including a special code-patching path that writes `0xCD` at `ES:[BX-1]`. The structures behind `DS:[0x0030]`, `DS:[0x0036]`, `DS:[0x003A]`, and `CS:[0x2151]` remain under investigation; do not assign symbolic relocation names yet. See dossier section 2081–2090.

## Importauflösung im Originalkernel (Untersuchungen 2101–2110)

Der deutsche GeoWorks-1.x-Originalkernel bestätigt nun den Importtabellenpfad: `0034` zählt die 14-Byte-Importeinträge. Routine `2652` verarbeitet je Eintrag die Felder bei `+08`, `+0A` und `+0C`, ruft `271C` zur Auflösung auf und schreibt den resultierenden WORD-Segmentwert in die Tabelle ab `0036`. Der Relocation-Dispatcher-Zweig `10h` indiziert diese Tabelle mit `2 * AH` und lädt den gefundenen Wert nach `DS`. `0030` liegt unmittelbar hinter dieser WORD-Tabelle (`0036 + 2*0034`). Die Header-Offsets `0046h` und `005Eh` werden abhängig von Flag `80h` ausgewählt; ihre konkrete Variantenbedeutung wird noch mit Original-GEODE-Dateien abgeglichen. Details und Disassembly: [Reassessment-Dossier, Untersuchungen 2101–2110](GEODE_RELOCATION_REASSESSMENT_2026-11-08.md). Statische Analyse, noch kein Laufzeittest.
