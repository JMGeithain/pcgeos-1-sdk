# GEOTEST / PC-GEOS 1.x – Untersuchung 2472
## Sonderfälle der CALL-FAR-Relokationen und Parser-Grenzfälle
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Ausgangsbasis
Fortsetzung der Untersuchung 2471. Geprüft wurde das vom Nutzer bereitgestellte `GEOWORKS.zip`.
Die Stichprobe umfasst 221 unterschiedliche, per SHA-256 deduplizierte GEODE-1-Binärdateien, die der aktuelle Prüfer vollständig einlesen konnte. Darin liegen 35.250 Relokationen `source=0, type=0`; alle 35.250 stehen auf dem Offsetoperand einer `CALL FAR`-Instruktion.

## 2. Die fünf Offsetwerte außerhalb sämtlicher Ressourcengrößen
Die fünf Fälle aus 2471 wurden direkt im Bytekontext geprüft:

| Datei | Ressource | Relokationsoffset | CALL-FAR-Offsetoperand | Segmentwort |
|---|---:|---:|---:|---:|
| ABSGEN.GEO | R3 | `0x006B` | `0x022F` | `0x0000` |
| DISK.GEO | R3 | `0x004B` | `0x022E` | `0x0000` |
| DISK.GEO | R3 | `0x0079` | `0x022F` | `0x0000` |
| GENMOUSE.GEO | R3 | `0x006B` | `0x022F` | `0x0000` |
| ICON.GEO (ICONEDIT.OR) | R2 | `0x0003` | `0x0238` | `0x0000` |

Bei allen fünf Fällen ist das Byte unmittelbar vor dem Relokationsoperand `0x9A`. Das Maschinenmuster lautet jeweils `9A <offset-low> <offset-high> 00 00`.

### 2.1 Gemeinsamkeiten und Unterschiede
- ABSGEN.GEO und GENMOUSE.GEO besitzen an der Fundstelle dieselbe Bytefolge und dieselbe Importdeklaration `im`.
- DISK.GEO besitzt als Import `swap`.
- ICON.GEO besitzt als Import `ui`.
- Alle fünf GEODEs haben an diesen Fundstellen keine Exporttabelleneinträge, die den Offsetoperand unmittelbar als Exportziel erklären würden.
- Die Offsetwerte liegen außerhalb aller Ressourcengrößen der jeweiligen Datei.

Diese Gemeinsamkeiten belegen, dass es sich nicht um gewöhnliche, innerhalb der aufrufenden Ressource liegende Codeziele handelt. Sie beweisen aber nicht, ob die Aufrufe auf einen Kernel-/Systemvektor, einen speziellen Loader-Einstieg oder einen anderen globalen Adressraum zielen.

### 2.2 Was nicht gefolgert werden darf
Die Werte `0x022E`, `0x022F` und `0x0238` dürfen nicht als Exportordinale, Kernel-Funktionsnummern oder absolute Offsets einer bestimmten Systemdatei bezeichnet werden. Die Relokationsrecords und Segmentwörter reichen für diese Zuordnung nicht aus.

## 3. Die 294 nichtnulligen Segmentliterale – zusätzliche Einordnung
Die 294 Fälle enthalten 56 verschiedene 16-Bit-Segmentliterale. Häufige Werte sind:
- `0x0E18`: 20 Fälle
- `0x0E24`: 19
- `0x0DF4`: 15
- `0x0E0C`: 15
- `0x0E30`: 15
- `0x0E3C`: 15

Vergleich mit Ressourcenlängen, Ressourcen-Dateioffsets und Export-Offsets der jeweiligen GEODE:
- 285 Werte haben keinen direkten Tabellen-Treffer;
- 8 Werte entsprechen einer Ressourcenlänge;
- 1 Wert entspricht einem Export-Offset.

Das sind nur numerische Koinzidenzen. Es gibt keinen belastbaren Beleg, dass diese Literale Segmentadressen oder Ressourcenkennungen darstellen. Die Verteilung kann auch durch wiederverwendete Codevorlagen oder Compiler-/Linker-Konventionen entstehen.

## 4. Sieben Dateien, die der aktuelle Parser nicht vollständig akzeptiert
Der strenge Prüfer hat sieben Dateipfade mit GEODE-Format-1-Signatur nicht in die 221-Datei-Statistik aufgenommen. Die Fehler sind nicht einheitlich:

### 4.1 SPLAY.GEO und NPLAYGCM.GEO
- Beide besitzen 14 Ressourcen, 3 Imports und 5 Exporte.
- Der Prüfer findet in einer Relokationstabelle einen Zielwert, der größer als die angegebene Ressourcengröße ist:
  - SPLAY.GEO: R3, Relokationsrecord 2, Zielwert `0x2C00`, gemeldete Ressourcengröße `0x1950`.
  - NPLAYGCM.GEO: R2, Relokationsrecord 3, Zielwert `0x0F00`, gemeldete Ressourcengröße `0x0500`.

Dies kann auf eine Sonderform der Relokationsziele, eine andere Ressourcendarstellung oder eine falsche Annahme des Prüfers über die Record-Semantik hinweisen. Es ist kein ausreichender Beleg für beschädigte Dateien.

### 4.2 PCX2A.GEO und zwei Kopien von PCX2.GEO/PCX2A.GEO
- Die Dateien haben 7 Ressourcen und keine Imports/Exports.
- Die aktuelle Tabelleninterpretation liest für Ressource 0 Größe und Position als null und verwirft deshalb die Datei.
- Die Dateien sind 3.330 Byte groß und besitzen die Format-1-Signatur.
- Die drei Pfade gehören zu derselben PCX2A/PCX2-Variante; sie dürfen in einer Statistik nicht mehrfach als unabhängige Beispiele zählen.

### 4.3 ICON-ED.GEO und ICOON-ED.GEO
- Beide Dateien haben 11 Ressourcen, 1 Import und 1 Export.
- Die aktuelle Tabelleninterpretation liest für Ressource 0 eine Nullgröße/-position und verwirft die Dateien.
- Die Dateien sind zwei leicht unterschiedliche Binärvarianten, nicht dieselbe SHA-256-Datei.

### 4.4 Parser-Fazit
Die sieben Fälle zeigen, dass die bisherige strenge Format-1-Tabelleninterpretation noch nicht für alle Varianten des Archivs validiert ist. Insbesondere darf ein Nullwert in einer vermeintlichen Ressourcenlängen-/Positionsspalte nicht automatisch als beschädigte GEODE-Datei gewertet werden.
Der Parser braucht eine getrennte Untersuchung der Tabellenlayout-Varianten und der Relokationszielsemantik. Die Dateien werden vorerst nicht in die 35.250-Statistik aufgenommen.

## 5. Belastbare Schlussfolgerungen
1. Die fünf Offsetwerte außerhalb sämtlicher Ressourcengrößen sind echte CALL-FAR-Offsetoperanden, aber ihre Zielräume sind unbekannt.
2. Die fünf Aufrufe sind nicht durch Exportziele derselben GEODE erklärt.
3. Die wiederkehrenden Segmentliterale in anderen GEODEs bleiben numerisch auffällig, aber semantisch ungeklärt.
4. Die sieben Parser-Ausnahmen sind kein Beweis für defekte Originaldateien; sie weisen auf Grenzen der aktuellen Parserannahmen hin.
5. Es gibt weiterhin keinen ausreichenden Beleg, um Klasse 0 / Typ 0 in eine Loaderaktion oder konkrete Zieladressart umzudeuten.

## 6. Konsequenz für SDK und GEOTEST
Keine Änderung an `geode.py`, `packer.py` oder `buildsys.py`.
Der Parser soll vorerst:
- die Rohwerte der Relokation unverändert erhalten;
- die `CALL FAR`-Operandposition als Diagnose annotieren;
- Offsets außerhalb der Quellressource als Warnhinweis, nicht als Fehler, ausgeben;
- nichtnullige Segmentliterale separat anzeigen;
- unbekannte Tabellenvarianten nicht als beschädigte Dateien klassifizieren, sondern als `unsupported/unverified layout`.

## 7. Nächste Untersuchung 2473
1. Header- und Ressourcentabellen von PCX2A.GEO und ICON-ED.GEO unabhängig von der bisherigen Parserannahme neu rekonstruieren.
2. SPLAY.GEO und NPLAYGCM.GEO: die betreffenden Relokationsrecords einschließlich ihrer vollständigen Tabellenbytes untersuchen.
3. Nach einer autoritativen GeoWorks-1.x-/GEODE-Formatbeschreibung oder nach Loadercode suchen, der die Relokationsrecords verarbeitet.
4. Erst mit diesem Beleg die tatsächliche Zielauflösung der CALL-FAR-Relokationen spezifizieren.

## 8. Änderungsstatus
- `GEOWORKS.zip` nur gelesen.
- Keine GEO-Datei verändert.
- TOKEN.DB nicht verändert.
- SDK-Quelldateien und GEOTEST.GEO nicht verändert.
- Kein Build und kein Emulator-Laufzeittest.
