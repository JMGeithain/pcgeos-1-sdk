# GEOTEST – DESKTOPG.GEO: Erste Bitmap-Moniker technisch dekodiert (2390)

Stand: 2026-11-10

## Ziel / Abgrenzung

Fortsetzung der Analyse ausschließlich für GeoWorks / PC/GEOS 1.x. Ziel bleibt die Entwicklung eines nativen GEOTEST-Dokuments mit eigenem Symbol. Keine Treiberentwicklung. Die Originaldatei `DESKTOPG.GEO` wurde nur lesend analysiert.

Original:
- `GEOWORKS/SYSAPPL/DESKTOPG.GEO`
- 101.524 Bytes
- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`

## 1. Bitmap-Payload in Ressource 40

Ressource 40:
- Dateioffset: `14FD0h`
- Dateigröße: 4.180 Bytes
- Ressource-relative Chunk-Payload: `0056h` (zweiter Chunk)
- Längenwort unmittelbar davor bei `0054h`: `00BCh` = 188 Bytes

Die ersten acht Payload-Bytes sind:

```
30 00 1E 00 00 00 00 00
```

Als zwei little-endian 16-Bit-Maße gelesen:
- Breite: `0030h` = 48
- Höhe: `001Eh` = 30

Nach dem 8-Byte-Header folgen genau 180 Bytes. Das entspricht bei 1 Bit pro Pixel und 48 Pixeln Breite:
`48 / 8 × 30 = 180 Bytes`.

Damit ist die Payload-Länge exakt konsistent mit einer 48×30-Bitmap mit einem Bit pro Pixel und einem 8-Byte-Vorspann. Das ist eine strukturelle Ableitung aus Länge und Abmessungen; die exakten historischen Feldnamen des Vorspanns sind noch nicht bestimmt.

## 2. Bitmap-Payload in Ressource 41

Ressource 41:
- Dateioffset: `16024h`
- Dateigröße: 2.068 Bytes
- Ressource-relative Chunk-Payload: `0056h` (zweiter Chunk)
- Längenwort unmittelbar davor bei `0054h`: `005Ch` = 92 Bytes

Die ersten acht Payload-Bytes:

```
30 00 0E 00 00 00 00 00
```

Daraus ergeben sich:
- Breite: 48 Pixel
- Höhe: 14 Pixel

Nach dem 8-Byte-Vorspann folgen genau 84 Bytes:
`48 / 8 × 14 = 84 Bytes`.

Auch diese Payload ist exakt konsistent mit einer 48×14-Bitmap mit einem Bit pro Pixel.

## 3. Was die Dekodierung zeigt – und was nicht

Bestätigt:
- In DESKTOPG.GEO liegen in Ressourcen 40 und 41 strukturierte Bild-Payloads.
- Beide besitzen einen 8-Byte-Vorspann mit den plausiblen Maßen 48×30 bzw. 48×14.
- Die verbleibenden Payload-Längen stimmen exakt mit 1-bpp-Rasterdaten überein.
- Die Daten lassen sich als monochrome Rasterbilder interpretieren.

Noch nicht bestätigt:
- die symbolische Bedeutung der Bildressourcen;
- ob sie Dateityp-, Laufwerks-, Toolbar- oder andere UI-Moniker darstellen;
- welche der Bildressourcen dem Token `FILE`, `FLDR`, `gAPP` oder `gDAT` zugeordnet wird;
- ob ein Dokumenttyp-Icon für `WDAT/WP00` oder `DDAT/DP00` denselben Pfad verwendet.

Die ersten gerenderten Raster zeigen nur eine Form, deren fachliche Zuordnung ohne vollständige Moniker-/Maskeninterpretation nicht sicher ist. Es wird deshalb kein Bildmotiv behauptet.

## 4. Bedeutung für GEOTEST

Wir kennen jetzt konkrete historische GeoWorks-1.x-Grafikdaten, deren Struktur sich als 1-bpp-Bitmap lesen lässt. Das kann später als Vergleich für die eigenen Icon-Ressourcen dienen.

Es reicht jedoch nicht, die 48×30-Bitmapdaten zu kopieren. GEOTEST benötigt:
1. einen eigenen nativen Dokumenttyp-/Creator-Eintrag;
2. die korrekte Registrierung oder Erkennung durch GeoManager;
3. eine Moniker-/Iconressource im erwarteten GeoWorks-1.x-Format;
4. eine nachgewiesene Zuordnung zwischen Dokumenttyp und Moniker.

## 5. Nächste Schritte

1. Alle Chunks der Ressourcen 39–50 nach demselben 8-Byte-Bitmapvorspann und konsistenter 1-bpp-Länge untersuchen.
2. Die einzelnen Bild-Payloads getrennt dekodieren und als Kontaktbogen vergleichen, ohne Motive voreilig zu benennen.
3. Die Referenzwerte in Ressource 38 gegen die Chunk-Verzeichnisse der Ressourcen 39–50 abgleichen.
4. Danach die generischen Desktop-Tokens und die Moniker-Auswahlroutine verbinden.
5. Separat den Mechanismus für anwendungsspezifische Dokumenttypen `WDAT/WP00` und `DDAT/DP00` ermitteln.

## Status

- Zweiter Chunk in Ressource 40 (Payload ab `0056h`) strukturell als 48×30-/1-bpp-Raster bestätigt.
- Zweiter Chunk in Ressource 41 (Payload ab `0056h`) strukturell als 48×14-/1-bpp-Raster bestätigt.
- Bildmotiv und Dateitypzuordnung offen.
- Keine Originaldatei geändert; kein GEOTEST-Build erstellt; kein Laufzeiterfolg behauptet.


## Korrektur der Chunkpositionen

Die ursprüngliche Fassung hatte die Längenwörter bei `0040h` bzw. `0030h` fälschlich dem Bildchunk zugeordnet. Die Chunk-Verzeichnisse zeigen, dass der jeweilige Bildpayload der zweite Chunk ist und in beiden Ressourcen bei `0056h` beginnt. Die Längenwörter stehen deshalb in beiden Fällen bei `0054h`. Die Größen-/Rasterrechnung bleibt unverändert; korrigiert wurden die relativen Offsets und die Bezeichnung als zweiter Chunk.
