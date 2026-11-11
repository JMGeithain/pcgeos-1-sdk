# GeoWrite 1.x – Identifikation der variablen Seitenverweise als ObjRelocationIDs (Untersuchung 2406)

## Ergebnis

Die veränderlichen WORD-Werte in den Seiten-Chunks `0022h` und `0030h` von `SOLAR_DE.000` sind im Format einer GEOS-`ObjRelocationID` codiert. Die Zuordnung folgt aus drei unabhängigen Quelltextbelegen:

1. `Source/reference/object.def` definiert `ObjRelocationID` als Bitfeld mit `RID_SOURCE:4` und `RID_INDEX:12`.
2. Dieselbe Datei listet `ORS_NON_STATE_VM` als Relokationsquelle auf; deren Index ist ausdrücklich ein VM-Index, dessen VM-Dateihandle im Blockheader gespeichert ist.
3. `Source/showcase-format/public-source/convertText.asm` enthält `RelocToVMBlock`. Die Routine maskiert den übergebenen WORD mit `mask RID_INDEX`, multipliziert den Index mit `size VMBlockHandle` und addiert `offset VMH_blockTable`, um die Position des zugehörigen VM-Blockhandles in der VM-Blocktabelle zu berechnen.

## Bitfeld-Dekodierung

Die untersuchten WORD-Werte lauten:

| Hex-Wert | RID_SOURCE | RID_INDEX |
|---|---:|---:|
| `7004h` | `7` | `004h` |
| `7047h` | `7` | `047h` |
| `7049h` | `7` | `049h` |
| `704Bh` | `7` | `04Bh` |
| `706Dh` | `7` | `06Dh` |

Die Quellen-Enumeration zählt `ORS_NULL` ab 0. Damit ist der Quellenwert 7 `ORS_NON_STATE_VM`. Der untere 12-Bit-Index ist der von `RelocToVMBlock` verwendete `RID_INDEX`.

## Fundstellen im Dokument

In Chunk `0022h` (104 Bytes) erscheinen die variablen Relokations-WORDs zweimal:
- Payload-Offset `0x4C`
- Payload-Offset `0x56`

In Chunk `0030h` (89 Bytes) erscheint derselbe seitenabhängige WORD-Wert einmal:
- Payload-Offset `0x17`

Die Wertefolge über die Seiten 1–21 ist:
`7004h, 7047h, 7049h, 704Bh, 704Dh, 704Fh, 7051h, 7053h, 7055h, 7057h, 7059h, 705Bh, 705Dh, 705Fh, 7061h, 7063h, 7065h, 7067h, 7069h, 706Bh, 706Dh`.

Die Werte in allen drei Feldern stimmen je Seite überein. Die Veränderung ist daher keine einfache Seitennummer im Objektinhalt, sondern eine seitenweise andere Relokationskennung mit Quelle `ORS_NON_STATE_VM`.

## Zusammenhang mit dem GeoWrite-Konverter

In `convertGeoWrite.asm` liest der Konverter die Seiteninhaltsstruktur:
- `GW12_PageContent = 22h`
- `Vis_offset`
- `VCI_comp.CP_firstChild.offset`
- anschließend `VI_link.LP_next`

Im Haupttext-/Spaltenpfad wird der nächste Link als WORD-Paar gelesen, die vorherige VM-Sperre aufgehoben und bei einem Nicht-Parent-Link `RelocToVMBlock` aufgerufen. Der Quelltext bestätigt damit, dass Relokationskennungen in der visuellen Seitenobjektverkettung erwartet und in VM-Blockhandles aufgelöst werden.

Wichtige Einschränkung: Der Quelltext erklärt die allgemeine Relokationsmechanik. Er benennt nicht einzeln, welches konkrete Zielobjekt jedes der drei in `SOLAR_DE.000` beobachteten Felder referenziert. Die Identifikation als ObjRelocationID / `ORS_NON_STATE_VM` ist durch Bitfelddefinition und Umsetzungsroutine gestützt; die semantische Rolle der jeweiligen Referenz innerhalb der Seitenstruktur bleibt noch zu untersuchen.

## Bedeutung für den Generator

Für einen nativen GeoWrite-Dokumentgenerator dürfen diese WORDs nicht als beliebige Zahlen oder als direkte VM-Blockhandles behandelt werden. Es sind relocationscodierte Verweise. Die Zielindizes müssen zu den Einträgen der VM-Blocktabelle der erzeugten Datei passen und beim Speichern/Öffnen korrekt aufgelöst werden.

Das ist ein wichtiger Hinweis für den geplanten GEOTEST-Generator: Ein bloßes Kopieren der Beispielwerte in ein neu aufgebautes VM-Dokument wäre nicht zuverlässig, wenn die zugehörigen Blocktabelleneinträge nicht dieselbe Zuordnung besitzen.

## Quellen

- `Source/reference/object.def`, Abschnitt `ObjRelocationSource` und `ObjRelocationID` (Quelltextzeilen 453–482 im Archivstand).
- `Source/showcase-format/public-source/convertText.asm`, Routine `RelocToVMBlock` (Quelltextzeilen 572–614).
- `Source/showcase-format/public-source/convertGeoWrite.asm`, Seitenverarbeitung `pageLoop` / `columnLoop` (Quelltextzeilen 148–215).
- `Showcase/Deutsch/GeoWrite/SOLAR_DE.000`, Seitenblöcke 1–21.

## Grenzen

Statische Dateianalyse und Quelltextabgleich. Es wurde kein Laufzeittest ausgeführt. Die konkreten Zielobjekte der Relokationsindizes und die genaue Feldzuordnung innerhalb der Seitenobjektverkettung sind noch nicht abschließend identifiziert.
