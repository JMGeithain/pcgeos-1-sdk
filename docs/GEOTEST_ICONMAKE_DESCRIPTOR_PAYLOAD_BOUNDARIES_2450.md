# Untersuchung 2450 – 64-Byte-Icondeskriptoren und direkt anschließende Datenbereiche

## Ziel

Die vier Provider `GDOC.000`, `PAPR.000`, `GTI1FFFE.000` und `GTI2FFFD.000` wurden erneut anhand ihrer tatsächlichen Bytepositionen geprüft. Ziel war, die Icon-Datenbereiche unabhängig von den bislang ungeklärten Feldern +0x0C und +0x18 abzugrenzen.

## 1. Drei Deskriptoren mit jeweils 64 Byte

In allen vier Dateien beginnen die drei Deskriptoren an folgenden Positionen:

| Variante | GDOC / GTI1 | PAPR / GTI2 | Deskriptorende (exklusiv) |
|---|---:|---:|---:|
| CGA, Typ 04 | 0x3F0 | 0x3F0 | 0x430 |
| HGC, Typ 05 | 0x494 | 0x494 | 0x4D4 |
| EGA, Typ 06 | 0x598 | 0x5A8 | 0x5D8 bzw. 0x5E8 |

Jeder Deskriptor umfasst genau 0x40 = 64 Byte. Das Ende wurde jeweils als Startposition + 0x40 berechnet.

## 2. Datenbereiche unmittelbar nach den Deskriptoren

Die Bytes nach dem jeweiligen 64-Byte-Deskriptor reichen bis zum Beginn des nächsten Deskriptors bzw. beim EGA-Profil bis zum Dateiende:

| Variante | GTI1 / GDOC | Länge | GTI2 / PAPR | Länge |
|---|---:|---:|---:|---:|
| CGA | 0x430–0x493 | 100 Byte | 0x430–0x493 | 100 Byte |
| HGC | 0x4D4–0x597 | 196 Byte | 0x4D4–0x5A7 | 212 Byte |
| EGA | 0x5D8–0x8CF | 760 Byte | 0x5E8–0x89F | 696 Byte |

Die Bereichsenden in der Tabelle sind inklusive angegeben. Die Längen sind deshalb jeweils Endadresse - Startadresse + 1.

Diese Abgrenzung folgt allein aus den Deskriptorpositionen und den Dateigrenzen. Sie ist keine Interpretation des Feldes +0x0C.

## 3. Vergleich mit den Original-Providern

Die direkt anschließenden Datenbereiche der ICONMAKE-Dummys stimmen fast vollständig mit den jeweiligen Original-Providern überein:

| Paar | Profil | Bytevergleich |
|---|---|---|
| GTI1 / GDOC | CGA | 100 von 100 Byte identisch |
| GTI1 / GDOC | HGC | 194 von 196 Byte identisch |
| GTI1 / GDOC | EGA | 758 von 760 Byte identisch |
| GTI2 / PAPR | CGA | 100 von 100 Byte identisch |
| GTI2 / PAPR | HGC | 209 von 212 Byte identisch |
| GTI2 / PAPR | EGA | 696 von 696 Byte identisch |

Die Abweichungen liegen jeweils am Ende der Bereiche:
- GTI1/GDOC HGC: Offsets 0x58A und 0x58B; GTI1 enthält dort 00 00, GDOC CC CC.
- GTI1/GDOC EGA: Offsets 0x8CA und 0x8CB; GTI1 enthält dort 00 00, GDOC CC CC.
- GTI2/PAPR HGC: Offsets 0x5A1 bis 0x5A3; GTI2 enthält dort 00 00 00, PAPR CC CC CC.

Das passt zu einem Entfernen bzw. Nullsetzen von Füllbytes am Bereichsende durch ICONMAKE. Die Bilddaten selbst sind in diesen Bereichen ansonsten identisch mit der jeweiligen Vorlage.

## 4. Was ist daraus belastbar abzuleiten?

**Bestätigt:**
1. Die drei Icondeskriptoren sind jeweils 64 Byte lang.
2. Ein Datenbereich beginnt direkt nach jedem Deskriptor.
3. Die Bereiche lassen sich über die nächste Deskriptorposition bzw. Dateigrenze abgrenzen.
4. ICONMAKE übernimmt bei den hier getesteten PCX-Extraktionen die nachfolgenden Providerdaten nahezu byteidentisch aus der Vorlage; die beobachteten Unterschiede betreffen nur die genannten abschließenden CC-Füllbytes.
5. Das Feld +0x0C ist für diese Bereichsabgrenzung nicht erforderlich.

**Noch nicht bestätigt:**
1. Die genaue Kodierung der Datenbereiche (Kompression, Packung, RLE-Variante oder anderes Format).
2. Ob die Bytes vollständig nur die Pixel enthalten oder zusätzlich Steuer-/Zeileninformationen.
3. Die genaue Semantik der Felder +0x0C, +0x18 und weiterer unbekannter Deskriptorfelder.
4. Ob GeoWorks 1.2 die Testprovider bereits korrekt zur Laufzeit anzeigt.

## 5. Konsequenz für GEOTEST

Für einen eigenen Provider muss die Struktur mindestens diese Reihenfolge berücksichtigen:

- 64-Byte-Deskriptor CGA, danach CGA-Datenbereich
- 64-Byte-Deskriptor HGC, danach HGC-Datenbereich
- 64-Byte-Deskriptor EGA, danach EGA-Datenbereich

Die Deskriptoren und ihre Datenbereiche müssen beim Aufbau zusammenbleiben. Noch ist nicht geklärt, welche weiteren Ressourcen- und Geode-Headerfelder für einen eigenständigen Dokument-Token erforderlich sind. Daher wird aus diesem Befund noch kein eigener GEOTEST-Provider erzeugt.

## 6. Nächster Schritt

Als nächstes die Datenbereiche byteweise und strukturell untersuchen:
1. CGA: 100 Byte gegen das 48×14-PCX-Pixelbild.
2. HGC: 196/212 Byte gegen das 48×30-PCX-Pixelbild.
3. EGA: 760/696 Byte gegen die 4-Ebenen-PCX-Datei.
4. Wiederkehrende Steuerbytes, Zeilenmuster und Füllbytes erkennen.
5. Erst danach eine Dekodierungshypothese testen.

## Quellen und Reproduzierbarkeit

- Nutzerdateien: `GTI1FFFE.000`, `GTI2FFFD.000`.
- Originaldateien aus `GEOWORKS.zip`: `GEOWORKS/ICONS/GDOC.000`, `GEOWORKS/ICONS/PAPR.000`.
- Nutzer-PCX-Dateien: GDOC/PAPR CGA, HGC und EGA.
- Deskriptorpositionen, Bereichslängen und Byteunterschiede wurden direkt aus den vier vollständigen Binärdateien berechnet.
- Es wurde kein GeoWorks-Runtime-Test behauptet.
