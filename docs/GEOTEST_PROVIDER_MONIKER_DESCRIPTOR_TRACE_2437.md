# Untersuchung 2437 – Verfolgung der eingebetteten Moniker-Deskriptoren

## Anlass

Die Rohdaten wurden erneut direkt aus den sieben Provider-Geodes gelesen. Dabei wurde die Lage der Deskriptoren innerhalb der durch die äußere Offsettabelle begrenzten Ressource genauer geprüft. Wichtig ist die Unterscheidung zwischen:

- äußeren Ressourcenoffsets aus der Geode-Offsettabelle;
- inneren Deskriptoren, die innerhalb einer Ressource liegen.

Die inneren Deskriptoren sind keine zusätzlichen Einträge der äußeren Offsettabelle.

## Äußere Ressourcenpositionen

Für GDOC, PAPR, BEER, BILL, BUTN, ZIPR und GEXE liegt der vierte unterschiedliche Zieloffset bei `0x4F4`. Der vorhergehende Bereich `0x3B0–0x4F3` enthält daher die untersuchten inneren Strukturen.

Die äußere Offsettabelle weist außerdem auf den nächsten Bereich bei:

- GDOC, BEER: `0x598`
- PAPR, BUTN, ZIPR: `0x598`
- BILL, GEXE: `0x588`

## Innerer Deskriptor 04

Alle sieben Dateien enthalten bei `0x3F0` das Präfix:

```
23 00 00 00 04 00 20 00 00 C0 02 00
```

Danach folgen wiederholte 16-Bit-Werte und weitere strukturierte Felder. Die Werte bei `0x3FC` und `0x408` sind nicht als Breite oder Höhe bestätigt. Auch die Folge `26 00 2A 00` und die späteren Wörter dürfen ohne Formatdefinition nicht semantisch benannt werden.

## Innerer Deskriptor 05

Ein zweiter Deskriptor mit dem Präfix

```
23 00 00 00 05 00 20 00 00 C0 02 00
```

liegt innerhalb derselben äußeren Ressource, aber nicht immer an derselben Position:

- GDOC, PAPR, BEER, BUTN, ZIPR: `0x494`
- BILL, GEXE: `0x484`

Nach dem Präfix folgen unter anderem diese 16-Bit-Werte:

| Datei | erstes Wort nach Präfix |
|---|---:|
| GDOC | `0x00F4` |
| PAPR | `0x010C` |
| BEER | `0x00F4` |
| BILL | `0x00EC` |
| BUTN | `0x0108` |
| ZIPR | `0x010C` |
| GEXE | `0x00F4` |

Diese Werte sind weiterhin nur rohe Feldwerte. Die Lage des zweiten Deskriptors zeigt, dass die innere Struktur variabel lang ist und nicht über einen global festen Offset gefunden werden darf.

## Äußerer Bereich ab 0x598 beziehungsweise 0x588

Am Beginn des nächsten äußeren Bereichs liegt ein weiterer Deskriptor mit dem Präfix:

```
23 00 00 00 06 00 20 00 00 C0 02 00
```

Beispiele:

- GDOC bei `0x598`: `23 00 00 00 06 00 20 00 00 C0 02 00 30 03 02 00 ...`
- PAPR bei `0x598`: der Deskriptor beginnt erst 16 Byte nach dem Bereichsanfang; davor liegen weitere Bytes.
- BILL bei `0x588`: am Bereichsanfang liegen zunächst Nullbytes; der Deskriptor ist nicht am Anfang sichtbar.
- GEXE bei `0x588`: der Deskriptor beginnt am Bereichsanfang.

Damit ist ein dritter innerer Datensatz mit Kennwert `06 00` nachgewiesen. Er ist in den Dateien nicht durchgehend am Beginn des äußeren Bereichs ausgerichtet.

## Konsequenz für die bisherige Interpretation

Die Muster `23 00 00 00 04 00`, `23 00 00 00 05 00` und `23 00 00 00 06 00` treten als wiederkehrende Kennungen in inneren Strukturen auf. Das legt drei zusammengehörige Datensätze nahe. Es beweist jedoch nicht, dass diese unmittelbar CGA, HGC/MCGA und EGA repräsentieren.

Die inneren Datensätze müssen als strukturierte Moniker-/Provider-Metadatenkandidaten behandelt werden. Die Bedeutung des Präfixes `23 00 00 00`, des 16-Bit-Kennwerts 04/05/06 und der folgenden Wörter bleibt offen.

## Korrektur zur Untersuchung 2436

Die dort dokumentierten Werte bei `0x3FC`, `0x408` und den nachfolgenden Feldern sind Rohwerte innerhalb des Deskriptors 04. Sie dürfen nicht als Maße oder Längen interpretiert werden. Die zweite Struktur bei `0x484`/ `0x494` ist ein innerer Datensatz innerhalb der äußeren Ressource `0x3B0–0x4F3`, nicht ein zusätzlicher äußerer Ressourcenoffset.

## Nächster Schritt

Die drei Datensatztypen 04, 05 und 06 werden nun in mehreren Providern als vollständige Bytebereiche extrahiert und gegeneinander ausgerichtet. Gesucht werden:

1. konstante Feldpositionen relativ zum jeweiligen Deskriptor;
2. Werte, die mit nachfolgenden Datenlängen oder Offsets rechnerisch übereinstimmen;
3. gemeinsame Strukturmuster, die in allen Providern erhalten bleiben;
4. ein reproduzierbarer Decoder, der die ICONMAKE-Sollprofile 48×14 und 48×30 tatsächlich erzeugt.

## Methodik und Grenzen

- Direkter Bytezugriff auf die Originaldateien im Archiv `GEOWORKS.zip`.
- Ausschließlich statische, lesende Analyse.
- Keine Änderungen an Provider-Dateien, `TOKEN.DB` oder `GEOS.INI`.
- Kein Laufzeittest in GeoWorks.
- Keine bestätigte Zuordnung der Datensatztypen 04/05/06 zu CGA, HGC/MCGA oder EGA.
