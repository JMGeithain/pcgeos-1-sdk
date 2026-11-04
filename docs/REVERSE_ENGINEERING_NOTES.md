# Reverse Engineering Notes

The SDK was derived from several concrete PC/GEOS 1.x/2.x investigations.

## Findings that shaped the SDK

- 1.x and 2.x geode containers are structurally different; changing a signature or protocol field is not a valid backport.
- Specific UI and generic UI protocols are meaningful ABI boundaries.
- Imported function ordinals must be validated against the exact target export table; an in-range number still does not prove semantic compatibility.
- Native UI object instance layouts are safer to recover from matching target applications than to guess from later source revisions.
- Native Help in the target can be built from the Viewer's title-bar trigger/hint plus its scrollable help dialog; it is not necessary to imitate Help in application drawing.
- Native GenFileSelector controls provide correct drive/directory behavior and should be preferred to custom browser widgets.
- Modern `-m16` compilation is practical for 386+ systems but needs a carefully isolated native ABI bridge.
- File services should execute on the original GEOS stack, not a compiler-private stack.
- Reproducible builds, input hashes and relocation audits are essential when the historical SDK is not used.

## Later public source trees

Public PC/GEOS source code is valuable for understanding structures and semantics, but it may represent later releases. SDK 0.1 therefore treats the exact target binaries as authoritative for private UI layouts and recovered message/interface details.


## Research contributions planned for the JMGeithain fork

This fork is intended to preserve a strict PC/GEOS 1.x research boundary. Findings from PC/GEOS 2.x, FreeGEOS, or later source trees must never be presented as verified 1.x behavior without independent evidence against a 1.x target.

### Evidence classification

Every reconstructed fact should be tagged with one of these states:

- **Verified on target** — reproduced on a named GeoWorks/Ensemble 1.x installation or directly confirmed from its binary behavior.
- **Static-analysis confirmed** — supported by disassembly, resource inspection, export tables, or repeatable binary comparison, but not yet runtime-tested.
- **Cross-reference only** — suggested by later source code, manuals, symbols, or another GEOS generation; not yet confirmed on 1.x.
- **Hypothesis** — a working explanation that still needs a test.
- **Rejected** — disproved by a repeatable test or contradictory binary evidence.

Each record should include target identity, file name and SHA-256, offset/address, tool and version, method, observation, interpretation, confidence/status, and reproduction steps. Keep raw observations separate from interpretation.

### Existing 1.x research streams to integrate

1. **Kernel and DOS interface research**
   - Preserve separate identities for original and patched KERNEL.EXE, DOS5.GEO, and other system modules.
   - Record provenance and hashes for every binary.
   - Track entry points, callers, register inputs/outputs (AX, BX, CX, DX, SI, DI), stack effects, far/near behavior, and error paths.
   - Do not treat a patched module as evidence of original GeoWorks behavior unless the patch is explicitly accounted for.

2. **Graphics-driver research**
   - Keep display-driver work separate from application UI APIs.
   - Record mode detection, mode tables, setup callbacks, register programming, memory layout, bank switching, palette behavior, and supported hardware assumptions.
   - Current research targets include SVGA16 modes 1024x768x16, 1280x1024x16, and 1280x720x16, plus related VESA/SVGA modes. These are research targets, not claims of support.
   - Retain the known 800x600x16 SVGA8004 baseline as a comparison target.

3. **Mouse-driver and input research**
   - Document the GeoWorks 1.x mouse-driver interface and distinguish it from later wheel-aware interfaces.
   - Track callback tables, data offsets, packet formats, initialization, polling/interrupt behavior, and exact register/stack conventions.
   - Mouse-wheel support remains an investigation target until a native 1.x callback or safe compatibility mechanism is demonstrated.

4. **Tooling and binary-analysis workflow**
   - Document repeatable use of GEODUMP, Ghidra, disassemblers, binary diffing, archive scanning, and SDK inspection.
   - Preserve offsets as file offsets or load/runtime addresses explicitly; never mix these coordinate systems.
   - Store analysis notes and small non-copyright-sensitive test fixtures where licensing permits.

### Compatibility boundary

The research baseline includes GeoWorks 1.2 installations and patched DOSBox/BaseBox test environments. Each environment must be described independently. A successful run under a patched kernel does not establish compatibility with an unmodified installation. PC/GEOS 2.x and FreeGEOS may be used as comparison material only, with every borrowed observation marked **Cross-reference only** until verified on 1.x.

### Contribution rule

No driver register sequence, kernel ordinal, object offset, callback signature, or ABI statement should enter the public API as established fact solely because it appears in a disassembly or later source tree. Require a provenance record and a reproducible validation plan first.

## German GeoWorks 1.2 target — initial binary inventory (2026-11-04)

This is an initial inventory of user-supplied files. It is not yet a completed target profile: the unmodified German kernel has not been supplied in this batch, and runtime compatibility has not been tested.

### Supplied binary identities

SHA-256 values are recorded exactly as calculated from the supplied files:

| File | Size (bytes) | SHA-256 | Initial classification |
|---|---:|---|---|
| `KERNEL(5).EXE` | 72937 | `601d0ba51bbf45508dba1997974fda669928a8cd4478bf6f7557427a21a0d527` | Patched kernel according to prior project provenance; not the original German kernel |
| `DOS5.OLD` | 6392 | `d76e8562da86e7025c839631928c17153d575654121737d9d7e717345118034d` | Original German DOS5 candidate |
| `DOS5(1).GEO` | 6312 | `2b74f591044a5fa02b3a585c7c0392410096e5cd3bd7dd1b1c9d23e7cd7b6a23` | Patched DOS5 candidate |
| `NOTEPAD.GEO` | 8070 | `a1ebd0cb84712a126b1f67f5fd1ca6b57f8bda2e9038e9224ba16ebc008f9ea9` | PC/GEOS 1.x container; internal application name “Notizblock” |
| `SPINTEXT.GEO` | 3764 | `6a9ddda1c491438d29b10c044eb92e5b9e8bd701c922172dd6bb89988e2c1261` | PC/GEOS 1.x container; contains “3D Schrift Demo”, “Geithain” and “www.moellerjaner.de”; do not treat as an unmodified stock skeleton |
| `TERM.GEO` | 63718 | `a62ebc0fb3c01acb4b59c8172d20d520653822a6d42f0bec4831dfdb93e1cf3a` | PC/GEOS 1.x container; internal application name “GeoComm” |
| `VIEWER.GEO` | 59984 | `c884b76cdc4f9119d4794f7830d5438e0abcc1d92d3cc248aa912bde85ed43e7` | PC/GEOS 1.x container; internal application name “Quattro Pro Ansicht” |
| `GEOS(4).INI` | 6960 | `ac83b8aae7381468247eeb805fc86342637ea9178006c892ab47c98d5c15e2da` | Configuration snapshot; GeoWorks 1.2, German keyboard configuration, BaseBox display and absolute-coordinate BaseBox mouse |

### Direct comparison: DOS5

The supplied `DOS5.OLD` and `DOS5(1).GEO` are not identical. Their sizes differ by 80 bytes (6392 versus 6312), and a byte-level comparison shows changes in executable code and message/data regions. The old file contains German disk-related messages, while the candidate patched file contains corresponding English messages. This supports keeping them as separate original and patched test inputs; it does not by itself establish every patch's purpose or runtime effect.

### Container and target cautions

All five supplied `.GEO` files begin with the observed byte signature `C7 45 CF 53`. Record this as a raw observation; do not infer full ABI compatibility from the signature alone.

The supplied `GEOS.INI` selects `BB96_64.GEO` for the active screen and `CTMABS.GEO` for the mouse. It is therefore a BaseBox configuration snapshot, not evidence of operation with physical SVGA hardware.

The supplied `SPINTEXT.GEO` hash does not match the existing SDK 0.1 Pro 1.2 donor hash. Its embedded demo and personal-site strings also make it unsuitable as an assumed stock donor until its provenance and intended role are confirmed.

### Outstanding evidence required

- Obtain the unmodified German `KERNEL.OLD` and calculate its hash. Do not substitute the supplied patched `KERNEL(5).EXE`.
- Confirm the exact installation provenance of the four application GEO files and whether any are locally modified.
- Parse and validate the complete GEODE headers, export/import tables, resource maps, and protocol requirements against the SDK parser.
- Establish a separate German GeoWorks 1.2 target profile only after the kernel and application identities are confirmed.
- Perform runtime tests independently on the unmodified and patched environments. No runtime compatibility claim is made by this inventory.

## External developer report: GNU Chess 6.3.0 on PC/GEOS 1.2 (2026-10-27)

A user-supplied 38-page technical report (English and German editions) describes a source-based GNU Chess 6.3.0 port. Its demonstrated runtime is GeoWorks Pro / Ensemble 1.2 (English), with kernel protocol 622.3 and UI protocol 693.0. The application targets 8088/8086 instructions. The report cites hash-bound native execution evidence, but this SDK repository has not independently rerun those campaigns. It does not establish compatibility with the user's German GeoWorks 1.2 installation, other 1.x releases, or physical 8088 hardware.

### Reusable engineering method

- Separate portable application logic from the old OS boundary; construct the final 1.x geode with a target-specific native writer rather than installing a later runtime or assuming a later SDK ABI.
- Keep two build routes distinct: a quick route reuses a manifest-bound intermediate; a full route recompiles adapted C/C++ using GOC, Open Watcom and Glue (-G 2), then passes that intermediate through the same native 1.x writer. Only the final 1.x output is installed.
- Parse the final output independently from the serializer. Validate ranges, resource indexes, relocation operands and file extent; reject unknown inputs rather than guessing repairs.
- Maintain immutable input/tool hashes, resource and ordinal manifests, target-specific API ledgers, and separate structural, CPU, native-runtime, memory and semantic evidence.
- Treat optrs, handles and chunk IDs as stable identities, not stable addresses. Global block movement and local LMem compaction can invalidate derived segment:offset pointers independently.
- Keep movable code locked for the entire call/return lifetime; reacquire derived addresses after operations that can move storage.
- Explicitly test the 8086 instruction floor, segmented pointers, DS/SS assumptions, calling convention, stack cleanup, register preservation, allocation failure, repeated interactions, focus, expose, resize and shutdown.
- The report's library plan is a proposal, not a demonstrated library implementation: export encoding, loader lifecycle, protocol rules, client isolation, reentrancy and two-client behavior require separate proof.

### Native geode format: case-study data, not a universal 1.x specification

For the report's own writer/parser, a 0x120-byte header is followed by import/export records and four parallel resource arrays. Its formulas are:

    table_start = 0x120 + 14 * L + 4 * E
    payload_start = table_start + 10 * N

For English EN14 (N=63, L=1, E=0), the table begins at 0x12e and the first payload at 0x3a4. Resource payload sizes are paragraph-rounded, but absolute payload positions need not be paragraph-aligned. The four arrays are parallel (sizes WORD, positions DWORD, relocation_sizes WORD, flags WORD), not interleaved records. Relocation records in this implementation use little-endian <BBH>.

These values describe the case-study writer and tested output. They must not overwrite the existing SDK 0.1 GEODE notes. Cross-check each field against original 1.x binaries and the user's target before promoting it to a general format specification.

### Target-specific UI/API evidence for the provisional API ledger

The report audits a native GenText object against its supplied English 1.2 target and a SpinText donor. It records GenTextClass export 86; reference resource 3 / chunk 0x3a; ObjMessage kernel ordinal 0x00a9 with AX=message, BX=live block handle, SI=chunk and DI=0x8000 for synchronous dispatch; text get-all 0x2204; replace-all 0x2200; enable/disable 0x41bc/0x41bd; and focus request 0x208d.

The audited text payload has a five-character maximum. Get-all returns a count in CX without a NUL terminator, so the caller must enforce capacity before copying and append its own terminator. The report says DL=1 selects immediate visible update; value 0 left the old disabled stipple visible despite logical state change. Focus must be explicitly restored after disable/re-enable for the tested input flow.

These are report claims for the audited English 1.2 environment. Put them in a provisional API ledger with provenance and bounded/native case evidence; independently compare ordinals, payload offsets and behavior against the German target before treating them as shared 1.2 contracts.

### Toolchain architecture implications

The report demonstrates a second toolchain route alongside the SDK's current -m16 C approach: adapted C/C++ engine source and GOC scaffold; Open Watcom 16-bit OMF output and Glue -G 2 as an intermediate only; controlled OMF normalization and a strict resource-identity manifest; then a target-specific writer emitting the native 1.x header, object resources, imports, relocations, runtime and bridges; finally an independent parser/auditor and hash-bound tests.

The report's builder is deliberately application-specific: 63 resources, one UI import, a process class/application object, zero public exports, fixed class/messages, and chess-specific memory/asset assumptions. Reuse parsers, serialization discipline, tests and object examples; do not copy those fixed assumptions into the general SDK.

### Limits and follow-up

- The report is not a complete replacement SDK or general GEOS 2.x-to-1.x converter.
- Its native proof is for English GeoWorks Pro / Ensemble 1.2, not German 1.2.
- The report describes prior execution evidence and hash checks; reading the PDF is not a new emulator run.
- It references GNUChess-Ensemble1(1).zip (17,678,481 bytes; SHA-256 0645270262dd21ea7d1b07857725f3d0a941203832b0fa3de8f9ae86cb10f475). The archive itself must be obtained and hash-checked before inspecting or reproducing its source/build pipeline.
- The 0x120 header layout, protocol values, GenText details and writer rules are not universal historical 1.x specifications.

### SDK work items suggested by this report

1. Add a separate application-builder backend/profile instead of merging fixed GNU Chess assumptions into the existing SDK 0.1 builder.
2. Implement a general native 1.x writer only after the independent reader and a minimal native sample pass against exact target binaries.
3. Extend the GEODE parser with named, validated structures for parallel resource arrays and relocation streams, preserving separate 1.x and 2.x schemas.
4. Add symbolic imports/exports and a versioned target API ledger with confidence/provenance.
5. Add object/LMem construction and GenText as separate opt-in modules, with target-specific layout profiles.
6. Add 8086/ABI tests for DS/SS separation, stack/register canaries, movable-resource lock lifetime and adversarial relocation.
7. Keep library generation as a later milestone after export, loader lifecycle, two-client, reentrancy and unload tests exist.
## User-supplied GNU Chess source packages — archive verification (2026-11-04)

Two separate ZIP archives were supplied and inspected locally. ZIP CRC/integrity checks passed for both. Do not conflate their root layouts or release generations:

| Archive | Bytes | SHA-256 | Contents / status |
|---|---:|---|---|
| `GNUChess-Ensemble1.zip` | 17,678,481 | `0645270262dd21ea7d1b07857725f3d0a941203832b0fa3de8f9ae86cb10f475` | 1,760 entries; root prefix `GNUChess-Ensemble1-MoveEntry/`; contains extensive MoveEntry, bilingual and `cpu8086-history12-13` evidence |
| `GNUChess-Ensemble1-DE-EN-8086.zip` | 16,768,589 | `0bf99b6b9aeea212827a275a2680b33483385b41299c7ad640d9bf4917958c5e` | 1,598 entries; root prefix `GNUChess-Ensemble1-8086/`; explicit 8088/8086 release package |

The first archive's size and SHA-256 exactly match the values previously stated in the technical report. The second is a distinct package, not a byte-identical repack: after removing the differing top-level directory prefix, 33 common paths have different contents and 261 / 99 paths are unique to the first / second archive respectively.

### Verified 8086 release artifacts in the second archive

The second archive's `RELEASE.json`, `DEVELOPMENT/source-rebuild-report.json`, `EVIDENCE/cpu8086/acceptance.json`, and actual GEO members agree on these outputs:

| Edition | Release | GEO bytes | SHA-256 |
|---|---:|---:|---|
| English | 6.3.0.12 | 170,028 | `2676a6fb7f2539399a184718cc8aa15b29ab146fe6d5efe281e439ffe31acb70` |
| German | 6.3.0.13 | 170,012 | `4e18a9d01870d7e9b78acf568b5a1b346de19a074dc10c94e0c75ce0b4a10b9e` |

Both archive member files were hashed directly and matched these values. The package reports a source-manifest allowlist of 410 files and an SDK-free rebuild requiring Python 3 standard library plus NASM 2.16 or later. Its optional full engine rebuild uses the separately documented GOC/Glue/Open Watcom route. The package does not include the commercial GEOS runtime, SDK, compiler or fonts.

### CPU and native acceptance — precise scope

The package's acceptance report marks both editions passed for its declared 8086 target. The native run uses the dedicated DOSBox-X 2024.03.01 SDL2 8086 normal core, 640 KiB conventional memory, VGA 640x480/16, `disk.geo` swapping only, and no XMS/EMS/UMB. It records GeoManager launch, mouse and keyboard moves with engine replies, depth 4, Undo/New Game, maximize/resize, expose repaint, close/reopen and native exit to DOS. The maximized incremental-Undo board and genuine full-Expose comparison report zero differing RGB pixels.

This is strong, bounded 8086 instruction-compatibility and native-emulator evidence, not physical 8088/8086 hardware, cycle/bus timing, a minimum-RAM guarantee, or exhaustive chess-position proof. The native run is on the supplied **English** GeoWorks Pro / Ensemble 1.2 system for both English and German applications; a German system runtime was not supplied. The report explicitly says the kernel CPU-type byte and guest heap peaks were not directly observed in this acceptance run.

The opcode verifier is not based on NASM's `CPU 8086` switch alone: its independent raw decoder rejects later-CPU forms that NASM accepts in that mode. The package reports a 207-case independent verifier review and guards known semantic differences such as PUSH SP and unmasked CL shift counts. These are finite verifier/test suites, not an exhaustive formal proof of every instruction path.

### ABI bridge and memory findings

The 8086 package replaces PUSHA/POPA and later conditional-branch encodings with 8086-compatible sequences. Its report describes per-target near-call stubs and a shared movable-resource lock/return bridge. A separate thunk ABI review covers RETF and RETF N cleanup, register/FLAGS preservation, nested resource-lock lifetimes and failure paths. The fixed bridge assumes the engine's private DGROUP remains DS on entry/return; it is not a universal thunk for arbitrary routines returning another DS.

The report's release accounting gives DGROUP 8,400 bytes, arena 34,336 bytes (34,260 used after initialization), stack reservation 49,152 bytes, fixed initialized resources plus stack 127,616 bytes for both editions, and all resource reservations plus stack 214,848 bytes EN / 214,832 bytes DE. These are file-derived reservations and explicitly exclude actual GEOS heap/handle/loader/UI overhead.

### Target/API caution and SDK use

These archives provide excellent reproducible engineering examples for a native 1.x application builder, strict instruction audit, relocation/resource manifest, and movable-code bridge. They do not by themselves establish that their private object layouts, UI messages, ordinals, or kernel details apply unchanged to the user's German GeoWorks 1.2 system. The native test system is English 1.2. Keep GNU Chess's application-specific object and resource assumptions out of the general SDK API until independently cross-checked.

Recommended SDK reuse order: (1) archive/hash and manifest verification; (2) independent GEODE reader and relocation audit; (3) 8086 raw opcode verifier and bounded execution harness; (4) ABI bridge tests as an isolated module; (5) one minimal non-chess application through a general writer; (6) German 1.2 target validation. Do not import the whole GNU Chess application as SDK runtime code.