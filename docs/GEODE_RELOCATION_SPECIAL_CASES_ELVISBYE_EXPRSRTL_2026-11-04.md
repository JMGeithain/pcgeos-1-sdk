# PC/GEOS 1.x – ELVISBYE.GEO / EXPRSRTL.GEO relocation special-case audit

Date: 2026-11-04  
Status: static byte analysis; no runtime validation  
Scope: GeoWorks / PC/GEOS 1.x only. No inference from PC/GEOS 2.x or FreeGEOS.

## Question

Determine what the unusual relocation info bytes `DDh` and `63h` mean in resource 10 of `ELVISBYE.GEO` and `EXPRSRTL.GEO`, compared with `SENDFAX2.GEO`.

## Provenance

All three files were read unchanged from `GEOWORKS(4).zip`.

| Archive member | Bytes | SHA-256 |
|---|---:|---|
| `.../ELVIS/ELVISBYE.GEO` | 4,240 | `880f61d25a3728574df74ec524bc2d589ead610511ca507cc8eb2410c2780eb8` |
| `.../EXPRESS/EXPRSRTL.GEO` | 4,240 | `ee8b1fc7a2b1185a3773a2b86d62888350fe64dae94efb1daff33c9fd010ebfb` |
| `.../SENDFAX/SENDFAX2.GEO` | 4,240 | `bcf55d2381a42f9fc6b5559a60d1bc753e4fe27a3bf54df901801eec50777bf5` |

## Resource 10 and the four-byte relocation record

Resource 10 starts at file offset `0C98h`; its declared size is `03F0h`. The relocation stream therefore begins at file offset `1088h` (`0C98h + 03F0h`). In these files it contains four bytes, i.e. one four-byte record.

| File | Bytes at `1088h` | Info | Extra | Offset word |
|---|---|---:|---:|---:|
| ELVISBYE.GEO | `DD 02 DD 02` | `DDh` | `02h` | `02DDh` |
| EXPRSRTL.GEO | `63 02 63 02` | `63h` | `02h` | `0263h` |
| SENDFAX2.GEO | `23 00 00 00` | `23h` | `00h` | `0000h` |

Each row is one four-byte record, not two records. The split into info byte, extra byte and 16-bit offset follows the four-byte record model used in the prior 1.x analysis. `23h` is already associated with `GRS_RESOURCE / GRT_CALL` in the earlier original-file audit. The semantics of `DDh` and `63h` remain unproven.

## The 68-word repeated sequence

In the initialized resource data, offsets `0368h–03EFh` contain 136 bytes, or 68 little-endian words:

- ELVISBYE: 68 copies of `DD 02`, i.e. word value `02DDh`.
- EXPRSRTL: 68 copies of `63 02`, i.e. word value `0263h`.
- SENDFAX2: a heterogeneous sequence at the same location, not 68 copies of one word.

The two target offsets lie within resource 10:

- ELVIS target `02DDh`: `0D 80 0D 00 D8 00 D0 0D DD 00 D0 0D D0 0D 00 D0 ...`
- EXPRESS target `0263h`: `88 00 FE DD 17 D0 0D 80 0D 00 D8 00 D8 0D DD 08 ...`

This is a strong structural correlation: the 68 data words repeat the same offset value found in the corresponding single relocation record. The 68-word sequence is initialized resource data, not the relocation stream. Whether it is a special offset/pointer array, compressed data structure, or another application-specific table is not established.

## Resource comparison

The resource-10 bytes of ELVISBYE and EXPRSRTL are identical except for the 68 words in `0368h–03EFh`, where `02DDh` is replaced by `0263h`. Their single relocation records correspondingly differ in the info byte and offset word.

SENDFAX2 shares portions of resource 10, including the inspected sequence beginning at `0348h`, but has a different structure from `0368h` onward and the comparison record `23 00 00 00`.

## Formal nibble split and evidence limit

Nachtrag 1045 records that `GRI_SOURCE` is the upper nibble and `GRI_TYPE` the lower nibble. Thus:

- `DDh` → source nibble `Dh`, type nibble `Dh`.
- `63h` → source nibble `6h`, type nibble `3h`.
- `23h` → source nibble `2h`, type nibble `3h`.

The values `DDh` and `63h` are outside the subset semantically assigned so far from the examined GeoWorks 1.x original files. Their meaning is **OPEN**. The nibble split alone proves neither that they are valid loader operations nor that the files are damaged. Loader acceptance cannot be confirmed without tracing the original 1.x loader or performing a controlled runtime test.

## Unconfirmed working hypothesis

The match between the 68 repeated offset words and the offset word in the corresponding relocation record may indicate an application-specific offset table pointing to one shared data block, while the relocation record describes a special resource relationship. This is only a hypothesis. We have not yet shown how the 68 words are consumed at runtime or how the loader interprets `GRI_info=DDh` / `63h`.

## Next checks

1. Reconcile resource 10 with every resource-directory entry and establish the meaning of the extra byte `02h`.
2. Search the other ELVISBYE and EXPRSRTL resources for references or consumers of `0368h–03EFh` and targets `0263h` / `02DDh`.
3. Compare the identical code/data areas of both applications and inspect the 68-word sequence in the context of its consumers.
4. Search more hash-identified GeoWorks 1.x originals for `GRI_info=DDh` and `63h`.
5. Trace the original 1.x loader path for relocation info bytes before implementing any parser rule or SDK exception.
6. Only after static clarification consider a controlled runtime test on a disposable working copy.

## SDK consequence

The parser must neither silently accept `DDh` and `63h` as ordinary relocation types nor reject them as definitely invalid at this stage. Record them as open special cases. No parser change and no patch to original files follows from this audit.

## Reproducibility and limits

The three archive members were read directly from the ZIP; sizes, SHA-256 values, raw bytes and difference ranges were recalculated. Resource 10's relocation position is derived from `0C98h + 03F0h = 1088h`. The 68 word values were counted as 16-bit little-endian words over `0368h–03EFh`. This is static byte analysis, not a GeoManager loader test or a complete GEODE specification.


## Archive-wide search for the two 68-word sequences

An additional search was run across the complete `GEOWORKS(4).zip` archive:

- Scope: 263 archive members with the `.GEO` extension.
- Exact contiguous 136-byte patterns searched:
  - `DD 02` repeated 68 times.
  - `63 02` repeated 68 times.
- Result: the first complete pattern occurs only in `ELVISBYE.GEO`; the second occurs only in `EXPRSRTL.GEO`.
- Neither complete pattern was found in the other 261 GEO files.

**Evidence limit:** This is an exact-pattern search for these two complete 136-byte sequences. It is not a complete decoder of all relocation tables and does not establish that the archive contains no other unknown `GRI_info` values. In particular, it does not semantically classify all individual occurrences of bytes `DDh` or `63h`.


## Byte-level occurrences of the target offset words outside the repeated table

A further raw-byte scan searched the two complete GEO files for the little-endian words `02 DD` (ELVIS target offset) and `63 02` (EXPRESS target offset).

- In ELVISBYE, five additional occurrences of `DD 02` occur in resource 10 at file offsets `0D0Eh`, `0E69h`, `0E80h`, `0E86h`, and `0EB3h` (resource-relative offsets `0076h`, `01D1h`, `01E8h`, `01EEh`, `021Bh`).
- The bytes surrounding all five occurrences are identical in ELVISBYE and EXPRSRTL.
- In EXPRSRTL, no additional occurrence of `63 02` was found outside the 68-word repeated table and the four-byte relocation record.

**Interpretation limit:** These are raw byte matches, not proven code references. Without disassembly, entry-point context, or runtime observation, they cannot be called pointer consumers. The asymmetry is recorded as a lead for subsequent analysis, not as evidence that the two applications use different relocation semantics.


## Correction/qualification: bitmap GString context

A byte-level recheck of the beginning of resource 10 identifies a bitmap command immediately before the data region:

- Resource-relative offset `002Fh` (file offset `0CC7h`): opcode `1Ah`.
- It is followed by `B6 03`, the little-endian value `03B6h`.
- Next are `40 00 28 00`, followed by bitmap data.
- The bitmap data begins at resource-relative offset `0036h`.

The arithmetic `0036h + 03B6h = 03ECh` exactly matches the value `03ECh` stored in the resource header at offset `0008h`. The header also contains `03F0h` at offset `0014h`; the relocation stream begins at resource-relative `03F0h` (file offset `1088h`). This is strong structural evidence that the `03B6h)-byte sequence beginning at `0036h` is the bitmap-data region ending immediately before `03ECh`. The exact semantics of every resource-header field are not yet fully specified.

This requires an important qualification of the earlier interpretation:

- Resource-relative range `0368h–03EBh` is 132 bytes = 66 words and lies inside the bitmap-data region described by the bitmap command.
- The final four bytes `03ECh–03EFh` (two more words `DD 02` or `63 02`) lie after the calculated bitmap-data end, but remain inside the declared resource size `03F0h`.
- Thus, the previously described 68-word run is **not an established pointer table**. At least 66 of the 68 words are bitmap-data bytes; the final two words are a separate four-byte tail whose meaning remains open.
- Target offsets `02DDh` and `0263h` also lie inside the bitmap-data range `0036h–03EBh`.
- The five additional raw `DD 02` matches at resource-relative offsets `0076h`, `01D1h`, `01E8h`, `01EEh`, and `021Bh` also lie inside that bitmap-data region. They must not be called code-pointer references.

The 68-fold byte repetition remains a correct observation. Its interpretation as an offset/pointer table is withdrawn. One possible explanation is that these values belong to the encoded bitmap representation; the precise bitmap compression/data format has not yet been fully decoded.

**Consequence for further work:** The relocation record `DD 02 DD 02` or `63 02 63 02` has an offset word that lands inside a region structurally identified as bitmap data. This makes a special GString/bitmap relocation relationship a new working hypothesis. It does not prove which loader operation `GRI_info=DDh` or `63h` performs.

This qualification supersedes the earlier pointer-table hypothesis. The byte observations remain valid; only their interpretation is corrected.


## 13. Korrektur/Präzisierung: Einbettung in den Bitmap-GString

Eine erneute bytegenaue Prüfung des Anfangs von Ressource 10 zeigt unmittelbar vor dem auffälligen Datenbereich einen GString-Bitmap-Befehl:

- Ressourcenrelativer Offset `002Fh` (Dateioffset `0CC7h`): Opcode `1Ah`.
- Darauf folgen `B6 03`, als Little-Endian-Wert `03B6h`.
- Danach stehen `40 00 28 00` sowie die Bitmap-Daten.
- Der Beginn der Bitmap-Daten liegt bei Ressourcenoffset `0036h`.

Die Rechnung `0036h + 03B6h = 03ECh` stimmt exakt mit dem im Ressourcenheader bei Offset `0008h` gespeicherten Wert `03ECh` überein. Der Ressourcenheader enthält außerdem bei Offset `0014h` den Wert `03F0h`; der Relokationsstrom beginnt bei `03F0h` relativ zur Ressource (Dateioffset `1088h`). Das ist ein starker struktureller Beleg dafür, dass die `03B6h`-Bytefolge ab `0036h` den Bitmap-Datenbereich bis unmittelbar vor `03ECh` beschreibt. Die exakte Semantik sämtlicher Ressourcenheaderfelder ist damit noch nicht vollständig spezifiziert.

Daraus folgt eine wichtige Präzisierung der früheren Interpretation:

- Der Bereich `0368h–03EBh` umfasst 132 Bytes = 66 Wörter und liegt innerhalb des durch den Bitmap-Befehl beschriebenen Datenbereichs.
- Die letzten vier Bytes `03ECh–03EFh` (zwei weitere Wörter `DD 02` bzw. `63 02`) liegen nach dem berechneten Bitmap-Datenende, aber noch innerhalb der Ressourcengröße `03F0h`.
- Der zuvor als 68-Wort-Tabelle beschriebene Gesamtbereich ist also **keine nachgewiesene Pointertabelle**. Mindestens 66 der 68 Wörter sind Teil der Bitmap-Datenbytes; die letzten zwei Wörter sind ein separater vier Byte langer Restbereich, dessen Bedeutung offen bleibt.
- Die Zieloffsets `02DDh` und `0263h` liegen ebenfalls innerhalb des Bitmap-Datenbereichs `0036h–03EBh`.
- Die fünf zusätzlichen Rohbyte-Treffer von `DD 02` bei Ressourcenoffsets `0076h`, `01D1h`, `01E8h`, `01EEh` und `021Bh` liegen ebenfalls im Bitmap-Datenbereich. Sie dürfen daher nicht als Code-Pointer-Referenzen bezeichnet werden.

Die 68-fache Wiederholung ist weiterhin als bytegenaue Beobachtung korrekt. Ihre Deutung als Offset-/Pointertabelle wird jedoch zurückgenommen. Eine mögliche Erklärung ist, dass die Werte zur kodierten Bitmapdarstellung gehören; das genaue Kompressions-/Bitmapdatenformat ist hier noch nicht vollständig dekodiert.

**Folgerung für die weitere Arbeit:** Der Relokationseintrag `DD 02 DD 02` bzw. `63 02 63 02` verweist mit seinem Offsetwort in einen Bereich, der strukturell als Bitmapdatenbereich ausgewiesen ist. Das macht eine spezielle GString-/Bitmap-Relokationsbeziehung zu einer neuen Arbeitshypothese. Es beweist noch nicht, welche Loader-Operation `GRI_info=DDh` oder `63h` ausführt.

Diese Präzisierung ersetzt die frühere Vermutung einer 68-Einträge-Pointertabelle. Alle Bytebeobachtungen bleiben erhalten; nur die Interpretation wird korrigiert.


## 14. Kontrollvergleich mit SENDFAX2.GEO

Als Kontrollfall wurde dieselbe Ressource 10 in `SENDFAX2.GEO` untersucht. Die drei Dateien besitzen an den geprüften Strukturstellen denselben Aufbau:

- Ressourcenheader ab Dateioffset `0C98h` mit dem Wert `03ECh` bei Ressourcenoffset `0008h` und `03F0h` bei Ressourcenoffset `0014h`.
- GString-Bitmap-Opcode `1Ah` bei Ressourcenoffset `002Fh`.
- Danach derselbe Längenwert `03B6h` und dieselben vier Bytes `40 00 28 00`.
- Der Bitmap-Datenbereich beginnt damit in allen drei Fällen bei `0036h`; die Rechnung `0036h + 03B6h = 03ECh` ist für alle drei identisch.
- Der Relokationsstrom beginnt in allen drei Dateien bei Ressourcenoffset `03F0h`.

Der Vergleich des Ressourcenendes zeigt jedoch drei unterschiedliche Datenmuster:

| Datei | Ressourcenoffset `03ECh–03EFh` | Relokationsdatensatz ab `03F0h` |
|---|---|---|
| `ELVISBYE.GEO` | `DD 02 DD 02` | `DD 02 DD 02` |
| `EXPRSRTL.GEO` | `63 02 63 02` | `63 02 63 02` |
| `SENDFAX2.GEO` | `00 00 00 00` | `23 00 00 00` |

Damit ist jetzt ein zusätzlicher Vergleichspunkt gesichert: In ELVISBYE und EXPRSRTL wiederholt sich das jeweilige Zwei-Byte-Muster unmittelbar über die rechnerische Bitmap-Datengrenze hinweg und anschließend nochmals im vier Byte langen Relokationsdatensatz. In SENDFAX2 endet der Bitmap-Datenbereich dagegen mit vier Nullbytes; der Relokationsdatensatz ist der bislang zugeordnete Wert `23 00 00 00`.

**Was dieser Vergleich belegt:** Die Ressource und der Bitmap-GString-Aufbau sind nicht nur zufällig ähnlich; die drei Dateien teilen dieselben Strukturwerte und dieselbe berechnete Bitmap-Datengrenze. Zugleich ist das auffällige `DD 02`-/`63 02`-Muster nicht einfach ein allgemeines Merkmal jeder solchen Ressource: Im Kontrollfall SENDFAX2 tritt es an dieser Stelle nicht auf.

**Was weiterhin offen bleibt:** Der Vergleich erklärt nicht, warum die Bytes `DD 02` bzw. `63 02` in ELVISBYE/EXPRSRTL sowohl am Ende des Bitmap-Datenbereichs als auch im Relokationsdatensatz stehen. Er beweist insbesondere nicht, dass die vier Bytes bei `03ECh–03EFh` vom Bitmap-Decoder gelesen werden oder dass der Loader sie als Verweis auf Bitmapdaten behandelt. Die Beziehung zwischen Bitmap-Ende, vier Byte langem Ressourcenrest und Relokationsdatensatz bleibt daher eine gezielte offene Frage.

### Aktualisierte nächste Prüfschritte

1. Die GString-Bitmap-Kommando-Spezifikation für Opcode `1Ah` anhand einer originalen PC/GEOS-1.x-Quelle verifizieren: insbesondere Bedeutung des Längenworts, der Koordinatenbytes und die Frage, ob die Länge ausschließlich Bitmapdaten oder einen größeren Befehlsteil umfasst.
2. Die letzten 16 bis 32 Bytes des Bitmap-Datenbereichs in allen drei Dateien vergleichen und prüfen, ob `DD 02`/`63 02` in ELVISBYE/EXPRSRTL als reguläre komprimierte Bitmapdaten dekodierbar sind.
3. Den vier Byte langen Bereich `03ECh–03EFh` getrennt vom Bitmapdatenbereich und getrennt vom Relokationsstrom behandeln, bis seine Funktion nachgewiesen ist.
4. Im originalen GeoManager-Lader die Verarbeitung des Relokationsdatensatzes `DD 02 DD 02` bzw. `63 02 63 02` verfolgen. Erst daraus lässt sich die Bedeutung der Info-Bytes belastbar bestimmen.

**SDK-Folge:** Keine Änderung an Parser oder Loaderannahmen. `SENDFAX2.GEO` ist ein nützlicher struktureller Kontrollfall, aber kein Beweis für die Bedeutung der unbekannten Werte `DDh` und `63h`.


## 15. RLE-Hinweis zur Folge DD 02 (Vergleichsquelle, noch kein PC/GEOS-Beweis)

Bei der Prüfung der Bitmapdaten fiel auf, dass die Folge `DD 02` auch als mögliches Kompressionsmuster gelesen werden kann. Eine veröffentlichte technische Beschreibung der Bitmapkompression von Commodore-GEOS nennt `DD–FF` als Bigcount-Marker: Auf den Marker folgt ein Bigcount-Byte; anschließend werden die folgenden `count - DC` Bytes entsprechend dem Bigcount wiederholt und als innerer Datenstrom nach Repeat-/Unique-Regeln interpretiert. Für `DD 02` bedeutet dies nicht, dass die beiden Bytes isoliert ein vollständiges Paket bilden; die nachfolgenden Bytes müssen in die Dekodierung einbezogen werden.

**Wichtige Versions- und Plattformgrenze:** Die Beschreibung bezieht sich auf Commodore-GEOS und Photo Scraps/BitmapUp. Sie ist keine Spezifikation von PC/GEOS 1.x und darf nicht ungeprüft auf den GString-Bitmapbefehl übertragen werden.

### Bytegenaue Einordnung

- Im Bereich `0368h–03EBh` liegen 132 Bytes, also 66 Paare `DD 02` in ELVISBYE bzw. `63 02` in EXPRSRTL.
- Im Bereich `03ECh–03EFh` liegen weitere vier Bytes, also zwei weitere Paare außerhalb des rechnerischen Bitmapdatenbereichs.
- Bei SENDFAX2.GEO ist diese repetitive Folge nicht vorhanden; der entsprechende Bereich enthält eine andere Bytefolge.

Nach der Commodore-GEOS-Tabelle wäre `63h` ein Unique-Marker (`81h–DBh`) und würde 227 wörtliche Bytes ankündigen. Das passt nicht unmittelbar zur beobachteten alternierenden Folge `63 02`. Damit zeigt gerade EXPRSRTL, warum eine ungeprüfte Übertragung dieser Fremdplattformregel unzulässig ist.

### Ergebnis und Konsequenz

1. `DD 02` ist formal mit einem Bigcount-Anfang der dokumentierten Commodore-GEOS-Kompression vereinbar; die vollständige Dekodierung hängt aber von den nachfolgenden Bytes ab.
2. Dieselbe Regel erklärt `63 02` nicht als entsprechende kurze Wiederholung.
3. Es liegt weiterhin kein Nachweis vor, dass PC/GEOS 1.x dieselbe Kompression oder dieselben Kontrollbytes verwendet.
4. Der PC/GEOS-1.x-Decoder bzw. eine originale 1.x-Spezifikation muss direkt untersucht werden.

**SDK-Regel:** Keine Parseränderung. Commodore-GEOS-Dokumentation bleibt eine ausdrücklich gekennzeichnete Vergleichsquelle und ist kein Beleg für das PC/GEOS-1.x-Binärformat.
