# GEOTEST – Untersuchung 2486
## Aufrufer des Dokument-Prüf- und Initialisierungspfads im GeoWorks-1.x-Kernel

**Stand:** 12.11.2026  
**Primärquelle:** `GEOWORKS/KERNEL.OLD` aus `GEOWORKS.zip`  
**Zielprofil:** ausschließlich GeoWorks / PC-GEOS 1.x

## 1. Ziel

Nach Untersuchung 2485 werden die direkten Aufrufer der Kernelroutinen bei Dateioffset `0xB62D` (Dateistrukturprüfung) und `0xB6D5` (FB00-Strukturinitialisierung) verfolgt.

## 2. Primärquellendaten und Adresskonvention

- Datei: `GEOWORKS/KERNEL.OLD`
- Dateigröße: 72.688 Bytes
- MZ-Header: `0x600` Bytes
- Disassemblierung: 8086-Modus, Rohdatei mit Dateioffsets als Adressen.

Die relativen CALL-Ziele sind bei dieser Betrachtung korrekt, weil Quell- und Zieladresse denselben konstanten MZ-Header-Offset enthalten. Es handelt sich um statische Disassemblierung; kein Laufzeit-Tracing.

## 3. Direkte CALL-Xrefs

Die Suche nach 8086-near-CALL-Instruktionen (Opcode `E8`, signed `rel16`) ergibt:

- Ziel `0xB62D`: Aufrufstellen `0xA9CE` und `0xB775`.
- Ziel `0xB6D5`: Aufrufstelle `0xAAAA`.

Die Aufrufstelle `0xB775` liegt innerhalb der Kernelroutine bei `0xB76F`. Die Aufrufstelle `0xA9CE` liegt innerhalb der Routine ab `0xA97B`. Die Initialisierung `0xB6D5` wird im übergeordneten Ablauf unmittelbar nach `0xB17D` und vor `0xB305` aufgerufen.

## 4. Übergeordneter Ablauf ab 0xA97B

Die Routine ab Dateioffset `0xA97B` wird direkt aus `0xAE36` aufgerufen. Der Aufrufer beginnt bei `0xAE25` und sichert unter anderem AH, BX, DS, ES, SI und DI. Am Einstieg `0xAE31` wird AH in eine lokale Variable gespeichert. Danach ruft der Aufrufer `0xA97B` auf. Nach erfolgreicher Rückkehr wird der weitere Ablauf fortgesetzt.

Das belegt eine gemeinsame übergeordnete Kerneloperation, erlaubt für sich allein aber noch keine eindeutige symbolische Benennung als „VMOpen“, „VMCreate“ oder ähnliches.

## 5. Zwei Pfade innerhalb 0xA97B

### 5.1 Vorhandene Datei / Validierungspfad

Bei `0xA9CE` ruft der Code `0xB62D` auf. Der relevante Ablauf lautet:

- `0xA9CA`: DS sichern.
- `0xA9CB`: `0xB17D` aufrufen.
- `0xA9CE`: `0xB62D` aufrufen (Dateikopf-/Zielblockprüfung).
- `0xA9D1`: DS wiederherstellen.
- `0xA9D2`: `0xB305` aufrufen.
- Anschließend entscheidet der Code anhand des Carry-Flags über den weiteren Fehler-/Erfolgspfad.

Damit wird die in Untersuchung 2485 analysierte Strukturprüfung in einem übergeordneten Dateiablauf tatsächlich verwendet.

### 5.2 Initialisierungs-/Neuanlagepfad

Bei `0xAAAA` ruft der Code `0xB6D5` auf. Der relevante Ablauf:

- `0xAAA7`: `0xB17D` aufrufen.
- `0xAAAA`: `0xB6D5` aufrufen (FB00-Strukturinitialisierung).
- `0xAAAD`: `0xB305` aufrufen.
- `0xAAB0`: DS wiederherstellen.
- `0xAAB1/AAB2`: Rückgabestatus wird auf Erfolg gesetzt.
- `0xAAB3`: `0xB319` aufrufen.

Der Initialisierungspfad ist damit in einen größeren Kernelablauf eingebettet und wird nicht als isolierte Hilfsfunktion aufgerufen.

## 6. Routine 0xB76F

Eine weitere Routine ab `0xB76F` ruft zunächst `0xB62D` auf (CALL bei `0xB775`). Danach folgen unter anderem Aufrufe bei `0xB77E` und `0xB781` sowie das Setzen von Feldern in einer internen Struktur. Dies ist ein weiterer Pfad, der die Dokumentstrukturprüfung vor einer nachfolgenden Verarbeitung ausführt. Die genaue Funktion dieses Pfades bleibt offen.

## 7. Bedeutung für die Dokumenterzeugung

Die neuen Aufrufstellen belegen:

- Der Kernel prüft die Datei-/Dokumentstruktur in einem konkreten übergeordneten Dateiablauf.
- Derselbe übergeordnete Ablauf enthält einen Pfad, der die FB00-Struktur initialisiert.
- Nach der Initialisierung folgen weitere Kernelroutinen (`0xB305` und `0xB319`), die für das vollständige Anlegen/Registrieren/Abschließen der Operation relevant sein können.
- Der bloße Aufruf `0xB6D5` erzeugt daher nicht nachweislich eine vollständige, auf Datenträger gespeicherte GeoWorks-Dokumentdatei.

## 8. Offene Punkte

- Semantische Namen des Ablaufs ab `0xA97B` und seines Aufrufers ab `0xAE25`.
- Rolle und Parameter von `0xB17D`, `0xB305` und `0xB319`.
- Welche Kernelroutine tatsächlich die Headerbytes und den FB00-Block auf Datenträger schreibt.
- Ob das übergeordnete Verfahren eine VM-Datei, eine andere strukturierte Datei oder einen Kernel-internen Dokumentcontainer verwaltet.
- Welche Anwendungs-API GeoWrite/GeoDraw zum Start dieses Pfades verwenden.

## 9. Konsequenz für GEOTEST

Noch keine eigene Dokumentdatei direkt erzeugen. Die belastbare nächste Aufgabe ist, die Aufrufketten von `0xB17D`, `0xB305` und `0xB319` zu verfolgen und die Datei-I/O-Aufrufe darunter zu identifizieren. Parallel müssen die Exporte/Imports und Aufrufstellen in GeoWrite/GeoDraw ausgewertet werden, um den öffentlichen oder anwendungsseitigen Einstieg zu finden. Keine Zuordnung zu PC/GEOS 2.x-VM-APIs vornehmen.

## 10. Nächster Schritt 2487

Die Routinen `0xB17D`, `0xB305` und `0xB319` sowie ihre direkten Aufrufer und Rückgabeverträge untersuchen. Ziel ist, den letzten Schritt vom internen FB00-Objekt zur tatsächlich geschriebenen Dokumentdatei nachzuweisen.

## 11. Grenzen

Statische Analyse der Originaldatei `KERNEL.OLD`. Die CALL-Xref-Suche erfasst direkte near-CALLs (`E8 rel16)); indirekte Aufrufe über Tabellen/Funktionszeiger sind damit nicht ausgeschlossen oder vollständig erfasst. Keine dynamische Ausführung, keine Änderung an `GEOWORKS.zip`, kein Laufzeittest und keine neue `GEOTEST.GEO`.
