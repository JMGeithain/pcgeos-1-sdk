# GEOTEST / ICONMAKE – HGC-Payload-Byte-Audit (Untersuchung 2452)

Stand: 12.11.2026  
Repository: `JMGeithain/pcgeos-1-sdk`

## Fragestellung

Untersucht wird der Bereich unmittelbar nach dem HGC-Icon-Descriptor in den ICONMAKE-Testprovidern `GTI1FFFE.000` und `GTI2FFFD.000`. Ziel ist, die Grenzen und Byte-Eigenschaften des Bereichs mit den Originalprovidern `GDOC.000` und `PAPR.000` sowie den extrahierten HGC-PCX-Dateien zu vergleichen.

## Datenbasis

- `GTI1FFFE.000`: 2256 Bytes
- `GTI2FFFD.000`: 2208 Bytes
- `GDOC_HGC.PCX`: 48 × 30 Pixel, monochrom (1 Bit/Pixel)
- `PAPR_HGC.PCX`: 48 × 30 Pixel, monochrom (1 Bit/Pixel)
- Originalprovider aus `GEOWORKS/ICONS/GDOC.000` und `GEOWORKS/ICONS/PAPR.000` im bereitgestellten `GEOWORKS.zip`

Die PCX-Dateien liegen im Arbeitsverzeichnis mit dem vom Upload erzeugten Suffix `(1)`; der Suffix ist nicht Teil des ursprünglichen Dateinamens.

## Descriptor und untersuchte Grenzen

Der HGC-Descriptor beginnt bei absolutem Datei-Offset `0x494` und ist 64 Bytes lang. Der nächste Descriptor beginnt bei:

- GDOC/GTI1: `0x598`
- PAPR/GTI2: `0x5A8`

Daraus ergeben sich die verglichenen Nachfolgebereiche:

| Provider | Start | Ende exklusiv | Länge |
|---|---:|---:|---:|
| GDOC / GTI1 | `0x4D4` | `0x598` | 196 Bytes |
| PAPR / GTI2 | `0x4D4` | `0x5A8` | 212 Bytes |

Diese Grenzen sind durch die Descriptor-Positionen definiert. Die Bezeichnung „Payload-Bereich“ ist hier eine Arbeitsbezeichnung; sie beweist für sich allein weder ein bestimmtes Kompressionsverfahren noch eine konkrete interne Datenstruktur.

## Byteweiser Vergleich mit den Originalprovidern

### GDOC / GTI1

- Bereichslänge: 196 Bytes
- Bytes an relativen Indizes 0 bis 181: identisch
- Abweichungen: relative Indizes 182 und 183, entsprechend absoluten Offsets `0x58A` und `0x58B`
- Im Original stehen dort `CC CC`; im GTI1-Testprovider stehen dort `00 00`.
- Die verbleibenden Bytes stimmen wieder überein.

SHA-256 des gesamten GTI1-Bereichs `0x4D4–0x597`:
`6bfedbb5957cfa36a3918d18ceec97fb6b21059b7414cd0218b3f6104e34c4f3`

### PAPR / GTI2

- Bereichslänge: 212 Bytes
- Bytes an relativen Indizes 0 bis 204: identisch
- Abweichungen: relative Indizes 205 bis 207, entsprechend absoluten Offsets `0x5A1–0x5A3`
- Im Original stehen dort `CC CC CC`; im GTI2-Testprovider stehen dort `00 00 00`.
- Die verbleibenden Bytes stimmen wieder überein.

SHA-256 des gesamten GTI2-Bereichs `0x4D4–0x5A7`:
`2ebf5e334544568cd6ac028d942d119102990d1cd857ba3f027984b534ec921b`

**Korrektur/Präzisierung gegenüber einer pauschalen Kopierannahme:** Die HGC-Bereiche wurden nicht vollständig byteidentisch übernommen. Die Abweichungen sind auf die oben genannten abschließenden Bytes begrenzt. Aus dem Vergleich allein lässt sich nicht bestimmen, warum ICONMAKE diese Bytes auf Null setzt.

## Vergleich mit den extrahierten PCX-Bitmapdaten

Beide HGC-PCX-Dateien dekodieren zu 48 × 30 monochromen Pixeln. Bei einer zeilenweisen Packung mit 6 Bytes pro Zeile entstehen jeweils 180 Bytes:

- GDOC-HGC gepackte Pixelmatrix SHA-256: `306495fc5dd5f7e7ee97dd78d69e70a86f543ec447b58816450cbde549b2368b`
- PAPR-HGC gepackte Pixelmatrix SHA-256: `70cd9b1fb57999cd0142d3290e261b224e4a202b5b9484008fc3fdb26fad5fa9`

Die folgenden direkten Varianten wurden geprüft: normale Bitreihenfolge (MSB zuerst), invertierte Bits, umgekehrte Bitreihenfolge innerhalb jedes Bytes sowie Kombination aus Umkehrung und Invertierung. Keine dieser 180-Byte-Folgen liegt als zusammenhängende Bytefolge im jeweils untersuchten Providerbereich.

Damit ist lediglich ausgeschlossen, dass die getestete einfache Packung unverändert als zusammenhängender Block im Bereich abgelegt ist. Nicht ausgeschlossen sind andere Packungsarten, zeilenweise Kodierung, RLE, Delta-Kodierung, Steuerbytes oder eine andere interne Darstellung.

## Sichtbare Byte-Muster

Im GDOC-HGC-Bereich treten wiederholt Sequenzen wie `FD FF` sowie Muster mit `00 70`, `05 0E` und `38 EE` auf. Im PAPR-HGC-Bereich ist die Bytefolge deutlich anders strukturiert und enthält unter anderem wiederkehrende Teilfolgen mit `05` als führendem Byte.

Diese Beobachtungen sind reine Byte-Befunde. Eine Bedeutung als Zeilenende, Wiederholungsbefehl, Lauflänge oder Pixelcode ist bislang **nicht nachgewiesen**.

## Ergebnis

1. Die Descriptor-Grenzen und die Längen der beiden HGC-Nachfolgebereiche sind bestimmt.
2. Die Testprovider stimmen im HGC-Bereich fast vollständig mit ihren jeweiligen Originalprovidern überein; die konkreten Abweichungen sind zwei bzw. drei aufeinanderfolgende `CC`-Bytes, die in den Testprovidern als Nullbytes erscheinen.
3. Eine direkte 180-Byte-Bitmapablage in den getesteten einfachen Bitvarianten wurde nicht gefunden.
4. Das HGC-Datenformat ist weiterhin nicht dekodiert. Insbesondere werden keine Aussagen über die Semantik einzelner Steuerbytes getroffen.

## Nächster sinnvoller Untersuchungsschritt

CGA- und HGC-Bereiche sollten anhand der wiederkehrenden Bytefolgen und ihrer Unterschiede systematisch gegenübergestellt werden. Danach ist gezielt nach einer Dekodier-/Render-Routine oder einer Formatbeschreibung in den mitgelieferten ICONMAKE-Unterlagen bzw. im GeoWorks-1.x-Codebestand zu suchen. Bis eine solche Routine nachvollziehbar rekonstruiert ist, darf keine eigene Interpretation der Bytes als bestätigtes Format dokumentiert werden.
