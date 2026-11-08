# PC/GEOS 1.x GEODE-Relocations – Neubewertung und Korrektur

**Datum:** 2026-11-08  
**Projekt:** `JMGeithain/pcgeos-1-sdk`  
**Branch:** `main`  
**Untersuchungsfortsetzung:** 2041–2050  
**Geltungsbereich:** ausschließlich GeoWorks / PC/GEOS 1.x. PC/GEOS 2.x und FreeGEOS werden nicht als Beleg für 1.x-Verhalten verwendet.

## 1. Anlass und Korrektur früherer Chat-Auswertungen

Die Gesprächsauswertungen 1991–2040 enthielten mehrere Fehlinterpretationen. Sie hatten Relocation-Daten teilweise unmittelbar hinter `resource_position + resource_size` gelesen und die ersten zwei Bytes eines Datensatzes als WORD zusammengefasst. Beides widerspricht dem bereits im Repository dokumentierten GEODE-Formatmodell und dem Parser `pcgeos1/geode.py`.

Diese Neubewertung ersetzt die betreffenden früheren Aussagen:

- Relocation-Daten beginnen bei den vom aktuellen 1.x-Parser unterstützten Dateien bei `resource_position + align16(resource_size)`, nicht allgemein direkt hinter den initialisierten Ressourcendaten.
- Ein Relocation-Datensatz ist vier Byte lang und wird als `<BBH>` gelesen: `info`, `extra`, `target_offset`.
- `info` ist ein Byte. Oberes Nibble: `source = info >> 4`; unteres Nibble: `type = info & 0x0F`.
- `extra` ist ein eigenständiges Byte.
- `target_offset` ist ein 16-Bit-Little-Endian-Wert.
- Eine Big-Endian-Deutung der letzten beiden Bytes ist keine zulässige allgemeine Korrektur. Sie entstand in den vorherigen Chat-Antworten teilweise durch falsch positionierte Relocation-Streams oder durch Sonderdateien.

Die vorigen Aussagen über vermeintliche Relocation-Klassen `0014`, `0022`, `0023`, `0024` als WORD-Typen, über eine allgemeine Big-Endian-Variante und über 806 ungültige Offsets werden hiermit ausdrücklich zurückgenommen. Diese Werte müssen als Bytefelder und unter Berücksichtigung der richtigen Streamposition neu bewertet werden.

## 2. Maßgebliches Parsermodell im Repository

Die bestehende Implementierung `pcgeos1/geode.py` verwendet für GEOS 1.x:

```python
reloc_at = resource_file_offset + align16(resource_size)
info, extra, target = struct.unpack_from('<BBH', data, reloc_at)
source = info >> 4
type = info & 0x0F
```

mit:

```python
def align16(n):
    return (n + 15) & ~15
```

Der Parser prüft außerdem:

- Relocation-Bytezahl ist durch vier teilbar.
- Zieloffset plus zwei Bytes liegt innerhalb der initialisierten Ressource.
- Source-Klasse liegt im derzeit akzeptierten Bereich 0–2.
- Relocation-Typ liegt im derzeit akzeptierten Bereich 0–5.
- Bei Source-Klasse 1 ist `extra` ein gültiger Importindex.
- Ressourcengrenzen und Überlappungen sind konsistent.

Dies ist das derzeit implementierte, durch mehrere Originaldateien statisch gestützte SDK-Modell. Es ist keine vollständige, durch Laufzeit-Tracing bewiesene Spezifikation aller historischen GEODE-Loaderpfade.

## 3. Untersuchungen 2041–2050

### 2041 – Parserdefinition gegen die Originaldateien abgeglichen

Die im Repository vorhandene Implementierung wurde gelesen und als Referenz für die erneute Byteauswertung verwendet. Die drei Relocation-Felder sind `info` (BYTE), `extra` (BYTE) und `target_offset` (WORD Little Endian). Die frühere Interpretation der ersten beiden Bytes als gemeinsames WORD ist verworfen.

### 2042 – Archivweite Zählung mit korrekter Streamposition

Das Archiv `/mnt/data/GEOWORKS.zip` enthält 263 `.GEO`-Einträge. Davon besitzen 260 die 1.x-Signatur `C7 45 CF 53`.

Unter Verwendung der Ressourcentabellen und der Absatz-Ausrichtung wurden insgesamt 102.365 vier Byte lange Relocation-Datensätze gezählt. Diese Zahl ist eine Inventur der deklarierten Relocation-Bytebereiche; sie bedeutet ausdrücklich nicht, dass alle Datensätze durch den derzeitigen Parser semantisch akzeptiert werden.

### 2043 – NOTEPAD.GEO als Kontrollfall

Datei: `GEOWORKS/DOCUMENT/NOTEPAD.GEO`  
Größe: 8.070 Bytes  
SHA-256: `3d0bbaf6640eecca7c884a3351ddd957435096af6ff0b6b02793fa9eb7286b29`

Der korrekte Parserlauf ergibt 15 Ressourcen und 105 Relocation-Datensätze. Alle Datensätze bestehen die aktuellen strukturellen Prüfungen.

- Ressource 1: 20 Datensätze; häufigste Kombinationen `(source=2,type=2,extra=0)` mit 18 Vorkommen sowie je ein Eintrag `(1,1,0)` und `(1,2,0)`.
- Ressource 2: 73 Datensätze; 67 Einträge `(0,0,0)` und 6 Einträge `(1,4,0)`.

Damit sind die früheren Deutungen, die aus einem WORD `0014h` eine Relocation-Klasse ableiteten, nicht haltbar. Die tatsächliche Info-Byte-Klasse ist `14h`, also `source=1`, `type=4`; das Zusatzbyte ist `00h`.

### 2044 – GROBJ.GEO als unabhängige Gegenprobe

Datei: `GEOWORKS/SYSTEM/GROBJ.GEO`  
Größe: 42.926 Bytes  
SHA-256: `7c30a27e2d2868393622c210e57b2103e99f0b956381815d3a65da0bc02c6383`

Der korrekte Parserlauf ergibt 20 Ressourcen, einen Import, 21 Exporte und 1.801 Relocation-Datensätze. Alle Datensätze bestehen die aktuellen strukturellen Prüfungen.

Ressource 1 enthält:

- 365 Einträge `(source=2,type=2,extra=0)`
- 32 Einträge `(source=1,type=1,extra=0)`
- 32 Einträge `(source=1,type=2,extra=0)`

Das bestätigt die Wiederkehr dieser Source-/Type-Kombinationen in einer weiteren nativen 1.x-Datei. Es bestätigt nicht allein ihre vollständige Loadersemantik.

### 2045 – SPLAY.GEO und WORLD/SPLAY.GEO

Beide Archivmitglieder sind byteidentisch:

- Größe: 31.390 Bytes
- SHA-256: `98cacf83465e6dbe2225f44bfb1a0de04dc04aeca6f8ad453397521ce9a4a646`

Der Parserlauf ergibt 14 Ressourcen und 389 Relocation-Datensätze; alle bestehen die aktuellen Prüfungen.

Ressource 2:

- Ressourcendaten beginnen bei `05C2h`.
- Initialisierte Größe `04E2h`.
- Ende der initialisierten Daten `0AA4h`.
- Relocation-Stream beginnt bei `0AB2h`.
- Padding: 14 Bytes.
- 74 Relocation-Datensätze, alle Zieloffsets innerhalb der Ressource.
- Typverteilung: 60 Einträge `(source=1,type=4,extra=2)` und 14 Einträge `(source=0,type=0,extra=0)`.

Ressource 3:

- Ressourcendaten beginnen bei `0BDAh`.
- Initialisierte Größe `194Fh`.
- Ende der initialisierten Daten `2529h`.
- Relocation-Stream beginnt bei `252Ah`.
- Padding: 1 Byte.
- 247 Relocation-Datensätze; alle bestehen die aktuellen Source-/Type-/Target-Prüfungen.
- Häufigste Kombinationen: 179 Einträge `(0,0,0)`, 34 `(1,4,1)`, 18 `(2,2,0)`, 8 `(1,4,0)` und 6 `(2,4,0)`; die übrigen zwei Einträge verteilen sich je einmal auf `(0,1,0)` und `(0,2,0)`.

Dies bestätigt für diese beiden Dateien die Absatz-Ausrichtung und das `<BBH>`-Datensatzmodell.

### 2046 – DOCUMENT/SPLAY.GEO ist eine echte Ausnahme

Datei: `GEOWORKS/DOCUMENT/SPLAY.GEO`  
Größe: 31.470 Bytes  
SHA-256: `ff492d3cf9551ea77e8a6de892bd1b817140432a22b5a9fb6edb2f048c322a68`

Diese Datei ist nicht byteidentisch mit `SPLAY.GEO`. Sie besitzt zwar dieselbe Ressourcenanzahl und dieselbe Gesamtzahl von 389 Relocation-Datensätzen, aber zwei Ressourcen bestehen die aktuellen Parserprüfungen nicht:

- Ressource 2: 66 von 74 Datensätzen verletzen mindestens eine aktuelle Source-/Type-/Target-Prüfung.
- Ressource 3: 238 von 247 Datensätzen verletzen mindestens eine aktuelle Prüfung.

Die Relocation-Streams liegen bei der erwarteten Absatz-Ausrichtung. Das Problem wird also nicht durch ein zusätzliches Umstellen auf Big Endian behoben. Die Datei bleibt ein eigenständiger, ungeklärter Kompatibilitätsfall. Sie darf nicht durch Byte-Swapping oder gelockerte Parserregeln künstlich passend gemacht werden.

### 2047 – NPLAYGCM-Varianten

`GEOWORKS/SYSAPPL/NPLAYGCM.GEO`:

- Größe: 34.698 Bytes
- SHA-256: `60b69fc28807ca5b3e4f72f68180f38fc804b24a54e814e9331b590ee135bffa`
- 14 Ressourcen, 376 Relocation-Datensätze.
- Alle Datensätze bestehen die aktuellen strukturellen Prüfungen.
- Ressource 2: 60 Einträge `(source=1,type=4,extra=2)` und 14 `(source=0,type=0,extra=0)`.

`GEOWORKS/NPLAYGCM.GEO` im Archivwurzelverzeichnis:

- Größe: 34.570 Bytes
- SHA-256: `6a685d0dfc3c9bc6ce65f9de73b98a0dea914e7d2db6871d73cf85b71762554a`
- 14 Ressourcen, 376 Relocation-Datensätze.
- Ressourcen 2 und 3 bestehen die aktuellen Parserprüfungen nicht: 70 von 74 beziehungsweise 223 von 234 Datensätzen sind auffällig.

Die SYSAPPL-Variante ist somit kein Beleg dafür, dass die Root-Variante nur mit Big Endian gelesen werden müsste. Die Root-Variante bleibt ein separater Sonderfall.

### 2048 – Paddingwerte der Sonderfälle festgehalten

Die korrekten Positionen nach `position + align16(size)` lauten:

| Datei | Ressource | Position | Größe | Ende Daten | Relocation-Start | Padding |
|---|---:|---:|---:|---:|---:|---:|
| SPLAY.GEO | 2 | `05C2h` | `04E2h` | `0AA4h` | `0AB2h` | 14 |
| SPLAY.GEO | 3 | `0BDAh` | `194Fh` | `2529h` | `252Ah` | 1 |
| SYSAPPL/NPLAYGCM.GEO | 2 | `05C2h` | `04F3h` | `0AB5h` | `0AC2h` | 13 |
| SYSAPPL/NPLAYGCM.GEO | 3 | `0BEAh` | `17BEh` | `23A8h` | `23AAh` | 2 |
| DOCUMENT/SPLAY.GEO | 3 | `0BDAh` | `1950h` | `252Ah` | `252Ah` | 0 |

Diese Beispiele zeigen, warum `position + size` als allgemeine Relocation-Position falsch ist.

### 2049 – Frühere Big-Endian-Aussagen zurückgenommen

Die früheren Chat-Aussagen, SPLAY Ressource 3 müsse Big Endian verwenden und NPLAYGCM Ressource 2 sei ebenfalls eine Big-Endian-Variante, sind falsch beziehungsweise nicht belegt. Sie beruhten auf einer falschen Stream-/Feldinterpretation.

Die korrekte Auswertung der Root-SPLAY- und SYSAPPL-NPLAYGCM-Dateien erfolgt mit `<BBH>` und Little Endian für das letzte WORD. DOCUMENT/SPLAY und Root-NPLAYGCM bleiben Parser-Ausnahmen; ihre Abweichungen sind nicht durch eine alternative Byte-Reihenfolge geklärt.

Die zuvor genannte Zahl von 806 angeblich ungültigen Offsets ist ebenfalls zurückgezogen. Die aktuelle Reanalyse klassifiziert die oben genannten Ressourcen anhand der tatsächlichen Parserregeln; eine allgemeine Zahl „ungültiger Offsets“ ohne Angabe von Datei, Ressource und Prüfkriterium wird nicht mehr verwendet.

### 2050 – Konsequenz für SDK und weitere Loaderanalyse

- `pcgeos1/geode.py` wurde nicht geändert.
- Die Originaldateien wurden nicht verändert.
- Die Parserregeln werden nicht erweitert oder gelockert, um DOCUMENT/SPLAY oder Root-NPLAYGCM passend zu machen.
- Die Sonderfälle werden getrennt dokumentiert und müssen anhand der Original-1.x-Loaderroutine untersucht werden.
- Es wurde in diesem Untersuchungsblock keine Loader-Routine abschließend identifiziert und kein Laufzeitverhalten behauptet.

Der nächste sinnvolle Schritt ist die gezielte Rückverfolgung der Loaderverarbeitung der Felder `info`, `extra` und `target_offset` im unveränderten GeoWorks-1.x-Kernel. Dabei sind die Original- und gepatchten Kernel strikt getrennt zu halten.

## 4. Reproduzierbarkeit

Die Rohdaten stammen aus den genannten Mitgliedern des vom Nutzer bereitgestellten `GEOWORKS.zip`. Die Ressourcen- und Relocation-Positionen wurden aus den GEODE-Tabellen gelesen. Die Relocation-Position wurde mit der im Repository implementierten Formel `position + align16(size)` berechnet. Datensätze wurden als vier Bytes `<BBH` dekodiert und gegen die bestehenden Parsergrenzen geprüft.

Dies ist statische Byteanalyse. Es ist kein GeoManager-Laufzeittest und keine vollständige Spezifikation aller PC/GEOS-1.x-Relocation-Varianten.

## 5. Verknüpfte Repository-Unterlagen

- `pcgeos1/geode.py` – implementierter, bounds-geprüfter GEODE-Leser.
- `docs/GEODE_FORMAT.md` – Überblick über Container- und Relocationformat.
- `docs/GEODE_RELOCATION_ALIGNMENT_AUDIT_2026-11-04.md` – Nachweis der Absatz-Ausrichtung anhand SPLAY und weiterer Donor-Dateien.
- `docs/GEODE_RELOCATION_SPECIAL_CASES_ELVISBYE_EXPRSRTL_2026-11-04.md` – offene Sonderfälle ELVISBYE / EXPRSRTL.

# Untersuchung 2051–2060 – Kernel-Einstieg und Loader-Suche

Datum: 2026-11-08  
Geltungsbereich: GeoWorks / PC/GEOS 1.x. Statische Analyse der beiden Kernel-Dateien aus dem bereitgestellten `GEOWORKS.zip`. Keine Änderungen an Kernel- oder GEO-Dateien.

## 2051 – Originaldateien und Prüfsummen

Die beiden Kernel-Dateien wurden direkt aus `GEOWORKS/KERNEL.OLD` und `GEOWORKS/KERNEL.EXE` extrahiert und mit SHA-256 geprüft:

| Datei | Bytes | SHA-256 | Provenienz im Projekt |
|---|---:|---|---|
| `KERNEL.OLD` | 72.688 | `bd4d680b15f8dd66b2b09b506de96672972f716a11e0a38220477bf07b6c1e9b` | Originaler deutscher Kernel |
| `KERNEL.EXE` | 72.736 | `c2cc8952cdb01d0f459bf281ee3b78f8ce9464aba0b58c3758f8c73e24fb6eb5` | Gepatchter englischer Kernel, im Projekt als DOSBox-kompatible Fassung geführt |

Die Dateien werden als getrennte Beweisobjekte behandelt. `KERNEL.EXE` wird nicht als unveränderte Referenz für den deutschen Originalkernel verwendet.

## 2052 – MZ-Header von KERNEL.OLD

Aus dem DOS-MZ-Header von `KERNEL.OLD` wurden folgende Felder gelesen:

| Feld | Wert |
|---|---:|
| `e_cparhdr` | `0x0060` Paragraphen |
| Headerlänge | `0x0600` Bytes |
| `e_crlc` | `0x0111` = 273 DOS-Relocation-Einträge |
| `e_lfarlc` | `0x003C` |
| `e_ip` | `0x02B1` |
| `e_cs` | `0x0000` |
| `e_ss` | `0x0E35` |
| `e_sp` | `0x15B0` |
| Dateigröße | 72.688 Bytes (`0x11BF0`) |
| nach MZ-Header verbleibender Ladebereich | 71.152 Bytes (`0x115F0`) |

Die 273 Einträge im MZ-Header sind DOS-EXE-Relocations. Sie sind nicht mit den vier Byte langen GEODE-Ressourcenrelocations gleichzusetzen. Diese Trennung ist für die weitere Untersuchung zwingend.

## 2053 – MZ-Header von KERNEL.EXE

Die gepatchte Datei hat einen ähnlichen, aber nicht identischen Header:

| Feld | Wert |
|---|---:|
| `e_cparhdr` | `0x0060` Paragraphen |
| Headerlänge | `0x0600` Bytes |
| `e_crlc` | `0x0114` = 276 DOS-Relocation-Einträge |
| `e_lfarlc` | `0x003C` |
| `e_ip` | `0x02B1` |
| `e_cs` | `0x0000` |
| `e_ss` | `0x0E34` |
| `e_sp` | `0x15F0` |
| Dateigröße | 72.736 Bytes (`0x11C20`) |
| nach MZ-Header verbleibender Ladebereich | 71.200 Bytes (`0x11620`) |

Obwohl der DOS-Einstieg `CS:IP = 0000:02B1` bei beiden Dateien gleich ist, unterscheiden sich Stackwerte, Anzahl der DOS-Relocations und die Dateigröße. Gleiche Einstiegsoffsets beweisen keine identische Kernelversion oder identischen Code.

## 2054 – Einstiegscode im Originalkernel

Der MZ-Einstieg liegt im Ladebereich bei Offset `0x02B1`. Dort stehen in `KERNEL.OLD` die Bytes:

```asm
02B1  9A 00 00 90 0F    lcall 0F90:0000
02B6  2E 01 06 C8 02    add   ax,cs:[02C8]
02BB  B0 04             mov   al,04
02BD  BB 02 00          mov   bx,0002
02C0  33 C9             xor   cx,cx
02C2  E8 E2 FE          call 01A7
```

Der erste Schritt ist somit ein Far-Call in Segment `0x0F90`, Offset `0x0000`. Das ist der tatsächliche DOS-Einstiegspfad; er darf nicht mit einer GEODE-Relocation-Routine verwechselt werden.

## 2055 – Bootstrap-Routine bei Segment 0F90h

Die Far-Call-Zieladresse `0F90:0000` entspricht innerhalb des geladenen MZ-Abbilds dem linearen Ladebereich-Offset `0x0F900`.

Der dortige Code beginnt:

```asm
F900  FC                cld
F901  8C D8             mov   ax,ds
F903  BB 35 0E          mov   bx,0E35
F906  8E DB             mov   ds,bx
F908  8C 16 40 00       mov   [0040],ss
F90C  89 26 42 00       mov   [0042],sp
F910  C6 06 46 00 00    mov   byte ptr [0046],00
F915  8E D8             mov   ds,ax
...
F92D  B9 90 0F          mov   cx,0F90
F930  8E D9             mov   ds,cx
F932  33 F6             xor   si,si
F934  33 FF             xor   di,di
F936  B9 E0 1C          mov   cx,1CE0
F939  D1 E9             shr   cx,1
F93B  F3 A5             rep movsw
F93D  8C C0             mov   ax,es
F93F  2D 90 0F          sub   ax,0F90
F942  1F                pop   ds
F943  CB                retf
```

Die Routine kopiert `0x1CE0` Bytes aus `0F90:0000` in einen neu berechneten Zielbereich und liefert anschließend eine Segmentdifferenz in `AX` zurück. Die Kopierlänge ist durch `CX=1CE0h` und `rep movsw` belegt: `0x1CE0 / 2 = 0x0E70` WORDs, also 7.392 Bytes.

**Interpretation mit Beleggrenze:** Dies ist eine Bootstrap-/Selbstverlagerungsroutine des Kernels. Die genaue Rolle des Zielbereichs ist aus diesem Ausschnitt allein noch nicht vollständig erklärt. Es ist keine nachgewiesene GEODE-Relocation-Verarbeitung.

## 2056 – Trennung von DOS- und GEODE-Relocations

Es liegen zwei unabhängige Ebenen vor:

1. DOS-MZ-Relocationstabelle im EXE-Header: 273 Einträge bei `KERNEL.OLD`, 276 bei `KERNEL.EXE`; Eintragsformat und Verarbeitung gehören zum DOS-EXE-Lader.
2. GEODE-Relocationstabellen in `.GEO`-Dateien: je Ressource ein durch die Ressourcentabellen referenzierter Stream mit vier Byte langen Datensätzen `<BBH>`.

Aus der DOS-Relocation-Anzahl oder aus einzelnen MZ-Relocation-Adressen darf nicht auf GEODE-Relocationtypen geschlossen werden.

## 2057 – Original und gepatchte Kerneldatei nicht vermischen

Die beiden Kerneldateien unterscheiden sich in Dateigröße, DOS-Relocation-Anzahl, Stackinitialisierung und in zahlreichen Bytes des Ladebereichs. Die Differenz ist nicht auf eine einzelne Text- oder Sprachressource beschränkt.

Folgerung: Die Loaderanalyse muss primär auf `KERNEL.OLD` als deutschem Originalkernel aufbauen. `KERNEL.EXE` bleibt ein Vergleichsobjekt zur späteren Erkennung von Patchänderungen. Eine Routine darf nicht allein deshalb als Original-1.x-Loaderfunktion bezeichnet werden, weil sie in der gepatchten Datei gefunden wurde.

## 2058 – String- und Signatursuche

Im Kernelabbild wurden unter anderem die ASCII-Zeichenfolge `Could not load data block` sowie die Bytefolge `C7 45 CF 53` gefunden. Die Fundstellen liegen im hinteren Bereich des MZ-Ladeabbilds.

Eine bloße Fundstelle ist kein Beweis für die zugehörige Loaderfunktion: Die Signatur kann in einer Tabelle oder Datenstruktur liegen; die Fehlermeldung kann über eine indirekte Nachrichten-/Stringtabelle referenziert werden. Ohne gesicherte Code-Xrefs werden diese Fundstellen nur als Suchanker festgehalten.

## 2059 – GEODE-Loader noch nicht identifiziert

Die Disassemblierung des MZ-Einstiegs und der Far-Call-Zielroutine `0F90:0000` zeigt zunächst den Kernel-Bootstrap und die Selbstverlagerung. In diesem Untersuchungsblock wurde keine Routine nachgewiesen, die `GRI_info`, das Zusatzbyte oder den Zieloffset eines GEODE-Relocation-Eintrags liest und verarbeitet.

Daher werden keine Typnummern semantisch neu zugeordnet. Insbesondere bleibt die Behandlung der dokumentierten Sonderfälle (DOCUMENT/SPLAY und Root-NPLAYGCM) offen.

## 2060 – Nächste technische Schritte

1. Den MZ-Ladebereich und die internen Kernel-Segmente von `KERNEL.OLD` vollständig kartieren.
2. Den Aufrufpfad zu Datei-/GEODE-Ladefunktionen anhand tatsächlicher Code-Xrefs rekonstruieren.
3. Kandidatenroutinen darauf prüfen, ob sie Ressourcentabellen, Import-/Exportverzeichnisse oder die vier Byte langen Relocation-Datensätze lesen.
4. Register, Segmentannahmen und Speicheränderungen an jeder gefundenen Routine dokumentieren.
5. Erst danach die Source-/Type-/Extra-Felder der GEODE-Relocations endgültig benennen.

Keine Kerneldatei, GEO-Datei oder Parserdatei wurde geändert. Dies ist statische Disassemblierungs- und Headeranalyse, kein GeoManager-Laufzeittest.

## Untersuchungen 2061–2070 – Segmentstruktur des DOS-Kernelabbilds

### 2061 – DOS-Relocation-Einträge nach Segmentziel gruppiert

Die MZ-Relocationstabelle von `KERNEL.OLD` wurde vollständig gelesen. Jeder DOS-Relocation-Eintrag besteht aus Offset und Segmentziel. Gruppierung nach dem Segment-WORD:

| Segmentziel | Anzahl | Offsetbereich |
|---|---:|---|
| `0000h` | 60 | `0162h–D225h` |
| `0E35h` | 57 | `0004h–0F8Dh` |
| `0F90h` | 156 | `0004h–1CC6h` |
| **Gesamt** | **273** | |

Dies sind ausschließlich MZ-/DOS-Fixups. Die Gruppierung beschreibt, auf welche im Kernelabbild enthaltenen Segmente DOS beim Laden Segmentwerte addieren muss.

### 2062 – Segmentziel 0F90h und Bootstrap-Kopierlänge

Die 156 MZ-Fixups für Segment `0F90h` liegen im Offsetbereich `0004h` bis `1CC6h`. Der Bootstrap bei `0F90:0000` kopiert `1CE0h` Bytes. Damit liegen alle 156 zugehörigen Fixup-Offets innerhalb des kopierten Segmentblocks.

Das ist konsistent mit dem Befund, dass `0F90h` einen zusammenhängenden, selbstverlagerten Kernelblock bezeichnet. Es beweist noch nicht, dass dieser Block die GEODE-Laderoutine enthält.

### 2063 – Segmentziel 0E35h

Die 57 MZ-Fixups für `0E35h` liegen zwischen Offset `0004h` und `0F8Dh`. Der MZ-Header von `KERNEL.OLD` initialisiert außerdem `SS=0E35h` und `SP=15B0h`.

Die Übereinstimmung von `SS` und dem häufigen Fixup-Segmentziel ist ein starker Hinweis, dass `0E35h` eine zentrale Kernel-Daten-/Stacksegmentrolle hat. Die genaue Aufteilung von Stack und globalen Daten wird hier noch nicht festgelegt.

### 2064 – Gepatchter Kernel: verschobene Segmentziele

Die gleiche Gruppierung für `KERNEL.EXE` ergibt:

| Segmentziel | Anzahl | Offsetbereich |
|---|---:|---|
| `0000h` | 61 | `0162h–D216h` |
| `0E34h` | 59 | `0004h–0FCBh` |
| `0F93h` | 156 | `0004h–1CCFh` |
| **Gesamt** | **276** | |

Die Segmente sind gegenüber dem deutschen Original verschoben: `0E35h` wird zu `0E34h`, `0F90h` zu `0F93h`. Die 156 Fixups im großen Segmentblock bleiben in der Anzahl gleich. Das unterstreicht, warum Segmentnummern des gepatchten Kernels nicht ungeprüft auf `KERNEL.OLD` übertragen werden dürfen.

### 2065 – Interner GEODE-Signaturtreffer im Kernel

Die Bytefolge `C7 45 CF 53` wurde im Ladeabbild von `KERNEL.OLD` einmal gefunden:

- MZ-Dateioffset: `F9C6h`
- Offset relativ zum Beginn des MZ-Ladebereichs (`0600h`): `F3C6h`
- Rohkontext ab Ladebereichoffset `F3B0h`:

```text
00 00 00 00 00 03 71 9F 43 9F B5 9F 7B 9F BB 9F
C8 9F 01 00 00 00 C7 45 CF 53 01 00 00 00 00 00
```

Die Signatur steht nach mehreren WORD-Werten, die wie Offset-/Segmentpaare aussehen können, und vor Nullbytes. Das ist ein Datenkontext, kein nachgewiesener Ausführungspfad.

### 2066 – Vergleich des Signaturfunds im gepatchten Kernel

In `KERNEL.EXE` wurde die gleiche vier Byte lange Folge ebenfalls einmal gefunden, jedoch an einer anderen Position:

- MZ-Dateioffset: `F9F6h`
- Ladebereichoffset: `F3F6h`

Der Abstand gegenüber `KERNEL.OLD` beträgt `30h` Bytes. Ohne die umgebende Struktur vollständig zu dekodieren, darf daraus nicht geschlossen werden, dass die Kernel-GEODE-Struktur inhaltlich geändert wurde. Gesichert ist nur die Verschiebung der Fundstelle.

### 2067 – Keine direkte Code-Xref auf die Signatur behauptet

Die bisherige Suche hat die Signatur als Rohbytefolge gefunden, aber keine gesicherte Instruktion identifiziert, die diese vier Bytes unmittelbar vergleicht. Ein Code-Xref kann über Segmentregister, Tabellen oder indirekte Zeiger erfolgen. Solange diese Wege nicht rekonstruiert sind, bleibt die Signatur ein Suchanker und kein Beweis für den GEODE-Loader.

### 2068 – Segmentmodell als Arbeitskarte

Für `KERNEL.OLD` ist aus dem MZ-Header und der Fixup-Tabelle derzeit folgende Arbeitskarte belegt:

- `CS:IP = 0000:02B1`: DOS-Einstiegspunkt.
- `0F90:0000`: Far-Call-Ziel des Einstiegs; Bootstrap-/Selbstverlagerung, Kopierlänge `1CE0h`.
- `SS:SP = 0E35:15B0`: initialer Stackzeiger.
- 156 MZ-Fixups referenzieren Segment `0F90h`.
- 57 MZ-Fixups referenzieren Segment `0E35h`.
- 60 MZ-Fixups referenzieren Segment `0000h`.

Dies ist eine Segment-/Ladeabbildkarte, noch keine vollständige Karte der Kernelmodule oder ihrer öffentlichen Funktionen.

### 2069 – Konsequenz für die GEODE-Loader-Suche

Die GEODE-Loaderfunktion ist weiterhin nicht identifiziert. Die MZ-Fixup-Tabelle hilft, die internen Kernel-Segmente auseinanderzuhalten, ist aber nicht selbst die GEODE-Relocation-Tabelle. Der nächste Suchschritt muss von Kernel-Codepfaden ausgehen, die Dateiressourcen einlesen und die GEODE-Ressourcenverzeichnisse verarbeiten.

### 2070 – Zwischenstand

- Der originale Kernel-MZ-Einstieg und die Bootstrap-Selbstverlagerung sind bytegenau lokalisiert.
- Die DOS-MZ-Fixups sind in drei Segmentzielgruppen aufgeteilt.
- Der gepatchte Kernel besitzt verschobene Segmentziele und darf nicht als Offsetreferenz für den Originalkernel verwendet werden.
- Die GEODE-Signatur kommt im Kernelabbild vor; ihre Funktion und der zugehörige Code-Xref sind noch offen.
- Keine GEODE-Relocation-Typsemantik wurde neu festgelegt; keine Dateien wurden gepatcht.

## Untersuchungen 2071–2080 – GEODE-Lader und Relocation-Dispatcher im deutschen Originalkernel

**Untersuchungsbasis:** `GEOWORKS/KERNEL.OLD` aus dem bereitgestellten `GEOWORKS.zip`. MZ-Headergröße `0x0600`; die nachfolgenden Adressen sind Ladeabbild-Offsets ab dem ersten Byte nach dem MZ-Header, sofern nicht ausdrücklich eine Segmentadresse angegeben ist. Die Disassemblierung erfolgte im 8086-Modus. Es wurde keine Binärdatei verändert.

### 2071 – Aufrufpfad zum GEODE-Lader

Im Kernel-Ladeabbild bei `0x1970` liegt ein Far-Call-Wrapper:

```asm
1970  call 1F0E
1973  call 197A
1976  call 1F15
1979  retf
```

Die zentrale Routine `197A` nimmt den Dateinamen über `DS:SI` entgegen, setzt `DX=SI`, `AL=A0` und ruft über `12F6` die DOS-Dateiöffnung auf. `12F6` setzt `AH=3Dh`; der tatsächliche DOS-Aufruf erfolgt in der darunterliegenden Dateifunktionsschicht.

Der Pfad `0F90:0645` im Kernel-Initialisierungscode ruft `0000:1970` auf. In diesem Kontext wird unter anderem `local.geo` vorbereitet. Der Aufrufpfad belegt damit, dass `1970` als GEODE-Ladepfad verwendet wird; er ist nicht bloß ein allgemeiner DOS-Dateiöffner.

### 2072 – Headerprüfung liest zunächst 0x44 Bytes

Die Routine `1A56` liest zunächst `CX=0x44` Bytes in den Stackpuffer `SS:[BP-0x6A]`:

```asm
1A56  push ss
1A57  pop  ds
1A58  mov  cx,0044
1A5B  lea  dx,[bp-006A]
1A5E  xor  al,al
1A60  call 1088
```

`1088` ist der kernelinterne Leseweg; in seinem Unterpfad wird DOS-Funktion `AH=3Fh` verwendet. Die Routine prüft danach die ersten Headerfelder, bevor weitere Daten verarbeitet werden.

### 2073 – GEODE-Signatur bytegenau bestätigt

Die Vergleiche bei `1A6B` und `1A72` lauten:

```asm
cmp word ptr [bp-006A],45C7
cmp word ptr [bp-0068],53CF
```

Auf x86-Little-Endian entsprechen diese Werte den Dateibytes:

```text
C7 45 CF 53
```

Das ist die GEODE-Kennung, die wir zuvor in NOTEPAD.GEO, GROBJ.GEO und weiteren Dateien gefunden haben. Damit ist die Signaturprüfung im Originalkernel unmittelbar belegt.

### 2074 – Headerfeld bei Offset 0x04

Die Prüfung bei `1A7C` verlangt, dass das WORD an Dateioffset `0x04` Null ist. Ein von Null abweichender Wert führt in den Fehlerpfad. Die genaue semantische Bezeichnung dieses Feldes wird hier noch nicht festgelegt.

### 2075 – Protokollprüfung über die Felder bei 0xCC und 0xCE

Nach erfolgreicher Signaturprüfung positioniert der Lader den Dateizeiger mit DOS-Seek `AH=42h` auf Offset `0x00C8` und liest `0x18` Bytes:

```asm
1A82  xor  al,al
1A84  xor  cx,cx
1A86  mov  dx,00C8
1A89  call 10CA
1A8C  mov  cx,0018
1A8F  lea  dx,[bp-0026]
1A92  xor  al,al
1A94  call 1088
```

Danach werden die WORD-Felder bei Dateioffset `0xCC` und `0xCE` mit dem Paar `0x026E` und `0x0003` verglichen. Für NOTEPAD.GEO stehen dort tatsächlich `6E 02 03 00`. Die Routine `1AD4` prüft die zulässige Versions-/Protokollrelation. Die genaue textuelle Benennung des Protokolls bleibt bis zum Abgleich mit weiteren GEODE-Versionen offen.

### 2076 – Aufbau der Ressourcendaten-Verarbeitung

Die Routine `1AEA` berechnet aus den zuvor gelesenen Headerfeldern eine Größe und fordert über `6E87` Speicher an. Anschließend wird ein 0x40-Byte-Block eingelesen. Die Routinen `1B45`, `1C76`, `1B6B` und `1B81` arbeiten danach mit daraus abgeleiteten Tabellenpositionen und Zählern.

Die Berechnungen zeigen, dass der Loader Tabellenbereiche anhand der im Header gespeicherten Zähler adressiert. Die vollständige Zuordnung jedes internen Arbeitsfeldes zu den vier Dateitabellen ist noch nicht abgeschlossen; insbesondere werden die internen Offsets `[0x30]` bis `[0x40]` nicht vorschnell mit gleichnamigen Dateioffsets gleichgesetzt.

### 2077 – Ressourcendaten werden über eine 32-Bit-Dateiposition gelesen

Die Hilfsroutine `2218` verwendet den aktuellen Ressourcenindex `SI`, berechnet einen Eintrag in der Positionstabelle und liest zwei WORD-Werte als Dateiposition `CX:DX`. Danach wird der DOS-Dateizeiger mit `10CA` auf diese Position gesetzt. Der von der aufrufenden Routine übergebene Leseumfang bleibt über den Seek-Aufruf erhalten; anschließend liest `1088` die Ressourcendaten in den Zielsegmentbereich.

Der Codepfad ist damit ein direkter Beleg, dass der Kernel Ressourcendaten über eine tabellengestützte Dateiposition lädt.

### 2078 – Relocation-Daten werden unmittelbar nach dem Ressourcendaten-Lesen verarbeitet

Die Routine `20FE` ruft zuerst `2218` auf und erhält das Zielsegment in `AX`, das anschließend nach `ES` übernommen wird. Danach liest sie die Relocation-Größe aus der zum Ressourcenindex gehörenden Tabelle. Sie führt keinen neuen Dateiseek zwischen dem Ende des Ressourcendaten-Lesens und dem Beginn des Relocation-Lesens aus.

Der Relocation-Bereich wird in Blöcken von höchstens `0x100` Bytes eingelesen. Da `2218` zuvor den Dateizeiger auf den Beginn der Ressource gesetzt und die Ressourcendaten gelesen hat, verarbeitet `20FE` anschließend die direkt folgenden Bytes. Dies bestätigt für diesen Loaderpfad die bereits an NOTEPAD und NOTEPADG beobachtete Anordnung: Ressourcendaten und zugehörige Relocation-Daten folgen in der Datei unmittelbar aufeinander.

### 2079 – Vier-Byte-Datensatz wird vom Kernel als zwei WORDs eingelesen

Die Schleife in `20FE` verarbeitet jeden Datensatz mit vier Bytes Schrittweite:

```asm
2135  mov  ax,[bp+si]
2138  mov  bx,[bp+si+2]
213B  call 2153
213F  add  si,0004
```

Damit liest der Kernel das erste WORD in `AX` und das zweite WORD in `BX`. `BX` wird in `2153` unmittelbar als Patchposition verwendet:

```asm
215B  mov  di,es:[bx]
```

Das letzte WORD des Datensatzes ist folglich der Offset in der gerade bearbeiteten Ressource, an dem der Loader den vorhandenen WORD-Wert liest und gegebenenfalls ändert. Dies ist jetzt nicht mehr nur aus den Datenmustern abgeleitet, sondern durch den ausführbaren Loadercode bestätigt.

### 2080 – Korrektur der bisherigen Typ-/Zusatzfeld-Deutung

Die Routine `2153` zerlegt das erste WORD in weitere Felder:

```asm
2154  mov  dx,ax
2156  and  dl,F0
2159  and  al,0F
```

Bei Little Endian bedeutet dies:

- `AL` enthält das erste Byte des Datensatzes; sein niederes Nibble (`byte0 & 0x0F`) wird als Operationsauswahl verwendet.
- `DL` enthält zunächst ebenfalls das erste Byte; sein höheres Nibble (`byte0 & 0xF0`) wählt den Verarbeitungszweig.
- `AH` ist das zweite Byte. In einem Verarbeitungszweig wird es als Index verwendet (`mov dl,ah`, danach `shl dx,1`).
- `BX` enthält das letzte WORD und bezeichnet die Patchposition.

Damit war die frühere Beschreibung „Byte 0 = vollständiger Typ, Byte 1 = allgemeines Zusatzfeld“ zu grob. Die Datenstruktur kann weiterhin als `<BBH>` gespeichert werden, aber die Semantik des ersten Bytes ist mindestens in Operations-Nibble und Klassen-Nibble aufzuteilen. Das zweite Byte ist in bestimmten Klassen ein Index und darf nicht als bedeutungsloses Zusatzbyte behandelt werden.

Die Routine unterscheidet im sichtbaren Code mindestens die Klassenwerte `0x00` und `0x10` im oberen Nibble des ersten Bytes und Operationswerte `0`, `1`, `2` und `3` im unteren Nibble. Weitere Zweige sowie die vollständige Bedeutung der Kombinationen werden im nächsten Untersuchungsblock verfolgt. Noch nicht entschlüsselte Typen werden ausdrücklich nicht benannt.

### Zwischenstand nach 2080

- GEODE-Loader-Einstieg `0000:1970` und Hauptpfad `197A` sind im deutschen Originalkernel gefunden.
- Die GEODE-Signatur `C7 45 CF 53` wird bei `1A6B`/`1A72` geprüft.
- Die Headerprüfung liest zunächst 0x44 Bytes und danach 0x18 Bytes ab Dateioffset 0xC8.
- `20FE` ist der Relocation-Verarbeitungspfad; er liest 4-Byte-Datensätze und ruft für jeden `2153` auf.
- Das letzte WORD ist durch `ES:[BX]` als Patchoffset innerhalb der Ressource bestätigt.
- Das erste WORD enthält mindestens zwei Nibble-Felder; das zweite Byte liefert in einem Zweig einen Index.
- Die bisherige Deutung als „erstes Byte vollständiger Typ / zweites Byte bloßes Zusatzfeld“ ist korrigiert.
- Keine Kernel-, GEO- oder Parserdatei wurde geändert. Die Analyse ist statisch; ein Laufzeittest unter GeoManager steht aus.

**Nächster Block 2081–2090:** Die Verzweigungen von `2153` werden vollständig verfolgt. Wir gleichen die Klassen-/Operationskombinationen mit echten NOTEPAD-, GROBJ- und SPLAY-Relocation-Datensätzen ab und bestimmen, welche Tabellen die Segment-/Ressourcenindizes liefern.

## Untersuchungen 2081–2090 – Kontrollfluss des Relocation-Dispatchers

**Untersuchungsbasis:** Original `KERNEL.OLD`, Ladeabbild `/tmp/geodework/KERNEL.OLD.LOAD`; 8086-Disassemblierung. Die Funktion wurde ausdrücklich ab ihrer tatsächlichen Einsprungadresse `0x2153` disassembliert. Ein Disassemblerstart mitten in der vorhergehenden Instruktion bei `0x2151` erzeugt irreführende Instruktionsgrenzen; deshalb gilt für diesen Block ausschließlich die ab `0x2153` ausgerichtete Folge.

### 2081 – Eintritt und gesicherte Eingangsregister

`20FE` lädt pro Datensatz das erste WORD nach `AX` und das zweite WORD nach `BX`, danach erfolgt `call 2153`. Zu Beginn von `2153`:

```asm
2153  push ds
2154  mov  dx,ax
2156  and  dl,F0
2159  and  al,0F
215B  mov  di,es:[bx]
```

Damit ist der Eingabewert an `ES:[BX]` bereits vor der Verzweigung als `DI` geladen. `DL` enthält die Klassenmaske des ersten Bytes; `AL` dessen Operationsnibble. `AH` bleibt zunächst das zweite Byte.

### 2082 – Klasse 0x00

Bei `DL=0` führt der Code aus:

```asm
2163  mov  si,cs
2165  shl  di,1
2167  mov  ds,cs:[2151]
216C  jmp  21C4
```

Der ursprüngliche WORD-Wert aus der Ressource wird verdoppelt und dient als Index in einer WORD-Tabelle im durch `CS:[2151]` bezeichneten Segment. `SI` erhält den aktuellen Code-Segmentwert. Die Routine springt danach in die gemeinsame Operationsauswertung ab `21C4`.

**Noch offen:** Welche konkrete Kernel-Tabelle das Segment `CS:[2151]` bezeichnet und welche symbolische GEODE-Relocation-Art Klasse 0x00 repräsentiert.

### 2083 – Klasse 0x10: Segmenttabelle über Byte 1

Bei `DL=0x10` springt der Dispatcher nach `21A7`:

```asm
21A7  xor  dx,dx
21A9  mov  dl,ah
21AB  shl  dx,1
21AD  mov  si,[0036]
21B1  add  si,dx
21B3  mov  ds,[si]
```

Das zweite Datensatzbyte wird als WORD-Tabellenindex verwendet. Die Basisadresse dieser Segmenttabelle steht im Kernel-Arbeitsfeld `DS:[0036]`; der gelesene Tabellen-WORD wird anschließend in `DS` geladen. Damit ist die Indexfunktion des zweiten Bytes für diese Klasse unmittelbar durch den Code belegt.

### 2084 – Sonderwert FFFFh in Klasse 0x10

Unmittelbar danach prüft der Code den zuvor aus `ES:[BX]` geladenen Wert `DI` durch `inc di` und `je 2179`. Der Wert `FFFFh` ist somit ein eigener Sonderfall und führt nicht in die normale Ressourcen-/Exporttabelle. Für andere Werte wird `DI` wiederhergestellt und als Index weiterverarbeitet.

### 2085 – Aufbau eines Vier-Byte-Tabelleneintrags

Der normale Pfad bei `2179` berechnet `DI*4 + DS:[0030]` und liest aus dem Eintrag zwei WORDs:

```asm
2179  mov  si,[di]
...
21BD  add  di,[0030]
21C1  mov  si,[di+2]
21C4  mov  di,[di]
```

Damit ist für diesen Pfad ein Tabelleneintrag aus zwei WORD-Feldern belegt. Das erste Feld wird in `DI`, das zweite in `SI` übernommen. Die konkrete Feldbedeutung wird erst nach Rückverfolgung der Tabelle `DS:[0030]` festgelegt.

### 2086 – Weitere Klassen benutzen eine andere Tabelle

Klassen außer `0x00` und `0x10` laufen über `2173`. Dort wird der Ressourcen-/Exportwert aus `ES:[BX]` verdoppelt, zur Basis `DS:[003A]` addiert und ein WORD in `SI` gelesen. Danach folgt je nach Operation ein Sonderpfad oder der Aufruf `9630`. Anschließend wird ein WORD aus `[SI]` nach `DI` geladen.

Das zeigt, dass mindestens ein weiterer Klassenbereich eine getrennte Tabelle über `DS:[003A]` verwendet. Die genaue Bedeutung der übrigen oberen Nibblewerte ist noch nicht bewiesen.

### 2087 – Metadatenprüfungen vor bestimmten Operationen

Im Pfad über `217F` werden zwei Eintragsmerkmale geprüft:

```asm
2184  test byte ptr [si+0A],80
218A  cmp  byte ptr [si+0B],FF
```

Wenn Bit 7 des Bytes `SI+0x0A` gesetzt ist oder das Byte `SI+0x0B` gleich `FFh` ist, springt der Code zum gemeinsamen Schreibpfad. Andernfalls hängt die weitere Verarbeitung unter anderem von `AL` ab. Die Bedeutung dieser Metadatenbytes wird nicht ohne Struktur-Xref benannt.

### 2088 – Gemeinsame Operationsauswertung

Ab `21C4` unterscheidet der Code die unteren Nibblewerte:

- `AL=2`: direkter Schreibpfad mit `DI` nach `ES:[BX]`.
- `AL=1`: ebenfalls Schreibpfad `DI` nach `ES:[BX]`.
- `AL=0`: schreibt abhängig von `SI` ein WORD nach `ES:[BX+2]`; bei `SI>=F000h` wird stattdessen `DI` geschrieben.
- `AL=3`: eigener Pfad mit Prüfung `SI` gegen `F000h`; bei kleineren Werten folgt ein Aufruf `724B`, andernfalls wird ein anderer Rücksprung-/Trampolinpfad vorbereitet.

Diese Beschreibung benennt nur die beobachteten Speicheroperationen und Kontrollflusswege, nicht die semantischen Namen der Relocation-Typen.

### 2089 – Spezialpfad erzeugt Codebytes

Für einen Zweig mit `AL=2` und den zuvor geprüften Metadaten wird bei `21E9` das Byte `CDh` an `ES:[BX-1]` geschrieben. Danach wird ein Wert aus `SI` um vier Bit nach rechts verschoben, mit `80h` verknüpft und als Teil des Wertes für `ES:[BX]` verwendet. Das ist eine konkrete Codepatch-Operation und kein gewöhnlicher WORD-Pointer-Patch.

Der Aufruf bei `21E6` geht nach `220F`; diese kurze Hilfsroutine schiebt `SI` viermal nach links und kehrt zurück. Der genaue Zweck des gesamten erzeugten Byte-/WORD-Musters muss anhand der betroffenen GEODE-Datensätze und des Laufzeitkontexts weiter untersucht werden.

### 2090 – Dispatcher-Karte und offene Punkte

Der derzeit gesicherte Kontrollfluss lässt sich so zusammenfassen:

| Erstes Byte: oberes Nibble | Beobachteter Pfad | Zweites Byte |
|---|---|---|
| `0x00` | Segment-/Tabellenbasis aus `CS:[2151]`; gemeinsamer Dispatcher | in diesem Pfad nicht verwendet |
| `0x10` | Segment wird über Tabelle ab `DS:[0036]` geladen | Index in Segmenttabelle |
| andere Werte | Tabelle ab `DS:[003A]`, danach ggf. Metadatenprüfung | in diesem Pfad nicht als Index nachgewiesen |

Die unteren Nibblewerte `0` bis `3` steuern verschiedene Schreib- und Sonderpfade. Nicht alle Kombinationen sind gleichbedeutend, und einzelne Klassen verzweigen vor der gemeinsamen Operationsauswertung.

**Noch nicht erledigt:**

1. Xrefs und Aufbau der Tabellen `DS:[0030]`, `DS:[0036]`, `DS:[003A]` sowie des Segmentzeigers `CS:[2151]` bestimmen.
2. Die Aufrufziele `9630` und `724B` untersuchen.
3. Reale NOTEPAD-, GROBJ- und SPLAY-Datensätze nach Klassen-/Operationskombinationen gruppieren und ihre Zielwerte mit den Tabellen abgleichen.
4. Erst danach symbolische Namen für die Relocation-Arten festlegen.

**Status:** Ausschließlich statische Analyse. Keine Änderungen an `KERNEL.OLD`, `KERNEL.EXE`, GEO-Dateien oder `pcgeos1/geode.py`.

## 2091–2100 – Rückverfolgung der GEODE-internen Tabellenfelder

### 2091 – Die drei Tabellenzeiger werden im GEODE-Kontext aufgebaut

Die Routine ab `1B45` berechnet `DS:[0030]` aus `DS:[0036]` und `DS:[0034]`:

```asm
1B45  mov dx,[0034]
1B49  shl dx,1
1B4B  add dx,[0036]
1B4F  mov [0030],dx
```

Damit gilt exakt:

`0030 = 0036 + 2 * 0034` (16-Bit-Arithmetik).

Das ist ein abgeleiteter Zeiger hinter einem WORD-Array mit `0034` Einträgen. Die Bezeichnung des Arrays wird noch nicht festgelegt.

### 2092 – Der Bereich ab 0030 wird mit Vier-Byte-Einträgen dimensioniert

Direkt anschließend liest `1B6B` die Anzahl aus `DS:[0032]`, multipliziert sie mit vier und verwendet `DS:[0030]` als Startadresse. Die Routine `1C04` wird für jedes Element mit einem Offset aufgerufen, der jeweils um vier Bytes steigt.

Damit ist belegt, dass der Bereich ab `0030` mindestens `0032` Datensätze zu je vier Bytes enthält. Das passt strukturell zu den im Relocation-Dispatcher gelesenen Paaren aus zwei WORDs, beweist aber allein noch nicht, dass alle Datensätze identisch semantisch interpretiert werden.

### 2093 – Der Zeiger 003A liegt hinter dem Vier-Byte-Array

Routine `1C76` berechnet:

```asm
1C76  mov ax,[0032]
1C79  shl ax,1
1C7B  shl ax,1
1C7D  add ax,[0030]
1C81  mov [003A],ax
```

Somit gilt exakt:

`003A = 0030 + 4 * 0032`.

`003A` zeigt unmittelbar hinter das zuvor dimensionierte Vier-Byte-Array. Dies bestätigt, dass die Felder `0030` und `003A` auf benachbarte Bereiche einer gemeinsamen internen GEODE-Datenstruktur verweisen.

### 2094 – Die nachfolgenden Bereiche 003C und 003E

Im selben Aufbaupfad werden zwei weitere Zeiger berechnet:

- `003C = 003A + 2 * 0038`
- `003E = 003C + 4 * 0038`

Die Routine reserviert danach weitere Bereiche anhand der Anzahl `0038`. Die exakten Feldinhalte sind anhand dieses Codes allein noch nicht festgelegt. Die Berechnungen belegen aber eine zusammenhängende Folge von Tabellenbereichen mit WORD- und DWORD-Elementbreiten.

### 2095 – 0036 ist ein Eingangszeiger, nicht bloß eine Relocation-Konstante

Da `0030` aus `0036` plus `2*0034` gebildet wird, muss `0036` bereits vor `1B45` initialisiert sein. Der Wert ist daher Teil des zuvor aufgebauten GEODE-Kontexts. Der Dispatcher bei `21A7` benutzt `0036` als Basis einer WORD-Tabelle und lädt aus dieser Tabelle einen Segmentwert in `DS`.

Die Verbindung zwischen Initialisierung und Dispatcher ist damit durch konkrete Lese-/Rechenoperationen nachgewiesen. Der semantische Name des Arrays bleibt offen.

### 2096 – Die Funktion 9630h ist ein Segmentkontext-Umschalter

Der Aufruf `9630h` beginnt tatsächlich mit dem Segmentpräfix an Adresse `9630`:

```asm
9630  2E 8E 1E 2E 96    mov ds,cs:[962E]
9635  C3                ret
```

Die parallel verwendete Routine `9636h` lädt entsprechend `ES` aus demselben Kernelwort:

```asm
9636  2E 8E 06 2E 96    mov es,cs:[962E]
963B  C3                ret
```

Damit ist `9630h` keine allgemeine Datei- oder Tabellenlesefunktion. Sie setzt `DS` auf den durch `CS:[962E]` bezeichneten Segmentkontext. Diese Präzisierung korrigiert jede weitergehende Funktionsvermutung aus den vorherigen Abschnitten.

### 2097 – 724Bh arbeitet mit einem übergebenen Segment-/Handle-Kontext

Die Routine `724B` übernimmt `CX` als Segmentkontext, setzt `DS= CX`, liest dort ein Wort am Offset null und ruft anschließend `9630h` sowie `701Bh` auf. Danach prüft sie unter anderem Alignment, Grenzen und Einträge in Kernel-Verwaltungsstrukturen. Sie kann einen passenden Verwaltungs-/Handleeintrag finden und gibt einen Wert über `CX` zurück; in bestimmten Fällen setzt sie Carry.

Sicher belegt ist damit eine Kernel-interne Segment-/Handle-Auflösung beziehungsweise -Prüfung. Eine präzisere Bezeichnung wie „Lock“, „Pin“ oder „Resource load“ wäre ohne zusätzliche Xrefs und Laufzeitbeobachtung nicht ausreichend abgesichert.

### 2098 – Der Relocation-Dispatcher nutzt 9630h für den Kernelkontext

Im Zweig ab `217F` wird `9630h` aufgerufen, bevor `SI` dereferenziert und Metadaten bei `[SI+0A]` und `[SI+0B]` geprüft werden. Nach dem neuen Befund bedeutet das: `DS` wird vor diesen Zugriffen ausdrücklich auf den Segmentkontext `CS:[962E]` gesetzt. Die Metadatenprüfung erfolgt daher nicht mehr im zuvor für die Zielressource geladenen `DS`, sondern im Kernelkontext.

Das ist für die Interpretation der Tabellenfelder entscheidend: Die Tabellen-/Metadatenadressen dürfen nicht pauschal als Felder im gerade relocatierten Ressourcenblock behandelt werden.

### 2099 – Die GEODE-Headerzählungen und die internen Tabellenbereiche

Die nachgewiesenen Größenbeziehungen lauten zusammengefasst:

| Feld | Berechnung / Verwendung | Sicherer Befund |
|---|---|---|
| `0030` | `0036 + 2*0034` | Start eines WORD-vorangehenden Bereichs; danach folgen `0032` Vier-Byte-Einträge |
| `0036` | Eingangszeiger | Basis einer WORD-Tabelle im Relocation-Pfad |
| `003A` | `0030 + 4*0032` | Start des direkt folgenden Tabellenbereichs |
| `003C` | `003A + 2*0038` | Start nach einem WORD-Bereich mit `0038` Elementen |
| `003E` | `003C + 4*0038` | Start nach einem DWORD-Bereich mit `0038` Elementen |

Diese Beziehungen sind aus den Maschinenbefehlen abgeleitet. Die Zähler `0032`, `0034`, `0038` und die Felder `0030` bis `003E` gehören zum selben internen GEODE-Kontext, aber ihre symbolischen Namen werden erst nach Abgleich mit realen Headern und Loader-Aufrufpfaden vergeben.

### 2100 – Korrigierter Stand und nächste Prüfschritte

Der Tabellenaufbau ist jetzt in Teilen mathematisch rekonstruiert. Zusätzlich ist die Rolle von `9630h` eindeutig: `DS` wird aus `CS:[962E]` geladen. `724Bh` ist eine Segment-/Handle-Verwaltungsroutine, deren genaue Wirkung noch nicht abschließend benannt wird.

**Nächste Schritte:**

1. Den Initialisierungspfad vor `1B45` zurückverfolgen, um Herkunft und Bedeutung von `0034`, `0036`, `0032` und `0038` festzustellen.
2. Die Aufrufstellen von `1B45`, `1C76` und `21A7` vergleichen, um die Lebensdauer der Tabellenbereiche zu verstehen.
3. Den Wert `CS:[962E]` und seine Schreibstellen finden.
4. Die realen GEODE-Dateitabellen aus NOTEPAD und GROBJ gegen die internen Tabellenbeziehungen spiegeln.

**Status:** Statische Disassemblierung des deutschen Originalkernels `KERNEL.OLD`. Keine Änderung an Kerneldateien, GEO-Dateien oder `pcgeos1/geode.py`; keine Laufzeitbestätigung.

## Untersuchungen 2101–2110 – Importtabelle und nachfolgende Verwaltungsarrays

### 2101 – Rückverfolgung von Feld 0036

Die Routine `2652` initialisiert `0036` explizit:

```asm
2652  mov ax,0046
2655  test byte ptr [0003],80
265A  je   265F
265C  mov ax,005E
265F  mov [0036],ax
```

Damit ist `0036` in diesem Loader-Kontext kein beliebig berechneter Zeiger, sondern ein ausgewählter Offset innerhalb der eingelesenen GEODE-Metadaten: entweder `0046h` oder `005Eh`, abhängig vom Flag `80h` in `[0003]`. Die genaue Bedeutung der beiden Header-Varianten muss separat anhand der Headerdaten belegt werden.

### 2102 – Feld 0034 zählt 14-Byte-Importeinträge

Unmittelbar danach liest `2652` den Wert `0034` und reserviert `14 * 0034` Bytes temporären Speicher. Die Schleife verarbeitet pro Durchlauf genau 14 Bytes:

```asm
2662  mov cx,[0034]
2668  mov si,cx
266A  mov ax,000E
266D  mul cx
...
2693  mov ax,es:[di+0A]
2698  mov bx,es:[di+0C]
269C  mov cx,es:[di+08]
26A4  mov dx,[0000]
26A6  call 271C
26AA  mov [bx],ax
26AC  add di,000E
26AF  add bx,0002
26B2  dec si
```

Der Befund passt zur bereits aus den GEO-Dateien bekannten 14-Byte-Importstruktur. `0034` ist damit im untersuchten Kontext die Anzahl dieser Importeinträge. Die Routine löst jeden Eintrag über `271C` auf und schreibt das Ergebnis in eine WORD-Tabelle, deren Basis bei `0036` liegt.

### 2103 – 0036 ist die Basis der aufgelösten Import-Segmentwerte

Der Dispatcherzweig `21A7` verwendet `0036` als Basis und indexiert mit dem oberen Byte des Relocation-Feldes:

```asm
21A7  xor dx,dx
21A9  mov dl,ah
21AB  shl dx,1
21AD  mov si,[0036]
21B1  add si,dx
21B3  mov ds,[si]
```

Zusammen mit dem Aufbau in `2652` ergibt sich: Die WORD-Tabelle ab Offset `0036` enthält die durch `271C` aufgelösten Segmentwerte der Imports. Der Index ist ein WORD-Index (Byteindex `2 * AH`). Das ist eine deutlich engere und besser belegte Aussage als die bisherige Bezeichnung „Eingangszeiger“.

### 2104 – 0030 beginnt hinter der Import-Segmenttabelle

`1B45` berechnet:

```asm
1B45  mov dx,[0034]
1B49  shl dx,1
1B4B  add dx,[0036]
1B4F  mov [0030],dx
```

Damit liegt `0030` exakt `2 * Importanzahl` Bytes hinter der Basis `0036`. Das bestätigt die Tabellenfolge: zuerst die aufgelösten WORD-Segmentwerte der Imports, danach der nächste interne Tabellenbereich.

### 2105 – 0032 zählt vier Byte breite Einträge im folgenden Bereich

`1B6B` durchläuft `0032` Einträge. Für jeden Eintrag wird die Position um vier Bytes weitergeschoben:

```asm
1B6B  mov cx,[0032]
1B71  mov di,[0030]
1B75  add di,0002
1B78  call 1C04
1B7B  add di,0004
1B7E  loop 1B78
```

Die Schleife überspringt jeweils die ersten zwei Bytes ab `0030` und ruft die Verarbeitung für die nachfolgenden Vier-Byte-Schritte auf. Sicher ist deshalb die Anzahl `0032` und der Vier-Byte-Abstand der Einträge. Eine fachliche Benennung als Export-, Ressource- oder Relocation-Anzahl wäre an dieser Stelle noch nicht gerechtfertigt.

### 2106 – 003A, 003C und 003E bilden drei parallele Arrays

Die Berechnung in `1C76` lautet:

```asm
1C76  mov ax,[0032]
1C79  shl ax,1
1C7B  shl ax,1
1C7D  add ax,[0030]
1C81  mov [003A],ax
1C86  mov cx,[0038]
1C8D  shl cx,1
1C8F  add ax,cx
1C91  mov [003C],ax
1C94  shl cx,1
1C96  add ax,cx
1C98  mov [003E],ax
```

Somit gilt:

- `003A = 0030 + 4 * 0032`
- `003C = 003A + 2 * 0038`
- `003E = 003C + 4 * 0038`

Anschließend wird `8 * 0038` Bytes reserviert. Das entspricht drei unmittelbar aufeinanderfolgenden Arrays mit Elementbreiten 2, 2 und 4 Bytes. Die konkrete Semantik der drei Arrays ist noch nicht abschließend geklärt.

### 2107 – Der Relocation-Dispatcher liest tatsächlich aus dem Import-Segmentarray

Für Klasse `10h` wird das Indexbyte aus `AH` genommen und über `0036` in die gerade aufgebaute WORD-Tabelle umgesetzt. `DS` wird anschließend aus dem Tabellenwort geladen. Damit ist die Verbindung zwischen GEODE-Importauflösung und Relocation-Klassenpfad `10h` direkt im Code nachgewiesen.

### 2108 – Die Klasse 00h bleibt ein anderer Segmentquellenpfad

Der Dispatcherpfad für Klasse `00h` lädt `DS` nicht aus `0036`, sondern aus dem im Kernelcode hinterlegten Segmentwort `CS:[2151]`. Diese Klasse darf daher nicht mit dem Import-Segmentarray gleichgesetzt werden. Die Bedeutung der zugehörigen Tabelle und ihrer Einträge bleibt gesondert zu untersuchen.

### 2109 – Korrektur der bisherigen Feldinterpretation

Die bisherigen Abschnitte beschrieben `0036` zunächst nur als „Eingangszeiger“. Das ist jetzt präzisiert: Im Loader-Kontext wird `0036` auf `0046h` oder `005Eh` gesetzt und dient als Basis der WORD-Tabelle, in die `2652` die Ergebnisse der 14-Byte-Importauflösung schreibt. `0034` ist die Importanzahl. Diese Zuordnung ist durch Initialisierung, Schleifenschrittweite und Dispatcherzugriff gemeinsam belegt.

### 2110 – Stand und nächste Prüfschritte

**Neu gesichert:** `0034` = Anzahl der 14-Byte-Importeinträge; `0036` = Basis der WORD-Tabelle mit aufgelösten Import-Segmentwerten; `0030` = Ende dieser Tabelle und Beginn des nächsten Bereichs. `0032` zählt vier Byte weit auseinanderliegende Einträge. `0038` dimensioniert drei nachfolgende Arrays mit Elementbreiten 2, 2 und 4 Bytes.

**Nächste Schritte:** (1) `271C` und seine Aufrufkonvention analysieren, um die Importauflösung zu benennen; (2) die Headerbytes bei `0046h` und `005Eh` mit echten GEODE-Dateien vergleichen; (3) die drei Arrays ab `003Ah` anhand aller Leser und Schreiber semantisch identifizieren; (4) den Klasse-00h-Pfad separat auflösen.

**Status:** Statische Disassemblierung des deutschen Originalkernels `KERNEL.OLD`. Keine Änderung an Kerneldateien, GEO-Dateien oder `pcgeos1/geode.py`; keine Laufzeitbestätigung.

## Untersuchungen 2111–2120 – Importauflösung durch `271C` und GEODE-Namenssuche

### 2111 – Aufrufkonvention von `271C` aus dem Importtabellenleser

Die Routine `2652` liest jeden 14-Byte-Importeintrag und ruft `271C` mit folgenden Werten auf:

```asm
2693  push bx                 ; Zielslot in Import-Segmenttabelle sichern
2694  mov ax,es:[di+0A]       ; Importfeld +0Ah
2698  mov bx,es:[di+0C]       ; Importfeld +0Ch
269C  mov cx,es:[di+08]       ; Importfeld +08h
26A0  mov dx,[0000]           ; Kernel-Kontextwert
26A4  call 271C
26A7  pop bx
26A8  jb  26BB
26AA  mov [bx],ax             ; aufgelöstes Segment eintragen
```

Damit ist die Lage der drei WORD-Felder im Importdatensatz belegt. Ihre endgültigen symbolischen Namen werden noch nicht festgelegt: `AX:BX` wird später als Vergleichspaar verwendet; `CX` wirkt auf die Suche bereits geladener Module.

### 2112 – `271C` sucht zuerst nach einem bereits geladenen GEODE

Am Anfang von `271C` werden die Eingangsregister gesichert. Für die Suche setzt die Routine `AX=8`, `BX=0` und `DX=0` und ruft `1EBC` auf. `1EBC` richtet einen Suchlauf über die GEODE-Verwaltung ein; der Vergleichs-Callback liegt bei `1EDE`.

Der Callback vergleicht acht Bytes ab `ES:[DI]` des Importeintrags mit acht Bytes ab Offset `14h` im jeweiligen GEODE-Verwaltungsobjekt. Das ist ein direkter Namensvergleich über acht Zeichen.

### 2113 – Der Suchlauf berücksichtigt zusätzlich ein Flag-Muster

Der Callback bei `1EDE` liest das WORD bei `ES:[2]` des Verwaltungsobjekts und prüft es gegen `CX`. Die Sequenz `NOT SI` gefolgt von `TEST SI,CX` verwirft Einträge, deren gesetzte Bits nicht vollständig durch die Maske in `CX` abgedeckt sind. Wir halten diese beobachtete Bitprüfung fest, ohne dem Feld bereits einen nicht belegten Namen wie „Geode-Typ“ oder „Capabilities“ zu geben.

### 2114 – Ein bereits geladenes GEODE wird über seine Verwaltungsstruktur gefunden

Die Suchroutine `1E7E` traversiert eine verkettete Liste, deren Einstieg aus dem Kernelkontext über `ES:[05FD]` geladen wird. Für den nächsten Eintrag verwendet sie das Segment-/Linkfeld am Anfang des Verwaltungsobjekts und das Segmentfeld bei `ES:[44]`. Der Vergleichs-Callback `1EDE` liefert bei Namensübereinstimmung das gefundene Segment in `AX` zurück.

### 2115 – Bei einem Fehlschlag wird ein DOS-Dateiname aus dem GEODE-Namen erzeugt

Wenn `1EBC` keinen geladenen Treffer liefert, kopiert `271C` acht Zeichen aus `ES:DI` in den Kernelpuffer `CS:05E8`. Ein Punkt oder ein Nullbyte wird dabei durch Leerzeichen ersetzt; beim Punkt/Nullbyte wird der Quellzeiger zusätzlich zurückgesetzt, sodass die acht Zeichen als DOS-Basisname normalisiert werden.

Anschließend ruft `271C` die Routinen `1531`, `15A0` und `197A` auf. Der Codepfad führt damit von der Namenssuche zur Dateisuche beziehungsweise zum Öffnen und Laden des benötigten GEODE. Die genaue DOS-Funktion und Pfadpriorität bleiben Gegenstand der Folgeanalyse.

### 2116 – `197A` ist der GEODE-Datei-Einlesepfad

`197A` legt einen lokalen Arbeitsbereich an, ruft `12F6` mit `AL=A0h` auf und verarbeitet danach die Dateikennung und den GEODE-Kopf. Es folgen unter anderem die Prüfungen bei `1A56`, `1AEA`, `2652`, `1B45`, `1C76`, `1B6B` und `1B81`. Damit ist die zuvor untersuchte GEODE-Headerprüfung in den Datei-Ladepfad eingebettet.

### 2117 – Versionsvergleich `1AD4`

`1AD4` vergleicht zwei 32-Bit-Werte in der Registerpaar-Darstellung `AX:BX` und `CX:DX`. Bei Ungleichheit setzt die Routine Carry und liefert in `AX` einen Vergleichscode (`0` oder `1`); bei `AX:BX <= CX:DX` kehrt sie mit gelöschtem Carry zurück. Die Routine ist somit ein geordneter Versions-/Größenvergleich, aber der fachliche Name der verglichenen Werte ist aus diesem Ausschnitt allein noch nicht gesichert.

### 2118 – Importversion wird gegen GEODE-Kopfdaten geprüft

Nach erfolgreicher Namensauflösung stellt `271C` die ursprünglichen Importwerte `AX:BX` wieder her. Wenn `AX` ungleich null ist, lädt der Code die Vergleichswerte aus `[000E]` und `[0010]` des geladenen GEODE-Segments und ruft `1AD4` auf. Ein gesetztes Carry führt in den Fehlerpfad. Das belegt eine Kompatibilitätsprüfung anhand eines zweigliedrigen Wertes, ohne die Versionskomponenten bereits abschließend zu benennen.

### 2119 – Die aufgelöste Segmentadresse wird in die Importtabelle geschrieben

`271C` liefert das gefundene beziehungsweise neu geladene GEODE-Segment in `AX` zurück. `2652` schreibt diesen Wert nach erfolgreicher Rückkehr in den aktuellen WORD-Slot der Tabelle ab `0036`. Damit ist die Kette vollständig: Importdatensatz → Namenssuche/Dateiladen → Prüfung → Segmentwert im Import-Segmentarray → spätere Relocation-Auflösung über Klasse `10h`.

### 2120 – Abgleich mit Originaldateien und gesicherter Stand

Der erste Importdatensatz von `NOTEPAD.GEO` (DOCUMENT und WORLD) sowie `GROBJ.GEO` beginnt bei `0120h` und lautet byteweise: