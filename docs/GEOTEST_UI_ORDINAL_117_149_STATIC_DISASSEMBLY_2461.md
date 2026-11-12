# GEOTEST – Statische Disassemblierung der UI-Aufrufziele 117 und 149 (Runde 2461)

## Methodik und Grenzen

Die Analyse verwendet die originalen PC/GEOS-1.x-Dateien UI.GEO und ICON-ED.GEO aus GEOWORKS.zip. Die Hashwerte wurden erneut geprüft. Für die Intel-16-Bit-Instruktionssicht wurde GNU objdump auf isolierten Ressourcenbytes im i8086-Modus eingesetzt. Die Bytes wurden nicht verändert. Die Disassemblierung ist eine statische Interpretation der Bytefolgen; es gab keinen Laufzeittest.

UI.GEO SHA-256: 13a3a82ec3d4373b120890a11eb09b3a9f9ec456ca633819728f53c07883c73a
ICON-ED.GEO SHA-256: afbbd1d8115c82162e8d3c9331c5d945e073e0823852bb5c68055ba6148df064

## Ausgangspunkt aus Runde 2460

ICON-ED.GEO besitzt zwei Relokationseinträge vom Typ 4, die auf UI-Ordinal 149 und UI-Ordinal 117 zeigen. In beiden Fällen liegt am Aufrufort Opcode 0x9A (CALL FAR). Die UI-Exporttabelle ordnet die Ordinale zu:

| UI-Ordinal | Ressource | Exportoffset | Dateioffset |
|---:|---:|---:|---:|
| 117 | R2 | 0x0784 | 0x2B54 |
| 149 | R7 | 0x0E45 | 0x852D |

## UI-Ordinal 117 – R2 + 0x0784

Die ersten Bytes ergeben folgenden Einstieg:

~~~asm
0784  push ax
0785  push bx
0786  push cx
0787  push dx
0788  push bp
0789  push ds
078A  push si
078B  push es
078C  push di
078D  push cs
078E  call 0693
0791  jae  0796
0793  jmp  084A
0796  mov  di,bx
0798  call far 0000:0011   ; relocierter UI-Import
079D  push bx
079E  mov  bx,di
07A0  mov  di,ax
07A2  call far 0000:0013   ; relocierter UI-Import
~~~

Im weiteren Verlauf ruft die Routine zahlreiche über Klasse-1-Relokationen gebundene Funktionen aus Importindex 1 (dbase) auf. Die relevanten Relokationsziele innerhalb des Funktionsbereichs R2+0x0784 bis R2+0x0853 sind:

| Offset | Importordinal (Rohwert) |
|---:|---:|
| 0x0799 | 0x11 |
| 0x07A3 | 0x13 |
| 0x07B4 | 0x0D |
| 0x07B9 | 0x05 |
| 0x07E5 | 0x04 |
| 0x07EE | 0x0C |
| 0x07F3 | 0x07 |
| 0x07FE | 0x03 |
| 0x0803 | 0x05 |
| 0x081B | 0x08 |
| 0x0827 | 0x04 |
| 0x082E | 0x08 |
| 0x0833 | 0x01 |
| 0x083D | 0x12 |
| 0x0845 | 0x10 |

Die Routine enthält unter anderem ES-basierte Speicherzugriffe, Segmentregisterwechsel, eine REP MOVSB-Kopie und Schleifen über WORD-Werte. Sie kehrt bei Offset 0x0853 mit RETF zurück. Der Code ist somit deutlich mehr als ein einzelner Wrapper: er sichert Register, ruft Datenbankfunktionen auf und bearbeitet einen Speicherblock bzw. strukturierte Einträge.

**Interpretationsgrenze:** Das Muster ist mit einer Daten-/Objektverarbeitung vereinbar. Die konkrete Funktion (z.B. Moniker, Icon, Token oder andere UI-Daten) ist nicht bewiesen. Die Ordinalnamen der importierten dbase-Funktionen sind ebenfalls nicht bekannt.

## UI-Ordinal 149 – R7 + 0x0E45

Der Beginn der Routine lautet:

~~~asm
0E45  push cx
0E46  push dx
0E47  push bx
0E48  push bp
0E49  push si
0E4A  push di
0E4B  push bx
0E4C  push si
0E4D  push cx
0E4E  push dx
0E4F  push di
0E50  push bp
0E51  push ax
0E52  mov  bp,sp
0E54  call far 0000:0095   ; lokaler relocierter Aufruf
0E59  mov  cx,bx
0E5B  mov  dx,000Eh
0E5E  mov  ax,441Dh
0E61  call far 0000:0099   ; lokaler relocierter Aufruf
0E66  mov  di,0A000h
0E69  call far 0000:00A9   ; lokaler relocierter Aufruf
~~~

Weitere Instruktionen verwenden unter anderem die Konstanten 0x41BF, 0x41A2, 0x8000 und 0x0D sowie Aufrufe mit Zielwortwerten 0xA9 und 0x99. In der UI.GEO-Relokationstabelle sind die Far-Aufrufoperanden innerhalb des untersuchten Abschnitts als Klasse 0 / Typ 0 erfasst. Diese Relokationen sind keine ICON-ED-Importverweise; sie gehören zum lokalen Relokations-/Adressierungsbereich des Geodes. Eine genauere semantische Benennung der Ziele wird nicht vorgenommen.

Der Kontrollfluss enthält mehrere bedingte Verzweigungen und lokale Unterprogrammaufrufe. Die sichtbare Routine endet bei Offset 0x0ECB mit RETF. Der anschließende Code ab 0x0ECC ist ein weiterer Kontrollflussbereich und wurde nicht in die Routinegrenze 0x0E45–0x0ECB einbezogen.

Die Verwendung des unmittelbaren Wertes 0xA000 als Segment-/Adresswert und die Konstanten 0x8000, 0x41BF und 0x41A2 sind auffällig. Sie können auf einen hardwarenahen Speicher- oder Grafikpfad hindeuten, sind allein aber kein ausreichender Beleg für eine konkrete Grafikfunktion oder einen Icon-Decoder.

## Vergleich der beiden Routinen

| Merkmal | Ordinal 117 | Ordinal 149 |
|---|---|---|
| Ressource | R2 | R7 |
| Exportoffset | 0x0784 | 0x0E45 |
| Importrelokationen im Funktionsbereich | 15 Klasse-1/Typ-4-Verweise auf dbase | keine Klasse-1-Verweise im betrachteten Bereich |
| Sichtbare Struktur | Segment-/Speicheroperationen, REP MOVSB, Schleife, Datenbankaufrufe | lokale Far-Aufrufe, bedingte Verzweigungen, Konstanten 0xA000/0x8000 |
| Ende | RETF bei 0x0853 | RETF bei 0x0ECB |
| Semantik | offen | offen; hardware-/speichernahe Indizien, nicht bewiesen |

## Ergebnis

1. Beide ICON-ED-Aufrufziele sind echte exportierte Einstiegspunkte in UI.GEO.
2. UI-Ordinal 117 ist stark mit dbase-Aufrufen und strukturierter Speicherbearbeitung verbunden. Das ist ein belastbarer Datenbank-/Datenverarbeitungsbefund, aber noch kein Nachweis einer Icon-Funktion.
3. UI-Ordinal 149 enthält lokale Far-Aufrufe und auffällige Speicher-/Segmentkonstanten. Ein Grafikpfad ist denkbar, aber mit den vorliegenden Bytes nicht bewiesen.
4. Die zwei Routinen unterscheiden sich deutlich; es ist nicht gerechtfertigt, beide als Icon-Decoder zu bezeichnen.
5. Die konkreten symbolischen Namen und ABI-Verträge sind weiterhin unbekannt.

## Nächster Schritt – Runde 2462

Die internen Far-Aufrufziele in UI-Ordinal 149 (R7 + 0x0E45) werden über die Relokationstabelle auf ihre tatsächlichen Ressourcen-/Segmentziele zurückgeführt. Anschließend werden die lokalen Ziele 0x95, 0x99 und 0xA9 in ihrem jeweiligen Ressourcenkontext untersucht. Parallel werden die dbase-Ordinalwerte aus UI-Ordinal 117 mit dem dbase-Geode-Exportbestand abgeglichen, sofern die originale dbase-Datei in der Installation vorhanden ist.

Arbeitsregel: Keine Funktionsnamen aus Konstanten oder Opcode-Mustern ableiten. Keine Laufzeitbeobachtung behaupten. Originaldateien unverändert lassen.
