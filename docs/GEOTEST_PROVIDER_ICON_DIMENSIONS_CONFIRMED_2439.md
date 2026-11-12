# Untersuchung 2439 – Bildabmessungen in den Provider-Deskriptoren bestätigt

## Ergebnis

Die drei wiederkehrenden Provider-Deskriptoren enthalten an denselben relativen Positionen explizite Bildabmessungen:

- Breite: 16-Bit-Wert bei relativem Offset `+0x36`
- Höhe: 16-Bit-Wert bei relativem Offset `+0x38`

Bei allen sieben untersuchten Provider-Geodes ergeben sich dieselben Maße:

| Deskriptortyp | Breite | Höhe | Übereinstimmendes ICONMAKE-Profil |
|---|---:|---:|---|
| 04 | 48 | 14 | 48×14 monochrom (CGA) |
| 05 | 48 | 30 | 48×30 monochrom (HGC/MCGA) |
| 06 | 48 | 30 | 48×30, 16 Farben (EGA) |

Die Werte wurden direkt aus den Binärdateien gelesen und als little-endian 16-Bit-Wörter ausgewertet.

## Prüftabelle aller sieben Provider

Die Fundpositionen sind absolute Dateioffsets. Die Maße wurden jeweils an `Fundposition + 0x36` und `Fundposition + 0x38` gelesen.

| Provider | Typ 04 | Typ 05 | Typ 06 |
|---|---|---|---|
| GDOC | 0x3F0: 48×14 | 0x494: 48×30 | 0x598: 48×30 |
| PAPR | 0x3F0: 48×14 | 0x494: 48×30 | 0x5A8: 48×30 |
| BEER | 0x3F0: 48×14 | 0x494: 48×30 | 0x598: 48×30 |
| BILL | 0x3F0: 48×14 | 0x484: 48×30 | 0x578: 48×30 |
| BUTN | 0x3F0: 48×14 | 0x494: 48×30 | 0x5A8: 48×30 |
| ZIPR | 0x3F0: 48×14 | 0x494: 48×30 | 0x5A8: 48×30 |
| GEXE | 0x3F0: 48×14 | 0x484: 48×30 | 0x588: 48×30 |

Damit ist die Abmessungszuordnung nicht nur aus einer Datei abgeleitet: Sie wurde in allen sieben Provider-Dateien reproduziert.

## Konkreter Bytebeleg

Beispiel GDOC, Deskriptor 04 bei `0x3F0`:

- relatives Offset `+0x36`: Bytes `30 00` = 48
- relatives Offset `+0x38`: Bytes `0E 00` = 14

Beispiel GDOC, Deskriptor 05 bei `0x494`:

- relatives Offset `+0x36`: Bytes `30 00` = 48
- relatives Offset `+0x38`: Bytes `1E 00` = 30

Beispiel GDOC, Deskriptor 06 bei `0x598`:

- relatives Offset `+0x36`: Bytes `30 00` = 48
- relatives Offset `+0x38`: Bytes `1E 00` = 30

Die Prüfung aller sieben Dateien ergab dieselben Maße.

## Abgleich mit ICONMAKE 1.0

Die in Untersuchung 2430 aus der Archivdokumentation ICONMAKE 1.0 entnommenen Sollprofile lauten:

- CGA: 48×14, monochrom
- HGC/MCGA: 48×30, monochrom
- EGA: 48×30, 16 Farben

Die gemessenen Abmessungen stimmen exakt mit diesen Profilen überein. Damit ist die Zuordnung der Datensatztypen zu den jeweiligen **Bildabmessungen** bestätigt und die Profilzuordnung sehr stark gestützt.

## Was noch nicht bestätigt ist

Die Abmessungen allein beweisen nicht die Farbtiefe oder das Speicherformat. Im Feld bei relativem Offset `+0x3A` finden sich für Typ 04 und 05 in allen Beispielen die Bytes `01 00`, für Typ 06 dagegen `01 11`. Das ist ein klarer Unterschied, aber die genaue Semantik dieses Feldes ist noch nicht belegt.

Insbesondere bleiben offen:

- ob Typ 06 tatsächlich vier Bits pro Pixel beziehungsweise 16 Farben verwendet;
- ob die Pixel gepackt, planar oder anderweitig codiert sind;
- ob die Daten komprimiert sind;
- wie die Datenbereiche aus den übrigen Deskriptorfeldern lokalisiert werden.

## Konsequenz für GEOTEST

Wir kennen nun die drei erforderlichen Icon-Abmessungen aus den Original-Provider-Dateien. Ein GEOTEST-Provider muss daher die drei Profile in genau diesen Abmessungen berücksichtigen.

Für den nächsten Schritt wird das Feld bei `+0x3A` zusammen mit den benachbarten Werten untersucht. Danach sollen die tatsächlichen Bilddatenbereiche isoliert und mit den erwarteten Rohdatenlängen verglichen werden.

## Methodik und Grenzen

- Direkter Scan der vollständigen Deskriptorsignaturen in sieben Provider-Dateien aus `GEOWORKS.zip`.
- Abmessungen als little-endian 16-Bit-Werte an `+0x36` und `+0x38` gelesen.
- Ausschließlich statische, lesende Analyse.
- Keine Änderungen an Originaldateien, `TOKEN.DB` oder `GEOS.INI`.
- Kein Laufzeittest in GeoWorks.
- Farbtiefe und Kompression sind ausdrücklich noch nicht als bestätigt ausgewiesen.
