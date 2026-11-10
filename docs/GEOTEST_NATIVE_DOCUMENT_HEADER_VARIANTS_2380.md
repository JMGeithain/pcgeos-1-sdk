# GEOTEST – Variantenanalyse nativer Dokumentköpfe (2380)

Stand: 2026-11-10

## Umfang

Fortsetzung der Untersuchung nativer GeoWorks-1.x-Dokumente aus `GEOWORKS.zip`. Read-only; keine Änderungen an Originaldateien. Ziel bleibt GEOTEST mit eigenem nativen Dokument und eigenem Icon.

## 1. Archivweite Tokenzählung

Alle regulären ZIP-Dateieinträge wurden auf den GEOS-Dateikopf `C7 45 CF 53` geprüft. Für Einträge mit den Feldern bei Offset `0014h` und `001Ah` ergab sich:

| Typ-Token | Creator-Token | Anzahl ZIP-Einträge |
|---|---|---:|
| `WDAT` | `WP00` | 303 |
| `DDAT` | `DP00` | 297 |

Die Zahlen sind **Eintragszahlen im Archiv**, keine Zahl garantiert eindeutiger Dokumente. Das Archiv enthält Duplikate und Kopien in verschiedenen Verzeichnissen. Die breite Verteilung über zahlreiche Verzeichnisse und Dokumentnamen belegt jedoch, dass beide Paare nicht nur in zwei speziell ausgewählten Testdateien vorkommen.

Andere im Archiv gefundene GEOS-Dateitypen haben ebenfalls ein Tokenpaar an diesen Positionen, beispielsweise `Icon/GEOS`, `scbk/Scrp` und `adbk/ADBK`. Das stützt die Interpretation als allgemeine Typ-/Creator-Felder des GEOS-Dateikopfes. Die exakten historischen Feldnamen müssen weiterhin anhand einer passenden GeoWorks-1.x-Definition oder Kernelroutine bestätigt werden.

## 2. Stabile und variable Headerbereiche

Für alle gefundenen `WDAT/WP00`- und `DDAT/DP00`-Einträge gilt in den geprüften Beispielen:

- Bytes `00h–03h`: GEOS-Kennung `C7 45 CF 53`.
- Bytes `14h–17h`: Typ-Token.
- Bytes `18h–19h`: Nullbytes.
- Bytes `1Ah–1Dh`: Creator-Token.
- Bytes `1Eh–1Fh`: Nullbytes.
- Ab Offset `20h`: lesbarer Dokumentname, nullterminiert.

Der Bereich vor den Tokenfeldern ist nicht durchgehend konstant. Auch mehrere 16-Bit-Werte in den Bytes `08h–0Fh` unterscheiden sich zwischen Dokumenten. Daraus folgt: Für einen gültigen GEOTEST-Dateikopf reicht es nicht, nur die ersten vier Bytes und die beiden Tokenpaare zu kopieren. Die übrigen Felder können Versions-, Format- oder VM-Dateimetadaten enthalten; ihre genaue Bedeutung ist noch nicht zugeordnet.

## 3. Beispielvergleich

`TESTWRIT.000`:
- GEOS-Kennung: `C7 45 CF 53`
- Typ/Creator: `WDAT/WP00`
- Name: `testwrite`
- Größe: 2.752 Bytes

`TESTDRAW.000`:
- GEOS-Kennung: `C7 45 CF 53`
- Typ/Creator: `DDAT/DP00`
- Name: `TestDraw`
- Größe: 880 Bytes

Beide Dateien wurden im Archiv gefunden und byteweise aus dem ZIP gelesen. Die vollständigen Hashes stehen in Untersuchung 2379.

## 4. Bedeutung für GEOTEST

Der Headervergleich liefert jetzt einen belastbaren Weg für die spätere Dokumentregistrierung:
- eigenes Dokumenttyp-Token für GEOTEST,
- Creator-Token passend zum GEOTEST-App-Token `GTS1`,
- Dokumentname im Namensfeld ab `0020h`,
- weitere Headerfelder müssen aus der echten GeoWorks-1.x-Dateierzeugung übernommen werden, nicht geraten.

Es wird weiterhin **kein frei gewähltes Token in einen Build geschrieben**. Das konkrete GEOTEST-Dokumenttoken und die übrigen Headerwerte werden erst festgelegt, wenn die Schreib-/Erzeugungsroutinen oder eine vollständige, validierte 1.x-Dateikopfdefinition identifiziert sind.

## 5. Suche nach SDK-Definitionen

Eine Suche im aktuellen Repository `JMGeithain/pcgeos-1-sdk` nach `VMFileHeader`, `VMOpen`, `VMCreate`, `VMSetMapBlock`, `FileCreate` und `FileOpen` ergab keine Treffer. Daraus lässt sich nur ableiten, dass das aktuelle Repository keine entsprechend indizierten Definitionen bereitstellt; es ist kein Beleg für das Fehlen solcher APIs im historischen GeoWorks-System.

## 6. Nächste Schritte

1. Die relevanten GeoWorks-1.2-Kernel-/VM-Dateiroutinen im tatsächlichen Kernel und in den Bibliotheks-Geodes identifizieren.
2. Aus den Codepfaden herauslesen, welche Headerfelder beim Erzeugen einer neuen GeoWrite-Datei initialisiert werden.
3. Die Lese-/Schreibpfade der VM-Map-Block-/Dokumentdaten ermitteln.
4. Separat verfolgen, wie GeoManager aus Typ-/Creator-Token und App-Ressourcen das Dokument-Icon auswählt.
5. Erst danach eine GEOTEST-Datei erzeugen und im echten GeoWorks 1.2 testen.

## Status

- 303 ZIP-Einträge mit `WDAT/WP00`, 297 mit `DDAT/DP00` gezählt.
- Tokenfelder und Dokumentnamensbereich in den Beispielen bestätigt.
- Variable Headerfelder festgestellt; ihre Semantik ist offen.
- Vollständige Dateierzeugung, VM-Header-Initialisierung und Icon-Zuordnung noch nicht nachgewiesen.
- Keine Originaldatei geändert; kein GEOTEST-Build erstellt; kein Laufzeiterfolg behauptet.
