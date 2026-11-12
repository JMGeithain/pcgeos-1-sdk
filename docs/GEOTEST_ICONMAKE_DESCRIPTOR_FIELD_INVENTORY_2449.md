# Untersuchung 2449 – Feldinventar der Icon-Deskriptoren 04/05/06

## Ziel

Nach der Korrektur der Zeigerhypothese aus 2447/2448 werden die Deskriptoren nicht länger als bereits verstandene Pointerstrukturen behandelt. Diese Untersuchung hält zunächst nur ihre Bytefelder, Positionen und Unterschiede fest.

Untersuchte Dateien:
- `GTI1FFFE.000`
- `GTI2FFFD.000`
- Originale `GDOC.000` und `PAPR.000` aus `GEOWORKS.zip`

## 1. Deskriptorpositionen

| Datei | Typ 04 | Typ 05 | Typ 06 |
|---|---:|---:|---:|
| GTI1FFFE.000 | 0x3F0 | 0x494 | 0x598 |
| GDOC.000 | 0x3F0 | 0x494 | 0x598 |
| GTI2FFFD.000 | 0x3F0 | 0x494 | 0x5A8 |
| PAPR.000 | 0x3F0 | 0x494 | 0x5A8 |

Jeder erkannte Deskriptor beginnt mit der 4-Byte-Signatur `23 00 00 00`. Die nachfolgenden Felder werden hier relativ zum Beginn des jeweiligen Deskriptors angegeben.

## 2. Feldinventar der gemeinsamen Struktur

| Relativer Offset | Breite | Typ 04 | Typ 05 | Typ 06 | Status |
|---|---:|---|---|---|---|
| +0x00 | 4 | 23 00 00 00 | gleich | gleich | Signatur |
| +0x04 | 2 | 04 00 | 05 00 | 06 00 | Typwert |
| +0x06 | 2 | 20 00 | gleich | gleich | unbekannt |
| +0x08 | 2 | 00 C0 | gleich | gleich | unbekannt |
| +0x0A | 2 | 02 00 | gleich | gleich | unbekannt |
| +0x0C | 2 | variabel | variabel | variabel | unbekannt; kein bestätigter Pointer |
| +0x0E | 2 | 02 00 | gleich | gleich | unbekannt |
| +0x10–+0x16 | 8 | meist 00 | meist 00 | meist 00 | reserviert/unbekannt |
| +0x18–+0x22 | 12 | überwiegend 00 | überwiegend 00 | überwiegend 00 | unbekannt; teils Vorlage-spezifische Abweichung |
| +0x24 | 2 | 26 00 | gleich | gleich | unbekannt |
| +0x26 | 2 | 2A 00 | gleich | gleich | unbekannt |
| +0x28 | 2 | 04 00 | gleich | gleich | unbekannt |
| +0x2A | 2 | 00 02 | gleich | gleich | unbekannt |
| +0x2C–+0x34 | 10 | variabel | variabel | variabel | unbekannt |
| +0x36 | 2 | 30 00 | gleich | gleich | Breite 48 |
| +0x38 | 2 | 0E 00 / 1E 00 | 1E 00 | 1E 00 | Höhe 14 bzw. 30 |
| +0x3A | 2 | 01 00 / 01 11 | 01 00 | 01 11 | Rohwert; Bedeutung nicht vollständig geklärt |
| +0x3C | 2 | 00 00 | gleich | gleich | unbekannt |
| +0x3E | 2 | FD FF oder FE FF | abhängig vom Provider | abhängig vom Provider | unbekannt |

Hinweis: Die Tabelle zeigt gemeinsame Strukturmerkmale. Einzelne Felder zwischen +0x10 und +0x22 unterscheiden sich in den Originaldateien GDOC/PAPR; die vollständigen Rohbytes stehen unten.

## 3. Rohfeldvergleich – wichtige Unterschiede

### Typ 04 (CGA), Deskriptor 0x3F0

| Datei | +0x0C | +0x18 | Rohbytes +0x2C–+0x2F | Rohbytes +0x34–+0x37 | +0x36/+0x38 |
|---|---:|---:|---|---|---|
| GTI1 | 0x0094 | 0x0000 | 6C 00 61 30 | 61 00 30 00 | 48×14 |
| GDOC | 0x0094 | 0x00A0 | 6C 00 61 30 | 61 00 30 00 | 48×14 |
| GTI2 | 0x0098 | 0x0000 | 70 00 61 30 | 65 00 30 00 | 48×14 |
| PAPR | 0x0098 | 0x00A0 | 70 00 61 30 | 65 00 30 00 | 48×14 |

### Typ 05 (HGC), Deskriptor 0x494

| Datei | +0x0C | +0x18 | +0x2C/+0x2D | +0x34/+0x35 | +0x36/+0x38 |
|---|---:|---:|---|---|---|
| GTI1 | 0x00F4 | 0x0000 | CA 00 41 30 | BF 00 30 00 | 48×30 |
| GDOC | 0x00F4 | 0x0000 | CA 00 41 30 | BF 00 30 00 | 48×30 |
| GTI2 | 0x010C | 0x0000 | E1 00 41 30 | D6 00 30 00 | 48×30 |
| PAPR | 0x010C | 0x0110 | E1 00 41 30 | D6 00 30 00 | 48×30 |

### Typ 06 (EGA), Deskriptorposition 0x598 oder 0x5A8

| Datei | +0x0C | +0x18 | +0x2C/+0x2D | +0x34/+0x35 | +0x36/+0x38 |
|---|---:|---:|---|---|---|
| GTI1 | 0x0230 | 0x0000 | 06 00 46 30 | FB 00 30 00 | 48×30 |
| GDOC | 0x0230 | 0x0330 | 06 00 46 30 | FB 00 30 00 | 48×30 |
| GTI2 | 0x02F0 | 0x0000 | C8 02 46 30 | BD 02 30 00 | 48×30 |
| PAPR | 0x02F0 | 0x02F0 | C8 02 46 30 | BD 02 30 00 | 48×30 |

Die Felder +0x18 und +0x0C dürfen nicht gleichgesetzt werden. Die Tabelle zeigt, dass Originalprovider an +0x18 teils Werte tragen, während ICONMAKE-Dummys an dieser Stelle Nullen aufweisen. Auch daraus wird noch keine Semantik abgeleitet.

## 4. Korrektur und Abgrenzung der Pointer-Hypothese

Die frühere Formel `0x3B0 + WORD(+0x0C)` kann nicht allgemein als Bilddatenadresse gelten. Beim Typ 05 in GTI1 ergibt sie `0x4A4`, also eine Position innerhalb des Deskriptorblocks. Auch eine Addition des Feldwerts zum jeweiligen Deskriptoranfang ergibt keine allgemein belegte Bilddatenzuordnung.

Daher gilt:
- +0x0C ist vorerst nur ein unbekanntes 16-Bit-Feld.
- +0x18 ist ebenfalls unbekannt.
- Die Bilddatenpositionen sind mit diesen Feldern noch nicht nachgewiesen.
- Die tatsächlichen Bilddatenkodierungen bleiben offen.

## 5. Sicher bestätigte Felder

1. Signatur `23 00 00 00`.
2. Typwerte 04, 05 und 06 an +0x04.
3. Breite 48 an +0x36.
4. Höhe 14 (Typ 04) bzw. 30 (Typ 05/06) an +0x38.
5. Rohwerte an +0x0C, +0x18 und +0x3A wurden direkt aus den Dateien ausgelesen, ihre Bedeutungen sind aber nicht abschließend geklärt.

## 6. Nächster Schritt

Als nächstes wird die Struktur der Ressource ab 0x3B0 und die Bereiche um die Deskriptoren mit den Ressourcentabellen und den PCX-Extraktionen korreliert. Ziel ist, eine unabhängige Datenstruktur zu finden, bevor weitere Feldsemantik behauptet wird.

## Quellen / Reproduzierbarkeit

- Nutzerdateien: `GTI1FFFE.000`, `GTI2FFFD.000`.
- Originaldateien aus `GEOWORKS.zip`: `GEOWORKS/ICONS/GDOC.000`, `GEOWORKS/ICONS/PAPR.000`.
- PCX-Extraktionen des Nutzers: GDOC/PAPR CGA, HGC und EGA.
- Bytepositionen und Little-Endian-Werte wurden direkt aus den Dateien ausgelesen.
- Es wurde kein Laufzeittest behauptet.
