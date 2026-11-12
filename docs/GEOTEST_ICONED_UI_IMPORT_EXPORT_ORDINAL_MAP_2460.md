# GEOTEST – ICON-ED.GEO UI-Import- und Exportordinal-Abgleich (Runde 2460)

## Ziel

Statische Untersuchung von ICON-ED.GEO aus der GeoWorks-1.2.8-Installation. Die Relokationen zum importierten Modul `ui` werden mit der UI.GEO-Exporttabelle abgeglichen. PC/GEOS 2.x und FreeGEOS werden nicht als Belege verwendet. Es wurde kein Laufzeittest ausgeführt.

## Quellen und Integrität

Beide Dateien wurden direkt aus GEOWORKS.zip extrahiert:

| Datei | Größe | SHA-256 |
|---|---:|---|
| ICON-ED.GEO | 47.648 | afbbd1d8115c82162e8d3c9331c5d945e073e0823852bb5c68055ba6148df064 |
| UI.GEO | 87.900 | 13a3a82ec3d4373b120890a11eb09b3a9f9ec456ca633819728f53c07883c73a |

## ICON-ED.GEO – Import- und Relokationsbestand

ICON-ED.GEO besitzt 11 Ressourcen, eine Importdeklaration und 124 Relokationseinträge. Der einzige Import lautet `ui`; die im Header gespeicherten Protokollwörter sind 693 und 0.

Genau sechs Relokationseinträge haben Relokationsklasse 1 und Importindex 0 (`ui`). Alle sechs befinden sich in R1 oder R2:

| ICON-ED-Ressource | Offset innerhalb der Ressource | Relokationstyp | Zielordinal in UI |
|---:|---:|---:|---:|
| R1 | 0x0040 | 1 | 0 |
| R1 | 0x0042 | 2 | 0 |
| R1 | 0x0130 | 1 | 97 |
| R1 | 0x0132 | 2 | 97 |
| R2 | 0x156E | 4 | 149 |
| R2 | 0x161E | 4 | 117 |

Die ersten vier Einträge liegen paarweise im Datenbereich von R1. Die letzten beiden Einträge sind Typ-4-Relokationen in R2. An beiden Zielstellen steht im Rohdatenstrom der Opcode 0x9A, gefolgt vom zugehörigen vier Byte umfassenden Far-Aufrufoperand. Dies ist ein direkter statischer Hinweis, dass die beiden Typ-4-Relokationen CALL-FAR-Aufrufstellen betreffen. Die genaue Bedeutung der Typen 1 und 2 wird hier nicht weiter interpretiert.

## Abgleich mit UI.GEO-Exporttabelle

Die Exporttabelle von UI.GEO hat 262 Einträge. Die vier in ICON-ED.GEO verwendeten Zielordinalwerte lassen sich unmittelbar zuordnen:

| UI-Ordinal | UI-Ressource | Ressource-relativer Exportoffset | UI-Ressourcen-Dateioffset | Einordnung |
|---:|---:|---:|---:|---|
| 0 | R1 | 0x08E0 | 0x0F4C | Exportziel in R1 |
| 97 | R1 | 0x0836 | 0x0EA2 | Exportziel in R1 |
| 117 | R2 | 0x0784 | 0x2B54 | Exportziel in R2 |
| 149 | R7 | 0x0E45 | 0x852D | Exportziel in R7 |

Für Ordinal 117 zeigt die Bytefolge ab dem Exportziel einen plausiblen 16-Bit-Code-Einstieg mit Register-Sicherungen und weiteren Aufrufen. Für Ordinal 149 zeigt die Bytefolge ebenfalls einen Code-Einstieg mit Register-Sicherungen und einem Far-Aufruf. Die jeweiligen ICON-ED-Aufrufstellen sind durch 0x9A-Opcode und Relokationseintrag belegt.

Die Exportziele 0 und 97 liegen in R1. Die ICON-ED-Relokationen dazu sind zwei Paare vom Typ 1 und 2, keine Typ-4-Aufrufstellen. Das spricht gegen die vorschnelle Gleichsetzung dieser beiden Ordinalwerte mit direkt aufgerufenen Codefunktionen. Ihre genaue ABI-Bedeutung ist mit den vorliegenden Bytes allein nicht gesichert.

## Ergebnis

**Direkt nachgewiesen:**

1. ICON-ED.GEO importiert `ui`.
2. ICON-ED.GEO enthält sechs UI-bezogene Importrelokationen.
3. Die beiden UI-Zielordinalwerte 117 und 149 werden in R2 über Far-Aufrufstellen (Opcode 0x9A) referenziert.
4. UI-Ordinal 117 zeigt auf UI.GEO R2 + 0x0784.
5. UI-Ordinal 149 zeigt auf UI.GEO R7 + 0x0E45.
6. Die Ordinalwerte 0 und 97 sind in ICON-ED.GEO als Paare von Relokationstyp 1 und 2 im Datenbereich von R1 vertreten; sie sind nicht als direkte Far-Aufrufe nachgewiesen.

**Noch offen:**

- symbolische Namen und konkrete Aufgaben der UI-Ordinalwerte 117 und 149;
- Bedeutung der beiden Relokationspaare für Ordinal 0 und 97;
- ob eine der beiden aufgerufenen UI-Routinen Icon-Bitmap-Decodierung, Moniker-Verarbeitung oder Token-DB-Zugriff ausführt.

## Korrektur zur Gesamtzahl der UI.GEO-Relokationen aus Runde 2458

Beim erneuten Summieren der zehn bereits in Runde 2458 angegebenen Klassen-/Typzähler ergibt sich 2.884, nicht 2.784. Die Einzelzähler aus Runde 2458 ergeben:

- (Klasse 0, Typ 0): 1.125
- (Klasse 2, Typ 2): 997
- (Klasse 2, Typ 4): 378
- (Klasse 0, Typ 1): 121
- (Klasse 0, Typ 2): 121
- (Klasse 1, Typ 4): 100
- (Klasse 2, Typ 3): 39
- (Klasse 1, Typ 1): 1
- (Klasse 1, Typ 2): 1
- (Klasse 1, Typ 3): 1

Summe: 2.884 Relokationseinträge. Auch die Summe der in der Ressourcentabelle gespeicherten Relokationsgrößen geteilt durch vier ergibt 2.884. Der zuvor genannte Summenwert 2.784 war ein Additionsfehler; die zehn Einzelzähler werden durch diese Korrektur nicht verändert.

## Nächster Schritt – Runde 2461

Die beiden tatsächlichen Far-Aufrufziele UI-Ordinal 117 (R2 + 0x0784) und 149 (R7 + 0x0E45) werden in ihrem vollständigen Kontrollfluss untersucht. Dazu sind Funktionsprolog, alle Sprungziele, interne und externe Aufrufe sowie Zugriffe auf Token-/Moniker-Daten getrennt zu dokumentieren. Keine Funktionsnamen vergeben, bevor ein belastbarer String-, API- oder Aufrufkettenbeleg vorliegt.

Arbeitsregel: Originaldateien unverändert lassen. Keine semantischen Namen aus Ordinalnummern ableiten. Statische Befunde, Disassemblierung und Laufzeitbeobachtung strikt trennen.
