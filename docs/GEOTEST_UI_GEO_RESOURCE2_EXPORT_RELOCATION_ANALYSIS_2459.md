# GEOTEST / UI.GEO – Export- und Relokationsanalyse von Ressource 2 (Runde 2459)

## Ziel und Abgrenzung

Statische Untersuchung von UI.GEO aus GeoWorks 1.2.8 (PC/GEOS 1.x). Untersucht werden Export-Einstiegsoffsets in Ressource 2 und deren Relokationen. Kein Programm wurde ausgeführt; kein Laufzeittest. PC/GEOS 2.x und FreeGEOS sind keine Belegquellen dieser Runde.

## Quelldateien und Integrität

Die Dateien wurden erneut direkt aus GEOWORKS.zip extrahiert:

| Datei | Archivpfad | Größe | SHA-256 |
|---|---|---:|---|
| UI.GEO | GEOWORKS/SYSTEM/UI.GEO | 87.900 | 13a3a82ec3d4373b120890a11eb09b3a9f9ec456ca633819728f53c07883c73a |
| ICON-ED.GEO | GEOWORKS/WORLD/ICON-ED.GEO | 47.648 | afbbd1d8115c82162e8d3c9331c5d945e073e0823852bb5c68055ba6148df064 |

Beide Hashwerte stimmen mit den in Runde 2457 dokumentierten Werten überein.

## UI.GEO – Exporttabelle und Ressource 2

Der PC/GEOS-1.x-Headerparser lokalisiert die Exporttabelle bei Dateioffset 0x13C und die Ressourcentabelle bei 0x554. Ressource 2 hat Dateioffset 0x23D0, Größe 7.008 Bytes (0x1B60), 980 Relokationsbytes (= 245 Einträge) und den Flags-Rohwert 0x0A80.

Die Exporttabelle enthält 262 Einträge; 130 davon verweisen auf Ressource 2. Alle 130 ressourcenrelativen Exportoffsets sind verschieden. Der kleinste Wert ist 0x0010, der größte 0x1B34.

Die ersten 60 sortierten Offsets:

~~~text
0010 0011 0012 0013 0037 0047 0055 0063 007E 008B
009A 00E5 00FD 0116 0126 0135 01AF 0204 0210 021D
0229 0236 0245 0255 0264 0272 0283 03AE 0693 06C3
0753 0784 0854 0855 089F 08E2 0A03 0A58 0A6F 0A8F
0AA8 0CE4 0CF2 0D0A 0D0B 0D0C 0D0D 0D0E 0D0F 0D4C
0D7F 0D88 0D91 0DDA 0E00 0E3C 0EB6 0EBF 0EC8 1022
~~~

Große Abstände zwischen benachbarten Exportoffsets sind beispielsweise 0x03AE→0x0693 (741 Bytes), 0x0AA8→0x0CE4 (572), 0x0EC8→0x1022 (346) und 0x0283→0x03AE (299). Dies zeigt getrennte Exportcluster, aber keine gesicherten Funktionsgrenzen oder Funktionsnamen. Die Offsets 0x0010–0x0013 dürfen ohne Disassemblierung nicht als Funktionen klassifiziert werden.

## Relokationen in Ressource 2

Die 245 Relokationseinträge verteilen sich auf Klasse 0: 120, Klasse 1: 93 und Klasse 2: 32.

Bei Klasse 1 enthält das Zusatzbyte den Importindex:

| Importindex | Rohname | Anzahl |
|---:|---|---:|
| 0 | im | 8 |
| 1 | dbase | 85 |

Die 85 Verweise auf dbase haben Relokationstyp 4. Die acht Verweise auf im umfassen sechs Typ-4-, einen Typ-1- und einen Typ-2-Eintrag.

Die Zielwortwerte der 85 dbase-Relokationen umfassen die verschiedenen Ordinalwerte 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 16, 17, 18, 19 und 20. Für im treten 7, 15, 21 und 23 auf. Ohne die Exporttabellen der Importbibliotheken und eine gesicherte ABI-Zuordnung werden diese Werte nicht mit symbolischen Funktionsnamen versehen.

## Zusammenhang mit Ressource 1 und 3

| Ressource | Dateioffset | Größe | Relokationsbytes | Einträge |
|---|---:|---:|---:|---:|
| R1 | 0x066C | 4.928 | 2.596 | 649 |
| R2 | 0x23D0 | 7.008 | 980 | 245 |
| R3 | 0x4304 | 3.824 | 572 | 143 |

R1 enthält TOKEN.DB bei ressourcenrelativem Offset 0x0C50 (Dateioffset 0x12BC). R3 enthält Token DB bei ressourcenrelativem Offset 0x0361 (Dateioffset 0x4665), im Textumfeld von Specific UI, Clipboard, Screens und Screen Blanker.

Dies belegt Token-DB-Referenzen in UI.GEO. Es beweist nicht, dass R2 den Icon-Bitmap-Decoder enthält. Export- und Relokationsverteilung allein reichen für eine solche Funktionszuweisung nicht aus.

## ICON-ED.GEO – Importdeklaration

ICON-ED.GEO besitzt einen Import für ui mit Protokollrohwert 693. Das ist mit einer UI-abhängigen Anwendung vereinbar, benennt aber keine einzelne UI-Funktion. Für die Zuordnung der von ICON-ED.GEO verwendeten UI-Ordinalwerte zu den UI-Exporten ist eine gesonderte Relokationsanalyse aller ICON-ED-Ressourcen erforderlich.

## Schlussfolgerungen

**Gesichert:**
1. R2 von UI.GEO enthält 130 der 262 Exporte.
2. R2 hat 245 Relokationseinträge; 93 gehören zur Importklasse 1.
3. Davon adressieren 85 Importindex 1 (dbase) und acht Importindex 0 (im).
4. UI.GEO enthält Token-DB-Strings in R1 und R3.
5. Die erneut extrahierten Dateien stimmen bytegenau mit den zuvor dokumentierten Hashwerten überein.

**Nicht gesichert:** konkrete Namen/Aufgaben der 130 Exportpunkte; ob R2 den Icon-Decoder enthält; welche UI-Exporte ICON-ED.GEO tatsächlich aufruft; die vollständige Bedeutung aller Relokationstypen und Ressourcenflags.

## Nächster Schritt – Runde 2460

ICON-ED.GEO vollständig nach Import-Relokationen zur Bibliothek ui durchsuchen. Für jeden Treffer Ressource, Offset, Relokationstyp und Zielordinal dokumentieren. Anschließend die verwendeten UI-Ordinalwerte mit den 262 Exporttabelleneinträgen in UI.GEO abgleichen. Erst dann gezielt die korrespondierenden UI-Routinen disassemblieren.

Arbeitsregel: Originaldateien unverändert lassen. Keine Funktionsnamen aus bloßen Zahlenmustern ableiten. Keine Laufzeitbeobachtung behaupten, solange kein Test ausgeführt wurde.
