# GEOTEST / GeoWorks 1.x – Geode-Header- und Ressourcentabellen-Erstaufnahme (Untersuchung 2456)

Stand: 12.11.2026  
Datenquelle: `GEOWORKS.zip`, GeoWorks 1.2.8  
Methode: statische Hex-/Byteprüfung der Originaldateien, keine Ausführung

## Dateien und Prüfsummen

| Datei | Länge | SHA-256 |
|---|---:|---|
| `GEOWORKS/SYSTEM/UI.GEO` | 87.900 Bytes | `13a3a82ec3d4373b120890a11eb09b3a9f9ec456ca633819728f53c07883c73a` |
| `GEOWORKS/WORLD/ICON-ED.GEO` | 47.648 Bytes | `afbbd1d8115c82162e8d3c9331c5d945e073e0823852bb5c68055ba6148df064` |

## Beobachtete gemeinsame Kopfstruktur

Beide Dateien beginnen mit denselben ersten vier Bytes:

`C7 45 CF 53`

Ab Dateioffset `0x100` stehen die zuvor dokumentierten Geode-Token-Kennungen:

- UI.GEO: `UI00`
- ICON-ED.GEO: `ICED`

Die Bytes bei `0xC8–0xE7` enthalten in beiden Dateien einen strukturiert wirkenden Metadatenbereich. Ein Teil der Bytes ist identisch, andere Felder unterscheiden sich. Beispiel:

| Offset | UI.GEO | ICON-ED.GEO |
|---|---|---|
| `0xCA–0xCB` | `D0 02` | `92 01` |
| `0xCC–0xCD` | `6E 02` | `6E 02` |
| `0xCE–0xCF` | `03 00` | `03 00` |
| `0xD0–0xD1` | `1C 00` | `0B 00` |
| `0xD2–0xD3` | `02 00` | `01 00` |
| `0xD4–0xD5` | `06 01` | `01 00` |

Diese Tabelle dokumentiert nur die Bytes. Ohne eine passende PC/GEOS-1.x-Strukturdefinition werden die Felder nicht als Ressourcenanzahl, Tabellenoffset, Segmentgröße oder Flags etikettiert.

## Auffällige Daten bei Offset 0x2D0

Bei beiden Dateien wurde der Bereich ab `0x2D0` hexadezimal geprüft.

UI.GEO beginnt dort mit:
`8C 05 07 00 96 02 08 00 C9 02 08 00 13 00 02 00 ...`

ICON-ED.GEO beginnt dort mit:
`61 00 61 00 06 00 04 00 2C 00 00 00 00 00 00 00 ...`

Die Inhalte unterscheiden sich deutlich. Die Werte sehen teilweise wie 16-Bit-Felder aus, aber aus dem Hexdump allein lässt sich nicht entscheiden, ob es sich um eine Ressourcenoffset-Tabelle, Relokationsdaten, eine andere Tabelle oder normalen Ressourcencode/-inhalt handelt.

**Wichtige Einschränkung:** Offset `0x2D0` wird deshalb in dieser Untersuchung ausdrücklich nicht als Ressourcentabellenanfang bestätigt. Eine belastbare Tabellenrekonstruktion erfordert zunächst eine verifizierte Definition der Felder im Geode-Header und die Validierung der referenzierten Offsets gegen tatsächliche Ressourcenanfänge.

## Was in diesem Schritt noch nicht erreicht wurde

- Keine bestätigte Ressourcenzahl.
- Kein bestätigter Beginn oder Ende der Ressourcenoffset-Tabelle.
- Keine bestätigte Zuordnung von Ressourcennummern zu Dateioffsets.
- Keine Code-Ressource disassembliert.
- Keine Icon-Provider-Dekodierroutine identifiziert.

Die früheren Dateikopfbeobachtungen (Token, Herstellerkennung, langer Name) bleiben davon unberührt.

## Nächster Schritt

Die Ressourcentabelle darf nicht durch Raten aus plausibel aussehenden Wörtern konstruiert werden. Als nächstes ist eine autoritative PC/GEOS-1.x-Geode-Headerdefinition bzw. eine passende Originaldokumentation heranzuziehen. Erst danach werden die Headerfelder dekodiert und die Tabellen-Offsets durch Quervergleich mit mehreren Dateien validiert. Anschließend kann eine reproduzierbare Ressourcentabelle für UI.GEO und ICON-ED.GEO erzeugt werden.

PC/GEOS 2.x-/FreeGEOS-Headerdefinitionen werden nicht ungeprüft als PC/GEOS 1.x-Beleg verwendet. Die Originaldateien bleiben unverändert.
