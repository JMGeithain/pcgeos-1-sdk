# GEOTEST – GeoWrite als Referenz für native Dokumente (2375)

Stand: 2026-11-10

## Verbindliche Projektabgrenzung

Ziel ist eine kleine native GeoWorks / PC/GEOS 1.x Testanwendung `GEOTEST.GEO`, die eine **eigene native PC/GEOS-Dokumentdatei** erzeugt, speichert und wieder öffnet. Die Datei soll im GeoManager mit einem eigenen Dokument-Icon erscheinen.

Es wird aktuell kein Grafiktreiber entwickelt oder verändert.

Wichtige Unterscheidung nach Hinweis des Nutzers:
- `NOTEPAD.GEO` bearbeitet DOS-ASCII-Dateien. Es ist keine Vorlage für native PC/GEOS-Dokumentdateien.
- GeoWrite erzeugt und bearbeitet anwendungseigene PC/GEOS-Dokumente. `WRITE.GEO` ist daher der richtige erste Referenzkandidat für den nativen Dokument-Lifecycle.

PC/GEOS 2.x / FreeGEOS-Dokumentklassen und ABI-Details werden nicht als Beleg für GeoWorks 1.x verwendet.

## Statische Inventur von WRITE.GEO

Untersuchte Originaldatei: `GEOWORKS/WORLD/WRITE.GEO` aus dem vom Nutzer bereitgestellten `GEOWORKS.zip`.

- Größe: 73.110 Bytes
- SHA-256: `0d2958b810948603d15e412a61598623b9a4ccb73cfeb9fbe08d50ee718a6fd0`
- GEOS-1.x-Geode
- Kernel-Protokoll 622.3
- Geode-Protokoll 509.0
- Geode-Release 1.2.8.3
- Permanentname `write`, Extension `app`
- 36 Ressourcen
- 3 Imports:
  - `ui`, Protokoll 693.0
  - `spool`, Protokoll 613.0
  - `spell`, Protokoll 2.0

Ressourceninventur (Dateioffsets, Größen und Flags):

| Ressource | Offset | Größe | Flags | Relocations |
|---:|---:|---:|---:|---:|
| 0 | 02F2h | 0 | 0880h | 0 |
| 1 | 02F2h | 2512 | 0080h | 379 |
| 2 | 12AEh | 6640 | 0A72h | 308 |
| 3 | 316Eh | 6688 | 0A72h | 202 |
| 4 | 4EB6h | 5248 | 0A72h | 239 |
| 5 | 66F2h | 4256 | 0A72h | 142 |
| 6 | 79CAh | 960 | 0A72h | 38 |
| 7 | 7E22h | 2304 | 0A72h | 26 |
| 8 | 878Ah | 3440 | 0A72h | 125 |
| 9 | 96EEh | 1056 | 145Ah | 1 |
| 10 | 9B12h | 16 | 001Ah | 0 |
| 11 | 9B22h | 1648 | 087Ah | 1 |
| 12 | A196h | 608 | 087Ah | 1 |
| 13 | A3FAh | 768 | 145Ah | 1 |
| 14 | A6FEh | 240 | 0C7Ah | 1 |
| 15 | A7F2h | 80 | 0C7Ah | 1 |
| 16 | A846h | 96 | 0C7Ah | 1 |
| 17 | A8AAh | 48 | 0C7Ah | 1 |
| 18 | A8DEh | 48 | 0C7Ah | 1 |
| 19 | A912h | 528 | 0C7Ah | 1 |
| 20 | AB26h | 1376 | 087Ah | 1 |
| 21 | B08Ah | 128 | 041Ah | 1 |
| 22 | B10Eh | 1920 | 145Ah | 1 |
| 23 | B892h | 3344 | 145Ah | 1 |
| 24 | C5A6h | 3440 | 145Ah | 1 |
| 25 | D31Ah | 3600 | 145Ah | 1 |
| 26 | E12Eh | 272 | 1C7Ah | 1 |
| 27 | E242h | 384 | 1C7Ah | 1 |
| 28 | E3C6h | 496 | 1C7Ah | 1 |
| 29 | E5BAh | 1328 | 1C7Ah | 1 |
| 30 | EAEEh | 752 | 1C7Ah | 1 |
| 31 | EDE2h | 2048 | 1C7Ah | 1 |
| 32 | F5E6h | 2240 | 145Ah | 1 |
| 33 | FEAAh | 2528 | 145Ah | 1 |
| 34 | 1088Eh | 5040 | 145Ah | 1 |
| 35 | 11C42h | 336 | 145Ah | 1 |

The resource flags show a substantial code-resource group and many LMem/object/UI resources. This is consistent with a full document application, but the exact role of each resource is not yet assigned.

## Strings confirmed in resources

Static ASCII-string extraction found:
- Resource 6: `geoWrite`
- Resource 12: messages about importing/saving ASCII text files
- Resource 21: `Write unbenannt`
- Resource 34: labels such as `Format abrufen`, `Format merken`, `Speichern in ASCII-Textdatei`, `Einlesen aus ASCII-Textdatei`
- Resource 35: `GeoWrite`

These strings prove that WRITE.GEO includes GeoWrite UI and ASCII import/export operations. They do **not** by themselves identify the native document format or its document icon.

## NOTEPAD.GEO correction

The earlier candidate `GEOWORKS/WORLD/NOTEPAD.GEO` is not a native-document template. It uses DOS-ASCII files (including the `notiz.txt` string) and must not be used to infer GEOTEST's native document structure. Its UI/file-selector patterns may be examined separately if needed, but they are outside the native document-format investigation.

## Starker Befund: GeoWrite- und GeoDraw-Dokument-Token

Ein byteweiser Vergleich mit der ebenfalls vorhandenen nativen Anwendung `DRAW.GEO` zeigt eine wiederkehrende Token-Anordnung in Objektressourcen:

| Anwendung | App-Token im Geode-Header (Offset 0014h) | Token-Paar in Objektressource |
|---|---|---|
| GeoWrite / `WRITE.GEO` | `WP00` | `WDAT\0\0 WP00\0\0` |
| GeoDraw / `DRAW.GEO` | `DP00` | `DDAT\0\0 DP00\0\0` |

Exakte Fundstellen:
- `WRITE.GEO`: Ressource 9, Datei-Offset `9A4Ch`; `WDAT` beginnt bei `9A4Ch`, `WP00` bei `9A52h`.
- `DRAW.GEO`: Ressource 6, Datei-Offset `27DAh`; `DDAT` beginnt bei `27DAh`, `DP00` bei `27E0h`.
- Die App-Tokens `WP00` und `DP00` stimmen jeweils mit dem Token im Geode-Header bei Offset `0014h` überein.

Das ist ein starker struktureller Hinweis auf ein Paar aus anwendungsspezifischem Daten-/Dokument-Token (`WDAT` bzw. `DDAT`) und zugehörigem App-/Creator-Token (`WP00` bzw. `DP00`). Die genaue Feldsemantik und der Weg, auf dem GeoManager daraus das Dokument-Icon auswählt, sind noch nicht vollständig nachgewiesen. Die Token-Paare dürfen daher noch nicht als vollständige Dokumentregistrierung behandelt werden.

Im aktuellen experimentellen `GEOTEST.GEO` steht das App-Token `GTS1` im Header bei Offset `0014h`. Eine entsprechende zweite Token-Kennung für ein eigenes Dokument wurde im aktuellen Build nicht gefunden. Das bestätigt, dass die bisherige Test-App noch keine nachgewiesene native Dokumentregistrierung enthält.

## What is not yet proven

This pass has not yet identified:
1. GeoWrite's native document filename extension and file header.
2. The exact document class/object class and the message chain for New/Open/Save/Save As/Close.
3. The application token / document type / creator registration consumed by GeoManager.
4. The exact moniker resource and icon variant GeoManager displays for a GeoWrite document.
5. Which minimal subset of this mechanism can be implemented in the current experimental GEOTEST build.

No document format or icon association is inferred from resource numbers, strings, file extensions, or resource sizes alone.

## Next reverse-engineering sequence

1. Map the process and object method tables in WRITE.GEO and identify the document-control objects.
2. Trace New/Open/Save/Save As/Close paths from the UI messages into the native file/VM routines.
3. Follow the exact file-type/token and moniker references from the document object to the icon resource.
4. Inspect a known-good native GeoWrite document file if one can be positively identified in the installation or supplied separately.
5. Compare that document's on-disk structure with the corresponding WRITE.GEO load/save routines.
6. Implement only the minimal proven 1.x mechanism in GEOTEST.GEO, first generating a small document with no icon customization, then add and verify its own icon.
7. Run under the user's GeoWorks 1.2 installation and verify create/save/close/reopen and GeoManager icon display.

## Safety and provenance

- Original `WRITE.GEO`, `NOTEPAD.GEO`, and all other installation files were only read.
- No driver or application binary was modified in this analysis.
- No runtime success is claimed.
- No PC/GEOS 2.x / FreeGEOS ABI or document format has been adopted.
