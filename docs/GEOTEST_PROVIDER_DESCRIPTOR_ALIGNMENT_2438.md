# Untersuchung 2438 – Bytegenaue Ausrichtung der Deskriptoren 04, 05 und 06

## Ziel und Korrektur

Die sieben Original-Provider wurden erneut direkt aus `GEOWORKS.zip` ausgelesen. Diesmal wurden alle drei Signaturen vollständig gesucht und die ersten 48 Bytes ab jeder Fundstelle ausgegeben.

Wichtige Korrektur zu Untersuchung 2437: Der Datensatz 06 liegt nicht in jeder Datei am Beginn des nächsten äußeren Bereichs. Seine tatsächliche Position wird hier pro Datei anhand der vollständigen Signatur angegeben. Damit werden frühere pauschale Aussagen über seine Lage präzisiert.

## Signaturen

Die drei wiederkehrenden 12-Byte-Präfixe lauten:

```
Typ 04: 23 00 00 00 04 00 20 00 00 C0 02 00
Typ 05: 23 00 00 00 05 00 20 00 00 C0 02 00
Typ 06: 23 00 00 00 06 00 20 00 00 C0 02 00
```

Alle drei Signaturen wurden in jeder der sieben Dateien genau einmal gefunden.

## Tatsächliche Fundpositionen

| Provider | Typ 04 | Typ 05 | Typ 06 |
|---|---:|---:|---:|
| GDOC | 0x3F0 | 0x494 | 0x598 |
| PAPR | 0x3F0 | 0x494 | 0x5A8 |
| BEER | 0x3F0 | 0x494 | 0x598 |
| BILL | 0x3F0 | 0x484 | 0x578 |
| BUTN | 0x3F0 | 0x494 | 0x5A8 |
| ZIPR | 0x3F0 | 0x494 | 0x5A8 |
| GEXE | 0x3F0 | 0x484 | 0x588 |

## Feldvergleich relativ zum jeweiligen Deskriptor

Die ersten 12 Bytes sind das gemeinsame Präfix. Danach folgen unter anderem:

| Relativer Offset | Beobachtung |
|---:|---|
| +0x0C | providerabhängiges 16-Bit-Wort |
| +0x0E | in allen Beispielen `02 00` |
| +0x10 bis +0x17 | mehrere Nullbytes |
| +0x18 | 16-Bit-Wort, teils `00A0h`, `0090h` oder `00F0h` usw. |
| +0x1A bis +0x23 | überwiegend Nullbytes |
| +0x24 | Folge `26 00 2A 00` |
| +0x28 | Folge `04 00 00 02` |
| +0x2C | providerabhängige zwei Bytes |

Beispiele der Wörter bei +0x0C:

| Provider | Typ 04 | Typ 05 | Typ 06 |
|---|---:|---:|---:|
| GDOC | 0x0094 | 0x00F4 | 0x0330 |
| PAPR | 0x0098 | 0x010C | 0x02F0 |
| BEER | 0x0094 | 0x00F4 | 0x02CC |
| BILL | 0x0090 | 0x00EC | 0x0284 |
| BUTN | 0x0098 | 0x0108 | 0x02EC |
| ZIPR | 0x009C | 0x010C | 0x0340 |
| GEXE | 0x0090 | 0x00F4 | 0x0324 |

Diese Werte sind ausdrücklich nur als 16-Bit-Feldwerte notiert. Eine Interpretation als Länge, Breite, Höhe oder Offset ist nicht bewiesen.

## Weitere wiederkehrende Werte

Bei +0x0E steht für alle drei Datensatztypen und alle sieben Provider `02 00`.

Bei +0x24 steht ebenfalls durchgehend `26 00 2A 00`, bei +0x28 `04 00 00 02`. Diese Konstanten sind gute Kandidaten für feste Strukturfelder oder Flags. Ihre genaue Semantik ist offen.

Das Feld bei +0x18 variiert und korreliert nicht unmittelbar mit dem Wert bei +0x0C. Beispielsweise:

- GDOC Typ 04: +0x18 = `00A0h`
- GDOC Typ 05: +0x18 = `0100h`
- GDOC Typ 06: +0x18 = `0330h`

Für die Rekonstruktion ist deshalb wichtig, die beiden Felder getrennt zu behandeln.

## Einordnung

Gesichert ist nun eine regelmäßige Folge dreier Datensatztypen mit identischem 12-Byte-Präfixaufbau und weiteren konstanten Teilfeldern. Die drei Typkennungen 04/05/06 stehen an derselben relativen Position.

Nicht nachgewiesen ist, dass diese Datensätze direkt drei Bildschirmmodi oder Icongrößen beschreiben. Die ICONMAKE-Dokumentation bleibt ein unabhängiger Sollmaßstab; eine direkte Verknüpfung mit den Datensätzen besteht noch nicht.

## Nächster Schritt

Die nächsten Untersuchungen müssen die Daten nach den Deskriptoren auswerten. Dafür werden die 16-Bit-Felder gegen die tatsächlichen Abstände zwischen Deskriptoren, Ressourcengrenzen und Datenblöcken geprüft. Anschließend wird nach einem reproduzierbaren Decoder gesucht. Ein Feld wird erst dann als Offset oder Länge bezeichnet, wenn die Rechnung über mehrere Provider exakt aufgeht.

## Methodik und Grenzen

- Direkter Scan der vollständigen Signaturen in sieben Provider-Dateien aus `GEOWORKS.zip`.
- Die angegebenen Fundpositionen sind absolute Dateioffsets.
- Ausschließlich statische, lesende Analyse.
- Keine Änderungen an Originaldateien, `TOKEN.DB` oder `GEOS.INI`.
- Kein Laufzeittest in GeoWorks.
- Keine bestätigte Zuordnung zu CGA, HGC/MCGA oder EGA.
