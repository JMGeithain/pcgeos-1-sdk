# GeoWrite 1.x – Rohstruktur der Seiten-Selbstverweise und Objektverkettung (Untersuchung 2408)

## Ziel

Die drei in Untersuchung 2407 als Selbstreferenzen identifizierten ObjRelocationIDs werden hier im lokalen Byteumfeld ihrer LMem-Chunks betrachtet. Ziel ist, belegte Nachbarschaftsmuster festzuhalten, ohne unbekannte WORD-Felder vorschnell zu benennen.

## Geprüfte Daten

Datei: `SOLAR_DE.000`  
Seitenblöcke: 21  
LMem-Chunks: `0022h`, `0030h`, `0032h`, `0042h`  
Vergleich: vollständige Payloads der 21 Seitenblöcke.

## Chunk 0022h – Seiteninhalt

Payload-Länge: 104 Bytes.

In Seite 1 stehen die beiden Relokations-WORDs an Payload-Offsets `0x4C` und `0x56`. Die unmittelbar davorliegenden WORDs lauten jeweils `0022h`. Die Rohbytefolgen sind:

- Offset `0x4A`: `22 00 04 70`
- Offset `0x54`: `22 00 04 70`

Auf Seite 2 sind die Folgen entsprechend:

- Offset `0x4A`: `22 00 47 70`
- Offset `0x54`: `22 00 47 70`

Die beiden Relokations-WORDs sind auf jeder Seite identisch und lösen auf den jeweiligen Seiten-VM-Block selbst auf. Die benachbarten WORDs `0022h` bleiben über alle Seiten gleich.

## Chunk 0030h – zweiter veränderlicher Chunk

Payload-Länge: 89 Bytes.

Die Relokationskennung beginnt bei Payload-Offset `0x17`. In der Rohdatenfolge steht sie unmittelbar nach dem WORD `0022h`:

- Seite 1 ab Offset `0x15`: `22 00 04 70`
- Seite 2 ab Offset `0x15`: `22 00 47 70`

Auch dieser Relokationswert ist pro Seite identisch mit den beiden Werten in Chunk `0022h`.

## Chunk 0032h – sichtbarer Seitentext

Dieser Chunk enthält den sichtbaren Text `Unser Sonnensystem  |  n/21` einschließlich Nullterminierung. Bei Seiten 1–9 ist der Chunk 28 Bytes lang; ab Seite 10 sind es 29 Bytes. Die zusätzliche Byteposition entsteht durch die zweistellige Seitennummer.

## Chunk 0042h – unbekanntes Bytefeld

Payload-Länge: 39 Bytes. An Offset `0x14` enthalten die Seiten 1–9 den Wert `A1h`, die Seiten 10–21 den Wert `A8h`. Alle übrigen Bytes dieses Chunks sind im Vergleich über die 21 Seiten unverändert.

Die Korrelation mit dem Wechsel auf zweistellige Seitenzahlen ist belegt. Eine semantische Erklärung für das Feld ist nicht gefunden.

## Abgleich mit dem Konverter

`convertGeoWrite.asm` greift auf `GW12_PageContent = 22h` zu, folgt danach `VCI_comp.CP_firstChild.offset` und später `VI_link.LP_next`. Bei der Auflösung einer nicht-parentalen Verknüpfung wird `RelocToVMBlock` aufgerufen.

Das belegt den allgemeinen Ablauf der Seitenobjektverfolgung. Es reicht jedoch nicht aus, jedes benachbarte WORD in den Beispiel-Chunks einer konkreten Strukturkomponente zuzuordnen. Insbesondere sind die beiden vor den Selbstreferenzen stehenden `0022h`-WORDs noch nicht semantisch identifiziert.

## Gesicherte Aussagen und offene Fragen

Gesichert:
1. Die drei variablen WORDs sind `ORS_NON_STATE_VM`-Relokationskennungen.
2. Alle drei verweisen auf den eigenen Seiten-VM-Block.
3. Die beiden Relokations-WORDs in Chunk `0022h` stehen jeweils nach einem unveränderlichen WORD `0022h`.
4. Die Relokations-WORDs in Chunk `0030h` stehen ebenfalls nach einem unveränderlichen WORD `0022h`.
5. Der Konverter verfolgt visuelle Objektverknüpfungen und löst VM-Relokationen auf.

Offen:
1. Ob die vorangestellten `0022h`-WORDs Chunkhandles, Offsets oder andere Objektfelder sind.
2. Welche konkreten Objekte über die drei Selbstreferenzen adressiert werden.
3. Welche Struktur und Funktion Chunk `0030h` im Seitenobjektbaum besitzt.
4. Was das Byte `A1h/A8h` in Chunk `0042h` steuert.

## Konsequenz für GEOTEST

Die Selbstreferenzen können beim späteren Erzeugen einer neuen Datei aus der tatsächlichen VM-Blocktabellenposition generiert werden. Die sie umgebenden Felder dürfen dagegen noch nicht verändert oder synthetisch erzeugt werden. Der nächste Schritt ist, die in `convertGeoWrite.asm` verfolgten Objektfelder mit den konkreten Klassendefinitionen und Objektinstanzen des Dokuments abzugleichen.

## Quellen und Methode

- `SOLAR_DE.000`, 21 Seitenblöcke, VM1-/LMem-Parsing mit `vm1.py`.
- `convertGeoWrite.asm`, Seitenverarbeitung `pageLoop` und `columnLoop`.
- `convertText.asm`, Routine `RelocToVMBlock`.
- `object.def`, `ObjRelocationID` und `ORS_NON_STATE_VM`.

Statische Byteanalyse und Quelltextabgleich; kein GeoWrite-Laufzeittest.
