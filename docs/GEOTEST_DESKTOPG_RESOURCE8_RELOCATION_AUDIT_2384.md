# GEOTEST – DESKTOPG.GEO Ressource 8: Relocation-Prüfung der Dateiverwalter-Schleife (2384)

Stand: 2026-11-10

## Ausgangspunkt

Untersucht wird weiterhin ausschließlich GeoWorks / PC/GEOS 1.x. In Untersuchung 2383 wurden in `DESKTOPG.GEO`, Ressource 8, die Dateiverwalter-Schlüsselwörter und eine Schleife mit zwei Far-Calls bei Ressourcenoffsets `0516h` und `052Ah` gefunden.

Originaldatei:
- `GEOWORKS/SYSAPPL/DESKTOPG.GEO`
- 101.524 Bytes
- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`

## 1. Tabellenstruktur des Geode-Headers

Die Ressourcentabelle enthält 51 Einträge. In dieser Datei liegen:
- 51 Ressourcen-Dateioffsets ab `01D0h` (4 Bytes pro Eintrag),
- die zugehörigen Relocation-Bytezahlen ab `029Ch` (2 Bytes pro Ressource),
- die Ressourcenflags ab `0302h` (2 Bytes pro Ressource),
- erster Ressourceninhalt ab `0368h`.

Für Ressource 8:
- Dateioffset: `56FCh`
- Ende / nächster Ressourcenoffset: `5FACh`
- Gesamtbereich: 2.224 Bytes
- Relocation-Bytezahl aus Tabelle: `0150h` = 336 Bytes
- Ressourcenflags: `0A72h`

Die 336 Bytes am Ende des Ressourcenbereichs bilden 84 Vier-Byte-Relocation-Einträge. Der Code-/Datenbereich davor ist damit 1.888 Bytes lang und reicht bis Ressourcenoffset `075Fh`.

## 2. Die zwei Far-Calls und ihre Segmentfelder

Die in Untersuchung 2383 gefundenen Instruktionen lauten:

| Ressourcenoffset | Dateioffset | Bytes | Disassemblierung |
|---:|---:|---|---|
| `0516h` | `5C12h` | `9A 72 00 00 00` | `CALL FAR 0000:0072h` |
| `052Ah` | `5C26h` | `9A 71 00 00 00` | `CALL FAR 0000:0071h` |

Beim 8086-Far-Call stehen nach dem Opcode `9A` zuerst der 16-Bit-Offset und danach das 16-Bit-Segment. Die Segmentwörter befinden sich daher an Ressourcenoffsets:
- erster Call: `0519h`
- zweiter Call: `052Dh`

Die 84 Relocation-Einträge der Ressource wurden auf die tatsächlichen Segmentwortpositionen `0519h` und `052Dh` geprüft. Für keine dieser beiden Positionen ist ein Relocation-Eintrag vorhanden. Die zuvor genannten Positionen `0512h` und `0526h` waren um sieben Bytes verschoben.


### Dritter Aufruf aus der zweiten Token-Tabelle

Die zweite Schleife enthält außerdem `CALL FAR 0000:0073h` bei Ressourcenoffset `0581h` (Dateioffset `5C7Dh`). Das Segmentwort liegt bei `0584h`. Auch für `0584h` existiert kein Relocation-Eintrag in den 84 Einträgen von Ressource 8. Die Instruktionsbytes lauten `9A 73 00 00 00`.

## 3. Belastbare Aussage und Grenze

Bestätigt ist:
- Die drei Far-Calls stehen im Code-/Datenbereich der Ressource 8.
- Ihre Segmentwörter sind in der Rohdatei Null.
- Die drei tatsächlichen Segmentwortpositionen (`0519h`, `052Dh`, `0584h`) sind nicht in der Relocation-Liste dieser Ressource enthalten.
- Die Calls sind daher keine gewöhnlichen, durch diese Ressourcen-Relocationstabelle zu patchenden Segmentreferenzen.

Nicht bestätigt ist:
- ob die Offsets `0071h` und `0072h` feste Kernel-Einsprungpunkte, System-Call-Vektoren oder etwas anderes bezeichnen;
- welche konkrete Funktion jeder Call ausführt;
- ob sie direkt mit der Erkennung der GEOS-Typ-/Creator-Felder verbunden sind.

Die numerischen Offsets werden deshalb weiterhin nicht mit erfundenen API-Namen versehen.

## 4. Schleifenstruktur

Der Code lädt vor den Aufrufen Werte aus vier CS-relativen Tabellenadressen:
- `CS:[DI+0538h]`
- `CS:[DI+0544h]`
- `CS:[DI+0550h]`
- `CS:[DI+055Ch]`

Er initialisiert `DI=0`, verarbeitet die Werte, erhöht `DI` um zwei und vergleicht mit `000Ch`. Das entspricht sechs Iterationen über wortweise Tabelleneinträge. Die Datenbereiche liegen direkt hinter den Dateiverwalter-Strings in derselben Ressource.

Das ist ein nachgewiesener Tabellenverarbeitungsmechanismus. Die sechs Einträge sind noch nicht semantisch als Dokumenttypen, Dateiendungen oder Icon-IDs identifiziert.

## 5. Nächste Untersuchung

1. Die 84 Relocation-Einträge vollständig mit ihrer Typkodierung dekodieren und gegen andere Aufrufe im selben Codebereich vergleichen.
2. Die Geode-Import-/Exporttabelle und den UI-Import so weit rekonstruieren, dass echte importierte Bibliotheksaufrufe von festen Kernelvektoren unterschieden werden können.
3. Die sechs Tabelleneinträge ab `0538h` und die korrespondierenden Werte ab `0550h` als strukturierte Datensätze auswerten.
4. Den Pfad von Dateikopf-/Token-Erkennung zur Icon-/Monikerwahl weiterverfolgen.

## Status

Relocation-Längen-/Flags-Tabellen und Ressource-8-Relocationbereich ausgewertet. Keine Relocation an den Segmentworten der beiden Far-Calls gefunden. API-Semantik weiterhin offen. Keine Originaldatei geändert, kein GEOTEST-Build erstellt und kein Laufzeiterfolg behauptet.
