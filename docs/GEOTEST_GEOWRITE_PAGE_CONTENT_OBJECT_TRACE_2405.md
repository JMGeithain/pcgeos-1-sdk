# GeoWrite 1.x – Zuordnung des Seiteninhalts-Chunks zum Objektmodell (Untersuchung 2405)

## Fragestellung

Die Untersuchung 2404 hatte vier veränderliche LMem-Chunks in den 21 Seitenblöcken von `SOLAR_DE.000` identifiziert: `0022h`, `0030h`, `0032h` und `0042h`. Ziel dieser Untersuchung ist, die Zuordnung dieser Chunks anhand der im Archiv enthaltenen historischen PC/GEOS-1.x-Definitionen und des Konverter-Quelltexts zu prüfen.

## Quellen im Archiv

- `Source/showcase-format/public-source/convertGeoWrite.def`
- `Source/showcase-format/public-source/convertGeoWrite.asm`
- `Showcase/Deutsch/GeoWrite/SOLAR_DE.000`

Die Definitionsdatei enthält ausdrücklich den Kommentar, dass sie Definitionen für GeoWrite 1.x enthält. Die Datei ist Teil des mitgelieferten historischen Quelltextbestands; sie ist ein Konverter und keine vollständige Spezifikation des GeoWrite-Editors.

## Gesicherte Zuordnung: Chunk 0022h

In `convertGeoWrite.def` steht:

```asm
GW12_PageContent = 22h ;???
```

Der Kommentar `???` zeigt, dass der Autor die genaue Benennung bzw. Bedeutung im damaligen Konverterkontext selbst nicht weiter erläutert. Die anschließende Verwendung in `convertGeoWrite.asm` ist jedoch eindeutig:

- Zeile 156: `GW12_PAE_vmBlock` wird aus dem Seiteneintrag gelesen.
- Zeile 157: der betreffende Seitenblock wird mit `ourVMLockDS` gesperrt.
- Zeile 158: `mov si, ds:[GW12_PageContent]` lädt den Chunk `22h` als `content object`.
- Zeilen 162–163: der Code addiert `Vis_offset` und liest anschließend `VCI_comp.CP_firstChild.offset`. Der Quelltext kommentiert das Ergebnis als erstes Kindobjekt (Header).

Das bestätigt: Chunk `0022h` ist der Einstiegspunkt des visuellen Seiteninhaltsobjekts, das der Konverter als zusammengesetztes visuelles Objekt behandelt. Der Code verfolgt danach dessen Objektverknüpfungen.

## Ablauf der Seitenverarbeitung im Konverter

Der relevante Abschnitt `pageLoop` bis `nextPage` (ungefähr Zeilen 154–219) zeigt:

1. Das erste Kindobjekt wird über `CP_firstChild` ermittelt.
2. Der erste Durchlauf kopiert Header und Footer in die Konvertierungsstruktur.
3. Die Kindobjekt-Verknüpfung `VI_link.LP_next` wird verfolgt.
4. Weitere Objekte werden über `RelocToVMBlock` in ihren VM-Block aufgelöst und gesperrt.
5. `ConvertOldTextObject` verarbeitet die Textobjekte.
6. Der Seiten-ChunkArray-Zeiger wird um `size GW12_PageArrayElement` (30 Bytes) erhöht.

Damit passen die bereits festgestellte 30-Byte-Seitenarraystruktur und der Ablauf des historischen Konverters zusammen.

## Bytebefund aus SOLAR_DE.000

In den Seitenblöcken enthält Chunk `0022h` 104 Payload-Bytes. Die zwei seitenabhängigen Positionen liegen bei Payload-Offsets `0x4C` und `0x56`. In beiden Fällen ändern sich die Bytes synchron. Im Rohdump stehen diese Bytes jeweils als niederwertiges Byte eines 16-Bit-Werts, dessen folgendes Byte `70h` bleibt (z. B. Seite 1: Bytefolge `04 70`, Seite 2: `47 70`).

Chunk `0030h` enthält bei Payload-Offset `0x17` ebenfalls das jeweilige niederwertige Byte, gefolgt von `70h`. Dieser wiederkehrende Rohwert ist ein Grund, die Felder künftig als mögliche 16-Bit-Werte bzw. Objekt-/Relokationsdaten zu untersuchen. Eine konkrete Feldbedeutung ist daraus allein nicht bewiesen.

Chunk `0032h` enthält den sichtbaren Seitenanzeigetext `Unser Sonnensystem  |  n/21`.

Chunk `0042h` ändert an Payload-Offset `0x14` ab Seite 10 den Wert `A1h` zu `A8h`. Der Konverterabschnitt benennt diesen Chunk nicht.

## Was nicht bewiesen ist

- Der historische Konverter verwendet Chunk `0022h` als Seiteninhaltsobjekt, erklärt aber nicht die Bedeutung seiner veränderlichen Felder bei Offsets `0x4C` und `0x56`.
- Der betrachtete Konverterabschnitt weist Chunk `0030h`, `0032h` oder `0042h` keine symbolischen Namen zu.
- Die Werte mit dem Bytepaar `xx 70h` dürfen nicht ohne weitere ABI-/Objektdefinition als VM-Handles, Objekt-IDs oder Seiten-IDs bezeichnet werden.
- Der Wertwechsel in Chunk `0042h` korreliert mit dem Übergang zur zweistelligen Seitenanzeige; eine kausale Beziehung ist nicht nachgewiesen.

## Konsequenz für GEOTEST.GEO

Für den geplanten nativen Dokumentgenerator ist nun gesichert, dass jeder GeoWrite-Seitenblock einen visuellen zusammengesetzten Seiteninhalt über Chunk `0022h` bereitstellt. Ein Generator muss daher mindestens die Objektstruktur und ihre Verknüpfungen berücksichtigen; das bloße Schreiben eines Text-Chunks genügt nicht.

Die nächste sinnvolle Untersuchung ist eine strukturelle Auswertung der 16-Bit-Felder und Objektverknüpfungen in Chunk `0022h` sowie ein Abgleich der referenzierten Chunk-/VM-Objekte. Bis zur Identifikation der Felder werden keine Werte konstruiert oder verändert.

## Reproduzierbarkeit und Status

Die Quelltextstellen wurden aus den genannten Archivdateien gelesen. Der Rohbytevergleich bezieht sich auf die 21 Seitenblöcke von `SOLAR_DE.000`. Dies ist eine statische Analyse; ein Laufzeittest in GeoWrite wurde nicht ausgeführt.
