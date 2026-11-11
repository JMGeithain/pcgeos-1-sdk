# GeoWrite 1.x – Textchunk 0050h/0024h und Vergleich weiterer Dokumente (Untersuchung 2412)

## Ziel

Prüfen, ob der in `TESTWRIT.000` beobachtete Chunk `0024h` im VM-Block `0050h` Textdaten enthält, und ob weitere Originaldokumente diesen Befund stützen.

## Vorgehen und Quellen

- Binärvergleich der Originaldateien unter `/mnt/data/audit2409/` mit dem vorhandenen VM1-/LMem-Parser `/mnt/data/audit2407/vm1.py`.
- Zusätzliche Prüfung des im ZIP `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip` enthaltenen Quelltexts `Source/showcase-format/native_write.py`.
- Keine GeoWorks-Laufzeitprüfung und keine Änderung an Originaldateien.

## Befunde

### 1. Vergleich der kurzen GeoWrite-Dokumente

Bei `NEUES_DO.000`, `LEERER_B.000`, `_LEERER_.000` und `TESTWRIT.000` ist VM-Block `0050h` ein LMem-Block. Darin existiert jeweils Chunk `0024h`.

| Datei | Größe Chunk 0050h/0024h | Beobachtung |
|---|---:|---|
| `NEUES_DO.000` | 1 Byte | `00` |
| `LEERER_B.000` | 1 Byte | `00` |
| `_LEERER_.000` | 1 Byte | `00` |
| `TESTWRIT.000` | 145 Byte | Daten beginnen mit zwölf `2Ah`-Bytes; weitere Bytes sind überwiegend `2Ah` und `3Fh`; abschließendes Nullbyte |

Der Befund passt dazu, dass Chunk `0024h` bei leeren Dokumenten nur den Nullabschluss enthält und bei einem Dokument mit Inhalt wächst. Die Bytes von `TESTWRIT.000` sind aber kein normal lesbarer ASCII-Satz. Ihre konkrete Bedeutung bzw. ihr Ursprung ist damit noch nicht entschlüsselt.

### 2. Stützender Quelltext aus dem Enhanced-Colour-Paket

Die Datei `Source/showcase-format/native_write.py` enthält eine Funktion `native_encode(text)` und schreibt anschließend den erzeugten Text explizit nach:

```python
main.set(0x24, bytes(text)+b'\\0')
```

Die unmittelbar davorliegenden Zeilen bauen den Text absatzweise auf: Textbytes werden angefügt, jeder Absatz erhält ein CR-Byte (`0Dh`), und am Ende wird ein Nullbyte angehängt. Die Funktion kodiert Umlaute über eine eigene Tabelle (z. B. `ä=8Ah`, `ö=9Ah`, `ü=9Fh`, `ß=A7h`) und lässt ASCII-Zeichen unverändert.

Das ist ein direkter, konkreter Hinweis aus dem Generator des Showcase-Pakets, dass Chunk `0024h` im verwendeten GeoWrite-Dokumentmodell den fortlaufenden Textstrom enthält. Der Quelltext ist allerdings Teil des späteren Showcase-/Patch-Pakets und keine vollständige originale GeoWorks-1.x-Formatspezifikation. Er belegt daher die Verwendung in diesem Dokumentmodell, nicht automatisch jede historische Sonderform.

### 3. Weitere Datei `ERSTES_A.000`

`ERSTES_A.000` besitzt zwar ebenfalls die GEOS-/VM-Signatur, aber eine andere VM-Blockstruktur: Handles `0020h`, `0044h`, `0068h`, `008Ch` und `00B0h`; ein Block `0050h` existiert nicht. Sie ist daher kein direkt vergleichbares Beispiel für den hier untersuchten GeoWrite-Chunk. Die Dateien `KINDER.000`, `KINDERIC.000` und `NUNJA.000` tragen am erwarteten VM-Signaturfeld bei `00C8h` nicht den Wert `ADEBh`; der vorhandene VM1-Parser weist sie deshalb zu Recht nicht als dieselbe VM1-Dateistruktur aus. Sie wurden nicht als Belege für den GeoWrite-Textchunk verwendet.

## Schlussfolgerung

**Chunk `0050h/0024h` ist im vom Showcase-Generator verwendeten GeoWrite-Dokumentmodell der Textstrom-Chunk.** Das ist durch den expliziten Schreibzugriff in `native_write.py` belegt. Die drei leeren Originaldokumente mit einem einzelnen Nullbyte und `TESTWRIT.000` mit 145 Byte passen zu dieser Einordnung.

Noch offen bleibt, warum der Inhalt von `TESTWRIT.000` fast ausschließlich aus `2Ah` und `3Fh` besteht. Ohne gesicherte Herkunft bzw. eine unabhängige Dekodierung darf daraus kein konkreter Textinhalt abgeleitet werden. Ebenso ist nicht bewiesen, dass alle GeoWrite-1.x-Versionen und alle Dokumentvarianten exakt dieselbe Kodierung verwenden.

## Konsequenz für GEOTEST

- Chunk `0024h` ist ein aussichtsreicher Ansatzpunkt für den Textinhalt eines minimalen GeoWrite-Dokuments.
- Ein Generator darf nicht nur diesen Chunk ersetzen: Der Vergleich `NEUES_DO.000` gegen `TESTWRIT.000` zeigte bereits Änderungen an weiteren Chunks im Block `0050h` sowie in anderen VM-Blöcken.
- Vor einem GEOTEST-Schreibversuch müssen Text-Run-Arrays (u. a. `0026h`, `0028h`, `002Ah`), Seiten-/Objektstrukturen und VM-Relokationen zusammenhängend verstanden werden.
- Keine Originaldatei wurde verändert; kein Test in GeoWorks wurde ausgeführt.

## Reproduzierbarkeit

Untersuchungsbasis: Dateien im Arbeitsverzeichnis `/mnt/data/audit2409/`, Parser `/mnt/data/audit2407/vm1.py`, ZIP-Quelltext `Source/showcase-format/native_write.py` aus `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`.
