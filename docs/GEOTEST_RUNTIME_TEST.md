# GEOTEST 1.0 – Laufzeittest in GeoWorks 1.2

**Testdatum:** 09.11.2026  
**Projekt:** [pcgeos-1-sdk](https://github.com/JMGeithain/pcgeos-1-sdk)  
**Anwendung:** `examples/geotest/` → `GEOTEST.GEO`  
**Build-SHA-256:** `9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b`  
**Dateigröße:** 70.794 Bytes

## Ergebnis

Der Nutzer hat die erzeugte Anwendung in seiner GeoWorks-1.x-Umgebung gestartet und einen Screenshot des laufenden Programms übermittelt. Die Rückmeldung lautete: **„es geht alles.“**

Im Screenshot sichtbar:

- GeoWorks-Arbeitsoberfläche und Programmfenster „GeoWorks 1.x Test“;
- Hauptfenster mit schwarzem View-Bereich;
- Befehl „Help…“;
- nativer Dialog „Help for GeoWorks 1.x Test“;
- erwarteter Hilfetext „GEOTEST“, „Minimal GeoWorks 1.x SDK test application.“ und „Click the view or press Enter to exercise an application callback.“;
- Schaltflächen „Page Up“, „Page Down“ und „Close“.

Damit sind Laden/Starten der Anwendung, Anzeige des Hauptfensters und Öffnen/Anzeigen des Help-Dialogs im Zielsystem visuell bestätigt.

## Grenzen des Belegs

Der Screenshot dokumentiert einen geöffneten Help-Dialog. Er belegt nicht einzeln die Funktionsweise jedes Tastatur-, Maus- oder Schließpfades. Obwohl der Nutzer den Gesamttest mit „es geht alles“ bestätigt hat, sollen folgende Punkte für eine belastbare Regressionstestmatrix separat geprüft werden:

- Klick in den View-Bereich;
- Enter-Taste;
- Page Up / Page Down;
- Close des Help-Dialogs;
- Close der Hauptanwendung und Rückkehr zum GeoManager;
- Redraw nach Überdeckung sowie erneutes Öffnen.

Die genaue Build-/Kernelvariante der Testumgebung und deren Hash lassen sich aus dem Screenshot nicht sicher bestimmen.

## Lizenz- und Distributionshinweis

Die aus dem GeoWorks-Zielarchiv übernommenen UI-Templatebytes können proprietärem Material entstammen. Deshalb wird die abgeleitete Binärdatei `GEOTEST.GEO` nicht in dieses öffentliche Repository aufgenommen. Eingecheckt werden Quellprojekt, Buildanleitung, Prüfmetadaten und Testdokumentation. Für einen eigenen Build ist eine rechtmäßig vorhandene GeoWorks-1.x-Zielinstallation erforderlich.

## Verwandte Dokumentation

- [Vollständiges GEOTEST-Entwicklungsprotokoll](GEOTEST_DEVELOPMENT_LOG.md)
- [SDK-Einstieg](GETTING_STARTED.md)
- [Zielkompatibilität](TARGET_COMPATIBILITY.md)
