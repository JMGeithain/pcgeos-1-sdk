# GeoWrite 1.x – Vollständiger Seitenblockvergleich (Untersuchung 2404)

## Ziel und Methode

Untersucht wurde ausschließlich das native GeoWrite-Dokument `Showcase/Deutsch/GeoWrite/SOLAR_DE.000` aus `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`. Die Datei wurde mit dem im selben Archiv enthaltenen VM1-Leser `vm1.py` gelesen. Es wurden keine Quelldateien oder Binärdateien verändert.

Der VM-Map-Block verweist auf den Seiten-ChunkArray. Dessen Header enthält 21 Elemente mit jeweils 30 Bytes. Das erste WORD jedes Elements liefert den VM-Block der jeweiligen Seite.

## Seitenblock-Inventar

Alle 21 referenzierten Seitenblöcke sind jeweils 848 Bytes groß. Jeder Block besitzt dieselben 18 belegten LMem-Chunks mit den Handles:

`0020h, 0022h, 0024h, 0026h, 0028h, 002Ah, 002Ch, 002Eh, 0030h, 0032h, 0034h, 0036h, 0038h, 003Ah, 003Ch, 003Eh, 0040h, 0042h`.

Ein vollständiger Bytevergleich aller 18 Chunks über alle 21 Seiten zeigt: 14 Chunks sind über alle Seiten byteidentisch. Vier Chunks unterscheiden sich.

## Vollständige Änderungsmuster

### Chunk 0022h

- Länge: 104 Bytes auf allen Seiten.
- Zwei abweichende Positionen: Payload-Offsets `0x4C` und `0x56`.
- Beide Positionen enthalten auf jeder Seite denselben Wert.
- Seiten 1–21: `04, 47, 49, 4B, 4D, 4F, 51, 53, 55, 57, 59, 5B, 5D, 5F, 61, 63, 65, 67, 69, 6B, 6D` (hex).
- Die Änderung beginnt auf Seite 2. Die Werte steigen ab Seite 2 jeweils um zwei.

### Chunk 0030h

- Länge: 89 Bytes auf allen Seiten.
- Eine abweichende Position: Payload-Offset `0x17`.
- Seiten 1–21 enthalten dort exakt dieselbe Wertefolge wie Chunk 0022h an den beiden dort abweichenden Positionen.
- Auch hier beginnt die Änderung auf Seite 2.

### Chunk 0032h

- Enthält den sichtbaren Text `Unser Sonnensystem  |  n/21` mit abschließendem Nullbyte.
- Seiten 1–9: 28 Bytes.
- Seiten 10–21: 29 Bytes.
- Der Längenwechsel entsteht durch die zusätzliche Ziffer der zweistelligen Seitenzahlen. Der Text ist ein direkter, sicherer Beleg für die Seitennummerierung in diesem Chunk.

### Chunk 0042h

- Länge: 39 Bytes auf allen Seiten.
- Eine abweichende Position: Payload-Offset `0x14`.
- Seiten 1–9: `A1h`.
- Seiten 10–21: `A8h`.
- Der Wechsel erfolgt exakt mit dem Übergang von einstelligen zu zweistelligen Seitenzahlen. Ein Zusammenhang ist denkbar, aber aus dem Bytevergleich allein nicht bewiesen. Die Feldbedeutung bleibt daher offen.

## Abgleich mit historischem Konverter-Quelltext

Die im Archiv enthaltene Datei `convertGeoWrite.def` beschreibt `GW12_PageArrayElement` als 30-Byte-Struktur. Das erste WORD ist `GW12_PAE_vmBlock`, gefolgt von Seitengröße, Attributen, View-Position, View-Größe, Dokumentoffset und neun reservierten Bytes. Die 30-Byte-Elementgröße stimmt exakt mit dem im Dokument gelesenen Seiten-ChunkArray überein.

Die Datei `convertGeoWrite.asm` liest die Elemente der Seitenliste, verwendet das erste WORD als VM-Blockhandle und sperrt den jeweiligen Seitenblock. Anschließend greift der Konverter auf `GW12_PageContent = 22h` zu. Das bestätigt die grundsätzliche Zuordnung des Seiten-ChunkArrays und den Zugriff auf den Seiteninhalt im historischen 1.x-Konverter.

Wichtig: Der Konverter ist ein Konvertierungspfad und keine vollständige Spezifikation aller GeoWrite-internen Chunks. Die Übereinstimmung von 30-Byte-Element und erstem WORD ist stark; die Bedeutungen der vier variablen Seiten-Chunks werden dadurch nicht erklärt.

## Interpretation und Grenzen

1. Der Seiten-ChunkArray und seine VM-Blockreferenzen sind strukturell durch Dokumentbytes und historischen Quelltext abgesichert.
2. Chunk `0032h` enthält nachweislich eine druckbare Seitenanzeige.
3. Chunks `0022h` und `0030h` tragen synchron veränderte Werte. Ihre Funktion ist noch nicht identifiziert. Es wäre unbelegt, sie bereits als Seiten-ID, Objekt-ID oder Handle zu bezeichnen.
4. Chunk `0042h` enthält eine ab Seite 10 geänderte Byteposition. Dass der Wechsel mit der zweistelligen Seitennummer zusammenfällt, ist beobachtet; eine kausale oder semantische Beziehung ist nicht bewiesen.
5. Die Analyse ist eine statische Dateiuntersuchung. Es wurde kein GeoWrite-Laufzeittest ausgeführt.

## Konsequenz für GEOTEST.GEO

Für einen minimalen nativen GeoWrite-Dokumentgenerator darf nicht angenommen werden, dass ein Seitenblock aus einem einzigen Textchunk besteht. Das untersuchte Beispieldokument verwendet 18 belegte Chunks pro Seite. Für den nächsten Schritt sollten die vier veränderlichen Chunks mit den tatsächlichen Erzeugungs- und Schreibstellen im GeoWrite-Quellcode abgeglichen werden. Bis dahin dürfen diese Bytes bei einer Dokumenterzeugung nicht frei erfunden oder als bedeutungslos weggelassen werden.

## Reproduzierbarkeit

Eingabedatei: `SOLAR_DE.000` aus dem oben genannten ZIP-Archiv.  
Parser: `Source/showcase-draw/vm1.py` aus demselben Archiv.  
Prüfung: 21 Seitenreferenzen, 21 × 848-Byte-Seitenblöcke, 18 Chunk-Handles pro Block, Bytevergleich jedes gleichnamigen Chunks über alle Seiten.

Keine Änderungen an den Originaldateien; keine Laufzeitaussage.
