# GeoWrite 1.x – Seitenblock 005Ch: Objektverweise und variable Seitenbereiche (Untersuchung 2415)

## Ziel

Prüfen, welche Teile des ersten Seitenblocks `005Ch` in kleinen Originaldokumenten stabil bleiben und welche Bereiche sich mit Dokumentinhalt bzw. Layout ändern. Dabei wird ausdrücklich zwischen belegten Objektverweisen und noch nicht identifizierten Cache-/Seitendaten unterschieden.

## Quellen und Methode

- Originaldateien `NEUES_DO.000`, `LEERER_B.000`, `TESTWRIT.000` und `_LEERER_.000` aus `/mnt/data/audit2409/`.
- Parser `/mnt/data/audit2407/vm1.py` (VM1-Header und LMem-Chunk-Tabelle).
- `Source/showcase-format/public-source/convertGeoWrite.asm` und `convertText.def` aus `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`.
- Bytevergleich der LMem-Chunks im VM-Block `005Ch`; keine Laufzeitprüfung.

## 1. Seitenblock und Chunkinventar

Alle vier Dateien besitzen den ersten Seitenblock unter VM-Handle `005Ch`, Größe 928 Byte. Die LMem-Chunkhandles und -größen sind in allen vier Dateien identisch:

| Chunk | Größe |
|---|---:|
| `0020h` | 38 |
| `0022h` | 104 |
| `0024h` | 89 |
| `0026h` | 1 |
| `0028h` | 18 |
| `002Ah` | 18 |
| `002Ch` | 14 |
| `002Eh` | 18 |
| `0030h` | 89 |
| `0032h` | 1 |
| `0034h` | 18 |
| `0036h` | 18 |
| `0038h` | 14 |
| `003Ah` | 18 |
| `003Ch` | 10 |
| `003Eh` | 143 |
| `0040h` | 10 |
| `0042h` | 143 |

Die identische Größe und Chunkbelegung zeigen ein gemeinsames Seitenblock-Grundgerüst. Sie beweisen allein noch nicht, dass alle Chunks aktive Seitendaten oder dieselbe semantische Funktion haben.

## 2. Seiten-Content-Chunk 0022h

Chunk `0022h` ist in allen vier Dateien 104 Byte groß. Er enthält mehrere wiederkehrende Werte und Verweise. In den bereits untersuchten Showcase-Seiten waren an den Payload-Offsets `004Ch` und `0056h` Relocation-IDs mit Quelle `ORS_NON_STATE_VM` nachgewiesen. Diese IDs verweisen über die VM-Block-Handle-Tabelle auf den jeweiligen Seitenblock selbst.

Im Vergleich der kleinen Originaldokumente sind diese beiden Felder ebenfalls als relocationsartige Werte vorhanden; die konkreten Bytes unterscheiden sich abhängig vom Dokument. Deshalb dürfen sie nicht als feste Konstanten übernommen werden. Die zuvor ermittelte Formel für `ORS_NON_STATE_VM` bleibt maßgeblich: Der RID-Index adressiert einen 12-Byte-Eintrag der VM-Handle-Tabelle (Tabellenbasis `0x2c`).

Der Quelltext `convertGeoWrite.asm` liest `GW12_PageContent` als Content-Objekt, folgt `VCI_comp.CP_firstChild` zum Header und danach über `VI_link.LP_next` zum Footer und weiteren Objekten. Die Routine bestätigt damit, dass die Seite eine verkettete Objektstruktur enthält. Die für eine vollständige Feldzuordnung nötigen Definitionen von `VCI_comp` und `VI_link` liegen in den hier untersuchten Dateien nicht vollständig vor. Daher wird hier kein bestimmter Offset im 104-Byte-Chunk als `firstChild` oder `next` deklariert.

## 3. Stabile und variable Seiten-Chunks

Der Vergleich von `NEUES_DO.000` und `TESTWRIT.000` zeigt:

- Die Chunks `0024h` bis `003Ch` haben dieselben Größen; viele davon sind byteidentisch.
- Chunk `003Eh` (143 Byte) unterscheidet sich deutlich. Er enthält in `NEUES_DO.000` einen lesbaren Textanteil („Willkommen ...“), während die Bytes in `TESTWRIT.000` anders aussehen.
- Chunk `0042h` (143 Byte) unterscheidet sich ebenfalls deutlich. In `TESTWRIT.000` ist darin die Bytefolge `Carta-Thiu` als ASCII sichtbar.
- Die Chunks `003Eh` und `0042h` können aufgrund ihrer Größe und Veränderlichkeit nicht ohne weitere Belege als reine Cache-Daten bezeichnet werden. Ihre exakte Rolle bleibt offen.
- `0020h` (38 Byte) verändert sich stark zwischen den Dokumenten; seine Felder sind hier nicht abschließend klassifiziert.

Auch `LEERER_B.000` und `_LEERER_.000` zeigen, dass die variablen Bereiche nicht einfach nur vom Vorhandensein des Haupttextes abhängen: `_LEERER_.000` hat zusätzliche/andere Objekt- und Layoutdaten, obwohl sein Haupttext-Chunk im Block `0050h` weiterhin nur ein Nullbyte enthält.

## 4. Was ist für GEOTEST gesichert?

Gesichert ist:

1. Ein kleines GeoWrite-Dokument verwendet einen 928-Byte-Seitenblock `005Ch` mit einem stabilen LMem-Chunkinventar.
2. Chunk `0022h` ist der Seiten-Content-/Objektknoten, den der historische Konverter als `GW12_PageContent` verarbeitet.
3. Die Seite enthält eine Objektverkettung; der Konverter folgt vom Content-Objekt zu Header/Footer und weiteren Objekten.
4. Bestimmte Felder in Chunk `0022h` sind VM-Relocation-IDs und müssen bei einer Neuerstellung konsistent sein.
5. Die übrigen Seiten-Chunks enthalten teils deutlich veränderliche Daten; ihre Semantik ist noch nicht hinreichend geklärt.

Nicht gesichert ist:

- welche der Chunks `003Eh` und `0042h` im konkreten Dokument Header-, Footer-, Layout- oder Cacheobjekte darstellen;
- die genaue Feldposition und Struktur von `CP_firstChild` und `VI_link.LP_next` im Binärchunk;
- ob sämtliche veränderlichen Daten beim Öffnen durch GeoWrite neu berechnet werden;
- ob ein neuer Seitenblock aus einem Minimaltemplate sicher erzeugt werden kann, ohne diese Bereiche zu erhalten.

## Konsequenz

Für GEOTEST ist der sicherste Weg weiterhin, einen echten kleinen GeoWrite-1.x-Dokumentseitenblock als Vorlage zu erhalten. Ein eigener Seitenblock sollte erst erzeugt werden, wenn die Objektkette und die VM-Relokationen vollständig dekodiert sind. Insbesondere dürfen die beiden 143-Byte-Chunks nicht pauschal gelöscht oder als entbehrlicher Cache behandelt werden.

## Nicht durchgeführt

- Kein Dokument wurde erzeugt oder verändert.
- Kein GeoWorks-Laufzeittest.
- Keine Annahme, dass unbekannte Chunks Cache-Daten sind.
- Keine vollständige Dekodierung von `VCI_comp` oder `VI_link`.

## Reproduzierbarkeit

Die Chunkgrößen und Bytevergleiche stammen aus dem VM-Block `005Ch` der vier genannten Dateien. Die Objektverkettung ist durch die symbolischen Feldzugriffe in `convertGeoWrite.asm` belegt; die genaue Binärfeldzuordnung bleibt ausdrücklich offen.
