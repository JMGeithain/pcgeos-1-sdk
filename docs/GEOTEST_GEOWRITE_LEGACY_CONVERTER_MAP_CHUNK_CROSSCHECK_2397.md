# GEOTEST – Abgleich GeoWrite-Konvertierungsdefinitionen mit nativer Showcase-Datei (2397)

Stand: 2026-11-11

## Fragestellung

Passen die Chunk-Konstanten aus `convertGeoWrite.def` und die Zugriffe in `convertGeoWrite.asm` unmittelbar zu den vier aktiven Chunks des nativen Dokuments `SOLAR_DE.000`?

## Quellen

Aus dem bereitgestellten Paket:
- `Source/showcase-format/public-source/convertGeoWrite.def`
- `Source/showcase-format/public-source/convertGeoWrite.asm`
- `Source/showcase-format/native_write.py`
- `Showcase/Deutsch/GeoWrite/SOLAR_DE.000`

## 1. Historischer Konvertierungscode

`convertGeoWrite.def` definiert:
- `GW12_PageContent = 22h`
- `GW12_PAGE_ARRAY_CHUNK = 22 + 4 = 26h`
- `GW12_MASTER_PAGE_ARRAY_CHUNK = 22 + 6 = 28h`
- `GW12_DOCUMENT_DATA_CHUNK = 22 + 8 = 2Ah`

`convertGeoWrite.asm` verwendet diese Konstanten im Kontext der Konvertierung:
- Zeile 82: Zugriff auf `ds:[GW12_DOCUMENT_DATA_CHUNK]`
- Zeile 150: Zugriff auf `ds:[GW12_PAGE_ARRAY_CHUNK]`
- Zeile 158: Zugriff auf `ds:[GW12_PageContent]`

Die Routine heißt `ConvertOldGeoWriteDocument`; der Quelltext beschreibt ausdrücklich die Konvertierung eines alten GeoWrite-Dokuments.

## 2. Tatsächliche LMem-Handle-Tabelle von SOLAR_DE.000

Der VM-Map-Block liegt in VM-Handle `0044h`. Seine ersten 12 Bytes lauten:

`F0 3C 18 00 00 81 02 00 6C 03 10 00`

Daraus:
- LMem-Handle-Tabelle beginnt bei `0018h`
- LMem-Blockgröße: `036Ch` (876 Byte)
- Anzahl Handle-Slots: `0010h` (16)

Die 16 Tabellenpositionen und ihre Werte:

| Chunk-Handle-Position | Tabellenwert | Befund |
|---:|---:|---|
| `18h` | `003Ah` | aktiv |
| `1Ah` | `004Eh` | aktiv |
| `1Ch` | `02CAh` | aktiv |
| `1Eh` | `032Ah` | aktiv |
| `20h` | `0000h` | leer |
| `22h` | `0000h` | leer |
| `24h` | `0000h` | leer |
| `26h` | `0000h` | leer |
| `28h` | `0000h` | leer |
| `2Ah` | `0000h` | leer |
| `2Ch`–`36h` | jeweils `0000h` | leer |

Die vier aktiven Chunk-Payloads haben nach den unmittelbar vorangestellten Längenwörtern diese Größen:
- Handle `18h`: 18 Byte
- Handle `1Ah`: 636 Byte
- Handle `1Ch`: 93 Byte
- Handle `1Eh`: 66 Byte

Hinweis zur Zählweise: Die Payload-Größe ist jeweils das Längenwort minus die zwei Bytes des Längenworts selbst.

## 3. Konsequenz

Die historischen Konstanten `26h`, `28h` und `2Ah` zeigen auf leere Slots in der LMem-Handle-Tabelle von `SOLAR_DE.000`. Damit kann die Mapblock-Struktur dieses konkreten Dokuments nicht ohne Weiteres als direkte Instanz der vom Konvertierer erwarteten alten Chunk-Anordnung behandelt werden.

Das ist kein Widerspruch zur Existenz eines nativen GeoWrite-Dokuments. Die Routine ist ausdrücklich ein Konvertierer für alte GeoWrite-Dokumente; der Quelltext darf daher nicht als vollständige Spezifikation jeder späteren bzw. anders aufgebauten nativen 1.x-Dokumentvariante verwendet werden.

## 4. Was weiterhin gilt

- `SOLAR_DE.000` hat einen echten GEOS-VM-Dateiaufbau.
- Der Dateiheader enthält `WDAT` und `WP00`.
- Der VM-Header verweist auf Map-Block-Handle `0044h`.
- Der Map-Block ist ein LMem-Block mit 16 Slots und vier aktiven Chunks.
- Der Generator `native_write.py` verändert weitere VM-Blöcke gezielt und verwendet native Artikel-, Stil- und Grafikstrukturen.
- Die konkrete Bedeutung der vier Map-Chunks ist noch nicht abschließend bestimmt.

## 5. Nächster Schritt

Die vier aktiven Map-Chunks müssen jetzt anhand der tatsächlichen GeoWrite-1.2-Programmzugriffe oder durch einen Vergleich mit dem originalen `NEW_DOCU.000`-Template aufgelöst werden. Dafür ist das Originaltemplate erforderlich; es liegt nicht unter seinem referenzierten Pfad im bereitgestellten ZIP.

Parallel ist zu prüfen, ob der Generator die Map-Chunks unverändert aus dem Template übernimmt oder einzelne davon gezielt verändert. Erst danach ist eine belastbare Zuordnung möglich.

## Status

Statische Byte- und Quellcodeprüfung. Kein Laufzeittest und keine Änderung an Originaldateien. Die vier Chunk-Größen und Tabellenwerte beziehen sich konkret auf die bereitgestellte Datei `SOLAR_DE.000`.
