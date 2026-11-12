# Untersuchung 2429 – Vergleich der Ressourcenbereiche in GDOC.000 und PAPR.000

## Ausgangspunkt

Die Untersuchung baut auf der Offsettabelle aus Untersuchung 2428 auf. Die Dateien wurden erneut direkt aus `GEOWORKS.zip` gelesen. Alle Offsets unten sind absolute Dateioffsets, sofern ausdrücklich als relativ bezeichnet.

## Bestätigte Offsets und Endgrenzen

Die Geode-Basis liegt bei `0x100`. Die sieben Tabellenwerte werden als Offsets relativ zu dieser Basis interpretiert. Die beiden ersten Tabelleneinträge zeigen in beiden Dateien auf dieselbe Position `0x274`.

| Bereich | GDOC.000 | PAPR.000 |
|---|---:|---:|
| gemeinsamer erster Bereich | 0x274–0x2DB | 0x274–0x2DB |
| gemeinsamer zweiter Bereich | 0x2DC–0x3AF | 0x2DC–0x3AF |
| gemeinsamer dritter Bereich | 0x3B0–0x4F3 | 0x3B0–0x4F3 |
| vierter Bereich | 0x4F4–0x597 | 0x4F4–0x597 |
| fünfter Bereich | 0x598–0x69B | 0x598–0x6AB |
| sechster Bereich | 0x69C–Dateiende | 0x6AC–Dateiende |

Die Endgrenzen ergeben sich jeweils aus dem nächsten unterschiedlichen Offset beziehungsweise dem Dateiende. Das sind zunächst reine Bytebereiche, noch keine abschließend klassifizierten Ressourcen.

## Strukturvergleich

Die Bereiche ab `0x274`, `0x2DC` und `0x3B0` sind byteidentisch zwischen beiden Dateien. Das ist ein starker Befund für einen gemeinsamen Bestandteil der beiden Provider-Geodes.

Ab `0x4F4` unterscheiden sich die Dateien. Auch die letzte Offsetposition unterscheidet sich: GDOC verweist auf relativ `0x59C` (absolut `0x69C`), PAPR auf relativ `0x5AC` (absolut `0x6AC`). Damit ist die fünfte Position in PAPR um 16 Byte länger als in GDOC, bevor der letzte Bereich beginnt.

## Auffällige Bytes an den Bereichsanfängen

Die folgenden Hexfolgen sind die ersten Bytes der jeweiligen Bereiche:

| Dateioffset | GDOC.000 | PAPR.000 |
|---|---|---|
| `0x274` | `44 00 00 00 08 00 00 00 ...` | identisch |
| `0x2DC` | `08 00 00 03 02 02 02 00 ...` | identisch |
| `0x3B0` | `28 00 00 40 C6 10 22 00 ...` | identisch |
| `0x4F4` | `05 0E 3F C7 F1 F8 70 00 ...` | `91 49 9C 40 63 80 05 9D ...` |
| `0x598` | `23 00 00 00 06 00 20 00 ...` | `00 C0 00 1F FD FF 00 80 ...` |
| letzter Bereich | `0x69C`: `22 FF F7 70 DD DD 00 0F ...` | `0x6AC`: `00 70 FD 77 06 7F FF 07 ...` |

## Vorläufige Interpretation

1. Die ersten drei Bereiche sind in beiden Provider-Dateien exakt gleich. Sie gehören daher wahrscheinlich zum gemeinsamen Programm-/Metadatenanteil oder zu gemeinsam genutzten Ressourcen. Eine genauere Klassifikation erfordert die Dekodierung der jeweiligen Unterstrukturen.
2. Die Bereiche ab `0x4F4` sind providerabhängig. Die Daten sind nicht als einfacher gemeinsamer Header zu behandeln.
3. Die Bytes ab `0x598` enthalten bei beiden Dateien auffällige strukturierte Felder und anschließend Daten, die sich deutlich unterscheiden.
4. Die letzten Bereiche ab `0x69C` (GDOC) und `0x6AC` (PAPR) sehen in den Rohdaten nach kompakten Grafik-/Bitmapdaten aus. Das ist ein Kandidat, keine bestätigte Dekodierung.
5. Die Daten können erst dann als CGA-, HGC- oder EGA-Moniker klassifiziert werden, wenn ein Decoder die erwarteten Maße, Bitplanes und Pixelwerte reproduzierbar aus ihnen gewinnt.

## Konsequenz für GEOTEST

Die Untersuchung bestätigt noch keine konkrete Icon-Registrierung für `GEOTEST.GEO`. Sie grenzt aber den interessanten Teil der Provider-Dateien ein: Die providerabhängigen Bereiche beginnen ab `0x4F4`; die mutmaßlich grafischen Rohdaten liegen am Ende der Dateien.

Es wäre weiterhin verfrüht, `GTD1`, `.GTD` oder ein TOKEN.DB-Feld als fertige Lösung zu übernehmen. Für GEOTEST bleibt ein eigener Dokumenttyp samt eigener Token-/Icon-Registrierung das Ziel, sobald der GeoWorks-1.x-Mechanismus vollständig verstanden ist.

## Nächster Schritt

Die Bereiche ab `0x4F4`, `0x598` und dem jeweiligen letzten Offset müssen anhand ihrer internen Headerfelder dekodiert werden. Insbesondere sind Breite, Höhe, Pixelformat, Planes und mögliche Kompressionsverfahren zu identifizieren. Anschließend kann geprüft werden, ob die Daten zu den zuvor notierten CGA-/HGC-/EGA-Moniker-Kandidaten passen.

## Methodik und Grenzen

- Ausschließlich statische, lesende Analyse der Originaldateien aus dem Archiv.
- Keine Änderung an `TOKEN.DB`, `GEOS.INI` oder Provider-Geodes.
- Kein Laufzeittest in GeoWorks.
- Die Bezeichnung „Bitmap-/Moniker-Kandidat“ ist ausdrücklich vorläufig und kein bestätigtes Formatlabel.
