# GEOTEST – GeoWrite-Seitenverwaltung im nativen Dokument SOLAR_DE.000 (2399)

Stand: 2026-11-11

## Ziel

Die zwei größeren Map-LMem-Chunks aus `SOLAR_DE.000` werden anhand ihrer ChunkArray-Header und Elementgrößen ausgewertet. Die Einordnung wird auf das beschränkt, was Byteaufbau und historischer Quellcode tatsächlich belegen.

## Quelldatei

- `Showcase/Deutsch/GeoWrite/SOLAR_DE.000`
- 316.084 Byte
- VM-Map-Block: Handle `0044h`
- Mapblock ist ein LMem-Block mit 16 Chunk-Slots.

## 1. Chunk 001Ah: 21 Elemente à 30 Byte

Die Payload beginnt mit:

`15 00 1E 00 5C 00 64 02 18 03 ...`

Als `GW12_ChunkArrayHeader` interpretiert:
- Elementanzahl: `0015h` = 21
- Elementgröße: `001Eh` = 30 Byte

Die Gesamtlänge stimmt exakt:
- Header: 4 Byte
- 21 Elemente × 30 Byte = 630 Byte
- Gesamt: 634 Byte

Die historische Definition `GW12_PageArrayElement` hat genau 30 Byte:
- VM-Block-Handle: 2 Byte
- Seitengröße XYSize: 4 Byte
- Attribute: 2 Byte
- View-Position: 4 Byte
- View-Größe: 4 Byte
- Dokumentoffset: 4 Byte
- reservierte Bytes: 9 Byte
- Ausrichtung auf gerade Größe: 1 Byte

Damit stimmen sowohl Elementanzahl-/Größenheader als auch die Elementgröße exakt mit dem historischen PageArrayElement überein. Der historische Konvertierer behandelt den Seitenarray-Chunk ebenfalls als ChunkArray und greift in jeder Iteration auf `GW12_PAE_vmBlock` zu.

### 21 gespeicherte Seitenblock-Handles

Das erste WORD jedes 30-Byte-Elements ergibt:

`005Ch, 0380h, 0398h, 03B0h, 03C8h, 03E0h, 03F8h, 0410h, 0428h, 0440h, 0458h, 0470h, 0488h, 04A0h, 04B8h, 04D0h, 04E8h, 0500h, 0518h, 0530h, 0548h`

Alle 21 Werte existieren als VM-Block-Handles in der VM-Header-Tabelle von `SOLAR_DE.000`. Dies ist ein besonders starker Nachweis, dass es sich um Verweise auf die zugehörigen Seitenblöcke handelt.

Die Seitengrößen-WORDs in den Elementen beginnen im Beispiel jeweils mit `0264h` und `0318h`; die folgenden View-/Offsetfelder sind überwiegend null. Die semantische Interpretation der übrigen Felder folgt der historischen Strukturdefinition, wurde aber nicht durch einen GeoWorks-Laufzeittest separat bestätigt.

## 2. Chunk 001Ch: ChunkArray mit einem 87-Byte-Element

Die Payload beginnt mit:

`01 00 57 00 64 02 18 03 48 00 48 00 ...`

Als ChunkArray-Header:
- Elementanzahl: 1
- Elementgröße: `0057h` = 87 Byte

Die Gesamtlänge stimmt exakt:
- Header: 4 Byte
- 1 × 87 Byte = 87 Byte
- Gesamt: 91 Byte

Damit ist ein einzelnes 87-Byte-Element nachgewiesen. Es liegt nahe, diesen Chunk aufgrund seiner Position in der Map-LMem-Tabelle und des historischen Kontexts mit dem Master-Page-Array in Verbindung zu bringen. **Die semantische Identität des 87-Byte-Elementtyps ist aber noch nicht durch eine passende Strukturdefinition oder einen direkten Codezugriff bewiesen.** Daher wird er hier nur als 1-Element-ChunkArray bezeichnet.

## 3. Chunk 0018h und Chunk 001Eh bleiben getrennt

- Chunk `0018h`: 16 Byte, beginnt mit `00 08 08 08 ...`; Struktur noch nicht aufgelöst.
- Chunk `001Eh`: 64 Byte, beginnt mit ASCII `DX` und enthält unter anderem Werte, die mit VM-Block-Handles übereinstimmen; Felddefinition noch offen.

Es wäre nicht korrekt, die beiden Chunks ohne weiteren Beleg als Dokumentdaten- oder Page-Setup-Struktur zu benennen.

## 4. Abgleich mit dem historischen GeoWrite-Konvertierer

`convertGeoWrite.def` definiert:
- `GW12_ChunkArrayHeader`
- `GW12_PageArrayElement` mit 30 Byte
- `GW12_PAGE_ARRAY_CHUNK`
- `GW12_MASTER_PAGE_ARRAY_CHUNK`
- `GW12_DOCUMENT_DATA_CHUNK`

`convertGeoWrite.asm` liest den Page-Array-Chunk, nimmt dessen Elementanzahl aus dem Header, läuft mit `size GW12_PageArrayElement` durch die Elemente und verwendet das erste WORD als VM-Handle des Seitenblocks. Das passt exakt zur 30-Byte-Elementgröße und zum ersten WORD der 21 Elemente in `SOLAR_DE.000`.

Wichtig bleibt: Die numerischen Chunk-Handle-Slots der historischen Konvertierungsdefinition sind nicht ohne Weiteres auf die Slot-Belegung des konkreten Showcase-Dokuments übertragbar. Die Strukturübereinstimmung ist hier auf Header, Elementgröße und VM-Blockreferenzen gestützt, nicht auf eine pauschale Gleichsetzung aller Slotnummern.

## 5. Konsequenz für GEOTEST

Ein natives GeoWrite-Dokument enthält nicht nur Text- und Stilblöcke, sondern auch eine explizite Seitenverwaltung:
- ein ChunkArray mit 21 PageArrayElements,
- jedes Element verweist auf einen eigenen VM-Seitenblock,
- zusätzlich ein weiteres ChunkArray mit einem 87-Byte-Element, dessen genaue Rolle noch offen ist.

Ein minimaler GEOTEST-Prototyp kann diese Komplexität nicht durch bloßes Anlegen eines Text-LMem-Blocks umgehen, wenn er die GeoWrite-Dokumentarchitektur nachbilden soll. Andererseits ist noch nicht bewiesen, dass GEOTEST überhaupt die komplette GeoWrite-Seitenarchitektur benötigt. Eine eigene einfachere Dokumentklasse bleibt eine offene Option.

## 6. Nächste Schritte

1. Die 21 Seiten-VM-Blöcke stichprobenartig untersuchen und den gemeinsamen Seitenblockaufbau vergleichen.
2. Das 87-Byte-Element aus Chunk `001Ch` gegen weitere GeoWrite-Dokumente und den WRITE.GEO-Code prüfen.
3. Chunk `0018h` und `001Eh` weiter auflösen.
4. Danach die minimalen GEOTEST-Anforderungen festlegen, ohne unbewiesene GeoWrite-Strukturen zu übernehmen.

## Status

Statische Auswertung der nativen Showcase-Datei und des historischen 1.x-Konvertierungscodes. Kein Laufzeittest in GeoWorks. Keine Änderungen an Originaldateien und kein GEOTEST-Dokument erzeugt.
