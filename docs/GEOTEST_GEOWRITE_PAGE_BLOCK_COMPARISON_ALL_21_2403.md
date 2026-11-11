# GeoWorks 1.x – GeoWrite-Seitenblöcke: Vollvergleich aller 21 Seiten (2403)

## Ziel und Abgrenzung

Untersucht wurde ausschließlich das native GeoWrite-Beispieldokument `Showcase/Deutsch/GeoWrite/SOLAR_DE.000` aus `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`. Die VM-Datei wurde mit dem im selben Archiv enthaltenen `Source/showcase-draw/vm1.py` gelesen. Dies ist eine statische Byte- und Strukturprüfung; GeoWorks wurde dabei nicht gestartet und das Dokument nicht im Programm geöffnet.

## Reproduzierbarer Aufbau

1. VM-Container-Signatur geprüft: Bytes `C7 45 CF 53`; VM-Signatur `ADEBh` am Containeroffset `0xC8`.
2. VM-Map-Block: Handle `0044h`.
3. Map-LMem-Chunk `001Ah): ChunkArray-Kopf `count=21`, `element size=30`; Gesamtlänge exakt `4 + 21 × 30 = 634` Bytes.
4. Aus dem ersten WORD jedes 30-Byte-Elements wurden die 21 Seiten-VM-Handles ausgelesen:
   `005C, 0380, 0398, 03B0, 03C8, 03E0, 03F8, 0410, 0428, 0440, 0458, 0470, 0488, 04A0, 04B8, 04D0, 04E8, 0500, 0518, 0530, 0548`.
5. Jeder referenzierte VM-Block existiert. Alle 21 Seitenblöcke haben 848 Bytes, VM-Flag `01FFh`, dieselbe LMem-Struktur mit 38 Handle-Slots und 18 belegten Chunks. Alle 21 Seiten besitzen exakt dieselbe Menge an Chunk-Handles:
   `0020h, 0022h, 0024h, 0026h, 0028h, 002Ah, 002Ch, 002Eh, 0030h, 0032h, 0034h, 0036h, 0038h, 003Ah, 003Ch, 003Eh, 0040h, 0042h`.

## Ergebnis des vollständigen Bytevergleichs

Gegenüber Seite 1 sind **vier** Chunk-Handles variabel. Die übrigen **14 von 18** Chunks sind auf allen 21 Seiten byteidentisch mit Seite 1. Die Aussage bezieht sich auf die vollständigen Chunk-Payloads, nicht nur auf deren Länge.

| Chunk | Länge | Veränderung gegenüber Seite 1 | Befund |
|---|---:|---|---|
| `0022h` | 104 | Payload-Offsets `0x4C` und `0x56` | Beide Bytes ändern sich synchron: Seite 1 hat `04h`; Seiten 2–21 haben `47h,49h,4Bh,...,6Dh` (ungerade Werte in Zweierschritten). |
| `0030h` | 89 | Payload-Offset `0x17` | Seite 1 `04h`; Seiten 2–21 dieselbe Folge `47h,49h,4Bh,...,6Dh` wie in Chunk `0022h`. |
| `0032h` | 28 bzw. 29 | Seitenzähler in ASCII | Enthält den sichtbaren Text `Unser Sonnensystem  |  n/21` mit abschließendem Nullbyte. Seiten 1–9 benötigen 28 Bytes; Seiten 10–21 29 Bytes, weil die Seitenzahl zweistellig wird. |
| `0042h` | 39 | Payload-Offset `0x14` | Seiten 1–9: `A1h`; Seiten 10–21: `A8h`. Alle übrigen Bytes dieses Chunks bleiben gleich. |

### Exakte Werte der beiden synchronen Felder

Für Seiten 1 bis 21 ergeben sich an den genannten Positionen in `0022h` (Offsets `0x4C` und `0x56`) sowie in `0030h` (Offset `0x17`) diese Werte:

- Seite 1: `04h`
- Seite 2: `47h`
- Seite 3: `49h`
- Seite 4: `4Bh`
- Seite 5: `4Dh`
- Seite 6: `4Fh`
- Seite 7: `51h`
- Seite 8: `53h`
- Seite 9: `55h`
- Seite 10: `57h`
- Seite 11: `59h`
- Seite 12: `5Bh`
- Seite 13: `5Dh`
- Seite 14: `5Fh`
- Seite 15: `61h`
- Seite 16: `63h`
- Seite 17: `65h`
- Seite 18: `67h`
- Seite 19: `69h`
- Seite 20: `6Bh`
- Seite 21: `6Dh`

## Bedeutung und Grenzen der Interpretation

- Der 30-Byte-Eintrag im PageArray verweist nachweislich über sein erstes WORD auf einen existierenden Seiten-VM-Block. Das stützt die Zuordnung der Array-Elemente zu den 21 Seiten.
- Chunk `0032h` ist durch den lesbaren, fortlaufenden Text eindeutig als sichtbare Seitenangabe identifizierbar.
- Die parallelen Änderungen in `0022h` und `0030h` sind bytegenau belegt. **Ihre semantische Bedeutung ist noch nicht geklärt.** Insbesondere werden die Werte nicht als VM-Handles, Seiten-IDs oder Objekt-IDs bezeichnet, solange keine Code- oder Laufzeitreferenz dies belegt.
- Chunk `0042h` weist einen klaren Seitenbereichswechsel zwischen Seite 9 und Seite 10 auf. **Die Bedeutung des Bytes `A1h/A8h` ist unbekannt.** Der Wechsel könnte mit der zweistelligen Seitenzahl zusammenhängen, aber der Bytevergleich allein beweist das nicht.
- Die zuvor untersuchten Seiten 1–6 zeigten nur die ersten drei variablen Chunks. Der Vollvergleich deckt zusätzlich auf, dass Chunk `0042h` ab Seite 10 variiert und dass Chunk `0032h` ab Seite 10 um ein Byte wächst. Die frühere Beobachtung war für die ersten sechs Seiten korrekt, aber nicht vollständig für das gesamte Dokument.

## Konsequenz für GEOTEST

Für einen minimalen nativen GeoWrite-Dokumentgenerator ist es nicht ausreichend, nur die Seitenzahl in Chunk `0032h` zu ändern. Das Originaldokument zeigt mindestens drei weitere seitenabhängige Payload-Felder (zwei in `0022h`, eines in `0030h`) sowie den Seitenbereichswechsel in `0042h`. Vor einer Übernahme dieser Struktur in GEOTEST müssen die Feldbedeutungen durch Quellcode-/Disassemblierungsreferenzen oder kontrollierte GeoWrite-Erzeugung geklärt werden.

**Empfohlener nächster Schritt (2404):** Die Chunks `0022h`, `0030h` und `0042h` in den GeoWrite-Quellen bzw. im historischen Konverter nach konkreten Zugriffen, Felddefinitionen und Schreibstellen suchen. Dabei zuerst die exakten Bytes/Offsets mit den Quelltext-Konstanten und Strukturen abgleichen; keine Bedeutung aus den Zahlenmustern ableiten.

## Prüfumfang / Reproduzierbarkeit

- Archiv: `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`
- Eingabedatei: `Showcase/Deutsch/GeoWrite/SOLAR_DE.000`
- Parser: `Source/showcase-draw/vm1.py`
- Geprüfte Seiten: 21 von 21 referenzierten Seiten-VM-Blöcken
- Vergleich: Chunk-Handle-Mengen, Chunk-Längen und vollständige Payload-Bytes
- Ergebnis: 21 vorhandene Seitenblöcke; 18 Chunks je Seite; 4 variable und 14 durchgehend identische Chunks
- Nicht durchgeführt: Laufzeittest in GeoWorks, Öffnen/Speichern des Dokuments, Veränderung der Originaldatei
