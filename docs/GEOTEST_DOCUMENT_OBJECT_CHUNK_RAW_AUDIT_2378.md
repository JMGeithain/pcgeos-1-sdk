# GEOTEST – Rohstruktur des gemeinsamen Dokument-UI-Chunks (2378)

Stand: 2026-11-10

## Ziel

Fortsetzung der ausschließlich auf GeoWorks / PC/GEOS 1.x begrenzten Untersuchung zur nativen Dokumenterzeugung in `GEOTEST.GEO`. Kein Grafiktreiberprojekt. `NOTEPAD.GEO` ist wegen der DOS-ASCII-Dateien keine Vorlage für native GEOS-Dokumentdateien.

## Quellen und Prüfmethode

Read-only untersucht wurden die unveränderten Dateien aus dem vom Nutzer bereitgestellten `GEOWORKS.zip`:

- `GEOWORKS/WORLD/WRITE.GEO`, 73.110 Bytes, SHA-256 `0d2958b810948603d15e412a61598623b9a4ccb73cfeb9fbe08d50ee718a6fd0`
- `GEOWORKS/WORLD/DRAW.GEO`, 31.624 Bytes, SHA-256 `9b980dd04175d3c901835a96bc7b40f7a36f92f0b4fc66f0609300a11d04d70`

Geprüft wurden die Ressourcenbytes, die Chunkgrenzen aus der LMem-Chunktabelle und die Bytepositionen. Es wurde kein Programm ausgeführt und keine Originaldatei verändert.

## 1. Exakte Chunks

| Anwendung | Ressourcenindex | Ressourcendateioffset | Chunk-Tabellenindex (0-basiert) | Chunkoffset relativ zur Ressource | Chunklänge |
|---|---:|---:|---:|---:|---:|
| GeoWrite | 9 | `96EEh` | 29 | `02A6h` | 228 Bytes |
| GeoDraw | 6 | `20B0h` | 46 | `0672h` | 228 Bytes |

Daraus ergeben sich die absoluten Dateioffsets der Chunkanfänge:
- WRITE: `9994h`
- DRAW: `2722h`

Beide Chunks enden am jeweils nächsten Chunkbeginn. Die Länge ist damit nicht aus einem willkürlichen Suchfenster abgeleitet.

## 2. Bytevergleich

Die Chunks sind jeweils 228 Bytes lang. Ein vollständiger Bytevergleich ergibt acht abweichende Positionen; 220 Bytes sind identisch.

| Chunkoffset | WRITE | DRAW |
|---:|---:|---:|
| `000Ch` | `0Ch` | `58h` |
| `000Dh` | `01h` | `00h` |
| `000Eh` | `22h` | `00h` |
| `000Fh` | `10h` | `40h` |
| `00B8h` | `57h` ('W') | `44h` ('D') |
| `00BEh` | `57h` ('W') | `44h` ('D') |
| `00D9h` | `5Ch` | `7Eh` |
| `00DFh` | `15h` | `0Bh` |

Die gemeinsamen Bytes umfassen auch die Tokenumgebung und die nachfolgenden UI-Daten. Der String `Kein Dokument` liegt in beiden Chunks an derselben relativen Position. Er folgt **nicht unmittelbar** auf das Tokenpaar; dazwischen liegen weitere Felder. Diese Präzisierung korrigiert die verkürzte Formulierung aus der vorherigen Zwischenmeldung.

## 3. Token- und Markerpositionen

Innerhalb beider Chunks:
- Offset `00B6h`: Bytes `18 E7`
- Offset `00B8h`: erstes Token, `WDAT` bzw. `DDAT`
- Offset `00BEh`: App-Token, `WP00` bzw. `DP00`

Die Bytefolge `18 E7` kommt in jeder vollständigen Referenz-Geode genau einmal vor und steht jeweils zwei Bytes vor dem ersten Token. Sie ist im aktuellen GEOTEST-Build nicht vorhanden.

Das ist ein präziser Ortsbefund. Die Interpretation als Klassenzeiger, Objekt-ID, Flags oder Registrierungsschlüssel wäre ohne Definition/Codepfad Spekulation und wird ausdrücklich nicht vorgenommen.

## 4. Rohdaten am Chunkanfang

Die ersten 32 Bytes des jeweiligen Chunks lauten:

WRITE:
`00 30 2C 00 00 00 08 00 00 00 00 00 0C 01 22 10 00 00 00 00 00 00 00 00 00 00 00 C0 00 00 00 00`

DRAW:
`00 30 2C 00 00 00 08 00 00 00 00 00 58 00 00 40 00 00 00 00 00 00 00 00 00 00 00 C0 00 00 00 00`

Die ersten zwölf Bytes stimmen vollständig überein; die vier Bytes `000Ch–000Fh` unterscheiden sich. Ohne ein passendes GeoWorks-1.x-Strukturdefinition- oder Codebeleg werden diese Felder nicht semantisch benannt.

## 5. Was der Befund beweist – und was nicht

**Bestätigt:**
1. Die Tokenpaare befinden sich in LMem-Objekt-/UI-Ressourcen.
2. Die zugehörigen Chunks haben dieselbe Länge und stimmen in 220 von 228 Bytes überein.
3. Die Tokenpaare stehen in beiden Chunks an identischen relativen Positionen.
4. Der UI-Text `Kein Dokument` liegt ebenfalls an identischer relativer Position.
5. Die zwei Anwendungen verwenden daher sehr wahrscheinlich eng verwandte oder aus derselben Vorlage abgeleitete UI-Chunk-Strukturen.

**Noch nicht bestätigt:**
1. die konkrete Objektklasse;
2. die Bedeutung von `18 E7`;
3. die Semantik der Token `WDAT` / `DDAT`;
4. ob GeoManager diese Token direkt für Dateityp und Icon auswertet;
5. das native Dateiformat und der Dokument-Lifecycle;
6. die Dokument-Icon-Monikerreferenz.

## 6. Nächster Schritt

Der nächste Schritt ist kein Patch, sondern die Zuordnung des Chunks zu einer Klasse und zu ausführbarem Code:

1. Die in der Ressource enthaltene LMem-/Objektstruktur anhand einer nachweislich passenden GeoWorks-1.x-Definition dekodieren.
2. Die Objekt-/Klassenreferenz und Chunk-ID verfolgen.
3. In den GeoWrite-Code-Ressourcen die Konstruktion bzw. Initialisierung dieses Objekts finden.
4. Die Nachrichtenpfade für Neu, Öffnen, Speichern und Schließen verfolgen.
5. Den Monikerpfad zum Dokument-Icon separat nachweisen.

Die bisherige Code-Suche im GitHub-Repository `JMGeithain/pcgeos-1-sdk` nach den Begriffen `GenDocumentControl`, `DocumentControlClass`, `WDAT WP00` und `GenDocument` lieferte keine Treffer. Das ist kein Beweis, dass diese Klassen/Begriffe im historischen System fehlen; es zeigt nur, dass die aktuelle Repository-Suche keine passende Definition bereitstellt.

## Status

Keine Änderung an `GEOTEST.GEO`, keine Änderung an GeoWorks-Originalen, kein Laufzeittest. Die Dokumenterzeugung und das eigene Dokument-Icon sind weiterhin nicht implementiert.
