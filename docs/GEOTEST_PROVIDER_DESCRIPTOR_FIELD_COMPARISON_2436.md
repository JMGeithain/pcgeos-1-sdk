# Untersuchung 2436 – Feldvergleich der Provider-Deskriptoren bei 0x3F0 und 0x48x

## Ziel

Die in Untersuchung 2435 erkannten Strukturen mit Präfix `23 00 00 00` wurden anhand der Originalbytes aus sieben Provider-Geodes verglichen. Dabei wurden die Positionen nicht pauschal als feste Offsets angenommen: Der zweite Deskriptor liegt je nach Datei bei `0x484` oder `0x494`.

## Datenbasis

Dateien aus `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/`:

`GDOC.000`, `PAPR.000`, `BEER.000`, `BILL.000`, `BUTN.000`, `ZIPR.000`, `GEXE.000`.

## Erster Deskriptor

Alle sieben Dateien enthalten bei Dateioffset `0x3F0` die Folge:

```
23 00 00 00 04 00 20 00 00 C0 02 00
```

Unmittelbar danach steht ein 16-Bit-Wert, der je Provider variiert:

| Datei | Wort bei 0x3FC |
|---|---:|
| GDOC | 0x0094 |
| PAPR | 0x0098 |
| BEER | 0x0094 |
| BILL | 0x0090 |
| BUTN | 0x0098 |
| ZIPR | 0x009C |
| GEXE | 0x0090 |

Weitere Wörter im Bereich sind beispielsweise bei `0x408`:

- GDOC/PAPR/BEER/BUTN/ZIPR: `0x00A0`
- BILL/GEXE: `0x0090`

Die Bytes an `0x3FC` und `0x408` dürfen noch nicht als Bildbreite, Bildhöhe oder Datenlänge bezeichnet werden. Ihre Semantik ist offen.

## Gemeinsame Felder ab 0x410

Bei allen sieben Dateien sind in diesem Teil mehrere Werte identisch:

- `0x414`: `26 00 2A 00`
- `0x418`: beginnt mit `04 00`
- `0x41C`: enthält ein 16-Bit-Wort mit dem Wert `0x3061` an Byteposition `0x41E`
- `0x420`: enthält `0E 00 1A 00`

Einige unmittelbar benachbarte Werte variieren providerabhängig. Zum Beispiel stehen bei `0x418` die ersten beiden Bytes als `6C 00` bei GDOC/BEER, `70 00` bei PAPR, `65 00` bei BILL, `6E 00` bei BUTN, `73 00` bei ZIPR und `68 00` bei GEXE.

Diese Werte liegen in einem strukturierten Datensatz, aber ohne Kenntnis des zugrundeliegenden Resource-/Monikerformats ist ihre Bedeutung nicht sicher.

## Zweiter Deskriptor: variable Position

Der nächste sichtbare Datensatz mit Präfix `23 00 00 00 05 00 20 00 00 C0 02 00` liegt nicht immer an derselben Position:

| Dateien | Position |
|---|---:|
| GDOC, PAPR, BEER, BUTN, ZIPR | 0x494 |
| BILL, GEXE | 0x484 |

Das ist ein wichtiger Hinweis: Die zweite Struktur wird nicht über einen für alle Provider identischen absoluten Offset adressiert. Eine starre GEOTEST-Vorlage darf diese Position daher nicht fest verdrahten.

Nach dem gemeinsamen 12-Byte-Präfix folgt wiederum ein variierender 16-Bit-Wert:

| Datei | Wort nach Präfix |
|---|---:|
| GDOC | 0x00F4 |
| PAPR | 0x010C |
| BEER | 0x00F4 |
| BILL | 0x00EC |
| BUTN | 0x0108 |
| ZIPR | 0x010C |
| GEXE | 0x00F4 |

## Was die Bytes belegen – und was nicht

Gesichert:

1. Der erste Deskriptor beginnt in allen sieben Dateien bei `0x3F0`.
2. Sein 12-Byte-Präfix ist identisch.
3. Danach folgen providerabhängige 16-Bit-Werte.
4. Der zweite Deskriptor besitzt ebenfalls ein wiederkehrendes 12-Byte-Präfix.
5. Der zweite Deskriptor liegt je nach Datei bei `0x484` oder `0x494`.
6. Seine nachfolgenden 16-Bit-Werte variieren.

Nicht bewiesen:

- dass die 16-Bit-Werte Offsets, Längen, Breiten oder Höhen sind;
- dass jeder Deskriptor genau einer Bildschirmvariante entspricht;
- dass die folgenden Bytes unkomprimierte Pixel enthalten;
- dass die beiden Deskriptoren bereits alle drei ICONMAKE-Varianten abdecken.

## Konsequenz für den Decoder

Ein Decoder-Prototyp darf nicht von einem festen zweiten Deskriptoroffset ausgehen. Er muss zunächst das Strukturpräfix `23 00 00 00 05 00 20 00 00 C0 02 00` erkennen und anschließend die Feldgrenzen unabhängig validieren.

Die Werte `0x0090` bis `0x009C` sowie `0x00EC` bis `0x010C` werden vorerst nur als rohe 16-Bit-Feldwerte dokumentiert. Eine Interpretation als Bildgröße oder Ressourcengröße wäre derzeit Spekulation.

## Nächster Schritt

Die Datensätze werden über ihre vollständigen Bytebereiche verfolgt, insbesondere über die variablen Positionen und die Übergänge zu den providerabhängigen Bildkandidaten. Danach werden die Ergebnisse mit den ICONMAKE-Profilen 48×14 monochrom, 48×30 monochrom und 48×30 16 Farben abgeglichen. Erst wenn ein Feldwert rechnerisch mit einer nachgewiesenen Datenlänge zusammenpasst, wird ihm eine Bedeutung zugewiesen.

## Methodik und Grenzen

- Statische, lesende Analyse der Originaldateien aus `GEOWORKS.zip`.
- Keine Änderung an `TOKEN.DB`, `GEOS.INI` oder Provider-Geodes.
- Kein Laufzeittest in GeoWorks.
- Alle nicht direkt belegten Felddeutungen bleiben ausdrücklich offen.
