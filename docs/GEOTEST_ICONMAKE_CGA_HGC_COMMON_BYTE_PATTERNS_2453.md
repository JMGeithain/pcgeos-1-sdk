# GEOTEST / ICONMAKE – CGA/HGC-Vergleich gemeinsamer Bytefolgen (Untersuchung 2453)

Stand: 12.11.2026  
Repository: `JMGeithain/pcgeos-1-sdk`

## Ziel

Die bereits abgegrenzten CGA- und HGC-Nachfolgebereiche der Originalprovider GDOC.000 und PAPR.000 werden auf identische Bytefolgen untersucht. Besonderes Augenmerk liegt auf der Folge `FD FF 00`, die in beiden Auflösungsbereichen bereits aufgefallen war.

## Untersuchte Bereiche

| Provider | Bereich | Länge |
|---|---|---:|
| GDOC CGA | `0x430–0x493` (Ende exklusiv `0x494`) | 100 Bytes |
| GDOC HGC | `0x4D4–0x597` (Ende exklusiv `0x598`) | 196 Bytes |
| PAPR CGA | `0x430–0x493` (Ende exklusiv `0x494`) | 100 Bytes |
| PAPR HGC | `0x4D4–0x5A7` (Ende exklusiv `0x5A8`) | 212 Bytes |

Die Bereiche wurden aus den Descriptor-Grenzen abgeleitet. Ihre Interpretation als Grafikdatenbereich ist eine Arbeitsannahme; die konkrete interne Kodierung ist nicht dekodiert.

## Treffer der Bytefolge FD FF 00

Es wurden alle Vorkommen der exakten dreibyteigen Folge `FD FF 00` in den jeweiligen Bereichen gesucht. Die folgenden Positionen sind absolute Datei-Offsets und bezeichnen jeweils das erste Byte `FD`.

| Original-Provider | CGA-Fundstellen | Anzahl | HGC-Fundstellen | Anzahl |
|---|---|---:|---|---:|
| GDOC | `0x434, 0x479, 0x47F` | 3 | `0x4D8, 0x4DE, 0x577, 0x57D, 0x583` | 5 |
| PAPR | `0x449, 0x487` | 2 | `0x59C` | 1 |

Die Sequenz kommt somit in allen vier untersuchten Bereichen vor. Ihre Häufigkeit ist nicht proportional zur Bereichslänge und unterscheidet sich auch zwischen den beiden Providern.

## Bytevergleich CGA gegen HGC

Für jede Providerfamilie wurden gemeinsame zusammenhängende Bytefolgen verschiedener Länge gesucht. Neben `FD FF` und `FD FF 00` gibt es kurze gemeinsame Folgen, darunter Nullbytefolgen. Bei GDOC treten außerdem gemeinsame Fragmente wie `00 03 FD FF` auf. Bei PAPR beschränken sich die längeren gemeinsamen Fragmente in diesem einfachen exakten Vergleich weitgehend auf kurze Sequenzen; längere gemeinsame Folgen werden durch die stark unterschiedlichen Grafikdaten nicht sichtbar.

Diese Schnittmengen sind zunächst nur statistische/exakte Byteüberschneidungen. Kurze Sequenzen wie `00 00` sind wenig aussagekräftig und können zufällig auftreten.

## Was daraus folgt – und was nicht

**Gesichert:**
1. `FD FF 00` kommt in allen vier untersuchten Originalbereichen vor.
2. Die absoluten Fundstellen und Anzahlen sind in der Tabelle dokumentiert.
3. Die Sequenz ist kein ausschließliches Merkmal des CGA- oder HGC-Bereichs.
4. Die beiden Providerfamilien zeigen unterschiedliche Verteilungen.

**Nicht gesichert:**
- dass `FD FF 00` ein Steuerkommando, Escape-Code, Zeilenabschluss oder Wiederholungsmarker ist;
- dass CGA und HGC denselben vollständigen Kompressionsalgorithmus verwenden;
- dass die Bytes direkt Pixel, Zeilen oder Lauflängen beschreiben.

Aus den vier Beispielen allein kann keine Semantik der Sequenz abgeleitet werden.

## Nächster Untersuchungsschritt

Als nächstes sollte die Suche von bloßen Byteüberschneidungen auf die ausführbare Verarbeitung verlagert werden: In den GeoWorks-1.x-Dateien und den ICONMAKE-Unterlagen nach Routinen suchen, die Provider-Descriptoren bzw. Icon-Daten lesen und interpretieren. Dabei sind nur belegbare Querverweise und Disassemblierungsbefunde als Formatnachweis zu akzeptieren. Die Folge `FD FF 00` ist ein Suchmuster, keine vorweggenommene Dekodierung.
