# DESKTOPG.GEO – Analyse der größeren Bitmap-Payloads (2393)

## Ziel und Abgrenzung

Statische Untersuchung der größeren Bitmap-Payloads aus Ressourcen 39, 40, 41 und 50. Es wird ausschließlich GeoWorks / PC/GEOS 1.x betrachtet. Keine Binärdatei wurde verändert; kein Treiber und kein GEOTEST-Build wurde erstellt.

## Ausgangsdatei

- `GEOWORKS/SYSAPPL/DESKTOPG.GEO` aus `GEOWORKS.zip`
- Größe: 101.524 Byte
- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`

## Extraktionsmethode

Die Payload-Offsets und Chunk-Längen wurden aus dem Chunk-Verzeichnis der Ressourcen übernommen. Die Längenwörter stehen jeweils unmittelbar vor dem Payload. Die ersten vier Payload-Bytes enthalten die little-endian Maße:

- 48×30: `30 00 1E 00`
- 48×14: `30 00 0E 00`

Die Bytes 4–7 wurden als Headerbereich belassen; ihre genaue Feldbedeutung ist noch offen. Die Rasterdaten beginnen bei Payload-Offset +8.

Bei 48 Pixel Breite beträgt die Zeilenlänge für eine 1-Bit-Ebene 6 Byte. Daraus folgt:

- eine Ebene bei 48×30: 6×30 = 180 Byte
- fünf Ebenen bei 48×30: 5×180 = 900 Byte
- eine Ebene bei 48×14: 6×14 = 84 Byte
- fünf Ebenen bei 48×14: 5×84 = 420 Byte

## Befund: exakte Fünf-Block-Aufteilung

| Payload-Länge | Maße | Rasterbytes nach 8-Byte-Header | Aufteilung |
|---:|---:|---:|---|
| 908 Byte | 48×30 | 900 | 5 × 180 Byte, ohne Rest |
| 914 Byte | 48×30 | 906 | 5 × 180 Byte + 6 Byte Rest |
| 434 Byte | 48×14 | 426 | 5 × 84 Byte + 6 Byte Rest |

Die 908-Byte-Payloads lassen sich damit exakt in fünf gleich große Rasterblöcke zerlegen. Dasselbe Fünf-Block-Muster ist bei den 914- und 434-Byte-Varianten vorhanden; dort folgen allerdings jeweils sechs zusätzliche Bytes.

## Betroffene Payloads

Offsets sind relativ zum Anfang der jeweiligen Ressource.

| Ressource | Payload-Offsets | Länge |
|---:|---|---:|
| 39 | `0056h, 03E2h, 076Eh, 0AFAh, 0E86h, 1212h, 159Eh, 192Ah, 1CB6h, 2042h, 23CEh, 275Ah | 908 Byte |
| 39 | `2AE6h, 2E7Ah` | 914 Byte |
| 40 | `0926h, 0CBAh` | 914 Byte |
| 41 | `04A6h, 065Ah` | 434 Byte |
| 50 | `0036h, 03E2h` | 908 Byte |

## Headerbeobachtungen

Die ersten vier Bytes sind bei den jeweiligen Maßen konsistent. Die Bytes 4–7 sind nicht durchgehend konstant. Beispiele:

- Ressource 39, Payload `0056h`: `30 00 1E 00 00 11 00 00`
- Ressource 39, Payload `0AFAh`: `30 00 1E 00 00 11 00 FC`
- Ressource 50, Payload `0036h`: `30 00 1E 00 00 11 00 FF`

Der wiederkehrende Wert `00 11` an Headerposition 4–5 ist auffällig. Die Bytes 6–7 variieren und dürfen daher nicht ohne weiteren Nachweis als ungenutzte Padding-Bytes behandelt werden. Ihre Bedeutung ist offen.

## Interpretation – was gesichert ist und was nicht

**Gesichert:**
1. Die Maße 48×30 bzw. 48×14 sind in den Payloads explizit vorhanden.
2. Nach dem 8-Byte-Header folgen bei den 908-Byte-Varianten genau 900 Rasterbytes.
3. Diese 900 Bytes zerfallen rechnerisch exakt in fünf Blöcke zu je 180 Bytes.
4. Bei 434-Byte-Payloads ergeben sich fünf Blöcke zu je 84 Bytes und sechs zusätzliche Bytes.
5. Bei 914-Byte-Payloads ergeben sich fünf Blöcke zu je 180 Bytes und sechs zusätzliche Bytes.

**Noch nicht gesichert:**
- Ob die fünf Blöcke fünf getrennte 1-bpp-Planes sind oder eine andere codierte Rasterorganisation darstellen.
- Ob die fünf Ebenen vier Farbebenen plus eine Maske bilden.
- Ob die sechs Zusatzbytes Kontroll-, Masken-, Zeilen- oder sonstige Metadaten enthalten.
- Welche Bit-Reihenfolge und welche Plane-Reihenfolge der GeoManager tatsächlich verwendet.
- Welche Dateitypen oder UI-Elemente die einzelnen Motive repräsentieren.

Die Bezeichnung „fünf 1-Bit-Ebenen“ ist daher eine rechnerische Strukturhypothese, keine abschließend identifizierte GEOS-Bitmap-Spezifikation.

## Nächste Untersuchung

1. Die fünf 180-Byte-Blöcke bzw. 84-Byte-Blöcke einzeln visualisieren und statistisch vergleichen.
2. Prüfen, ob ein Block als Maske fungiert und die übrigen Blöcke zusammen ein konsistentes Farb-/Indexbild ergeben.
3. Die sechs Zusatzbytes der 914-/434-Byte-Varianten mit Ressourcen- und Chunk-Nachbarschaft vergleichen.
4. Erst danach die genaue Bitmap-Struktur benennen und die Moniker-Referenzen in Ressource 38 damit verbinden.

## Vorarbeiten

- `docs/GEOTEST_DESKTOPG_MONIKER_CHUNK_INVENTORY_2391.md`
- `docs/GEOTEST_DESKTOPG_MONIKER_CONTACT_SHEET_AUDIT_2392.md`
- `docs/GEOTEST_DESKTOPG_LMEM_MONIKER_RESOURCE_AUDIT_2389.md`

## Teststatus

Rein statische Analyse der Originaldatei. Kein Laufzeittest unter GeoWorks 1.2.8. Keine Änderung an DESKTOPG.GEO, GEOTEST.GEO oder anderen Originaldateien.
