# GeoWrite 1.x – Direktvergleich NEUES_DO.000 und TESTWRIT.000 (Untersuchung 2411)

## Ziel und Methode

Verglichen wurden die beiden originalen GeoWrite-1.x-Dokumente aus der entpackten Originalinstallation in `GEOWORKS.zip`:

- `NEUES_DO.000` – 2.352 Bytes
- `TESTWRIT.000` – 2.752 Bytes

Beide wurden mit dem VM1-/LMem-Parser aus dem Enhanced-Colour-Archiv gelesen. Die VM-Blocktabellen, Blockgrößen und LMem-Chunks wurden direkt verglichen. Es wurden keine Dateien verändert und kein GeoWrite-Laufzeittest durchgeführt.

## 1. VM-Blockvergleich

Beide Dateien besitzen dieselben acht belegten VM-Blockhandles:
`0020h, 002Ch, 0038h, 0044h, 0050h, 005Ch, 0068h, 0074h`.

Sie unterscheiden sich jedoch in den Blockgrößen:

| VM-Handle | NEUES_DO.000 | TESTWRIT.000 | Befund |
|---|---:|---:|---|
| `0020h` | 176 | 176 | Inhalt unterscheidet sich |
| `002Ch` | 96 | 96 | LMem-Inhalt unterscheidet sich |
| `0038h` | 80 | 80 | Chunk `0020h` ändert sich |
| `0044h` | 288 | 288 | Map-LMem ändert sich |
| `0050h` | 480 | 880 | **+400 Bytes** |
| `005Ch` | 928 | 928 | Seitenblock gleich groß, mehrere Chunks ändern sich |
| `0068h` | 48 | 48 | Inhalt unterscheidet sich |
| `0074h` | 48 | 48 | Inhalt unterscheidet sich |

Die gesamte Dateigrößendifferenz beträgt 400 Bytes. Sie entspricht exakt dem Größenanstieg des VM-Blocks `0050h` von 480 auf 880 Bytes. Die übrigen Blöcke behalten ihre Größe.

## 2. Map-Block 0044h

Der Map-Block enthält in beiden Dateien vier belegte Chunks:
`0018h`, `001Ah`, `001Ch`, `001Eh`.

Der Page-Array-Chunk `001Ah` ist in beiden Dateien 34 Bytes lang, hat Count 1, Elementgröße 30 und verweist auf Seitenblock `005Ch`. Die Seitenzahl und die 30-Byte-Elementgröße bleiben also unverändert.

Chunk `0018h` unterscheidet sich an mehreren Bytes. Chunk `001Eh` unterscheidet sich an Payload-Offsets `0x1C` und `0x1D` (in `TESTWRIT.000` steht dort `FFFFh`, in `NEUES_DO.000` `0000h`). Die übrigen Map-Chunks `001Ah` und `001Ch` sind byteidentisch.

## 3. Dokumentdatenblock 0050h

Der LMem-Block `0050h` wächst von 480 auf 880 Bytes. Er enthält in beiden Dateien neun belegte Chunks mit denselben Chunkhandles.

Der auffälligste Unterschied ist Chunk `0024h`:
- `NEUES_DO.000`: 1 Byte, Inhalt `00h`.
- `TESTWRIT.000`: 145 Bytes, Beginn `2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 15 3F ...`.

Die Bytes sind kein unmittelbar lesbarer ASCII-Text. Sie stellen einen deutlichen Inhaltsunterschied dar, aber ohne die passende GeoWrite-Text-/Zeichenkodierungsdefinition darf daraus kein wörtlicher Dokumenttext abgeleitet werden.

Weitere Chunks in `0050h` ändern sich ebenfalls:
- `0020h`: 32 Bytes, mehrere geänderte Felder.
- `0022h`: 93 Bytes, 8 abweichende Bytes.
- `002Eh`: wächst von 10 auf 20 Bytes.
- `0030h`: 143 Bytes, umfangreich verändert (104 Bytepositionen unterscheiden sich).
- `0026h`, `0028h`, `002Ah`, `002Ch` bleiben byteidentisch.

Das beweist, dass der Unterschied zwischen leerer Vorlage und Testdokument nicht nur aus einem eingefügten Textpuffer besteht. Auch Metadaten-/Objekt- und weitere Daten-Chunks ändern sich.

## 4. Seitenblock 005Ch

Beide Seitenblöcke sind 928 Bytes groß und besitzen dieselben 18 belegten Chunkhandles. Die wichtigsten Unterschiede:

| Chunk | NEUES_DO.000 | TESTWRIT.000 | Befund |
|---|---:|---:|---|
| `0020h` | 38 Bytes | 38 Bytes | Metadaten-/Monikerinhalt ändert sich deutlich |
| `0022h` | 104 Bytes | 104 Bytes | mehrere Feldwerte ändern sich; Selbstreferenz-WORDs bleiben `7004h` |
| `003Eh` | 143 Bytes | 143 Bytes | Inhalt ändert sich stark |
| `0042h` | 143 Bytes | 143 Bytes | Inhalt ändert sich stark |
| übrige 14 Chunks | gleich groß | gleich groß | im direkten Vergleich byteidentisch |

Chunk `0022h` behält die beiden Selbstreferenz-Relokationen an Payload-Offsets `0x4C` und `0x56`; beide enthalten in beiden Dokumenten `7004h`. Der Seitenblock ist in beiden Dateien weiterhin VM-Handle `005Ch`.

Die Chunks `003Eh` und `0042h` sind beide 143 Bytes lang, unterscheiden sich aber stark. In `0042h` von `TESTWRIT.000` ist im druckbaren ASCII-Bereich die Zeichenfolge `Carta-Thiu` sichtbar. Das ist ein Rohdatenbefund; die genaue Interpretation und Kodierung muss separat anhand des GeoWrite-Textformats geprüft werden.

## 5. Was sich daraus sicher ableiten lässt

1. Beide Dateien sind echte einseitige GeoWrite-Dokumente mit derselben Grundtopologie: acht VM-Blöcke, Map-Block `0044h`, Seitenarray mit einem Element und Seitenblock `005Ch`.
2. Der Page-Array-Eintrag und die Seitengrundstruktur bleiben bestehen.
3. Der Dokumentdatenblock `0050h` wächst um genau 400 Bytes und enthält die stärksten Änderungen.
4. Innerhalb von `0050h` wächst Chunk `0024h` von einem Nullbyte auf 145 Bytes. Das ist ein starker Kandidat für einen text-/inhaltsbezogenen Datenbereich, aber seine genaue Funktion ist ohne Quellcode-/ABI-Abgleich noch nicht bewiesen.
5. Auch die Seitenblöcke `005Ch` werden in mehreren Chunks angepasst. Es wäre deshalb falsch, nur `0050h` zu ersetzen und den Seitenblock grundsätzlich unverändert zu lassen.
6. Die Dokumentdatei `TESTWRIT.000` ist nicht einfach `NEUES_DO.000` plus 400 angehängte Bytes. Die zusätzlichen 400 Bytes liegen als Größenwachstum im VM-Block `0050h`; außerdem ändern sich zahlreiche vorhandene Chunks.

## 6. Konsequenz für GEOTEST.GEO

Die beiden Dateien liefern eine wertvolle Differenzprobe. Ein zukünftiger Generator kann nicht sicher auf „Textpuffer austauschen“ reduziert werden: mindestens der Dokumentdatenblock `0050h`, Map-Metadaten und mehrere Seitenblock-Chunks müssen konsistent betrachtet werden.

Der nächste sinnvolle Schritt ist, die Text-/Inhalts-Chunks in `0050h` und die geänderten Seiten-Chunks `003Eh`/`0042h` gegen GeoWrite-1.x-Textobjekt- und Zeichenkodierungsdefinitionen abzugleichen. Bis dahin sollte keine der Dateien als rohe Schreibvorlage verändert werden.

## Reproduzierbarkeit

Parser: `vm1.py` aus `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`.  
Eingaben: `NEUES_DO.000` und `TESTWRIT.000` aus `GEOWORKS.zip`.  
Prüfung: VM-Blockgrößen, VM-Blockinhalte, LMem-Chunkhandles, Chunkgrößen und Byteunterschiede.  
Status: statische Analyse; kein Laufzeittest und keine Veränderung der Originaldateien.
