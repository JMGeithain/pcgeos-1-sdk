# GEOTEST – TOKEN.DB: VM- und LMem-Blockinventar (2422)

Stand: 2026-11-12  
Geltungsbereich: originales GeoWorks / PC/GEOS 1.x, keine Vermischung mit GEOS 2.x  
Quelle: `GEOWORKS/SYSTEM/TOKEN.DB` aus dem bereitgestellten `GEOWORKS.zip`; statische, lesende Analyse.

## 1. VM-Dateikopf

Die Datei ist 952.688 Bytes groß; SHA-256:

`c7fa3d51c9bdce14b988d20fd8ed57ac7da9837803090ac858990613ec53ae35`

Bestätigte Rohwerte:
- GEOS-Dateisignatur bei Offset `0000h`: `C7 45 CF 53`.
- VM-Signatur bei Offset `00C8h`: `EB AD` (little-endian Wort `ADEBh`).
- VM-Headergröße bei `00CAh`: `10F0h` (4.336 Byte).
- VM-Headerposition bei `00CCh`: `000CF400h`.
- Map-Blockhandle im VM-Header: `0044h`.

Der VM-Header liegt damit am Dateiende bei `CF400h`; die Datenblöcke liegen davor. Der Headerbereich endet innerhalb der Datei bei `D04F0h`.

## 2. VM-Blockverzeichnis: relevante Handles

Das vorhandene PC/GEOS-1.x-VM-Leseformat aus dem Projekt-SDK wurde auf die unveränderte TOKEN.DB angewendet. Die folgenden Einträge stammen aus dem VM-Blockhandle-Verzeichnis:

| VM-Handle | Datei-Offset | Größe | Flags | statische Einordnung |
|---:|---:|---:|---:|---|
| `0044h` | `00D0h` | 16 | `00FFh` | VM-Map-Block |
| `0080h` | `DAB50h` | 56.864 | `01FFh` | großer LMem-Block mit Token-/Metadatentexten |
| `00BCh` | `15780h` | 8.256 | `01FFh` | LMem-Block mit zahlreichen 48×14-Moniker-Payloads |
| `0470h` | `51340h` | 8.256 | `01FFh` | LMem-Block mit zahlreichen 48×14-Moniker-Payloads |
| `03D4h` | `2E040h` | 8.080 | `01FFh` | LMem-Block mit 48×30-Payloads |
| `0DF4h` | `C5820h` | 7.664 | `01FFh` | LMem-Block mit 48×30-Payloads |
| `1010h` | `AE A60h` | 2.192 | `01FFh` | LMem-Block mit mehreren Grafik-/Moniker-Chunks |

Hinweis: Die Handles sind VM-Blockhandles, keine Dateioffsets. Die Flags werden als Rohwerte wiedergegeben; eine vollständige symbolische Dekodierung aller Flagbits ist nicht Gegenstand dieser Untersuchung.

## 3. Haupt-Tokenbereich in VM-Block 0080h

VM-Block `0080h` beginnt bei Datei-Offset `DAB50h` und enthält einen LMem-Block. In seinem Datenbereich liegen unter anderem folgende ASCII-Kennungen:

| Token | Offset innerhalb des VM-Blockdatenbereichs | Datei-Offset |
|---|---:|---:|
| `WP00` | `01FCh` und `6A00h` | `DAD4Ch`, `E1550h` |
| `WDAT` | `0216h` und `6A1Ah` | `DAD66h`, `E156Ah` |
| `DP00` | `018Ch`, `0DE6h`, `0E9Eh`, `134Eh`, `6990h`, `75EAh`, `76A2h`, `7B52h` | jeweils Blockoffset plus `DAB50h` |
| `DDAT` | `01AEh`, `0E3Ch`, `69B2h`, `7640h` | jeweils Blockoffset plus `DAB50h` |
| `PAPR` | `0BF6h`, `73FAh` | `DB746h`, `E1F4Ah` |
| `gDOC` | `0A58h`, `725Ch` | `DB5A8h`, `E1DACh` |

Damit sind die in Untersuchung 2421 gefundenen Token nicht nur als Treffer in der Gesamtdatei bestätigt, sondern einem konkreten VM-Block zugeordnet. Die beiden wiederkehrenden Vorkommen von `WP00/WDAT`, `PAPR` und `gDOC` liegen im selben VM-Block.

### 3.1 Bytekontexte

Im Bereich um `WP00` bei Blockoffset `01FCh` folgt im selben Datenstrom nach 26 Byte die Kennung `WDAT`. Das Muster ist:

```
... 57 50 30 30 00 00 74 00 46 00 ...
... 57 44 41 54 00 00 74 00 4A 00 ...
```

Im Bereich um `PAPR` bei `0BF6h`:

```
50 41 50 52 FF 00 74 00 DC 01 00 00 ...
```

Im Bereich um `gDOC` bei `0A58h`:

```
67 44 4F 43 FF 00 74 00 9C 01 00 00 ...
```

Die Herstellerkennung `FF 00` ist bei den Provider-Tokenmustern unmittelbar nach dem vierstelligen Token sichtbar. Bei den WP00/WDAT- und DP00/DDAT-Mustern ist diese Byteposition nicht identisch belegt. Die nachfolgenden Werte werden hier noch nicht als Icon-Handles oder Moniker-IDs interpretiert.

## 4. Grafik-/Monikerblöcke – getrennt von der Tokenliste

Die VM-Blockdaten von `00BCh` und `0470h` sind ebenfalls LMem-Blöcke. Ihre ersten Chunks beginnen mit wiederkehrenden Moniker-Kopfdaten:

- VM-Block `00BCh`, erster Chunk: `61 30 00 0E 00 1A ...` – Maße 48×14.
- VM-Block `0470h`, erster Chunk: `61 30 00 0E 00 1A ...` – Maße 48×14.
- VM-Block `03D4h`, erster Chunk: `46 30 00 1E 00 1A ...` – Maße 48×30.
- VM-Block `0DF4h`, erster Chunk: `46 30 00 1E 00 1A ...` – Maße 48×30.

Diese Daten stimmen strukturell mit den bereits untersuchten Provider-/Desktop-Monikerformaten überein. Sie belegen, dass TOKEN.DB selbst zahlreiche Grafik-/Moniker-Payloads enthält.

**Wichtige Grenze:** In dieser Untersuchung ist noch kein Zeiger von einem konkreten Token-Datensatz in Block `0080h` auf einen konkreten Chunk in den Grafikblöcken nachgewiesen. Die räumliche Nähe in der Datenbank oder die ähnliche Moniker-Kopfform reicht dafür nicht aus.

## 5. Was Untersuchung 2422 sicher feststellt

1. TOKEN.DB ist ein GEOS-VM-Container mit VM-Header bei `CF400h`, Größe `10F0h`, Map-Handle `0044h`.
2. Der große VM-Block `0080h` enthält die zentralen sichtbaren Tokenfolgen für GeoWrite, GeoDraw und die Provider PAPR/gDOC.
3. Die Tokenfolgen liegen in einem LMem-Datenblock; die konkreten Blockoffsets sind nun bekannt.
4. Die Datenbank enthält separate LMem-Blöcke mit zahlreichen 48×14- und 48×30-Moniker-Payloads.
5. Der direkte Token-Datensatz-zu-Moniker-Verweis ist noch nicht aufgelöst.

## 6. Nächster Schritt – Untersuchung 2423

1. Die LMem-Chunk-Verzeichnisse und Datensatzgrenzen in VM-Block `0080h` vollständig und korrekt dekodieren.
2. Die Token-Datensatzfelder bytegenau vergleichen: `WP00/WDAT`, `DP00/DDAT`, `PAPR`, `gDOC`.
3. Die dort enthaltenen Offset-/Handlewerte gegen VM-Blockhandles und Chunk-IDs der Grafikblöcke testen.
4. Wiederholte Token-Vorkommen nach Funktion unterscheiden (z.B. Primärdatensatz, Alias, Index oder weitere Metadaten) – nicht allein anhand der Häufigkeit benennen.
5. Erst nach einem nachvollziehbaren Verweis die Token-zu-Icon-Kette als bewiesen dokumentieren.

## 7. Sicherheit und Reproduzierbarkeit

Die Analyse erfolgte ausschließlich lesend. Die originale TOKEN.DB wurde nicht verändert. Es wurde keine GEOS.INI angepasst, kein Provider installiert, kein GEOTEST-Build erstellt und kein Laufzeiterfolg behauptet.
