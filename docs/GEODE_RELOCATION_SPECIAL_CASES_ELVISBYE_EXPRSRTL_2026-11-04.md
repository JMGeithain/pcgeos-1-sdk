# PC/GEOS 1.x – ELVISBYE.GEO / EXPRSRTL.GEO relocation special-case audit

Date: 2026-11-04  
Status: static byte analysis; no runtime validation  
Scope: GeoWorks / PC/GEOS 1.x only. No inference from PC/GEOS 2.x or FreeGEOS.

## Question

Determine what the unusual relocation info bytes `DDh` and `63h` mean in resource 10 of `ELVISBYE.GEO` and `EXPRSRTL.GEO`, compared with `SENDFAX2.GEO`.

## Provenance

All three files were read unchanged from `GEOWORKS(4).zip`.

| Archive member | Bytes | SHA-256 |
|---|---:|---|
| `.../ELVIS/ELVISBYE.GEO` | 4,240 | `880f61d25a3728574df74ec524bc2d589ead610511ca507cc8eb2410c2780eb8` |
| `.../EXPRESS/EXPRSRTL.GEO` | 4,240 | `ee8b1fc7a2b1185a3773a2b86d62888350fe64dae94efb1daff33c9fd010ebfb` |
| `.../SENDFAX/SENDFAX2.GEO` | 4,240 | `bcf55d2381a42f9fc6b5559a60d1bc753e4fe27a3bf54df901801eec50777bf5` |

## Resource 10 and the four-byte relocation record

Resource 10 starts at file offset `0C98h`; its declared size is `03F0h`. The relocation stream therefore begins at file offset `1088h` (`0C98h + 03F0h`). In these files it contains four bytes, i.e. one four-byte record.

| File | Bytes at `1088h` | Info | Extra | Offset word |
|---|---|---:|---:|---:|
| ELVISBYE.GEO | `DD 02 DD 02` | `DDh` | `02h` | `02DDh` |
| EXPRSRTL.GEO | `63 02 63 02` | `63h` | `02h` | `0263h` |
| SENDFAX2.GEO | `23 00 00 00` | `23h` | `00h` | `0000h` |

Each row is one four-byte record, not two records. The split into info byte, extra byte and 16-bit offset follows the four-byte record model used in the prior 1.x analysis. `23h` is already associated with `GRS_RESOURCE / GRT_CALL` in the earlier original-file audit. The semantics of `DDh` and `63h` remain unproven.

## The 68-word repeated sequence

In the initialized resource data, offsets `0368h–03EFh` contain 136 bytes, or 68 little-endian words:

- ELVISBYE: 68 copies of `DD 02`, i.e. word value `02DDh`.
- EXPRSRTL: 68 copies of `63 02`, i.e. word value `0263h`.
- SENDFAX2: a heterogeneous sequence at the same location, not 68 copies of one word.

The two target offsets lie within resource 10:

- ELVIS target `02DDh`: `0D 80 0D 00 D8 00 D0 0D DD 00 D0 0D D0 0D 00 D0 ...`
- EXPRESS target `0263h`: `88 00 FE DD 17 D0 0D 80 0D 00 D8 00 D8 0D DD 08 ...`

This is a strong structural correlation: the 68 data words repeat the same offset value found in the corresponding single relocation record. The 68-word sequence is initialized resource data, not the relocation stream. Whether it is a special offset/pointer array, compressed data structure, or another application-specific table is not established.

## Resource comparison

The resource-10 bytes of ELVISBYE and EXPRSRTL are identical except for the 68 words in `0368h–03EFh`, where `02DDh` is replaced by `0263h`. Their single relocation records correspondingly differ in the info byte and offset word.

SENDFAX2 shares portions of resource 10, including the inspected sequence beginning at `0348h`, but has a different structure from `0368h` onward and the comparison record `23 00 00 00`.

## Formal nibble split and evidence limit

Nachtrag 1045 records that `GRI_SOURCE` is the upper nibble and `GRI_TYPE` the lower nibble. Thus:

- `DDh` → source nibble `Dh`, type nibble `Dh`.
- `63h` → source nibble `6h`, type nibble `3h`.
- `23h` → source nibble `2h`, type nibble `3h`.

The values `DDh` and `63h` are outside the subset semantically assigned so far from the examined GeoWorks 1.x original files. Their meaning is **OPEN**. The nibble split alone proves neither that they are valid loader operations nor that the files are damaged. Loader acceptance cannot be confirmed without tracing the original 1.x loader or performing a controlled runtime test.

## Unconfirmed working hypothesis

The match between the 68 repeated offset words and the offset word in the corresponding relocation record may indicate an application-specific offset table pointing to one shared data block, while the relocation record describes a special resource relationship. This is only a hypothesis. We have not yet shown how the 68 words are consumed at runtime or how the loader interprets `GRI_info=DDh` / `63h`.

## Next checks

1. Reconcile resource 10 with every resource-directory entry and establish the meaning of the extra byte `02h`.
2. Search the other ELVISBYE and EXPRSRTL resources for references or consumers of `0368h–03EFh` and targets `0263h` / `02DDh`.
3. Compare the identical code/data areas of both applications and inspect the 68-word sequence in the context of its consumers.
4. Search more hash-identified GeoWorks 1.x originals for `GRI_info=DDh` and `63h`.
5. Trace the original 1.x loader path for relocation info bytes before implementing any parser rule or SDK exception.
6. Only after static clarification consider a controlled runtime test on a disposable working copy.

## SDK consequence

The parser must neither silently accept `DDh` and `63h` as ordinary relocation types nor reject them as definitely invalid at this stage. Record them as open special cases. No parser change and no patch to original files follows from this audit.

## Reproducibility and limits

The three archive members were read directly from the ZIP; sizes, SHA-256 values, raw bytes and difference ranges were recalculated. Resource 10's relocation position is derived from `0C98h + 03F0h = 1088h`. The 68 word values were counted as 16-bit little-endian words over `0368h–03EFh`. This is static byte analysis, not a GeoManager loader test or a complete GEODE specification.


## Archive-wide search for the two 68-word sequences

An additional search was run across the complete `GEOWORKS(4).zip` archive:

- Scope: 263 archive members with the `.GEO` extension.
- Exact contiguous 136-byte patterns searched:
  - `DD 02` repeated 68 times.
  - `63 02` repeated 68 times.
- Result: the first complete pattern occurs only in `ELVISBYE.GEO`; the second occurs only in `EXPRSRTL.GEO`.
- Neither complete pattern was found in the other 261 GEO files.

**Evidence limit:** This is an exact-pattern search for these two complete 136-byte sequences. It is not a complete decoder of all relocation tables and does not establish that the archive contains no other unknown `GRI_info` values. In particular, it does not semantically classify all individual occurrences of bytes `DDh` or `63h`.
