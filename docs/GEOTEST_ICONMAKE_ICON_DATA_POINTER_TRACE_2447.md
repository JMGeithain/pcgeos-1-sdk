# Untersuchung 2447 – Verfolgung der Icon-Datenverweise (+0x0C)

## Ziel

Die 16-Bit-Felder bei Deskriptoroffset +0x0C in den ICONMAKE-Providern wurden gegen die Ressourcenanfänge und tatsächlichen Dateibytes geprüft. Untersucht wurden `GTI1FFFE.000`, `GTI2FFFD.000`, `GDOC.000` und `PAPR.000`.

## 1. Ergebnis: +0x0C ist ein relativer Offset ab Dateiposition 0x3B0

Für alle drei Icondeskriptoren ergibt sich dieselbe Bezugsbasis:

`Zielposition = 0x3B0 + WORD(Deskriptor + 0x0C)`

Die Basis `0x3B0` ist zugleich der absolute Start der vierten Ressource (Ressourcen-Offset relativ zum Geode-Basisoffset 0x100: 0x2B0).

| Profil | Datei | Deskriptor | Wert +0x0C | Berechnetes Ziel |
|---|---|---:|---:|---:|
| CGA | GTI1 / GDOC | 0x3F0 | 0x0094 | 0x444 |
| CGA | GTI2 / PAPR | 0x3F0 | 0x0098 | 0x448 |
| HGC | GTI1 / GDOC | 0x494 | 0x00F4 | 0x4A4 |
| HGC | GTI2 / PAPR | 0x494 | 0x010C | 0x4BC |
| EGA | GTI1 / GDOC | 0x598 | 0x0330 | 0x6E0 |
| EGA | GTI2 / PAPR | 0x5A8 | 0x02F0 | 0x6A0 |

Die berechneten Ziele zeigen auf unterschiedliche Datenbereiche und nicht auf die Deskriptoren selbst.

## 2. Bytebereich der monochromen Bilder

Die PCX-Profile sind 48 Pixel breit. Bei 1 Bit pro Pixel ergeben sich pro Zeile 6 Byte.

- CGA: 48 × 14 / 8 = 84 Byte.
- HGC: 48 × 30 / 8 = 180 Byte.

Die Zielbereiche sind in den untersuchten Dateien bytegenau mit diesen Längen abgrenzbar:

| Profil | GTI1/GDOC-Ziel | Länge | GTI2/PAPR-Ziel | Länge |
|---|---:|---:|---:|---:|
| CGA | 0x444 | 84 Byte | 0x448 | 84 Byte |
| HGC | 0x4A4 | 180 Byte | 0x4BC | 180 Byte |

Die CGA- und HGC-Bereiche liegen an den berechneten Zielen. Die Größen stimmen exakt mit der unkomprimierten 1-Bit-Zeilendatenmenge überein. Das ist ein starker, direkt nachrechenbarer Beleg, dass +0x0C auf die Icon-Bilddaten verweist.

Hinweis: Die Bytezahl allein beweist noch nicht sämtliche Details der Bitreihenfolge, Zeilenorientierung oder eventueller Zusatzflags.

## 3. EGA-Bilddaten

Die EGA-Zielpositionen lauten:

- GTI1/GDOC: 0x6E0
- GTI2/PAPR: 0x6A0

Die jeweiligen Dateien enden bei 0x8D0 bzw. 0x8A0. Damit verbleiben ab Zielposition jeweils 496 Byte (GTI1/GDOC) bzw. 512 Byte (GTI2/PAPR).

Ein 48×30-Bild mit 4 Bit pro Pixel würde unkomprimiert 720 Byte benötigen. Die kürzeren Datenbereiche zeigen, dass die EGA-Daten nicht einfach als 720 Byte rohe 4-Bit-Pixelmatrix vorliegen. Eine Kompression oder ein anderes gepacktes Datenformat ist wahrscheinlich; die konkrete Kodierung ist mit diesem Schritt noch nicht dekodiert.

## 4. Bedeutung für die Ressourcenstruktur

Die Offsetbasis 0x3B0 fällt mit dem Beginn der vierten Ressource zusammen. Die berechneten Bildziele liegen je nach Profil in späteren Dateibereichen. Der Deskriptor kann daher auf Bilddaten außerhalb seines eigenen unmittelbaren Deskriptorbereichs verweisen.

Das ist wichtig für einen eigenen Provider: Ein Deskriptor und sein Bilddatenblock dürfen nicht unabhängig voneinander verschoben werden, ohne den relativen Offset korrekt anzupassen.

## 5. Ergebnisstatus

**Nachgewiesen:**
1. Das Feld +0x0C ist in allen vier untersuchten Providern mit der Bezugsbasis 0x3B0 konsistent.
2. Die berechneten Ziele führen zu den tatsächlichen Bilddatenbereichen.
3. Die monochromen Datenbereiche umfassen exakt 84 Byte (CGA) und 180 Byte (HGC).
4. Die EGA-Bereiche sind kürzer als eine rohe 48×30×4-Bit-Matrix und benötigen weitere Formatuntersuchung.

**Noch offen:**
1. Bitreihenfolge und Pixelorientierung der monochromen Bilddaten.
2. Exakte EGA-Kompression bzw. Packung.
3. Vollständige Bedeutung der übrigen Deskriptorfelder.
4. Laufzeitbestätigung durch GeoWorks 1.2/GeoManager.

## 6. Nächster Schritt

Als nächstes die 84-Byte- und 180-Byte-Monochrombereiche mit den jeweiligen PCX-Bildern pixelweise vergleichen. Danach die EGA-Payload separat untersuchen und ein kleines Testprogramm zur Dekodierung aufbauen. Noch keine Änderungen an produktiven Token- oder Systemdateien vornehmen.

## Quellen und Reproduzierbarkeit

- Nutzerdateien: `GTI1FFFE.000`, `GTI2FFFD.000`.
- Originale aus `GEOWORKS.zip`: `GEOWORKS/ICONS/GDOC.000`, `GEOWORKS/ICONS/PAPR.000`.
- Nutzer-PCX-Dateien: GDOC_CGA/HGC/EGA und PAPR_CGA/HGC/EGA.
- `ICONMAKE.ENG` und `ICONMAKE.DOC`, Beschreibung der drei Bildprofile.
- Offsets und Längen wurden direkt aus den Dateien gelesen; Little-Endian-Wörter wurden als 16-Bit-Werte interpretiert.
