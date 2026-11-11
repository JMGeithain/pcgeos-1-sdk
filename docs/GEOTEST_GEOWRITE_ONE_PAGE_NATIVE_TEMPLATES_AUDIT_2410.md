# GeoWrite 1.x – Einseitige native Vorlagen aus GEOWORKS.zip (Untersuchung 2410)

## Ziel

Nachdem die Strukturdefinitionen `VCI_comp` und `VI_link` im Patch-Archiv nicht vorhanden waren, wurde die Originalinstallation `GEOWORKS.zip` nach tatsächlich ausgelieferten GeoWrite-Dokumenten durchsucht. Besonders relevant sind die kleinen einseitigen Vorlagen und ein kleines Testdokument.

Die Untersuchung ist strikt auf GeoWorks 1.x ausgerichtet. Die analysierten Dateien tragen im GEOS-Dateikopf die Dokumenttokens `WDAT` und `WP00`.

## Untersuchte Dateien

| Datei | Größe | Titel im Dateikopf | Dokumenttoken | App-Token |
|---|---:|---|---|---|
| `GEOWORKS/DOCUMENT/NEUES_DO.000` | 2.352 Bytes | Neues Dokument | `WDAT` | `WP00` |
| `GEOWORKS/DOCUMENT/BRIEFE/LEERER_B.000` | 2.352 Bytes | Leerer Brief | `WDAT` | `WP00` |
| `GEOWORKS/DOCUMENT/BEWERBGN/_LEERER_.000` | 2.448 Bytes | Leerer Bewerbungsbrief | `WDAT` | `WP00` |
| `GEOWORKS/DOCUMENT/TESTWRIT.000` | 2.752 Bytes | testwrite | `WDAT` | `WP00` |

Die Dateien wurden aus `GEOWORKS.zip` extrahiert und mit dem VM1-/LMem-Leser `vm1.py` aus dem Enhanced-Colour-Archiv statisch untersucht.

## Gemeinsame Struktur der einseitigen Dokumente

Alle vier untersuchten Dokumente haben:
- GEOS-Signatur `C7 45 CF 53`
- VM-Signatur `ADEBh` am VM-Header
- Map-VM-Handle `0044h`
- einen Page-Array-Chunk bei Map-LMem-Chunkhandle `001Ah`
- genau einen Page-Array-Eintrag
- Elementgröße 30 Bytes
- Seiten-VM-Handle `005Ch`
- einen Seitenblock von 928 Bytes
- dieselben 18 belegten LMem-Chunks im Seitenblock.

Die 18 Seitenblock-Chunks sind:
`0020h, 0022h, 0024h, 0026h, 0028h, 002Ah, 002Ch, 002Eh, 0030h, 0032h, 0034h, 0036h, 0038h, 003Ah, 003Ch, 003Eh, 0040h, 0042h`.

## VM-Blöcke und Dateigröße

`NEUES_DO.000`, `LEERER_B.000` und `TESTWRIT.000` besitzen jeweils acht belegte VM-Blöcke:
- `0020h`: 240-Byte-Block
- `002Ch`: 96-Byte-LMem-Block
- `0038h`: 80-Byte-LMem-Block
- `0044h`: 288-Byte-LMem-Mapblock
- `0050h`: 480-Byte-LMem-Block
- `005Ch`: 928-Byte-LMem-Seitenblock
- `0068h`: 48-Byte-LMem-Block
- `0074h`: 48-Byte-LMem-Block

`_LEERER_.000` besitzt ebenfalls acht belegte VM-Blöcke, aber größere Verwaltungsblöcke:
- `002Ch`: 160 Bytes
- `0038h`: 112 Bytes
- `0044h`: 288 Bytes
- `0050h`: 480 Bytes
- `005Ch`: 928 Bytes
- `0068h`: 48 Bytes
- `0074h`: 48 Bytes
- zusätzlich `0020h`: 176 Bytes

## Seitenarray

Der Seitenarray-Chunk `001Ah` beginnt in allen vier Dateien mit:
- Count = 1
- Elementgröße = 30 (`001Eh`)
- erstes WORD des Elements = `005Ch` (Seiten-VM-Handle)

Damit liegt eine echte, kleine, einseitige GeoWrite-Dateistruktur vor. Dies ist ein wesentlich besserer Minimalvergleich als die 21-seitige Showcase-Datei `SOLAR_DE.000`.

## Seitenblock – wichtige Struktur

Der 928-Byte-Seitenblock `005Ch` enthält in allen vier Dokumenten dieselben 18 belegten Chunkhandles. Besonders relevant:
- `0022h`: 104 Bytes (PageContent / visueller Seiteninhalt, siehe Untersuchungen 2405–2409)
- `0024h`: 89 Bytes (Objekt-/Seiteninhaltstruktur; genaue Semantik hier nicht neu zugeordnet)
- `0026h`: 1 Byte
- `0028h`, `002Ah`: je 18 Bytes
- `002Ch`: 14 Bytes
- `0030h`: 89 Bytes
- `0032h`: 1 Byte
- `0034h`, `0036h`: je 18 Bytes
- `0038h`: 14 Bytes
- `003Ch`, `0040h`: je 10 Bytes
- `003Eh`, `0042h`: je 143 Bytes.

Die beiden Seiten-Selbstreferenzen in Chunk `0022h` und die Selbstreferenz in Chunk `0030h` haben in diesen Dokumenten ebenfalls den Wert `7004h`. Die zugehörige Seite ist VM-Handle `005Ch`; der Index `004h` löst über die 12-Byte-VM-Blocktabelleneinträge auf den eigenen Seitenblock auf.

## Unterschied zwischen leerer Vorlage und Testdokument

`NEUES_DO.000` und `LEERER_B.000` besitzen dieselbe Dateigröße und denselben grundlegenden VM-/Seitenblockaufbau, unterscheiden sich aber in Dokumenttitel, Seiteneinstellungen, Positionen/Größenfeldern und weiteren Seiteninhalten. `TESTWRIT.000` besitzt dieselbe VM-Block- und Seitenblockgröße, enthält aber zusätzliche Text-/Formatierungsdaten und ist 400 Bytes größer als `NEUES_DO.000`.

`_LEERER_.000` hat einen größeren Verwaltungsbereich und ist damit kein identischer Ersatz für die beiden 2.352-Byte-Dateien.

## Bedeutung für GEOTEST.GEO

Dies ist der bisher stärkste Kandidat für eine belastbare Ausgangsbasis:
- `NEUES_DO.000` ist eine originale, einseitige GeoWrite-Datei aus der GeoWorks-1.x-Installation und trägt den Titel „Neues Dokument“.
- Sie enthält bereits die vollständige minimale Ein-Seiten-VM-/LMem-Struktur, inklusive Mapblock, Page Array und Seitenobjekt-Chunks.
- Ein Generator könnte konzeptionell mit einer Kopie dieser Struktur beginnen und gezielt Text-/Metadatenbereiche ändern. Vorher muss aber geklärt werden, welche Chunks und Relokationen bei jeder Änderung konsistent angepasst werden müssen.

Die Datei wurde in dieser Untersuchung nur gelesen. Es wurde keine Vorlage verändert, keine neue GEOS-Datei geschrieben und kein Laufzeittest in GeoWrite durchgeführt. Daher ist `NEUES_DO.000` ein verifizierter Strukturvergleich, noch keine bestätigte Generatorvorlage.

## Quellen und Grenzen

- `GEOWORKS.zip`: die vier oben genannten Originaldokumente.
- `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`: `Source/showcase-draw/vm1.py`.
- Statische Auswertung der GEOS-Dateiköpfe, VM-Header, VM-Blocktabellen, Map-LMem- und Seiten-LMem-Strukturen.

Die fehlenden Klassendefinitionen für `VCI_comp` und `VI_link` werden durch diese Dokumente nicht automatisch ersetzt. Die Untersuchung liefert reale native Vergleichsdateien, aber keine vollständige Quellcode-ABI-Spezifikation.
