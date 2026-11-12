# GEOTEST – TOKEN.DB: systematische Erfassung der 74-00-Datensatzkandidaten (2425)

Stand: 2026-11-12  
Geltungsbereich: originales GeoWorks / PC/GEOS 1.x; statische Rohdatenanalyse.  
Datei: `GEOWORKS/SYSTEM/TOKEN.DB`  
Größe: 952.688 Byte  
SHA-256: `c7fa3d51c9bdce14b988d20fd8ed57ac7da9837803090ac858990613ec53ae35`

## 1. Korrektur und Methode

Ausgangspunkt ist der in Untersuchung 2424 beschriebene wiederkehrende Aufbau:

```
4 ASCII-Bytes (Tokenkandidat)
2 Bytes Herstellerkennung
74 00
2 Bytes Kennwert
```

Für diese Untersuchung wurde der komplette VM-Block `0080h` (Dateioffset `DAB50h`, 56.864 Byte) nach genau dieser Bytefolge durchsucht. Als Herstellerwörter wurden zunächst nur `0000h` und `00FFh` akzeptiert. Die ersten vier Bytes mussten druckbare ASCII-Zeichen aus dem Bereich A–Z, a–z oder 0–9 sein.

Das Verfahren findet **528 syntaktische Kandidaten**. Diese Zahl ist ausdrücklich keine Anzahl bestätigter Tokenregistrierungen: Spätere Bereiche enthalten auch eingebettete Zeichenfolgen und andere Daten, die zufällig dieselbe Byteform besitzen können.

## 2. Bestätigte regelmäßige Folge im frühen Tabellenbereich

Im Bereich ab Blockoffset `0060h` stehen die folgenden generischen und anwendungsspezifischen Einträge:

| Blockoffset | Token | Herstellerwort | Kennwert |
|---:|---|---:|---:|
| `0060h` | `DESK` | 0 | `000Eh` |
| `0092h` | `FLDR` | 0 | `0012h` |
| `00ACh` | `FILE` | 0 | `0016h` |
| `00C6h` | `gAPP` | 0 | `001Ah` |
| `00E0h` | `gDAT` | 0 | `001Eh` |
| `00FAh` | `gDOS` | 0 | `0022h` |
| `0114h` | `GBNR` | 0 | `0026h` |
| `013Eh` | `TERM` | 0 | `002Ah` |
| `0158h` | `ADBK` | 0 | `002Eh` |
| `0172h` | `adbk` | 0 | `0032h` |
| `018Ch` | `DP00` | 0 | `0036h` |
| `01AEh` | `DDAT` | 0 | `003Ah` |
| `01C8h` | `PLNR` | 0 | `003Eh` |
| `01E2h` | `plnr` | 0 | `0042h` |
| `01FCh` | `WP00` | 0 | `0046h` |
| `0216h` | `WDAT` | 0 | `004Ah` |
| `0238h` | `NPAD` | 0 | `004Eh` |
| `0252h` | `VIEW` | 0 | `0052h` |
| `026Ch` | `VWQ1` | 0 | `0056h` |
| `0286h` | `VEPS` | 0 | `005Ah` |
| `02A0h` | `VWK1` | 0 | `005Eh` |

Die Kennwerte steigen in dieser Folge jeweils um `0004h`. Die Abstände zwischen den Tokenanfängen sind dagegen nicht überall gleich: häufig `001Ah`, aber z.B. auch `0022h` oder `0032h`. Daher ist die Folge nicht als starres Array gleich großer Datensätze zu beschreiben.

## 3. Provider-Tokens im späteren Abschnitt

Im Abschnitt mit Herstellerkennung 255 finden sich u.a.:

| Blockoffset | Token | Herstellerwort | Kennwert |
|---:|---|---:|---:|
| `08C2h` | `BEER` | 255 | `0160h` |
| `08DCh` | `BILL` | 255 | `0164h` |
| `08F6h` | `BKUP` | 255 | `0168h` |
| `0910h` | `BUTN` | 255 | `016Ch` |
| `0A58h` | `gDOC` | 255 | `019Ch` |
| `0BF6h` | `PAPR` | 255 | `01DCh` |
| `0D84h` | `ZIPR` | 255 | `0218h` |

Auch hier steigen die Kennwerte in vielen aufeinanderfolgenden Einträgen um vier. Die Herstellerkennung und das Token sind direkt im Rohdatenstrom lesbar. Die Daten nach dem Kennwert unterscheiden sich stark und können nicht ohne Formatkenntnis als Pixel-, Moniker- oder Zeigerdaten klassifiziert werden.

## 4. Auffällige Abweichungen und Grenzen

1. **Variable Abstände:** Die Kandidaten liegen nicht alle in einem festen 26-Byte-Raster. Einzelne Bereiche haben zusätzliche Bytes oder andere Daten zwischen den Einträgen.
2. **Eingebettete Treffer:** Im Block gibt es auch spätere Vorkommen, bei denen eine druckbare Viererfolge und `74 00` innerhalb anderer Daten auftauchen. Sie sind zunächst nur syntaktische Treffer.
3. **Herstellerfeld:** `0000h` und `00FFh` sind in den Beispielen konsistent, aber die Suche allein beweist nicht, dass alle anderen Herstellerwerte ausgeschlossen sind.
4. **Kennwert:** Die fortlaufenden Werte im Abstand vier sehen wie IDs/Indizes aus. Ihre Semantik bleibt unbewiesen.
5. **Iconverweis:** Kein Kandidat wird allein aufgrund seiner Kennwertnähe einem bestimmten Moniker-VM-Block zugeordnet.

## 5. Ergebnis

Die Untersuchung bestätigt eine umfangreiche Folge von Token-/Hersteller-/Kennwertstrukturen innerhalb des VM-Blocks. Besonders belastbar ist die frühe Folge von `DESK` bis `VWK1` sowie die Providerfolge ab `BEER`. Die Kennwerte sind geordnet, die Datensatzabstände aber variabel.

Die Analyse liefert damit eine bessere Grundlage zur Rekonstruktion des TOKEN.DB-Formats, aber noch keinen nachgewiesenen Token-zu-Icon-Zeiger.

## 6. Nächster Schritt (2426)

1. Die Struktur der ersten Einträge `DESK`, `FLDR`, `FILE`, `gAPP`, `gDAT`, `gDOS` mit den späteren Einträgen vergleichen.
2. Die Bytefelder nach dem Kennwert in Gruppen nach Datenlänge und Muster klassifizieren.
3. Die tatsächlichen Datensatzgrenzen anhand der jeweils nächsten Einträge bestimmen.
4. Den Kennwert gegen die VM-Blockhandles bzw. die Icon-Monikerblöcke prüfen, aber nur dann als Verweis benennen, wenn die Referenzregeln dies bestätigen.
5. Die TOKEN.DB unverändert lassen.

## 7. Reproduzierbarkeit und Sicherheit

Die Suche erfolgte in der unveränderten Datei mit dem oben genannten Hash. Die 528 Treffer sind maschinell reproduzierbare syntaktische Kandidaten, nicht 528 semantisch bestätigte Registrierungen. Keine Datenbank oder GEOS.INI wurde verändert; kein Laufzeittest und kein GEOTEST-Build wurden ausgeführt.
