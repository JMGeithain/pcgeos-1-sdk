# GeoWrite 1.x – Zeichen-, Absatz- und Grafik-Läufe (Untersuchung 2413)

## Ziel

Untersuchung der Chunks `0050h/0026h`, `0050h/0028h` und `0050h/002Ah` in kleinen originalen GeoWrite-Dokumenten. Ziel ist, den minimalen Laufbestand eines einfachen Textdokuments zu bestimmen.

## Quellen und Methode

- Originaldateien `NEUES_DO.000`, `LEERER_B.000`, `_LEERER_.000` und `TESTWRIT.000` aus dem extrahierten Originalarchiv unter `/mnt/data/audit2409/`.
- VM1-/LMem-Parser `/mnt/data/audit2407/vm1.py`.
- `Source/showcase-format/public-source/convertText.def` und `Source/showcase-format/native_write.py` aus `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`.
- Reine statische Binäranalyse; kein GeoWorks-Laufzeittest.

## 1. Lauf-Arrays im VM-Block 0050h

Bei `NEUES_DO.000` und `TESTWRIT.000` sind alle drei Lauf-Chunks bytegenau identisch:

| Chunk | Länge | Inhalt nach 10-Byte-Kopf |
|---|---:|---|
| `0026h` Zeichenformat-Läufe | 18 Byte | ein Eintrag Position 0, Token `0006h`, danach Terminator `8000h/0000h` |
| `0028h` Absatzformat-Läufe | 18 Byte | ein Eintrag Position 0, Token `0001h`, danach Terminator `8000h/0000h` |
| `002Ah` Grafik-Läufe | 14 Byte | nur Terminator `8000h/0000h`, kein Lauf-Eintrag |

Die vollständigen Bytes:

- `0026h`: `22 00 02 70 00 00 06 70 00 00 00 00 06 00 00 80 00 00`
- `0028h`: `22 00 01 70 00 00 06 70 00 00 00 00 01 00 00 80 00 00`
- `002Ah`: `22 00 07 70 00 00 06 70 00 00 00 80 00 00`

Damit verändert das Hinzufügen des Textinhalts in `TESTWRIT.000` diese drei Lauf-Arrays nicht. Der Textstrom wächst in Chunk `0024h`; die vorhandenen Standard-Läufe bleiben erhalten.

## 2. Struktur laut convertText.def

Die mitgelieferte Definition beschreibt einen `RunArray`-Kopf aus fünf WORD-Feldern:
- ElementArray-Chunkhandle
- ElementArray-VM-Blockhandle (oder 0, wenn im selben Block)
- NameArray-Chunkhandle oder 0
- NameArray-VM-Blockhandle (oder 0, wenn im selben Block)
- letzter Token zur Optimierung

Ein `RunArrayElement` besteht aus zwei WORDs:
- `RAE_position`: Position, an der der Lauf beginnt
- `RAE_token`: Token des zugehörigen Elements

Die gemessenen 10 Byte vor den Einträgen entsprechen damit der im Quelltext beschriebenen Kopfgröße. Der Eintrag bei Position 0 und der folgende Terminator sind mit der Definition vereinbar.

**Einschränkung:** Die Felder des 10-Byte-Kopfes enthalten im konkreten Binärbeispiel auch Werte wie `7002h` und `7006h`. Deren konkrete Relokations-/Handle-Bedeutung wird hier nicht weiter aufgelöst. Die Größen- und Feldaufteilung folgt der Definition; eine weitergehende Interpretation dieser Werte wäre ohne zusätzliche Relokationsanalyse nicht gesichert.

## 3. Zugehörige Format-Elemente

Die Lauf-Tokens stehen im Zusammenhang mit Element-Arrays in anderen VM-Blöcken:

- VM-Block `0038h`, Chunk `0022h`: Zeichenformat-Element-Array, bei den beiden Dokumenten 24 Byte groß; der Kopf weist einen Eintrag aus.
- VM-Block `002Ch`, Chunk `0022h`: Absatz-/Lineal-Element-Array, bei den beiden Dokumenten 42 Byte groß; der Kopf weist einen Eintrag aus.

`convertText.def` beschreibt ein generisches Element mit Referenzzähler und Element-ID. Die Definition von `OVisTextStyle` enthält unter anderem Font, Punktgröße, Textstil und Farbe; `OVisTextRuler` enthält unter anderem Rand-/Ausrichtungs-, Farb-, Abstand- und Tabulatorinformationen.

Der Generator `native_write.py` bestätigt die Zuordnung auf Anwendungsebene: Er baut Zeichenformat- und Lineal-Element-Arrays, setzt sie in VM `0038h` bzw. `002Ch` ein und erzeugt Lauf-Einträge mit Position und Token. Er schreibt die drei Lauf-Arrays nach `0026h`, `0028h` und `002Ah`.

## 4. Gegenprobe mit _LEERER_.000

`_LEERER_.000` besitzt jeweils drei Zeichenformat- und drei Lineal-Elemente (Chunks in VM `0038h` und `002Ch` sind größer). Seine Lauf-Chunks `0026h` und `0028h` haben weiterhin 18 Byte, aber andere Tokens (`002Ah` bzw. `000Ah`) als die beiden zuvor verglichenen Dokumente. Das zeigt, dass die Lauf-Tokens nicht pauschal als feste Konstanten für alle Dokumente behandelt werden dürfen: Sie hängen von den Elementen des jeweiligen Dokuments ab.

## Schlussfolgerungen für GEOTEST

1. Ein einfaches Textdokument kann mit genau einem Zeichenformat-Lauf ab Position 0 und einem Absatzformat-Lauf ab Position 0 auskommen.
2. Ohne eingebettete Grafiken kann das Grafik-Lauf-Array nur den Terminator enthalten.
3. Die Lauf-Arrays referenzieren Format-Elemente; die zugehörigen Element-Arrays in VM `0038h` und `002Ch` müssen konsistent bleiben.
4. Die Tokens `0006h` und `0001h` sind für diese beiden Beispieldokumente belegt, aber nicht als universelle Konstanten bewiesen.
5. Für einen GEOTEST-Prototyp sollte zunächst die Struktur eines vorhandenen einfachen Dokuments erhalten und nur der Textstrom kontrolliert verändert werden. Auch das bleibt bis zu einem erfolgreichen Öffnen und Speichern in GeoWrite ein unvalidierter Prototypenschritt.

## Nicht durchgeführt

- Kein Start von GeoWorks.
- Kein Öffnen/Neuspeichern eines erzeugten Dokuments.
- Keine Änderung der Originaldateien.
- Keine vollständige Auflösung der VM-Relokationsfelder im RunArray-Kopf.

## Reproduzierbarkeit

Die drei Lauf-Chunks und die beiden Format-Element-Arrays wurden direkt aus den VM1-/LMem-Blöcken der genannten Originaldateien extrahiert und byteweise verglichen.
