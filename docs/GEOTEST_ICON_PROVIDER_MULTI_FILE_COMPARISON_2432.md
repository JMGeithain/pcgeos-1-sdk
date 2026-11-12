# Untersuchung 2432 – Vergleich mehrerer originaler Icon-Provider-Geodes

## Ziel

Die in Untersuchung 2429 eingegrenzten Ressourcenbereiche von `GDOC.000` und `PAPR.000` wurden mit weiteren originalen Icon-Provider-Geodes aus demselben GeoWorks-Archiv verglichen. Damit sollte geprüft werden, ob die ersten Ressourcenbereiche ein gemeinsames Template bilden und welche Bereiche je Token variieren.

## Datenbasis

Untersuchte Dateien aus `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/`:

- `GDOC.000` – 2.256 Byte
- `PAPR.000` – 2.208 Byte
- `BEER.000` – 2.160 Byte
- `BILL.000` – 2.064 Byte
- `BUTN.000` – 2.208 Byte
- `ZIPR.000` – 2.288 Byte
- `GEXE.000` – 2.240 Byte
- zusätzlich `EART00FF.000` – 2.080 Byte

Die Geode-Basis wurde bei Dateioffset `0x100` angesetzt. Die sieben 32-Bit-Werte der Offsettabelle beginnen bei `0x13C` und werden relativ zur Geode-Basis interpretiert. Die Bereichsgrenzen werden aus den sortierten unterschiedlichen Zieloffsets und dem Dateiende gebildet.

## Ergebnis: drei vollständig gemeinsame Bereiche

Bei GDOC, PAPR, BEER, BILL, BUTN, ZIPR und GEXE sind die ersten drei unterschiedlichen Zielpositionen identisch:

| Bereich | Absoluter Dateioffset | Länge |
|---|---:|---:|
| 1 | `0x274` | 104 Byte |
| 2 | `0x2DC` | 212 Byte |
| 3 | `0x3B0` | 324 Byte |

Ein Bytevergleich ergab für diese drei Bereiche vollständige Identität über alle sieben Provider-Dateien.

Das ist ein belastbarer Hinweis auf einen gemeinsamen Geode-/Provider-Grundaufbau. Die exakte Semantik jedes einzelnen Bereichs ist damit noch nicht festgelegt; insbesondere wird hier nicht behauptet, dass alle drei Bereiche ausschließlich Programmcode enthalten.

## Die nachfolgenden Bereiche variieren

Ab dem Zieloffset `0x4F4` unterscheiden sich die Inhalte zwischen den Providern. Auch die nachfolgenden Offsetpositionen und Bereichslängen sind nicht durchgehend identisch.

Beispiele:

| Provider | Bereich ab 0x4F4 | nächster Bereich | letzter Bereich |
|---|---:|---:|---:|
| GDOC | 164 Byte | 260 Byte | 564 Byte |
| PAPR | 164 Byte | 276 Byte | 500 Byte |
| BEER | 164 Byte | 260 Byte | 468 Byte |
| BILL | 148 Byte | 244 Byte | 404 Byte |
| BUTN | 164 Byte | 276 Byte | 500 Byte |
| ZIPR | 164 Byte | 276 Byte | 580 Byte |
| GEXE | 148 Byte | 260 Byte | 564 Byte |

Die Werte sind die gemessenen Bytebereiche zwischen den unterschiedlichen Offsetpositionen beziehungsweise bis zum Dateiende. Sie sind keine bestätigten isolierten Bitmapgrößen.

## Sonderfall EART00FF.000

`EART00FF.000` weist ebenfalls die gemeinsamen ersten drei Bereiche bei `0x274`, `0x2DC` und `0x3B0` auf. Seine spätere Offsettabelle weicht jedoch deutlich ab: Der letzte unterschiedliche Zieloffset liegt bei `0x81C`, und bis zum Dateiende verbleiben dort nur vier Byte.

Diese Datei darf daher nicht ohne gesonderte Prüfung in die Annahme eines einheitlichen Drei-Icon-Ressourcenlayouts einbezogen werden. Möglicherweise handelt es sich um eine abweichende Variante oder eine besondere Datenstruktur; die Ursache ist offen.

## Konsequenzen für die Bitmap-Analyse

Der Vergleich mit mehreren Provider-Dateien stärkt die Annahme, dass der gemeinsame Bereich bis `0x4F3` zum wiederverwendeten Provider-Grundgerüst gehört. Die tokenabhängigen Daten beginnen in den regulären Beispielen ab `0x4F4`.

Damit lässt sich die nächste Analyse gezielter durchführen:

1. Gemeinsame Bereiche `0x274–0x4F3` vorerst als gemeinsames Grundgerüst behandeln.
2. Providerabhängige Bereiche ab `0x4F4` getrennt untersuchen.
3. Nach wiederkehrenden Headern und Datenlängen über viele Icons suchen.
4. Die drei ICONMAKE-Bildprofile 48×14 monochrom, 48×30 monochrom und 48×30 mit 16 Farben als Sollprofile verwenden.
5. Erst nach erfolgreicher Dekodierung eine konkrete Ressource als CGA-, HGC/MCGA- oder EGA-Icon bezeichnen.

## Gesicherte Aussagen und offene Fragen

Gesichert:

- Sieben Provider-Dateien haben dieselben ersten drei unterschiedlichen Zieloffsets.
- Die ersten drei Bereiche sind in diesen sieben Dateien byteidentisch.
- Ihre Längen betragen 104, 212 und 324 Byte.
- Die späteren Bereiche unterscheiden sich in Inhalt und zum Teil auch in Länge.

Noch offen:

- die exakte semantische Rolle der ersten drei Ressourcen;
- die interne Struktur und Codierung der tokenabhängigen Bereiche;
- die konkrete Zuordnung der späteren Bereiche zu CGA, HGC/MCGA und EGA;
- die Erklärung des Sonderfalls EART00FF.000.

## Konsequenz für GEOTEST

Für GEOTEST ist ein eigener Provider nach dem Muster der originalen Icon-Dummy-Geodes nun ein plausibler Entwicklungsweg. Das gemeinsame Grundgerüst könnte als Referenz dienen. Es wird aber noch kein Original-Provider kopiert oder verändert und kein eigener Dokument-Token als lauffähig bestätigt.

Die konkrete GEOTEST-Provider-Geode wird erst nach vollständiger Analyse der Ressourcenstruktur und einem separaten GeoWorks-1.2.8-Laufzeittest gebaut.

## Methodik und Grenzen

- Ausschließlich statische, lesende Analyse der Dateien im Archiv `GEOWORKS.zip`.
- Keine Änderungen an `TOKEN.DB`, `GEOS.INI` oder den Provider-Dateien.
- Kein Laufzeittest in GeoWorks.
- Die Aussagen gelten für die genannten Dateien aus dem untersuchten Archiv.
