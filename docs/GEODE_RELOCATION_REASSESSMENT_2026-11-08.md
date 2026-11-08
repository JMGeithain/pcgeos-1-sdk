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

```text
75 69 20 20 20 20 20 20  00 40  B5 02  00 00
u  i  [sechs Leerzeichen]  0040h 02B5h 0000h
```

Das bestätigt die 14-Byte-Schrittweite und die Feldpositionen `+08`, `+0A` und `+0C` anhand realer Dateien. Der sichtbare 8-Zeichenname `ui      ` stimmt mit dem Acht-Byte-Namensvergleich in `1EDE` überein. Die beiden Dateien liefern damit einen direkten Format-/Kernelabgleich; die semantischen Bezeichnungen der drei WORD-Felder bleiben bis zur weiteren Auswertung offen.

**Ergebnis:** `271C` ist nicht nur eine abstrakte Import-Auflösung. Die Routine sucht zuerst in der Liste bereits geladener GEODEs anhand des 8-Byte-Namens, erzeugt bei Bedarf einen DOS-Basisnamen, stößt den Datei-Ladepfad an, prüft anschließend einen zweigliedrigen Kompatibilitätswert und gibt das GEODE-Segment zurück. `2652` speichert dieses Segment in der Importtabelle ab `0036`.

**Quellenbasis:** Statische Disassemblierung des deutschen Originalkernels `KERNEL.OLD` (Load-Image-Offsets `1E7E–1F0D`, `197A–1AD3`, `2652–26BA`, `271C–27D6`) und Bytevergleich der Originaldateien `NOTEPAD.GEO` (DOCUMENT/WORLD) sowie `GROBJ.GEO` aus `GEOWORKS.zip`. Kein Laufzeittest.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, alle GEO-Dateien und `pcgeos1/geode.py`.

## Untersuchungen 2121–2130 – DOS-Dateischnittstelle des GEODE-Laders

### 2121 – `12F6` ist der zentrale Öffnungs-Einstieg

```asm
12F6  B4 3D       mov ah,3Dh
12F8  E8 01 00    call 12FC
12FB  CB          retf
```

Der Kernel setzt `AH=3Dh` und delegiert an `12FC`. DOS-Funktion `3Dh` ist der Dateiöffnungsaufruf. Der an `12F6` übergebene `AL`-Wert wird dabei nicht verändert. Im GEODE-Ladepfad setzt `197A` zuvor `AL=A0h`; dieser Wert darf nicht ohne weitere Prüfung als gültiger, gewöhnlicher DOS-Zugriffsmodus interpretiert werden, da `12FC` eine Kernelvermittlung mit zusätzlichen Prüfungen ausführt.

### 2122 – `12FC` führt die Öffnung durch einen Kernelvermittler

`12FC` sichert `CX`, `BX`, `DI` und `ES`, ruft `172F`, `15EB` und `17C3` auf und prüft danach über `AL & 03h` sowie `17F0` einen Pfad-/Statuszustand. Je nach Ergebnis wird `7A8`, `9636`, ein indirekter Callback über `ES:[05B8]` (mit `DI=4`) und gegebenenfalls `11CB` aufgerufen. Das ist mehr als ein unveränderter direkter DOS-Aufruf; die genaue Semantik der Vermittlungs- und Callback-Schritte wird separat verfolgt.

### 2123 – `1088` ist der DOS-Lesevermittler

```asm
1088  call 0F7F
108B  call 1891
108E  mov ah,3Fh
1090  call 0F63
```

DOS-Funktion `3Fh` liest Bytes von einem geöffneten Handle. Die Routine bereitet den Kontext vor und übergibt den eigentlichen DOS-Aufruf über `0F63`. Im GEODE-Kopftest wird `1088` mit `CX=0044h` und einem Stackpuffer als `DS:DX` aufgerufen.

### 2124 – `10CA` ist der DOS-Seek-Vermittler

```asm
10CA  call 0F7F
10CD  mov ah,42h
10CF  call 0F6D
```

DOS-Funktion `42h` positioniert den Dateizeiger. Der Kernel reicht den Aufruf über `0F6D` weiter. Die Parameter in `CX:DX` werden von den Aufrufern bereitgestellt; die konkrete Offset-/Origin-Kombination muss je Aufruf verfolgt werden.

### 2125 – `10D3` kombiniert Positionierung und anschließenden Lese-/Schreibpfad

```asm
10D3  call 0F7F
10D6  mov al,00h
10D8  call 10CA
10DB  jb 10E2
10DD  xor cx,cx
10DF  call 10A4
```

Die Routine setzt `AL=0` für die Seek-Operation und ruft danach bei Erfolg `10A4` auf. `10A4` setzt `AH=40h` (DOS-Schreiben) und verwendet `0F56`. Diese Routine ist daher ein zusammengesetzter Seek-/Schreibpfad, nicht der GEODE-Leseweg.

### 2126 – `1531` ist kein DOS-Open-Aufruf

Der Einstieg `1531` ruft `29DC`, `17B5`, `1666`, `142C` und `1445` auf, aktualisiert Verwaltungsfelder und markiert ein Byte bei `SI+0Ah` mit Bit `10h`. Der Ablauf sichert und restauriert außerdem den aktuellen Kontext über `17BC` und `29EE`. Damit ist `1531` als GEODE-/Dateikontextverwaltung einzuordnen, nicht als unmittelbarer DOS-Dateiöffner.

### 2127 – `15A0` baut einen Pfadpuffer auf

`15A0` reserviert `68h` Bytes auf dem Stack, kopiert `34h` WORDs aus dem Puffer bei `04A4h` und ergänzt abhängig von `BP` gegebenenfalls einen Backslash sowie einen Pfadbestandteil aus einer Tabelle ab `DS:0544h`. Anschließend ruft es `14AA` mit `DS:DX` auf den Stackpuffer auf. Das belegt eine Pfad-/Verzeichnisstring-Konstruktion; welche Pfadklasse der Index in `BP` bezeichnet, bleibt offen.

### 2128 – `197A` öffnet die Datei über `12F6` und liest den Header

Der Ladepfad setzt `DX=SI`, `AL=A0h`, `CS` als Aufrufsegment und ruft `12F6`. Bei Erfolg wird das zurückgelieferte Handle in `BX` übernommen. Danach liest der Kernel zunächst einen 44h-Byte-Headerblock über `112C`/`1088` und prüft die GEODE-Kennung `C7 45 CF 53`. Später positioniert er die Datei über `10CA` auf `00C8h` und liest weitere `18h` Bytes.

### 2129 – Die geprüften DOS-Funktionsnummern

Für den untersuchten Pfad sind folgende DOS-Funktionsnummern direkt im Kernelcode sichtbar:

- `AH=3Dh`: Datei öffnen (`12F6`)
- `AH=3Fh`: aus Handle lesen (`1088`)
- `AH=42h`: Dateizeiger positionieren (`10CA`)
- `AH=40h`: in Handle schreiben (`10A4`)

Die letzte Funktion ist ein allgemeiner Kernelvermittler und nicht als Bestandteil des GEODE-Lesevorgangs belegt.

### 2130 – Ergebnis und offene Fragen

**Gesichert:** Der GEODE-Lader öffnet über `12F6`/`12FC`, liest über `1088`/`0F63` und positioniert über `10CA`/`0F6D`. `1531` verwaltet GEODE-/Dateikontext; `15A0` baut einen Pfadpuffer auf. Der Header wird zunächst mit 44h Bytes gelesen, die GEODE-Kennung wird geprüft, anschließend wird zu `00C8h` positioniert und ein weiterer 18h-Byte-Block gelesen.

**Offen:** (1) die genaue Kernelbedeutung des `AL=A0h`-Parameters beim Öffnen; (2) die durch `15A0` ausgewählten Pfadvarianten; (3) die exakte Funktion von `112C` und `14AA`; (4) die DOS-Fehlercodes und ihre Abbildung auf GEODE-Laderfehler.

**Quellenbasis:** Statische Disassemblierung von `KERNEL.OLD` (Load-Image-Offsets `0F56–10DF`, `12F6–133A`, `14AA–15EA`, `197A–1AD3`, `271C–27D6`). DOS-Funktionsnummern sind anhand der DOS-API-Schnittstelle benannt. Keine Laufzeitbestätigung.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, sämtliche GEO-Dateien und `pcgeos1/geode.py`.

## Untersuchungen 2131–2140 – Dateigröße, Pfadwechsel und Headerfehler

### 2131 – `112C` ermittelt die Dateigröße über drei Seek-Operationen

Die Routine `112C` prüft zunächst über `1164`, ob der Handle für diesen Weg geeignet ist. Im normalen Handle-Zweig führt sie danach diese DOS-Seek-Sequenz aus:

```asm
1135  xor cx,cx
1137  xor dx,dx
1139  mov al,01
113B  call 10CA       ; SEEK_CUR, aktuelle Position lesen
113E  mov si,dx
1140  xchg ax,di      ; aktuelle Position DX:AX sichern
1141  mov al,02
1143  xor cx,cx
1145  xor dx,dx
1147  call 10CA       ; SEEK_END, Dateiende ermitteln
114A  push ax
114B  push dx          ; Dateigröße sichern
114C  mov cx,si
114E  mov dx,di
1150  mov al,00
1152  call 10CA       ; SEEK_SET, ursprüngliche Position restaurieren
1155  pop dx
1156  pop ax
```

Die DOS-Ursprungswerte sind `AL=0` (Dateianfang), `AL=1` (aktuelle Position) und `AL=2` (Dateiende). Damit liefert `112C` im normalen Zweig die 32-Bit-Dateigröße in `DX:AX` zurück und stellt zugleich den vorherigen Dateizeiger wieder her. Das ist für den GEODE-Lader relevant, weil `197A` direkt nach dem Öffnen `112C` aufruft und anschließend aus `DX:AX` einen Größen-/Allokationswert berechnet.

### 2132 – Die Sonderbehandlung in `112C` hängt von der Handle-Klassifizierung ab

`1164` ruft `118F` auf. `118F` holt über den aktuellen DS-Kontext und `0F7F` einen Verwaltungszeiger und liest daraus das WORD-Feld bei `+06`. Ist dieses Feld null, wird ein kurzer Statusvergleich ausgeführt. Andernfalls werden `5A4` und `0CC5` aufgerufen und Bit `20h` aus `AH` ausgewertet. Nur bei gesetztem Statusbit wird der normale Seek-Ende-Weg ausgeführt. Der alternative Pfad setzt `DI=000Eh` und ruft `1180` auf, das einen indirekten Callback über `ES:[05B8]` ausführt. Die genaue Bedeutung dieses Handle-Typs und des Callbacks ist noch nicht benannt.

### 2133 – `14AA` wechselt Laufwerk und aktuelles Verzeichnis

Der Code ab `14AA` sichert den aktuellen Kontext, ruft `17B5` und `9630`, ermittelt das aktuelle Laufwerk/Verzeichnis und setzt anschließend mit DOS `AH=0Eh` das Ziellaufwerk sowie mit `AH=3Bh` das Zielverzeichnis. Bei Erfolg wird über `AH=47h` das Verzeichnis des Ziellaufwerks gelesen und in den Kernelkontext zurückgeführt. Die Routine ist damit kein einfacher String- oder Dateiname-Konverter, sondern verwaltet einen temporären Laufwerks-/Verzeichniswechsel.

### 2134 – `15A0` konstruiert einen Pfad für `14AA`

`15A0` reserviert `68h` Bytes auf dem Stack und kopiert `34h` WORDs aus dem Puffer ab `DS:04A4`. Wenn `BP` ungleich null ist, sucht es im kopierten Pfad nach dem abschließenden Nullbyte, ergänzt nötigenfalls `\` und hängt danach einen String aus der Tabelle der Zeiger bei `DS:0544` an. Der Index ist `2*BP`. Der zusammengesetzte Pfad wird an `14AA` übergeben. Belegt ist die Konstruktion aus Basisverzeichnis plus indiziertem Zusatzpfad; die symbolischen Namen und die Bedeutung aller Indizes bleiben offen.

### 2135 – `AL=A0h` wird unverändert bis zum DOS-Open-Vermittler weitergereicht

`197A` setzt vor dem Aufruf von `12F6` `AL=A0h`. `12F6` setzt lediglich `AH=3Dh` und springt nach `12FC`; der Wert in `AL` bleibt dabei unverändert. `12FC` führt zusätzliche Kernelprüfungen und Callback-Schritte aus, bevor der DOS-Open-Pfad erreicht wird. Daher ist `A0h` zunächst als kernelinterner Open-Modusparameter dokumentiert. Seine genaue Bedeutung kann aus diesem Ausschnitt allein nicht zuverlässig auf ein Standard-DOS-Zugriffsrecht reduziert werden.

### 2136 – `12FC` prüft den Pfadstatus vor dem eigentlichen Öffnen

`12FC` sichert Register, ruft `172F`, `15EB` und `17C3` auf und testet danach `AL & 03h`. Bei gesetzten Bits wird `17F0` ausgeführt. Danach folgen der Kernelvermittler `7A8`, das Setzen des ES-Kontexts über `9636` und ein indirekter Callback `ES:[05B8]` mit `DI=0004`. Bei erfolgreichem Callback wird `11CB` ausgeführt. Anschließend restauriert der Code den Kontext und ruft `1628` sowie `1736` auf. Das bestätigt, dass `12FC` kein transparenter Eins-zu-eins-Wrapper um DOS `3Dh` ist.

### 2137 – `17F0` liefert einen Status-/Fehlerwert für die Pfadprüfung

`17F0` wechselt in den Kernel-DS-Kontext, ruft `0885` auf und invertiert dessen Carry-Status. Bei einem Fehler folgt eine zweite Prüfung über `063C`; schlägt auch diese fehl, wird `AX=0013h` gesetzt. Der genaue fachliche Name des geprüften Zustands ist nicht belegt. Fest steht nur, dass `12FC` den Rückgabestatus von `17F0` zur Entscheidung über den folgenden Callback-Pfad verwendet.

### 2138 – `197A` liest nach dem 44h-Byte-Kopfblock gezielt ab Dateioffset `00C8h`

Nach Prüfung der GEODE-Signatur `C7 45 CF 53` und des WORD-Feldes bei Headeroffset `0004h` setzt `1A56` den Dateizeiger mit `AL=0`, `CX=0`, `DX=00C8h` auf den absoluten Offset `00C8h`. Danach liest es genau `18h` Bytes in den Stackpuffer ab `BP-26h`. Damit ist der zweite Leseabschnitt nicht bloß ein Fortsetzen des Headerlesens, sondern ein gezielter Zugriff auf den festen Header-/Metadatenbereich ab `00C8h`.

### 2139 – Die Fehlernummern `02h` bis `08h` sind interne Loaderstatuswerte

Die Routine `197A` setzt in den jeweiligen Prüfpfaden unter anderem `AX=02h` nach fehlgeschlagenem Öffnen, `AX=04h` nach fehlgeschlagenem Lesezugriff, `AX=05h` bei falscher GEODE-Kennung, `AX=06h` bei nicht-null WORD an Headeroffset `0004h`, `AX=07h` bei einer nicht passenden gespeicherten WORD-Angabe und `AX=08h` bei fehlgeschlagener Bitmaskenprüfung. Das sind im untersuchten Code gesetzte interne Rückgabewerte des GEODE-Laders; sie dürfen nicht mit den DOS-Fehlercodes gleichgesetzt werden.

### 2140 – Ergebnis und offene Punkte

**Neu gesichert:** `112C` ermittelt im normalen Dateihandle-Zweig die Dateigröße mit `SEEK_END` und restauriert die ursprüngliche Dateiposition. `14AA` führt einen temporären Laufwerks-/Verzeichniswechsel durch. `15A0` konstruiert den dazu übergebenen Pfad aus einem Basisverzeichnis und einem indizierten Zusatzpfad. `AL=A0h` wird vom Einstieg `12F6` bis in die zusätzliche Kernelvermittlung `12FC` unverändert übernommen. `197A` liest nach dem ersten 44h-Byte-Block gezielt weitere 18h Bytes ab Dateioffset `00C8h`. Die Fehlerwerte `02h` bis `08h` sind interne Loaderstatuswerte.

**Offen:** (1) genaue Klassifizierung des Handles in `1164` und Semantik des Callbacks `ES:[05B8]`; (2) symbolische Bedeutung der Pfadzeigertabelle ab `0544h`; (3) fachliche Bedeutung des `A0h`-Open-Modusparameters; (4) Bedeutung der Metadaten ab `00C8h` und der dort geprüften WORD-/Bitmaskenfelder.

**Quellenbasis:** Statische Disassemblierung des deutschen Originalkernels `KERNEL.OLD`, Load-Image-Offsets `10CA–11CA`, `12F6–133A`, `14AA–15EA`, `17F0–180E` und `197A–1AD3`. DOS-Seek-Ursprünge und Funktionsnummern sind gemäß DOS-API benannt. Keine Laufzeitbestätigung.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, alle GEO-Dateien und `pcgeos1/geode.py`.

## Untersuchungen 2141–2150 – GEODE-Kopfblock ab 00C8h

### 2141 – Die 24 Byte ab 00C8h sind ein festes Loader-Metadatenfenster

Der Code im deutschen Originalkernel (Load-Image-Offsets 1A56h–1AE9h; Dateioffsets 2056h–20E9h) positioniert den Dateizeiger absolut auf 00C8h und liest genau 18h Bytes. Das ist ein gezielter Zugriff auf den GEODE-Metadatenkopf, nicht bloß ein Fortsetzen des vorherigen 44h-Byte-Lesens.

### 2142 – 00CAh enthält den vom Aufrufer erwarteten GEODE-Typ

Der Loader vergleicht das am Eintritt gesicherte BX mit dem WORD aus dem Metadatenpuffer bei 00CAh. Bei Abweichung liefert er den internen Status 07h zurück. Im Archiv passen die Werte zu den beobachteten GEODE-Kategorien: NOTEPAD.GEO hat 0001h (Anwendung), GROBJ.GEO 0002h (Bibliothek); zahlreiche Treiberdateien, etwa EGA.GEO und DOS5.GEO, tragen 0003h. Die Zuordnung 1=Anwendung, 2=Bibliothek, 3=Treiber ist durch mehrere Dateibeispiele gestützt.

### 2143 – 00CCh:00CEh wird gegen die Kernel-Protokollgrenze 026Eh:0003h geprüft

Der Loader lädt WORDs aus 00CCh und 00CEh und vergleicht das Paar mit der Konstanten 026Eh:0003h über Routine 20D4h. Die Vergleichsroutine akzeptiert Werte kleiner oder gleich dieser Grenze und weist größere Werte zurück. NOTEPAD.GEO, GROBJ.GEO und die geprüften System-GEODEs enthalten überwiegend 026Eh:0003h; CUA.GEO enthält beispielsweise 026Eh:0001h und liegt damit innerhalb der Grenze. Belegt ist damit eine obere Kompatibilitätsgrenze des vom GEODE angegebenen Protokollwerts. Ob die Felder in der offiziellen Terminologie „required kernel protocol“ oder anders benannt werden, wird ohne zusätzliche Spezifikation nicht festgelegt.

### 2144 – 00D0h, 00D2h und 00D4h sind Ressourcen-, Import- und Exportanzahl

Die Loaderarithmetik in 20EAh verwendet diese drei WORD-Felder in einer Weise, die mit dem GEODE-Tabellenlayout übereinstimmt. Unabhängig davon bestätigt der bestehende Formatparser die gleichen Felder: 00D0h = Ressourcenanzahl, 00D2h = Importanzahl, 00D4h = Exportanzahl. Beispiele: NOTEPAD = 15 Ressourcen, 2 Importe, 0 Exporte; GROBJ = 20 Ressourcen, 1 Import, 21 Exporte.

### 2145 – 00DAh ist eine Attributmaske, die der Loader mit zwei Aufrufermasken prüft

Der Loader liest das WORD bei 00DAh. Zuerst prüft er die Schnittmenge mit der vom Aufrufer gelieferten Maske in DX; eine Überschneidung führt zum Fehlerstatus 08h. Danach invertiert er die GEODE-Maske und prüft sie gegen die Aufrufermaske in CX; ebenfalls führt eine fehlende geforderte Eigenschaft zum Status 08h. Formal muss gelten: (GEODE-Attribute AND DX) = 0 und (GEODE-Attribute AND CX) = CX. Welche einzelnen Bits fachlich bedeuten, bleibt offen.

### 2146 – Bit 7 des Bytes 00C9h erweitert die interne Speicheranforderung um 18h Bytes

Routine 20EAh prüft `byte [00C9h] AND 80h`. Ist das Bit gesetzt, addiert sie 18h zur berechneten internen Allokationsgröße. Das ist direkt im Code belegt. NOTEPAD.GEO (C9h=96h), SPLAY.GEO (92h), NOTEPADG.GEO (96h) und zahlreiche weitere Applikations-GEODEs haben das Bit gesetzt; GROBJ.GEO (50h) und typische Treiber-GEODEs (30h/38h) nicht. Die Bedeutung der Zusatzstruktur ist damit noch nicht benannt.

### 2147 – Die interne Allokationsgröße wird aus den drei Zählern berechnet

Die Instruktionsfolge in 20EAh ergibt exakt:

`0x46 + 8 * Ressourcenanzahl + 4 * Exportanzahl + 2 * Importanzahl`

Bei gesetztem Bit 7 in 00C9h kommen weitere 0x18 Bytes hinzu. Das Ergebnis wird an die Kernelroutine 6E87h übergeben (Aufruf mit CX=8080h). Die frühere Adressangabe 7487h war falsch; sie wurde durch erneute Disassemblierung des Load-Image korrigiert. Diese Formel beschreibt die angeforderte interne Verwaltungsgröße; sie ist nicht die Dateigröße und auch nicht die Länge des GEODE-Dateikopfs.

### 2148 – Die Felder 00D6h und 00D8h–00DEh werden in diesem Prüfpfad nicht ausgewertet

Im untersuchten 24-Byte-Lese-/Prüfpfad verwendet der Kernel 00C9h, 00CAh, 00CCh, 00CEh, 00D0h, 00D2h, 00D4h und 00DAh. Die WORD-Felder 00D6h, 00D8h, 00DCh und 00DEh werden in diesem Pfad nicht verwendet. Aus ihren Werten allein werden daher keine Bedeutungen abgeleitet.

### 2149 – Stichprobenabgleich über die mitgelieferten GeoWorks-1.x-GEODEs

Der Abgleich wurde nicht nur an NOTEPAD und GROBJ durchgeführt. Im Archiv zeigen beispielsweise EGA.GEO und DOS5.GEO Typ 0003h; CUA.GEO Typ 0002h; NOTEPADG.GEO Typ 0001h. Die Protokollwerte liegen bei diesen Beispielen innerhalb der vom Kernel akzeptierten Grenze. Die Anzahlwerte an 00D0h/00D2h/00D4h stimmen mit den Duplikatfeldern und Tabellenpositionen überein, die der vorhandene Parser prüft.

### 2150 – Ergebnis und offene Punkte

**Neu gesichert:** 00CAh ist der erwartete GEODE-Typ; 00CCh:00CEh ist ein Protokoll-/Kompatibilitätswert, der höchstens 026Eh:0003h betragen darf; 00D0h/00D2h/00D4h sind Ressourcen-/Import-/Exportanzahl; 00DAh ist eine vom Aufrufer maskiert geprüfte Attributmaske. Bit 7 von 00C9h erweitert die interne Verwaltungsallokation um 18h Bytes. Die Allokationsformel lautet `46h + 8*R + 4*E + 2*I`, zuzüglich optional 18h.

**Offen:** (1) offizielle symbolische Namen und Bedeutung aller Bits im WORD 00C8h/Attributfeld 00DAh; (2) genaue Struktur der zusätzlichen 18h Bytes; (3) Semantik der übrigen Felder 00D6h und 00D8h–00DEh; (4) offizielle Benennung des Protokollpaares 00CCh:00CEh.

**Quellenbasis:** Deutscher Originalkernel `KERNEL.OLD`, Load-Image-Offsets 1A56h–1AE9h und 20EAh–210Ah (die Speichergrößenberechnung liegt im Load-Image-Bereich 20EAh–210Ah); Original-GEODE-Dateien im `GEOWORKS.zip`, insbesondere NOTEPAD.GEO, GROBJ.GEO, CUA.GEO, EGA.GEO, DOS5.GEO und NOTEPADG.GEO; vorhandene `pcgeos1/geode.py`-Parserdefinition. Statische Analyse, keine Laufzeitbestätigung.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, alle GEO-Dateien und `pcgeos1/geode.py`.

## Untersuchungen 2151–2155 – Verwaltungsblock und Allokationspfad

### 2151 – Korrektur der Allokationsadresse aus Untersuchung 2147

Die erneute Prüfung der Bytes im tatsächlich extrahierten `KERNEL.OLD.LOAD` korrigiert die frühere Zieladresse: Die Routine bei Load-Image-Offset `7487h` ist nicht das Ziel des Aufrufs in der GEODE-Laderoutine. Der Aufruf liegt bei `1B09h` und hat das relative Ziel `6E87h` (`E8 7B 53`). Die Größenformel aus 2147 bleibt unverändert belegt; ausschließlich die Zieladresse war falsch dokumentiert.

### 2152 – Aufrufkonvention der Allokationsroutine 6E87h

Vor `CALL 6E87h` enthält `AX` die berechnete Verwaltungsgröße und `CX` den Wert `8080h`. Die Routine `6E87h` liest zunächst `SS:[0002h]` nach `BX` und fällt anschließend in den gemeinsamen Verwaltungs-/Speicherpfad ab `6E8Ch`. Bei Rückkehr aus dem Aufruf prüft der GEODE-Loader das Carry-Flag. Im Erfolgszweig wird `AX` als Segment in `DS` übernommen; `BX` wird als Verwaltungswert weiterverwendet. Die genaue symbolische API-Bezeichnung ist durch diese statische Analyse allein nicht gesichert.

### 2153 – Initialisierung der festen ersten 40h Bytes

Nach erfolgreicher Allokation setzt der Loader `DS=AX`, ruft die Dateileseroutine `1088h` mit `CX=0040h`, `DX=0000h` und `AL=0` auf und initialisiert damit die ersten `40h` Bytes des neuen Blocks auf null. Danach folgen diese WORD-Schreibzugriffe:

| Blockoffset | Eingetragener Wert |
|---|---|
| `0000h` | `SI` (aus dem vorherigen Allokations-/Verwaltungspfad) |
| `0040h` | `BX` (zurückgekehrter Verwaltungswert) |
| `0042h` | `SS:[0002h]` |

Zusätzlich wird der globale WORD-Zähler bei `0026h` inkrementiert. Die Offsets sind direkte Speicheroperanden der Instruktionen bei `1B1Fh–1B32h`; die fachlichen Namen der Felder bleiben offen.

### 2154 – Die Bereiche ab 30h werden aus den GEODE-Zählern berechnet

Die Folge ab `1B45h` berechnet im neuen Block zunächst `WORD [0030h] = 2 * WORD [0034h] + WORD [0036h]`. Der Wert bei `0032h` wird anschließend als Schleifenzähler verwendet. In `1C76h–1C9Dh` wird aus `WORD [0032h]` ein Vierfacher gebildet und zu `WORD [0030h]` addiert; das Ergebnis wird bei `003Ah` abgelegt. Aus `WORD [0038h]` werden weitere, aufeinanderfolgende Bereichsgrenzen `003Ch` und `003Eh` berechnet. Diese Werte dienen danach als Ziel-/Grenzpositionen beim Nullsetzen und beim Aufbau von Zeiger-/Tabellenbereichen. Eine abschließende Zuordnung der Zähler bei `0032h`, `0034h`, `0036h` und `0038h` zu Ressourcen, Importen oder Exporten ist aus diesem Ausschnitt allein noch nicht sicher; sie wird nicht vorweggenommen.

### 2155 – Der 18h-Zusatzbereich wird nicht als einfacher Tabellenanhang behandelt

Der gesetzte Bit-7-Zweig des Bytes `00C9h` addiert weiterhin `18h` zur Allokationsgröße. Spätere Initialisierung verwendet außerdem das Bit `80h` im Statusbyte bei Blockoffset `0003h` und greift dann auf zusätzliche Metadaten/Zeiger zu, unter anderem auf `00A`/`008` in einem über einen Zeiger ermittelten Segment sowie auf einen Bereich ab `0056h`. Das zeigt, dass der Zusatzbereich mit einer gesonderten Initialisierungslogik zusammenhängt. Seine vollständige Struktur und sein offizieller Zweck sind damit noch nicht bewiesen.

**Quellenbasis:** Deutscher Originalkernel `KERNEL.OLD`, Load-Image-Offsets `1AEAh–1B44h`, `1B45h–1C75h`, `1C76h–1D68h`, `6E87h–6E9Ah` und `2153h–21BDh`. Analyse ausschließlich statisch; keine Laufzeitbestätigung.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, alle GEO-Dateien und `pcgeos1/geode.py`.


## Untersuchungen 2156–2160 – Ressourcenallokation und optionaler Zusatzblock

### 2156 – Die Routine 1D51h legt einen einzelnen Ressourcenblock an

Die Routine `1D51h` wird aus der Schleife ab `1D0Bh` aufgerufen, nachdem ein Eintrag aus dem bei `003Ah` adressierten Bereich gelesen wurde. Sie prüft zunächst `SI=2`; in diesem Sonderfall addiert sie den lokalen Wert bei `[BP-18h]` zur angeforderten Größe und setzt Bit `80h` in `CH`. Anschließend ruft sie mit `CALL 6E87h` die gleiche Speicherverwaltung wie der Hauptblock auf. Nach Erfolg werden Verwaltungsdaten in den neuen Block geschrieben und der zurückgegebene Blockzeiger in die bei `003Ah` adressierte Tabelle eingetragen. Damit ist belegt, dass der Loader neben dem zentralen GEODE-Verwaltungsblock weitere Speicherblöcke anlegt. Die genaue Bedeutung der Sondergröße bei `SI=2` bleibt offen.

### 2157 – Der Loader speichert Blockverweise in einer indizierten Tabelle

In `1D8Ah–1D98h` schreibt der Loader einen Wert aus dem Kernel-Segment an Blockoffset `0008h`, übernimmt den neuen Blockzeiger aus `BX` nach `AX` und speichert ihn bei `[003Ah + SI]`. Die Schleife erhöht `SI` jeweils um zwei. Das ist ein WORD-indiziertes Zeigerfeld. Welche konkrete Ressourcenkategorie die einzelnen Indizes repräsentieren, ist aus diesem Ausschnitt nicht abzuleiten.

### 2158 – Die optionale 18h-Struktur besitzt mindestens Felder bei 46h und 48h

Die Routine `1E1Fh` prüft den lokalen Wert `[BP-12h]`. Ist er ungleich null, schreibt sie ihn nach `DS:[0046h]`. Danach berechnet sie einen Tabellenindex aus `[BP-10h]`, liest den zugehörigen WORD-Wert aus der Tabelle ab `003Ah` und schreibt ihn nach `DS:[0048h]`. Beide Felder liegen direkt hinter dem festen 46h-Byte-Grundbereich und sind damit konkrete Bestandteile des optionalen Zusatzbereichs bzw. des erweiterten Verwaltungsblocks. Die Funktion dieser beiden Zeigerwerte ist noch nicht abschließend benannt.

### 2159 – Der Aufbau des optionalen Bereichs greift zusätzlich auf Offset 56h zu

Die Routine `1C16h` wird nur ausgeführt, wenn Bit `80h` im Statusbyte bei Blockoffset `0003h` gesetzt ist. Sie liest Werte über die Tabellen-/Segmentzeiger bei `003Ah` und `0036h`, schreibt zwei WORD-Werte in ein ermitteltes Segment bei Offsets `0008h` und `000Ah` und initialisiert anschließend vier WORDs ab `0056h`. Bei gesetztem globalen Zustand `WORD [0FB8h]` stammen diese vier WORDs aus dem Segment `SS:[0004h]`, andernfalls werden sie mit null gefüllt. Danach folgt ein weiterer Aufruf zur Initialisierung über `27D8h`. Damit ist die Nutzung des Zusatzbereichs bei `0056h` direkt belegt; die vier WORDs sind noch nicht symbolisch identifiziert.

### 2160 – Zwischenstand: Allokation und Verwaltungsarrays getrennt betrachten

Die Befunde zeigen zwei Ebenen: (1) den zentralen Verwaltungsblock mit festem Grundbereich `46h` und den daraus berechneten Tabellenbereichen; (2) zusätzliche, einzeln über `6E87h` angelegte Speicherblöcke, deren Verweise in einem WORD-indizierten Bereich abgelegt werden. Der optionale Zusatzbereich ab `46h` enthält mindestens die beschriebenen Felder bei `46h`, `48h` und `56h`; seine Gesamtstruktur bleibt offen. Eine endgültige Zuordnung der Tabellenindizes zu GEODE-Ressourcen, Importen oder Exporten wird erst nach Verfolgung der vorgelagerten Zähler- und Tabellenbefüllung vorgenommen.

**Quellenbasis:** Deutscher Originalkernel `KERNEL.OLD`, Load-Image-Offsets `1C16h–1C75h`, `1D0Bh–1D68h`, `1D8Ah–1E37h` und `2300h–2355h`. Analyse ausschließlich statisch; keine Laufzeitbestätigung.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, alle GEO-Dateien und `pcgeos1/geode.py`.


## Untersuchungen 2161–2165 – Offsetprüfung und Tabellenlayout

### 2161 – Korrektur der zwischenzeitlichen Offset-Warnung

Eine zwischenzeitliche Warnung, die Routine bei Load-Image-Offset `197Ah` liege im DOS-Startcode, war falsch. Ursache war die fehlerhafte Kombination von `objdump --adjust-vma` und `--start-address`: Der Startoffset wurde dadurch als VMA statt als gewünschter Dateioffset behandelt. Die korrekte Disassemblierung erfolgt hier ohne `--adjust-vma`, direkt mit `--start-address=0x197a` auf `KERNEL.OLD.LOAD`. Sie zeigt bei `197Ah` die GEODE-Laderoutine, bei `1A56h` den Headerlese-/Signaturpfad und bei `1AEAh` die Größenberechnung. Die Befunde 2141–2160 werden daher nicht verworfen; die zwischenzeitliche gegenteilige Aussage wird ausdrücklich zurückgenommen.

### 2162 – Allokationsformel direkt aus den Headerzählern bestätigt

Die korrekte Instruktionsfolge bei `1AEAh–1B06h` lautet:
- `AX = 2 * [BP-1Eh]` (Headerwort `D0h`, Ressourcenanzahl),
- Addition von `[BP-1Ah]` (Headerwort `D4h`, Exportanzahl),
- Verdopplung,
- Addition von `[BP-1Ch]` (Headerwort `D2h`, Importanzahl),
- erneute Verdopplung,
- Addition `46h`,
- optional Addition `18h`, falls Bit 7 von Headerbyte `C9h` gesetzt ist.

Damit ist die Formel `46h + 8*R + 4*E + 2*I` unmittelbar durch die Maschineninstruktionen belegt. Anschließend erfolgt `CALL 6E87h` mit `CX=8080h`.

### 2163 – Tabellenanfänge werden im Verwaltungsblock dynamisch berechnet

Die Routine `1C76h` berechnet:
- `[3Ah] = [30h] + 4 * [32h]`
- `[3Ch] = [3Ah] + 2 * [38h]`
- `[3Eh] = [3Ah] + 6 * [38h]`

Davor setzt `1B45h`:
- `[30h] = 2 * [34h] + [36h]`

Diese Gleichungen sind direkte Befunde. Sie zeigen, dass die Verwaltungsstruktur mehrere aufeinanderfolgende Tabellen-/Teilbereiche über Offsets verwaltet. Die symbolische Zuordnung von `[32h]`, `[34h]`, `[36h]` und `[38h]` zu den GEODE-Zählertypen wird noch nicht behauptet.

### 2164 – Die Tabellenbereiche werden tatsächlich für Ressourcenverweise benutzt

Die Routine `1D9Ch` greift auf den über `[3Ah]` adressierten Bereich zu, liest über den zweiten WORD-Eintrag einen Segmentwert und über den folgenden WORD-Eintrag eine Anzahl, die mit 16 multipliziert und um einen lokalen Größenwert vermindert wird. Danach wird `SI=2` gesetzt und eine weitere Speicher-/Laderoutine aufgerufen. In der Schleife `1DD4h–1E1Bh` werden weitere WORD-Einträge des Bereichs `[3Ah]` mit Schrittweite 2 gelesen und als Verweise auf separate Blöcke verwendet. Das bestätigt eine WORD-indizierte Tabelle von Blockverweisen; eine Gleichsetzung jedes Eintrags mit genau einer Ressource ist ohne die vollständige Befüllungsroutine noch nicht bewiesen.

### 2165 – Relokations-/Adressauflösung liest mehrere Tabellenbereiche

Die Routine bei `2153h` wird von `1C04h` aufgerufen und verarbeitet den Relokationstyp in `AL` sowie die Klasse in `DL`. Die Verzweigung für Klasse `10h` verwendet `[36h]` als Basis einer WORD-Tabelle; andere Klassen verwenden den über `[3Ah]` berechneten Bereich oder die über `[30h]` adressierten Einträge. Das belegt, dass die Felder `30h`, `36h` und `3Ah` nicht bloße Größenwerte sind, sondern zur Laufzeit als Tabellenbasen/Offsets in der Adressauflösung dienen. Die exakten Feldnamen und die komplette Klassenzuordnung bleiben Gegenstand der nächsten Untersuchung.

**Quellenbasis:** Deutscher Originalkernel `KERNEL.OLD`, Load-Image-Offsets `197Ah–1B0Ch`, `1B45h–1C16h`, `1C16h–1E37h` und `2153h–2217h`. Die Disassemblierung wurde ohne `--adjust-vma` erstellt, damit die angegebenen Startadressen den tatsächlichen Offsets im Load-Image entsprechen. Analyse ausschließlich statisch; keine Laufzeitbestätigung.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, alle GEO-Dateien und `pcgeos1/geode.py`.


## Untersuchungen 2166–2170 – Zuordnung der Tabellenbereiche

### 2166 – [34h] ist die Importanzahl und [36h] der Importtabellenanfang

Die Routine `2652h` setzt `[36h]` abhängig vom Statusbit `80h` bei `DS:[0003h]` auf `0046h` oder `005Eh`. Danach liest sie `[34h]` als Schleifenzähler und verarbeitet je Eintrag einen 14-Byte-Datensatz (`AX=000Eh`, `MUL CX`). Die Datensätze werden über die Dateileseroutine in einen temporären Stackbereich eingelesen. Pro Eintrag wird ein WORD-Ergebnis an `[36h]` mit Schrittweite 2 abgelegt. Das entspricht der Importanzahl und der zweibytebreiten Importtabelle. Die Zuordnung wird zusätzlich durch die GEODE-Headerangabe D2h (Importanzahl) und die 14-Byte-Importdatensatzgröße bestätigt.

### 2167 – [30h] ist der Exporttabellenanfang

Die Routine `1B45h` berechnet `[30h] = [36h] + 2 * [34h]`. Damit beginnt der nächste Bereich unmittelbar nach der WORD-Tabelle der Importverweise. Anschließend verwendet sie `[32h]` als Anzahl und verarbeitet `4 * [32h]` Bytes ab `[30h]`; die Schleife `1B6Bh–1B7Eh` läuft genau `[32h]` Mal mit 4-Byte-Schrittweite. Dies identifiziert `[32h]` als Exportanzahl und `[30h]` als Exporttabellenanfang.

### 2168 – [3Ah] ist der Ressourcentabellenanfang

Die Routine `1C76h` berechnet `[3Ah] = [30h] + 4 * [32h]`. Der Bereich folgt somit direkt auf die 4-Byte-Exporttabelle. `[38h]` steuert danach die Grenzen innerhalb dieses Bereichs: `[3Ch] = [3Ah] + 2 * [38h]` und `[3Eh] = [3Ah] + 6 * [38h]`. Da die Allokationsformel acht Bytes je Ressource vorsieht und die Ressourcenzugriffe den Bereich `[3Ah]` mit WORD-Schrittweite indizieren, ist `[38h]` die Ressourcenanzahl.

### 2169 – Vollständige Tabellenfolge stimmt mit der Allokationsgröße überein

Damit ist die interne Tabellenfolge im Verwaltungsblock jetzt durch Berechnungen und Zugriffe nachvollziehbar:
1. Importverweise: `[36h]`, Länge `2 * [34h]` (Importanzahl).
2. Exporteinträge: `[30h]`, Länge `4 * [32h]` (Exportanzahl).
3. Ressourceneinträge: `[3Ah]), Länge `8 * [38h]` (Ressourcenanzahl).

Die Reihenfolge der Zähler ist damit nicht identisch mit der Reihenfolge der Headerwörter: Header D0h = Ressourcen, D2h = Importe, D4h = Exporte; interne Felder [32h] = Exporte, [34h] = Importe, [38h] = Ressourcen. Die Gesamtlänge ist `46h + 2I + 4E + 8R`, zuzüglich optionaler `18h`.

### 2170 – Bedeutung der Offsets 3Ch und 3Eh bleibt auf Unterfelder begrenzt

Die Offsets `[3Ch]` und `[3Eh]` markieren innerhalb des Ressourcenbereichs Grenzen nach `2R` bzw. `6R` Bytes. Zusammen mit `[3Ah]` zerlegen sie die acht Bytes pro Ressourceneintrag in Teilbereiche von 2, 4 und 2 Bytes. Das ist eine belastbare strukturelle Beobachtung. Die exakten Feldnamen und die Semantik der drei Teilfelder werden erst nach Auswertung der Lese- und Schreibzugriffe in den Ressourcen-/Relokationsroutinen vergeben.

**Quellenbasis:** Deutscher Originalkernel `KERNEL.OLD`, Load-Image-Offsets `1B45h–1B7Eh`, `1C76h–1CA5h`, `1D9Ch–1E1Bh`, `2153h–2217h` und `2652h–26AFh`; GEODE-Headerzähler D0h/D2h/D4h und die 14-Byte-Importdatensatzstruktur. Analyse ausschließlich statisch; keine Laufzeitbestätigung.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, alle GEO-Dateien und `pcgeos1/geode.py`.



## Untersuchungen 2171–2180 – Ressourcenpfad und kleinste Vergleichs-GEODEs

### 2171 – Nach dem Tabellenaufbau folgt ein zweistufiger Ressourcenpfad

Die Routine bei `1B81h` prüft Statusbits im GEODE-Verwaltungsblock (`DS:[0003h]`). Bei gesetztem Bit `20h` wird über die bei `28h/2Ah` gespeicherte Callback-Adresse ein weit entfernter Aufruf ausgeführt; bei gesetztem Bit `40h` wird zusätzlich die Routine `2630h` aufgerufen. Danach folgen `1C16h` und `2329h`. Damit ist belegt, dass die Ressourcenverarbeitung nicht allein aus dem Lesen der Ressourcentabelle besteht: Callback- und Nachbearbeitungspfade sind Teil des Ladevorgangs. Die Bedeutung der Statusbits wird hier noch nicht über ihre beobachtete Kontrollflusswirkung hinaus benannt.

### 2172 – Callback-Aufruf verwendet einen GEODE-eigenen Funktionszeiger

Bei `1B90h–1BB8h` wird die Adresse aus den Verwaltungsfeldern `28h/2Ah` als FAR-Prozedur aufgerufen. Vorher werden `CX` und `DX` aus dem aktuellen Stackframe übernommen; `DI` wird auf null gesetzt. Ein gesetztes Carry führt anschließend zum Fehlercode `0Dh`, andernfalls wird Statusbit `01h` gesetzt. Das ist ein konkreter Loader-Callback-Pfad, aber noch kein Beleg dafür, dass jede Anwendung diesen Callback bereitstellen muss.

### 2173 – Importdatensätze werden mit 14 Byte eingelesen und einzeln aufgelöst

Die Routine `2652h–26B3h` liest je Import genau `0Eh` Bytes. Aus jedem Datensatz werden die WORDs bei Offset `+08h`, `+0Ah` und `+0Ch` an die Auflösungsroutine `271Ch` übergeben. Das Ergebnis wird in der internen Importtabelle ab `[36h]` als WORD gespeichert. Die 14-Byte-Größe und die Position der drei übergebenen WORDs sind direkt aus den Instruktionen belegt; symbolische Feldnamen werden noch nicht vergeben.

### 2174 – Importauflösung prüft vorhandene GEODEs anhand von Eigenschaften und Namen

Die Routine `271Ch` ruft `1EBCh` auf. Der dortige Suchpfad bei `1EDEh–1F0Dh` vergleicht zunächst die GEODE-Eigenschaften bei `ES:[0002h]` mit den übergebenen Masken und prüft optional einen weiteren WORD-Wert bei `ES:[0004h]`. Danach werden 20 Bytes zwischen einem Suchdatensatz und dem GEODE-Namensbereich verglichen. Damit ist eine Eigenschafts-/Namensprüfung bei der Suche nach einer passenden geladenen GEODE belegt. Die vollständige Bedeutung der Masken und des 20-Byte-Feldes bleibt offen.

### 2175 – Die Importtabelle enthält aufgelöste WORD-Verweise, nicht die 14-Byte-Datensätze

Nach erfolgreicher Auflösung schreibt `2652h–26B3h` nur AX an die jeweilige WORD-Position der Tabelle `[36h]`; der temporäre 14-Byte-Datensatz wird mit Schrittweite `0Eh` weitergeschaltet. Die interne Tabelle ist daher eine kompakte Folge aufgelöster WORD-Werte. Die vollständigen Importdatensätze dienen dem Such-/Auflösungsvorgang und werden nicht unverändert in diese Tabelle kopiert.

### 2176 – Ressourcenzugriffe bestätigen getrennte Laufzeitbereiche, aber noch keine symbolischen Feldnamen

Die Zugriffe bei `1D9Ch–1E1Bh` verwenden den über `[3Ah]` erreichbaren Bereich mit WORD-Schrittweite und lesen daraus Verweise, über die anschließend separate Speicherblöcke angesprochen werden. Die Grenzen `[3Ch]` und `[3Eh]` teilen den Gesamtbereich weiterhin in Teilbereiche von `2R`, `4R` und `2R` Bytes. Die statische Analyse reicht noch nicht aus, diese drei Teilbereiche zuverlässig als Segment, Größe, Dateiposition oder Flags zu benennen. Diese Bedeutungen bleiben ausdrücklich unbestimmt.

### 2177 – Kleinste gefundene Anwendung im GEOWORKS.zip: FONT.GEO

Im Archiv ist `GEOWORKS/WORLD/FONT.GEO` mit 1.910 Bytes die kleinste gefundene GEODE vom Typ 1 (Anwendung). Der Header enthält `R=4`, `I=1`, `E=0`, Attributwort `0001h` und Protokollpaar `026Eh:0000h`. Der einzige Importname ist `ui`; sein 14-Byte-Datensatz enthält die WORD-Werte `4000h`, `02B5h` und `0000h` an den Positionen `+08h/+0Ah/+0Ch`. Das ist ein konkreter Minimalvergleich für eine Anwendung, nicht der Beweis, dass jede Anwendung genau diese Werte verwenden muss.

### 2178 – FONT.GEO hat vier Ressourceneinträge und keine Exporte

Die Ressourcentabelle von FONT.GEO beginnt bei Datei-Offset `012Eh` und endet bei `0156h`. Die vier Ressourcen haben (ID, Größe, Dateiposition, Relokationsbytes, Flags): `(0,0,0156h,0,0880h)`, `(1,224,0156h,36,0080h)`, `(2,448,025Ah,104,0A72h)` und `(3,752,0482h,4,145Ah)`. Die Anwendung besitzt keine Exporte. Die Daten zeigen, dass selbst die kleinste gefundene Anwendung mehr als einen trivialen leeren Ressourcenblock enthält; die Funktion der einzelnen Ressourcen wird hier nicht allein aus den Größen abgeleitet.

### 2179 – BOUNCE.GEO ist ein größeres Anwendungsbeispiel, aber kein Minimalgerüst

`GEOWORKS/WORLD/BOUNCE.GEO` ist Typ 1 mit `R=11`, `I=1`, `E=0` und einer Dateigröße von 3.572 Bytes. Der Importname ist ebenfalls `ui`. Gegenüber FONT.GEO enthält BOUNCE.GEO sieben zusätzliche Ressourcen und ist deshalb für einen ersten Minimalaufbau weniger geeignet. Es bleibt ein nützlicher Vergleich für eine bereits bekannte, kleine Anwendung.

### 2180 – Importfreie Bibliotheken und Treiber sind keine Ersatzvorlage für eine Anwendung

Im selben Archiv gibt es kleinere importfreie GEODEs anderer Typen, beispielsweise `SWAP.GEO` (Typ 2, 4 Ressourcen, 6 Exporte, 1.068 Bytes) und `STREAM.GEO` (Typ 3, 3 Ressourcen, 4 Exporte, 2.410 Bytes). Sie zeigen, dass der Kernel auch GEODEs ohne Imports verarbeitet; wegen ihres anderen GEODE-Typs und ihrer Exporttabellen sind sie jedoch keine direkte Vorlage für ein Typ-1-Anwendungsprogramm. Für einen ersten Anwendungstest ist FONT.GEO der passendere strukturelle Vergleich.

**Quellenbasis:** Deutscher Originalkernel `KERNEL.OLD`, Load-Image-Offsets `1B81h–1C16h`, `1D9Ch–1E1Bh`, `1EBCh–1F0Dh`, `2630h–26B3h` und `271Ch–2788h`; Originaldateien aus `GEOWORKS.zip` (`FONT.GEO`, `BOUNCE.GEO`, `SWAP.GEO`, `STREAM.GEO`). Alle Größen, Zähler, Tabellenpositionen und Bytes wurden direkt aus den Dateien gelesen. Analyse ausschließlich statisch; keine Laufzeitbestätigung.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, alle GEO-Dateien und `pcgeos1/geode.py`.



## Untersuchungen 2181–2187 – vorhandener SDK-Buildpfad und Zielarchiv-Abgleich

### 2181 – Das SDK besitzt bereits einen experimentellen GEODE-Buildpfad

Die aktuelle SDK-README beschreibt einen Buildpfad für PC/GEOS 1.x-Anwendungen. `pcgeos1/buildsys.py` kompiliert C-Quellen, assembliert die Runtime, linkt ein ELF-Zwischenergebnis, extrahiert Code-/Datenbereiche und übergibt diese an `package_from_skeleton()`. Ein vollständiger GEODE-Packer muss daher für einen ersten Versuch nicht neu erfunden werden. Der Pfad ist laut README ausdrücklich experimentell und nicht ABI-vollständig.

### 2182 – Der vorhandene Packer verwendet SPINTEXT.GEO als Anwendungsskelett

`pcgeos1/buildsys.py` lädt SPINTEXT.GEO und VIEWER.GEO. `pcgeos1/packer.py` übernimmt Ressourcen und Relokationsdaten aus SPINTEXT.GEO, ersetzt unter anderem Ressourcen 1 bis 4, ergänzt eine Engine-Ressource und baut die GEODE-Tabellen und Payload-Blöcke neu auf. Das ist ein konkreter, bereits implementierter Erzeugungsweg für eine Anwendung mit nativer UI; er ist nicht identisch mit einem neu konstruierten Minimal-GEODE aus dem Header allein.

### 2183 – Der Hello-Beispielprojektaufbau ist bereits vorhanden

Im Repository existieren `examples/hello/project.json` und `examples/hello/src/app.c`. Das Projekt definiert den Namen, den permanenten Namen, den 4-Byte-Token, Ausgabe-GEO, Protokoll, Viewport, Quelltext und Stackgröße. Der Beispielcode zeichnet einen Begrüßungstext und reagiert auf Klicks und Enter. Ein Projekt namens geoTest kann strukturell aus diesem Beispiel abgeleitet werden, indem Projektidentität und Ausgabe auf `geoTest.geo` angepasst werden.

### 2184 – Der dokumentierte Standard-Build erwartet einen genau identifizierten Zielbestand

`pcgeos1/target.py` verlangt standardmäßig vier bestimmte GEODE-Dateien und vergleicht ihre SHA-256-Werte mit fest hinterlegten Referenzwerten. Der README-/Kompatibilitätsstand nennt Kernelprotokoll `622.3` und UI-Protokoll `693.0`. Eine bloß passende Protokollnummer ersetzt die Hashprüfung nicht; sie belegt nicht, dass die verwendeten UI-Ressourcenlayouts identisch sind.

### 2185 – GEOWORKS.zip stimmt bei den geprüften UI-Vorlagen nicht mit dem SDK-Referenzsatz überein

Im vorliegenden `GEOWORKS.zip` existieren `GEOWORKS/WORLD/SPINTEXT.GEO`, `GEOWORKS/WORLD/PROGRAMM.E/SPINTEXT.GEO`, `GEOWORKS/WORLD/VIEWER.GEO`, `GEOWORKS/WORLD/NOTEPAD.GEO` und `GEOWORKS/WORLD/TERM.GEO`. Keine dieser geprüften Dateien hat den im SDK hinterlegten Referenzhash. Außerdem erwartet `target.py` SPINTEXT unter dem Archivpfad `/WORLD/EXTRAS/SPINTEXT.GEO`; dieser Pfad ist im vorliegenden Archiv nicht vorhanden. Die beiden SPINTEXT-Varianten besitzen zwar Kernelprotokoll `622.3` und importieren UI mit Protokoll `693.0`, aber daraus folgt keine bestätigte Binärkompatibilität ihrer Ressourcen mit den SDK-Referenzvorlagen.

### 2186 – Der Hash-Bypass ist ein Forschungsmodus, keine Kompatibilitätsbestätigung

Die Buildkonfiguration kann laut `buildsys.py` mit `allow_unknown_target` die strikte Hashprüfung abschalten. Das löst jedoch nicht automatisch die Pfadfrage und beweist nicht, dass die aus GEOWORKS.zip übernommenen UI-Objektressourcen mit den vom Packer erwarteten Objektlayouts übereinstimmen. Ein solcher Build wäre ein gezielter Versuch mit unbekanntem Zielprofil und müsste als experimentell gekennzeichnet und in einer Wegwerf-/Snapshot-Installation getestet werden.

### 2187 – Konkrete Voraussetzungen für geoTest.geo

Für den ersten Build sind jetzt vier Punkte erforderlich: (1) ein temporäres, korrekt strukturiertes Zielarchiv mit einer ausgewählten SPINTEXT.GEO-Variante an dem vom Loader erwarteten Pfad sowie VIEWER.GEO, NOTEPAD.GEO und TERM.GEO; (2) eine bewusste Entscheidung, ob der Hash-Bypass für diesen Forschungsbuild aktiviert wird; (3) ein verfügbarer GCC/binutils- oder LLVM/LLD-Toolchain gemäß SDK-Dokumentation; (4) anschließende Strukturprüfung mit `pcgeos1 inspect` und ein echter Starttest in einer gesicherten GeoWorks-1.2-Umgebung. Der originale GEOWORKS.zip-Bestand bleibt dabei unangetastet.

**Quellenbasis:** Repository `JMGeithain/pcgeos-1-sdk`, insbesondere `README.md`, `pcgeos1/buildsys.py`, `pcgeos1/packer.py`, `pcgeos1/target.py`, `examples/hello/project.json`, `examples/hello/src/app.c`, `docs/GETTING_STARTED.md` und `docs/TARGET_COMPATIBILITY.md`; außerdem direkte SHA-256-, Header- und Importprüfungen der genannten Dateien in `GEOWORKS.zip`. Analyse des Buildpfads anhand des Quellcodes; ein Build mit dem vorliegenden GEOWORKS.zip wurde in diesem Untersuchungsschritt nicht ausgeführt.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, alle GEO-Dateien im Originalarchiv und `pcgeos1/geode.py`.


### 2188 – Die beiden SPINTEXT.GEO-Varianten sind nicht bytegleich

Die Dateien `GEOWORKS/WORLD/SPINTEXT.GEO` (3.764 Bytes) und `GEOWORKS/WORLD/PROGRAMM.E/SPINTEXT.GEO` (3.748 Bytes) unterscheiden sich nicht nur im Archivpfad. Ein byteweiser Vergleich ergibt 1.335 unterschiedliche Bytepositionen innerhalb des gemeinsamen Längenbereichs; zusätzlich ist die Dateilänge um 16 Bytes verschieden. Daher darf eine der Varianten nicht allein aufgrund des gleichen Kernel- und UI-Protokolls als Ersatz für die SDK-Referenzvorlage ausgewählt werden. Vor einem Build muss geklärt werden, welche Variante die vom Packer erwarteten Objekt-/Ressourcenlayouts enthält.

**Quellenbasis:** Direkter Bytevergleich der beiden SPINTEXT.GEO-Dateien aus `GEOWORKS.zip`. Keine Änderung an den Originaldateien.


### 2189 – Die vom SDK tatsächlich übernommenen SPINTEXT-Ressourcen unterscheiden sich ebenfalls

Der Packer übernimmt aus SPINTEXT.GEO ausdrücklich Ressourcen 3 und 4 als UI-Bestandteile. In den beiden Archivvarianten ist Ressource 3 unterschiedlich groß (496 gegenüber 480 Bytes) und hat unterschiedliche SHA-256-Werte; Ressource 4 ist in beiden 336 Bytes groß, besitzt aber ebenfalls unterschiedliche SHA-256-Werte. Damit ist die Abweichung genau in den vom Packer verwendeten Ressourcen vorhanden. Die Auswahl einer Variante kann deshalb nicht als reine Pfadkorrektur behandelt werden.

**Quellenbasis:** Ressourcenverzeichnisse und Payload-Bytes der beiden SPINTEXT.GEO-Dateien aus `GEOWORKS.zip`; Packerzugriffe `resource_bytes(original,q,3)` und `resource_bytes(original,q,4)` in `pcgeos1/packer.py`. Keine Änderung an den Originaldateien.


## Untersuchungen 2190–2194 – Ressourcenvergleich und Build-Voraussetzungen

### 2190 – SPINTEXT-Ressourcen 1 und 2 sind zwischen den Archivvarianten identisch

Der Bytevergleich der Ressourcen aus `WORLD/SPINTEXT.GEO` und `WORLD/PROGRAMM.E/SPINTEXT.GEO` ergibt für Ressourcen 1 und 2 identische Inhalte (160 bzw. 592 Bytes) und identische Relokationsdaten. Die Abweichung beginnt bei Ressource 3. Damit ist die Differenz der beiden GEODEs nicht pauschal auf alle Ressourcen verteilt.

### 2191 – Die UI-Ressourcen 3 und 4 sind in beiden Varianten verschieden

Ressource 3 hat 496 Bytes in `WORLD/SPINTEXT.GEO` und 480 Bytes in `WORLD/PROGRAMM.E/SPINTEXT.GEO`; die SHA-256-Präfixe der Inhalte lauten `ee6af314cce86bdb` bzw. `a22b1c6cd61a46c8`. Ressource 4 hat in beiden Dateien 336 Bytes, aber unterschiedliche Inhalte (SHA-256-Präfixe `c5d151805a8e34a0` bzw. `0df160360cf91ef3`). Da `buildsys.py` diese beiden Ressourcen ausdrücklich an `build_basic_ui()` übergibt, betrifft die Abweichung direkt den UI-Template-Eingang des SDK-Builds.

### 2192 – Weitere Ressourcen sind ebenfalls nicht vollständig austauschbar

Außer Ressourcen 3 und 4 unterscheiden sich auch die Inhalte der Ressourcen 5, 7, 9 und 10. Ressourcen 6 und 8 sind bytegleich. Die beiden SPINTEXT-Dateien sind somit keine bloß unterschiedlich langen Container mit identischem Anwendungskern; mehrere weitere Ressourcen weichen voneinander ab. Eine pauschale Übernahme von Ressourcen zwischen den Varianten wäre nicht gerechtfertigt.

### 2193 – VIEWER, NOTEPAD und TERM im Archiv erfüllen die SDK-Hashbindung nicht

Die im GEOWORKS.zip gefundenen Dateien haben folgende SHA-256-Werte:
- `WORLD/VIEWER.GEO`: `c884b76cdc4f9119d4794f7830d5438e0abcc1d92d3cc248aa912bde85ed43e7`
- `WORLD/NOTEPAD.GEO`: `a1ebd0cb84712a126b1f67f5fd1ca6b57f8bda2e9038e9224ba16ebc008f9ea9`
- `DOCUMENT/NOTEPAD.GEO`: `3d0bbaf6640eecca7c884a3351ddd957435096af6ff0b6b02793fa9eb7286b29`
- `WORLD/TERM.GEO`: `a62ebc0fb3c01acb4b59c8172d20d520653822a6d42f0bec4831dfdb93e1cf3a`

Keiner dieser Werte stimmt mit den in `pcgeos1/target.py` hinterlegten Referenzhashes überein. Für NOTEPAD liegen zwei Archivvarianten vor, die ebenfalls unterschiedliche Hashes besitzen. Der Standard-Build kann das vorhandene Archiv daher nicht unverändert als bekanntes Zielprofil akzeptieren.

### 2194 – Host-Toolchain ist grundsätzlich vorhanden; der fehlende Baustein ist die Zielprofil-Kompatibilität

In der aktuellen Arbeitsumgebung sind GCC, GNU ld, nm und objcopy vorhanden. Damit ist die im SDK dokumentierte GNU-Toolchain grundsätzlich verfügbar. Für den Windows-LLVM-Pfad fehlt hier `llvm-nm`; dies ist für einen Linux-GCC-Build unerheblich. Der nächste Engpass ist nicht die Host-Toolchain, sondern die nicht bestätigte Kompatibilität der UI-Vorlagen und die abweichende Archivpfadstruktur.

**Konsequenz für geoTest.geo:** Noch keinen produktiven Build auslösen. Zuerst muss eine der folgenden Grundlagen hergestellt werden: (A) das exakt zum SDK-Referenzsatz passende Zielarchiv beschaffen/identifizieren oder (B) ein eigenes, ausdrücklich als experimentell markiertes Zielprofil aus dem vorliegenden GEOWORKS.zip rekonstruieren und die verwendeten UI-Ressourcen gegen die Originalanwendung prüfen. Der bloße Hash-Bypass ist kein Ersatz für diesen Kompatibilitätsnachweis.

**Quellenbasis:** Direkter Ressourcen- und Relokationsvergleich beider SPINTEXT.GEO-Dateien aus `GEOWORKS.zip`; SHA-256-Prüfung der im Archiv vorhandenen VIEWER.GEO-, NOTEPAD.GEO- und TERM.GEO-Varianten; Quellcode `pcgeos1/buildsys.py`, `pcgeos1/packer.py`, `pcgeos1/target.py`; Prüfung der verfügbaren Host-Programme mit der Systempfadsuche. Keine GEO-Datei und kein SDK-Quelltext wurde verändert.


## Untersuchungen 2195–2197 – Präzisierung der tatsächlich verwendeten UI-Chunks

### 2195 – Die sieben von build_basic_ui() verwendeten SPINTEXT-Chunks sind byteidentisch

Die beiden SPINTEXT-Varianten unterscheiden sich zwar in den Gesamtinhalten von Ressourcen 3 und 4, jedoch nicht in den vom SDK-UI-Generator tatsächlich ausgelesenen Chunks. Für Ressource 3 sind dies die Handles `0x24`, `0x26` und `0x3E`; für Ressource 4 die Handles `0x22`, `0x24`, `0x26` und `0x28`. Alle sieben Chunk-Payloads haben in beiden Varianten dieselbe Länge und denselben SHA-256-Wert. Die Chunk-Längen betragen in R3: 33, 8 und 71 Bytes; in R4: 198, 42, 8 und 22 Bytes. Damit ist die zuvor festgehaltene Schlussfolgerung aus Untersuchung 2191 zu präzisieren: Die Ressourcen als Ganzes unterscheiden sich, aber die konkret vom aktuellen UI-Generator verwendeten Objektvorlagen sind in diesen beiden Archivvarianten identisch.

### 2196 – Auch die Relokationsdaten der SPINTEXT-Ressourcen 3 und 4 stimmen überein

Ressource 3 und Ressource 4 enthalten in beiden SPINTEXT-Dateien jeweils genau einen 4-Byte-Relokationseintrag. Der Eintrag ist in allen vier Fällen identisch: `(info=0x23, extra=0x00, target=0x0000)`. Die Gleichheit der verwendeten Chunk-Payloads wird somit nicht durch abweichende Relokationstabellen relativiert. Dies belegt die Gleichheit dieser beiden Ressourcen im Hinblick auf die vom SDK gelesenen Chunks und die zugehörigen Ressourcenrelokationen; es beweist nicht die vollständige Binär- oder Laufzeitkompatibilität der gesamten SPINTEXT-GEODEs.

### 2197 – Die vom UI-Generator benötigten VIEWER-Chunks sind im Archiv vorhanden

Die vorhandene `WORLD/VIEWER.GEO` besitzt 37 Ressourcen. Die im SDK referenzierten Ressourcen 12 und 28 sind vorhanden. In Ressource 12 existieren die vom Generator verwendeten Chunk-Handles `0x22`, `0x32`, `0x36`, `0x3C`, `0x40`, `0x44` und `0x48`; in Ressource 28 existieren `0x56` und `0x5A`. Die beiden Ressourcen enthalten jeweils einen Relokationseintrag `(0x23,0x00,0x0000)`. Damit ist die strukturelle Voraussetzung „referenzierte Ressource und Chunk vorhanden“ für diese konkret verwendeten VIEWER-Vorlagen erfüllt. Die Übereinstimmung mit dem SDK-Referenzsatz und die Laufzeitkompatibilität sind damit weiterhin nicht bewiesen.

**Quellenbasis für 2195–2197:** Direkte Auswertung der GEODE-Ressourcentabellen, Chunk-Verweise und Relokationstabellen aus `GEOWORKS/WORLD/SPINTEXT.GEO`, `GEOWORKS/WORLD/PROGRAMM.E/SPINTEXT.GEO` und `GEOWORKS/WORLD/VIEWER.GEO` in `GEOWORKS.zip`; Quellcode `pcgeos1/ui.py` (Funktion `build_basic_ui`) und `pcgeos1/buildsys.py`. Die Originaldateien und SDK-Quellen blieben unverändert. Keine Laufzeitprüfung durchgeführt.


## Untersuchungen 2198–2200 – Schreibgrenzen der UI-Objektvorlagen

### 2198 – Alle neun von build_basic_ui() instanziierten Objektvorlagen bestehen den statischen Schreibgrenzencheck

Die Funktion `build_basic_ui()` erzeugt neun Objektinstanzen aus den folgenden Original-Chunks: SPINTEXT R3/`0x24` (Primary), SPINTEXT R3/`0x3E` (GenView), VIEWER R28/`0x56` (Help-Trigger), VIEWER R12/`0x22` (Help-Dialog), VIEWER R12/`0x32` (Help-Textobjekt), VIEWER R12/`0x3C` (Button-Leiste) sowie VIEWER R12/`0x44`, `0x48` und `0x40` (Page-Up, Page-Down und Close). Für jede Instanz wurden die von `obj()` und die anschließend explizit gesetzten WORD-Felder gegen die tatsächliche Chunk-Länge geprüft. Kein Schreibbereich überschreitet die jeweilige Chunk-Grenze.

| Objektvorlage | Chunk-Länge | Ende des letzten Schreibzugriffs (exklusiv) | verbleibende Bytes |
|---|---:|---:|---:|
| Primary | 33 | 26 | 7 |
| GenView | 71 | 58 | 13 |
| Help-Trigger | 34 | 34 | 0 |
| Help-Dialog | 29 | 26 | 3 |
| Help-Textobjekt | 50 | 48 | 2 |
| Button-Leiste | 29 | 26 | 3 |
| Page-Up | 34 | 34 | 0 |
| Page-Down | 34 | 34 | 0 |
| Close | 34 | 34 | 0 |

Die drei 34-Byte-Vorlagen für Trigger/Buttons werden bis einschließlich Byteoffset `0x21` beschrieben; der Schreibzugriff endet exakt bei Chunk-Länge 34. Das ist innerhalb der Grenzen, lässt aber keinen unbeschriebenen Nachlauf.

### 2199 – Gemeinsame Objektfelder und klassenspezifische Zusatzfelder sind getrennt erfasst

Der Hilfsbaustein `obj()` schreibt sieben WORD-Werte an den Offsets `0x0C`, `0x0E`, `0x10`, `0x12`, `0x14`, `0x16` und `0x18`. Danach verändert `build_basic_ui()` abhängig vom Objekt weitere Felder: beim Primary Offset `0x0E`; bei der GenView Offsets `0x2E`, `0x32`, `0x34`, `0x36` und `0x38`; beim Help-Trigger Offsets `0x16`, `0x1C`, `0x1E` und `0x20`; beim Help-Textobjekt Offsets `0x1C`, `0x1E`, `0x26`, `0x2C` und `0x2E`; bei den drei Buttons Offsets `0x1C`, `0x1E` und `0x20`. Die Feldbereiche sind in Untersuchung 2198 vollständig in die Längenprüfung eingegangen. Insbesondere wird beim Help-Trigger Offset `0x16` nach dem allgemeinen Objektaufbau nochmals überschrieben.

### 2200 – Schreibgrenzen beweisen keine semantische Richtigkeit der Feldbelegung

Die Prüfung belegt ausschließlich, dass die vom Python-Code geschriebenen WORD-Bereiche innerhalb der jeweiligen Original-Chunks liegen. Sie belegt nicht, dass alle Offsets die beabsichtigten PC/GEOS-1.x-Instanzfelder darstellen, dass die gesetzten Bitwerte für die deutsche GeoWorks-1.2-UI korrekt sind oder dass die erzeugten Objektbäume zur Laufzeit fehlerfrei geöffnet werden. Für einen semantischen Nachweis sind passende PC/GEOS-1.x-Klassendefinitionen bzw. ein Abgleich mit bekannten, funktionierenden 1.x-Objektressourcen erforderlich. Allgemeine oder spätere FreeGEOS-/PC/GEOS-2.x-Dokumentation wird hierfür ausdrücklich nicht als ABI-Beleg verwendet.

**Quellenbasis für 2198–2200:** Repository-Quelltext `pcgeos1/ui.py`, insbesondere `obj()` und `build_basic_ui()`; direkt extrahierte Chunk-Längen und Payloads aus `GEOWORKS/WORLD/SPINTEXT.GEO` und `GEOWORKS/WORLD/VIEWER.GEO` im vorliegenden `GEOWORKS.zip`; unabhängige Bounds-Prüfung aller neun Objektvorlagen. Statische Analyse; kein Laufzeittest und keine Änderung an Originaldateien.


### 2201 – LMem-Kopfwerte und Chunk-Kennbytes des SDK-Generators stimmen mit Originalressourcen überein

Die LMem-Kopfbereiche der vier untersuchten Originalressourcen (SPINTEXT R3/R4 und VIEWER R12/R28) besitzen an den Offsets `0x00`, `0x02`, `0x04`, `0x06` und `0x0A` dieselben Grundwerte, die `lmem()` in `pcgeos1/ui.py` setzt: Ressourcen-ID, `0x20`, `0xE000`, `2` und die jeweilige Anzahl der Chunk-Tabelleneinträge. Auch die in den Originalressourcen vorhandenen Kennbytes im Flag-Chunk umfassen genau die Werte `0x00`, `0x02`, `0x03` und `0x07`; der Generator verwendet für seinen ersten Flag-Eintrag `0x00`, für Daten-Chunks `0x02`, für Objekt-Chunks `0x03` und für die als ignore-dirty markierten Objekte `0x07`. Die Werte und ihre Verwendung sind damit durch reale PC/GEOS-1.x-Dateien belegt. Aus diesem Vergleich allein wird keine weitergehende Bitfeld-Semantik abgeleitet. Die variierenden Kopfwerte an anderen Offsets (`0x08`, `0x14`) wurden nicht als identisch vorausgesetzt und bleiben gesondert zu untersuchen.

**Quellenbasis:** Direkte Auswertung der ersten 32 Bytes und des Flag-Chunks der Ressourcen 3 und 4 aus `GEOWORKS/WORLD/SPINTEXT.GEO` sowie der Ressourcen 12 und 28 aus `GEOWORKS/WORLD/VIEWER.GEO`; Vergleich mit `lmem()` in `pcgeos1/ui.py`. Statische Analyse; keine Änderung an Originaldateien.


### 2202 – Die LMem-Kopffelder bei Offsets 0x08 und 0x14 bleiben ein offener Kompatibilitätspunkt

Die vier Originalressourcen zeigen für die WORD-Felder bei Offset `0x08` und `0x14` unterschiedliche Werte:

| Originalressource | Ressourcengröße | WORD bei 0x08 | WORD bei 0x14 |
|---|---:|---:|---:|
| SPINTEXT R3 | 496 | `0x01EC` | `0x01E0` |
| SPINTEXT R4 | 336 | `0x014C` | `0x0150` |
| VIEWER R12 | 5.792 | `0x1698` | `0x1440` |
| VIEWER R28 | 704 | `0x02C0` | `0x02C0` |

Der Generator `lmem()` setzt Offset `0x08` auf die aktuelle Länge des erzeugten Blocks vor der abschließenden 16-Byte-Ausrichtung und Offset `0x14` auf die Länge nach dieser Ausrichtung. Diese Berechnung ist im Quelltext eindeutig. Die vier Originalwerte lassen sich damit jedoch nicht ohne Kenntnis der Feldsemantik als Bestätigung dieser Berechnung verwenden. Insbesondere ist bei SPINTEXT R3 der Wert bei `0x14` kleiner als das Ende des letzten ermittelten Chunks; bei VIEWER R12 weicht er deutlich vom Wert bei `0x08` ab. Die Bedeutung der beiden Felder ist daher aus den vorliegenden Vergleichen nicht sicher bestimmt.

**Konsequenz:** Die bisherigen positiven Befunde zu den LMem-Grundfeldern und Flag-Bytes bestätigen nicht den vollständigen LMem-Header. Vor einem Build mit Laufzeitanspruch müssen die Felder `0x08` und `0x14` anhand des PC/GEOS-1.x-Kernels oder zusätzlicher sicher identifizierter Originalressourcen untersucht werden. Bis dahin bleibt die LMem-Konstruktion experimentell.

**Quellenbasis:** Direkt gelesene LMem-Kopfbereiche und Chunk-Endpositionen aus `GEOWORKS/WORLD/SPINTEXT.GEO` (R3/R4) und `GEOWORKS/WORLD/VIEWER.GEO` (R12/R28); Quelltext `pcgeos1/ui.py`, Funktion `lmem()`. Keine Laufzeitannahme und keine Änderung an Originaldateien.


## Untersuchungen 2203–2204 – Historische LMem-Dokumentation und Grenzen der Header-Zuordnung

### 2203 – Ein zeitgenössisches PC/GEOS-Dokument bestätigt LMem, aber nicht den GeoWorks-1.2-Header

Das Dokument „PC/GEOS System Software Overview“, datiert auf den 10. November 1990, beschreibt den Local Memory Manager als Kernelbestandteil und nennt die Routinen LMemInitHeap, LMemAlloc, LMemReAlloc und LMemFree. Es erklärt außerdem, dass der LMem-Heap innerhalb eines Speicherblocks angelegt wird und UI-Objekte LMem intensiv verwenden. Die Abbildung auf Seite 39 bezeichnet den dargestellten LMem-Blockheader jedoch als 16 Bytes. Die hier untersuchten GeoWorks-1.2-Ressourcen besitzen einen 32-Byte-Kopfbereich mit weiteren Feldern. Das frühe Dokument ist daher ein zeitgenössischer Beleg für das Konzept und die API-Familie, aber kein hinreichender Feldplan für die konkrete 1.2-Struktur. Insbesondere können daraus die Bedeutungen der WORD-Felder bei 0x08 und 0x14 nicht abgeleitet werden.

### 2204 – Die Rohdaten bestätigen die Werte, aber nicht deren Semantik

Die vier Originalressourcen wurden erneut direkt aus dem GEOWORKS.zip gelesen. Ihre ersten 32 Bytes bestätigen die in Untersuchung 2202 dokumentierten Werte. Der WORD-Wert bei 0x08 beträgt bei den Beispielen Ressourcengröße minus 4 (SPINTEXT R3/R4 und VIEWER R12), während VIEWER R28 an dieser Stelle Ressourcengröße minus 8 enthält. Der WORD-Wert bei 0x14 variiert unabhängig davon: 0x01E0, 0x0150, 0x1440 und 0x02C0. Diese Beobachtung zeigt, dass eine einfache Gleichsetzung beider Felder mit derselben Blocklänge nicht durch alle Beispiele gedeckt ist. Sie beweist jedoch keine alternative Feldbedeutung. Eine Zuordnung als Heap-Ende, freie-Liste-Zeiger, freie Bytezahl oder Ähnliches wäre ohne Kernelzugriff oder eine passende 1.x-Strukturdefinition spekulativ und wird deshalb nicht vorgenommen.

**Weiterer Prüfpfad:** Die Felder müssen durch gezielte Rückverfolgung der LMem-Initialisierungs- und Validierungsroutinen im Originalkernel KERNEL.OLD oder durch eine eindeutig zur GeoWorks-1.2-Version gehörende Strukturdefinition identifiziert werden. Das vorliegende zeitgenössische 1990-Dokument ist dafür nur Hintergrundquelle. Bis zum Nachweis bleiben ui.py:lmem() und insbesondere seine Werte an 0x08 und 0x14 experimentell.

**Quellenbasis:** GEOWORKS/KERNEL.OLD aus dem bereitgestellten GEOWORKS.zip (72.688 Bytes); rohe Headerbytes der Ressourcen SPINTEXT R3/R4 und VIEWER R12/R28 aus demselben Archiv; pcgeos1/ui.py, Funktion lmem(); PC/GEOS System Software Overview, Draft vom 10. November 1990, Seiten 38–40 (insbesondere Seite 39). Die Quelle von 1990 wird ausdrücklich nicht als vollständige Spezifikation des 1.2-Headers verwendet. Keine Änderungen an Originaldateien oder SDK-Quelltexten; keine Laufzeitprüfung.


## Untersuchung 2205 – Erste statische Suche nach LMem-Headerzugriffen im Originalkernel

Der deutsche Originalkernel `GEOWORKS/KERNEL.OLD` wurde erneut aus dem bereitgestellten Archiv extrahiert. Die MZ-Datei ist 72.688 Bytes groß; der DOS-MZ-Header umfasst 0x600 Bytes. Für eine erste Orientierung wurde das nachfolgende Load-Image als 16-Bit-x86-Code linear disassembliert. Diese lineare Disassemblierung ist ausdrücklich nur eine Suchhilfe: Sie unterscheidet Code und eingebettete Daten nicht zuverlässig und ist kein vollständiger Kontrollfluss-Disassembler.

Bei der Suche nach direkten speicherbezogenen Operanden mit Displacement `0x14` ergaben sich nur wenige Treffer mit Basisregistern. Der Treffer bei Load-Image-Offset `0x8C29` verwendet `ES:[BX+DI+0x14]` innerhalb eines Bereichs, der zuvor Tabellenwerte aus einem über `ES` adressierten Objekt liest und anschließend eine Dispatch-/Callback-Entscheidung trifft. Der Treffer bei `0x98E1` schreibt `CX` nach `[DI+0x14]` innerhalb einer Routine, die unmittelbar zuvor einen 0x20-WORD-Kopierblock initialisiert und mehrere Kontextfelder setzt. Keiner dieser Treffer kann anhand des linearen Disassemblats belastbar als Zugriff auf den LMem-Header der UI-Ressourcen identifiziert werden. Die übrigen gefundenen Vorkommen von `0x14` sind überwiegend Stack-Frame-Zugriffe, absolute Kernelvariablen oder unmittelbare Konstanten.

Damit ist derzeit weder die Bedeutung des LMem-WORD-Feldes bei `0x14` noch die des Feldes bei `0x08` aus dem Kernelcode bewiesen. Insbesondere wird aus dem bloßen Auftreten eines Displacements nicht geschlossen, dass der jeweilige Zeiger auf einen LMem-Block zeigt. Der nächste notwendige Schritt ist die Identifikation der zuständigen Kernel-API-/Dispatch-Einstiegspunkte und die Rückverfolgung ihrer Aufrufpfade, statt weitere Displacement-Treffer ohne Kontext zu sammeln.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD` aus `GEOWORKS.zip`; MZ-Headerauswertung und 16-Bit-x86-Disassemblierung des Load-Images; Vergleich der Trefferumgebung an `0x8C0C–0x8C45` und `0x9892–0x9967`. Die lineare Disassemblierung wird nicht als vollständige Code-/Daten-Trennung gewertet. Keine Änderung an Kernel, Originaldateien oder SDK-Quelltexten; kein Laufzeittest.



## Untersuchung 2206 – Originales UI.GEO und Abgleich der SDK-LMem-Konstruktion

### 2206.1 – GEODE-Metadaten der deutschen GeoWorks-1.2-UI

Die Datei `GEOWORKS/SYSTEM/UI.GEO` wurde direkt aus dem bereitgestellten Archiv gelesen. Sie ist 87.900 Bytes groß und besitzt die GEODE-1.x-Signatur `C7 45 CF 53`. Der vorhandene SDK-Parser liest daraus 28 Ressourcen, 2 importierte Bibliotheken und 262 Exporte. Die beiden Importnamen lauten `im` und `dbase`; beide Importdatensätze enthalten die Protokoll-WORDs 601 und 0. Die UI.GEO-Metadaten liefern damit einen konkreten 1.x-Systembestand zum weiteren Vergleich, aber keine symbolischen Namen der Kernelroutinen.

Die Relokationstabellen enthalten in mehreren Ressourcen Einträge der vom SDK als Kernel-Relokationen behandelten Quellklasse 0. Beispiele: R2 enthält 120, R3 114, R4 23 und R12 18 solcher Einträge. R2 enthält daneben 93 Bibliotheksrelokationen (8 gegen Importindex 0 und 85 gegen Importindex 1). Diese Zahlen sind reine Zählungen der 4-Byte-Relokationseinträge nach dem vorhandenen Parser; sie identifizieren weder LMem-Funktionen noch deren Parameter oder Einsprungadressen. Die in den Relokationsfeldern gespeicherten WORD-Werte sind ohne Auflösung des Kernel-Dispatch-/Relokationsverfahrens keine Funktionsnamen.

### 2206.2 – Direkter Abgleich der von ui.py erzeugten LMem-Struktur

Die Funktion `pcgeos1/ui.py:lmem()` erzeugt zunächst 32 Byte Kopfbereich, legt ab Offset 0x20 eine WORD-Handle-Tabelle an und fügt die Chunkdaten anschließend hinzu. Der Chunk für Handle 0x20 enthält eine Byte-Tabelle mit einem Eintrag pro Handle. Das lässt sich direkt an SPINTEXT R3 aus beiden Archivvarianten prüfen: Der über Handle 0x20 adressierte Chunk hat in beiden Fällen 16 Bytes Nutzdaten und lautet:

```
00 02 03 02 03 02 07 02 02 07 02 07 02 03 02 07
```

Damit ist die konkrete Chunk-Anordnung der SDK-Funktion in diesem Teil mit dem Originalbestand vereinbar. Das ist jedoch keine Bestätigung der Bedeutung der einzelnen Flagwerte 0x02, 0x03 und 0x07.

Die vier ersten WORD-Felder der geprüften SPINTEXT-Ressourcen beginnen jeweils mit Ressourcen-ID, 0x0020, 0xE000 und 0x0002. Auch die Handleanzahl bei Offset 0x0A stimmt für SPINTEXT R3 (16) und R4 (6) mit der Zahl der WORD-Einträge ab Offset 0x20 überein. Diese beobachteten Werte entsprechen den entsprechenden Konstanten und der Handle-Tabellenkonstruktion in `lmem()`.

Die Felder bei Offset 0x08 und 0x14 bleiben dagegen ungeklärt. Ein wichtiger Kontrollbefund: SPINTEXT R4 hat 336 Bytes Ressourcendaten, den Wert 0x014C bei Offset 0x08 und 0x0150 bei Offset 0x14. Das passt zahlenmäßig zur SDK-Strategie „Länge vor Ausrichtung“ (332 Bytes) und „Länge nach 16-Byte-Ausrichtung“ (336 Bytes). SPINTEXT R3 aus `WORLD/PROGRAMM.E` hat 480 Bytes und bei beiden Offsets 0x01E0. Die andere SPINTEXT-R3-Datei unter `WORLD` ist 496 Bytes groß, enthält bei Offset 0x08 den Wert 0x01EC und bei Offset 0x14 den Wert 0x01E0; das Ende des zuletzt ermittelten Chunks liegt bei 0x01EC. Diese Abweichung zeigt, dass die beiden Headerfelder nicht pauschal als „vorherige und nachfolgende Gesamtlänge“ erklärt werden dürfen. Sie könnte mit Unterschieden in der konkreten Blockbelegung oder zusätzlichen Bytes zusammenhängen; die Ursache ist mit dem derzeitigen Befund nicht bewiesen.

### 2206.3 – Konsequenz für den ersten Testbuild

Der Originalvergleich stützt die Grundform der vom SDK verwendeten LMem-Handle-Tabelle und die konkreten ersten Headerwerte. Er bestätigt nicht den vollständigen 32-Byte-Header, nicht die Semantik der Flagwerte und insbesondere nicht die Berechnung der Felder 0x08 und 0x14 für beliebige neu erzeugte Ressourcen. Die Kernel-Relokationszählung in UI.GEO ist ein neuer Suchansatz, aber noch keine Identifikation der LMem-API.

**Arbeitsentscheidung:** Noch keinen `geoTest.geo`-Build mit Laufzeitanspruch freigeben. Als nächstes sind die Relokationsziele und Aufrufstellen der UI.GEO-Ressourcen mit den Kernel-Dispatch-Einstiegspunkten abzugleichen. Dabei muss zuerst geklärt werden, wie die Quellklasse-0-Relokationen vom GeoWorks-1.2-Loader aufgelöst werden. Erst danach kann eine gefundene Routine als LMem-Initialisierung, -Allokation oder -Freigabe klassifiziert werden.

**Quellenbasis:** `GEOWORKS/SYSTEM/UI.GEO`, `GEOWORKS/WORLD/SPINTEXT.GEO`, `GEOWORKS/WORLD/PROGRAMM.E/SPINTEXT.GEO` aus dem bereitgestellten `GEOWORKS.zip`; `pcgeos1/geode.py`, `pcgeos1/ui.py` und `pcgeos1/packer.py` im Repository. Ausschließlich statische Auswertung; keine Änderung an Originaldateien oder SDK-Quelltexten; kein Laufzeittest.


## Untersuchung 2207 – Importauflösung und erste Zuordnung von Kernel-Relokationsstellen

### 2207.1 – Der Kernel liest 14-Byte-Importdatensätze und löst sie einzeln auf

Im Originalkernel `KERNEL.OLD` ist der Bereich ab Load-Image-Offset `0x2652` erneut im Kontrollfluss verfolgt worden. Die Routine berechnet zunächst `0x0E * Importanzahl`, liest diesen zusammenhängenden Bereich in einen temporären Speicherbereich und durchläuft anschließend die Datensätze in Schritten von 14 Bytes. Für jeden Datensatz lädt sie die WORD-Felder bei +0x08, +0x0A und +0x0C in CX, AX und BX; DX erhält den Geode-Kontext aus `DS:0000`. Danach erfolgt der Aufruf `0x271C`. Bei Erfolg wird der zurückgegebene AX-Wert in die fortlaufende WORD-Tabelle geschrieben; der Datensatzzeiger wird um 0x0E und der Zieltabelleintrag um 2 erhöht.

Die Routine bei `0x271C` übernimmt die weitere Auflösung. Sie verwendet unter anderem die acht Zeichen des Bibliotheksnamens, sucht bzw. lädt die passende Bibliothek und prüft anschließend die angeforderten Protokoll-/Versionswerte. Der Kontrollfluss enthält Fehlerpfade, die den Aufruf mit gesetztem Carry abbrechen. Damit ist die bereits im GEODE-Parser angenommene Datensatzbreite von 14 Bytes durch den Originalkernel-Kontrollfluss bestätigt. Ebenso ist belegt, dass die Bibliotheksimporte vor ihrer Nutzung in eine kompakte WORD-Tabelle aufgelöst werden.

**Grenze:** Dieser Befund erklärt den Importpfad der Bibliotheksrelokationen, aber noch nicht die Quellklasse-0-Kernelrelokationen. Die Routine bei `0x271C` darf nicht als LMem-Funktion missverstanden werden; sie ist Teil der Bibliotheksauflösung.

### 2207.2 – Ein UI.GEO-Kernelrelokationseintrag liegt auf dem Operanden eines FAR-CALL

In UI.GEO, Ressource R2, liegt ein Quellklasse-0-/Typ-0-Relokationseintrag bei Ressourcenoffset `0x0005`. Der dort gespeicherte WORD-Wert ist `0x01E9`. Die Bytes unmittelbar davor und danach lauten:

```
BF 40 00 50 9A E9 01 00 00
```

Das ist syntaktisch ein 16-Bit-FAR-CALL (`9A`) mit dem codierten Offset `0x01E9` und dem Segmentwort `0x0000`. Im Kernel-Load-Image befindet sich bei Offset `0x01E9` tatsächlich eine Instruktion. Dieser Befund zeigt eine konkrete Verbindung zwischen einer UI.GEO-Relokationsstelle und einem Kernelcode-Offset. Er beweist noch nicht, wie der Loader den Segmentanteil behandelt, ob der codierte Offset unverändert bleibt oder welche symbolische API-Funktion an dieser Stelle beginnt.

Eine weitere Beobachtung in UI.GEO R16: Bei Offset `0x0016` steht eine FAR-JMP-Instruktion mit den beiden WORDs `0x00A9` und `0x00A9`. Auf diesen beiden WORD-Positionen liegen Quellklasse-0-Relokationen der Typen 1 und 2. Das ist ein Hinweis darauf, dass verschiedene Relokationstypen innerhalb eines FAR-Pointers auftreten. Ihre genaue Semantik wird ohne die entsprechende Relokationsroutine nicht festgelegt.

### 2207.3 – Nächster Prüfpunkt

Die Importauflösung ist nun vom Kernelcode her belegt. Für die eigentliche LMem-Frage muss als nächstes die Routine identifiziert werden, die die Relokationstypen der Quellklasse 0 verarbeitet und die bei UI.GEO gefundenen FAR-CALL-/FAR-JMP-Operanden korrigiert. Erst wenn dieser Pfad geklärt ist, kann man die Kernel-Offsets aus UI.GEO systematisch als API-Einstiegspunkte katalogisieren und nach LMem-Aufrufen suchen.

**Quellenbasis:** Originaldatei `GEOWORKS/KERNEL.OLD` aus `GEOWORKS.zip`, Load-Image-Disassemblierung und Kontrollflussbereiche `0x2652–0x27D6` sowie `0x01E9`; Originaldatei `GEOWORKS/SYSTEM/UI.GEO`, Ressourcen R2 und R16 einschließlich ihrer Relokationstabellen. Die Disassemblierung ist statisch; symbolische API-Namen und die genaue Semantik der Relokationstypen 1/2 sind weiterhin unbestimmt. Keine Änderung an Originaldateien oder SDK-Quelltexten; kein Laufzeittest.


## Untersuchung 2208 – Kernel-Relokationsdispatcher im Originalkernel identifiziert

### 2208.1 – Aufrufpfad und Eintragsformat

Die Verarbeitung der Ressourcenrelokationen ist im deutschen Originalkernel auf Load-Image-Offset `0x20FE` bis `0x2150` nachvollzogen. Die Routine ermittelt anhand der Ressourcentabelle den Relokationsbereich (Offset `DS:003E`), liest zuerst die Anzahl der Relokationseinträge und lädt die Einträge anschließend in temporären Blöcken von höchstens `0x100` Bytes. Die Schleife ab `0x2135` verarbeitet jeden Eintrag mit vier Bytes: WORD bei `[BP+SI]` in AX und WORD bei `[BP+SI+2]` in BX; danach Aufruf der Dispatcher-Routine bei `0x2153`. SI wird pro Eintrag um vier erhöht.

Damit sind für diesen Kernel die vier Byte pro Relokationseintrag und die Zerlegung in ein Informationswort sowie ein Ziel-Offset durch den ausführenden Code bestätigt. Die im SDK verwendete Parserstruktur `<BBH>` ist die Byte-für-Byte-Sicht auf dasselbe 4-Byte-Format.

### 2208.2 – Aufteilung des Informationsbytes in Quelle und Typ

Die Dispatcher-Routine bei `0x2153` übernimmt das Informationswort in AX. Der Kontrollfluss maskiert DL mit `0xF0` und AL mit `0x0F`. Damit werden das obere Nibble des ersten Bytes als Quellenkennung und das untere Nibble als Relokationstyp getrennt ausgewertet. Die drei im SDK unterstützten Quellen sind im Kernelpfad unterscheidbar:

- Quelle `0x00`: Kernelpfad. Der Dispatcher verwendet CS und eine kernelinterne Tabelle.
- Quelle `0x10`: Bibliothekspfad. Der Dispatcher nimmt den Index aus dem aufgelösten Importbereich ab `DS:0036`.
- Quelle `0x20`: Ressourcenpfad des aktuellen Geode. Der Dispatcher greift auf die Ressourcentabelle ab `DS:003A` zu.

Damit ist die Zuordnung der im SDK verwendeten Quellenwerte 0, 1 und 2 zum Kernel-, Bibliotheks- und eigenen Ressourcenpfad durch den 1.x-Kernelcode gestützt. Dies ist eine wichtige Bestätigung für die Zerlegung `source = info >> 4` und `type = info & 0x0F` in `pcgeos1/geode.py`.

### 2208.3 – Typzweige und Grenzen der Benennung

Der Dispatcher enthält getrennte Zweige für die Typwerte 0, 1, 2 und 3. Die Typen 0, 1 und 2 führen zu unterschiedlichen Schreiboperationen am Relokationsziel; Typ 3 verzweigt in einen Sonderpfad bei `0x2205`, der unter anderem einen zusätzlichen Kernel-/Geode-Kontext berücksichtigt. Der Code enthält außerdem einen Pfad, der einen Aufrufstub im Zielbereich erzeugt bzw. verändert (Instruktionen ab `0x21E6` bis `0x21FA`). Aus diesem Grund werden die Typen hier zunächst nur anhand ihrer beobachteten Verarbeitungszweige katalogisiert. Die symbolischen Bezeichnungen aus späteren GEOS-Dokumentationen werden nicht ungeprüft auf GeoWorks 1.2 übertragen.

### 2208.4 – Konkrete Probe aus UI.GEO

UI.GEO, Ressource R2, enthält einen Relokationseintrag mit Informationsbyte `0x00`, Quellenkennung 0 und Typ 0, Zieloffset `0x0005`. An dieser Stelle liegen die Bytes:

```
50 9A E9 01 00 00 72 03
```

Der Operand ab Offset 0x0005 ist damit ein FAR-CALL mit codiertem Offset `0x01E9` und Segmentwort `0x0000`. Der Kernel-Load-Image-Offset `0x01E9` enthält ausführbaren Code. Die Probe ist daher ein konkretes Beispiel für einen Kernelquellen-Relokationseintrag, der einen FAR-CALL-Operand bearbeitet. Sie weist dem Ziel bei 0x01E9 noch keinen symbolischen API-Namen zu.

UI.GEO R16 enthält am Zieloffset `0x0016` einen Relokationseintrag mit Info `0x01` (Quelle 0, Typ 1) und bei `0x0018` einen mit Info `0x02` (Quelle 0, Typ 2). Diese beiden Einträge liegen in einem Bereich mit FAR-JMP-Opcode `EA`; sie sind zusätzliche reale Proben für zwei getrennte Typzweige. Die exakte Bedeutung der beiden Typen bleibt bis zur vollständigen Nachverfolgung der jeweiligen Schreiboperationen offen.

### 2208.5 – Konsequenz und nächster Schritt

Die zentrale offene Frage aus Untersuchung 2207 ist nun eingegrenzt: Der Relokationsdispatcher ist gefunden, und die drei Quellenpfade sind im Kernel sichtbar. Als nächstes werden die Zieloperationen für die Typen 0–3 einzeln anhand von Originalrelokationen aus UI.GEO und weiteren 1.x-GEODEs verglichen. Danach können Kernel-Offsets, die durch Quelle 0 aufgelöst werden, als Kandidaten für API-Einstiegspunkte katalogisiert und ihre Aufrufpfade auf LMem-Operationen untersucht werden.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD` aus `GEOWORKS.zip`, Load-Image-Offsets `0x20FE–0x2217`; `GEOWORKS/SYSTEM/UI.GEO`, Ressourcen R2 und R16 sowie ihre originalen Relokationstabellen; `pcgeos1/geode.py`. Statische Analyse des Originalcodes, kein Laufzeittest. Keine Änderung an Kernel, Originaldateien oder SDK-Quelltexten.


## Untersuchung 2209 – Typ-3-Relokation durch zweite Originalanwendung belegt

### 2209.1 – UI.GEO allein deckt nicht alle Dispatcherzweige ab

Die Typen 0, 1 und 2 konnten anhand konkreter Relokationseinträge in UI.GEO R2 und R16 untersucht werden. In den beiden geprüften UI-Ressourcen wurde kein Typ-3-Eintrag als Probe verwendet. Die Existenz des Typ-3-Zweigs im Kernel war damit zwar sichtbar, aber noch nicht durch eine passende Probe aus dem installierten Originalbestand belegt.

### 2209.2 – Probe aus NPLAYGCM.GEO

In `GEOWORKS/NPLAYGCM.GEO`, Ressource R3, wurde ein Relokationseintrag mit Informationsbyte `0x03` gefunden: Quellenkennung 0, Typ 3, Zusatzbyte `0x0A`, Zieloffset `0x0000`. Die Ressource hat eine deklarierte Größe von `0x17C0` Bytes; der Zieloffset liegt damit innerhalb der Ressource. Die Bytes am Ziel beginnen:

```
50 53 51 52 56 1E 06 BF
```

Dies ist eine reale Typ-3-Probe aus einem zweiten PC/GEOS-1.x-GEODE im bereitgestellten Archiv. Sie bestätigt, dass der Kernelzweig für Quelle 0 / Typ 3 nicht nur ungenutzter Code ist. Die Probe erlaubt jedoch noch keine vollständige symbolische Benennung des Typs. Die Zusatzinformation `0x0A` und die genaue Wirkung des Zweigs `0x2205` müssen über weitere gleichartige Relokationen und den dortigen Zielcode untersucht werden.

### 2209.3 – Arbeitsfolge

Die nächste Analyse vergleicht die NPLAYGCM-Ressource mit dem Typ-3-Dispatcherpfad `0x21C6–0x2217`, insbesondere dem Sonderpfad `0x2205`, und verfolgt die Hilfsroutine `0x724B`. Parallel werden Typ-4- und höhere Typwerte nicht pauschal interpretiert: Sie werden erst dann in die unterstützte SDK-Formatmenge aufgenommen, wenn ihre Behandlung im 1.x-Kernel und anhand gültiger Originalproben einzeln bestätigt ist.

**Quellenbasis:** `GEOWORKS/NPLAYGCM.GEO`, Ressource R3 und deren Relokationstabelle; `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x21C6–0x2217` und `0x724B`. Statische Auswertung. Keine Änderung an Originaldateien oder SDK-Quelltexten; kein Laufzeittest.


## Untersuchung 2210 – Hilfsroutine 0x724B im Typ-3-Pfad

Die in Untersuchung 2209 offene Hilfsroutine `0x724B` wurde weiter verfolgt. Sie übernimmt den Segmentwert in CX, setzt DS auf dieses Segment und liest den WORD-Wert am Blockanfang (`DS:0000`) als Handle-/Blockbezug. Anschließend ruft sie `0x701B` auf. Auf dem Rückweg folgt `0x7014`.

Die beiden Hilfsfunktionen lassen sich im Kernel weiter auflösen: `0x701B` verzweigt zur gemeinsamen Speicherverwaltungsroutine `0x971D`; diese aktualisiert unter gesperrten Interrupts einen Zähler im Handleeintrag bei `[BX+4]` und aktualisiert bei Bedarf den zugehörigen Verwaltungszustand. `0x7014` verzweigt zu `0x9754`; diese Routine vermindert denselben Zähler und führt beim Übergang in den freizugebenden Zustand die entsprechende Freigabe-/Bereinigungsroutine aus. Das ist ein Lock-/Unlock- bzw. Referenzzählpfad des allgemeinen Kernel-Speichermanagers.

Innerhalb von `0x724B` werden außerdem Segment- und Handlebezüge gegen mehrere Kernel-Verwaltungsbereiche verglichen. Bei einem Treffer wird der gefundene Verwaltungsbezug in CX zurückgegeben; der Sperrzustand wird vor der Rückkehr wieder aufgehoben. Das passt zum Aufruf aus dem Typ-3-Dispatcher: Der Relokationscode prüft bzw. normalisiert einen Segment-/Blockbezug über den allgemeinen Speichermanager, statt unmittelbar einen LMem-Chunk zu bearbeiten.

**Wichtige Abgrenzung:** `0x724B`, `0x701B` und `0x7014` sind damit als allgemeiner Speicherverwaltungs-/Handlepfad eingegrenzt. Sie sind keine nachgewiesenen LMem-Initialisierungs- oder Chunk-Allocator-Funktionen. Der Typ-3-Relokationszweig allein liefert folglich noch keinen Beleg für die Felder 0x08 oder 0x14 des LMem-Headers.

**Nächster Schritt:** Den Dispatcherzweig für Typ 0 und die von ihm gelesene Kernel-Tabelle weiter zurückverfolgen. Dort liegen die direkten Kernelverweise, die für die API-Kandidatenliste relevant sind. Anschließend gezielt nach Funktionen suchen, die LMem-Blockkopf und Handle-Tabelle initialisieren, statt allgemeine Speicherhandle-Locks mit LMem zu verwechseln.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x724B–0x72B3`, `0x7014–0x701F` und `0x971D–0x9775`; Aufruf aus dem Relokationsdispatcher `0x21FC–0x2205`. Statische Analyse. Keine Änderung an Originaldateien oder SDK-Quelltexten; kein Laufzeittest.


## Untersuchung 2211 – Kernel-Exporttabelle und Auflösung von Quelle 0 / Typ 0

### 2211.1 – Der Zeiger bei 2151h ist ein DOS-relokierter Segmentzeiger

Die Bytes des Originalkernels bei Load-Image-Offset `0x2151` lauten `EC 0D`, also WORD `0x0DEC`. In der DOS-MZ-Relocationstabelle von `KERNEL.OLD` existiert ein Eintrag für Offset `0x2151`, Segmentziel `0x0000`. Der MZ-Lader addiert deshalb das tatsächliche Lade-Segment zum WORD an dieser Stelle. Der Dispatcher lädt diesen korrigierten Wert mit `mov ds, cs:[0x2151]` nach DS.

Damit zeigt DS zur Laufzeit auf das Segment `Ladesegment + 0x0DEC`. Der dazugehörige Tabelleninhalt liegt im MZ-Load-Image ab linearem Offset `0x0DEC0`. Es handelt sich nicht um Code bei Load-Image-Offset `0x0DEC`, sondern um eine WORD-Tabelle im gesonderten Segmentbereich. Die Unterscheidung ist durch den MZ-Fixup bei `0x2151` belegt.

### 2211.2 – Indexierung und Auflösung im Typ-0-Zweig

Der Quellklasse-0-Zweig des Dispatchers führt folgende Operationen aus:

1. `DI = ES:[BX]`: Der bisher im Relokationsziel gespeicherte WORD-Wert wird als Tabellenindex übernommen.
2. `DI <<= 1`: Der WORD-Index wird in einen Byteoffset für die WORD-Tabelle umgerechnet.
3. `DS = CS:[0x2151]`: DS wird auf das durch den MZ-Fixup korrigierte Tabellensegment gesetzt.
4. Im gemeinsamen Pfad wird `DI = DS:[DI]` gelesen; das ist der aufgelöste Kernel-Codeoffset.
5. Für Typ 0 schreibt der Dispatcher `SI` (zuvor mit CS geladen) nach `ES:[BX+2]` und danach den aufgelösten Offset nach `ES:[BX]`.

Damit ist für Quelle 0 / Typ 0 die konkrete Wirkung nachgewiesen: Ein im GEODE-Operand gespeicherter Kernel-Tabellenindex wird in einen FAR-Pointer `CS:Offset` aufgelöst. Die Tabelle enthält WORD-Codeoffsets; sie ist keine Tabelle von symbolischen Funktionsnamen.

### 2211.3 – Konkreter Abgleich mit UI.GEO R2

Der in Untersuchung 2207/2208 dokumentierte UI.GEO-Eintrag in R2 liegt bei Zieloffset `0x0005`. Dort steht vor der Relokation ein FAR-CALL-Operand mit Offset `0x01E9` und Segment `0x0000`:

```
50 9A E9 01 00 00
```

Der Tabellenindex ist somit `0x01E9` (dezimal 489). Der zugehörige WORD-Eintrag befindet sich bei Tabellenoffset `0x0DEC0 + 2 * 0x01E9 = 0x0E292`; sein Wert ist `0x8027`. Im Kernel-Load-Image liegt bei `0x8027` tatsächlich Code:

```
8027  53             push bx
8028  56             push si
8029  57             push di
802A  06             push es
802B  26 8B 5D 02    mov bx, es:[di+2]
802F  83 FB 01       cmp bx, 1
8032  74 0D          je 8041
```

Nach der Typ-0-Auflösung wird der Operand daher zum FAR-Pointer `CS:8027` (wobei CS das zur Laufzeit geladene Kernel-Code-Segment ist). Der Eintrag ist damit ein belastbarer End-to-End-Beleg vom ursprünglichen UI.GEO-Tabellenindex bis zum konkreten Kernel-Codeoffset.

### 2211.4 – Grenzen der Aussage

Die Tabelle und die Auflösung von Quelle 0 / Typ 0 sind nun statisch nachgewiesen. Der symbolische API-Name der Routine bei `0x8027` ist damit noch nicht bekannt. Der dortige Code arbeitet unter anderem mit `ES:[DI+2]`, `ES:[DI]` und weiteren über Register übergebenen Werten; daraus allein folgt weder „LMem“ noch eine bestimmte Speicher-API.

Ebenso ist diese Untersuchung keine vollständige Erklärung der Typen 1–3 oder der Quellklassen 1 und 2. Die Typ-0-Erkenntnis wird nicht auf andere Zweige übertragen.

### 2211.5 – Nächste Schritte

Als nächstes werden weitere Quelle-0-/Typ-0-Relokationen aus UI.GEO und unabhängigen Original-1.x-GEODEs katalogisiert. Für jeden eindeutigen Tabellenindex wird der aufgelöste Kernel-Codeoffset ermittelt. Danach werden die tatsächlichen Aufrufstellen und Funktionskörper dieser Kandidaten untersucht, um LMem-Initialisierung, Chunk-Allokation und Handleverwaltung anhand von Datenfluss und Speicherzugriffen voneinander zu trennen.

**Quellenbasis:** Deutscher Originalkernel `GEOWORKS/KERNEL.OLD`, MZ-Header und MZ-Relocationstabelle (Fixup für Load-Image-Offset `0x2151`), Load-Image-Offsets `0x2153–0x21DA`, Tabellenbereich ab `0x0DEC0` und Code bei `0x8027`; Originaldatei `GEOWORKS/SYSTEM/UI.GEO`, Ressource R2, Relokationsziel `0x0005`. Statische Analyse; kein Laufzeittest.

**Unverändert:** `KERNEL.OLD`, `KERNEL.EXE`, alle GEO-Dateien, `pcgeos1/geode.py` und alle SDK-Quelltexte.


## Untersuchung 2212 – Quelle-0-/Typ-0-Verweise in UI.GEO inventarisiert

### 2212.1 – Vollständige Auswertung der 28 UI-Ressourcen

Die 28 Ressourcen von `GEOWORKS/SYSTEM/UI.GEO` wurden anhand der Ressourcentabelle und der jeweils 16-Byte-ausgerichteten Relocation-Streams erneut durchlaufen. Berücksichtigt wurden ausschließlich Einträge mit `source=0` und `type=0`. Es ergeben sich 1.125 solche Relokationseinträge. Das Zusatzbyte `extra` ist bei allen 1.125 Einträgen `0x00`.

Die 1.125 Einträge verwenden 188 verschiedene WORD-Indizes. Der kleinste beobachtete Index ist 0, der größte 572. Für jeden dieser Indizes wurde der WORD-Wert aus der Kernel-Tabelle ab Load-Image-Offset `0x0DEC0` gelesen. Alle 188 resultierenden Offsets liegen innerhalb des 71.152 Byte großen Kernel-Load-Images.

### 2212.2 – Häufigste Indizes und aufgelöste Codeoffsets

| Kernel-Tabellenindex | Vorkommen in UI.GEO | Tabellenwert / Kernel-Codeoffset |
|---:|---:|---:|
| `0x1E6` (486) | 121 | `0x8000` |
| `0x0A9` (169) | 116 | `0x2AD3` |
| `0x006` | 60 | `0x6FE8` |
| `0x1E9` (489) | 31 | `0x8027` |
| `0x1EB` (491) | 30 | `0x8216` |
| `0x095` (149) | 30 | `0x2015` |
| `0x005` | 26 | `0x6FDF` |
| `0x186` (390) | 23 | `0xA505` |
| `0x187` (391) | 22 | `0xA551` |
| `0x208` (520) | 22 | `0x83CE` |

Die Vorkommenszahlen beziehen sich auf die 1.125 Quelle-0-/Typ-0-Einträge in UI.GEO. Sie sind keine Häufigkeiten über das gesamte GEOWORKS-Archiv.

### 2212.3 – Erste Codeproben

Die beiden häufigsten Tabellenindizes werden auf folgende Stellen abgebildet:

- Index `0x1E6` → Kerneloffset `0x8000`; dort beginnt die Bytefolge `53 56 57 06 8B 3C` (unter anderem `push bx`, `push si`, `push di`, `push es`).
- Index `0x1E9` → Kerneloffset `0x8027`; dort beginnt die in Untersuchung 2211 gezeigte Bytefolge `53 56 57 06 26 8B`.

Diese beiden Ziele liegen im selben zusammenhängenden Kernelcodebereich. Das ist ein sinnvoller Schwerpunkt für die nächste Kontrollfluss- und Aufrufkonventionsanalyse. Die Nähe der Offsets und die Häufigkeit der Aufrufe reichen jedoch nicht aus, um eine gemeinsame API-Familie oder LMem-Zugehörigkeit zu behaupten.

### 2212.4 – Aussagegrenzen

Die Inventur bestätigt für UI.GEO die wiederholte Nutzung der Kernel-Tabelle durch Quelle 0 / Typ 0. Sie liefert eine priorisierte Liste von 188 Kernel-Codeoffsets. Nicht jeder Offset wurde bereits als eigenständiger Funktionsanfang disassembliert; die lineare Disassemblierung kann überlappende Einsprungpunkte und eingebettete Daten falsch darstellen. Daher sind die Tabellenwerte zunächst als aufgelöste Relokationsziele zu behandeln, nicht pauschal als vollständig klassifizierte API-Funktionen.

### 2212.5 – Nächster Schritt

Die Untersuchung konzentriert sich zunächst auf die stark verwendeten Ziele `0x8000`, `0x8027` und die benachbarten Tabellenziele `0x8216`. Dazu werden Aufrufkonvention, Registereingaben, Segmentannahmen, Rückgabewerte und die tatsächlichen Schreibzugriffe auf die adressierten Strukturen verfolgt. Parallel werden die betroffenen UI.GEO-Aufrufstellen und weitere Original-1.x-GEODEs verglichen. Erst diese Datenflussanalyse kann entscheiden, ob eine Funktion LMem, Objektblöcke oder einen anderen Kernel-Verwaltungsbereich bearbeitet.

**Quellenbasis:** `GEOWORKS/SYSTEM/UI.GEO` aus dem bereitgestellten `GEOWORKS.zip`, alle 28 Ressourcentabellen und Relocation-Streams; `GEOWORKS/KERNEL.OLD`, MZ-korrigierter Kernel-Tabellenbereich ab `0x0DEC0` und die aufgelösten Kernel-Offsets. Statische Byteanalyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2213 – Häufiger UI.GEO-Verweis auf den allgemeinen Handle-Lock-Pfad

### 2213.1 – Tabellenindex 491 führt zu Kerneloffset 8216h

Aus der in Untersuchung 2212 erstellten UI.GEO-Inventur ergibt sich für Tabellenindex `0x1EB` (491) eine Häufigkeit von 30 Relokationseinträgen. Der Kernel-Tabellenwert für diesen Index ist `0x8216`. Dort beginnt:

```asm
8216  1E             push ds
8217  E8 16 14       call 9630
821A  E8 87 ED       call 6FA4
821D  72 02          jb 8221
821F  1F             pop ds
8220  CB             retf
8221  E8 FB 03       call 861F
8224  1F             pop ds
8225  CB             retf
```

Der Exportpfad sichert DS, ruft zunächst den Segment-/Datenkontext-Helfer bei `0x9630` und anschließend die Speicherverwaltungsroutine bei `0x6FA4` auf. Bei gesetztem Carry folgt ein zusätzlicher Fehler-/Nachladepfad bei `0x861F`.

### 2213.2 – Die Routine 6FA4h prüft einen Speicherhandle und erhöht den Lock-Zähler

Die Routine `0x6FA4` sichert DS und setzt DS auf das Kernel-Datensegment `0x0E35`. Sie prüft BX auf 16-Byte-Ausrichtung und auf den zulässigen Bereich zwischen `0x15B0` und dem in `DS:0x0E4C` gespeicherten Grenzwert. Anschließend sperrt sie kurz die Interrupts und liest den WORD-Wert bei `DS:[BX]`.

- Ist dieser WORD-Wert ungleich null, erhöht sie das BYTE-Feld bei `DS:[BX+0x0B]` und kehrt zurück.
- Ist der WORD-Wert null, ruft sie `0x7306` auf und versucht danach denselben Prüfpfad erneut.

Damit ist die Funktion von `0x6FA4` als allgemeiner Speicherhandle-Lock-/Residentmachungspfad eingegrenzt: Ein Handleeintrag wird geprüft, sein Lock-Zähler wird erhöht oder ein noch nicht residenter Block wird über den Ladepfad angefordert.

### 2213.3 – Abgrenzung zur LMem-Frage

Der UI.GEO-Tabellenindex 491 verweist somit auf einen Kernelpfad, der den allgemeinen Speicherhandle verwaltet. Die beobachteten Felder `[BX]` und `[BX+0x0B]` gehören in diesem Kontrollfluss zu einem Kernel-Handleeintrag. Sie sind nicht die zuvor gesuchten LMem-Headerfelder bei `0x08` oder `0x14`.

Dieser Befund ist wichtig, weil ein häufig verwendeter Kernelaufruf mit Speicherbezug nicht automatisch eine LMem-Operation ist. Die genaue symbolische API-Bezeichnung von `0x8216` bleibt offen; sie wird nicht aus dem Verhalten allein geraten.

### 2213.4 – Nächster Schritt

Die Ziele `0x8000` und `0x8027` bleiben die nächsten Kandidaten für eine getrennte Kontrollflussanalyse. Dabei wird insbesondere geprüft, ob die dort verwendeten Strukturen mit den allgemeinen Handleeinträgen aus `0x6FA4` zusammenhängen oder eine andere Ebene (z. B. Objekt-/Ressourcenreferenzen) darstellen. Eine LMem-Zuordnung erfolgt nur bei einem nachweisbaren Zugriff auf den LMem-Blockkopf oder die Chunk-Handle-Tabelle.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Kerneloffsets `0x8216–0x8225`, `0x9630–0x9635`, `0x6FA4–0x6FD1` und `0x7306`; UI.GEO-Quelle-0-/Typ-0-Relokationen mit Tabellenindex `0x1EB`. Statische Analyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2214 – Direkter LMem-Nachweis über die Chunk-Flag-Tabelle

### 2214.1 – Kernelroutine 8329h liest ein Chunk-Flagbyte

Im Originalkernel liegt bei Load-Image-Offset `0x8329` folgender Code:

```asm
8329  56             push si
832A  8B 36 02 00    mov si,WORD PTR ds:0x2
832E  2B C6          sub ax,si
8330  D1 E8          shr ax,1
8332  8B 34          mov si,WORD PTR [si]
8334  03 F0          add si,ax
8336  8A 04          mov al,BYTE PTR [si]
8338  32 E4          xor ah,ah
833A  5E             pop si
833B  CB             retf
```

Der Code liest zunächst den WORD-Wert bei `DS:0002`, zieht ihn vom übergebenen AX ab und halbiert die Differenz. Anschließend liest er den ersten WORD-Eintrag der dadurch adressierten Tabelle und verwendet diesen als Basis für einen Bytezugriff. Das gelesene Byte wird in AL zurückgegeben.

### 2214.2 – Kernelroutine 833Ch ändert ein Chunk-Flagbyte

Direkt anschließend liegt bei `0x833C`:

```asm
833C  50             push ax
833D  56             push si
833E  8B 36 02 00    mov si,WORD PTR ds:0x2
8342  2B C6          sub ax,si
8344  D1 E8          shr ax,1
8346  8B 34          mov si,WORD PTR [si]
8348  03 F0          add si,ax
834A  8A 04          mov al,BYTE PTR [si]
834C  8A E7          mov ah,bh
834E  F6 D4          not ah
8350  22 C4          and al,ah
8352  0A C3          or al,bl
8354  88 04          mov BYTE PTR [si],al
8356  E8 03 00       call 0x835C
```

Die Änderung entspricht exakt der Bitoperation:

```text
neues_flag = (altes_flag AND NOT BH) OR BL
```

Danach folgt eine weitere Routine bei `0x835C`, die abhängig von bestimmten Bits des resultierenden Flagbytes Zusatzbehandlung ausführt. Ihre vollständige Semantik ist noch offen.

### 2214.3 – Abgleich mit SPINTEXT.GEO, Ressource R3

Die Originaldatei `GEOWORKS/WORLD/SPINTEXT.GEO` wurde direkt aus dem bereitgestellten Archiv gelesen. Für Ressource R3 gelten:

| Feld | Wert |
|---|---:|
| Ressourcengröße | `0x01F0` |
| LMem-Kopf: WORD bei Offset `0x02` | `0x0020` |
| erster Handle-Tabelleneintrag bei Offset `0x20` | `0x0042` |
| Flagbyte-Tabelle ab Offset | `0x0042` |

Die 16 Bytes ab Offset `0x42` lauten:

```
00 02 03 02 03 02 07 02
02 07 02 07 02 03 02 07
```

Diese Bytes stimmen exakt mit dem bereits zuvor isolierten 16-Byte-Chunk für Handle `0x20` überein.

Die Indexberechnung der Kernelroutine passt dazu: Bei `DS:0002 = 0x20` und einem Handlewert `AX = 0x20` ergibt sich Index 0. Der erste WORD-Eintrag an `DS:0x20` liefert `0x42`; die Routine liest damit das Flagbyte an `DS:0x42`. Für nachfolgende Handlewerte wird der Index in WORD-Schritten erhöht, während die Flagwerte byteweise gelesen werden.

### 2214.4 – Bedeutung für den LMem-Aufbau

Damit ist anhand des deutschen GeoWorks-1.2-Originalbestands direkt belegt:

1. Das WORD-Feld bei LMem-Blockoffset `0x02` wird vom Kernel als Offset der Handle-Tabelle verwendet.
2. Der erste WORD-Eintrag dieser Tabelle verweist in der geprüften Ressource auf die Byte-Flagtabelle.
3. Die Kernelroutinen `0x8329` und `0x833C` lesen beziehungsweise ändern die zu einem Handle gehörende Flag-Information.
4. Die vom SDK bereits verwendete Anordnung mit Handle-Tabelle ab Offset `0x20` und dem Flag-Chunk ist mit diesem Originalbeispiel vereinbar.

**Nicht bewiesen** sind damit die vollständige Bedeutung des 32-Byte-Kopfs, die Bedeutung der Felder bei `0x08` und `0x14`, die Semantik aller Flagbits oder die symbolischen API-Namen der beiden Kernelroutinen. Auch die Funktionen bei `0x8000` und `0x8027` werden dadurch nicht automatisch als LMem-Funktionen klassifiziert.

### 2214.5 – Häufigkeit der beiden Kernelziele in UI.GEO

Die Kernel-Tabelle ordnet Index `0x1F2` (498) dem Codeoffset `0x8329` und Index `0x1F3` (499) dem Codeoffset `0x833C` zu. In den Quelle-0-/Typ-0-Relokationen der 28 UI.GEO-Ressourcen wurden drei Verweise auf Index 498 und 13 Verweise auf Index 499 gezählt. Die beiden Funktionen sind damit auch im realen System-GEODE referenziert.

### 2214.6 – Nächste Schritte

1. Die Zusatzroutine `0x835C` und ihre Bedingungen vollständig verfolgen.
2. Weitere originale 1.x-LMem-Ressourcen auf dieselbe Kopf-/Handle-/Flagtabellenstruktur prüfen.
3. Die übrigen Kernelroutinen untersuchen, die Handlewerte in derselben Weise in die Tabelle auflösen.
4. Erst nach der getrennten Analyse die offenen Kopffelder `0x08` und `0x14` untersuchen.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x8329–0x835C) und Kernel-Tabelle ab `0x0DEC0`; `GEOWORKS/WORLD/SPINTEXT.GEO`, Ressource R3, Bytes bei `0x0000–0x0051); `GEOWORKS/SYSTEM/UI.GEO`, Quelle-0-/Typ-0-Relokationen. Ausschließlich statische Analyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2215 – Zusatzbehandlung der LMem-Chunk-Flags

### 2215.1 – Bedingungspfad bei 835Ch

Die von der Flag-Änderungsroutine `0x833C` aufgerufene Routine `0x835C` wurde vollständig bis zu ihrem Rücksprung verfolgt. Sie prüft das resultierende Flagbyte in AL:

- Ist Bit `0x04` gesetzt, endet die Zusatzbehandlung sofort.
- Ist Bit `0x04` nicht gesetzt, aber Bit `0x08` ebenfalls nicht gesetzt, endet sie ebenfalls sofort.
- Nur wenn Bit `0x04` aus und Bit `0x08` an ist, wird zusätzlich Byte `DS:0005` auf Bit `0x01` geprüft.
- Ist auch dieses Bit gesetzt, wird über den bei `DS:0000` referenzierten Kernel-Handleeintrag die BYTE-Information bei `[SI+0x0A]` geprüft.
- Wenn dort Bit `0x20` gesetzt ist, wird die Routine `0xA567` aufgerufen.

### 2215.2 – Wirkung von A567h

Die Routine `0xA567` sichert BX und ES, übergibt BP in BX und ruft `0x9636` auf. Danach löscht sie Bit `0x20` im BYTE-Feld `ES:[BX+0x0A]` und ruft `0xAE4C` auf.

Damit ist die Zusatzwirkung präzise beschrieben: Unter den oben genannten Bedingungen wird ein Bit im zugehörigen Kernel-Handleeintrag gelöscht und eine weitere Kernelroutine ausgeführt. Die symbolische Bedeutung des Bits `0x20` und der Folgeroutine `0xAE4C` ist in dieser Untersuchung noch nicht abschließend benannt.

### 2215.3 – Aufrufstellen der Flag-API

Die statische Suche nach direkten Aufrufen der beiden Flagroutinen ergibt unter anderem:

- `0x8FDB` ruft `0x8329` auf und prüft anschließend Bit `0x02` des zurückgegebenen Flagbytes. Bei gesetztem Bit wird über `0x833C` Bit `0x08` gesetzt.
- `0x87A1` ruft `0x833C` mit `BX=0x0008` auf, setzt also Bit `0x08`, nachdem zuvor ein WORD-Block kopiert wurde.
- `0x9328` und `0x9336` rufen ebenfalls `0x833C` mit `BX=0x0008` auf.
- `0x8FF8` und `0x8FFD` sind kurze Weiterleitungen zu den Flag-Lese- und Flag-Änderungsroutinen.

Die Aufrufstellen belegen, dass Bit `0x08` in mehreren Kernelpfaden gezielt gesetzt wird. Seine offizielle symbolische Bedeutung bleibt offen; insbesondere wird es nicht ohne Beleg als „dirty“, „locked“ oder „discardable“ bezeichnet.

### 2215.4 – Konsequenz für die LMem-Rekonstruktion

Die Chunk-Flagtabelle ist nicht nur ein statisches Bytearray im Original-GEODE: Der Kernel liest und verändert ihre Einträge über dedizierte Routinen. Damit ist ein weiterer Teil der LMem-Verwaltung konkret nachvollzogen. Die Strukturbeobachtung aus SPINTEXT R3 ist durch die tatsächlichen Kernelzugriffe bestätigt.

Die Felder `0x08` und `0x14` des LMem-Kopfes werden von diesem Pfad nicht erklärt. Auch die Funktionen `0x8000` und `0x8027` bleiben getrennte Untersuchungskandidaten; ihre Codepfade werden nicht allein aufgrund der Nähe zu den LMem-Flagroutinen als LMem-Funktionen klassifiziert.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x833C–0x8384`, `0xA567–0xA578`, `0x87A1`, `0x8FDB–0x9001` und `0x9323–0x933F). Statische Kontrollfluss- und Datenflussanalyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2216 – Aufrufkontexte der Kernelziele 8000h und 8027h

### 2216.1 – Kernelziel 8000h: drei direkte Kernel-Aufrufstellen

Die lineare Disassemblierung enthält drei direkte CALL-Stellen auf `0x8000`:

- `0x829D`: Aufruf aus `0x828E), nachdem AX auf `0x0012` gesetzt und CX/BX aus `ES:[DI+4]` geladen wurde. Nach der Rückkehr wird über `DS:SI` ein Tabellen-/Eintragsbezug berechnet und ein DWORD an diesem Ziel aktualisiert.
- `0x9271`: Aufruf aus `0x926A), wenn BX dem WORD-Wert `DS:0000` entspricht. Der umgebende Code `0x9248–0x927D` liest einen Eintrag aus einer über SI/BX adressierten Tabelle und prüft Segment-/Offsetwerte.
- `0x9529`: kurzer Wrapper `0x9527–0x952D), der AX sichert, `0x8000` aufruft und AX anschließend wiederherstellt. Weitere Wrapper bei `0x952E–0x9553` rufen diesen Pfad auf.

Der Einstieg `0x8000` sichert BX, SI, DI und ES, lädt DI aus `[SI]` und geht in den gemeinsamen Pfad bei `0x8051`. Dort wird ein FAR-Zeiger aus `[DI]` nach ES:DI geladen. Anschließend wird über `0x8078` ein Datensatz geprüft. Danach wird über `0x9630` das Kernel-Datensegment gesetzt und DS aus dem zuvor gesicherten Wert bei `DS:0000` wiederhergestellt.

### 2216.2 – Gemeinsame Prüfung bei 8078h

Die Routine `0x8078` beginnt mit:

```asm
8078  26 F7 45 04 E1 FF    test WORD PTR es:[di+4],0xFFE1
807E  75 F2                jne 0x8072
```

Bei gesetzten Bits der Maske `0xFFE1` wird der Pfad bei `0x8072` ausgeführt. Dieser ruft `0x039C` auf und setzt danach AX auf `0x000A`. Der genaue symbolische Zweck dieser Prüfung und des Aufrufs bei `0x039C` ist noch nicht geklärt.

### 2216.3 – Kernelziel 8027h: Descriptor-Verarbeitung

Der Einstieg `0x8027` verwendet ES:DI als Zeiger auf einen Verwaltungsdatensatz:

- `ES:[DI+2]` wird als WORD nach BX geladen.
- Bei BX ungleich 1 wird der DWORD-Zeiger bei `ES:[DI]` geladen und ES auf BX gesetzt.
- Bei BX gleich 1 wird zusätzlich `ES:[DI+4]` gelesen. Über SI und eine weitere Tabelle wird ein Eintrag berechnet.
- Ist dessen erster WORD-Wert null, wird `0x828E` aufgerufen.
- Andernfalls wird der DWORD-Zeiger aus diesem Eintrag nach ES:DI geladen.
- Der gemeinsame Abschluss führt über `0x8078` und `0x9630` zurück.

Die Routine `0x828E` sichert mehrere Register, setzt AX auf `0x0012`, liest CX aus `ES:[DI+4]` und ruft `0x8000` auf. Danach berechnet sie über `DS:SI` und BX einen Tabelleneintrag und schreibt CX:DX als DWORD an diesen Eintrag. Damit hängen die Pfade `0x8027` und `0x8000` über die Descriptor-/Tabellenverwaltung zusammen.

### 2216.4 – UI.GEO-Referenzen

In UI.GEO wurden 31 Quelle-0-/Typ-0-Relokationen mit Kernel-Tabellenindex `0x1E9` (Ziel `0x8027`) und 121 entsprechende Relokationen mit Index `0x1E6` (Ziel `0x8000`) gezählt. Die Referenzen auf `0x8027` liegen in den Ressourcen R2, R5, R7, R8, R9, R10, R12, R14, R16 und R19. Die Referenzen auf `0x8000` verteilen sich auf mehrere UI-Ressourcen, unter anderem R2, R5, R7, R8, R10, R11, R14, R16, R19, R21, R22 und R23.

Die FAR-CALL-Operanden der 8027-Referenzen werden im GEODE vor der Relokation als Tabellenindex `0x01E9` gespeichert. Der Kernel-Dispatcher ersetzt diesen Index zur Laufzeit durch den Codeoffset `0x8027` und das Kernel-Code-Segment.

### 2216.5 – Abgrenzung zur LMem-Verwaltung

Die untersuchten Pfade bearbeiten indirekte FAR-Zeiger, Verwaltungsdatensätze und Tabellen. Die Felder `ES:[DI+2]`, `ES:[DI+4]`, `ES:[DI+10]` und `ES:[DI+11]` gehören in diesen Routinen zu dem über ES:DI adressierten Datensatz. Es gibt in diesem Pfad bisher keinen belegten Zugriff auf die LMem-Chunk-Flagtabelle, die bei Untersuchung 2214 über `DS:0002` und den ersten Handletabelleneintrag aufgelöst wurde.

Daher werden `0x8000` und `0x8027` vorläufig als Funktionen der allgemeinen Descriptor-/Ressourcen-/Handleverwaltung geführt. Eine symbolische API-Benennung und die vollständige Bedeutung der Descriptorfelder bleiben offen. Eine endgültige Aussage, dass diese Funktionen keinerlei LMem-Bezug haben, wäre auf Grundlage dieser Teilanalyse ebenfalls zu weitgehend.

### 2216.6 – Nächster Schritt

Als nächstes wird der Descriptor-Aufbau anhand mehrerer realer Aufrufstellen und der zugehörigen Ressourcen-/Handletabellenwerte rekonstruiert. Besonders relevant sind die Übergänge `0x8027 → 0x828E → 0x8000` und die Prüfung bei `0x8078`. Parallel werden weitere unabhängige Aufrufstellen der LMem-Flagroutinen `0x8329` und `0x833C` verfolgt, um deren Eingabekonvention und Handlebereich zu bestätigen.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x8000–0x808F), `0x828E–0x82B2), `0x9248–0x927D), `0x9527–0x9553), `0x9630–0x9636); `GEOWORKS/SYSTEM/UI.GEO`, Quelle-0-/Typ-0-Relokationen und Ressourcen R2, R5, R7, R8, R9, R10, R12, R14, R16, R19, R21, R22 und R23. Statische Analyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2217 – Reale UI.GEO-Aufrufkontexte für den Descriptorpfad 8027h

### 2217.1 – UI.GEO übergibt unterschiedliche Descriptoradressen und AX-Modi

Die Aufrufstellen der Kernel-Tabelle `0x1E9 → 0x8027` wurden in den Originalressourcen disassembliert. Beispiele:

- UI.GEO R2, Offset `0x0000`: `mov di,0x0040`, danach `push ax` und FAR CALL auf den Kernelindex `0x01E9`.
- UI.GEO R7, Offset `0x01B4`: `push dx; mov di,0x0040`; FAR CALL auf `0x01E9); danach wird das Carry-Flag geprüft.
- UI.GEO R7, Offset `0x021F`: `mov ax,0x2091; mov di,0x0040`; FAR CALL auf `0x01E9`.
- UI.GEO R8, Offset `0x0719`: `mov di,0x0543`; FAR CALL auf `0x01E9`; unmittelbar danach folgt `mov al,0x08; xor cx,cx` und ein weiterer FAR CALL.
- UI.GEO R8, Offset `0x0767`: `mov dx,ds:0; mov bp,si; mov di,0x0543; mov ax,0x0005`; FAR CALL auf `0x01E9`; danach ein weiterer Kernel-FAR-CALL auf Tabellenindex `0x0200`.

Diese Beispiele belegen, dass AX und DI vor dem Aufruf bewusst vorbereitet werden. Die DI-Werte sind keine einheitlichen LMem-Chunk-Handles: Es treten unter anderem `0x0040`, `0x0265`, `0x0543`, `0x071F`, `0x0743` und weitere Werte auf. Ohne den zugehörigen Descriptorbereich und die Segmentbelegung dürfen sie nicht als LMem-Handles interpretiert werden.

### 2217.2 – AX beeinflusst den Descriptor-/Ressourcenpfad

Im Kernelcode ab `0x8080` wird AX in BX kopiert, dreimal rotiert und mit 7 maskiert. Der daraus gewonnene Wert dient als Index in eine Byte-Tabelle bei `CS:0x8177` (Wertefolge `01 02 04 08 10 20 40 80`). Das resultierende Bit wird gegen `ES:[BP+0x11]` geprüft.

Damit ist belegt, dass AX bei diesem Pfad eine Auswahl eines einzelnen Bits aus einer Descriptor-Flagmaske steuert. Welche öffentliche API-Konstante beziehungsweise welcher symbolische Modus hinter den konkreten AX-Werten steht, ist noch nicht geklärt.

### 2217.3 – Ressourcenzustand und Nachladepfad

Der weitere Kontrollfluss untersucht die Descriptorfelder bei Offsets `+0x10` und `+0x11`, folgt bei Bedarf FAR-Zeigern über `ES:[BP]` und prüft einen weiteren Tabellen-/Datenbereich. Wenn ein erforderlicher Eintrag fehlt, wird `0x82B3` aufgerufen. Dieser Pfad arbeitet mit Descriptorfeldern `+0x04` und `+0x08`, ruft `0x8226` sowie `0x8021` auf und kehrt mit gesetztem Carry zurück.

Das Verhalten passt zu einer allgemeinen Ressourcen-/Descriptorverwaltung mit Zustandsprüfung und Nachlade-/Initialisierungspfaden. Eine eindeutige symbolische Benennung wird daraus noch nicht abgeleitet.

### 2217.4 – Konsequenz für die LMem-Suche

Die realen UI-Aufrufstellen bestätigen, dass `0x8027` einen Descriptorpfad mit Modus-/Bit-Auswahl und Ressourcenstatus bearbeitet. Sie liefern weiterhin keinen direkten Zugriff auf die LMem-Chunk-Flagtabelle oder auf die 32-Byte-LMem-Kopfstruktur. Deshalb bleibt `0x8027` als allgemeine Ressourcen-/Descriptorfunktion klassifiziert, nicht als nachgewiesene LMem-Funktion.

Die Funktionen `0x8329` und `0x833C` bleiben dagegen direkte LMem-Kandidaten, weil ihre Tabellenindizierung anhand von SPINTEXT R3 bytegenau auf die Chunk-Flagtabelle passt.

**Quellenbasis:** `GEOWORKS/SYSTEM/UI.GEO`, Originalressourcen R2, R7 und R8, Aufrufstellen bei `0x0000`, `0x01B4`, `0x021F`, `0x0719` und `0x0767`; `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x8027–0x8176`, `0x8226–0x82D3`. Statische Analyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2218 – Direkte LMem-Blockverwaltung im Kernel (7903h–7E93h)

### 2218.1 – LMem-Blockinitialisierung

Der Kernelcode `0x78B2–0x796E` legt einen neuen LMem-Block an und initialisiert dessen Kopfstruktur. Der Blocksegmentwert wird nach DS/ES geladen; danach erfolgen direkte Schreibzugriffe auf die Kopfstruktur:

```asm
7903  mov WORD PTR ds:0x0000,bx
7907  mov WORD PTR ds:0x0002,dx
790C  mov WORD PTR ds:0x0008,ax
790F  mov WORD PTR ds:0x000A,cx
...
7933  mov WORD PTR ds:0x0004,ax
7937  mov WORD PTR ds:0x0006,ax
...
7947  mov WORD PTR ds:0x0004,0x8800
794F  mov WORD PTR ds:0x0012,ax
7952  mov WORD PTR ds:0x0010,ax
7955  mov WORD PTR ds:0x0014,ax
```

Die genaue Zuordnung der Registerwerte folgt aus dem Kontrollfluss: DX wird zuvor aus der berechneten Strukturgröße/Tabellenposition abgeleitet; CX wird aus den Handle-/Tabellenparametern aufgebaut; AX enthält die berechnete Blockgröße. Der Pfad mit `AX==2` initialisiert zusätzlich die Felder `0x10`, `0x12` und `0x14` auf null.

### 2218.2 – Feld 0002h: Handle-Tabellenoffset bestätigt

Mehrere unabhängige Routinen lesen `DS:0002` und verwenden den Wert als Basisadresse der Handle-Tabelle:

- `0x7977`: DI = WORD `DS:0002`; scannt danach CX WORD-Einträge.
- `0x79C8`: berechnet Tabellenende aus `DS:0002 + 2*DS:000A`.
- `0x7A1A–0x7A28`: verwendet `DS:0002`, um aus einem Handleoffset den Index der Chunk-Flagtabelle zu berechnen.
- `0x7C89–0x7CA0`: durchläuft die Handle-Tabelle und passt Einträge bei einer Vergrößerung des Blocks an.
- `0x7DDD–0x7E1F`: durchläuft die Handle-Tabelle bei der Neuordnung/Verlagerung des freien Speicherbereichs.

Dies bestätigt die bereits in Untersuchung 2214 anhand von SPINTEXT R3 nachgewiesene Bedeutung von `DS:0002`: Offset der Handle-Tabelle innerhalb des LMem-Blocks.

### 2218.3 – Feld 000Ah: Anzahl der Handle-Einträge

`DS:000A` wird in den genannten Routinen als Schleifenzähler beziehungsweise Anzahl der WORD-Einträge verwendet. Beispielsweise liest `0x7977` den Wert nach CX und scannt ab `DS:0002` genau diese Anzahl WORD-Einträge. `0x79C8` multipliziert ihn mit zwei, um das Tabellenende zu bestimmen. Bei Erweiterungen wird der Wert in `0x7CB1–0x7CB6` um `0x18` erhöht.

Damit ist die Funktion als Anzahl der Handle-Tabelleneinträge direkt belegt.

### 2218.4 – Feld 0008h: Blockgröße/-grenze

`DS:0008` wird bei der Anlage mit einer berechneten Größe beschrieben. Die Speicherverwaltung verwendet es anschließend als obere Grenze beziehungsweise Größenlimit:

- `0x7B4A–0x7B52`: vergleicht Handle-/Offset plus angeforderte Größe mit `DS:0008`.
- `0x7CCE–0x7CE0`: berechnet benötigten Platz relativ zu `DS:0008` und prüft Überlauf/Größenlimit.
- `0x7D42–0x7D58`: berechnet eine neue Größe und schreibt sie nach `DS:0008`.
- `0x7E23–0x7E2B`: prüft den berechneten Endoffset gegen `DS:0008-1`.

Die vorsichtige Bezeichnung lautet daher: LMem-Blockgrößen-/Grenzwert. Ob das Feld in allen Zuständen exakt die physische Segmentgröße oder eine logische Heapgrenze repräsentiert, wird noch weiter geprüft.

### 2218.5 – Felder 000Ch und 000Eh: Heap-/Freispeicherverwaltung

`DS:000C` und `DS:000E` werden zusammen in der Speicherplatzverwaltung verwendet:

- `0x7919–0x7930`: initialisiert den Bereich ab `DS:000C` und schreibt einen Größenwert vor den Bereich.
- `0x7B8B–0x7B95`: setzt `DS:000E` auf null und aktualisiert `DS:000C`.
- `0x7C89–0x7CB6`: verschiebt die Handle-Tabelle und aktualisiert beide Felder.
- `0x7D42–0x7D70`: verwendet `DS:000E` bei der Größenberechnung und aktualisiert `DS:000C`/`DS:000E`.

Die Felder gehören damit nachweislich zur Verwaltung des freien Heapbereichs. Ihre exakte Einzelbedeutung (Cursor, Freiraumgröße oder Grenze) wird noch nicht endgültig festgelegt.

### 2218.6 – Feld 0010h: verkettete Hilfsliste

`0x7E7B–0x7E92` ruft die Routine `0x7977` zur Anlage eines Eintrags auf, schreibt den bisherigen Wert von `DS:0010` in das zweite WORD des neuen Eintrags und setzt `DS:0010` auf den neuen Eintrag. `0x7E93–0x7EAF` durchläuft diese verketteten Einträge und vergleicht deren erstes WORD mit dem gesuchten Wert.

Damit ist `DS:0010` der Kopf einer verketteten Hilfsliste. Die semantische Rolle der gelisteten Einträge bleibt offen.

### 2218.7 – Felder 0012h und 0014h: noch keine sichere Semantik

Beide Felder werden im Initialisierungspfad für den betreffenden Blocktyp auf null gesetzt. `DS:0012` wird außerdem in `0x8385` inkrementiert und in `0x838C` dekrementiert; bei Übergang auf null folgt eine Zustandsprüfung und gegebenenfalls ein Aufruf bei `0x900C`. An anderen Stellen wird der Wert vorübergehend gesichert und ersetzt. Das spricht für einen Zustands-/Verschachtelungswert, reicht aber noch nicht für eine eindeutige Benennung.

`DS:0014` wird unter anderem in `0x87B4` gelesen, gesichert und nach einem Bereinigungs-/Prüfpfad wieder in die ursprüngliche Struktur zurückgeschrieben. Eine vollständige Definition ist noch nicht bewiesen.

### 2218.8 – Bedeutung für den SDK-Aufbau

Die Originalkernelanalyse bestätigt nun mindestens diese Strukturmerkmale des LMem-Headers:

| Offset | Gesicherter Befund |
|---|---|
| `0x00` | WORD wird als Block-/Owner-Bezug initialisiert; genaue Semantik offen |
| `0x02` | Offset der Handle-Tabelle |
| `0x04` | Zustands-/Typfeld; im Typ-2-Pfad auf `0x8800` gesetzt |
| `0x06` | Initialisierungsparameter/Typwert; genaue Semantik offen |
| `0x08` | Blockgrößen-/Grenzwert |
| `0x0A` | Anzahl der Handle-Tabelleneinträge |
| `0x0C`, `0x0E` | Freispeicher-/Heapverwaltung |
| `0x10` | Kopf einer verketteten Hilfsliste |
| `0x12` | Zustands-/Verschachtelungswert; genaue Semantik offen |
| `0x14` | wird gesichert und wiederhergestellt; genaue Semantik offen |

Diese Befunde stammen aus dem Originalkernel und sind unabhängig von der SDK-Implementierung. Sie sind noch keine Freigabe, die SDK-Headerstruktur zu ändern: Vor einer Änderung müssen die Felder in mehreren realen LMem-Blöcken und über weitere Kernelpfade gegengeprüft werden.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x78B2–0x7EAF`, `0x8329–0x838C), `0x87AC–0x8913); ergänzend Original `GEOWORKS/WORLD/SPINTEXT.GEO`, Ressource R3, Header/Handle-/Flagtabellenwerte aus Untersuchung 2214. Statische Disassemblierung und Datenflussanalyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2219 – LMem-Chunk-Handles, Allokation, Resize und Freigabe

### 2219.1 – Handle-Tabelleneintrag und Chunkanfang

Die Routine `0x7977` sucht in der Handle-Tabelle ab dem in `DS:0002` gespeicherten Offset nach einem freien WORD-Eintrag. Die Anzahl der Einträge wird aus `DS:000A` gelesen. Ein freier Eintrag wird als WORD mit Wert null erkannt. Ist kein freier Eintrag vorhanden, ruft der Pfad `0x7C53` zur Erweiterung der Handle-Tabelle auf.

Für den gefundenen Eintrag ruft `0x7977` `0x79FB` auf. Diese Routine:

1. schreibt zunächst `0xFFFF` in den Handle-Tabelleneintrag;
2. gibt dessen Offset in AX zurück;
3. ruft bei nichtnull CX die Allokationsroutine `0x7A32` auf;
4. speichert den von `0x7CCE` gelieferten Chunkoffset in den Handle-Tabelleneintrag;
5. schreibt die aufgerundete Chunkgröße unmittelbar vor den Chunkinhalt, also an `ChunkOffset-2`.

Die Größe wird durch `(CX + 3) AND 0xFFFC` auf eine Vier-Byte-Grenze aufgerundet. Der Handle-Tabelleneintrag enthält damit einen Offset auf den Chunkinhalt; das WORD unmittelbar davor enthält die belegte Chunkgröße.

### 2219.2 – Chunk anlegen und Handle wiederverwenden

`0x7977` durchsucht die Handle-Tabelle nach einem freien Eintrag. Der Wert null kennzeichnet dabei einen freien Tabelleneintrag. Die Routine `0x79FB` setzt den Eintrag zunächst auf `0xFFFF` und übergibt die gewünschte Chunkgröße an `0x7A32).

Die Allokation selbst erfolgt über `0x7CCE`. Der zurückgegebene Offset wird in den Handle-Eintrag geschrieben. Damit ist der Zusammenhang zwischen Handle und Chunkdaten im Originalkernel direkt belegt.

Wenn die Tabelle keine freien Einträge enthält, erweitert `0x7C53` sie um `0x18` WORD-Einträge (24 Handles). Die Routine verschiebt den nachfolgenden Heapbereich um `0x30` Bytes, passt betroffene Handlewerte an und erhöht `DS:000A` um `0x18`.

### 2219.3 – Chunkgröße ändern

Die Routine `0x7A5D` ist der zentrale Resize-Pfad:

- AX enthält den Offset des Handle-Tabelleneintrags.
- CX enthält die angeforderte neue Chunkgröße.
- Der bisherige Chunkoffset wird aus dem Handle-Eintrag gelesen.
- Die alte Größe steht bei `[ChunkOffset-2]`.
- Die neue Größe wird wiederum auf eine Vier-Byte-Grenze aufgerundet.
- Bei unveränderter gerundeter Größe bleibt der Chunk an Ort und Stelle.
- Andernfalls versucht der Kernel zunächst, den Chunk im Heap zu erweitern beziehungsweise zu verschieben.
- Bei erfolgreicher Neuallokation wird der Handle-Eintrag auf den neuen Chunkoffset umgestellt und der bisherige Inhalt kopiert.
- Der bisherige Heapbereich wird anschließend über `0x7E32` angepasst.

Die Routine `0x7A5D` verwendet außerdem `0x7B42`, um zu prüfen, ob der Chunk unmittelbar in den angrenzenden freien Bereich hinein vergrößert werden kann. Reicht dieser Platz nicht aus, wird eine neue Allokation versucht; bei Bedarf wird der LMem-Block über `0x7D18` vergrößert.

### 2219.4 – Chunk freigeben

Es sind zwei unterschiedliche Vorgänge zu unterscheiden:

- `0x7A38`: liest den Chunkoffset aus dem Handle-Eintrag, setzt den Eintrag auf null und gibt den bisherigen Chunk über `0x7BE7` frei. Der Handle-Tabelleneintrag bleibt damit als freier Eintrag verfügbar.
- `0x7A4C`: tauscht den Handle-Eintrag mit `0xFFFF` aus. Wenn zuvor ein gültiger Chunkoffset darin stand, wird dessen Speicher ebenfalls über `0x7BE7` freigegeben. Der Handle wird damit nicht einfach als null-freier Eintrag zurückgelassen; der Sonderwert `0xFFFF` kennzeichnet einen anderen Zustand.

Die Unterscheidung zwischen null und `0xFFFF` ist für eine korrekte SDK-Abbildung wesentlich. Die genaue öffentliche API-Zuordnung dieser beiden Kernelpfade ist noch nicht bewiesen.

### 2219.5 – Einfügen und Löschen innerhalb eines Chunks

Die Routine `0x7ACA` verschiebt einen Teil des Chunkinhalts, um Platz für eine Einfügung zu schaffen. Sie bestimmt zunächst die aktuelle Chunkgröße, ruft `0x7A5D` mit der vergrößerten Größe auf und verschiebt danach den betroffenen Datenbereich innerhalb des Chunks. Der neu geschaffene Bereich wird mit null gefüllt.

Die Routine `0x7B08` führt den umgekehrten Vorgang aus: Sie verschiebt den verbleibenden Datenbereich nach vorn, verkleinert den Chunk über `0x7A5D` und passt damit den Chunkgrößeneintrag an.

Damit sind zwei eigenständige Chunkoperationen im Kernelcode nachgewiesen: Einfügen und Entfernen von Bytes innerhalb eines bestehenden Chunks.

### 2219.6 – Freispeicherliste und Zusammenführen benachbarter Blöcke

`0x7BE7` gibt einen Chunk in die verkettete Freispeicherliste zurück:

- liest die Chunkgröße bei `[SI-2]`;
- rundet sie auf eine Vier-Byte-Grenze;
- erhöht den Freispeicherzähler `DS:000E`;
- fügt den freigegebenen Bereich anhand seiner Adresse sortiert in die Liste ein;
- führt benachbarte freie Bereiche zusammen.

`0x7BCC` entfernt einen freien Bereich aus dieser Liste und aktualisiert die Verkettung. `0x7E32` passt einen Bereich an, wenn ein Chunk in seiner Größe verändert wird.

### 2219.7 – Blockvergrößerung und Kompaktierung

`0x7CCE` sucht einen passenden freien Bereich. Wenn keiner genügt, führt der Pfad über `0x7D18` eine Vergrößerung des LMem-Blocks aus. Dabei wird `DS:0008` angepasst und der neue Speicher über die Kernel-Speicherverwaltung angefordert.

`0x7D7C` prüft, ob Freispeicher vorhanden ist. `0x7D85–0x7E31` verschiebt Heapbereiche, aktualisiert die Handle-Tabelleneinträge, passt Verweise auf verschobene Chunks an und wiederholt den Vorgang, bis die Kompaktierung abgeschlossen ist oder die Blockgrenze erreicht wird.

### 2219.8 – Konsequenzen für den SDK-Entwurf

Für eine minimale LMem-Implementierung sind jetzt folgende Eigenschaften direkt belegt:

1. Die Handle-Tabelle enthält WORD-Offsets auf Chunkinhalte.
2. Ein freier Handle-Eintrag kann den Wert null enthalten.
3. Ein weiterer Sonderzustand ist `0xFFFF`; er darf nicht pauschal mit null gleichgesetzt werden.
4. Vor jedem Chunkinhalt liegt ein WORD mit der Chunkgröße.
5. Chunkgrößen werden auf Vier-Byte-Grenzen aufgerundet.
6. Handle-Tabellen-Erweiterung und Heapverschiebung erfordern die Anpassung der betroffenen Handlewerte.
7. Die Freispeicherliste ist verkettet und wird sortiert geführt; benachbarte freie Bereiche werden zusammengeführt.
8. Das Vergrößern eines Chunks kann eine Verschiebung des Chunkinhalts und eine Aktualisierung des Handles auslösen.

Die Befunde beschreiben die beobachteten Kernelpfade. Sie legen noch keine vollständige öffentliche LMem-API fest und sind keine Freigabe, die SDK-Implementierung ohne weitere Vergleichstests zu ändern.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x7977–0x7A37`, `0x7A38–0x7B41`, `0x7B42–0x7B75`, `0x7B76–0x7E50`. Ergänzend die LMem-Header-/Handle-/Flagtabellenbelege aus den Untersuchungen 2214 und 2218. Statische Disassemblierung und Datenflussanalyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2220 – Unabhängige Aufrufstellen bestätigen Chunk-Resize und Chunk-Edit

### 2220.1 – Descriptoraktualisierung verwendet Einfügen und Löschen

Die Kernelroutine `0x8226` arbeitet mit einem über SI adressierten Handle-/Datenbereich und vergleicht einen gespeicherten Größenwert mit einer neu berechneten Größe. Bei einer Größenänderung wird die Differenz gebildet:

- Bei negativer Differenz wird `0x7B08` aufgerufen.
- Bei positiver Differenz wird `0x7ACA` aufgerufen.
- Anschließend werden die betroffenen WORD-Offsets in einer nachfolgenden Eintragstabelle angepasst.

Damit ist der Einsatz von `0x7B08` und `0x7ACA` als Entfernen beziehungsweise Einfügen von Bytes nicht nur aus ihrem internen Speicherbewegungsalgorithmus abgeleitet, sondern auch durch einen unabhängigen Kernel-Aufrufer bestätigt.

### 2220.2 – Einfüge-/Löschoperationen wirken auf einen konkreten Chunk

In `0x8226` wird vor dem Aufruf der Chunkoffset aus dem Handle-Eintrag geladen. Die Routine berechnet den Größenunterschied und übergibt an `0x7B08` beziehungsweise `0x7ACA` die Handle-/Chunkreferenz und die Änderungsgröße. Danach werden die nachfolgenden Offsets in einer Tabelle angepasst.

Die Kombination aus Chunk-Resize und Offsetkorrektur zeigt, dass die Operationen dazu dienen, einen variabel großen Datenbereich innerhalb eines LMem-Chunks zu verändern, ohne die logischen Verweise auf die darin liegenden Einträge unverändert zu lassen.

### 2220.3 – Weitere Freigabe-/Resize-Aufrufstellen

Im Kernelbereich `0x3076–0x3093` wird ein vorhandener Chunk bei Bedarf über `0x7A38` freigegeben. Anschließend wird, abhängig von einem Statusbit, ein neuer Chunk der Größe `0x000E` über `0x7977` angelegt. Das ist eine unabhängige Bestätigung für die Kombination aus Handle-Freigabe und neuer Chunkallokation.

Im Bereich `0x8877–0x88AC` durchläuft der Kernel Handle-Tabelleneinträge und verwendet:

- `0x7A38`, um einen Chunk freizugeben;
- `0x7A5D` mit CX = 0, um den Chunk über den Resize-Pfad auf null Größe zu setzen beziehungsweise den entsprechenden Handlepfad auszuführen.

Der Code prüft vorher Statusbits im Chunk-/Objektkontext. Die Bedeutung dieser Bits wird nicht allein aus diesen Aufrufstellen abgeleitet.

### 2220.4 – Bedeutung der drei Handlezustände

Die beobachteten Routinen unterscheiden mindestens diese WORD-Werte in einem Handle-Tabelleneintrag:

| Wert | Beobachtetes Verhalten |
|---|---|
| `0x0000` | wird von `0x7977` als freier Handleeintrag gesucht |
| `0xFFFF` | wird von `0x79FB` während der Chunkanlage gesetzt; wird in `0x7A5D` als Sonderwert des Chunkoffsets erkannt |
| anderer Offset | wird als Offset des Chunkinhalts verwendet; die Chunkgröße liegt bei Offset minus zwei |

Die Bedeutung von `0xFFFF` als dauerhaftem Zustand ist noch nicht endgültig geklärt. Sicher ist lediglich, dass der Kernel den Wert von null unterscheidet und dass er im Allokations-/Freigabepfad als besonderer Marker behandelt wird.

### 2220.5 – Konsequenz für den Test-GEODE

Die Untersuchung bestätigt die internen Regeln für Chunk-Handles und Datenbereichsänderungen. Für einen ersten Test-GEODE ist damit weiterhin nicht ausreichend geklärt, welche öffentliche LMem-Aufruffolge der GEODE beim Laden tatsächlich benötigt und welche Ressourcen-/Relokationsanforderungen zusätzlich gelten. Die Erkenntnisse rechtfertigen deshalb noch keine Implementierung eines eigenen LMem-Blocks im SDK.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x8226–0x828D), `0x3076–0x3093), `0x8877–0x88AC), sowie die LMem-Routinen `0x7977`, `0x7A38`, `0x7A5D`, `0x7ACA`, `0x7B08`. Statische Disassemblierung und Datenflussanalyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2221 – Chunk-Flag-Schnittstelle und konkrete Aufrufer

### 2221.1 – Getter und Setter der Chunk-Flagtabelle

Die Routinen `0x8329` und `0x833C` greifen auf dieselbe Flagtabelle zu, deren Lage in Untersuchung 2214 anhand von SPINTEXT R3 bytegenau nachgewiesen wurde.

- `0x8329`: AX enthält den Handleoffset. Die Routine berechnet aus `DS:0002` und dem Handleoffset den Byteindex, liest das Flagbyte und gibt es in AL zurück.
- `0x833C`: AX enthält den Handleoffset. BH ist die zu löschende Bitmaske, BL die zu setzende Bitmaske. Die Operation lautet exakt `new = (old AND NOT BH) OR BL`.

Der Setter ruft danach `0x835C` auf. Diese Nachbehandlung hängt vom resultierenden Flagbyte ab.

### 2221.2 – Nachbehandlung in 835Ch

`0x835C` kehrt sofort zurück, wenn Bit `0x04` gesetzt ist oder Bit `0x08` nicht gesetzt ist. Nur wenn Bit 0x04 gelöscht und Bit 0x08 gesetzt ist, prüft die Routine zusätzlich:

1. `DS:0005`, Bit `0x01`;
2. den über `DS:0000` referenzierten Kernel-Handleeintrag;
3. dort Byteoffset `+0x0A`, Bit `0x20`.

Wenn auch diese letzte Bedingung zutrifft, ruft sie `0xA567` auf. Diese Routine löscht Bit `0x20` im betreffenden Kernel-Handleeintrag und ruft anschließend `0xAE4C` auf. Die Bedeutung von Bit 0x20 und die vollständige Wirkung von AE4C bleiben offen.

### 2221.3 – Direkter Aufrufer 8FD3h: Flagprüfung und Freigabepfad

Die Routine `0x8FD3` führt folgende Schritte aus:

1. ruft `0x838C` auf;
2. liest über `0x8329` das Flagbyte für den Handleoffset in SI;
3. prüft Bit `0x02`;
4. wenn Bit 0x02 gesetzt ist, setzt sie über `0x833C` zusätzlich Bit `0x08`, setzt CX auf null und ruft `0x7A5D` auf;
5. wenn Bit 0x02 nicht gesetzt ist, springt sie zu `0x7A38`, das den Chunk freigibt und den Handleeintrag auf null setzt.

Das ist ein direkter Beleg dafür, dass Bit 0x02 einen anderen Freigabe-/Resizepfad auswählt. Die Routine benennt die Semantik des Bits nicht; deshalb wird es hier ausdrücklich nicht als „shared“, „locked“ oder „discardable“ bezeichnet.

### 2221.4 – Weitere Setter-Aufrufer

- `0x87A1` setzt Bit `0x08` im Flagbyte des über SI referenzierten Handles, nachdem der zugehörige Datenbereich kopiert wurde.
- `0x9328` und `0x9336` setzen ebenfalls Bit `0x08`; die Aufrufe liegen im Pfad `0x9323`, der einen DS-Kontext sichert, den Flagzustand ändert und danach weitere Verwaltungsroutinen aufruft.
- `0x8FF8` ist ein Getter-Weiterleiter: CX wird nach AX kopiert und anschließend `0x8329` ausgeführt.
- `0x8FFD` ist ein Setter-Weiterleiter: CX wird nach AX, DX nach BX kopiert und anschließend `0x833C` ausgeführt.

Damit sind die Registerkonventionen der Getter-/Setter-Wrapper und mehrere reale Bit-Setzstellen belegt.

### 2221.5 – Präzisierung der Größenrundung aus Untersuchung 2219

Eine erneute Prüfung des Allokationscodes `0x79FB` präzisiert die dortige Größenrechnung:

- Vor dem Aufruf von `0x7A32` wird CX um zwei erhöht.
- Für die Allokation wird zusätzlich drei addiert und mit `0xFFFC` maskiert.
- Der zuvor um zwei erhöhte Wert wird anschließend als WORD bei `ChunkOffset-2` gespeichert.

Damit ist die gespeicherte Chunkgröße nicht einfach die gerundete Allokationsgröße: Das gespeicherte WORD entspricht der angeforderten Nutzgröße plus dem zwei Byte großen Größenpräfix; die für die Heapreservierung verwendete Größe wird separat auf eine Vier-Byte-Grenze aufgerundet. Diese Präzisierung ersetzt die vereinfachte Formulierung in Untersuchung 2219.1/2219.2.

### 2221.6 – Ergebnis und offene Fragen

Gesichert sind jetzt die Byteposition der Flagtabellen, die Rechenformel des Setters, die Getter-/Setter-Registerkonvention und konkrete Aufrufpfade, in denen Bit 0x02 geprüft und Bit 0x08 gesetzt wird.

Nicht gesichert sind die offiziellen symbolischen Namen beziehungsweise Bedeutungen der Bits 0x02, 0x04 und 0x08. Ebenso bleibt offen, ob alle Chunktypen dieselbe Flagsemantik verwenden. Diese Bezeichnungen werden erst nach einer weiteren unabhängigen Gegenprobe vergeben.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x8329–0x838C), `0x87A1), `0x8FD3–0x9001), `0x9323–0x933F), `0x79FB–0x7A37), `0xA567–0xA574). Ergänzend SPINTEXT R3, Untersuchung 2214. Statische Disassemblierung und Datenflussanalyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2222 – Drei getrennte Flag-/Statusbereiche nicht verwechseln

### 2222.1 – Chunk-Flagbyte (LMem-Handleindex → Flagtabelle)

Die Routinen `0x8329` und `0x833C` adressieren die separate Chunk-Flagtabelle. Der Index wird aus dem Handleoffset relativ zu `DS:0002` berechnet; die Basis der Flagbytes stammt aus dem ersten WORD der Handle-Tabelle. Diese Datenstruktur ist anhand SPINTEXT R3 direkt verifiziert (Untersuchung 2214).

Das Chunk-Flagbyte ist daher nicht identisch mit dem ersten Datenbyte des Chunks und auch nicht mit einem Byte im globalen Kernel-Handleeintrag.

### 2222.2 – LMem-Headerstatus bei DS:0005

Die Routine `0x835C` prüft `DS:0005`, Bit `0x01`. Weitere Kernelpfade lesen dort unter anderem Bits `0x04`, `0x10`, `0x20` und `0x80` (beispielsweise `0x838C`, `0x8887`, `0x8890`, `0x7A13`). Diese Zugriffe beziehen sich auf das Byte im LMem-Blockkopf bei Offset 5, nicht auf das einzelne Chunk-Flagbyte.

Der Befund ist für die SDK-Analyse wichtig: Ein Bitwert wie `0x08` in der Chunk-Flagtabelle darf nicht mit gleich nummerierten Bits in `DS:0005` gleichgesetzt werden. Es handelt sich um getrennte Speicherorte und getrennte Statusdomänen.

### 2222.3 – Kernel-Handleeintrag bei ES:[BX+0Ah]

Andere Routinen prüfen oder ändern ein Statusbyte bei Offset `+0x0A` eines Kernel-Handleeintrags:

- `0x835C` prüft dort Bit `0x20` und ruft bei gesetztem Bit `0xA567` auf; `0xA567` löscht dieses Bit.
- `0x8A46` prüft Bit `0x08` im Byte `ES:[BX+0x0A]`.
- `0x8A7E` prüft Bit `0x02` in einem weiteren Kernel-Handleeintrag.

Diese Zugriffe liegen im globalen Kernel-Handlekontext, nachdem der Eintrag über den Kernel-Handle-/Ressourcenpfad aufgelöst wurde. Sie sind nicht die LMem-Chunk-Flagtabelle. Auch die gleichlautenden Offsetnummern (zum Beispiel `+0x0A`) dürfen nicht als dieselbe Struktur interpretiert werden.

### 2222.4 – Chunkdatenbyte und Bereinigungsroutine 8867h

Die Routine `0x8867` durchläuft die LMem-Handle-Tabelle. Für jeden Eintrag liest sie den Chunkoffset, überspringt die Sonderwerte null und `0xFFFF`, und untersucht anschließend das erste Byte am Chunkinhalt (`DS:[ChunkOffset]`). Dieses Byte wird in AL/AH ausgewertet und über eine Tabelle bei `0x8857` in einen Bereinigungszweig umgesetzt.

Je nach Ergebnis ruft sie `0x7A38` (Chunk freigeben) oder `0x7A5D` mit CX=0 (Resize-/Nullgrößenpfad) auf. Für bestimmte Chunktypen folgt eine Descriptor-/Objektbereinigung, die über `0x8226` Datenbereiche anpasst.

Die Routine ist damit ein weiterer Beleg, dass LMem-Chunkinhalte selbst interne Typ-/Statusbytes besitzen können. Dieses erste Chunkdatenbyte ist wiederum weder das Chunk-Flagbyte aus der separaten Flagtabelle noch das Headerstatusbyte `DS:0005`.

### 2222.5 – Konsequenz für die Flagsemantik

Die bisher untersuchten Kernelzugriffe umfassen mindestens drei getrennte Bereiche:

| Bereich | Speicherstelle | Verwendung |
|---|---|---|
| LMem-Chunk-Flags | Separate Flagtabelle, indexiert über Handleoffset und `DS:0002` | Getter/Setter `0x8329`/`0x833C` |
| LMem-Headerstatus | `DS:0005` | Blockweite Verwaltungs-/Statusbits |
| Kernel-Handlestatus | Byte `+0x0A` im Kernel-Handleeintrag | globale Handle-/Ressourcenstatusbits |
| Chunkdaten | erstes Byte bei `DS:[ChunkOffset]` | chunkinterne Typ-/Statusauswertung in `0x8867` |

Damit sind gleich nummerierte Bits aus unterschiedlichen Bereichen ausdrücklich nicht austauschbar. Die Bedeutungen der einzelnen Bits bleiben dort offen, wo kein eindeutiger Kontrollflussbeleg vorliegt.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x8329–0x838C), `0x8867–0x8913), `0x8A41–0x8A84), `0xA567–0xA574); SPINTEXT R3, LMem-Header und Flagtabellenbeleg aus Untersuchung 2214. Statische Disassemblierung und Datenflussanalyse; kein Laufzeittest.

**Unverändert:** Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2223 – GEODE-Lader: interne Tabellen für Imports, Ressourcen und Relokationen

### 2223.1 – Importtabellenaufbau (1B45h–1B80h)

Die Laderoutine bei `0x1B45` berechnet den Start der Importfunktionsdatensätze:

```asm
1B45  mov dx,WORD PTR ds:0x34
1B49  shl dx,1
1B4B  add dx,WORD PTR ds:0x36
1B4F  mov WORD PTR ds:0x30,dx
1B53  mov cx,WORD PTR ds:0x32
...
1B5A  shl cx,1
1B5C  shl cx,1
1B5E  mov bx,WORD PTR ds:0x40
1B62  xor al,al
1B64  call 0x1088
```

Der berechnete Offset `DS:0030` liegt um `2 * DS:0034` WORDs hinter `DS:0036`. Der Lader liest anschließend `4 * DS:0032` Bytes in diesen Bereich. Danach durchläuft `0x1B6B–0x1B7E` genau `DS:0032` Einträge mit jeweils vier Byte Abstand und ruft für den zweiten WORD jedes Eintrags die Relokationsroutine `0x1C04` mit Quelle `0x22` auf.

Damit sind die internen Größenrelationen nachgewiesen: `DS:0034` zählt WORD-Einträge vor der Importfunktionsliste; `DS:0032` zählt vier Byte große Importfunktionsdatensätze. `DS:0036` ist der Anfangsbezug für die vorhergehende WORD-Tabelle. Die genaue Benennung der vorhergehenden Einträge wird nicht über die Feldnummer allein festgelegt.

### 2223.2 – Ressourcentabelle ist in drei parallele Bereiche gegliedert (1C76h–1CA3h)

Der Lader berechnet:

```asm
1C76  mov ax,WORD PTR ds:0x32
1C79  shl ax,1
1C7B  shl ax,1
1C7D  add ax,WORD PTR ds:0x30
1C81  mov WORD PTR ds:0x3a,ax
1C86  mov cx,WORD PTR ds:0x38
1C8D  shl cx,1
1C8F  add ax,cx
1C91  mov WORD PTR ds:0x3c,ax
1C94  shl cx,1
1C96  add ax,cx
1C98  mov WORD PTR ds:0x3e,ax
1C9B  shl cx,1
...
1CA3  call 0x1088
```

Daraus folgt unmittelbar:

- `DS:003A` = Anfang des Ressourcentabellenbereichs.
- `DS:003C` = Anfang plus `2 * Ressourcenzahl`.
- `DS:003E` = Anfang plus `6 * Ressourcenzahl`.
- Gelesen werden insgesamt `8 * Ressourcenzahl` Bytes.

Der Ressourcentabellenbereich enthält somit drei aufeinanderfolgende Arrays:

1. `n` WORD-Einträge ab `DS:003A` (pro Ressource ein Laufzeit-/Segmentplatz);
2. `n` Paare aus WORDs ab `DS:003C` (pro Ressource zwei WORD-Felder);
3. `n` WORD-Einträge ab `DS:003E` (pro Ressource ein weiteres WORD-Feld).

Die Zuordnung der zweiten und dritten Arrays wird durch die Verbraucher bestätigt: `0x2218` verwendet `DS:003C + 2*Index`, liest dort zwei WORDs und nutzt sie als Dateiposition und Lesegröße. `0x20FE` verwendet `DS:003E + 2*Index`, um die Anzahl der Relokationseinträge für die betreffende Ressource zu bestimmen.

### 2223.3 – Ressourcen laden und Relokationen anwenden (20FEh–2150h, 2218h–223Fh)

`0x2218` lädt eine Ressource anhand ihres Index:

1. liest die beiden WORD-Felder aus dem Ressourcendatenarray bei `DS:003C`;
2. verwendet `0x10CA` zum Positionieren im GEODE-Datei-Handle `DS:0040`;
3. liest die Ressourcendaten in einen temporären Puffer;
4. gibt das zugewiesene Segment an den Aufrufer zurück.

`0x20FE` ruft zuerst `0x2218` auf, setzt ES auf das zurückgegebene Ressourcensegment und liest die Relokationsanzahl aus `DS:003E + 2*Index`. Die Relokationsdatensätze werden in Blöcken von maximal `0x100` Bytes gelesen. Jeder Datensatz besteht aus zwei WORDs; diese werden als AX und BX an den Dispatcher `0x2153` übergeben. Der Dispatcher verarbeitet Quellklasse und Relokationstyp getrennt.

Damit ist die Ladefolge im Kernel belegt: Ressourcendaten laden, Zielsegment setzen, Relokationsanzahl lesen, Relokationsdatensätze blockweise einlesen und einzeln anwenden.

### 2223.4 – Ressourcentabelle und LMem sind verschiedene Ebenen

Die Ressourcentabelle beschreibt Ressourcen des GEODE und deren Laufzeitsegmente, Dateipositionen, Lesegrößen und Relokationszahlen. Sie ist nicht die LMem-Handle-Tabelle innerhalb einer einzelnen Ressource. Eine Ressource kann einen LMem-Block enthalten; die Ressourcentabelle selbst ist jedoch die übergeordnete Lade-/Relokationsebene.

Für die SDK-Implementierung müssen daher zwei voneinander unabhängige Strukturen korrekt sein:

- GEODE-Ressourcenverzeichnis und Relokationstabellen;
- gegebenenfalls LMem-Header, Handle-Tabelle und Chunk-Flagtabelle innerhalb einer geladenen Ressource.

### 2223.5 – Originaldatei-Kandidaten für die Gegenprüfung

Aus dem deutschen GeoWorks-Archiv wurden zwei kleine Original-GEODEs als Vergleichskandidaten isoliert:

| Datei | Größe | SHA-256 | Identifizierende Bytes |
|---|---:|---|---|
| `GEOWORKS/SYSTEM/SAVERS/BLANK.GEO` | 1.332 Bytes | `845b310069c51352242331c88531ef64f6b06d38dd9837a627b0333a82fac93f` | Signatur `C7 45 CF 53`; Typbytes bei Offset `0x14`: `SSAV`; Name `Blank`; sichtbare Ressourcennamen `saver`, `ui` |
| `GEOWORKS/SYSTEM/DISK.GEO` | 910 Bytes | `6363699f0b9af45106b59e432f3b715f4e9c38d5e5c07a45fcce660f3f964be9` | Signatur `C7 45 CF 53`; Typbytes bei Offset `0x14`: `EMDM`; Name `Disk Swap Driver` |

Die Dateien dienen zunächst nur als unveränderte Vergleichsobjekte. Ihre Dateiköpfe und Ressourcentabellen sind noch nicht vollständig auf die vom Lader erwarteten Felder abgebildet. Insbesondere wird BLANK.GEO nicht als „minimales GEODE“ bezeichnet, bevor Imports, Ressourcenflags, Relokationen und Startpfad vollständig geprüft sind.

### 2223.6 – Konsequenz für den ersten Test-GEODE

Der Kernel-Lader benötigt mindestens konsistente Importmetadaten, ein Ressourcenzählfeld, die drei parallelen Ressourcentabellenbereiche sowie zu jeder geladenen Ressource eine gültige Dateiposition, Größe und Relokationsliste. Daraus lässt sich noch kein vollständiger, gültiger Dateikopf ableiten: Die vorgelagerten Headerfelder, ihre Offsets im GEODE und die erforderlichen Ressourcenflags müssen als nächstes mit BLANK.GEO und einem zweiten Original-GEODE abgeglichen werden.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x1B45–0x1B80), `0x1C76–0x1CA3), `0x20FE–0x2153), `0x2218–0x223F); Originaldateien aus `GEOWORKS.zip`: `GEOWORKS/SYSTEM/SAVERS/BLANK.GEO` und `GEOWORKS/SYSTEM/DISK.GEO`, jeweils SHA-256 oben. Statische Disassemblierung und Dateibyteprüfung; kein Laufzeittest.

**Unverändert:** Originalarchiv, Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.


## Untersuchung 2224 – Importbibliotheken und Importfunktionen getrennt nachgewiesen

### 2224.1 – Bibliotheksdeskriptoren im GEODE

Die Routine `0x2652–0x26B5` legt die Importbibliotheksliste an. Sie setzt `DS:0036` auf den Laufzeitbereich `0x0046` oder `0x005E`, abhängig von einem GEODE-Statusbit. `DS:0034` gibt die Anzahl der importierten Bibliotheken an.

Für jede Bibliothek liest der Lader genau `0x0E` Bytes aus dem GEODE in einen temporären Stackbereich. Aus jedem 14-Byte-Datensatz werden die WORD-Felder bei +8, +10 und +12 an die Bibliotheksauflösungsroutine `0x271C` übergeben. Der zurückgegebene Bibliothekssegmentwert wird in die WORD-Tabelle ab `DS:0036` eingetragen. Der nächste Laufzeitplatz liegt jeweils zwei Byte weiter.

Damit ist `DS:0036` als Anfang einer WORD-Tabelle mit einem Laufzeitsegment pro importierter Bibliothek bestätigt. `DS:0034` ist die Zahl dieser Bibliothekseinträge. Die genaue semantische Bedeutung der drei aus dem 14-Byte-Deskriptor übergebenen WORD-Felder wird hier nicht weiter benannt, weil die vollständige Protokoll-/Versionsprüfung noch separat zu verfolgen ist.

### 2224.2 – Importfunktionsdatensätze

Nach Abschluss der Bibliotheksauflösung berechnet `0x1B45` den Start der Importfunktionsliste:

`DS:0030 = DS:0036 + 2 * DS:0034`

`DS:0032` ist die Anzahl der Importfunktionsdatensätze. Der Lader liest `4 * DS:0032` Bytes in diesen Bereich und durchläuft anschließend die Einträge mit jeweils vier Byte Abstand. Für jeden Eintrag wird der zweite WORD an die Relokationsroutine `0x1C04` übergeben.

Damit ist die interne Importstruktur präzisiert:

1. WORD-Segmenttabelle ab `DS:0036`, ein WORD je importierter Bibliothek;
2. anschließend vier Byte pro importierter Funktion ab `DS:0030`;
3. Anzahl der Bibliotheken in `DS:0034`;
4. Anzahl der Importfunktionen in `DS:0032`.

### 2224.3 – Relokationsquelle 10h bestätigt den Bibliotheksindex

Der Relokationsdispatcher `0x2153` behandelt Quellklasse `0x10` gesondert. Er nimmt den Bibliotheksindex aus AH, berechnet `DS:0036 + 2*AH`, lädt aus diesem WORD das Segment der betreffenden Bibliothek und verwendet anschließend den Importfunktionsdatensatzbereich ab `DS:0030). Damit stimmt die Laufzeitauflösung direkt mit der in `0x2652–0x26B5` aufgebauten Segmenttabelle überein.

### 2224.4 – Korrektur/Präzisierung zu Untersuchung 2223

Die Formulierung in 2223.1, `DS:0034` zähle lediglich WORD-Einträge vor der Importfunktionsliste, war zu unpräzise. Präzise ist: `DS:0034` ist die Anzahl importierter Bibliotheken; `DS:0036` zeigt auf die zugehörige WORD-Segmenttabelle. Die Importfunktionsliste folgt unmittelbar dahinter und wird über `DS:0030` adressiert; ihre Anzahl steht in `DS:0032`.

Die Ressourcentabelle ab `DS:003A` folgt wiederum nach den vier Byte großen Importfunktionsdatensätzen. Diese Bereiche sind getrennte Tabellen und dürfen nicht miteinander vermischt werden.

**Quellenbasis:** `GEOWORKS/KERNEL.OLD`, Load-Image-Offsets `0x2652–0x26B5), `0x1B45–0x1B80), `0x2153–0x21C6), `0x1C04–0x1C15). Statische Disassemblierung und Register-/Datenflussanalyse; kein Laufzeittest.

**Unverändert:** Originalarchiv, Originalkernel, gepatchter Kernel, GEO-Dateien und SDK-Quelltexte.
