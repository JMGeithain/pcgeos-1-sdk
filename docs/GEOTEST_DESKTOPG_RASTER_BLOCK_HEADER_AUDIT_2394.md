# DESKTOPG.GEO – Rasterblock- und Headervergleich (2394)

## Ziel

Untersuchung der fünf gleich großen Rasterblöcke in den größeren Bitmap-Payloads. Geprüft werden Headerunterschiede, Blockunabhängigkeit und die Möglichkeit, die Daten als fünf 1-bpp-Planes zu interpretieren.

## Originaldatei

- `GEOWORKS/SYSAPPL/DESKTOPG.GEO`
- Größe: 101.524 Byte
- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`

## 1. Headervergleich

Beispiele aus den Original-Payloads:

| Typ | Payload-Offset | Länge | Headerbytes |
|---|---:|---:|---|
| Einfach 48×30, Ressource 40 | `0056h` | 188 | `30 00 1E 00 00 00 00 00` |
| Einfach 48×14, Ressource 41 | `0056h` | 92 | `30 00 0E 00 00 00 00 00` |
| Groß 48×30, Ressource 39 | `0056h` | 908 | `30 00 1E 00 00 11 00 00` |
| Groß 48×30, Ressource 39 | `2AE6h` | 914 | `30 00 1E 00 00 11 00 00` |
| Groß 48×14, Ressource 41 | `04A6h` | 434 | `30 00 0E 00 00 11 00 00` |

Die Maßfelder sind little-endian: 48×30 bzw. 48×14. Bei den großen Varianten steht an Headerposition 4–5 wiederholt `00 11`; bei den einfachen 1-bpp-Beispielen stehen dort `00 00`. Das ist ein belastbarer Formatunterschied. Die Bedeutung des Wertes `1100h` ist noch nicht bekannt.

## 2. Fünf gleich große Rasterblöcke

Bei der 908-Byte-Payload (48×30) entfallen nach dem 8-Byte-Header 900 Bytes auf Rasterdaten. Diese lassen sich exakt in fünf Blöcke zu 180 Bytes teilen. Ein Block enthält damit rechnerisch genau 6×30 Bytes.

Die fünf Blöcke des Beispiels aus Ressource 39 / Payload `0056h` wurden separat betrachtet:

| Block | Bytes | Anzahl unterschiedlicher Bytewerte | gesetzte Bits | Bitdichte |
|---:|---:|---:|---:|---:|
| 0 | 180 | 25 | 903 von 1.440 | 62,7 % |
| 1 | 180 | 26 | 873 von 1.440 | 60,6 % |
| 2 | 180 | 24 | 809 von 1.440 | 56,2 % |
| 3 | 180 | 25 | 841 von 1.440 | 58,4 % |
| 4 | 180 | 32 | 856 von 1.440 | 59,4 % |

Die Dichte wurde durch Zählen gesetzter Bits in den 180 Bytes ermittelt; 180×8 = 1.440 Bits je Block.

Die Blöcke sind nicht identisch. Auch eine direkte Byte-für-Byte-Prüfung auf Gleichheit oder bitweise Invertierung zeigt keine identischen bzw. vollständig invertierten Blockpaare. Damit sind fünf unabhängige Rasterdatenblöcke belegt, nicht fünf Kopien.

## 3. Zusammengesetzte 5-Bit-Ansicht

Wenn jeder der fünf Blöcke als eine 1-Bit-Ebene behandelt wird, lassen sich fünf Bits pro Pixel und damit 32 mögliche Pixelwerte zusammensetzen. Im untersuchten Beispiel kommen alle 32 Werte mindestens einmal vor.

Das ist mit einer 5-bpp- bzw. fünf-Plane-Darstellung vereinbar. Die visuelle Graustufenansicht ergibt jedoch kein eindeutig identifizierbares Iconmotiv. Die Darstellung allein bestätigt daher weder Plane-Reihenfolge noch Bit-Reihenfolge, Farbpalette oder tatsächliche GEOS-Interpretation.

**Wichtige Präzisierung:** Die fünf 180-Byte-Blöcke sind zunächst nur eine exakte rechnerische Zerlegung. „Fünf Farb-Planes“ bleibt eine Hypothese. Eine verbindliche Formatspezifikation oder ein Decoder wurde noch nicht nachgewiesen.

## 4. Die sechs zusätzlichen Bytes

Bei den größeren Varianten mit 914 bzw. 434 Byte bleiben nach Abzug des 8-Byte-Headers und fünf Rasterblöcken jeweils sechs Bytes übrig:

- 914 − 8 − 5×180 = 6
- 434 − 8 − 5×84 = 6

Die sechs Bytes sind nicht durchgehend null. Beispiele:
- Ressource 39, Payload `2AE6h`: `BB BB 00 33 6E 64`
- Ressource 39, Payload `2E7Ah`: `00 80 54 00 20 01`
- Ressource 40, Payload `0926h`: `DD DD DD DD C4 02`
- Ressource 41, Payload `04A6h`: `00 00 00 00 00 00`
- Ressource 41, Payload `065Ah`: `00 00 00 00 F2 00`

Die sechs Bytes könnten eine zusätzliche Zeile oder Metadaten darstellen; beides ist nicht bewiesen. Weil die Werte variieren, dürfen sie nicht pauschal als Padding verworfen werden.

## 5. Ergebnis und offene Punkte

**Gesichert:**
1. Die großen Varianten haben einen anderen Header als die einfachen 1-bpp-Payloads.
2. Die 908-Byte-Variante enthält fünf gleich große 180-Byte-Rasterblöcke.
3. Die 434-Byte-Variante enthält fünf gleich große 84-Byte-Blöcke und sechs Zusatzbytes.
4. Die 914-Byte-Variante enthält fünf gleich große 180-Byte-Blöcke und sechs Zusatzbytes.
5. Im geprüften 48×30-Beispiel sind die fünf Blöcke nicht identisch; als fünf Bits pro Pixel zusammengesetzt entstehen 32 vorkommende Werte.

**Nicht gesichert:**
- Bedeutung von Headerfeld `1100h`
- Ob es tatsächlich fünf 1-bpp-Planes sind
- Bedeutung und Position der sechs Zusatzbytes
- Bit- und Plane-Reihenfolge, Palette und Farbbedeutung
- Zuordnung der Motive zu Datei-/Ordner-/Laufwerkstypen oder UI-Zuständen

## Nächster Schritt

Als Nächstes sollte die Byteorganisation in einer zweiten 908-Byte-Payload und in einer 434-Byte-Payload gegengeprüft werden. Zusätzlich müssen die sechs Zusatzbytes gegen Chunk-Nachbarschaft und Header-/Objektverweise untersucht werden. Erst wenn mehrere Beispiele dasselbe Layout bestätigen, ist eine Formatspezifikation vertretbar.

## Bezug

- `docs/GEOTEST_DESKTOPG_LARGE_BITMAP_FORMAT_AUDIT_2393.md`
- `docs/GEOTEST_DESKTOPG_MONIKER_CONTACT_SHEET_AUDIT_2392.md`
- `docs/GEOTEST_DESKTOPG_MONIKER_CHUNK_INVENTORY_2391.md`

## Teststatus

Statische Analyse der unveränderten GeoWorks-1.2.8-Datei. Kein Laufzeittest. Keine Änderung an Originaldateien oder GEOTEST.
