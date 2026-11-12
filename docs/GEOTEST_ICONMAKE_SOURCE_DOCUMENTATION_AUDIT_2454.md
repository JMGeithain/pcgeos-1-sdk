# GEOTEST / GeoWorks 1.x – Quellenprüfung ICONMAKE und Icon-Editor (Untersuchung 2454)

Stand: 12.11.2026  
Untersuchungsbasis: `/mnt/data/GEOWORKS.zip` (GeoWorks 1.2.8-Installationsarchiv)

## Ziel

Nach den Bytevergleichen von CGA- und HGC-Iconbereichen wird geprüft, ob die mitgelieferten ICONMAKE- und Icon-Editor-Unterlagen eine dokumentierte Dekodier- oder Render-Routine für die Icon-Bilddaten enthalten.

## Im Archiv gefundene relevante Dateien

| Datei | Größe | Bedeutung |
|---|---:|---|
| `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/ICONMAKE.ENG` | 6234 Bytes | Englische ICONMAKE-1.0-Dokumentation |
| `GEOWORKS/WORLD/PROGRAMM.E/G12/GEOTOOLS/ICONMAKE.DOC` | 6855 Bytes | Deutsche ICONMAKE-Dokumentation |
| `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/ICONMAKE.EXE` | 19477 Bytes | DOS-Konverter ICONMAKE 1.0 |
| `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/ICONED.EXE` | 27472 Bytes | DOS-Iconeditor ICONED |
| `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/ICON-EDI.001` | 12896 Bytes | Dokumentation des GeoWorks-Icon-Editors |
| `GEOWORKS/WORLD/PROGRAMM.E/G12/APPLIKAT.IES/ICON-EDI.000` | 30992 Bytes | GeoWorks-Dokumentation zum Icon-Editor |
| `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/ICON.GEO` | 1988 Bytes | Kleine GeoWorks-Anwendungsdatei |
| `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/L_MAKER.000` | 8832 Bytes | Icon-Maker-Datei |

Zusätzlich liegen zahlreiche Icon-Providerdateien in `GEOWORKS/ICONS/` und im ICONEDIT-Verzeichnis.

## Gesicherte Aussagen aus ICONMAKE.ENG und ICONMAKE.DOC

Beide Dokumentationen beschreiben:

1. ICONMAKE erzeugt aus PCX- oder Windows-ICO-Dateien kleine PC/GEOS-Dummy-Anwendungen mit Icon-Token.
2. Für die Standardprofile werden drei Bilder vorgesehen:
   - CGA: 48 × 14 Pixel, monochrom
   - HGC: 48 × 30 Pixel, monochrom
   - EGA: 48 × 30 Pixel, 16 Farben
3. Der Befehl `ICONMAKE x <dateiname>` extrahiert Icon-Definitionen aus vorhandenen GeoWorks-Programmen oder Dummy-Dateien in PCX-Dateien.
4. Der Befehl `ICONMAKE m ...` baut aus PCX-Dateien eine Dummy-Anwendung.
5. Die englische Dokumentation sagt ausdrücklich, dass die Konvertierung ein Codefragment aus der ursprünglichen GeoWorks-Icon-Sammlung verwendet und ICONMAKE dort die entsprechenden Bilder einfügt.

Die deutsche Dokumentation beschreibt denselben technischen Ansatz. Das stützt die Verwendung der Originalprovider als Strukturvorlage. Es erklärt jedoch nicht, wie die Pixel im Provider gespeichert oder zur Anzeige dekodiert werden.

## Gesicherte Aussagen aus ICONINST.TXT

Die Installationsanleitung erklärt die Zuordnung eines Tokens über den Abschnitt `[fileManager]` und den Eintrag `filenameTokens` in `GEOS.INI`. Ein Dummy wird als kleine PC/GEOS-Anwendung beschrieben. Die Beispielsyntax ordnet eine DOS-Dateiendung einem vierstelligen Token und einer Hersteller-ID zu.

Das ist ein Beleg für den Zuordnungs- und Installationsweg, aber kein Beleg für die interne Bildkodierung.

## Gesicherte Aussagen aus der Icon-Editor-Dokumentation

Die Dokumentation des GeoWorks-Icon-Editors beschreibt das Erstellen und Bearbeiten von Icons sowie die Verwendung verschiedener Icon-Typen (VGA/Farbe, Monochrom und CGA). Sie erklärt außerdem, dass der Editor kleine PC/GEOS-Anwendungen für Icons verwendet und dass GeoManager die Icons in der TOKEN.DB verwaltet bzw. installiert.

Die Dokumentation liefert keine bytegenaue Beschreibung des Provider-Descriptors und keine nachvollziehbare Dekodierformel für die CGA-/HGC-/EGA-Bilddaten.

## Binärdatei- und Quellcodeprüfung

Die Zeichenketten aus `ICONMAKE.EXE` bestätigen die Programmversion und die drei Hauptmodi:

- `ICONMAKE x <geos_file>`
- `ICONMAKE m...`
- `ICONMAKE w...`

Die sichtbaren Zeichenketten geben keine Pixel-Dekodiertabelle und keinen dokumentierten RLE-/Zeilenalgorithmus preis.

Im durchsuchten ZIP-Archiv wurden keine passenden Assembler-, C-, Header-, Definitions- oder Projektquelldateien gefunden, die unmittelbar als Quellcode einer Icon-Provider-Dekodierroutine identifiziert werden konnten. Das bedeutet nicht, dass im ausführbaren GeoWorks-Code keine solche Routine vorhanden ist; sie ist nur in den geprüften Dokumenten und Dateinamen nicht als Quelltext verfügbar.

## Ergebnis und Grenzen

**Bestätigt:**
- ICONMAKE verwendet laut eigener Dokumentation ein vorhandenes GeoWorks-Codefragment als Vorlage.
- Die Icon-Editor-Unterlagen bestätigen die Existenz unterschiedlicher Icon-Typen und den Token-/TOKEN.DB-Workflow.
- Die untersuchten Dokumentationen erklären nicht die konkrete Bytekodierung der Bilddaten.

**Nicht bestätigt:**
- die Semantik der Folge `FD FF 00`;
- ein RLE-, Delta- oder anderes Kompressionsverfahren;
- die konkrete Routine bzw. Ressource in `UI.GEO`, `ICON-ED.GEO` oder einer anderen GeoWorks-1.x-Datei, die den Provider-Payload dekodiert.

## Nächster Schritt

Die Untersuchung sollte nun gezielt in den ausführbaren GeoWorks-1.x-Dateien fortgesetzt werden. Kandidaten sind insbesondere `UI.GEO`, `ICON-ED.GEO`, `ICON-EDI.000` sowie die in der Installation vorhandenen System- und Dateimanager-Komponenten. Dabei muss zunächst der relevante Ressourcencode bzw. die Routine identifiziert werden; bloße Zeichenketten oder Byteähnlichkeiten reichen nicht als Nachweis einer Dekodierfunktion.

Alle Tests bleiben auf Kopien beschränkt. Die installierte `TOKEN.DB`, `GEOS.INI` und Originaldateien werden nicht verändert.
