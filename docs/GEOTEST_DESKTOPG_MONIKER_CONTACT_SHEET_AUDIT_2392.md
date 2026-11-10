# DESKTOPG.GEO – Moniker-Bitmap-Kontaktaudit (2392)

## Ziel

Die in Untersuchung 2391 inventarisierten 1-Bit-Bitmap-Chunks aus DESKTOPG.GEO wurden mit den bestätigten Payload-Offsets erneut extrahiert und visuell verglichen. Ziel ist die technische Prüfung der Rasterdaten, nicht die voreilige Benennung der dargestellten Motive.

## Ausgangsdatei

- Datei: `GEOWORKS/SYSAPPL/DESKTOPG.GEO` aus `GEOWORKS.zip`
- Dateigröße: 101.524 Byte
- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`
- Ressourcentabelle beginnt bei Datei-Offset `01D0h`; Ressourcenanfänge wurden aus den aufeinanderfolgenden 32-Bit-Offsets ermittelt.

## Extraktionsverfahren

Für jeden aufgeführten Payload-Offset wurde das unmittelbar davorliegende 16-Bit-Wort als Chunk-Länge gelesen. Der Payload beginnt am angegebenen Offset. Die ersten 8 Payload-Bytes bilden den Bitmap-Header; die ersten beiden 16-Bit-Werte (little-endian) ergeben Breite und Höhe. Die nachfolgenden Bytes bilden die Rasterdaten.

Für 48 Pixel Breite ergeben sich 6 Byte pro Zeile. Die erwartete Payload-Länge lautet:

- 48 × 30: 8 + 6 × 30 = 188 Byte (`00BCh`)
- 48 × 14: 8 + 6 × 14 = 92 Byte (`005Ch`)

Alle 28 Datensätze erfüllen diese Längenprüfung exakt.

## Extrahierte Datensätze

Offsets sind relativ zum Anfang der jeweiligen Ressource und hexadezimal angegeben.

| Ressource | Anzahl | Payload-Offsets | Länge je Payload | Maße |
|---:|---:|---|---:|---:|
| 40 | 12 | `0056h, 0112h, 01CEh, 028Ah, 0346h, 0402h, 04BEh, 057Ah, 0636h, 06F2h, 07AEh, 086Ah` | 188 Byte | 48×30 |
| 41 | 12 | `0056h, 00B2h, 010Eh, 016Ah, 01C6h, 0222h, 027Eh, 02DAh, 0336h, 0392h, 03EEh, 044Ah` | 92 Byte | 48×14 |
| 48 | 2 | `0036h, 00B2h` | 92 Byte | 48×14 |
| 49 | 2 | `0036h, 0112h` | 188 Byte | 48×30 |

Gesamt: 28 Datensätze. In der erneuten Extraktion ergaben sich 28 unterschiedliche vollständige Payload-Hashes; die Raster-Payloads sind also nicht einfach identische Wiederholungen.

## Visuelle Prüfung / Bit-Reihenfolge

Jeder Datensatz wurde in zwei Varianten gerendert:

1. MSB-first: Bit 7 ist das linke Pixel des jeweiligen Bytes.
2. LSB-first: Bit 0 ist das linke Pixel des jeweiligen Bytes.

Die Varianten unterscheiden sich in der horizontalen Bit-Anordnung innerhalb jedes 8-Pixel-Blocks. Aus den vorliegenden Rohdaten allein lässt sich die vom GeoManager verwendete Bit-Reihenfolge noch nicht abschließend beweisen. Deshalb wird keine der beiden Darstellungen als endgültig verbindlich festgelegt.

Die gerenderten Muster zeigen bei den 48×30- und 48×14-Datensätzen klar strukturierte, teils geräte- bzw. dateiähnliche grafische Formen. Das ist ein Hinweis auf grafische Moniker-/Icon-Daten, aber noch kein Nachweis, welches Motiv zu welchem Dateityp, Status oder Dialog gehört.

## Ergebnisse

- Ressource 40: 12 Datensätze mit 48×30 Pixeln, jeweils 188 Byte.
- Ressource 41: 12 Datensätze mit 48×14 Pixeln, jeweils 92 Byte.
- Ressource 48: 2 Datensätze mit 48×14 Pixeln, jeweils 92 Byte.
- Ressource 49: 2 Datensätze mit 48×30 Pixeln, jeweils 188 Byte.
- Gesamt: 28 Datensätze; 28 unterschiedliche vollständige Payload-Hashes.

## Grenzen der Aussage

1. Die 28 Datensätze sind technisch konsistent mit einfachen 1-Bit-Rasterbildern der angegebenen Abmessungen.
2. Die Einordnung als Moniker-/Icon-Kandidaten stützt sich auf Ressourcenlage und Rasterstruktur. Die konkrete semantische Zuordnung ist nicht bewiesen.
3. Die größeren Payload-Varianten (908, 914 bzw. 434 Byte), die in Untersuchung 2391 inventarisiert wurden, sind ausdrücklich nicht Teil dieser 1-Bit-Auswertung.
4. Es wurde keine Datei verändert und kein GeoWorks-Binärprogramm gepatcht.
5. Es erfolgte kein Laufzeittest unter GeoWorks 1.2.8. Die Auswertung ist eine statische Analyse.

## Nächster sinnvoller Schritt

Als Nächstes sollten die größeren Bitmap-Payloads in Ressourcen 39–41 und 50 untersucht werden: Headerfelder, mögliche zusätzliche Ebenen/Masken und Vergleich der Rasterdaten mit den hier bestätigten 1-Bit-Datensätzen. Erst danach sollte versucht werden, einzelne Motive konkreten Dateitypen oder GeoManager-Zuständen zuzuordnen.

## Bezug

Vorarbeiten:
- `docs/GEOTEST_DESKTOPG_MONIKER_CHUNK_INVENTORY_2391.md`
- `docs/GEOTEST_DESKTOPG_BITMAP_MONIKER_DECODE_2390.md`
- `docs/GEOTEST_DESKTOPG_LMEM_MONIKER_RESOURCE_AUDIT_2389.md`
