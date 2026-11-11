# GeoWrite / GeoDraw Enhanced Colour Patch – Eingangsprüfung und GEOTEST-Relevanz (2395)

Stand: 2026-11-11

## 1. Eingabepaket

Datei: `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`

- Größe: 5.132.635 Byte
- ZIP-Einträge: 167
- ZIP-CRC-Test: bestanden (`ZipFile.testzip()` lieferte keinen fehlerhaften Eintrag)
- Enthält `MANIFEST.json`, `SHA256SUMS.txt`, englische und deutsche Programme, Quellcode, native Showcase-Dokumente, PDF-Lesefassungen und Laufzeit-/Strukturprüfberichte.

## 2. Entscheidender Abgleich mit unserem deutschen GeoWorks 1.2.8

Die im Paket enthaltenen deutschen Original-Eingaben stimmen bytegenau mit den zuvor analysierten GeoWorks-1.2.8-Dateien überein:

| Datei | Größe | SHA-256 |
|---|---:|---|
| Deutsches Original WRITE.GEO | 73.110 Byte | `0d2958b810948603d15e412a61598623b9a4ccb73cfeb9fbe08d50ee718a6fd0` |
| Deutsches Original DRAW.GEO | 31.624 Byte | `9b980dd04175d3c901835a96bc7b40f7a36f92f0b4fc66f0609300a11d04d70` |

Diese Hashes entsprechen unseren bisherigen Originalreferenzen. Das Paket patcht somit tatsächlich die passende deutsche 1.x-Eingabebasis, nicht nur ein ähnlich benanntes Programm unbekannter Herkunft.

## 3. Gepatchte Programmdateien

| Sprache | Programm | Bytes | SHA-256 |
|---|---|---:|---|
| Deutsch | WRITE.GEO | 123.186 | `585e2984e71eccc589c3018e2a3c710f876e445e5b85c5761baa2183702b97ab` |
| Deutsch | DRAW.GEO | 82.612 | `2de11cc0c1089bf4cc3b6aace931179e928c90633b30abab7ec288695f066d97` |
| Englisch | WRITE.GEO | 122.434 | `258b9f8d320bb6d03eec0b558f52bb92413b3006b3ee74efd1269074965e779e` |
| Englisch | DRAW.GEO | 82.404 | `489fdb82a5febae9aeef41ba8cd08143c9571714c8bf7fc7665374e801ebe5c3` |

Die gepatchten Dateien behalten die nativen App-Tokens:
- GeoWrite: `WP00`
- GeoDraw: `DP00`

Die deutschen Dateien sind eigenständige Builds aus den deutschen Originalen. Laut Quellnotizen bleiben die lokalisierten Ressourcen erhalten; gemeinsame Farbpaletten-Erweiterungen werden aus der englischen Vorlage portiert.

## 4. Funktionsumfang des Patches

Das Paket ergänzt die vorhandenen nativen Farbfenster in sechs Kontexten:
- GeoWrite: Textfarbe, Absatzfarbe und Rahmenfarbe
- GeoDraw: Flächenfarbe, Linienfarbe und Textfarbe

Enthalten sind:
- RGB-Eingabefelder mit Werten von 0 bis 255
- Live-Farbvorschau mit versenktem Rand
- zusätzliche nichtmodale Palette mit „Weitere Farben...“ bzw. „More colors...“
- Erhalt der vorhandenen Formatierungs-/Übernehmen-Pfade
- dynamische Positionierung des Zusatzfensters relativ zum jeweils aktuellen Hauptfarbfenster

Die Vorschau wird laut Quellbeschreibung als 65-Byte-GString-Moniker realisiert, nicht als zusätzliche Offscreen-Bitmap. Die Ergänzung verwendet 8086-Code. Die angegebenen Objekt-/Codegrößen sind keine Messung des residenten RAM-Verbrauchs.

## 5. Laufzeit- und Reproduzierbarkeitsnachweise im Paket

Die enthaltenen Berichte nennen:
- CPU-/Emulatorprüfungen für DOSBox-X mit 8086-Profil und VGA 640×480 sowie 386-Profil mit TrueColor 1024×768
- CPU-Harness-Tests für die tatsächlich erzeugten Instruktionen und 8086-Kompatibilitätsprüfung
- reproduzierbare Builds der vier Programme aus einer minimalen Quellbasis mit byteidentischen Ergebnissen
- native GeoWorks-Laufzeitbeobachtungen für die angegebenen DOSBox-X-Profile
- Speichern und erneutes Öffnen von nativen Showcase-Dokumenten nach einer Bearbeitung

Die Laufzeitberichte weisen selbst Grenzen aus: Sie beweisen weder physische 8088-/8086-Timingwerte noch einen unabhängig gemessenen residenten RAM-Zuwachs. VGA- und TrueColor-Profile sind getrennt zu betrachten.

## 6. Besonders wichtig für unser GEOTEST-Projekt: native Dokumente

Das Paket enthält echte native GeoWrite- und GeoDraw-Dokumente mit der normalen Endung `.000`, keine umbenannten PDFs oder DOS-Textdateien.

Beispiele:
- `Showcase/Deutsch/GeoWrite/SOLAR_DE.000` – 316.084 Byte
- `Showcase/Deutsch/GeoDraw/FARBE.000` – 215.400 Byte

Die Dokumentheader zeigen die anwendungsspezifischen Tokenpaare:
- GeoWrite-Dokument: `WDAT` / `WP00`
- GeoDraw-Dokument: `DDAT` / `DP00`

Damit wird unsere frühere statische Beobachtung aus WRITE.GEO und DRAW.GEO durch tatsächlich vorhandene native Dokumentdateien ergänzt. Die Tokenpaare sind nicht bloß Zeichenfolgen in Programmressourcen, sondern stehen auch im Header der mitgelieferten nativen Dokumente.

Die Quellstruktur enthält darüber hinaus:
- `Source/showcase-format/native_write.py`: GeoWrite-VM-Dokumentgenerator
- `Source/showcase-format/public-source/`: historische 1.x-Konvertierungs- und VM-Referenzquellen mit Provenienz
- `Source/showcase-draw/document_lmem.py`: Writer für den nativen Dokument-LMem-Heap
- `Source/showcase-draw/GSTRING-CHAIN-ABI.md`: Hinweise zum nativen GString-Kettenformat
- unabhängige Struktur- und Pixelprüfungen der erzeugten Dokumente

Der GeoDraw-README beschreibt native DDAT/DP00-Dokumente, VM-Container, serialisierte Objekt-ABI und editierbare Objekte. Der GeoWrite-Generator verwendet vorhandene native Dokumentstrukturen als Vorlage und baut VM-Blöcke, LMem-Heap, Text-/Stil-/Absatz-Runs und Grafikreferenzen um.

Die beigefügten Laufzeitberichte protokollieren Bearbeitung, Speichern und erneutes Öffnen der deutschen und englischen GeoWrite-Beispieldokumente. Dies ist ein wesentlich stärkerer Praxisbeleg für native Dokumente als die bisherige reine Token- und Ressourcenanalyse.

## 7. Konsequenz für GEOTEST – aber noch keine Übernahme

Dieses Paket ist eine wertvolle Referenz für den nächsten Entwicklungsschritt:
1. GeoWrite-Dokumentgenerator und native VM-/LMem-Strukturen analysieren.
2. GeoDraw-Dokumentgenerator und Objekt-ABI separat analysieren.
3. Die Unterschiede zwischen Dokumentdatei-Header, VM-Container, Dokument-LMem und App-Geode sauber dokumentieren.
4. Prüfen, welche minimale Struktur für ein eigenes GEOTEST-Dokument erforderlich wäre.
5. Erst danach einen unabhängigen GEOTEST-Dokumentprototyp planen.

Wichtig: Die nativen Dokumentbeispiele stammen aus GeoWrite bzw. GeoDraw. Sie beweisen nicht automatisch, dass GEOTEST.GEO ohne eigene Dokumentklasse und ohne eigene Dokument-Tokenregistrierung dieselben Strukturen verwenden kann.

Die gepatchten WRITE.GEO-/DRAW.GEO-Dateien werden nicht in die laufende Installation kopiert und nicht als Teil von GEOTEST verwendet, solange Johannes dies nicht ausdrücklich freigibt. Originaldateien bleiben unverändert.

## 8. Grenzen und offene Prüfungen

- Die ZIP-Prüfung und Hashvergleiche wurden lokal durchgeführt.
- Die Runtime-Ergebnisse sind Angaben und Artefakte aus dem gelieferten Paket; sie wurden in dieser Untersuchung nicht erneut in einer eigenen GeoWorks-Installation ausgeführt.
- Die Quellcode- und Build-Berichte müssen bei Bedarf separat reproduziert und auf konkrete Codepfade geprüft werden.
- Der Pakettext weist darauf hin, dass die Programme für die bereitgestellten 1.2-Eingaben gelten und keine universellen Ersatzdateien für jede Ensemble-Ausgabe sind.

## 9. Quellen innerhalb des gelieferten Pakets

- `RELEASE-README-Deutsch.txt`
- `MANIFEST.json`
- `SHA256SUMS.txt`
- `Source/README.md`
- `Source/write-de/SOURCE-NOTES.md`
- `Source/draw-de/SOURCE-NOTES.md`
- `Source/showcase-format/README.md`
- `Source/showcase-format/native_write.py`
- `Source/showcase-format/public-source/provenance.json`
- `Source/showcase-draw/README.md`
- `Source/showcase-draw/document_lmem.py`
- `Source/runtime/VALIDATION.md`
- `Source/runtime/native-write-save-reopen-de.json`
