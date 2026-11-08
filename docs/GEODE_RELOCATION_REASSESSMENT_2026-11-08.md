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