# GEOTEST – verbindliche Projektkorrektur: eigenes GEOS-Dokument, kein GeoWrite-Format

Stand: 2026-11-12

## 1. Verbindliche Zieldefinition

Das Ziel bleibt eine native GeoWorks / PC/GEOS-1.x-Anwendung `GEOTEST.GEO`, die ein **eigenes GEOTEST-Dokument** erzeugen und verwalten kann. Dieses Dokument soll im GeoManager mit einem eigenen Dokument-Icon erscheinen.

Nicht erforderlich ist, dass das Dokument von GeoWrite geöffnet oder bearbeitet werden kann. Es wird **kein GeoWrite-kompatibles `WDAT/WP00`-Dokument** gebaut. Die Untersuchungen der GeoWrite-Text-, RunArray- und Seitenobjektstrukturen (Untersuchungen 2395–2418) sind für das GEOTEST-Ziel nicht mehr Voraussetzung und werden als separates Archivwissen behandelt.

## 2. Was „eigenes Dokument“ hier bedeutet

GEOTEST bekommt ein eigenes, anwendungsspezifisches Datenformat. Die Anwendung selbst ist für Erzeugen, Öffnen, Speichern, Schließen und erneutes Öffnen dieser Dateien verantwortlich.

Das Dateiformat muss ein gültiges GEOS-1.x-Datenfile sein, dessen Header die GEOS-Dateisignatur, einen eigenen vier Zeichen langen Dateityp und den Creator der GEOTEST-Anwendung trägt. Die exakten Typ-/Creator-Werte und das konkrete VM-/Dateiformat werden erst festgelegt, wenn sie gegen die originale GeoWorks-1.2-Implementierung geprüft sind. Es wird nicht ungeprüft `GTD1`, `.GTD` oder ein beliebiger Headerwert übernommen.

Das eigene Dokument-Icon ist getrennt vom Anwendungsicon zu behandeln:
- Anwendungsgeode: Token `GTS1`, Manufacturer ID 0.
- Dokumentdateityp: eigener vierstelliger Typcode, noch festzulegen.
- Icon-Zuordnung: historischer GeoWorks-1.x-Icon-Provider-/`filenameTokens`-Mechanismus, noch in einer Testumgebung zu validieren.

## 3. Gesicherter Stand des bestehenden GEOTEST

Die vorhandene `GEOTEST.GEO`:
- Dateigröße 70.794 Byte.
- SHA-256 `9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b`.
- App-Token `GTS1`.
- enthält ein natives Hauptfenster, GenView, Maus-/Tastatur-Callbacks und einen Help-Dialog.
- wurde vom Nutzer am 09.11.2026 in GeoWorks 1.2 gestartet; Hauptfenster und Help-Dialog sind im Laufzeittest bestätigt.

Der bisherige Quellcode `examples/geotest/src/app.c` enthält nur Fensterzeichnung, Klickzähler und Enter-Tastenbehandlung. Er enthält noch keine Dateierzeugung, kein Öffnen, Speichern oder Schließen eigener GEOTEST-Dokumente. Der Buildbericht bestätigt, dass diese Funktionen nicht implementiert sind.

## 4. Bereits gesicherte Grundlagen für das Dokument-Icon

Die originale GeoWorks-1.2-Dokumentation `GEOWORKS/ICONS/ICONINST.TXT` beschreibt kleine Icon-Provider-Geodes. Deren Dateinamensstamm ist der vierstellige Tokenname; die Beispielzuordnungen in `GEOS.INI` verwenden Manufacturer ID 255. Die Datei `DOS_ICON.TXT` dokumentiert außerdem die GEOS-Dateikopffelder:
- Dateityp bei Offset `0x14`;
- Creator bei Offset `0x1A`;
- langer Dateiname ab Offset `0x20`.

Die Beispieldateien `PAPR.000`, `GDOC.000` und `NBAT.000` sind Provider-Geodes; `TESTICON.000` ist dagegen eine Daten-Datei mit Typ `Icon` und Creator `GEOS`. Provider-Geode und Dokumentdatei sind daher zwei verschiedene Rollen.

Die Farb- und Monochrom-Entwürfe für das GEOTEST-Dokumenticon liegen als 48×30-PCX/PNG-Eingaben vor. Sie sind noch nicht als vollständige, in GeoManager bestätigte Dokument-Icon-Registrierung abgenommen.

## 5. Neuer Arbeitsplan

### A. Dateityp- und Providerpfad verifizieren
1. Originale `PAPR.000` und `GDOC.000` statisch vergleichen.
2. Das genaue Zusammenspiel aus Dateityp, Creator, Provider-Token und `filenameTokens`-Mapping nachweisen.
3. Einen GEOTEST-spezifischen Typcode und Provider-Token erst danach festlegen.
4. Farb-/Monochrom-Icon mit dem originalen GeoWorks-1.x-`ICONMAKE` erzeugen und in einer getrennten Testinstallation prüfen.

### B. Eigenes GEOTEST-Dokumentformat implementieren
1. Festlegen, ob das Dokument als GEOS-VM-Datei oder in einem anderen durch GeoWorks 1.x unterstützten Datencontainer gespeichert wird.
2. Native Kernel-/VM-Datei-APIs aus dem exakten GeoWorks-1.2-Ziel validieren.
3. Minimales eigenes Dokument mit GEOS-Header, GEOTEST-Dateityp, Creator und einfacher Nutzdatenstruktur erzeugen.
4. Öffnen, Speichern, Schließen und erneutes Öffnen implementieren.

### C. GEOTEST-Anwendung erweitern
1. Vorhandenes, bereits gestartetes `GEOTEST.GEO` als Basis verwenden.
2. Menü-/Befehle für Neu, Öffnen, Speichern und Schließen ergänzen.
3. Dokumentzustand und Fehlerfälle behandeln.
4. Dokument-Icon-Provider und Dateitypzuordnung anbinden.

### D. Test und Abnahme
Erfolgskriterien:
- GEOTEST startet in GeoWorks 1.2.
- GEOTEST erzeugt ein eigenes Dokument.
- Das Dokument erscheint im GeoManager mit dem vorgesehenen eigenen Icon.
- GEOTEST kann das Dokument wieder öffnen, ändern und speichern.
- Nach Schließen und erneutem Start bleibt das Dokument lesbar.
- Anwendungstoken `GTS1` und Dokumenttyp/Provider sind getrennt und konfliktfrei.

## 6. Ausdrückliche Nicht-Ziele

- Kein GeoWrite-`WDAT`-Dokumentformat.
- Keine GeoWrite-Seitenobjekte, VisText-RunArrays oder GeoWrite-Textcodierung.
- Keine Kompatibilität mit GeoWrite oder GeoDraw.
- Keine PC/GEOS-2.x-/FreeGEOS-Übernahme.
- Keine Änderung der Originalinstallation oder produktiven `TOKEN.DB` ohne getrennte Sicherung und ausdrücklichen Testplan.

## 7. Nächster konkreter Arbeitsschritt

Untersuchung 2419 wird nicht mehr an GeoWrite-Seitenrelokationen fortgesetzt. Sie beginnt mit dem Vergleich der originalen Icon-Provider-Geodes `PAPR.000` und `GDOC.000` sowie der dazugehörigen `ICONINST.TXT`-Zuordnungen. Parallel wird die GeoWorks-1.2-VM-/Datei-API für das eigene GEOTEST-Datenformat ermittelt.

Die vorhandene GEOTEST-GEO bleibt unverändert, bis ein nachvollziehbarer Implementierungsplan vorliegt.
