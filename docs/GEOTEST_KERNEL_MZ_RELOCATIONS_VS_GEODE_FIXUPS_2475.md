# GEOTEST / PC-GEOS 1.x – Untersuchung 2475
## KERNEL.EXE / KERNEL.OLD: DOS-MZ-Relokationen und CALL-FAR-Fixups
Datum: 12.11.2026

## 1. Dateien und Prüfsummen
Direkt aus dem vom Nutzer bereitgestellten GEOWORKS.zip gelesen:

| Datei | Größe | SHA-256 |
|---|---:|---|
| GEOWORKS/KERNEL.EXE | 72.736 | c2cc8952cdb01d0f459bf281ee3b78f8ce9464aba0b58c3758f8c73e24fb6eb5 |
| GEOWORKS/KERNEL.OLD | 72.688 | bd4d680b15f8dd66b2b09b506de96672972f716a11e0a38220477bf07b6c1e9b |

Nach der vom Nutzer zuvor mitgeteilten Provenienz ist KERNEL.EXE gepatcht und KERNEL.OLD die ursprüngliche deutsche Kernel-Datei. Sie wurden getrennt untersucht.

## 2. DOS-MZ-Header
| Feld | KERNEL.EXE | KERNEL.OLD |
|---|---:|---:|
| e_cblp | 0x0020 | 0x01F0 |
| e_cp | 0x008F | 0x008E |
| e_crlc (MZ-Relokationen) | 276 | 273 |
| e_cparhdr | 0x0060 | 0x0060 |
| e_ss | 0x0E34 | 0x0E35 |
| e_sp | 0x15F0 | 0x15B0 |
| e_ip | 0x02B1 | 0x02B1 |
| e_cs | 0x0000 | 0x0000 |
| e_lfarlc | 0x003C | 0x003C |

Headergröße: 0x60 * 16 = 0x600 Bytes. Die MZ-Relokationstabelle beginnt bei Dateioffset 0x003C und enthält e_crlc Records zu je vier Bytes.

Die DOS-Dateigrößenformel bestätigt die Archivgrößen:
- KERNEL.EXE: (0x8F - 1) * 512 + 0x20 = 72.736
- KERNEL.OLD: (0x8E - 1) * 512 + 0x1F0 = 72.688

## 3. Direkter Beleg: MZ-Relokation am CALL FAR
Der MZ-Einstiegspunkt CS:IP = 0000:02B1 liegt im Dateiinhalt bei 0x600 + 0x2B1 = 0x08B1.

KERNEL.EXE bei 0x08B1:
`9A 00 00 93 0F`
- Opcode 9A
- Offsetwort 0x0000
- Segmentwort 0x0F93

Die MZ-Tabelle enthält (offset=0x02B4, segment=0x0000), exakt Instruktionsanfang +3, also das Segmentwort.

Zweite Instruktion bei 0x08C5:
`9A C7 01 93 0F`
Die MZ-Tabelle enthält (offset=0x02C8, segment=0x0000), ebenfalls Instruktionsanfang +3.

KERNEL.OLD enthält an denselben Stellen:
- 0x08B1: `9A 00 00 90 0F`
- 0x08C5: `9A C7 01 90 0F`
Auch dort liegen die MZ-Relokationen bei 0x02B4 und 0x02C8.

Damit ist für diese Beispiele bytegenau belegt: Die DOS-MZ-Relokation liegt auf dem Segmentwort (+3), nicht auf dem Offsetwort (+1).

## 4. Scan der Kernel-CALL-FAR-Muster
| Datei | 0x9A-Treffer mit vier Folgebytes | MZ-Relokation am Offsetwort (+1) | MZ-Relokation am Segmentwort (+3) |
|---|---:|---:|---:|
| KERNEL.EXE | 215 | 0 | 178 |
| KERNEL.OLD | 208 | 0 | 175 |

Für jeden 0x9A-Treffer wurde geprüft, ob der MZ-Relokationsort auf Instruktionsanfang+1 oder +3 fällt. Dies ist ein statischer Bytevergleich; nicht jeder 0x9A-Treffer muss ausführbarer Code sein.

## 5. Abgrenzung zu GEODE-Relokationen
MZ-Relokationen und GEODE-Fixups sind getrennte Tabellen:
- MZ: DOS-Lader-Tabelle des Kernel-EXE; die Beispiele zeigen die Anpassung des Segmentwortes eines Far-Pointers.
- GEODE: Fixup-Records innerhalb der Ressourcen einer GEODE-Datei; die früheren Untersuchungen zeigen bei source=0,type=0 häufig einen Zielort auf dem Offsetwort einer CALL-FAR-Instruktion (0x9A unmittelbar davor).

Der MZ-Befund erklärt die GEODE-Fixup-Semantik nicht automatisch. Die konkrete GEODE-Relokationsroutine im GeoWorks-1.x-Kernel ist noch nicht identifiziert.

## 6. Externe Formatquelle
Marcus Gröbers GeoDump-Dokumentation beschreibt auf hoher Ebene den Aufbau einer Geode mit Programmheader, Import-/Exportlisten, Ressourcentabelle und Fixup-Tabelle. Die Fixups korrigieren Verweise auf Systemfunktionen oder verschiebbare Ressourcen. Die Dokumentation sagt, dass GeoDump bereits 1991 begonnen wurde. Sie ist eine historische Reverse-Engineering-Quelle, aber kein Nachweis der konkreten 1.x-Loader-Routine:
https://www.mgroeber.de/geodump-documentation.html (Abschnitte „Executable programs (geodes)“ und „Assigning symbolic names to library references“).

Es wurden keine PC/GEOS-2.x-/FreeGEOS-Strukturen als Beleg für GeoWorks 1.x übernommen.

## 7. Belastbare Ergebnisse
1. Beide Kerneldateien sind DOS-MZ-Executables mit 0x600-Byte-Header.
2. KERNEL.EXE enthält 276, KERNEL.OLD 273 DOS-MZ-Relokationsrecords.
3. Die zwei am Einstiegspunkt untersuchten CALL-FAR-Instruktionen haben MZ-Relokationen auf dem Segmentwort (+3).
4. Im Kernelmodul wurden 178 bzw. 175 CALL-FAR-Segmentwortpositionen durch MZ-Relokationen getroffen; kein Treffer lag auf dem Offsetwort (+1).
5. Dieser MZ-Befund ist nicht die gesuchte Erklärung der GEODE-Fixup-Records.
6. Die tatsächliche GEODE-Relokationsroutine im GeoWorks-1.x-Kernel ist noch nicht identifiziert.

## 8. Konsequenz für SDK und GEOTEST
- Keine Parseränderung auf Basis dieses Kernelvergleichs.
- MZ-Relokationen und GEODE-Fixups als getrennte Formate behandeln.
- GEODE-Records weiterhin roh speichern und ihre Felder nicht umdeuten.
- Nächster Schritt: Kernelmodul mit korrektem Einstiegspunkt und Relokationsbezug disassemblieren; gezielt Routinen mit Zugriff auf GEODE-Header, Ressourcentabellen und Fixup-Records verfolgen.

## 9. Änderungs- und Teststatus
- GEOWORKS.zip nur lesend untersucht.
- KERNEL.EXE und KERNEL.OLD nicht verändert.
- Keine GEO-Datei oder TOKEN.DB verändert.
- Keine SDK-Quelldatei geändert.
- Kein GEOTEST.GEO-Build und kein Emulator-Laufzeittest.
