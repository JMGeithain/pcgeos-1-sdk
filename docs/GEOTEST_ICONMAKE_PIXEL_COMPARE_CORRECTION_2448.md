# Untersuchung 2448 – Pixelvergleich und Korrektur der Bilddatenzeiger-Hypothese

## Ziel

Die sechs vom Nutzer mit ICONMAKE 1.0 extrahierten PCX-Dateien wurden mit den Binärdaten der beiden erzeugten Dummy-Provider verglichen. Dabei wurde zugleich die in Untersuchung 2447 aufgestellte Deutung des Feldes +0x0C überprüft.

## 1. PCX-Dateien technisch geprüft

Alle sechs Dateien lassen sich als PCX öffnen. Die Bildmaße und PCX-Kodierung lauten:

| Datei | Bildgröße | PCX-Bits je Ebene | Ebenen | Bytes je Ebene/Zeile | PIL-Modus |
|---|---:|---:|---:|---:|---|
| GDOC_CGA.PCX | 48×14 | 1 | 1 | 6 | 1 |
| GDOC_HGC.PCX | 48×30 | 1 | 1 | 6 | 1 |
| GDOC_EGA.PCX | 48×30 | 1 | 4 | 6 | P |
| PAPR_CGA.PCX | 48×14 | 1 | 1 | 6 | 1 |
| PAPR_HGC.PCX | 48×30 | 1 | 1 | 6 | 1 |
| PAPR_EGA.PCX | 48×30 | 1 | 4 | 6 | P |

Die EGA-Dateien sind also PCX-Dateien mit vier 1-Bit-Ebenen. Daraus ergeben sich 24 Bytes pro Bildzeile und 720 Bytes für 30 Zeilen, wenn die Ebenen unkomprimiert hintereinander gespeichert würden. Die PCX-Dateien selbst verwenden PCX-RLE; die angegebene Größe ist die dekodierte Ebenenmenge, nicht die Dateigröße.

## 2. Monochrome Pixel wurden neu gepackt

Für CGA und HGC wurden die mit PIL dekodierten Pixel zeilenweise in jeweils sechs Bytes pro Zeile gepackt (48 Pixel, MSB-zuerst). Zusätzlich wurden einfache Varianten mit invertierter Polarität und umgekehrter Bitreihenfolge geprüft.

Keiner dieser einfachen gepackten Pixelströme kommt als zusammenhängende Bytefolge in der entsprechenden vollständigen Providerdatei vor:
- GTI1 gegen GDOC_CGA und GDOC_HGC
- GTI2 gegen PAPR_CGA und PAPR_HGC

Das bedeutet nicht, dass die Icons nicht im Provider enthalten sind. Es bedeutet nur, dass sie nicht als direkt auffindbare, rohe 1-Bit-Zeilenmatrix in dieser einfachen Darstellung vorliegen. Möglich sind ein anderes Bitmap-Layout, eine gepackte/komprimierte Darstellung, zusätzliche Header oder eine andere Pixelcodierung. Keine dieser Möglichkeiten wird hier als erwiesen behauptet.

## 3. Entscheidende Korrektur zu Untersuchung 2447

Die zuvor verwendete Formel

`Dateiposition = 0x3B0 + WORD(Deskriptor + 0x0C)`

ist widerlegt.

Konkretes Beispiel aus `GTI1FFFE.000`:
- HGC-Deskriptor: `0x494`
- Feld +0x0C: `0x00F4`
- frühere Rechnung: `0x3B0 + 0x00F4 = 0x4A4`
- `0x4A4 = 0x494 + 0x10`, liegt also mitten im selben Deskriptor.

Damit kann die berechnete Position nicht der Anfang eines eigenständigen Bilddatenblocks sein. Die frühere Identifikation der vermeintlichen 84-/180-Byte-Bilddatenbereiche und die daraus abgeleitete EGA-Restlängeninterpretation werden zurückgenommen.

Die Rohwerte des Feldes +0x0C bleiben korrekt gemessen; seine Semantik und Bezugsbasis sind unbekannt.

## 4. Was weiterhin bestätigt ist

- Alle sechs PCX-Dateien sind lesbar und besitzen die erwarteten Maße.
- CGA/HGC verwenden PCX 1-Bit-Monochromprofile; EGA verwendet vier 1-Bit-Ebenen.
- Die Deskriptoren 04/05/06 und ihre Maßfelder bleiben als wiederkehrende Strukturen nachgewiesen.
- ICONMAKE hat aus den PCX-Dateien vollständige Dummy-Provider erzeugt.

## 5. Nächster Schritt

Nicht weiter versuchen, die Bilddaten anhand des ungeklärten +0x0C-Feldes zu lokalisieren. Stattdessen:
1. Alle Felder des Deskriptors 04/05/06 positionsgenau gegenüberstellen.
2. Die tatsächlichen Grenzen der Ressourcen und aller inneren Teilbereiche bestimmen.
3. In den Providerbytes nach bekannten Strukturmerkmalen und möglichen Längen-/Typfeldern suchen.
4. Erst wenn ein Bilddatenbereich unabhängig lokalisiert ist, die Bitmapdekodierung erneut angehen.

Bis dahin werden weder +0x0C noch andere unbekannte Felder als Pointer/Handle bezeichnet.

## Quellen und Reproduzierbarkeit

- Nutzerdateien: `GTI1FFFE.000`, `GTI2FFFD.000`.
- Originaldateien aus `GEOWORKS.zip`: `GEOWORKS/ICONS/GDOC.000`, `GEOWORKS/ICONS/PAPR.000`.
- Nutzer-PCX-Dateien: GDOC_CGA/HGC/EGA und PAPR_CGA/HGC/EGA.
- Binärprüfungen: PCX-Headerfelder, Bildmaße, Plane-Anzahl und Bytes-per-line; Little-Endian-Auswertung der Providerdeskriptoren.
- Pixelvergleich: dekodierte 1-Bit-Bilder, zeilenweise in sechs Bytes gepackt; zusätzlich Polaritätsinversion und Bitreihenfolgevarianten.
- Es wurde kein GeoWorks-Runtime-Test behauptet.
