# GEOTEST / PC-GEOS 1.x – Untersuchung 2473
## Nullressourcen und abweichende Relokations-Offsetdarstellung
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Ausgangslage
Fortsetzung der Untersuchungen 2471 und 2472 anhand des vom Nutzer bereitgestellten `GEOWORKS.zip`.
Es wurden keine Quelldateien, GEODEs oder Installationsdateien verändert.

## 2. Bestätigter Parserfehler: Nullgroße Ressource
Die Rohdaten der Ressourcen-Tabellen wurden unabhängig von der bisherigen Parser-Validierung ausgelesen. Die Tabellenstruktur ist für die folgenden Dateien konsistent:

### PCX2A.GEO
Pfad: `GEOWORKS/SYSTEM/PCX2A.GEO`
- Ressourcenanzahl: 7
- Imports/Exports: 0/0
- Ressource 0: Größe `0x0000`, Position `0x00000000`, Relokationsbytes `0x0000`
- Ressource 1: Größe `0x00E0`, Position `0x00000166`
- Ressource 2: Größe `0x00D0`, Position `0x0000024A`
- Ressource 3: Größe `0x0090`, Position `0x0000035A`
- Ressource 4: Größe `0x0710`, Position `0x0000040E`

### ICON-ED.GEO
Pfad: `GEOWORKS/WORLD/ICON-ED.GEO`
- Ressourcenanzahl: 11
- Imports/Exports: 1/1
- Ressource 0: Größe `0x0000`, Position `0x00000000`, Relokationsbytes `0x0000`
- Ressource 1: Größe `0x32F0`, Position `0x000001A0`
- Ressource 2: Größe `0x6200`, Position `0x00003544`
- Ressource 3: Größe `0x0140`, Position `0x00009860`

Die nachfolgenden Ressourcenpositionen und Relokationsbereiche sind innerhalb der Dateigrenzen plausibel. Ressource 0 ist daher als leere/Null-Ressource zu behandeln, nicht als Parserfehler. Die Kennzeichnung `unsupported layout` wäre hier ebenfalls zu streng.

### Konsequenz
Der Parser muss `size == 0` zulassen, sofern die übrigen Tabellenwerte und Dateigrenzen konsistent sind. Für eine Nullressource mit null Relokationsbytes ist keine Nutzdaten- oder Relokationsprüfung auszuführen.

## 3. SPLAY.GEO und NPLAYGCM.GEO: abweichende Interpretation des 16-Bit-Relokationsfeldes
Die beiden in 2472 beanstandeten Relokationstabellen wurden erneut geprüft.

### SPLAY.GEO
Pfad: `GEOWORKS/DOCUMENT/SPLAY.GEO`
- Ressource R3: Größe `0x1950`, Position `0x0BDA`, Relokationsbytes `0x03DC` (= 247 Records).
- Beim bisherigen Little-Endian-Lesen ist der dritte Relokationsrecord `0x2C00` und liegt damit außerhalb der Ressource.
- Die beiden gespeicherten Bytes lauten `00 2C`. Als Big-Endian-Offset gelesen ergibt sich `0x002C`.
- An R3+`0x002C` liegt ein `CALL FAR`-Offsetoperand: das vorhergehende Opcodebyte ist `0x9A`.
- Für alle 247 Records der R3-Tabelle liegt der Big-Endian-Kandidat innerhalb der Ressourcengröße; nur 25 Little-Endian-Kandidaten liegen innerhalb.

### NPLAYGCM.GEO
Pfad: `GEOWORKS/NPLAYGCM.GEO`
- Ressource R2: Größe `0x0500`, Position `0x05C2`, Relokationsbytes `0x0128` (= 74 Records).
- Der bisher beanstandete vierte Record enthält die Bytes `00 0F`.
- Little Endian ergibt `0x0F00` (außerhalb R2); Big Endian ergibt `0x000F`.
- An R2+`0x000F` liegt ein `CALL FAR`-Offsetoperand; das vorhergehende Opcodebyte ist `0x9A`.
- Für alle 74 Records der R2-Tabelle liegt der Big-Endian-Kandidat innerhalb der Ressourcengröße; nur 4 Little-Endian-Kandidaten liegen innerhalb.

### Bewertung – bewusst vorläufig
Die Befunde sprechen stark dafür, dass der Offsetteil dieser beiden konkreten Ressourcentabellen nicht mit der bisherigen Little-Endian-Annahme interpretiert werden darf. Die Bytefolgen `00 2C` und `00 0F` werden durch Big-Endian-Lesen zu plausiblen Relokationsstellen; beide zeigen direkt auf CALL-FAR-Operanden.
Das ist noch keine allgemeingültige GEODE-Formatregel. Die übrigen Ressourcen derselben Dateien zeigen andere Verteilungen der beiden Interpretationen. Es ist deshalb nicht zulässig, die Byteordnung pauschal für die gesamte GEODE oder alle Relokationsrecords umzustellen.

## 4. Gegenprobe mit normalen Dateien
Bei ABSGEN.GEO und GENMOUSE.GEO liegen die Relokationsstellen der geprüften Ressource im Little-Endian-Lesen innerhalb der Ressource. Ein globales Umschalten auf Big Endian wäre dort falsch.
Damit sind mindestens zwei unterschiedliche Muster in den untersuchten Dateien vorhanden. Ob die Ursache eine Ressourceneigenschaft, ein Record-Unterformat oder eine bisher falsch verstandene Feldsemantik ist, bleibt offen.

## 5. Kopien und Varianten im Archiv
Die vorhandenen Pfade lauten:
- `GEOWORKS/SYSTEM/PCX2A.GEO`
- `GEOWORKS/WORLD/PROGRAMM.E/G12/FAXEN/PCXFAX/PCX2.GEO`
- `GEOWORKS/WORLD/PROGRAMM.E/G12/FAXEN/PCXUPD/PCX2A.GEO`
- `GEOWORKS/WORLD/ICON-ED.GEO`
- `GEOWORKS/WORLD/PROGRAMM.E/ICOON-ED.GEO`

Die Namen und Pfade belegen allein keine Binäridentität. Für Statistiken müssen SHA-256-Hashes verwendet werden. Die Varianten `ICON-ED.GEO` und `ICOON-ED.GEO` dürfen nicht ohne Hashvergleich zusammengefasst werden.

## 6. Konsequenzen für den Parser
1. Nullgroße Ressourcen sind zulässig, wenn Tabellen und Dateigrenzen konsistent sind.
2. Relokations-Offsets dürfen nicht ohne Kontext auf eine einzige Byteordnung festgelegt werden.
3. Der Parser muss Rohbytes jedes Relokationsrecords erhalten.
4. Eine mögliche Big-Endian-Interpretation darf zunächst nur als Diagnosekandidat erscheinen.
5. Fehler wie „Relokationsziel außerhalb Ressource“ müssen die verwendete Interpretation nennen und dürfen nicht sofort die ganze GEODE verwerfen.
6. Keine Änderung am Packer oder am GEOTEST-Programm, bis die Record-Semantik aus Loadercode oder einer belastbaren Formatbeschreibung bestätigt ist.

## 7. Offene Punkte für Untersuchung 2474
1. Die Relokationstabellen aller Ressourcen von SPLAY.GEO und NPLAYGCM.GEO nach Byteordnung, Recordtyp und Ressourceneigenschaften gruppieren.
2. Für jede Interpretation prüfen, ob die Kandidaten tatsächlich auf Instruktionsoperanden oder Datenfelder zeigen.
3. Den Unterschied zwischen den R1/R2-Tabellen und den auffälligen R3-/R2-Tabellen erklären.
4. Loadercode bzw. SDK-Beschreibung suchen, um die Feldsemantik unabhängig zu bestätigen.
5. Erst danach eine Parserkorrektur implementieren und mit dem gesamten Archiv regressionsprüfen.

## 8. Änderungs- und Teststatus
- `GEOWORKS.zip`: nur lesend untersucht.
- Keine GEO-Datei verändert.
- Keine TOKEN.DB verändert.
- Keine SDK-Quelldatei geändert.
- Kein GEOTEST.GEO-Build.
- Kein Emulator-Laufzeittest.
- Bericht dokumentiert statische Binärbefunde; die Big-Endian-Deutung bleibt ausdrücklich eine Arbeitshypothese.
