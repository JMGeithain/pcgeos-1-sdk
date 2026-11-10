# GEOTEST – GeoWorks-1.2-Kernel-Bestand und VM-Datei-Recherche (2381)

Stand: 2026-11-10

## Ziel / Abgrenzung

Untersuchung ausschließlich GeoWorks / PC/GEOS 1.x. Ziel ist die native Dokumenterzeugung in `GEOTEST.GEO` mit eigenem Dokument-Icon. Keine Grafiktreiberentwicklung. Keine Originaldateien wurden geändert.

## 1. Kerneldateien aus dem Installationsarchiv

Aus `GEOWORKS.zip` wurden read-only extrahiert:

| Datei | Größe | SHA-256 | Einordnung |
|---|---:|---|---|
| `GEOWORKS/KERNEL.EXE` | 72.736 Bytes | `c2cc8952cdb01d0f459bf281ee3b78f8ce9464aba0b58c3758f8c73e24fb6eb5` | gepatchte Kerneldatei laut bisher dokumentierter Provenienz |
| `GEOWORKS/KERNEL.OLD` | 72.688 Bytes | `bd4d680b15f8dd66b2b09b506de96672972f716a11e0a38220477bf07b6c1e9b` | ursprüngliche deutsche Kerneldatei laut bisher dokumentierter Provenienz |

Beide Dateien beginnen mit einer DOS-MZ-Kennung. Die MZ-Kopfwerte wurden direkt aus den ersten 28 Bytes gelesen:

### KERNEL.EXE

- MZ-Signatur: `4D 5A`
- Headergröße: 96 Absatz-Einheiten = 0x600 Bytes
- Relocation-Einträge: 276
- Initialer CS:IP: `0000:02B1`
- Initialer SS:SP: `0E34:15F0`
- Ladebildgröße nach MZ-Header: 71.200 Bytes

### KERNEL.OLD

- MZ-Signatur: `4D 5A`
- Headergröße: 96 Absatz-Einheiten = 0x600 Bytes
- Relocation-Einträge: 273
- Initialer CS:IP: `0000:02B1`
- Initialer SS:SP: `0E35:15B0`
- Ladebildgröße nach MZ-Header: 71.152 Bytes

Die Dateien unterscheiden sich in Größe und MZ-Metadaten. Die Unterschiede sind mit der bekannten unterschiedlichen Provenienz vereinbar; aus den MZ-Kopfwerten allein lässt sich aber keine bestimmte VM-Funktion ableiten.

## 2. String- und Token-Suche

In beiden Kerneldateien wurden nach den ASCII-Zeichenfolgen `WDAT`, `DDAT`, `WP00`, `DP00`, `VMOpen`, `VMCreate` und `VMSetMapBlock` gesucht. Keine dieser Zeichenfolgen ist vorhanden.

Der ASCII-String `document` ist in beiden Dateien vorhanden:
- KERNEL.EXE: Dateioffset `0EE66h`
- KERNEL.OLD: Dateioffset `0EE76h`

Der Kernel enthält außerdem diverse Status-/Subsystemtexte. Diese Strings sind keine symbolische API-Tabelle und reichen nicht aus, um die VM-Aufrufe oder die Headerinitialisierung zu identifizieren.

## 3. Technische Grenze dieser Untersuchung

Die MZ-Datei ist kein gewöhnliches DOS-Programm, dessen exportierte Funktionsnamen aus einem Standard-Importverzeichnis abgelesen werden könnten. In den vorliegenden Dateien sind keine lesbaren VM-Funktionsnamen oder Dokument-Tokens vorhanden.

Ein einfacher ASCII-String-Scan ist deshalb kein Ersatz für:
- das korrekte Rekonstruieren der MZ-Ladeadresse und Relocations,
- die Segment-/Ressourcenstruktur des GEOS-Kernels,
- die Analyse der internen Dispatcher-/Systemcalltabellen,
- die Zuordnung der VM-Routinen zu ihren tatsächlichen Einsprungpunkten.

Es wäre nicht belastbar, aus dem Wort `document` oder aus beliebigen Codebytes einen VM-Datei-API-Aufruf zu behaupten. In dieser Untersuchung wurde daher noch kein Kernel-Einsprungpunkt als VMOpen/VMCreate o.ä. etikettiert.

## 4. Nächster sinnvoller Analyseweg

Der nächste Schritt soll nicht durch blindes Disassemblieren der gesamten Kerneldatei erfolgen. Stattdessen wird die Referenzkette aus den Anwendungen und Systembibliotheken eingegrenzt:

1. Ressourcen-/Importtabellen von `WRITE.GEO` und `DRAW.GEO` vollständig erfassen.
2. System-Geodes aus derselben Installation untersuchen, insbesondere `KLIB.GEO`, `UI.GEO`, `STREAM.GEO` und `SPOOL.GEO`, auf VM-/Datei-/Dokument-bezogene Imports und Protokolle.
3. Die GeoWorks-1.x-Kernel-/Geode-ABI aus dem tatsächlichen Import-/Exportformat und vorhandenen Dispatchertabellen rekonstruieren.
4. Die Codepfade in WRITE.GEO verfolgen, die den neuen Dokumentzustand erzeugen und die VM-Datei öffnen/schreiben.
5. Die Headerfelder der echten `TESTWRIT.000`- und `TESTDRAW.000`-Dateien erst dann semantisch benennen, wenn sie mit den tatsächlichen Schreib-/Leseroutinen verbunden sind.
6. Die Icon-/Monikerzuordnung separat über GeoManager-/UI-Ressourcen belegen.

## 5. Status

- KERNEL.EXE und KERNEL.OLD im Originalarchiv identifiziert, extrahiert und gehasht.
- MZ-Kopfmetadaten beider Varianten erfasst.
- Die erwarteten Dokumenttokens und VM-API-Namen sind nicht als ASCII-Strings im Kernel enthalten.
- Noch keine VM-API-Routine identifiziert.
- Noch kein nativer GEOTEST-Dokumentkopf implementiert.
- Keine Originaldatei geändert; kein Laufzeiterfolg behauptet.
