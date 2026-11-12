# Untersuchung 2431 – Größen- und Strukturprüfung der drei Icon-Kandidaten

## Datenbasis

Untersucht wurden die Originaldateien aus `GEOWORKS/ICONS/` im Archiv `GEOWORKS.zip`:

- `GDOC.000`: 2.256 Byte, SHA-256 `fe19cbcb46c2a92cf02da64c963facb8decb95d7e60bca34eb0d1c5e00b01733`
- `PAPR.000`: 2.208 Byte, SHA-256 `30b08761294ccd7762c686ca3d477e509cb454f56b6c7db5aa2b1497efbabfbe`

Die Offsettabelle beginnt bei Dateioffset `0x13C`; die Werte werden relativ zur Geode-Basis `0x100` interpretiert. Die drei letzten unterschiedlichen Positionen liegen bei `0x4F4`, `0x598` und `0x69C` (GDOC) beziehungsweise `0x4F4`, `0x598` und `0x6AC` (PAPR).

## Gemessene Bereichslängen

Die Grenzen ergeben sich aus dem jeweils folgenden Offset bzw. Dateiende:

| Kandidat | GDOC.000 | PAPR.000 |
|---|---:|---:|
| Bereich ab `0x4F4` | 164 Byte | 164 Byte |
| Bereich ab `0x598` | 260 Byte | 276 Byte |
| letzter Bereich | 564 Byte | 500 Byte |

Die Längen unterscheiden sich von den reinen Pixeldaten-Größen der in ICONMAKE.DOC beschriebenen Standardformate:

| Dokumentiertes Format | Unkomprimierte Pixeldaten bei dicht gepackten Zeilen |
|---|---:|
| 48 × 14, 1 Bit/Pixel | 84 Byte |
| 48 × 30, 1 Bit/Pixel | 180 Byte |
| 48 × 30, 4 Bit/Pixel | 720 Byte |

Berechnung:
- 48 × 14 × 1 / 8 = 84 Byte.
- 48 × 30 × 1 / 8 = 180 Byte.
- 48 × 30 × 4 / 8 = 720 Byte.

Diese Werte berücksichtigen weder Ressourcenheader noch Zeilenpadding, Planes, Kompression oder Alignment.

## Rohdatenbeobachtungen

### Bereich ab 0x4F4

GDOC und PAPR haben jeweils 164 Byte. Die Inhalte unterscheiden sich vollständig bereits am Anfang:

- GDOC: `05 0E 3F C7 F1 F8 70 00 0E FD 00 00 70 ...`
- PAPR: `91 49 9C 40 63 80 05 9D 49 54 5A A2 80 00 80 FE ...`

### Bereich ab 0x598

- GDOC: 260 Byte; Beginn `23 00 00 00 06 00 20 00 00 C0 02 00 30 03 02 00 ...`
- PAPR: 276 Byte; Beginn `00 C0 00 1F FD FF 00 80 00 CC CC CC 00 00 00 00 23 00 00 00 ...`

Bei PAPR taucht die markante Folge `23 00 00 00 06 00 20 00` erst 16 Byte nach dem Bereichsanfang auf. Das legt nahe, dass dieser Bereich bei PAPR zusätzliche oder anders angeordnete Daten vor dem gemeinsamen Muster enthält. Die Bedeutung ist offen.

### Letzter Bereich

- GDOC: 564 Byte; Beginn `22 FF F7 70 DD DD 00 0F FD FF 00 F0 ...`
- PAPR: 500 Byte; Beginn `00 70 FD 77 06 7F FF 07 07 0D DD DD FC FF 00 E0 ...`

Beide Bereiche enthalten wiederkehrende Bytefolgen und stark strukturierte Werte. Das ist mit einer kodierten oder komprimierten Darstellung vereinbar, beweist aber weder ein bestimmtes RLE-Verfahren noch eine konkrete Pixelanordnung.

## Bewertung der Format-Hypothesen

Die drei providerabhängigen Bereiche könnten zu den drei dokumentierten Icon-Varianten gehören. Die Längen allein reichen nicht aus, um sie CGA, HGC/MCGA und EGA zuzuordnen:

- Der 164-Byte-Bereich ist größer als 84 Byte, aber kleiner als 180 Byte.
- Die 260-/276-Byte-Bereiche sind größer als 180 Byte.
- Die 500-/564-Byte-Bereiche sind kleiner als 720 Byte.

Eine Kompression könnte diese Abweichungen erklären; Header, Zeilenpadding oder getrennte Planes könnten sie ebenfalls beeinflussen. Ohne Decoder ist keine dieser Erklärungen bestätigt.

## Ergebnis

Gesichert sind die drei unterschiedlichen Datenbereiche und ihre exakten Längen. Die Inhalte sind providerabhängig. Die drei dokumentierten ICONMAKE-Profile liefern nützliche Sollwerte, aber noch keine bewiesene Zuordnung.

**Keine bestätigte Bitmap-Dekodierung liegt vor.** Insbesondere werden die Bereiche nicht als CGA, HGC/MCGA oder EGA etikettiert, solange Breite, Höhe, Farbtiefe und dekodierte Pixel reproduzierbar nachgewiesen sind.

## Nächster Schritt

Als nächstes sind die Datenbereiche auf interne Header-/Längenfelder, Zeilenstrukturen, Bitplane-Muster und mögliche Lauflängencodierung zu prüfen. Ein Decoder muss anschließend mindestens ein plausibles 48×14- beziehungsweise 48×30-Bild erzeugen und die Ergebnisse gegen beide Provider-Dateien reproduzierbar machen.

## Methodik und Grenzen

- Ausschließlich statische, lesende Analyse der Archivdateien.
- Keine Änderung an `TOKEN.DB`, `GEOS.INI` oder Provider-Geodes.
- Kein Laufzeittest in GeoWorks.
- Die Größenangaben beziehen sich auf Bytebereiche zwischen den aus der Offsettabelle abgeleiteten Grenzen, nicht auf bestätigte isolierte Bitmapressourcen.
