# GEOTEST / PC-GEOS 1.x – Untersuchung 2474
## Ressourcengruppen und Byteinterpretation der Relokationstabellen
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Ziel
Untersuchung 2473 hatte gezeigt, dass die Relokations-Offsetbytes in bestimmten Ressourcentabellen von SPLAY.GEO und NPLAYGCM.GEO unter Big-Endian-Lesen plausible Stellen ergeben. Hier werden die übrigen Ressourcen derselben GEODEs als Gegenprobe betrachtet.

## 2. SPLAY.GEO – Ressourcenübersicht
Pfad: `GEOWORKS/DOCUMENT/SPLAY.GEO`

| Ressource | Größe | Flags (roh) | Records | LE-Kandidaten innerhalb Ressource | BE-Kandidaten innerhalb Ressource |
|---:|---:|---:|---:|---:|---:|
| R1 | 0x02F0 | 0x0080 | 58 | 58 | 0 |
| R2 | 0x04F0 | 0x0A72 | 74 | 74 | 17 |
| R3 | 0x1950 | 0x0A72 | 247 | 25 | 247 |
| R4 | 0x0030 | 0x001A | 1 | 1 | 1 |
| R5 | 0x0300 | 0x001A | 1 | 1 | 1 |
| R6 | 0x42C0 | 0x145A | 1 | 1 | 1 |
| R7 | 0x0150 | 0x145A | 1 | 1 | 1 |

R1 spricht klar für Little Endian, R3 klar für Big Endian als Kandidat. R2 liegt überwiegend im Little-Endian-Bereich. R2 und R3 haben denselben Roh-Flagwert `0x0A72`; dieser Flagwert allein erklärt die unterschiedliche Verteilung nicht.

In R3 liegen 5 der 8 Records mit `info=0x00` bei Big-Endian-Interpretation unmittelbar hinter einem `0x9A`-Opcode (CALL FAR). Die anderen drei Kandidaten sind innerhalb der Ressource, zeigen aber nicht auf dieses Opcode-Muster. Das zeigt, dass auch die Kombination aus Recordtyp und Offsetkandidat untersucht werden muss.

## 3. NPLAYGCM.GEO – Ressourcenübersicht
Pfad: `GEOWORKS/NPLAYGCM.GEO`

| Ressource | Größe | Flags (roh) | Records | LE-Kandidaten innerhalb Ressource | BE-Kandidaten innerhalb Ressource |
|---:|---:|---:|---:|---:|---:|
| R1 | 0x02F0 | 0x0080 | 58 | 58 | 0 |
| R2 | 0x0500 | 0x0A72 | 74 | 4 | 74 |
| R3 | 0x17C0 | 0x0A72 | 234 | 234 | 216 |
| R4 | 0x07F0 | 0x145A | 1 | 1 | 1 |
| R5 | 0x0240 | 0x001A | 1 | 1 | 1 |
| R6 | 0x4690 | 0x145A | 1 | 1 | 1 |
| R7 | 0x0150 | 0x145A | 1 | 1 | 1 |

R1 spricht klar für Little Endian, R2 klar für Big Endian als Kandidat. R3 lässt beide Interpretationen überwiegend innerhalb der Ressourcengröße zu. Auch hier haben R2 und R3 denselben Roh-Flagwert `0x0A72`, so dass der Flagwert allein die Unterschiede nicht erklärt.

In R2 liegen 5 der 19 Records mit `info=0x00` bei Big-Endian-Interpretation unmittelbar hinter einem `0x9A`-Opcode. Drei weitere `info=0x00`-Records sind Nullwerte am Tabellenanfang. Die übrigen Kandidaten sind zwar innerhalb R2, aber nicht direkt durch das CALL-FAR-Muster bestätigt.

## 4. Konsequenz für die bisherige Parserlogik
Die Prüfung bestätigt:
- Eine globale Byteordnungsänderung für eine ganze GEODE wäre falsch.
- Eine globale Byteordnungsannahme für jede Ressource ist mit den vorliegenden Daten ebenfalls nicht abgesichert.
- Der Roh-Flagwert `0x0A72` reicht nicht aus, um zwischen den Mustern zu unterscheiden.
- Die Zahl „Offset innerhalb Ressourcengröße“ ist nur ein Plausibilitätsfilter und kein Beweis für die Bedeutung eines Relokationsfeldes.
- Der bisherige Fehler bei SPLAY R3 und NPLAYGCM R2 darf nicht mehr als Beleg für eine beschädigte Datei gelten.

## 5. Dateivarianten und Hashprüfung
Die fünf genannten Archivpfade wurden SHA-256-geprüft:

| Datei | Größe | SHA-256 |
|---|---:|---|
| SYSTEM/PCX2A.GEO | 3.330 | `0ad2b302f1fc24ec453e6393534418ddbacff54e595b98febd13fdf052d5c199` |
| PROGRAMM.E/G12/FAXEN/PCXFAX/PCX2.GEO | 3.330 | `7e4e855d2a76eb1e9fb79d6e95e11dbfd270298a885bf1b3d07cf1c689c366e4` |
| PROGRAMM.E/G12/FAXEN/PCXUPD/PCX2A.GEO | 3.330 | `8bc6e12d2946fc02e3f7047f494a9dcba40e0824c4d14ce959d34561a04d51fd` |
| WORLD/ICON-ED.GEO | 47.648 | `afbbd1d8115c82162e8d3c9331c5d945e073e0823852bb5c68055ba6148df064` |
| WORLD/PROGRAMM.E/ICOON-ED.GEO | 47.536 | `a7340dd2e08ab1553aec684de3513b622e36503c37a79a73c0fe8677904ecb08` |

Die drei PCX-Dateien sind drei unterschiedliche Binärdateien. ICON-ED.GEO und ICOON-ED.GEO sind ebenfalls unterschiedliche Binärdateien. Eine Zusammenfassung als Duplikate wäre falsch.

## 6. Zwischenfazit
Die Relokationstabellen zeigen ressourcenabhängige Muster. Für SPLAY R3 und NPLAYGCM R2 ist die Big-Endian-Kandidateninterpretation stark plausibel, aber nicht für die ganze GEODE verallgemeinerbar. Der Parser muss deshalb Rohbytes, Ressourcenkontext, Flags und alternative Offsetkandidaten getrennt protokollieren, bis der Loadercode die Feldsemantik erklärt.

## 7. Nächste Untersuchung 2475
1. Die Rohstruktur der Relokationseinträge mit einer unabhängigen Formatbeschreibung bzw. Loader-Routine abgleichen.
2. Den 4-Byte-Record nicht nur als `info, extra, little-endian word` modellieren, sondern alternative Feldaufteilungen gegen echte Code-/Datenstellen prüfen.
3. KERNEL.EXE und weitere GeoWorks-1.x-Systemkomponenten auf Loaderpfade untersuchen, ohne PC/GEOS 2.x-Code einzubeziehen.
4. Erst nach Bestätigung der Recordstruktur Parseränderungen vornehmen.

## 8. Änderungs- und Teststatus
- Archiv nur lesend untersucht.
- Keine GEO-Datei verändert.
- Keine TOKEN.DB verändert.
- Keine SDK-Quelldatei geändert.
- Kein GEOTEST.GEO-Build und kein Emulator-Laufzeittest.
- Die Big-Endian-Interpretation bleibt ein Diagnosekandidat, keine bestätigte Formatregel.
