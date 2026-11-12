# Untersuchung 2451 – CGA-Datenbereich: Byteinventar und Vergleich

## Ziel

Der 100-Byte-Bereich direkt hinter dem CGA-Deskriptor wurde in den vier Providerdateien untersucht. Die PCX-Dateien GDOC_CGA und PAPR_CGA wurden mit Pillow dekodiert und als einfache 1-Bit-Zeilenmatrizen (6 Bytes je Zeile, MSB zuerst) gepackt. Diese Rohdarstellungen wurden gegen den Providerbereich geprüft.

## 1. Exakte Bereiche und Prüfsummen

CGA-Deskriptor: `0x3F0–0x42F` (64 Byte).
Unmittelbar folgender Bereich: `0x430–0x493` (100 Byte, Endadresse inklusive).

| Datei | SHA-256 des 100-Byte-Bereichs |
|---|---|
| GTI1FFFE.000 | `c29a256a40f75ad22d930d27581a49386efd294b9c7963d22203a54f343471e0` |
| GDOC.000 | `c29a256a40f75ad22d930d27581a49386efd294b9c7963d22203a54f343471e0` |
| GTI2FFFD.000 | `791f9b6ab4e2ba1078c7a6855215fccf140b5a0b754b854bb444fea454b9b537` |
| PAPR.000 | `791f9b6ab4e2ba1078c7a6855215fccf140b5a0b754b854bb444fea454b9b537` |

GTI1 und GDOC sind in diesem gesamten 100-Byte-Bereich identisch. GTI2 und PAPR sind ebenfalls vollständig identisch.

## 2. Strukturbeobachtung am GDOC-CGA-Bereich

Die ersten 16 Bytes lauten:

`00 01 00 0F FD FF 00 C1 00 1E FE 00 01 01 E1 05`

Danach folgt ein wiederkehrendes Muster, unter anderem:

`E1 05 1C 38 CC 33 00`

Die Folge wiederholt sich mit Variationen an bestimmten Positionen. Gegen Ende folgen weitere Steuer-/Datenbytes und 13 abschließende Nullbytes.

Das ist ein beobachtetes Byteinventar. Die Bytes werden hier ausdrücklich nicht als bekannte RLE-Kommandos oder als Zeilenmarker bezeichnet, da deren Semantik noch nicht nachgewiesen ist.

## 3. Vergleich mit dem dekodierten PCX-Bild

Die PCX-Datei GDOC_CGA hat:
- 48 × 14 Pixel
- eine 1-Bit-Ebene
- 6 Bytes pro Zeile bei dekodierter, ungepackter Zeilenmatrix

Die so erzeugte 84-Byte-Rohmatrix wurde in drei einfachen Varianten geprüft:
1. Bits innerhalb jedes Bytes MSB-zuerst.
2. Bits innerhalb jedes Bytes LSB-zuerst.
3. Invertierte Pixelpolarität.

Keine der drei Varianten kommt als zusammenhängende Bytefolge im 100-Byte-Providerbereich oder in der vollständigen Providerdatei vor. Derselbe Test wurde für PAPR_CGA durchgeführt und ergab ebenfalls keinen direkten Treffer.

Das beweist nicht, dass die Daten nicht das Bild enthalten. Es schließt nur diese einfachen direkten Rohdarstellungen aus. Eine abweichende Packung, Steuerinformationen, zeilenweise Kodierung oder ein anderes Format bleiben möglich und sind noch nicht voneinander unterschieden.

## 4. Was ist belastbar?

**Bestätigt:**
- Der CGA-Bereich umfasst 100 Byte und beginnt unmittelbar bei 0x430.
- Die beiden ICONMAKE-Dummys übernehmen den vollständigen CGA-Bereich byteidentisch aus ihrer jeweiligen Originalvorlage.
- GDOC-CGA und PAPR-CGA unterscheiden sich deutlich voneinander.
- Die einfache 84-Byte-Rohmatrix aus dem PCX ist nicht direkt als zusammenhängende Bytefolge im Providerbereich enthalten.

**Nicht bestätigt:**
- RLE oder eine bestimmte Kompressionsart.
- Eine konkrete Bedeutung der Bytes FD, FE oder E1.
- Zeilenanfänge oder Zeilenlängen.
- Eine bestimmte Pixelbitreihenfolge im nativen Providerformat.

## 5. Nächster Schritt

Als nächstes werden die wiederkehrenden Bytefolgen und möglichen Zeilengruppen systematisch gegen die dekodierten 14 PCX-Zeilen verglichen. Dabei werden keine Steuerbyte-Bedeutungen vorweggenommen. Wenn keine eindeutige Zuordnung entsteht, wird HGC als zweites monochromes Profil herangezogen, um gemeinsame Muster zu identifizieren.

## Quellen und Reproduzierbarkeit

- Originale aus `GEOWORKS.zip`: `GEOWORKS/ICONS/GDOC.000`, `GEOWORKS/ICONS/PAPR.000`.
- Nutzerdateien: `GTI1FFFE.000`, `GTI2FFFD.000`.
- Nutzer-PCX-Dateien: `GDOC_CGA(1).PCX`, `PAPR_CGA(1).PCX`.
- PCX-Maße und -Ebenen wurden aus den Dateien gelesen und die Bilder mit Pillow dekodiert.
- Die 84-Byte-Rohmatrizen wurden zeilenweise aus 48 Pixeln gebildet, 6 Bytes je Zeile; MSB-/LSB-Varianten und Polaritätsinversion wurden getestet.
- Prüfsummen und Bytevergleiche wurden direkt auf den vollständigen Dateien berechnet.
- Kein GeoWorks-Laufzeittest wurde durchgeführt oder behauptet.
