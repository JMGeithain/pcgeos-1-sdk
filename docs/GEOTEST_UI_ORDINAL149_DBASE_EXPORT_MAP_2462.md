# GEOTEST – UI-Ordinal-149-Relokationen und DBASE-Exportabgleich (Runde 2462)

## Ziel und Methode

Diese Runde setzt die statische Untersuchung von UI.GEO (GeoWorks 1.2.8 / PC/GEOS 1.x) fort. Untersucht werden die sieben Relokationseinträge im Bereich von UI-Exportordinal 149 sowie die DBASE-Exportziele, die von UI-Ordinal 117 referenziert werden. Die Originaldateien wurden byteweise gehasht; die DBASE.GEO-Datei wurde direkt aus dem ursprünglichen GEOWORKS.zip extrahiert.

Es wurde kein Laufzeittest ausgeführt. Relokationsklassen/-typen werden nur als Rohwerte behandelt, soweit ihre vollständige Semantik nicht belegt ist.

## Quellen und Prüfsummen

| Datei | Größe | SHA-256 |
|---|---:|---|
| UI.GEO | 87.900 | 13a3a82ec3d4373b120890a11eb09b3a9f9ec456ca633819728f53c07883c73a |
| ICON-ED.GEO | 47.648 | afbbd1d8115c82162e8d3c9331c5d945e073e0823852bb5c68055ba6148df064 |
| DBASE.GEO | 2.930 | 209d45d361cff3daeb982c07d8faa4fbd3b7f86b4fbba1d18a54a78b44ed12cd |

DBASE.GEO befindet sich im Archiv unter GEOWORKS/SYSTEM/DBASE.GEO. Der Header weist fünf Ressourcen, keine Imports und 23 Exporte aus. UI.GEO importiert dbase mit Protokollrohwert 601.

## UI-Ordinal 149 – genaue Relokationsbefunde

UI-Ordinal 149 zeigt auf UI.GEO R7 + 0x0E45 (Dateioffset 0x852D). Im Codebereich 0x0E45–0x0ECB befinden sich sieben Far-Aufrufstellen mit Klasse-0-/Typ-0-Relokationseinträgen:

| Aufrufstelle (R7-Offset) | Rohwert im Offsetfeld | Relokation info | Klasse | Typ |
|---:|---:|---:|---:|---:|
| 0x0E55 | 0x0095 | 0x00 | 0 | 0 |
| 0x0E62 | 0x0099 | 0x00 | 0 | 0 |
| 0x0E6A | 0x00A9 | 0x00 | 0 | 0 |
| 0x0E9A | 0x00A9 | 0x00 | 0 | 0 |
| 0x0EA5 | 0x0099 | 0x00 | 0 | 0 |
| 0x0EB2 | 0x00A9 | 0x00 | 0 | 0 |
| 0x0EC0 | 0x00A9 | 0x00 | 0 | 0 |

Die fünf Bytes jeder Aufrufstelle beginnen mit Opcode 0x9A (CALL FAR). Die beiden folgenden WORD-Felder sind die Rohwerte Offset 0x0095/0x0099/0x00A9 und Segment 0x0000.

**Wichtige Einschränkung:** Der Parser weist für diese Einträge Klasse 0 und Typ 0 aus. Die Semantik dieser Kombination ist hier nicht vollständig geklärt. Deshalb werden 0x0095, 0x0099 und 0x00A9 nicht als bestätigte Exportordinale oder als bestätigte Funktionsanfänge bezeichnet. Ein isolierter Disassemblierungsstart bei 0x0099 bzw. 0x00A9 landet innerhalb der von einem linearen Disassembler ab 0x0095 erkannten Instruktionsfolge. Das unterstreicht, dass man aus den Zahlen allein keine Funktionsgrenze ableiten darf.

Der Bytebefund bestätigt sieben far-call-artige Aufrufstellen und die zugehörigen Relokationsfelder. Er beweist nicht, dass die Ziele eigenständige Routinen innerhalb von R7 sind.

## UI-Ordinal 117 – Zuordnung der DBASE-Importordinale

UI-Ordinal 117 liegt in UI.GEO R2 + 0x0784. In seinem Bereich wurden 15 Klasse-1-/Typ-4-Relokationen mit Importindex 1 (dbase) identifiziert. Die Zielwerte sind DBASE-Importordinalwerte. Abgleich mit der DBASE.GEO-Exporttabelle:

| DBASE-Ordinal (hex) | DBASE-Ressource | Exportoffset | Dateioffset in DBASE.GEO |
|---:|---:|---:|---:|
| 0x01 | R2 | 0x0335 | 0x04F3 |
| 0x03 | R4 | 0x0087 | 0x0AC5 |
| 0x04 | R4 | 0x00A8 | 0x0AE6 |
| 0x05 | R4 | 0x00B3 | 0x0AF1 |
| 0x07 | R2 | 0x03BD | 0x057B |
| 0x08 | R2 | 0x048B | 0x0649 |
| 0x0C | R2 | 0x063D | 0x07FB |
| 0x0D | R2 | 0x0651 | 0x080F |
| 0x10 | R2 | 0x066E | 0x082C |
| 0x11 | R2 | 0x0674 | 0x0832 |
| 0x12 | R4 | 0x00C3 | 0x0B01 |
| 0x13 | R4 | 0x00D4 | 0x0B12 |

Die 15 Relokationsverweise im UI-Ordinal-117-Bereich verwenden zwölf unterschiedliche DBASE-Ordinalwerte: 0x01, 0x03, 0x04, 0x05, 0x07, 0x08, 0x0C, 0x0D, 0x10, 0x11, 0x12 und 0x13. Die DBASE-Exporttabelle hat 23 Einträge; die hier referenzierten Werte sind gültige Tabellenindizes.

Die Exporttabelle enthält keine symbolischen Funktionsnamen. Daher werden die DBASE-Exporte hier nur durch Ordinal, Ressource und Offset identifiziert. Die Byteanfänge zeigen unterschiedliche Codeformen: etwa kurze Far-Thunk-Exporte in R2 und kleine Wrapper in R4. Ohne gesicherte ABI- und Aufrufkontextanalyse werden daraus keine Funktionsnamen abgeleitet.

## Was sich daraus ableiten lässt

**Gesichert:**

1. UI-Ordinal 149 enthält sieben far-call-artige Stellen mit Klasse-0-/Typ-0-Relokationen.
2. Die Roh-Offsetfelder dieser Stellen lauten 0x0095, 0x0099 und 0x00A9.
3. Die Bedeutung dieser Klasse-0-/Typ-0-Ziele ist noch nicht geklärt; es wäre falsch, sie bereits als lokale Funktionsadressen oder UI-Ordinalwerte zu bezeichnen.
4. UI-Ordinal 117 verwendet 15 dbase-Importrelokationen mit zwölf verschiedenen DBASE-Ordinalwerten.
5. Alle zwölf DBASE-Ordinalwerte sind in der echten DBASE.GEO-Exporttabelle vorhanden und zeigen auf R2 oder R4.
6. Die Dateiprüfsummen belegen die untersuchten Originaldateien.

**Nicht bewiesen:**

- dass UI-Ordinal 149 einen Icon-Decoder implementiert;
- dass die Konstanten 0xA000, 0x8000, 0x41BF oder 0x41A2 bestimmte Grafikhardware oder einen konkreten Icon-Puffer bezeichnen;
- die symbolischen Namen oder API-Verträge der DBASE-Ordinalwerte;
- die semantische Bedeutung der Klasse-0-/Typ-0-Relokationen.

## Nächster Schritt – Runde 2463

Die DBASE-Exportziele aus R2 und R4 werden als vollständige Kontrollflussbereiche untersucht. Parallel wird die Bedeutung der Klasse-0-/Typ-0-Relokation anhand weiterer UI.GEO-Ressourcen und Vergleichsstellen geprüft. Besonders wichtig ist, die Relokationsfelder mit ihren vollständigen Segment-/Offsetkontexten zu vergleichen, statt die Rohwerte 0x0095, 0x0099 und 0x00A9 isoliert zu interpretieren.

Arbeitsregel: Keine Funktionsnamen erfinden. Keine semantische Deutung allein aus Konstanten oder einzelnen Opcodes. Originaldateien unverändert lassen und statische Analyse strikt von Laufzeitbeobachtung trennen.
