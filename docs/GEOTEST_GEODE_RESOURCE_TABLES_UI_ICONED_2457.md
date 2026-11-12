# GEOTEST / GeoWorks 1.x – Korrigierte Geode-Ressourcentabellen für UI.GEO und ICON-ED.GEO (Untersuchung 2457)

Stand: 12.11.2026  
Datenquelle: `GEOWORKS.zip`, GeoWorks 1.2.8  
Parserquelle: `pcgeos1/geode.py` im Repository `JMGeithain/pcgeos-1-sdk`  
Methode: unveränderte Anwendung des vorhandenen, bounds-geprüften SDK-Parsers auf die Originaldateien

## Wichtige Korrektur zu Untersuchung 2456

Die vorherige Untersuchung 2456 stellte fest, dass die Ressourcentabellen noch nicht bestimmt seien und eine Headerdefinition erst gesucht werden müsse. Das war ein Fehler in der Projektfortführung: Im Repository waren die PC/GEOS-1.x-Headerstruktur und der Parser bereits dokumentiert bzw. implementiert.

Die maßgebliche Datei ist:

- `docs/GEODE_FORMAT.md`
- Parser: `pcgeos1/geode.py`

Die Parserdokumentation unterscheidet ausdrücklich:
- PC/GEOS 1.x: Signatur `C7 45 CF 53`, Headerbeginn bei Dateioffset 200 (`0xC8`), Ressourcenpositionen absolut.
- PC/GEOS 2.x: andere Signatur `C7 45 C1 53`, Headerbeginn 256 und andere Positionsbehandlung.

Für diese Untersuchung wurden ausschließlich die 1.x-Dateien mit Signatur `C7 45 CF 53` verarbeitet. Die PC/GEOS-2.x-Regeln wurden nicht angewendet.

## Parserregeln für die Ressourcentabelle

Aus dem vorhandenen Parser ergeben sich für 1.x:

- Geode-Header beginnt bei `h = 0xC8`.
- Importtabelle beginnt bei `h + 88`.
- Jeder Importeintrag ist 14 Bytes lang.
- Exporttabelle folgt auf die Importtabelle; jeder Exporteintrag ist 4 Bytes lang.
- Ressourcentabelle folgt auf die Exporttabelle.
- Jeder Ressourceneintrag belegt 10 Bytes:
  - alle Ressourcengrößen als WORD-Tabelle,
  - danach Dateipositionen als DWORD-Tabelle,
  - danach Relokationsgrößen als WORD-Tabelle,
  - danach Ressourcenflags als WORD-Tabelle.

Die Berechnung des Tabellenanfangs lautet:

`resource_at = h + 88 + 14 * import_count + 4 * export_count`

Das Tabellenende ist:

`table_end = resource_at + 10 * resource_count`

Diese Formeln sind keine neue Vermutung dieser Untersuchung; sie sind die bereits im SDK-Parser implementierte und mit mehreren Dateien verwendete Struktur.

## UI.GEO

Original:
- Pfad im Archiv: `GEOWORKS/SYSTEM/UI.GEO`
- Länge: 87.900 Bytes
- SHA-256: `13a3a82ec3d4373b120890a11eb09b3a9f9ec456ca633819728f53c07883c73a`
- Signatur: `C7 45 CF 53`
- Headerbeginn: `0xC8`

Vom Parser gelesene Zähler:
- Ressourcen: 28
- Imports: 2
- Exports: 262

Tabellenanfang:
- `0xC8 + 0x58 + 2*14 + 262*4 = 0x554`

Tabellenende:
- `0x554 + 28*10 = 0x66C`

Die Ressourcentabelle ist damit auf `0x554–0x66B` (Ende exklusiv `0x66C`) abgegrenzt.

### UI.GEO – Ressourcenliste

Dateioffsets sind absolut.

| Ressource | Größe | Dateioffset | Relokationsbytes | Flags |
|---:|---:|---:|---:|---:|
| 0 | 0 | `0x0066C` | 0 | `0x0880` |
| 1 | 4928 | `0x0066C` | 2596 | `0x0080` |
| 2 | 7008 | `0x023D0` | 980 | `0x0A80` |
| 3 | 3824 | `0x04304` | 572 | `0x0A62` |
| 4 | 1856 | `0x05430` | 188 | `0x0A72` |
| 5 | 3456 | `0x05C2C` | 512 | `0x0A72` |
| 6 | 2480 | `0x06BAC` | 396 | `0x0A72` |
| 7 | 4064 | `0x076E8` | 828 | `0x0A72` |
| 8 | 3440 | `0x08A04` | 716 | `0x0A72` |
| 9 | 1216 | `0x09A40` | 324 | `0x0A72` |
| 10 | 5568 | `0x0A044` | 752 | `0x0A72` |
| 11 | 17408 | `0x0B8F4` | 724 | `0x0A72` |
| 12 | 704 | `0x0FFC8` | 120 | `0x0A72` |
| 13 | 112 | `0x10300` | 40 | `0x0A72` |
| 14 | 1088 | `0x10398` | 424 | `0x0A72` |
| 15 | 384 | `0x10980` | 80 | `0x0A72` |
| 16 | 944 | `0x10B50` | 248 | `0x0A72` |
| 17 | 32 | `0x10FF8` | 20 | `0x0A72` |
| 18 | 352 | `0x1102C` | 52 | `0x0A72` |
| 19 | 2256 | `0x111C0` | 392 | `0x0A72` |
| 20 | 560 | `0x11C18` | 32 | `0x0A72` |
| 21 | 4656 | `0x11E68` | 900 | `0x0A72` |
| 22 | 5120 | `0x1341C` | 300 | `0x0A72` |
| 23 | 1472 | `0x14948` | 280 | `0x0A72` |
| 24 | 800 | `0x15020` | 8 | `0x0A72` |
| 25 | 112 | `0x15348` | 0 | `0x0A72` |
| 26 | 256 | `0x153B8` | 48 | `0x0A72` |
| 27 | 624 | `0x154E8` | 4 | `0x1C7A` |

## ICON-ED.GEO

Original:
- Pfad im Archiv: `GEOWORKS/WORLD/ICON-ED.GEO`
- Länge: 47.648 Bytes
- SHA-256: `afbbd1d8115c82162e8d3c9331c5d945e073e0823852bb5c68055ba6148df064`
- Signatur: `C7 45 CF 53`
- Headerbeginn: `0xC8`

Vom Parser gelesene Zähler:
- Ressourcen: 11
- Imports: 1
- Exports: 1

Tabellenanfang:
- `0xC8 + 0x58 + 1*14 + 1*4 = 0x132`

Tabellenende:
- `0x132 + 11*10 = 0x1A0`

Die Ressourcentabelle ist damit auf `0x132–0x19F` (Ende exklusiv `0x1A0`) abgegrenzt.

### ICON-ED.GEO – Ressourcenliste

| Ressource | Größe | Dateioffset | Relokationsbytes | Flags |
|---:|---:|---:|---:|---:|
| 0 | 0 | `0x00000` | 0 | `0x0880` |
| 1 | 13040 | `0x001A0` | 180 | `0x0080` |
| 2 | 25088 | `0x03544` | 284 | `0x0A72` |
| 3 | 320 | `0x09860` | 4 | `0x087A` |
| 4 | 448 | `0x099A4` | 4 | `0x145A` |
| 5 | 6432 | `0x09B68` | 4 | `0x145A` |
| 6 | 320 | `0x0B48C` | 4 | `0x145A` |
| 7 | 128 | `0x0B5D0` | 4 | `0x041A` |
| 8 | 144 | `0x0B654` | 4 | `0x1C7A` |
| 9 | 224 | `0x0B6E8` | 4 | `0x1C7A` |
| 10 | 592 | `0x0B7CC` | 4 | `0x1C7A` |

## Vergleich mit DESKTOPG.GEO als Kontrollprobe

Zur Gegenprüfung wurde derselbe Parser zusätzlich auf die bereits untersuchte GeoWorks-1.x-Datei `DESKTOPG.GEO` angewendet. Er liefert:
- Ressourcen: 51
- Imports: 1
- Exports: 15
- Ressourcentabellenanfang: `0x16A`
- Tabellenende: `0x368`

Das passt zu den bereits zuvor verwendeten absoluten Dateioffsets der Ressourcen 39, 40, 41 und 50. Insbesondere meldet der Parser für Ressource 40 den Dateioffset `0x14FD0` und für Ressource 41 `0x16024`, wie in den früheren Bitmap-Untersuchungen verwendet.

## Validierungen

Der verwendete Parser prüft unter anderem:
- GEOS-1.x-Signatur und Mindestlänge,
- doppelt gespeicherte Zählerfelder,
- Grenzen der Tabellen,
- Ressourcengrößen und absolute Dateipositionen,
- Relokationsgrößen auf Vierbyte-Ausrichtung,
- Grenzen der Ressourcendaten und Relokationstabellen,
- Überlappungen von Ressourcenspannen,
- Export-Ressourcenindizes,
- Relokationsziele und Importindizes.

Alle drei Dateien wurden ohne Parserfehler eingelesen. Das ist eine erfolgreiche statische Strukturvalidierung gegen die Regeln des vorhandenen SDK-Parsers; es ist kein Laufzeittest des GeoWorks-Kernels.

## Korrektur des vorigen Dossiers

Die Aussage in Untersuchung 2456, dass keine Ressourcenzahl und kein Ressourcentabellenanfang bestätigt seien, ist für UI.GEO und ICON-ED.GEO zurückzunehmen. Die Werte sind mit dem vorhandenen Parser nun bestimmt.

Der frühere Befund, dass `0x2D0` kein Tabellenanfang sei, bleibt bestehen: Für UI.GEO liegt die Ressourcentabelle bei `0x554`, für ICON-ED.GEO bei `0x132`.

## Nächster Schritt

Jetzt kann gezielt mit Ressourcen statt mit willkürlichen Dateioffsets gearbeitet werden. Für die Icon-Verarbeitung ist als nächstes:
1. UI.GEO-Ressourcen anhand ihrer Flags und Relokationen zu klassifizieren;
2. ICON-ED.GEO-Ressourcen 1 und 2 zunächst als große Kandidaten für Code-/Datenressourcen zu untersuchen, ohne ihre Funktion allein aus der Größe abzuleiten;
3. nach Token-/Moniker-/Bitmap-Referenzen zu suchen und deren Relokationsziele in den Ressourcen zu verfolgen;
4. die Ergebnisse mit den bereits dekodierten DESKTOPG.GEO-Monikerressourcen zu vergleichen.

Originaldateien wurden nicht verändert. Keine Produktions-TOKEN.DB oder GEOS.INI wurde angefasst. Kein Laufzeiterfolg wird behauptet.
