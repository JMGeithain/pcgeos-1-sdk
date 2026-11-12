# Korrektur zu Untersuchung 2447 – Feld +0x0C ist kein bestätigter Bilddatenzeiger

## Anlass

Die in Untersuchung 2447 angenommene Formel

`Dateiposition = 0x3B0 + WORD(Deskriptor + 0x0C)`

wurde in Untersuchung 2448 anhand der tatsächlichen Deskriptorgrenzen überprüft. Dabei zeigte sich ein Widerspruch. Die Formel darf nicht als entschlüsselte Zeigerberechnung verwendet werden.

## Konkreter Gegenbeweis

In `GTI1FFFE.000` beginnt der HGC-Deskriptor bei `0x494`. Sein Feld `+0x0C` enthält `0x00F4`.

Die bisherige Formel liefert:

`0x3B0 + 0x00F4 = 0x4A4`

`0x4A4` liegt jedoch innerhalb des HGC-Deskriptors, denn es ist `0x494 + 0x10`. Es ist damit kein eigenständiger Beginn eines Bilddatenblocks. Der gleiche methodische Fehler betrifft die daraus abgeleiteten Aussagen über CGA/HGC/EGA-Payloadlängen.

## Status der früheren Aussagen

Folgende Aussagen aus 2447 werden zurückgenommen und sind nicht als Befund zu verwenden:

- +0x0C sei ein direkter relativer Dateizeiger mit Basis 0x3B0.
- Die berechneten Ziele seien die tatsächlichen Bilddatenanfänge.
- Die Bereiche von 84 bzw. 180 Byte seien dadurch als Bilddaten identifiziert.
- Die abgeleiteten Restlängen der EGA-Daten belegten ein komprimiertes Format.

Die Rechnungen waren arithmetisch korrekt, aber die angenommene Semantik und Bezugsbasis waren nicht belegt und widersprechen im HGC-Fall den Deskriptorgrenzen.

## Was bleibt gültig?

- Die Rohwerte des Feldes +0x0C wurden in den untersuchten Dateien korrekt abgelesen.
- Die Größenangaben der Iconvarianten 48×14 und 48×30 wurden separat aus den Deskriptoren ermittelt und mit den PCX-Dateien abgeglichen.
- Der tatsächliche Speicherort und die Kodierung der Bilddaten bleiben offen.

## Nächster Schritt

Die Bedeutung von +0x0C muss unabhängig neu bestimmt werden. Dazu sind die vollständigen Deskriptorfelder, Ressourcengrenzen und Referenzen innerhalb des Providerformats gemeinsam zu untersuchen. Bis dahin wird +0x0C nur als unbekanntes 16-Bit-Feld geführt.

