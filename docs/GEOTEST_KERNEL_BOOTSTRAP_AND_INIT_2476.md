# GEOTEST – Untersuchung 2476

## Kernel-Bootstrap, relocierter Kernelbereich und Initialisierung

Stand: 12.11.2026

### 1. Untersuchungsgrundlage

Untersucht wurden die beiden Kernel-Dateien aus `GEOWORKS.zip`:

- `GEOWORKS/KERNEL.EXE`: 72.736 Bytes, SHA-256 `c2cc8952cdb01d0f459bf281ee3b78f8ce9464aba0b58c3758f8c73e24fb6eb5`
- `GEOWORKS/KERNEL.OLD`: 72.688 Bytes, SHA-256 `bd4d680b15f8dd66b2b09b506de96672972f716a11e0a38220477bf07b6c1e9b`

Die Provenienz bleibt getrennt: `KERNEL.EXE` ist laut Nutzer die gepatchte englische Kernel-Datei; `KERNEL.OLD` ist der originale deutsche Kernel. Die Untersuchung verändert keine dieser Dateien.

### 2. MZ-Einstieg und erster Fernaufruf

Für `KERNEL.EXE` liegt der MZ-Einstieg bei CS:IP = `0000:02B1`. Bei einem MZ-Header von `0x600` Bytes ergibt sich Datei-Offset `0x08B1`.

Dort steht:

```asm
08B1: 9A 00 00 93 0F   CALL FAR 0F93:0000
```

Der MZ-Relokationseintrag (Offset `0x02B4`, Segment 0) zeigt auf das Segmentwort der CALL-FAR-Instruktion (Instruktionsanfang +3). Das ist eine DOS-MZ-Relokation und nicht mit einer GEODE-Ressourcen-Fixup-Tabelle gleichzusetzen.

Der Aufruf bei `0F93:0000` erreicht den Code am Datei-Offset `0xFF30` (MZ-Header `0x600` plus Segment `0xF93 * 16`).

### 3. Funktion bei 0F93:0000 – Kopieren des Kernelbereichs

Der Code bei Datei-Offset `0xFF30`:

- sichert SS und SP im Kernel-Datensegment (Offsets `0x40` und `0x42`),
- liest den oberen Speichersegmentwert aus DS:[0002],
- zieht `0x0642` Paragraphen ab (entspricht `0x6420` Bytes),
- setzt ES auf das so berechnete Zielsegment,
- setzt DS auf `0F93`,
- kopiert mit REP MOVSW insgesamt `0x0E70` Wörter = `0x1CE0` Bytes ab `0F93:0000` nach ES:0000,
- berechnet anschließend AX = ES - `0F93` und kehrt mit RETF zurück.

Der Aufrufer addiert den zurückgegebenen Wert AX zu CS:[02C8]. Die Sequenz belegt damit eine Verlagerung/Kopie eines Kernelbereichs in einen neu berechneten Speicherbereich. Sie belegt keine GEODE-Ressourcen-Fixup-Verarbeitung.

### 4. Zweiter Fernaufruf – Initialisierungsroutine

Der zweite frühe Fernaufruf lautet:

```asm
08C5: 9A C7 01 93 0F   CALL FAR 0F93:01C7
```

Sein Ziel liegt bei Datei-Offset `0x100F7`. Dort beginnt eine längere Initialisierungsroutine. Sie richtet DS auf das Kernel-Datensegment ein und sichert Segment-/Statuswerte, ruft mehrere interne Initialisierungsroutinen auf, führt DOS-Dateioperationen aus (unter anderem ist im Folgecode ein INT 21h / AH=3Dh zum Öffnen einer Datei erkennbar) und ruft weitere Initialisierungsfunktionen auf, bevor sie mit RETF zurückkehrt.

Der Aufrufname und die exakte semantische Bedeutung der einzelnen Unterroutinen sind aus den hier vorliegenden Bytes allein nicht sicher bestimmbar. Insbesondere wird der Routine hier kein erfundener Name wie „GeodeLoad“ zugewiesen.

### 5. Übergang in den Kernel-Hauptablauf

Nach den beiden Fernaufrufen setzt der Bootstrap den Stackwert, ruft eine weitere interne Routine auf und springt bei Datei-Offset `0x08E0` nach `0xA0C0`.

Der Code ab `0xA0C0` lädt SS aus einem CS-relativen Speicherfeld, setzt SP auf `0x15F0`, initialisiert DS und ES auf `0x0E34`, aktiviert Interrupts und arbeitet anschließend mit Kernelzustandsfeldern und weiteren internen Routinen. Das ist ein Kernel-Hauptablauf-/Scheduler-naher Pfad. Auch dieser Code ist kein Nachweis des GEODE-Laders.

### 6. Vergleich KERNEL.OLD

`KERNEL.OLD` zeigt dieselbe Grundstruktur, mit versionsbedingten Segment- und Offsetdifferenzen:

- erster Fernaufruf: `0F90:0000` statt `0F93:0000`,
- zweiter Fernaufruf: `0F90:01C7` statt `0F93:01C7`,
- erster Kopiercode bei Datei-Offset `0xFF00` statt `0xFF30`,
- kopierte Länge ebenfalls `0x1CE0` Bytes,
- Quellsegment im Kopiercode `0F90` statt `0F93`,
- MZ-Einstieg springt nach der Initialisierung nach `0xA0D6` statt `0xA0C0`.

Die Bootstrap-/Kopierstruktur ist somit in beiden Dateien vorhanden. Die Differenzen belegen keine Änderung der GEODE-Fixup-Semantik.

### 7. Ergebnis und Grenzen

**Gesichert:**

- Die frühen MZ-Relokationen fixieren Segmentwörter von CALL-FAR-Instruktionen.
- Der erste frühe Fernaufruf kopiert einen `0x1CE0` Byte großen Kernelbereich an eine neu berechnete Speicherposition und liefert einen Segmentverschiebungswert zurück.
- Der zweite frühe Fernaufruf startet eine umfangreiche Kernel-Initialisierung.
- `KERNEL.OLD` und `KERNEL.EXE` besitzen dieselbe grundsätzliche Bootstrap-Struktur.

**Nicht gesichert:**

- Die tatsächliche Routine, die GEODE-Dateien lädt.
- Das Format und die Laufzeitverarbeitung der GEODE-Ressourcen-Fixup-Einträge im Kernel.
- Die Interpretation der in den vorherigen Untersuchungen gefundenen class0/type0-Einträge durch den GEODE-Lader.

Es wurden keine Parserregeln geändert, keine SDK-Dateien gepatcht und kein GEOTEST.GEO-Build oder Laufzeittest durchgeführt.

### 8. Quellenhinweis

Marcus Gröbers GeoDump-Dokumentation beschreibt auf hoher Ebene GEODE-Header, Bibliothekslisten, Exporttabellen, Ressourcentabellen und ressourcenbezogene Fixup-Tabellen. Sie ist eine historische, externe Formatbeschreibung und kein direkter Nachweis für die konkrete Kernelroutine dieser GeoWorks-1.x-Version: https://www.mgroeber.de/geodump-documentation.html

PC/GEOS-2.x-/FreeGEOS-Quellen wurden nicht als Beleg für GeoWorks 1.x herangezogen.
