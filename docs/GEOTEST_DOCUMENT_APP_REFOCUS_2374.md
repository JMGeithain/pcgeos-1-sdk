# GEOTEST – Fokus Test-App mit eigenem Dokument (2374)

Stand: 2026-11-10

## Verbindlicher Projektfokus

Das aktuelle Ziel ist **keine Entwicklung oder Anpassung eines Grafiktreibers**. Ziel ist eine native GeoWorks / PC/GEOS 1.x Test-Anwendung `GEOTEST.GEO`, die ein eigenes Dokument erzeugt bzw. anlegt und diesem Dokument ein eigenes Dateisymbol (Dokument-Icon) zuordnet.

Die SVGA-/Basebox-Treiberarbeiten aus anderen Untersuchungen sind für diesen Arbeitsschritt nicht Teil des Umfangs. Originaldateien und installierte Treiber bleiben unverändert.

## Was das neu gelieferte Basebox-SVGA-Ensemble für dieses Ziel enthält

Das Archiv enthält zusätzlich `colour-test/BCOLTEST.GEO`, eine kleine native GEOS-1.x-Testanwendung.

- Dateigröße: 4.000 Bytes
- SHA-256: `3e5d7a9cdb0ed5d506e5b79056b3f274a04e97b9b07845fd1c8d4fe99295dcac`
- Kernel-Protokoll: 622.3
- Geode-Protokoll: 1.0
- 11 Ressourcen
- ein Import: `ui`, Protokoll 693.0
- Ressourcen 3 und 4 sind LMem-Objektressourcen; Ressourcen 5 bis 10 sind weitere LMem-/Monikerressourcen.

Die mitgelieferte `colour-test/README.txt` sagt ausdrücklich, dass die Anwendung unmittelbar ihr natives Fenster öffnet und **kein Dokument und keinen Dateiauswahldialog** verwendet. Sie ist deshalb ein weiterer nativer App-/Fenster-Test, aber keine Vorlage für die Dokumenterzeugung. Ihre dokumentierte RGB565-Funktionalität ist für das aktuelle GEOTEST-Dokumentziel nicht erforderlich.

## Korrektur: NOTEPAD.GEO ist keine native GEOS-Dokumentvorlage

Der Nutzer hat klargestellt, dass `NOTEPAD.GEO` keine eigenen PC/GEOS-Dokumentdateien wie GeoWrite erzeugt oder verwaltet, sondern DOS-ASCII-Dateien bearbeitet. Diese Einordnung ist für das Projekt maßgeblich.

Die zuvor notierten Fakten zu `NOTEPAD.GEO` bleiben als Geode-Befunde gültig (8.070 Bytes, Kernel-Protokoll 622.3, 15 Ressourcen, Imports `ui` und `spool`, Dateiname `notiz.txt)). Sie belegen jedoch gerade keinen nativen GEOS-Dokument-Lifecycle. NOTEPAD darf daher nicht als Vorlage für das eigene GEOTEST-Dokumentformat oder dessen Icon-Registrierung verwendet werden. Allenfalls kann die Anwendung später als Referenz für allgemeine UI-/Dateiauswahlabläufe dienen.

## Neuer Referenzkandidat: GeoWrite

In der Installation liegt `GEOWORKS/WORLD/WRITE.GEO`, die native GeoWrite-Anwendung:

- Dateigröße: 73.110 Bytes
- SHA-256: `0d2958b810948603d15e412a61598623b9a4ccb73cfeb9fbe08d50ee718a6fd0`
- GEOS-1.x-Geode, Kernel-Protokoll 622.3
- Geode-Protokoll 509.0, Release 1.2.8.3
- 36 Ressourcen
- Imports: `ui` (693.0), `spool` (613.0), `spell` (2.0)
- Geode-Permanentname `write`, Extension `app`

Strings in WRITE.GEO belegen unter anderem die Anwendung GeoWrite und Funktionen zum Importieren bzw. Speichern von ASCII-Textdateien. Die Datei enthält viele Code- und Objektressourcen. Das macht sie zum deutlich besseren Kandidaten für die Untersuchung eines nativen Dokument-Lifecycles.

Noch nicht nachgewiesen sind:
- das konkrete native GeoWrite-Dateiformat,
- die Dokumentklasse und ihre Erzeugungs-/Speicheraufrufe,
- die genaue Dateityp-/Creator-Registrierung,
- die Referenzkette zum Dokument-Icon.

Auch WRITE.GEO wird deshalb zunächst nur statisch untersucht. Aus Ressourcenanzahl, Strings oder Importen allein wird keine Dokumentstruktur abgeleitet.

## Aktueller GEOTEST-Stand

Der bisherige `GEOTEST.GEO`-Build (SHA-256 `9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b`) ist eine minimale native Testanwendung mit Fenster, View, Zeichen-/Tastatur-Callbacks und Hilfedialog. Die dokumentierte Methodentabelle umfasst acht native Prozessmethoden.

Der bisherige Buildbericht kennzeichnet den Stand als experimentell und ohne GeoWorks-1.2-Laufzeittest. Er weist keine implementierte Dokumenterzeugung, kein Save/Save-As und keine bestätigte Dokumentdatei-Registrierung nach. Das Ziel „eigenes Dokument mit eigenem Icon“ ist daher noch nicht erreicht.

## Nächste Untersuchungsschritte

1. `WRITE.GEO` auf die nativen Dokument-Lifecycle-Aufrufe untersuchen: neues Dokument, Öffnen, Speichern, Speichern unter, Schließen.
2. Die dafür verwendeten Kernel-/UI-/Spool-Imports, Prozessmethoden und Objektklassen identifizieren; jeden Ordinal gegen den exakten deutschen GeoWorks-1.2-Kernel bzw. die passende Bibliothek validieren.
3. In `WRITE.GEO` die tatsächliche Dateityp-/Dokumentmoniker-Registrierung und die Referenz auf das Dokument-Icon nachweisen. Keine Ressourcen allein anhand ihrer Strings oder Größen als Dokument-Icon deklarieren.
4. Die minimal erforderlichen Mechanismen auf `GEOTEST.GEO` übertragen: zunächst „Neu“ und Erzeugen eines kleinen eigenen Dokumentinhalts; anschließend Speichern und erneutes Öffnen.
5. Das eigene Dokumentformat und den Dokument-Dateinamen festlegen und das eigene Icon über einen belegten Ressourcen-/Monikerpfad anbinden.
6. Erst danach einen neuen Build erzeugen und unter GeoWorks 1.2 testen. Erfolgskriterien: Anwendung startet, erzeugt Dokument, speichert es, GeoManager zeigt das eigene Dokument-Icon, und das Dokument lässt sich erneut öffnen.

## Abgrenzung

- Kein neuer Grafiktreiber wird gebaut.
- Keine Änderung an `SVGA8004.GEO`, `S16_1280.GEO` oder anderen Originaltreibern.
- Keine Übernahme von PC/GEOS 2.x-/FreeGEOS-Dokumentstrukturen ohne eigenständigen 1.x-Nachweis.
- Keine Behauptung eines Laufzeiterfolgs, solange der neue GEOTEST-Build nicht tatsächlich unter GeoWorks 1.2 ausgeführt wurde.
