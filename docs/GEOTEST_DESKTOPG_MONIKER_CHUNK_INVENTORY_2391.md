# GEOTEST – DESKTOPG.GEO: Inventar wiederkehrender 48-Pixel-Moniker-Chunks (2391)

Stand: 2026-11-10

## Ziel / Abgrenzung

Ausschließlich GeoWorks / PC/GEOS 1.x. Ziel ist die spätere Zuordnung der Desktop-Dateitypen zu den historischen Icon-/Moniker-Ressourcen. Keine Treiberentwicklung und keine Änderung an Originaldateien.

Original:
- `GEOWORKS/SYSAPPL/DESKTOPG.GEO`
- 101.524 Bytes
- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`

## 1. Methode

Für Ressourcen 39–50 wurde das LMem-Chunk-Verzeichnis ab Ressourcenoffset `0020h` gelesen. Jeder Chunk-Eintrag enthält einen Ressourcen-relativen Payload-Offset. Das 16-Bit-Längenwort steht unmittelbar vor dem Payload.

An den Payload-Anfängen wurden wiederkehrende little-endian Maßfelder gesucht. Die Werte `0030h` und `001Eh` entsprechen 48×30; `0030h` und `000Eh` entsprechen 48×14.

Ein einfacher 1-bpp-Payload ist in diesen Beispielen genau 8 Bytes Vorspann plus `ceil(48/8) × Höhe` Rasterbytes:
- 48×30: 8 + 6×30 = 188 Bytes (`00BCh`)
- 48×14: 8 + 6×14 = 92 Bytes (`005Ch`)

## 2. 48×30-Payloads

| Ressource | Payload-Anzahl mit 48×30-Maßfeldern | Häufige Länge | Datenbytes nach 8-Byte-Vorspann | Bewertung |
|---:|---:|---:|---:|---|
| 39 | 14 | 908 Bytes (bei 12 Chunks), zusätzlich 914 Bytes (2 Chunks) | 900 bzw. 906 | nicht einfacher 1-bpp-Payload |
| 40 | 14 | 188 Bytes (bei 12 Chunks), zusätzlich 914 Bytes (2 Chunks) | 180 bzw. 906 | 12 Chunks passen exakt zu 1 bpp; 2 weitere Formate offen |
| 49 | 2 | 188 Bytes | 180 | beide passen exakt zu 1 bpp |
| 50 | 2 | 908 Bytes | 900 | anderes Raster-/Planeformat; nicht als 1 bpp klassifiziert |

Beispielhafte Ressourcen-relative Payload-Offsets:

- Ressource 39: `0056h, 03E2h, 076Eh, 0AFAh, 0E86h, 1212h, 159Eh, 192Ah, 1CB6h, 2042h, 23CEh, 275Ah, 2AE6h, 2E7Ah`
- Ressource 40: `0056h, 0112h, 01CEh, 028Ah, 0346h, 0402h, 04BEh, 057Ah, 0636h, 06F2h, 07AEh, 086Ah, 0926h, 0CBAh`
- Ressource 49: `0036h, 0112h`
- Ressource 50: `0036h, 03E2h`

Die Offsets sind relative Payload-Adressen, nicht Dateioffsets.

## 3. 48×14-Payloads

| Ressource | Payload-Anzahl mit 48×14-Maßfeldern | Häufige Länge | Datenbytes nach 8-Byte-Vorspann | Bewertung |
|---:|---:|---:|---:|---|
| 41 | 14 | 92 Bytes (bei 12 Chunks), zusätzlich 434 Bytes (2 Chunks) | 84 bzw. 426 | 12 Chunks passen exakt zu 1 bpp; 2 weitere Formate offen |
| 48 | 2 | 92 Bytes | 84 | beide passen exakt zu 1 bpp |

Beispielhafte Ressourcen-relative Payload-Offsets:

- Ressource 41: `0056h, 00B2h, 010Eh, 016Ah, 01C6h, 0222h, 027Eh, 02DAh, 0336h, 0392h, 03EEh, 044Ah, 04A6h, 065Ah`
- Ressource 48: `0036h, 00B2h`

## 4. Was die Größenrechnung beweist

Für die 188-Byte- und 92-Byte-Payloads stimmen Maße, Vorspann und Rasterlänge exakt mit 1 Bit pro Pixel überein. Das ist eine belastbare strukturelle Klassifikation der betreffenden Payloads als 1-bpp-Bitmaps.

Für die 908-/914-Byte- bzw. 434-Byte-Payloads reicht die Längenrechnung nicht aus, um das konkrete Format zu benennen. Die 900 Datenbytes bei 48×30 bzw. 426 Datenbytes bei 48×14 könnten zusätzliche Ebenen, Masken oder sonstige Metadaten enthalten. Ohne Dekodierung der Formatfelder wird keine dieser Möglichkeiten als Tatsache ausgegeben.

## 5. Grenzen der Zuordnung

Die Ressourcen enthalten viele Bild-Payloads, aber ihre Motive und semantischen Rollen sind noch nicht bekannt. Die Anzahl der Chunks sagt allein nicht, ob sie:
- normale Datei-/Ordnersymbole,
- Laufwerkssymbole,
- Toolbar-/Menü-Moniker,
- Statusgrafiken,
- oder Auswahl-/Invertierungsvarianten

darstellen.

Ebenso ist noch nicht nachgewiesen, welche dieser Bildressourcen durch die generischen Dateitypen `FILE`, `FLDR`, `gAPP`, `gDAT` oder durch anwendungsspezifische Dokumenttokens ausgewählt werden.

## 6. Nächste Schritte

1. Die 1-bpp-Payloads als Kontaktbogen darstellen und die sichtbaren Motive vorsichtig klassifizieren.
2. Die 908-/914-/434-Byte-Payloads anhand ihrer Headerfelder und Plane-Struktur analysieren.
3. Die Chunk-/Objektverweise in Ressource 38 gegen konkrete Chunk-Offsets in Ressourcen 39–50 auflösen.
4. Die Dateityp-Objektfelder und den Moniker-Selektionscode verbinden.
5. Den separaten Weg für `WDAT/WP00` und `DDAT/DP00` zur GeoManager-Darstellung untersuchen.

## Status

- 48×30-Payloads in Ressourcen 39, 40, 49 und 50 inventarisiert.
- 48×14-Payloads in Ressourcen 41 und 48 inventarisiert.
- 1-bpp-Längenformel für 188- und 92-Byte-Payloads exakt bestätigt.
- Weitere größere Payload-Varianten gefunden, aber nicht abschließend dekodiert.
- Bildmotive und Token-/Icon-Zuordnung offen.
- Keine Originaldatei geändert; kein GEOTEST-Build erstellt; kein Laufzeiterfolg behauptet.
