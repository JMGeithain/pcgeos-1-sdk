# GEOTEST – native GeoWrite-/GeoDraw-Dokumentstruktur: Vergleich echter 1.x-Dateien (2396)

Stand: 2026-11-11

## 1. Untersuchungsgrundlage

Untersucht wurden die beiden deutschen nativen Showcase-Dateien aus dem vom Nutzer bereitgestellten Paket `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`:

- `Showcase/Deutsch/GeoWrite/SOLAR_DE.000` – 316.084 Byte
- `Showcase/Deutsch/GeoDraw/FARBE.000` – 215.400 Byte

Die Dateien wurden mit dem im Paket enthaltenen `Source/showcase-draw/vm1.py` unabhängig eingelesen. Die Prüfroutine prüft die GEOS-Dateisignatur, den VM-Dateisignatureintrag und den VM-Header. Die hier genannten Strukturwerte stammen aus dem Byteinhalt dieser beiden konkreten Dateien.

## 2. Gemeinsamer äußerer VM-Dateiaufbau

Beide Dateien beginnen mit:
- Dateisignatur: Bytes `C7 45 CF 53`
- VM-Dateisignatur bei Datei-Offset `00C8h`: `ADEBh`
- VM-Headergröße bei `00CAh`
- VM-Headerposition bei `00CCh`
- Map-Block-Handle im VM-Header bei relativem VM-Headeroffset `14h`: `0044h`

Die beiden Dateien haben also in diesen Beispielen dieselbe Map-Block-Handle-ID `0044h`, aber unterschiedliche Map-Block-Inhalte und VM-Headergrößen.

## 3. GeoWrite-Dokument: WDAT / WP00

Datei: `SOLAR_DE.000`

### Geos-/Dokumentkopf

- Dokumenttyp-Token bei Datei-Offset `0014h`: `WDAT`
- Herstellerwort: `0000h`
- Erzeuger-/Anwendungstoken: `WP00`
- Dokumenttitel im Headerbereich: `Unser Sonnensystem`
- VM-Headergröße: `0554h`
- VM-Headerposition: `04CD60h`
- Map-Block-Handle: `0044h`

### Map-Block und VM-Blöcke

VM-Block `0044h` ist ein LMem-Block mit vier Chunk-Handles:
- `0018h`: 16 Byte
- `001Ah`: 634 Byte
- `001Ch`: 91 Byte
- `001Eh`: 64 Byte

Die konkreten semantischen Namen dieser vier Map-Chunks werden hier noch nicht endgültig festgelegt. Ihre Existenz, Reihenfolge und Größen sind direkt aus dem nativen Dokument gelesen.

Weitere relevante VM-Blöcke, die der mitgelieferte Generator `native_write.py` ausdrücklich als GeoWrite-Dokumentteile verwendet:
- `0050h`: Haupt-/Artikel-LMem; darin werden Text und Text-/Absatz-/Grafik-Runs bearbeitet
- `0038h`: Zeichenstil-LMem
- `002Ch`: Absatz-/Linealstil-LMem
- `0074h`: Grafik-/GString-Referenz-LMem

Diese Zuordnung folgt dem Generatorcode. Die genaue semantische Zuordnung jedes einzelnen Map-Chunks ist davon getrennt zu behandeln.

### GeoWrite-Artikel-LMem

Der Generator bearbeitet im VM-Block `0050h` die Chunk-Handles:
- `0024h`: Textbytes, einschließlich abschließendem Nullbyte
- `0026h`: Zeichenstil-Runs
- `0028h`: Absatz-/Lineal-Runs
- `002Ah`: Grafik-Runs

Die historischen Definitionen in `convertGeoWrite.def` beschreiben unter anderem PageArrayElement, PageSetupAttributes und WriteDocumentData. Die Definitionen nennen VM-Block-Handles für Stil-, Lineal-, GString- und Namensdaten. Die vollständige Zuordnung aller Felder des konkreten Map-LMem zu diesen Definitionen bleibt ein eigener Prüfpunkt.

## 4. GeoDraw-Dokument: DDAT / DP00

Datei: `FARBE.000`

### Geos-/Dokumentkopf

- Dokumenttyp-Token bei Datei-Offset `0014h`: `DDAT`
- Herstellerwort: `0000h`
- Erzeuger-/Anwendungstoken: `DP00`
- Dokumenttitel: `Farbe - Bildhinweise`
- VM-Headergröße: `02D8h`
- VM-Headerposition: `034690h`
- Map-Block-Handle: `0044h`

### GeoDraw-Mapblock

Der VM-Block `0044h` ist in diesem Beispiel 16 Byte lang. Seine ersten beiden WORDs sind:

- `002Ch`: Dokumentdaten-VM-Block
- `0038h`: Body-/Objekt-VM-Block

Das entspricht direkt der historischen Definition `DrawDocMap1X` in `convertDrawDocument.def`:
- `DDM_1X_documentData`
- `DDM_1X_bodyBlock`

Der Dokumentdatenblock `002Ch` ist 16 Byte groß. Der Bodyblock `0038h` ist ein LMem-Block und in dieser Datei 240 Byte groß. Die ersten beiden WORDs des Mapblocks liefern damit eine sehr klare und direkt überprüfbare 1.x-Struktur.

Wichtig: `DrawMapBlock` am Anfang derselben Definitionsdatei beschreibt ausdrücklich ein 2.0-Format. Für die hier untersuchte GeoWorks-1.x-Datei ist `DrawDocMap1X` die relevante Definition. Diese beiden Strukturen dürfen nicht vermischt werden.

## 5. Was dies für GEOTEST aussagt

1. Native GeoWorks-Dokumente sind VM-Dateien mit eigenem Dokumenttyp-/Erzeugertoken und einem VM-Map-Block.
2. GeoWrite und GeoDraw verwenden nicht denselben internen Dokumentaufbau.
3. GeoDraw 1.x besitzt im untersuchten Beispiel einen besonders überschaubaren Mapblock: zwei VM-Block-Handles für Dokumentdaten und Body.
4. GeoWrite 1.x besitzt im Beispiel einen LMem-Mapblock mit vier Chunks sowie getrennte VM-Blöcke für Artikel, Zeichenstile, Absatzstile und Grafiken.
5. Das Erzeugen eines nativen GEOTEST-Dokuments erfordert daher eine eigene, konsistente VM-/Map-/Dokumentstruktur. Ein bloßes Ändern der Tokenbytes in einer GeoWrite- oder GeoDraw-Datei wäre keine gültige Implementierung.

## 6. Wichtige Einschränkung des mitgelieferten Generators

`native_write.py` beginnt mit einem existierenden GeoWrite-Dokumenttemplate:
`Source/original/GWSVGA/DOCUMENT/NEW_DOCU.000`

Der Generator lädt daraus VM-Blöcke und ändert gezielt ausgewählte LMem-Inhalte. Das Paketarchiv enthält jedoch nicht diesen Templatepfad bzw. die Datei `NEW_DOCU.000`; es enthält die deutschen Original-Geodes, die Showcase-Dokumente und den Quellcode. Der Generator kann deshalb aus dem ZIP allein nicht vollständig reproduziert werden. Die fehlende Template-Datei muss aus der im Paket vorausgesetzten Originalinstallation stammen.

Ebenso benötigt die GeoDraw-Showcase-Erzeugung die in den README-Dateien genannten Original-1.x-Dokumenttemplates. Das ist bei der Reproduktion zu berücksichtigen.

## 7. Nächste Schritte für GEOTEST

1. Die vier GeoWrite-Map-LMem-Chunks einzeln gegen `convertGeoWrite.def` und den historischen Konvertierungscode auflösen.
2. Den minimalen GeoWrite-VM-Blockbestand aus dem Originaltemplate dokumentieren.
3. Die GeoDraw-1.x-Struktur separat weiter untersuchen: Dokumentdatenblock, Body-LMem, Objektklasse und notwendige VM-Referenzen.
4. Prüfen, ob eine minimale native Dokumentklasse für GEOTEST einfacher an den GeoDraw-1.x-Objektaufbau oder an den GeoWrite-Artikelaufbau angelehnt werden kann.
5. Erst nach dieser Analyse einen minimalen GEOTEST-Dokumentprototyp entwerfen. Keine Token- oder Headeränderung als Ersatz für die vollständige Struktur.

## 8. Quellen im gelieferten ZIP

- `Source/showcase-format/native_write.py`
- `Source/showcase-draw/document_lmem.py`
- `Source/showcase-draw/vm1.py`
- `Source/showcase-format/public-source/convertGeoWrite.def`
- `Source/showcase-format/public-source/convertDrawDocument.def`
- `Source/showcase-format/public-source/vmInt.h`
- `Showcase/Deutsch/GeoWrite/SOLAR_DE.000`
- `Showcase/Deutsch/GeoDraw/FARBE.000`

## Status

Statische Prüfung zweier echter nativer 1.x-Dokumente. Die mitgelieferten Runtime-Berichte wurden als Paketartefakte gelesen, aber in dieser Untersuchung nicht erneut ausgeführt. Kein GEOTEST-Dokument wurde erzeugt oder unter GeoWorks getestet. Keine Originaldatei verändert.
