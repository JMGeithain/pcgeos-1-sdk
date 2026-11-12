# Untersuchung 2478 – Kernel-Dispatcher und Speicherblockverwaltung

**Stand:** 12.11.2026  
**Geltungsbereich:** GeoWorks / PC/GEOS 1.x. Keine Übertragung von PC/GEOS-2.x-/FreeGEOS-Implementierungsdetails.

## Grundlage

Untersucht wurden die beiden Kernel-Dateien aus `GEOWORKS.zip`, ohne Änderungen:

- `KERNEL.EXE` (laut Nutzer gepatchte englische Datei), 72.736 Bytes, SHA-256 `c2cc8952cdb01d0f459bf281ee3b78f8ce9464aba0b58c3758f8c73e24fb6eb5`
- `KERNEL.OLD` (laut Nutzer originaler deutscher Kernel), 72.688 Bytes, SHA-256 `bd4d680b15f8dd66b2b09b506de96672972f716a11e0a38220477bf07b6c1e9b`

**Adressierung:** Ein Fernaufruf `0000:0513` verweist auf Kernel-Offset `0x0513) im geladenen MZ-Modul. Für die Dateiabbildung ist der MZ-Header von `0x600` Bytes zu addieren. Eine Multiplikation des Offsets mit 16 wäre hier falsch.

## 1. Dispatcher bei `0000:0513`

Aufruf aus dem Initialisierungspfad bei Kernelcode `0x1079C`; Datei-Offset des Ziels: `0x0B13`.

Dort setzt der Code `AX=0x49` und verzweigt in eine gemeinsame Dispatchroutine. Diese richtet DS über den Kernel-Datenbereich ein und greift über eine Tabelle mit 4-Byte-Einträgen (Offset/Segment) auf einen indirekten Funktionszeiger zu. Die Routine bei `0x2537` berechnet den Tabelleneintrag als `AX*4 + Tabellenbasis` und ruft den Fernzeiger auf.

**Gesichert:** Dispatcher-Einstieg mit Funktionsindex `0x49`.  
**Offen:** Symbolischer Name des Index. Er wird mangels passender Symboltabelle nicht geraten.

## 2. Ziel `0000:6FD5`: Speicherblock-Zähler

Datei-Offset des Ziels: `0x75D5`. Es ruft `0x759A` auf.

Die Routine `0x759A` setzt DS auf das Kernel-Datensegment `0x0E34`, prüft BX auf Ausrichtung und einen gültigen Heapbereich, deaktiviert Interrupts und liest das Wort am Blockanfang `[BX]`. Ist dieses Wort ungleich null, erhöht sie das Byte bei `BX+0x0B` um eins. Bei Null folgt eine interne Beschaffungs-/Warte-Routine.

Der Bytezugriff `INC BYTE PTR [BX+0x0B]` ist unmittelbar belegt. Ob das Feld exakt „Lock Count“, „In-use Count“ oder anders heißt, ist ohne Strukturdefinition nicht endgültig bewiesen. Der Code gehört eindeutig in die Speicherblock-/Handle-Verwaltung, nicht in eine GEODE-Fixup-Schleife.

## 3. Ziel `0000:6EDA`: Block-/Heap-Rückgabe

Datei-Offset des Ziels: `0x74DA`. Der Pfad sichert zunächst Register und Kernel-Datenkontext, prüft BX auf Ausrichtung und einen gültigen Heapbereich und ruft `0x7B1E` auf.

`0x7B1E` aktualisiert einen Kernel-Zähler und prüft den Blockeintrag. Wenn ein Daten-Segment vorhanden ist, setzt der Code am Anfang des Datenbereichs einen `0xCCCC`-Marker, setzt Verwaltungsfelder bei `+8` und `+0x0A` auf null, addiert die Blockgröße zum freien Speicherzähler zurück und ruft eine interne Heaproutine auf. Ohne Daten-Segment folgt ein alternativer Heap-Pfad.

Das belegt einen Speicherblock-/Heap-Freigabe- bzw. Rückgabeweg. Die genaue öffentliche API-Bezeichnung bleibt offen.

## 4. Zusammenhang im Initialisierungspfad

Die Routine ab `0x10789`:

1. setzt `CS:[0x0B91]` auf null;
2. ruft `0000:0513` auf (Dispatcherindex `AX=0x49`);
3. prüft Carry;
4. speichert bei Erfolg BX in `CS:[0x0B91]`;
5. ruft `0000:6FD5` auf, wodurch `[BX+0x0B]` erhöht wird;
6. übernimmt AX als DS und setzt SI auf null.

Die Aufräumroutine bei `0x107CC` prüft `CS:[0x0B91]`; bei einem nicht-null Wert ruft sie `0000:6EDA` auf und setzt den gespeicherten Wert anschließend auf null.

Das Muster ist konsistent mit dem Beziehen eines Speicherblocks, seiner vorübergehenden Nutzung und anschließenden Rückgabe. Die exakte API-Namensgebung bleibt mangels Symboltabelle offen.

## 5. Vergleich mit zeitgenössischer Dokumentation

Der GeoWorks-Entwurf **PC/GEOS System Software Overview** vom 10.11.1990 führt im Anhang B unter Memory Management unter anderem `MemLock`, `MemUnlock`, `HandleP` und `HandleV) auf. Separat nennt er unter Geode Management `GeodeLoad`, `GeodeLoadResourceAt` und `GeodeLockResource`.

Das bestätigt die Trennung von Speicherblockverwaltung und Geode-Verwaltung in der damaligen Systemarchitektur. Es ordnet aber weder Dispatcherindex `0x49` noch die untersuchten Offsets explizit zu. Deshalb wird keine direkte Gleichsetzung mit `MemLock`/`MemUnlock` oder `GeodeLoad` behauptet.

Quelle: [PC/GEOS System Software Overview, Draft 10.11.1990 (PDF)](https://www.lyonlabs.org/commodore/onrequest/geos/PC-GEOS-System-Software-Overview.pdf), Anhang B, Seiten 51–53.

## Ergebnis

**Gesichert:**
- `0000:0513` ist ein Dispatcher-Einstieg mit `AX=0x49`.
- `0000:6FD5` erhöht nach Blockheader-Prüfung das Byte `[BX+0x0B]).
- `0000:6EDA` führt einen Block-/Heap-Rückgabeweg aus.
- Der Hilfspfad bezieht einen Block, hält ihn während der Initialisierung verfügbar und gibt ihn im Aufräumpfad zurück.
- Die Grundstruktur ist auch im deutschen `KERNEL.OLD` erkennbar, mit verschobenen Offsets und Segmentwerten.

**Nicht gesichert:**
- Symbolischer Name des Dispatcherindex `0x49).
- Exakter Name und vollständige Semantik des Zählerfeldes `+0x0B).
- GEODE-Header-Parser, Ressourcen-Tabellenleser und Fixup-Schleife.

## Änderungs- und Teststatus

- Keine Änderung am GEODE-Parser oder SDK-Code.
- Kein GEOTEST.GEO-Build und kein Laufzeittest.
- Nur statische Disassemblierung und Byteanalyse.
