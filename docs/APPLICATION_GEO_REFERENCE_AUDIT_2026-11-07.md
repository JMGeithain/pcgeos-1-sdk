# Native PC/GEOS 1.x application GEO reference audit — 2026-11-07

## Purpose and scope

This note records the current static investigation toward **GEOTEST.GEO as a real, startable PC/GEOS 1.x application**. GEOTEST is not a display driver and must not be designed as one.

The investigation uses four user-supplied application files:

- `BOUNCE.GEO`
- `GEODEX.GEO`
- `GEOPLAN.GEO`
- `BANNER.GEO`

The existing `EGA.GEO` and `SVGA8004.GEO` files remain driver-format comparison material only. No PC/GEOS 2.x or FreeGEOS behavior is promoted to verified 1.x behavior.

**Evidence status:** all byte observations below are static-analysis observations from the supplied files. No claim is made here that these four binaries were launched in the user's current GeoWorks installation. No GEOTEST binary has yet been built or runtime-tested.

## 1. Input identity

File sizes and SHA-256 hashes were recalculated from the uploaded files on 2026-11-07.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| `BOUNCE.GEO` | 3,572 | `154b3ed8b6ab568e7cdc76aa35cbc2b9e54cd6e199b845b6a3922ff5111e8ecd` |
| `GEODEX.GEO` | 53,816 | `fc07b894a4824a5f8b0fa4ea38c711cf37022befbc262e3d3ae17b20d2dea47f` |
| `GEOPLAN.GEO` | 58,546 | `00f2319be1520f8ab768dbdc4426a63ce16ed3dbc6cd782e42139c66996c11cb` |
| `BANNER.GEO` | 11,544 | `e61507241d5db616ed7e1fbc6d527c025cb433c80e2ebc62343d9cb1b6583932` |

These hashes identify the uploaded copies only. Their provenance as stock, unmodified distribution files has not been established.

## 2. Shared file prefix and identification fields

All four files begin with the same 16 bytes:

```
C7 45 CF 53 00 00 00 00 01 00 02 00
```

Correction: the complete first 16 bytes are not identical. The final four bytes vary by file. At offset `0010h`, the observed little-endian words are:

| File | Bytes at 0010h | Little-endian value |
|---|---|---:|
| BOUNCE | `65 00 00 00` | first word 0065h |
| GEODEX | `05 02 00 00` | first word 0205h |
| GEOPLAN | `0B 02 00 00` | first word 020Bh |
| BANNER | `F6 01 00 00` | first word 01F6h |

At `0014h` each file contains a four-byte application token:

- BOUNCE: `BONC`
- GEODEX: `ADBK`
- GEOPLAN: `PLNR`
- BANNER: `GBNR`

At `001Ah` the ASCII bytes `GEOS` occur in all four files. This is a raw observation; the complete semantics of these fields are not inferred here.

The existing SDK note `docs/GEODE_FORMAT.md` records the observed PC/GEOS 1.x signature `C7 45 CF 53` and states that the executable header begins at file byte 200 (decimal, `0xC8`). Keep file offsets distinct from executable-header-relative offsets and runtime addresses.

## 3. Names and descriptive strings

The files contain readable application names near the start:

- BOUNCE: `Bounce`
- GEODEX: `GeoDex`
- GEOPLAN: `GeoPlanner`
- BANNER: `GeoBanner`

All four contain the ASCII string `Copyright GeoWorks 1991` in the region beginning around file offset `00A8h`.

Near `00F0h`, the files contain identifying text including `app` and the four-byte application token. The exact surrounding bytes differ. These strings support classification as application examples, but they do not identify the loader entry point or establish a complete header schema.

## 4. Resource-name area around file offset 0120h

All four files contain the eight-byte padded name `ui` at file offset `0120h`:

```
75 69 20 20 20 20 20 20
```

The six bytes immediately following that name are:

```
00 40 B5 02 00 00
```

This six-byte sequence is identical in all four supplied files.

**Important correction to the preliminary discussion:** the evidence does not support calling the resource records 16 bytes long. In GEODEX, GEOPLAN and BANNER, the next resource name begins at file offset `012Eh`, i.e. 14 bytes after the beginning of the `ui` name. The observed layout is therefore consistent with an eight-byte name followed by a six-byte descriptor, with a 14-byte stride for these entries. This is a structural observation, not yet a complete interpretation of the descriptor.

Additional visible resource names in the same area:

| File | Visible names |
|---|---|
| BOUNCE | `ui` |
| GEODEX | `ui`, `dbase`, `spool` |
| GEOPLAN | `ui`, `dbase`, `spool` |
| BANNER | `ui`, `spool` |

For GEODEX, the bytes at `012Eh` begin the padded name `dbase`; the next name `spool` follows at `013Ch`. The same visible 14-byte spacing is present for the corresponding names in GEOPLAN and BANNER. The BOUNCE file is shorter and its area after the `ui` descriptor must be interpreted in the context of its complete header/tables rather than assuming the same visible number of entries.

## 5. The descriptor value 02B5h

The byte sequence `B5 02` occurs at file offsets `012Ah–012Bh` in the six-byte descriptor after `ui`. Interpreted as a little-endian WORD, it is `02B5h`.

At file offset `02B5h` in BOUNCE, the byte is `51h`. The surrounding bytes beginning at `02B0h` are:

```
0B ED 74 1E 50 51 06 8B DD 9A 05 00 00 00 8E D8
```

A provisional 8086 decode from this byte stream gives:

```asm
02B0  OR  BP,BP
02B2  JE  02D2
02B4  PUSH AX
02B5  PUSH CX
02B6  PUSH ES
02B7  MOV  BX,BP
02B9  CALL FAR 0000:0005
```

This establishes that `02B5h` is an instruction boundary in this provisional linear decode and that the byte there is `51h` (`PUSH CX`). It does **not** prove that the `ui` descriptor points directly to executable code at file offset `02B5h`. The descriptor's address space and relocation/loader treatment remain unresolved.

## 6. Disassembly and relocation cautions

The preliminary conversational analysis of BOUNCE included several interpretations of code beginning around `02B0h`, including copy sequences and FAR calls. Those interpretations are not yet a validated reconstruction of the application's startup path.

In particular:

- a file offset is not automatically a loaded segment offset;
- a far pointer with zero segment bytes in the file cannot be interpreted as a runtime `0000:offset` call without resolving relocation and loader behavior;
- code/data boundaries must be established before linear disassembly is treated as a routine;
- a byte sequence that resembles `REP MOVSB` must be checked against instruction boundaries and the complete control-flow path;
- the apparent reference to `007Ch` and the observed `0070h` copy length are leads only, not yet identified application data structures.

No startup function, application object, UI object, or required system-call list has yet been proven from this disassembly.

## 7. Correction log for earlier preliminary statements

The following earlier statements should not be reused as established facts:

1. **“All bytes through the initial header are identical.”** Only the first 12 bytes are common; the words beginning at `0010h` differ.
2. **“The resource records are 16 bytes.”** The observed next-name positions in GEODEX/GEOPLAN/BANNER support a 14-byte stride (8-byte name + 6-byte descriptor), not 16.
3. **“The data at 0220h is common across the four applications.”** A direct byte comparison disproves this; BOUNCE and BANNER have different data there, and GEODEX/GEOPLAN also differ.
4. **“02B5h is a confirmed UI resource pointer.”** It is only a little-endian value in the descriptor. Its address-space semantics have not been determined.
5. **“The code around 02B0h is a fully understood initialization/copy routine.”** It is not. The previous decode is provisional and needs relocation-aware control-flow analysis.

These corrections are deliberate. Raw observations must remain separate from hypotheses.

## 8. Current findings by confidence

### Static-analysis confirmed

- The four uploaded files have the sizes and SHA-256 values in Section 1.
- Each begins with signature bytes `C7 45 CF 53`.
- The application tokens are `BONC`, `ADBK`, `PLNR`, and `GBNR` at `0014h`.
- The ASCII marker `GEOS` occurs at `001Ah`.
- The padded `ui` name occurs at `0120h`.
- The six bytes following `ui` are `00 40 B5 02 00 00`.
- Additional visible names `dbase` and `spool` occur in the larger examples at the offsets described above.
- The BOUNCE bytes at `02B0h` are exactly as printed in Section 5.

### Hypotheses / unresolved

- The six bytes after a resource name are a resource descriptor; their field-by-field semantics are unknown.
- `02B5h` may participate in a resource/code reference, but this is not proven.
- The code around `02B0h` may be part of application initialization, but its control flow and runtime segment context are not reconstructed.
- The visible resource names may not be the complete resource inventory.

### Not demonstrated

- Successful launch of any of the four uploaded applications on the user's current German GeoWorks 1.2 installation.
- The exact loader entry point and application lifecycle.
- The complete resource directory format.
- The minimum valid application resource set.
- The minimum UI object tree needed for a visible window.
- A working `GEOTEST.GEO` build.

## 9. GEOTEST.GEO development objective

The intended artifact is a **native, startable PC/GEOS 1.x application**, not a graphics or mouse driver.

Initial acceptance goals:

1. GeoManager recognizes and starts `GEOTEST.GEO`.
2. The application opens a native application window.
3. The window displays a short test string such as “GeoWorks 1.x — GEOTEST”.
4. The application can close through the normal GEOS UI lifecycle.
5. The same source/build investigation keeps German GeoWorks 1.2 and English GeoWorks 1.2 as separate target profiles where binary/API differences require it.

The first implementation should be derived from a proven native application skeleton and exact target resources, consistent with the SDK's existing conservative packer strategy. Do not synthesize undocumented header fields or UI object layouts from guesses.

## 10. Next reproducible research tasks

1. Parse each reference with the repository's existing GEODE reader and compare its resource count, resource positions, flags and relocation streams.
2. Verify whether the apparent 14-byte resource-name/descriptor layout is a name table distinct from the SDK's resource descriptor arrays.
3. Trace the six descriptor bytes using references from the executable header and loader-facing tables.
4. Identify BOUNCE's code and data resource boundaries before further disassembly.
5. Resolve every relevant FAR call using the actual relocation records and the exact target import/export tables.
6. Compare BOUNCE's startup lifecycle with the SDK's known native application skeleton and with BANNER.
7. Select the smallest **verified** native application skeleton for a GEOTEST prototype.
8. Keep runtime tests separate for English and German GeoWorks 1.2.

## Reproduction notes

The hashes above were calculated directly from the four uploaded files. The byte excerpts are file offsets (hexadecimal), not runtime addresses. The preliminary 8086 decode is a linear decode of the printed bytes only; it is not a loader-aware disassembly. No supplied original GEO file was modified.


## 11. SDK parser cross-check of four native application examples (2026-11-07)

This section supersedes the preliminary interpretation of the bytes at file offset 0x120 in Sections 4–5 above.

### Import table, not resource-name table

The SDK reader `pcgeos1/geode.py` uses the following PC/GEOS 1.x table layout:

- executable header origin: file offset 200 (0xC8);
- import table: `header + 88` = 0x120;
- each import record: 14 bytes;
- export table follows the imports, with four bytes per export;
- resource descriptor arrays follow the exports.

The 14-byte record at 0x120 in BOUNCE is therefore an **import-library record**, not a resource record:

```
0120: 75 69 20 20 20 20 20 20   "ui      "
0128: 00 40                    attributes = 0x4000
012A: B5 02                    protocol = 0x02B5 = 693
012C: 00 00                    protocol minor = 0
```

Thus the previous hypothesis that `02B5h` was a UI-resource file pointer is rejected. It is the imported `ui` library's protocol value (693). The same import appears in all four applications.

Other imports observed:

| Library | Protocol major | Protocol minor |
|---|---:|---:|
| `ui` | 693 | 0 |
| `dbase` | 601 | 0 |
| `spool` | 613 | 0 |

The import attributes for these records are 0x4000 in the four supplied examples.

### Parser-derived application table summary

The four files were checked against the layout and validation logic implemented by `pcgeos1/geode.py`: duplicate header counts, import/export table positions, resource extents, paragraph-aligned relocation stream positions, relocation record bounds, source classes, type range, and import indexes.

| File | Resources | Imports | Exports | Relocation records |
|---|---:|---:|---:|---:|
| BOUNCE.GEO | 11 | 1 | 0 | 46 |
| GEODEX.GEO | 59 | 3 | 3 | 957 |
| GEOPLAN.GEO | 32 | 3 | 14 | 1,324 |
| BANNER.GEO | 14 | 2 | 2 | 174 |

This was a parser-equivalent execution of the checked logic against the four uploaded binaries. It is a static structural validation, not a GEOS runtime test. It does not establish that the parser models every loader rule or every private resource flag.

### BOUNCE resource descriptor summary

The SDK reader calculates the following first resource entries for BOUNCE:

| Resource ID | Size | Absolute file position | Relocation bytes | Flags |
|---:|---:|---:|---:|---:|
| 0 | 0x0000 | 0x019C | 0x0000 | 0x0880 |
| 1 | 0x00F0 | 0x019C | 0x0024 | 0x0080 |
| 2 | 0x0200 | 0x02B0 | 0x0074 | 0x0A72 |
| 3 | 0x0180 | 0x0524 | 0x0004 | 0x145A |
| 4 | 0x0150 | 0x06A8 | 0x0004 | 0x145A |
| 5 | 0x00A0 | 0x07FC | 0x0004 | 0x1C7A |
| 6 | 0x0060 | 0x08A0 | 0x0004 | 0x1C7A |
| 7 | 0x0100 | 0x0904 | 0x0004 | 0x1C7A |
| 8 | 0x0270 | 0x0A08 | 0x0004 | 0x1C7A |
| 9 | 0x0090 | 0x0C7C | 0x0004 | 0x1C7A |
| 10 | 0x00E0 | 0x0D10 | 0x0004 | 0x1C7A |

Resource 2 begins at file offset 0x02B0. Consequently, the earlier code examination at 0x02B0 is examining bytes within resource 2, not a standalone file-level startup entry. Resource 2's semantic role has not yet been identified.

The 46 BOUNCE relocation records are distributed as follows: resource 1 has 9; resource 2 has 29; resources 3 through 10 have one each. This distribution is static evidence only; relocation types and runtime effects still need individual tracing.

### Important interpretation corrections

1. `ui`, `dbase`, and `spool` at 0x120 onward are imported library names, not resource names.
2. The 14-byte spacing is the import-record size: 8-byte library name plus 6 bytes of attributes/protocol fields.
3. `02B5h` is protocol major 693 for the `ui` import, not a pointer to code or a resource.
4. File offset 0x02B0 is the beginning of BOUNCE resource 2 according to the SDK resource-position table.
5. The resource table is distinct from the import and export tables. Resource IDs are zero-based in the SDK parser.

### Consequence for GEOTEST

BOUNCE remains a useful small native application specimen: 11 resources, one imported library (`ui`), no exports, and 46 relocation records. It is not yet proven that all 11 resources are needed to start the application, nor which resource contains the process object, UI tree, or startup code.

Next work should identify resource types and flags from target-matched evidence, trace resource 1 and resource 2 relocations, resolve imported UI symbols/ordinals, and compare the application's process/object lifecycle with BANNER. Do not delete or synthesize resources based only on size or flag values.


## 12. Resource 1 / Resource 2 relocation audit: BOUNCE and BANNER (2026-11-07)

This section records a fresh byte-level pass over the locally available, user-supplied `BOUNCE.GEO` and `BANNER.GEO`. Hashes were recalculated and match Section 1. The repository parser's table model was reproduced against the local files; no original GEO was modified.

### 12.1 BOUNCE resource 1

Resource 1 descriptor:

| Field | Value |
|---|---:|
| Resource ID | 1 |
| File offset | 0x019C |
| Initialized size | 0x00F0 |
| Relocation bytes | 0x0024 (36 bytes / 9 records) |
| Flags | 0x0080 |

The first nonzero structured fields are visible around resource-relative offset 0x0040. Its nine relocation records are:

| Target offset | Info | Source class | Type | Extra | Word at target |
|---:|---:|---:|---:|---:|---:|
| 0x0040 | 0x11 | 1 | 1 | 0 | 0x0000 |
| 0x0042 | 0x12 | 1 | 2 | 0 | 0x0000 |
| 0x0062 | 0x22 | 2 | 2 | 0 | 0x0002 |
| 0x0066 | 0x22 | 2 | 2 | 0 | 0x0002 |
| 0x006A | 0x22 | 2 | 2 | 0 | 0x0002 |
| 0x006E | 0x22 | 2 | 2 | 0 | 0x0002 |
| 0x0072 | 0x22 | 2 | 2 | 0 | 0x0002 |
| 0x0076 | 0x22 | 2 | 2 | 0 | 0x0002 |
| 0x007A | 0x22 | 2 | 2 | 0 | 0x0002 |

Under the parser's nibble split, info 0x11 and 0x12 use source class 1 and import index 0 (the `ui` import); the six 0x22 records use source class 2 and extra 0. This establishes structural import/resource relocation relationships under the SDK model. It does not, by itself, establish the runtime operation performed by relocation types 1 and 2.

### 12.2 BOUNCE resource 2

Resource 2 descriptor:

| Field | Value |
|---|---:|
| Resource ID | 2 |
| File offset | 0x02B0 |
| Initialized size | 0x0200 |
| Relocation bytes | 0x0074 (116 bytes / 29 records) |
| Flags | 0x0A72 |

All 29 records have info byte 0x00 (source class 0, type 0, extra 0). Their target offsets and pre-relocation WORD values are:

```
target  value
000A    0005
001B    0006
0028    01E9
003F    0000
0050    0006
0065    0096
0075    00A9
007E    01E9
008A    0095
0095    00A9
00AA    01E9
00BD    0095
00C8    00A9
00E1    0095
00EC    00A9
00F5    00D3
00FA    01BE
010F    01BF
0114    00D4
0122    00D3
012A    00D4
0132    00B8
013E    0095
0149    00A9
0175    01B8
01C9    0163
01D1    0150
01DB    0163
01E3    0150
```

Several target offsets coincide with the offset-word fields of far-call instructions in the raw resource bytes. This is consistent with the SDK's broad note that its runtime emits kernel far-call and resource relocations, but the exact mapping of source class 0/type 0 to a particular loader operation must still be confirmed from the original 1.x loader/kernel implementation. Do not treat the pre-relocation segment words in the file as runtime segment values.

### 12.3 BANNER comparison

BANNER resource 1 has size 0x0100, relocation bytes 0x006C (27 records), and flags 0x0080. Its first two records also have info bytes 0x11 and 0x12 and import index 0 (`ui`). Additional records include import index 1 (`spool`) and source-class-2 relocations.

BANNER resource 2 has size 0x1040, relocation bytes 0x0220 (136 records), and flags 0x0A72. Its much larger relocation set includes source classes 0, 1 and 2. This provides a second application specimen with the same first-resource flag group and first two UI import relocation encodings.

### 12.4 Resource flags observed in BOUNCE and BANNER

| Resource group | BOUNCE flags | BANNER flags |
|---|---:|---:|
| R0 | 0x0880 | 0x0880 |
| R1 | 0x0080 | 0x0080 |
| R2 | 0x0A72 | 0x0A72 |
| Further resources | 0x145A / 0x1C7A | 0x145A / 0x087A / 0x1C7A |

The repeated values are useful classification evidence. Their full bit-level semantics are not established by this comparison. Do not name the flags (fixed, shared, discardable, code, data, etc.) without a target-matched definition or loader trace.

### 12.5 Header library-entry field

The parser currently exposes the two WORDs at header-tail offsets +44 and +46 as `library_entry`. Both BOUNCE and BANNER yield (offset 0, resource 0). This is only the parser's current field label and raw value. It has **not** been established that this is the application's process entry point, or that its semantics are the same for applications and libraries. Do not use (0,0) as a GEOTEST entry point without further header/loader evidence.

### 12.6 Current confidence and open questions

Confirmed by raw bytes and parser calculations:

- BOUNCE R1: 9 relocation records, including two import-index-0 records and six source-class-2 records with extra 0.
- BOUNCE R2: 29 records, all info 0x00.
- BANNER R1 begins with the same 0x11 / 0x12 encodings for import `ui`.
- BOUNCE and BANNER share flags 0x0880, 0x0080 and 0x0A72 for their first three resource IDs.
- BOUNCE R2 begins at file offset 0x02B0.

Not established:

- The exact loader semantics of relocation types 0, 1, 2 and 3 in every source class.
- The semantic role of BOUNCE R1 (including whether it contains a process object, an application object, or a startup descriptor).
- The meaning of all resource flag bits.
- Whether the header field exposed as `library_entry` is an application entry point.
- Which resources are essential to launch versus loaded later.

### 12.7 Next investigation

1. Trace source-class-0 relocations against the exact GeoWorks 1.x kernel/loader relocation dispatcher.
2. Trace import-index-0 relocations to the actual imported `ui` symbols/ordinals and protocol checks.
3. Decode BOUNCE R1's structures at resource-relative offsets 0x0040–0x007A and compare with BANNER R1.
4. Identify process/application object structures using confirmed PC/GEOS 1.x definitions, not later 2.x assumptions.
5. Resolve the application-versus-library meaning of the header-tail entry fields.
6. Only after these steps identify the minimal startup resource set for GEOTEST.

No GEOTEST binary was built or runtime-tested in this pass. The original four GEO files and SDK parser source remain unchanged.
