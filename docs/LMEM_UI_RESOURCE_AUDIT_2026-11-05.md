# LMem- und UI-Ressourcen-Audit (2026-11-05)

## Geltungsbereich

Diese Untersuchung betrifft ausschließlich native GeoWorks / PC/GEOS 1.x Ressourcen. Referenzdateien:

- `SPINTEXT.GEO`, GeoWorks 1.x, SHA-256 `848f5afb43a2184b01d2a4ad3231957b6ab9936006b23b4b2a260d1224d44370`
- `VIEWER.GEO`, GeoWorks 1.x, SHA-256 `3d433a39c455a9cea242763dad0e3f681b4196fb7b1a75a08ca47e1aa8aa4a30`

Untersuchte Ressourcen:

- SPINTEXT R03 und R04
- VIEWER R0C und R1C

Die Dateien wurden aus dem vom Nutzer bereitgestellten `GWP2.zip` extrahiert. Die Originalarchive und GEO-Dateien wurden nicht verändert. Die Analyse ist statisch; es wurden weder SDK-Dateien gepatcht noch ein Build ausgeführt.

## 1. LMem-Header: Messwerte

Die ersten Headerfelder wurden mit `struct.unpack_from("<H", raw, 8)` und Offset 20 ausgelesen.

| Ressource | Länge | Feld bei 08h | Feld bei 14h |
|---|---:|---:|---:|
| SPINTEXT R03 | 01E0h | 01E0h | 01E0h |
| SPINTEXT R04 | 0150h | 014Ch | 0150h |
| VIEWER R0C | 1440h | 143Ch | 1440h |
| VIEWER R1C | 02C0h | 02B8h | 02C0h |
| Synthetischer Generator-Test | 0070h | 006Ch | 0070h |

Der Generator-Test verwendete:

```python
lmem(
    3,
    {0x22: None, 0x24: b"OBJECT", 0x26: b"HINT", 0x3e: b"VIEW"},
    {0x24, 0x3e},
    {0x3e}
)
```

### Bewertung

- Das Feld bei Offset 14h entspricht bei allen vier Originalressourcen der tatsächlichen Ressourcengröße.
- Das Feld bei Offset 08h liegt bei drei der vier Originalressourcen vor dem tatsächlichen Ressourcenende; SPINTEXT R03 ist die Ausnahme.
- Der Generator schreibt Offset 08h vor der abschließenden 16-Byte-Ausrichtung und Offset 14h danach. Sein Ergebnis (006Ch / 0070h) entspricht dem Muster von SPINTEXT R04, VIEWER R0C und VIEWER R1C.
- **Kein Header-Fehler ist durch diese Messung nachgewiesen.** Die genaue historische Semantik der Felder ist damit noch nicht abschließend belegt.

Korrektur einer früheren Zwischeninterpretation: Die Behauptung, Offset 08h und Offset 14h seien bei allen vier Originalressourcen identisch, war falsch. Maßgeblich sind die obigen gemessenen Werte.

## 2. Handle-Tabellen und Flag-Werte

In den untersuchten Ressourcen kommen bei den Handle-Flags die Werte `00`, `02`, `03` und `07` vor.

Beobachtete Flag-Folgen:

- SPINTEXT R03 (16 Handles): `00 02 03 02 03 02 07 02 02 07 02 07 02 03 02 07`
- SPINTEXT R04 (6 Handles): `00 03 02 02 02 00`
- VIEWER R0C (22 Handles): `00 03 02 03 02 03 02 03 02 03 02 02 02 02 03 02 03 02 03 02 03 02`
- VIEWER R1C (30 Handles): `00 02 03 02 03 02 03 02 07 07 02 02 03 02 02 03 02 02 03 02 02 03 02 02 03 02 02 03 02 02`

Handle 0020h enthält in allen vier untersuchten Ressourcen die Flag-Tabelle. Die ausgelesenen Bytes an diesem Handle stimmen mit den angezeigten Flag-Folgen überein.

### Leere Handles

Es wurden mindestens zwei unterschiedliche Offsetdarstellungen beobachtet:

- SPINTEXT R03 Handle 0022h: Offset FFFFh, Flag 02h.
- VIEWER R1C Handle 0022h: Offset FFFFh, Flag 02h.
- SPINTEXT R04 Handle 002Ah: Offset 0000h, Flag 00h.

Diese Fälle werden nicht gleichgesetzt. Der aktuelle Generator schreibt für `None` FFFFh. Ob und wann zusätzlich der Zustand 0000h erzeugt werden muss, ist offen.

## 3. Beobachtungen zu Flags 02h, 03h und 07h

In den untersuchten Beispielen gilt:

- Flag 02h tritt unter anderem bei Monikern und kleineren Daten-Chunks auf.
- Flag 03h tritt bei zahlreichen objektartig aufgebauten Chunks auf.
- Flag 07h tritt ebenfalls bei objektartig aufgebauten Chunks auf; es ist daher nicht einfach als Kennzeichen einer separaten Daten-Chunk-Klasse zu beschreiben.

Beispiele:

- SPINTEXT R03: Handles 0024h, 0028h und 003Ah tragen 03h; Handles 002Ch, 0032h, 0036h und 003Eh tragen 07h.
- VIEWER R1C: Handle 0032h trägt 07h, während 0038h 03h trägt. Beide Chunks beginnen mit `00 30 50` und sind jeweils 29 Bytes lang.
- VIEWER R1C enthält außerdem Handle 0030h mit Flag 07h und Anfangsbytes `01 60 0A`; Handle 0028h beginnt mit `01 60 01` und trägt Flag 03h.

Die binäre Darstellung der Werte lautet:

| Flag | Binär |
|---|---|
| 02h | 00000010 |
| 03h | 00000011 |
| 07h | 00000111 |

Das zeigt die gesetzten Bits, erklärt aber nicht deren GEOS-Laufzeitsemantik.

**Nicht belegt:** Die Bedeutung von Flag 07h ist nicht geklärt. Bezeichnungen wie „dirty“, „fixed“, „shared“ oder „permanent“ dürfen daraus nicht abgeleitet werden. Der Parametername `ignore_dirty` in `pcgeos1/ui.py` ist eine interne SDK-Bezeichnung und kein Beleg für die historische Bedeutung des Flags.

## 4. Byteweiser Objektvergleich

### VIEWER R1C: Handle 0032h (07h) gegen 0038h (03h)

Beide Chunks sind 29 Bytes lang. Die Unterschiede liegen ausschließlich an diesen Offsets:

| Offset | Handle 0032h | Handle 0038h | XOR |
|---:|---:|---:|---:|
| 0Ch | 38h | 3Eh | 06h |
| 12h | 1Bh | 19h | 02h |
| 14h | 34h | 3Ah | 0Eh |
| 18h | 36h | 3Ch | 0Ah |

Beide besitzen dieselbe erkennbare Anfangsstruktur (`00 30 50`). Die Daten belegen, dass gleiche Grundstruktur und Länge mit unterschiedlichen Flags vorkommen. Sie belegen nicht, dass die vier abweichenden Bytes die Flagwahl verursachen.

### SPINTEXT R03: Handle 0032h gegen 0036h (beide 07h)

Beide Chunks sind 31 Bytes lang. Die Unterschiede liegen an:

| Offset | Handle 0032h | Handle 0036h | XOR |
|---:|---:|---:|---:|
| 0Ch | 36h | 2Dh | 1Bh |
| 14h | 34h | 38h | 0Ch |
| 1Dh | FFh | 00h | FFh |
| 1Eh | FFh | 00h | FFh |

Beide haben Flag 07h und denselben erkennbaren Grundtyp (`00 30 52`). Die Unterschiede zeigen, dass Flag 07h nicht an eine einzelne feste Bytefolge gebunden ist.

## 5. Interpretation der 16-Bit-Werte

Die Objekt-Chunks wurden zusätzlich als Little-Endian-Wörter ausgegeben. Beispielsweise ergeben die Bytes `38 00` den Wert 0038h, `1B 10` den Wert 101Bh und `04 C0` den Wert C004h.

Diese Wörter sind zunächst Rohwerte. Werte, die wie Handle-Nummern aussehen, dürfen erst dann als Objektverweise bezeichnet werden, wenn Feldposition und Verknüpfungssemantik unabhängig bestätigt sind. Insbesondere sind 101Bh und C004h nicht automatisch Handle-Nummern.

## 6. Stand der Implementierung in ui.py

Die derzeitige Flag-Generierung lautet sinngemäß:

- Handle 0020h: 00h
- Handle in `ignore_dirty`: 07h
- Handle in `object_handles`: 03h
- alle übrigen Handles: 02h

Damit ist die Implementierung eine heuristische Vereinfachung. Die Originalressourcen zeigen, dass Flag 07h auch bei Objektstrukturen vorkommt, die sich nicht allein durch den gemeinsamen Anfang oder die Länge von Flag-03h-Objekten unterscheiden.

Die aktuelle Sonderliste in `build_basic_ui()` (0020h-Handles der generierten Ressource 3Eh, A6h, A8h, AAh) ist projektbezogen und ihre historische Notwendigkeit ist noch nicht nachgewiesen.

## 7. Offene Fragen und nächste Prüfschritte

1. Flag-Bit-Semantik durch weitere native 1.x Ressourcen und/oder Loader-/Kernel-Code untersuchen.
2. Objektfelder und Referenzen anhand bestätigter Objektstrukturen dekodieren; nicht allein aus numerischen Handle-Ähnlichkeiten schließen.
3. Die unterschiedlichen leeren Handle-Offsets 0000h und FFFFh weiter untersuchen.
4. Die Sonderbehandlung mit 07h in `ui.py` erst nach belastbarem Nachweis ändern.
5. Die erzeugten LMem-Ressourcen später gegen native 1.x Loader-/Laufzeitergebnisse testen; statische Ähnlichkeit allein ersetzt keinen GEOS-Test.

## 8. Arbeitsregeln

- Ausschließlich GeoWorks / PC/GEOS 1.x als Zielsystem.
- Keine Vermischung mit PC/GEOS 2.x oder FreeGEOS.
- Originaldateien und SDK-Code bleiben während dieser statischen Auditphase unverändert.
- Kein Build oder Patch, bis die relevanten Strukturen ausreichend verstanden und dokumentiert sind.
- Messwerte, gesicherte Beobachtungen und Hypothesen sind in diesem Dossier ausdrücklich getrennt.


## 9. Zeitgenössische Systemdokumentation (10.11.1990)

Als zusätzliche Referenz wurde die GeoWorks-Dokumentation *PC/GEOS System Software Overview*, Entwurfsfassung vom 10. November 1990, ausgewertet. Sie ist eine zeitgenössische PC/GEOS-Systembeschreibung und damit näher am Zielsystem 1.x als spätere FreeGEOS-/PC/GEOS-2.x-Unterlagen.

Quelle: Lyon Labs, PDF, Seiten 38–40:
https://www.lyonlabs.org/commodore/onrequest/geos/PC-GEOS-System-Software-Overview.pdf

Dort wird ausdrücklich beschrieben:

- Ein lokaler Heap wird innerhalb eines globalen Speicherblocks angelegt; vor der Initialisierung wird der Block alloziert und gelockt.
- `LMemInitHeap` initialisiert den Heap ab einem bestimmten Offset; der Heap reicht von dort bis zum Ende des Blocks.
- Der `LMemBlockHeader` liegt am Anfang des Blocks. Die Abbildung bezeichnet ihn als 16 Byte groß.
- Die lokale Handle-Tabelle enthält die Chunk-Handles. Ein Chunk-Handle ist ein Offset in den Block auf den Tabelleneintrag, an dem der tatsächliche Chunk-Offset gespeichert ist.
- Die tatsächlichen Chunk-Positionen können sich durch LMem-Operationen ändern; gespeichert werden soll deshalb der Handle und nicht ein zuvor dereferenzierter Offset.
- Ein Objektblock verwendet diesen LMem-Heap; jedes Objekt wird als eigener Chunk abgelegt. Die Kombination aus globalem Block-Handle und Chunk-Handle bildet den Object Descriptor (OD).

### Aussagegrenze

Die Dokumentation bestätigt das allgemeine LMem-Modell und die Rolle von LMem bei UI-Objekten. Sie erklärt in den ausgewerteten Passagen **nicht** die Bytewerte 02h, 03h und 07h in der Handle-Tabelle unserer GEO-Ressourcen. Daraus wird keine Flag-Semantik abgeleitet.

Insbesondere bestätigt die Dokumentation nicht, dass das Generatorfeld `ignore_dirty` tatsächlich ein historisches Dirty-Bit steuert. Dieser Parametername bleibt eine interne Bezeichnung des SDK-Codes, bis Kernel-/Loader-Code oder eine passende 1.x-Strukturdefinition die Semantik belegt.

### Konsequenz für die weitere Analyse

Die nächste belastbare Spur ist die konkrete Implementierung von LMem im PC/GEOS-1.x-Kernel bzw. der Ressourcendatei-Lader. Die Dokumentation liefert zwar die abstrakte Struktur, aber keine ausreichende Grundlage, um die Flag-Bits oder die Leer-Handle-Codierung im Generator zu ändern.
