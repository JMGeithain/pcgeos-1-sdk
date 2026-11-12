# Untersuchung 2440 – Formatkennfeld bei +0x3A in den Icon-Deskriptoren

## Ziel

Nach der Bestätigung der Bildabmessungen aus Untersuchung 2439 wurde das 16-Bit-Feld bei relativem Offset `+0x3A` der drei Provider-Deskriptortypen 04, 05 und 06 geprüft. Außerdem wurden die zeitgenössische ICONMAKE-Dokumentation und das mitgelieferte `ICONMAKE.EXE` als Referenz herangezogen.

## Direkte Binärbefunde

In den sieben untersuchten Provider-Dateien gilt:

- Deskriptortyp 04: Feld `+0x3A = 0x0001`
- Deskriptortyp 05: Feld `+0x3A = 0x0001`
- Deskriptortyp 06: Feld `+0x3A = 0x1101`

Die Werte wurden als little-endian 16-Bit-Wörter gelesen. Die Unterscheidung ist in allen sieben Dateien reproduzierbar.

| Provider | Typ 04 | Typ 05 | Typ 06 |
|---|---:|---:|---:|
| GDOC | 0x0001 | 0x0001 | 0x1101 |
| PAPR | 0x0001 | 0x0001 | 0x1101 |
| BEER | 0x0001 | 0x0001 | 0x1101 |
| BILL | 0x0001 | 0x0001 | 0x1101 |
| BUTN | 0x0001 | 0x0001 | 0x1101 |
| ZIPR | 0x0001 | 0x0001 | 0x1101 |
| GEXE | 0x0001 | 0x0001 | 0x1101 |

## Zusammenhang mit den bestätigten Bildmaßen

Die Bildmaße aus Untersuchung 2439 bleiben:

| Typ | Breite | Höhe | Feld +0x3A |
|---|---:|---:|---:|
| 04 | 48 | 14 | 0x0001 |
| 05 | 48 | 30 | 0x0001 |
| 06 | 48 | 30 | 0x1101 |

Damit unterscheidet das Feld Typ 06 von den beiden monochromen Profilen. Das passt zum unabhängigen ICONMAKE-Dokumentationsbefund, dass das 48×30-EGA-Profil 16 Farben verwendet, während CGA und HGC/MCGA monochrom sind.

**Wichtig:** Die Korrelation ist stark, aber die exakte Semantik des Wertes `0x1101` ist durch die vorliegenden Belege nicht formal bewiesen. Es wird deshalb als Format-/Flags-Kandidat bezeichnet, nicht als bestätigter numerischer Farbtiefenwert.

## ICONMAKE-Referenz

Die deutsche und englische Dokumentation `ICONMAKE.DOC` / `ICONMAKE.ENG` aus dem Archiv beschreibt drei Profile:

- CGA: 48×14 Pixel, monochrom;
- HGC/MCGA: 48×30 Pixel, monochrom;
- EGA: 48×30 Pixel, 16 Farben.

Die Dokumentation bestätigt somit die Profilbedeutung der drei Bildabmessungen. Sie erklärt in den vorliegenden Textpassagen jedoch nicht das interne 16-Bit-Feld bei `+0x3A`.

Das archivierte `ICONMAKE.EXE` (19.477 Byte) enthält unter anderem die Strings `_CGA`, `_HGC`, `_EGA`, `ICONMAKE x <geos_file>` und `to extract icons to PCX files`. Diese Strings bestätigen die drei Varianten und die Extraktionsfunktion des Werkzeugs. Sie liefern für sich genommen keine Felddefinition für `0x1101`.

## Konsequenz

Die Kombination aus Bildmaßen und Feldwerten erlaubt nun eine sichere Klassifikation der drei Profile auf Ebene der Provider-Deskriptoren:

- Typ 04: 48×14, monochromes Profil;
- Typ 05: 48×30, monochromes Profil;
- Typ 06: 48×30, EGA-Farbprofil mit 16 Farben laut ICONMAKE-Dokumentation; das Feld `0x1101` ist das zugehörige, noch nicht formal entschlüsselte Kennfeld.

Noch nicht entschlüsselt sind:

- die genaue Bedeutung der Bits in `0x1101`;
- die konkrete Pixelablage (packed oder planar);
- die Kompression oder Kodierung der Bilddaten;
- die genaue Startposition und Länge der Bilddaten relativ zu den Deskriptoren.

## Nächster Schritt

Der nächste Schritt ist die Untersuchung des mitgelieferten `ICONMAKE.EXE`-Codes beziehungsweise ein reproduzierbarer Extraktionstest mit ICONMAKE unter einer geeigneten DOS-Umgebung. Besonders wertvoll wäre ein Vergleich: Ein Original-Provider wird mit ICONMAKE extrahiert; die erzeugten PCX-Daten werden dann mit den Bytebereichen aus dem Provider abgeglichen. So ließe sich die Bilddatenkodierung ohne Spekulation bestimmen.

## Methodik und Grenzen

- Direkter Bytevergleich von sieben Original-Provider-Geodes aus `GEOWORKS.zip`.
- `ICONMAKE.DOC`, `ICONMAKE.ENG` und `ICONMAKE.EXE` wurden im Archiv nachgewiesen.
- Ausschließlich statische, lesende Analyse; `ICONMAKE.EXE` wurde nicht ausgeführt.
- Keine Änderungen an Originaldateien, `TOKEN.DB` oder `GEOS.INI`.
- Kein Laufzeittest in GeoWorks.
- Die Feldsemantik von `0x0001` und `0x1101` ist nicht abschließend bewiesen.
