# GEOTEST – Vergleich der Token-tragenden LMem-Chunks (2377)

Stand: 2026-11-10

## Ausgangspunkt

Untersucht wurden unverändert die GeoWorks-1.x-Originaldateien `WRITE.GEO` und `DRAW.GEO` aus dem bereitgestellten `GEOWORKS.zip`. Ziel bleibt ausschließlich die native GEOTEST-Dokumentanwendung; Treiberentwicklung ist nicht Gegenstand dieser Untersuchung.

## Exakter LMem-Chunk-Vergleich

Die Token-Paare liegen in folgenden LMem-Chunks der jeweiligen OBJECT/UI-Ressource:

| Datei | Ressource | LMem-Chunk-Eintrag (0-basiert) | Chunk-Beginn relativ zur Ressource | nächster Chunk | Länge |
|---|---:|---:|---:|---:|---:|
| WRITE.GEO | 9 | 29 | `02A6h` | `038Ah` | 228 Bytes |
| DRAW.GEO | 6 | 46 | `0672h` | `0756h` | 228 Bytes |

Die Token-Paare beginnen in beiden Chunks exakt bei relativem Offset `00B8h` (184 dezimal):
- WRITE: `WDAT 00 00 WP00 00 00`
- DRAW: `DDAT 00 00 DP00 00 00`

Die Zeichenfolge `Kein Dokument` folgt in beiden Chunks an gleicher Position nach dem Tokenbereich.

## Byteweiser Vergleich

Beide Chunks sind jeweils exakt 228 Bytes lang. Ein Byte-für-Byte-Vergleich ergibt **nur acht abweichende Bytepositionen**:

| Chunk-relativer Offset | WRITE.GEO | DRAW.GEO | Beobachtung |
|---:|---:|---:|---|
| `000Ch` | `0Ch` | `58h` | anwendungsspezifischer Strukturwert |
| `000Dh` | `01h` | `00h` | anwendungsspezifischer Strukturwert |
| `000Eh` | `22h` | `00h` | anwendungsspezifischer Strukturwert |
| `000Fh` | `10h` | `40h` | anwendungsspezifischer Strukturwert |
| `00B8h` | `57h` ('W') | `44h` ('D') | erstes Token: WDAT/DDAT |
| `00BEh` | `57h` ('W') | `44h` ('D') | App-Token: WP00/DP00 |
| `00D9h` | `5Ch` | `7Eh` | anwendungsspezifischer Strukturwert |
| `00DFh` | `15h` | `0Bh` | anwendungsspezifischer Strukturwert |

Alle übrigen 220 Bytes stimmen exakt überein.

## Aussagekraft

Das ist ein sehr starker Strukturvergleich: Zwei unterschiedliche GeoWorks-1.x-Anwendungen enthalten in ihren LMem-Objektressourcen einen gleich langen, nahezu byteidentischen Chunk. Die beiden Dokument-/App-Token-Paare stehen jeweils an derselben Stelle; auch der Text `Kein Dokument` liegt im gleichen Chunk an derselben Position.

Damit ist eine gemeinsame oder eng verwandte Objektstruktur für den Dokumentbereich ein gut gestützter Untersuchungsansatz. Der Vergleich identifiziert jedoch noch nicht die Klasse oder die API. Insbesondere wird **nicht** behauptet, dass es sich bereits nachweislich um `GenDocumentControlClass`, einen GeoManager-Dateitypeintrag oder den vollständigen Icon-Registrierungsdatensatz handelt.

Die vier Unterschiede am Chunk-Anfang und zwei weitere Strukturwerte zeigen zudem, dass die Chunks nicht vollständig identisch sind. Ihre Bedeutung ist noch offen.


## Zusatzprüfung des Wortes vor dem Tokenpaar

Das unmittelbar vor dem ersten Token stehende Bytepaar `18 E7` wurde zusätzlich in den vollständigen Dateien gesucht:

- WRITE.GEO: genau ein Treffer, Datei-Offset `9A4Ah`.
- DRAW.GEO: genau ein Treffer, Datei-Offset `27D8h`.
- GEOTEST.GEO (bisheriger Build): kein Treffer.

Damit ist `18 E7` in jeder der beiden Referenz-Geodes lokal auf den Token-tragenden Chunk begrenzt. Das macht es zu einem sinnvollen Feld für die weitere Objektstruktur-Analyse, legt seine Bedeutung aber nicht fest. Insbesondere wird es noch nicht als Klassenzeiger oder API-Kennung interpretiert.

## Nächster Schritt

1. Die LMem-Chunk-Struktur anhand der GeoWorks-1.x-Objekt-/LMem-Definitionen dekodieren.
2. Den gemeinsamen Objektklasseneintrag bzw. Klassenzeiger im Chunk identifizieren; insbesondere die Bedeutung des identischen Wortes `18E7h` unmittelbar vor dem Tokenpaar prüfen.
3. Die Objektklasse mit den in WRITE.GEO und DRAW.GEO verwendeten Nachrichten/Methoden und Codepfaden verbinden.
4. Erst wenn die Klasse und der Dokument-Lifecycle nachgewiesen sind, den kleinsten kompatiblen GEOTEST-Ansatz ableiten.

## Status

- Beide Chunks: 228 Bytes, bestätigt.
- Tokenposition: jeweils +184 Bytes, bestätigt.
- Gleiche Position des Textes `Kein Dokument`, bestätigt.
- Byteabweichungen: exakt 8 von 228, bestätigt.
- Konkrete Objektklasse, Token-Semantik, Dokumentdateiformat und Icon-Pfad: weiterhin nicht abschließend nachgewiesen.
- Keine Originaldatei verändert; kein neuer Build und kein Laufzeittest.
