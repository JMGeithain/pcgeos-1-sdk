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