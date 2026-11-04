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
