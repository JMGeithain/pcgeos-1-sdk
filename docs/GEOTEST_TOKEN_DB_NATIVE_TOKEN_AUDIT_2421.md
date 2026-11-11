# GEOTEST – TOKEN.DB: native Dokumenttoken und Provider-Einträge (2421)

Stand: 2026-11-12  
Geltungsbereich: ausschließlich originales GeoWorks / PC/GEOS 1.x  
Quelle: vom Nutzer bereitgestelltes `GEOWORKS.zip`; ausschließlich lesende Rohdatenanalyse.

## 1. Untersuchte Dateien

| Datei | Größe | SHA-256 |
|---|---:|---|
| `GEOWORKS/SYSTEM/TOKEN.DB` | 952.688 Byte | `c7fa3d51c9bdce14b988d20fd8ed57ac7da9837803090ac858990613ec53ae35` |
| `GEOWORKS/SYSTEM/TOKENDB.ALT/TOKEN.DB` | 1.102.576 Byte | `566ce17e4de804a45423c7357d20e8c0fa2d589c3c6ba508210a8c7a6f60f298` |
| `GEOWORKS/BUCH/TOKEN.DB` | 124.576 Byte | `1b786d398986288e3b1f3e79d020dd18c8549632f9fad9266365bb2f785d1e51` |
| `GEOWORKS/GEOS.INI` | 6.754 Byte | `8d0f477d276770c43c8ea878ea2e8593c5f397912ba61535b93ce4cf976014bf` |

Alle drei TOKEN.DB-Dateien beginnen mit der GEOS-Signatur `C7 45 CF 53`; bei Offset `0020h` steht der Dateiname `TOKEN.DB`. Die Hauptdatei und TOKENDB.ALT sind deutlich umfangreicher als die Buch-Ausgabe. Die vorliegende Untersuchung nimmt keine vollständige VM-/LMem-Dekodierung der Datenbank vor.

## 2. Native GeoWrite-/GeoDraw-Tokens sind in der Systemdatenbank enthalten

In der Hauptdatei `GEOWORKS/SYSTEM/TOKEN.DB` wurden folgende ASCII-Treffer bytegenau gefunden:

| Token | Anzahl | Datei-Offsets |
|---|---:|---|
| `WP00` | 4 | `42C6Ch, 5333Ch, DAD4Ch, E1550h` |
| `WDAT` | 4 | `42C86h, 53356h, DAD66h, E156Ah` |
| `DP00` | 12 | `532CCh, AF126h, AF1DEh, C7568h, DACDCh, DB936h, DB9EEh, DBE9Eh, E14E0h, E213Ah, E21F2h, E26A2h` |
| `DDAT` | 8 | `42C1Eh, 532EEh, AF17Ch, C7506h, DACFEh, DB98Ch, E1502h, E2190h` |

Damit ist für die konkrete GeoWorks-Installation belegt, dass die anwendungsspezifischen GeoWrite-/GeoDraw-App- und Dokumenttokens als Daten in TOKEN.DB vorkommen. Das stützt die Aussage aus `DOS_ICON.TXT`, dass `WDAT` und `DDAT` in TOKEN.DB geführt werden.

Die Wiederholungen zeigen mehrere Vorkommen innerhalb der Datenbankdatei. Ohne VM-Map-/Block- und LMem-Referenzauflösung werden sie hier nicht als vier bzw. zwölf unabhängige Registrierungseinträge interpretiert.

## 3. PAPR und gDOC sind ebenfalls in TOKEN.DB auffindbar

Die Hauptdatei enthält außerdem:

| Token | Anzahl | Datei-Offsets |
|---|---:|---|
| `PAPR` | 3 | `AEF36h, DB746h, E1F4Ah` |
| `gDOC` | 3 | `2FF58h, DB5A8h, E1DACh` |

Am Vorkommen `PAPR` bei `AEF36h` folgt unmittelbar die Bytefolge:

```
50 41 50 52 FF 00 74 00 DC 01 00 00 ...
 P  A  P  R  255
```

Am Vorkommen `gDOC` bei `2FF58h` folgt:

```
67 44 4F 43 FF 00 74 00 9C 01 00 00 ...
 g  D  O  C  255
```

Die Herstellerkennung `FF 00` (255) stimmt mit den Headerwerten der untersuchten Provider-Geodes `PAPR.000` und `GDOC.000` überein. Das ist ein konkreter Zusammenhang zwischen Provider-Token/Herstellerkennung und TOKEN.DB-Daten. Die vollständige Bedeutung der nachfolgenden Wörter und Zeiger ist noch nicht aufgelöst.

## 4. GEOTEST ist in den untersuchten Datenbanken noch nicht eingetragen

Die Zeichenfolge `GTS1` wurde in keiner der drei untersuchten TOKEN.DB-Dateien gefunden. Auch die bislang nur als Kandidat diskutierten Kennungen `GTD1` und `GTD ` wurden nicht als bestätigte Einträge festgestellt.

Das ist kein Hindernisbeweis für die spätere Implementierung: Es zeigt lediglich, dass die unveränderten Archivdatenbanken keinen sichtbaren `GTS1`-Eintrag enthalten. Eine neue Kennung müsste erst nach Klärung des Datenbankformats und des Registrierungsweges korrekt ergänzt werden. Die Original-TOKEN.DB bleibt unangetastet.

## 5. Abgrenzung zu GEOS.INI / filenameTokens

Die originale `GEOWORKS/GEOS.INI` enthält im Abschnitt `[fileManager]` eine `filenameTokens`-Tabelle. Die dort vorhandenen Beispiele lauten u.a.:

- `*.EXE = "gDOS",0`
- `*.COM = "gDOS",0`
- `*.BAT = "gDOS",0`
- `*.TXT = "FILE",0,"NPAD",0`
- `*.DOC = "FILE",0,"NPAD",0`

Die Tabelle ordnet DOS-Dateinamenerweiterungen generischen Typ-/Anwendungskennungen zu. Sie enthält keine `GTD`- oder `GTS1`-Zuordnung. Das bestätigt weiterhin nicht, dass `filenameTokens` der Weg für native GEOS-Dateien mit internem Typ-/Creator-Kopf ist.

## 6. Was jetzt belegt ist – und was nicht

**Belegt:**
1. Die GeoWorks-Systemdatei TOKEN.DB enthält die nativen GeoWrite-/GeoDraw-Tokens `WP00`, `WDAT`, `DP00`, `DDAT`.
2. TOKEN.DB enthält außerdem `PAPR` und `gDOC`; bei diesen Vorkommen ist die Herstellerkennung 255 in den benachbarten Bytes sichtbar.
3. Die Haupt-GEOS.INI verwendet `filenameTokens` für DOS-Dateierweiterungen wie EXE, COM, BAT, TXT und DOC.
4. `GTS1` ist in den drei untersuchten TOKEN.DB-Dateien nicht als ASCII-Token vorhanden.

**Noch nicht belegt:**
1. Welche TOKEN.DB-Blöcke und LMem-Chunks für die einzelnen Tokens maßgeblich sind.
2. Wie GeoManager einen nativen GEOS-Dateikopf (Typ, Hersteller-ID, Creator) in einen konkreten TOKEN.DB-Datensatz übersetzt.
3. Wie die Token-Datensätze auf die Icon-/Moniker-Ressourcen verweisen.
4. Ob ein neuer Provider-Eintrag genügt oder ob zusätzlich ein bestimmter Token-DB-Registrierungs- bzw. Installationsschritt erforderlich ist.
5. Ob und wie ein GEOTEST-Dokumenttyp mit eigener Hersteller-ID registriert werden muss.

## 7. Nächster Untersuchungsschritt (2422)

Die nächste Untersuchung muss die TOKEN.DB-VM-Struktur auflösen, nicht die Datenbank verändern:

1. VM-Header, Map-Block und VM-Blockverzeichnis der Haupt-TOKEN.DB auslesen.
2. Die wiederkehrenden Token-Vorkommen `WP00/WDAT`, `DP00/DDAT`, `PAPR` und `gDOC` ihren VM-Blöcken und LMem-Chunks zuordnen.
3. Die jeweiligen Datensätze mit den Icon-/Moniker-Payloads verbinden.
4. Den Unterschied zwischen Haupt-TOKEN.DB, TOKENDB.ALT und der kleinen BUCH/TOKEN.DB anhand ihrer Blockstruktur untersuchen.
5. Erst nach belegtem Format einen sicheren, separaten Testdatenbank-Prototyp planen. Niemals die originale Systemdatenbank überschreiben.

## 8. Reproduzierbarkeit / Sicherheit

Die genannten Größen, Hashes, ASCII-Treffer und Bytekontexte stammen aus den unveränderten ZIP-Mitgliedern. Es wurde keine TOKEN.DB geschrieben oder verändert, keine GEOS.INI geändert, kein Provider installiert und kein Laufzeittest ausgeführt. Diese Untersuchung ist statische Dateianalyse, keine Bestätigung des tatsächlichen GeoManager-Ladeverhaltens.
