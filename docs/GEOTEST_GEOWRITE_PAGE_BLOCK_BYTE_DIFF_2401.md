# GEOTEST – Byteweiser Vergleich der drei GeoWrite-Seitenblöcke (2401)

Stand: 2026-11-11

## Quelle und Reproduzierbarkeit

- Eingabepaket: `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`
- Dokument: `Showcase/Deutsch/GeoWrite/SOLAR_DE.000`
- VM-Blöcke: `005Ch`, `0380h`, `0398h`
- Parser: `Source/showcase-draw/vm1.py` und `Source/common.py`
- Die drei VM-Blöcke wurden erneut direkt aus der nativen Datei gelesen und ihre LMem-Chunks anhand der Handle-Tabelle extrahiert.

## 1. Korrigierte Gesamtübersicht

Jeder der drei Seitenblöcke hat:
- 848 Byte VM-Blockgröße
- VM-Flag `01FFh`
- LMem-Handle-Tabellenoffset `0020h`
- 38 Handle-Slots
- 18 tatsächlich belegte Chunk-Payloads

Die Unterscheidung zwischen 38 Slots und 18 belegten Chunks ist wichtig.

## 2. Byteweiser Vergleich aller 18 belegten Chunks

| Chunk-Handle | Größe | Vergleich Seite 1/2/3 | Byteunterschiede ggü. Seite 1 |
|---:|---:|---|---:|
| `0020h` | 38 | identisch | 0 / 0 |
| `0022h` | 104 | unterschiedlich | 2 / 2 |
| `0024h` | 89 | identisch | 0 / 0 |
| `0026h` | 1 | identisch | 0 / 0 |
| `0028h` | 18 | identisch | 0 / 0 |
| `002Ah` | 18 | identisch | 0 / 0 |
| `002Ch` | 14 | identisch | 0 / 0 |
| `002Eh` | 18 | identisch | 0 / 0 |
| `0030h` | 89 | unterschiedlich | 1 / 1 |
| `0032h` | 28 | unterschiedlich | 1 / 1 |
| `0034h` | 18 | identisch | 0 / 0 |
| `0036h` | 18 | identisch | 0 / 0 |
| `0038h` | 14 | identisch | 0 / 0 |
| `003Ah` | 18 | identisch | 0 / 0 |
| `003Ch` | 10 | identisch | 0 / 0 |
| `003Eh` | 143 | identisch | 0 / 0 |
| `0040h` | 10 | identisch | 0 / 0 |
| `0042h` | 39 | identisch | 0 / 0 |

Ergebnis: 15 der 18 belegten Chunks sind byteidentisch in allen drei Seitenblöcken. Nur drei Chunks unterscheiden sich: `0022h`, `0030h` und `0032h`. Alle 18 Chunks haben in den drei Seiten dieselbe Länge.

## 3. Exakte Seitenunterschiede

### Chunk 0032h – Seitenkennzeichnung

Der 28-Byte-Chunk enthält:
- Seite 1: `Unser Sonnensystem  |  1/21\0`
- Seite 2: `Unser Sonnensystem  |  2/21\0`
- Seite 3: `Unser Sonnensystem  |  3/21\0`

Hier unterscheidet sich genau ein Byte zwischen Seite 1 und 2 sowie Seite 1 und 3: das ASCII-Ziffernbyte der Seitenzahl.

### Chunk 0030h

Der Chunk ist 89 Byte lang. Zwischen Seite 1 und Seite 2 gibt es genau eine Byteabweichung; zwischen Seite 1 und Seite 3 ebenfalls genau eine. Die Abweichungen liegen im Bereich des eingebetteten Binärinhalts; eine semantische Feldzuordnung wird ohne Klassen-/Strukturdefinition nicht behauptet.

### Chunk 0022h

Der Chunk ist 104 Byte lang. Zwischen Seite 1 und Seite 2 gibt es genau zwei Byteabweichungen; zwischen Seite 1 und Seite 3 ebenfalls genau zwei. Die Änderungen sind lokal und lassen den Chunkumfang unverändert. Die genaue Bedeutung dieser zwei Bytepaare bleibt offen.

## 4. Was aus dem Vergleich folgt

**Direkt nachgewiesen:**
1. Die drei Seitenblöcke verwenden dieselbe LMem-Chunk-Belegung und dieselben Chunkgrößen.
2. 15 von 18 belegten Chunks sind in allen drei Blöcken byteidentisch.
3. Drei Chunks enthalten seitenabhängige Bytes.
4. Die sichtbare Seitenkennung ist eine separate Zeichenfolge in Chunk `0032h`.
5. Die Seitenblöcke sind keine unabhängigen, völlig verschiedenen Datenstrukturen; sie sind sehr ähnliche Instanzen eines gemeinsamen Layouts.

**Nicht nachgewiesen:**
- Die Objektklassen und semantischen Rollen der Chunks `0022h` und `0030h`.
- Ob die 15 identischen Chunks in allen 21 Seiten identisch sind.
- Ob die 15 gemeinsamen Chunks für ein Minimaldokument zwingend sind.
- Ob sich die drei veränderlichen Chunks auf reine Seitennummerierung, Layout oder andere Seiteneigenschaften beziehen.

## 5. Konsequenz für GEOTEST

Der Vergleich ist ein guter Ansatzpunkt für die Suche nach einer minimalen Seitenstruktur: Ein Großteil des 848-Byte-Seitenblocks ist in den ersten drei Seiten bytegleich. Das beweist aber noch nicht, dass diese gemeinsamen Chunks für eine neue Anwendung übernommen werden dürfen oder dass sie alle benötigt werden.

Ein GEOTEST-Dokument sollte nicht durch ungeprüftes Klonen eines GeoWrite-Seitenblocks erzeugt werden. Die Klassen-/Objektbezüge müssen zuerst identifiziert werden.

## 6. Nächste Schritte

1. Die konkreten Offsets der Abweichungen in `0022h` und `0030h` protokollieren und als little-endian Felder prüfen.
2. Dieselbe Chunk-Differenzprüfung über weitere Seitenblöcke (z. B. Seiten 4–6) durchführen.
3. Die Chunks `0022h` und `0030h` gegen die historischen Strukturen und die WRITE.GEO-Codepfade abgleichen.
4. Erst danach eine minimale, sichere Seitenstruktur für GEOTEST ableiten.

## Status

Statische Byteanalyse. Keine Datei verändert, kein Laufzeittest und kein GEOTEST-Dokument erzeugt.
