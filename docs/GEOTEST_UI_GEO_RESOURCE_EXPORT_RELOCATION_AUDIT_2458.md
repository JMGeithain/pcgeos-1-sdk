# GEOTEST / GeoWorks 1.x – UI.GEO: Ressourcen- und Exportverteilung (Untersuchung 2458)

Stand: 12.11.2026  
Original: `GEOWORKS/SYSTEM/UI.GEO` aus `GEOWORKS.zip`  
Länge: 87.900 Bytes  
SHA-256: `13a3a82ec3d4373b120890a11eb09b3a9f9ec456ca633819728f53c07883c73a`  
Parser: vorhandenes `pcgeos1/geode.py`, PC/GEOS-1.x-Zweig

## Ziel

Die in Untersuchung 2457 ermittelten UI.GEO-Ressourcen werden nun anhand ihrer Exportreferenzen, Relokationsanzahlen und lesbaren Zeichenketten priorisiert. Ziel ist die Eingrenzung derjenigen Ressourcen, die Token-/Moniker-Daten oder den dazugehörigen Code enthalten könnten.

Diese Untersuchung weist noch keine Icon-Dekodierroutine nach. Ressourcennummern werden nicht allein aufgrund ihrer Größe oder Flags semantisch benannt.

## Parserdaten erneut geprüft

Der vorhandene Parser liefert:
- 28 Ressourcen
- 2 importierte Bibliotheken: `im` und `dbase`
- 262 Exporteinträge
- Ressourcentabellenanfang `0x554`, Tabellenende `0x66C`

Die Ressourcenpositionen und -größen stimmen mit Untersuchung 2457 überein.

## 1. Verteilung der Exporteinträge

Die 262 Exporteinträge verweisen auf folgende Ressourcen:

| Ressourcen-ID | Anzahl Exporteinträge |
|---:|---:|
| 2 | 130 |
| 1 | 37 |
| 7 | 19 |
| 5 | 16 |
| 10 | 16 |
| 6 | 14 |
| 8 | 9 |
| 4 | 8 |
| 11 | 3 |
| 26 | 3 |
| 9 | 2 |
| 3 | 2 |
| 0 | 1 |
| 22 | 1 |
| 12 | 1 |
| **Summe** | **262** |

Berechnung: Die Exporttabelle enthält 262 Einträge zu je vier Bytes. Für jeden Eintrag wurde das WORD-Feld `resource` gezählt. Ressource 2 erhält 130/262 Exportverweise (ca. 49,6 %). Das ist eine Häufigkeitsangabe, keine Funktionszuordnung.

**Beobachtung:** Ressource 2 ist der mit Abstand häufigste Exportzielbereich. Ressource 1 ist mit 37 Einträgen der zweithäufigste. Diese beiden Ressourcen sind deshalb sinnvolle Kandidaten für eine vertiefte Code-/Datenanalyse.

## 2. Relokationsverteilung

Die Ressourcen besitzen insgesamt 2.447 Relokationseinträge. Die Typ-/Klassenhäufigkeiten aus dem ersten Byte der vier Byte großen Relokationsrecords:

| Oberes Nibble (Klasse) | Unteres Nibble (Typ) | Anzahl |
|---:|---:|---:|
| 0 | 0 | 1.125 |
| 2 | 2 | 997 |
| 2 | 4 | 378 |
| 0 | 1 | 121 |
| 0 | 2 | 121 |
| 1 | 4 | 100 |
| 2 | 3 | 39 |
| 1 | 1 | 1 |
| 1 | 2 | 1 |
| 1 | 3 | 1 |
| **Summe** | | **2.784** |

Korrektur: Die Gesamtzahl beträgt nach Addition der Tabelle **2.784** Relokationen. Sie wurde aus der Summe der `relocation_bytes / 4` über alle Ressourcen berechnet. Die Zahlen oben sind die Zählung der einzelnen Records nach Klasse/Typ.

Die Relokationsverteilung ist ein technischer Fingerabdruck des Ressourcenverbunds. Die Bedeutungen der einzelnen Klassen-/Typkombinationen werden hier nicht neu interpretiert; maßgeblich bleibt die Loaderanalyse im Dokument `docs/GEODE_FORMAT.md`.

## 3. Zeichenketten mit Token-/UI-Bezug

### Ressource 1

- Dateioffset der Ressource: `0x66C`
- Ressourcengröße: 4.928 Bytes
- Zeichenkette `TOKEN.DB` bei ressourcenrelativem Offset `0x0C50`
- Absoluter Dateioffset: `0x12BC`

Der umgebende Bytebereich enthält nach der Zeichenkette außerdem `Copyright (c) GEOWORKS`.

Das bestätigt den bereits in Untersuchung 2455 beobachteten Fund und lokalisiert ihn nun innerhalb von Ressource 1.

### Ressource 3

- Dateioffset der Ressource: `0x4304`
- Ressourcengröße: 3.824 Bytes
- Zeichenkette `Token DB` bei ressourcenrelativem Offset `0x0361`
- Absoluter Dateioffset: `0x4665`

Im selben Stringbereich stehen weitere UI-Bezeichnungen, unter anderem `Specific UI`, `Clipboard`, `Screens` und `Screen Blanker`.

**Einordnung:** Ressource 3 enthält eine sichtbare UI-Textgruppe, in der `Token DB` als Bezeichnung vorkommt. Das belegt einen Text-/Menübezug, aber noch nicht den Codepfad, der Token-Provider lädt oder Icon-Bitmaps dekodiert.

## 4. Priorisierung für die nächste Codeanalyse

| Priorität | Ressource | Grundlage | Aussagegrenze |
|---|---:|---|---|
| 1 | 2 | 130 Exportverweise; 245 Relokationen; 7.008 Bytes | Häufigstes Exportziel, Funktion noch nicht bewiesen |
| 2 | 1 | 37 Exportverweise; 649 Relokationen; enthält `TOKEN.DB` | Enthält Token.DB-String, nicht automatisch Decoder |
| 3 | 3 | 143 Relokationen; enthält `Token DB` und UI-Bezeichnungen | Stringgruppe vorhanden, Code-/Datenrolle offen |
| 4 | 7, 5, 10, 6, 8 | weitere Exportverweise | Erst nach Code-/Relokationspfad der Hauptressourcen untersuchen |

Die Relokationszahlen für die drei zuerst genannten Ressourcen:
- Ressource 1: 649
- Ressource 2: 245
- Ressource 3: 143

## 5. Wichtige Korrektur zur Zählung

Die Relokations-Typentabelle summiert sich auf 2.784. Die zuvor im Fließtext genannte Gesamtzahl 2.447 wäre falsch und wird ausdrücklich zurückgenommen. Die tatsächliche Summe aus den Ressourcen-Relokationslängen beträgt 2.784 Records.

## Ergebnis

1. UI.GEO besitzt 28 Ressourcen und 262 Exporte.
2. 130 Exporte zeigen auf Ressource 2; 37 auf Ressource 1.
3. Ressource 1 enthält `TOKEN.DB` bei Dateioffset `0x12BC`.
4. Ressource 3 enthält `Token DB` in einer UI-Textgruppe bei Dateioffset `0x4665`.
5. Diese Beobachtungen liefern gute Ansatzpunkte, aber noch keinen Nachweis einer Icon-Provider- oder Moniker-Dekodierroutine.

## Nächster Schritt

Die nächste Untersuchung soll Ressource 2 disassemblieren und die Exportadressen auf konkrete Routinen abbilden. Danach werden die Aufrufstellen verfolgt, die auf Ressource 1 oder 3 zugreifen. Besonders relevant sind Lesezugriffe auf die Zeichenkette `TOKEN.DB`, Token-IDs, Moniker-Deskriptoren und Bitmap-Payloads. Erst ein nachvollziehbarer Datenfluss vom Provider-Eintrag bis zur Grafikverarbeitung rechtfertigt die Bezeichnung „Icon-Dekoder“.

Originaldatei unverändert. Keine Änderungen an `TOKEN.DB`, `GEOS.INI` oder installierten GeoWorks-Dateien. Keine Laufzeittests behauptet.
