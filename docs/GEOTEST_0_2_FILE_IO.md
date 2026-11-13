# GEOTEST 0.2 – experimenteller Dateizugriff

**Zielprofil:** deutsches GeoWorks 1.2.8 / ausschließlich PC/GEOS 1.x  
**Arbeitszweig:** `geotest-0.2-fileio-prototype`  
**Status:** Quellprototyp angelegt; Build und Live-Test stehen noch aus.

## Testablauf

Beim Klick in den Anwendungsbereich oder bei Enter versucht GEOTEST:

1. `TEST.GTD` mit dem Kernel-Dienst `FileCreate` neu anzulegen.
2. Einen kurzen Datensatz mit Kennung `GTD1` zu schreiben.
3. Das Handle mit `FileClose` zu schließen.
4. Die Datei mit `FileOpen` erneut zu öffnen.
5. Den Datensatz mit `FileRead` vollständig einzulesen.
6. Das Dateiende durch einen zusätzlichen Ein-Byte-Leseversuch zu prüfen.
7. Die eingelesenen Bytes mit dem ursprünglichen Datensatz zu vergleichen.
8. Das Handle zu schließen und das Ergebnis im GEOTEST-Fenster anzuzeigen.

## Sicherheitsverhalten

- `FileCreate` wird als Neuanlage verwendet; ein existierender Dateiname wird nicht absichtlich überschrieben.
- Existiert `TEST.GTD` bereits, bricht der Test ab. Die Datei muss für einen weiteren Durchlauf manuell entfernt werden.
- Bei einem Schreib-, Lese- oder Schließfehler wird der Test abgebrochen.
- Die Testdatei wird nach erfolgreichem Test nicht gelöscht, damit sie außerhalb von GeoWorks untersucht werden kann.

## Implementierungsquelle

Der Adapter in `runtime/native.S` und die C-Wrapper in `runtime/sdk_runtime.c` folgen dem fortgeschrittenen MiniCalc-Referenzcode. Die Kernel-Aufrufnummern sind aus dieser Referenz übernommen. Der im vorigen Schritt festgestellte byteidentische Kernelstand ist ein Kompatibilitätsindiz, aber noch kein Ersatz für den Laufzeittest.

## Grenzen

- `TEST.GTD` ist ein privates GEOTEST-Testformat, kein natives GeoWorks-Dokument.
- Es gibt noch keinen nativen Öffnen-/Speichern-Dialog.
- Es gibt noch kein eigenes Dokument-ICON.
- Ein erfolgreicher Host-Build oder ein modellierter Instruktionstest belegt nicht, dass die Kernelaufrufe im laufenden GeoWorks korrekt funktionieren.
- Vor einem Build sind die ABI-Argumentübergabe, die Linker-Relokationen für `native_file` und der Stackpfad zu prüfen.

## Abnahmekriterien

- Build ohne neue Relokations- oder Linkerfehler.
- GeoWorks 1.2.8 lädt GEOTEST.GEO.
- Ein erster Testlauf erzeugt TEST.GTD.
- Ein zweiter Lauf ohne Löschen wird mit „existiert bereits“ abgebrochen und lässt die Datei unverändert.
- Nach manuellem Entfernen wird die Datei neu angelegt und die Byteprüfung meldet Erfolg.
- Die Datei ist nach Beenden von GeoWorks weiterhin vorhanden und enthält den erwarteten GTD1-Datensatz.
