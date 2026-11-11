# GEOTEST – GeoWrite-Mapblock und Generator-Schreibpfade (2398)

Stand: 2026-11-11

## Ziel

Die vier aktiven Chunks im Map-LMem-Block von `SOLAR_DE.000` werden bytegenau dokumentiert und mit den tatsächlich vom mitgelieferten Generator veränderten VM-Blöcken abgeglichen. Ziel ist, nicht belegte Chunk-Namen zu vermeiden und den kleinsten sicher bekannten Schreibumfang zu bestimmen.

## Untersuchte Datei und Prüfbasis

- `Showcase/Deutsch/GeoWrite/SOLAR_DE.000` aus `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`
- Größe: 316.084 Byte
- VM-Dateisignatur: `ADEBh` bei Datei-Offset `00C8h`
- VM-Headergröße: `0554h`
- VM-Headerposition: `04CD60h`
- Map-Block-Handle: `0044h`

Die Datei wurde mit dem im Paket enthaltenen `Source/showcase-draw/vm1.py` eingelesen. Die LMem-Chunk-Offsets wurden aus der Handle-Tabelle und den unmittelbar vor den Payloads stehenden Längenwörtern gelesen.

## 1. Map-LMem-Block

Der VM-Block `0044h` ist 880 Byte groß. Sein LMem-Header zeigt:
- Handle-Tabellenoffset: `0018h`
- Chunk-Slot-Anzahl: `0010h` (16)
- Heapgröße: `036Ch` (876 Byte)

Aktive Slots:

| Chunk-Handle | Payloadgröße | Payload-Anfang (relativ zum LMem-Block) |
|---:|---:|---:|
| `0018h` | 16 Byte | `0028h` |
| `001Ah` | 634 Byte | `003Ch` |
| `001Ch` | 91 Byte | `02D8h` |
| `001Eh` | 64 Byte | `0338h` |

Die Slots `0020h` bis `0036h` sind in dieser Datei leer. Die vier aktiven Chunks sind damit unmittelbar aus der Handle-Tabelle bestätigt. Ihre vollständige semantische Benennung bleibt offen.

## 2. Chunk 001Eh: sichtbare WORD-Felder

Die 64-Byte-Payload des Chunks `001Eh` lautet:

`44 58 00 01 09 00 00 00 00 00 48 00 48 00 48 00 48 00 00 40 38 00 2C 00 74 00 68 00 F0 00 00 64 02 18 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00`

Als WORDs an geraden Offsets interpretiert:

| Chunk-Offset | WORD |
|---:|---:|
| `00h` | `5844h` |
| `02h` | `0100h` |
| `04h` | `0009h` |
| `0Ah` | `0048h` |
| `0Ch` | `0048h` |
| `0Eh` | `0048h` |
| `10h` | `0048h` |
| `12h` | `4000h` |
| `14h` | `0038h` |
| `16h` | `002Ch` |
| `18h` | `0074h` |
| `1Ah` | `0068h` |
| `1Ch` | `00F0h` |
| `1Eh` | `6400h` |
| `20h` | `1802h` |
| `22h` | `0003h` |

Die Werte `0038h`, `002Ch`, `0074h` und `0068h` entsprechen VM-Handle-IDs, die in der VM-Header-Tabelle der Datei tatsächlich vorhanden sind. Die Übereinstimmung ist ein starker Hinweis, dass dieser Chunk VM-Blockreferenzen enthält. Die Bedeutung und Feldnamen der einzelnen WORDs sind damit aber noch nicht bewiesen.

## 3. Tatsächliche VM-Blöcke und Generatorzugriffe

Die VM-Header-Tabelle der Datei enthält unter anderem diese Blöcke:

| VM-Handle | Größe | LMem-Kennzeichnung | Generator |
|---:|---:|---|---|
| `002Ch` | 192 Byte | LMem | wird geladen und geändert |
| `0038h` | 144 Byte | LMem | wird geladen und geändert |
| `0044h` | 880 Byte | LMem | Mapblock; vom Generator nicht geändert |
| `0050h` | 1.856 Byte | LMem | wird geladen und geändert |
| `005Ch` | 848 Byte | LMem | im Generator nicht verändert |
| `0068h` | 48 Byte | LMem | im Generator nicht verändert |
| `0074h` | 688 Byte | LMem | wird geladen und geändert |

Direkt aus `native_write.py`:
- `main = LMem(vm.entries[0x50]['data'])`
- `char_styles = LMem(vm.entries[0x38]['data'])`
- `para_styles = LMem(vm.entries[0x2c]['data'])`
- `graphics = LMem(vm.entries[0x74]['data'])`

Die Änderungsliste lautet exakt:
`{0x50: main.build(), 0x38: char_styles.build(), 0x2c: para_styles.build(), 0x74: graphics.build()}`

Der Generator ersetzt somit vier VM-Blöcke. Der Mapblock `0044h` wird nicht neu aufgebaut und nicht überschrieben. Die nicht bearbeiteten VM-Blöcke bleiben aus dem Template erhalten.

## 4. Bedeutung für die vorherige Analyse

Die vier aktiven Map-LMem-Chunks `0018h`, `001Ah`, `001Ch` und `001Eh` dürfen nicht mit den vier vom Generator bearbeiteten VM-Blöcken `002Ch`, `0038h`, `0050h` und `0074h` verwechselt werden. Das sind zwei unterschiedliche Ebenen:
- Mapblock: ein LMem-VM-Block mit eigenen Chunk-Handles.
- Dokumentinhalt: mehrere separate VM-Blöcke, die der Generator gezielt bearbeitet.

Der Generator liefert damit ein wichtiges Indiz für einen sicheren Änderungsumfang: Er bewahrt den vorhandenen Mapblock und ersetzt nur die vier Dokumentdatenblöcke, deren Strukturen er gezielt kennt.

## 5. Grenzen

- Die semantischen Namen der vier Map-LMem-Chunks sind nicht bewiesen.
- Die Felder in Chunk `001Eh` sind anhand ihrer Werte beschrieben; die Felddefinitionen wurden nicht abschließend aufgelöst.
- Dass die Werte `0038h`, `002Ch`, `0074h`, `0068h` VM-Handle-IDs sind, ist durch die VM-Tabelle gestützt. Welche Objekt-/Datenrolle jeder Block hat, muss weiter untersucht werden.
- Der Generator startet von `original/GWSVGA/DOCUMENT/NEW_DOCU.000`. Diese Baseline-Datei ist im bereitgestellten ZIP nicht enthalten. Der Generator ist aus dem ZIP allein daher nicht vollständig reproduzierbar.

## 6. Nächster Schritt

Die vier Map-Chunks werden nun mit dem originalen GeoWrite-1.2-Code und den VM-Handle-Zugriffen in `WRITE.GEO` verglichen. Vorrang hat Chunk `001Eh`, da er mehrere tatsächlich vorhandene VM-Handles enthält. Danach werden die großen Chunk-Payloads `001Ah` und `001Ch` auf interne Strukturen untersucht.

## Status

Statische Prüfung der bereitgestellten nativen GeoWrite-Datei und des Generatorquellcodes. Keine Änderung am Dokument oder an GeoWorks-Binärdateien. Kein GEOTEST-Prototyp erstellt oder getestet.
