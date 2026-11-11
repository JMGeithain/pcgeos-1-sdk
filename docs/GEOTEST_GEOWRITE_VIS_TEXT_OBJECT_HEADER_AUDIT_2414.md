# GeoWrite 1.x – VisText-Objektkopf und Chunk-Verknüpfungen (Untersuchung 2414)

## Ziel

Abgleich des 93 Byte großen Chunks `0050h/0022h` aus kleinen originalen GeoWrite-Dokumenten mit der im Enhanced-Colour-Quellpaket enthaltenen Struktur `OldVisTextInstance`. Schwerpunkt sind die Verweise auf Text und RunArrays.

## Quellen und Methode

- Originale GeoWrite-Dokumente `NEUES_DO.000`, `LEERER_B.000`, `TESTWRIT.000`.
- VM1-/LMem-Parser `/mnt/data/audit2407/vm1.py`.
- `Source/showcase-format/public-source/convertText.def`.
- `Source/showcase-format/public-source/convertText.asm`.
- `Source/showcase-format/native_write.py`.
- Statische Analyse; keine Änderungen an den Quelldateien und kein GeoWorks-Laufzeittest.

## 1. Objekt- und Instanzgröße

Der Chunk `0050h/0022h` ist in den drei verglichenen Dateien jeweils 93 Byte lang. An Chunk-Offset `04h` steht in allen drei Fällen der WORD-Wert `0008h`. Der Generator `native_write.py` liest genau diesen Wert als `vis = u16(article, 4)` und verwendet ihn als Basis für weitere Instanzfeldzugriffe.

Die Definition `OldVisTextInstance` beginnt mit `OVTI_meta VisInstance`; die nachfolgenden Felder sind in `convertText.def` ausdrücklich aufgelistet. Die Definition markiert `VisInstance` als zwischen 1.x und 2.0 gleich. Das ist ein Quelltextbeleg für die Struktur, ersetzt aber keine vollständige ABI-Spezifikation des gesamten Objekts.

## 2. Feldfolge und beobachtete Verweise

Laut `convertText.def` folgen nach `OVTI_meta` in dieser Reihenfolge:

1. `OVTI_text` – Text-Chunk (lptr)
2. `OVTI_styleRuns` – Zeichenformat-Läufe
3. `OVTI_rulerRuns` – Absatz-/Lineal-Läufe
4. `OVTI_typeRuns` – Typ-Läufe
5. `OVTI_gstringRuns` – Grafik-/GString-Läufe
6. Zustand und Typflags, danach weitere Objektzustände.

Im Binärchunk sind im Bereich nach dem Meta-Anteil die Werte für die bereits identifizierten Chunk-Handles `0026h`, `0028h`, `002Ch` und `002Ah` in genau dieser Reihenfolge sichtbar. Der Textverweis ist als relocations-/handle-artiger Wert kodiert und nicht als einfacher WORD-Wert `0024h` zu behandeln. Deshalb darf ein Generator diesen Wert nicht blind als normale Chunknummer schreiben.

Die Zuordnung der RunArray-Chunks wird zusätzlich durch `native_write.py` unabhängig bestätigt: Der Generator schreibt explizit `main.set(0x26, ...)`, `main.set(0x28, ...)` und `main.set(0x2a, ...)`; er setzt außerdem den Grafik-Lauf-Chunk im Objektkontext über die vorhandene Objektstruktur voraus. Die alte Konverterroutine `convertText.asm` verwendet die symbolischen Felder `OVTI_text`, `OVTI_styleRuns`, `OVTI_rulerRuns` und `OVTI_gstringRuns` beim Kopieren der entsprechenden Chunks.

## 3. Unterschiede zwischen leerem und gefülltem Dokument

Zwischen `NEUES_DO.000` und `TESTWRIT.000` bleiben die 93 Bytes des Objektchunks bis auf wenige Zustands-/Cachebereiche sehr ähnlich. Die Verweise auf Text- und Lauf-Chunks bleiben stabil. Der Generator `native_write.py` ändert nach dem Setzen der Text- und Laufdaten gezielt zwei WORD-Felder relativ zu `vis`:

```python
vis = u16(article, 4)
put16(article, vis+71, 0xffff)
put16(article, vis+73, 0xffff)
```

Die Felder werden im Quelltext nicht mit symbolischen Namen kommentiert. Deshalb werden sie hier nicht als bestimmte Cache- oder Layoutfelder benannt. Der Generator ruft danach `apply_cache(...)` auf, was zeigt, dass weitere abgeleitete Layoutdaten in den Objekt-/Seitenstrukturen relevant sind.

## 4. Wichtige Einschränkungen

- Die 93-Byte-Struktur ist eine konkrete Instanz in den untersuchten Dateien; nicht jedes Feld ist semantisch entschlüsselt.
- Der Textverweis ist relocations-/handle-kodiert. Ein einfacher Ersatz durch `0024h` wäre nicht belegt.
- `OVTI_typeRuns` ist in der Felddefinition vorhanden; seine konkrete Behandlung im vorliegenden Minimaldokument ist noch nicht vollständig geklärt.
- Der Generator greift nach dem Schreiben des Textes auf weitere Layout-/Cacheinformationen zu. Ein syntaktisch gültiger Textchunk allein garantiert daher kein korrektes Layout oder ein zuverlässig öffnendes Dokument.
- Die Quelltexte stammen aus dem späteren Showcase-/Patch-Paket. Sie liefern wertvolle Strukturbelege, sind aber keine vollständige offizielle GeoWorks-1.x-Formatspezifikation.

## Schlussfolgerung für GEOTEST

Der Objektchunk `0050h/0022h` ist der zentrale Knoten, der den Textstrom und die Lauf-Arrays zusammenführt. Für einen GEOTEST-Dokumentgenerator müssen mindestens diese Dinge gemeinsam konsistent sein:

- Objektinstanz `0022h`
- Textdaten `0024h`
- Zeichenformat-Läufe `0026h`
- Absatzformat-Läufe `0028h`
- Typ-Läufe `002Ch`
- Grafik-Läufe `002Ah`
- Relokations-/Handle-Referenz für den Text sowie VM-Block- und Seitenbezüge.

Der sichere nächste Schritt ist nicht, einen neuen Objektkopf aus Einzelwerten zusammenzusetzen, sondern die vollständigen Objekt- und Seitenstrukturen zweier kleiner Originaldokumente zu vergleichen und die noch unbekannten Relokationen sowie Cachefelder einzeln zuzuordnen.

## Nicht durchgeführt

- Kein GeoWorks-Start.
- Kein Testdokument erzeugt oder geöffnet.
- Keine Originaldateien verändert.
- Keine Binärpatches angewendet.

## Reproduzierbarkeit

Die Rohbytes des Chunks `0050h/0022h` wurden mit dem vorhandenen VM1-/LMem-Parser aus den drei genannten Dokumenten gelesen. Die Feldfolge stammt aus `OldVisTextInstance` in `convertText.def`; die Zugriffe auf die Felder sind in `convertText.asm` und `native_write.py` nachvollziehbar.
