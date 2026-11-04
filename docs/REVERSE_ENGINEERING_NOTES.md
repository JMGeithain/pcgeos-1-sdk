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
