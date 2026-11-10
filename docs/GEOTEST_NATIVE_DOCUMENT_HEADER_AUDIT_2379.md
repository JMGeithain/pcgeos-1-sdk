# GEOTEST – Native Dokumentdateien im GeoWorks-1.2-Archiv: Header-Nachweis (2379)

Stand: 2026-11-10

## Ziel / Abgrenzung

Untersuchung ausschließlich GeoWorks / PC/GEOS 1.x. Ziel ist eine kleine native Testanwendung `GEOTEST.GEO`, die eigene native Dokumentdateien erzeugt, speichert, wieder öffnet und im GeoManager mit einem eigenen Dokument-Icon angezeigt wird.

Keine Treiberentwicklung. `NOTEPAD.GEO` ist wegen DOS-ASCII-Dateien keine Vorlage für native GEOS-Dokumente. Es wurden keine Originaldateien geändert.

## 1. Entscheidender Fund: echte Dokumentdateien

Im bereitgestellten `GEOWORKS.zip` liegen echte Dateien mit dem GEOS-VM-Dateikopf `C7 45 CF 53`, darunter:

| Archivpfad | Größe | Header-Typ bei 0014h | Creator bei 001Ah | Dokumentname ab 0020h |
|---|---:|---|---|---|
| `GEOWORKS/DOCUMENT/TESTWRIT.000` | 2.752 Bytes | `WDAT` | `WP00` | `testwrite` |
| `GEOWORKS/DOCUMENT/TESTDRAW.000` | 880 Bytes | `DDAT` | `DP00` | `TestDraw` |
| `GEOWORKS/DOCUMENT/DRAW_UNB.000` | 1.440 Bytes | `DDAT` | `DP00` | `Draw unbenannt` |
| `GEOWORKS/DOCUMENT/HANNES.000` | 2.608 Bytes | `WDAT` | `WP00` | `Hannes` |
| `GEOWORKS/BUCH/ASCII-KO.000` | 15.856 Bytes | `WDAT` | `WP00` | `ASCII-Konvertierung` |

Die ersten 32 Bytes von TESTWRIT.000:

```
C7 45 CF 53 01 00 00 00 01 00 02 00 08 00 03 00
01 00 00 00 57 44 41 54 00 00 57 50 30 30 00 00
74 65 73 74 77 72 69 74 65 00
```

Die ersten 32 Bytes von TESTDRAW.000:

```
C7 45 CF 53 01 00 00 00 01 00 02 00 08 00 02 00
01 00 01 00 44 44 41 54 00 00 44 50 30 30 00 00
54 65 73 74 44 72 61 77 00
```

Damit ist unmittelbar belegt: `WDAT` / `WP00` bzw. `DDAT` / `DP00` stehen im Dateikopf echter GeoWrite-/GeoDraw-Dokumentdateien. Die gleiche Kennungsfolge, die in den jeweiligen Geodes gefunden wurde, ist also Teil des nativen Dokument-Headers.

## 2. Bedeutung der beiden Tokenfelder

Die Zuordnung ist nun erheblich besser abgesichert:

- Feld bei Offset `0014h`: anwendungsspezifischer Dokument-/Dateityp-Token (`WDAT` für GeoWrite, `DDAT` für GeoDraw).
- Feld bei Offset `001Ah`: zugehöriger Creator-/Anwendungs-Token (`WP00` für GeoWrite, `DP00` für GeoDraw).

Diese Feldnamen beschreiben die beobachtete Zuordnung. Die exakten historischen Strukturbezeichner der GeoWorks-1.x-Headerdefinition sind noch nicht aus einer passenden 1.x-Headerdatei oder Kernelroutine belegt. Daher ist die Funktion als Typ-/Creator-Paar sehr stark belegt, während die originalen Symbolnamen noch offen sind.

Zusätzliche Evidenz:
- Die Tokenfelder stehen in echten, zahlreichen GeoWrite- und GeoDraw-Dokumentdateien.
- Die Creator-Tokens entsprechen den App-Tokens der jeweiligen Geodes.
- In den entsprechenden Objektressourcen der Geodes stehen die gleichen Paare.
- Im Archiv wurden 303 Einträge mit `WDAT/WP00` und 297 mit `DDAT/DP00` gezählt. Das sind ZIP-Einträge, keine garantiert eindeutigen Dokumente; Duplikate und verschiedene Verzeichnisse sind enthalten.

## 3. Abgrenzung: Icon-Dateien

Im Archiv existieren auch separate Icon-Dateien, z.B.:
- `GEOWORKS/DOCUMENT/TESTICON.000`
- `GEOWORKS/DOCUMENT/ALTESGEO.000`

Sie beginnen ebenfalls mit `C7 45 CF 53`, tragen aber bei Offset `0014h` den Typ `Icon` und bei `001Ah` den Creator `GEOS`. Ihr Name beginnt bei Offset `0020h`.

Das ist ein eigener Dateityp und nicht mit einem GeoWrite-Dokument gleichzusetzen. Dass Icon-Dateien existieren, beweist noch nicht, wie GeoManager einem neuen Dokumenttyp ein eigenes Icon zuordnet. Dafür muss der Icon-/Monikerpfad der Anwendung bzw. die Desktop-Zuordnung separat untersucht werden.

## 4. Hashes der zentralen Testdateien

- TESTWRIT.000, 2.752 Bytes, SHA-256: `5b47b33db34bfaf8e57e8f7285827a99b8ffcca5f7630e3fba5c83144ac66263`
- TESTDRAW.000, 880 Bytes, SHA-256: `8c4b99666610730c2b2fc69ade326b2053c5462eb27f5a3509be49e584338f71`
- DRAW_UNB.000, 1.440 Bytes; zusätzliches bestätigendes GeoDraw-Beispiel.
- HANNES.000, 2.608 Bytes; zusätzliches bestätigendes GeoWrite-Beispiel.

## 5. Konsequenz für GEOTEST

Der zentrale Unsicherheitsblock aus den Untersuchungen 2375–2378 ist teilweise aufgelöst: Die Tokenpaare sind keine bloßen UI-Strings, sondern erscheinen in den Dateiköpfen nativer GeoWrite-/GeoDraw-Dokumente.

Für GEOTEST brauchen wir entsprechend ein eigenes, vier Zeichen langes Dokumenttyp-Token und den Creator-Token `GTS1`. **Ein konkretes GEOTEST-Dokumenttoken wird noch nicht festgelegt**, bis die korrekte GEOS-1.x-Headerstruktur und die zugehörigen Erzeugungs-/Speicherroutinen aus dem Code nachgewiesen sind. Wir werden nicht einfach eine Datei durch Kopieren/Ersetzen der Headerbytes herstellen.

## 6. Nächste Untersuchung

1. Die ersten 64–128 Bytes mehrerer GeoWrite- und GeoDraw-Dateien vergleichen, um variable Headerfelder von stabilen Feldern zu trennen.
2. Headerfelder mit den VM-/Datei-API-Aufrufen in WRITE.GEO und DRAW.GEO verbinden.
3. Im GeoWrite-Code die Create/New-/Save-/Open-Pfade verfolgen und ermitteln, welche Kernel-/UI-Funktionen den Header schreiben und lesen.
4. Die Desktop-/GeoManager-Icon-Zuordnung getrennt untersuchen; insbesondere die Rolle der Icon-Dateien und der Monikerressourcen.
5. Danach erst die minimale GEOTEST-Dokumentstruktur definieren und unter GeoWorks 1.2 testen.

## Status

- Native GEOS-Dateikennung `C7 45 CF 53` in den Referenzdateien bestätigt.
- GeoWrite-Dokument-Tokenpaar `WDAT/WP00` in echten Dokumenten bestätigt.
- GeoDraw-Dokument-Tokenpaar `DDAT/DP00` in echten Dokumenten bestätigt.
- Feldpositionen 0014h / 001Ah und Name ab 0020h in den Beispielen bestätigt.
- Exakte historische Headerstrukturbezeichner, Schreib-/Leseroutinen und Icon-Zuordnung noch offen.
- Keine Originaldatei geändert, kein GEOTEST-Build erstellt, kein Laufzeiterfolg behauptet.
