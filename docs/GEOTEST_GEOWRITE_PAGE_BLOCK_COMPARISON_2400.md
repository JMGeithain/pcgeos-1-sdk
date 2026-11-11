# GEOTEST – Vergleich der GeoWrite-Seitenblöcke 005Ch, 0380h und 0398h (2400)

Stand: 2026-11-11

## 1. Ziel

Verglichen werden die ersten drei VM-Seitenblöcke, auf die das 21-Elemente-PageArray in `SOLAR_DE.000` verweist. Untersucht werden Blockgröße, LMem-Header, Chunkanzahl und ausgewählte Chunk-Payloads. Die Analyse bleibt auf nachprüfbare Strukturmerkmale beschränkt.

## 2. Quelle und Parser

- Datei: `Showcase/Deutsch/GeoWrite/SOLAR_DE.000`
- Größe: 316.084 Byte
- Parser: `Source/showcase-draw/vm1.py` aus dem bereitgestellten Patch-Paket
- VM-Block-Handles: `005Ch`, `0380h`, `0398h`

Der Parser prüft GEOS-Dateisignatur `C7 45 CF 53`, VM-Signatur `ADEBh), liest den VM-Header und ermittelt die VM-Blöcke anhand der Header-Tabelle. Die LMem-Chunk-Offsets werden aus dem LMem-Handle-Verzeichnis gelesen.

## 3. Gemeinsame Struktur

| Merkmal | VM-Block 005Ch | VM-Block 0380h | VM-Block 0398h |
|---|---:|---:|---:|
| VM-Blockgröße | 848 Byte | 848 Byte | 848 Byte |
| VM-Flag | `01FFh` | `01FFh` | `01FFh` |
| LMem-Handle-Tabellenoffset | `0020h` | `0020h` | `0020h` |
| Chunk-Slots | 38 | 38 | 38 |
| Aktive Chunk-Payloads im Dump | 18 | 18 | 18 |

Hinweis: Der LMem-Parser zählt die Handle-Slots; in diesen drei Blöcken sind die im Dump sichtbaren aktiven Chunks `20h` bis `42h` in geraden Schritten. Die Slotanzahl beträgt 38; davon sind in jedem dieser drei Blöcke 18 Chunk-Payloads belegt. Bei der Auswertung sind Handle-Slot-Zahl und aktive Chunk-Anzahl zu unterscheiden.

## 4. Vergleich der ersten Chunks

| Chunk-Handle | VM 005Ch | VM 0380h | VM 0398h |
|---:|---:|---:|---:|
| `0020h` | 38 Byte | 38 Byte | 38 Byte |
| `0022h` | 104 Byte | 104 Byte | 104 Byte |
| `0024h` | 89 Byte | 89 Byte | 89 Byte |
| `0026h` | 1 Byte | 1 Byte | 1 Byte |
| `0028h` | 18 Byte | 18 Byte | 18 Byte |
| `002Ah` | 18 Byte | 18 Byte | 18 Byte |
| `002Ch` | 14 Byte | 14 Byte | 14 Byte |
| `002Eh` | 18 Byte | 18 Byte | 18 Byte |
| `0030h` | 89 Byte | 89 Byte | 89 Byte |
| `0032h` | 28 Byte | 28 Byte | 28 Byte |

Die Größen der aufgeführten Chunks sind in allen drei Blöcken gleich. Die Inhalte sind jedoch nicht durchgehend identisch.

## 5. Nachweis seitenabhängiger Inhalte

Chunk `0032h` enthält in allen drei untersuchten Seitenblöcken eine lesbare Seitenkennzeichnung:

- VM-Block `005Ch`: `Unser Sonnensystem  |  1/21`
- VM-Block `0380h`: `Unser Sonnensystem  |  2/21`
- VM-Block `0398h`: `Unser Sonnensystem  |  3/21`

Dies ist ein direkter Nachweis, dass die drei getrennten VM-Blöcke seitenbezogene, voneinander abweichende Inhalte enthalten. Die sichtbare Zeichenfolge allein erklärt noch nicht, welche Objektklasse oder welcher UI-Mechanismus sie rendert.

Auch weitere Chunks unterscheiden sich seitenbezogen:
- Chunk `0022h` enthält unterschiedliche Positions-/Größenwerte und Referenzen.
- Chunk `0024h` enthält in den drei Seiten unterschiedliche kurze binäre Daten.
- Chunk `0030h` enthält unterschiedliche längere Binärdaten.

Die Chunkgrößen bleiben dabei in diesen Beispielen gleich.

## 6. Einordnung

**Direkt belegt:**
1. Die drei PageArray-Verweise zeigen auf existierende VM-Blöcke.
2. Alle drei VM-Blöcke sind 848 Byte groß und als LMem-Blöcke markiert.
3. Die drei LMem-Blöcke besitzen dieselbe Slot-/Chunk-Anordnung für die untersuchten ersten zehn Chunks.
4. Die Seitenkennzeichnung in Chunk `0032h` unterscheidet die Seiten 1/21, 2/21 und 3/21.
5. Die Daten sind damit keine identischen Kopien desselben Seitenblocks.

**Noch nicht belegt:**
- Semantische Klassen-/Objektnamen der einzelnen LMem-Chunks.
- Ob Chunk `0032h` ein Titel-, Status- oder sonstiges Textobjekt ist.
- Welche Chunks für eine leere GEOTEST-Seite zwingend erforderlich wären.
- Ob der gesamte 848-Byte-Seitenblock als Minimaltemplate verwendet werden kann.

## 7. Bedeutung für GEOTEST

Der Seitenblock enthält mehr als nur den sichtbaren Text. Ein minimaler GEOTEST-Dokumentprototyp darf deshalb nicht einfach einen 848-Byte-Block kopieren und nur Textbytes ersetzen. Zuerst müssen die Objekt- und Referenzstrukturen identifiziert werden.

Gleichzeitig ist die Wiederholung der Chunkgrößen und Handle-Anordnung ein guter Ansatzpunkt: Wir können nun systematisch zwischen seitenabhängigen Daten und vermutlich gemeinsamen Struktur-/Steuerdaten unterscheiden. „Gemeinsam“ bedeutet hier nur gleiche Größe/Position, nicht zwingend identischer Inhalt.

## 8. Nächster Schritt

1. Alle 38 Handle-Slots der drei Seitenblöcke vollständig inventarisieren.
2. Byte-Differenzen je Chunk ermitteln, um konstante und seitenabhängige Felder zu trennen.
3. Text- und Objekt-Runs mit den im Generator bearbeiteten Blöcken `0050h`, `0038h`, `002Ch` und `0074h` abgleichen.
4. Erst danach einen Minimal-Seitenblock für GEOTEST spezifizieren.

## 9. Status

Statische Analyse einer nativen GeoWrite-1.x-Dokumentdatei. Kein Laufzeittest. Keine Änderung an `SOLAR_DE.000`, GeoWrite oder GEOTEST. Die Zuordnung der Chunk-Klassen bleibt offen.
