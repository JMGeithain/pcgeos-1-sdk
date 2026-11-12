# GEOTEST – TOKEN.DB: Datensatzsignatur und wiederholte Tabellenbereiche (2424)

Stand: 2026-11-12  
Geltungsbereich: originales GeoWorks / PC/GEOS 1.x; statische Analyse ohne Änderungen.

## 1. Datenbasis

Untersucht wurde ausschließlich das ZIP-Mitglied `GEOWORKS/SYSTEM/TOKEN.DB`:

- Größe: 952.688 Byte
- SHA-256: `c7fa3d51c9bdce14b988d20fd8ed57ac7da9837803090ac858990613ec53ae35`
- VM-Block: Handle `0080h`
- Blockbasis im File: `DAB50h`
- Blockgröße laut VM-Verzeichnis: 56.864 Byte

## 2. Wiederkehrende Kennungsfolge

Im frühen Bereich des Blocks finden sich mehrere Tokenstrings mit einem wiederkehrenden Rohmuster:

```
4 Byte Token
2 Byte Herstellerkennung
74 00
2 Byte Kennwert
danach variable bzw. noch nicht vollständig verstandene Felder
```

Beispiele:

| Token | Blockoffset | Herstellerkennung | Kennwert |
|---|---:|---:|---:|
| `DP00` | `018Ch` | 0 | `0036h` |
| `DDAT` | `01AEh` | 0 | `003Ah` |
| `PLNR` | `01C8h` | 0 | `003Eh` |
| `plnr` | `01E0h` | 0 | `0042h` |
| `WP00` | `01FCh` | 0 | `0046h` |
| `WDAT` | `0216h` | 0 | `004Ah` |
| `gDOC` | `0A58h` | 255 | `019Ch` |
| `PAPR` | `0BF6h` | 255 | `01DCh` |

Die Kennwerte der ersten sechs Beispiele steigen in Schritten von vier: `0036h, 003Ah, 003Eh, 0042h, 0046h, 004Ah`. Das ist eine reproduzierbare Zahlenfolge in den Rohdaten. Die Bedeutung als ID, Index, Handle oder sonstiger Schlüssel ist noch nicht bewiesen.

## 3. Nicht alle Tokenvorkommen haben dieses Muster

Wichtig ist die Unterscheidung zwischen Tokenstrings, die in solchen Eintragsfolgen vorkommen, und bloßen Texttreffern innerhalb anderer Datenstrukturen.

Beispielsweise beginnt ein weiteres `DP00`-Vorkommen bei Blockoffset `0DE6h` nicht mit dem Muster `DP00 00 00 74 00`, sondern wird von Text-/Datenbytes gefolgt (u.a. `Icons `). Ein späteres `DDAT`-Vorkommen bei `0E3Ch` hat ebenfalls eine andere Nachbarschaft.

Daher dürfen nicht sämtliche ASCII-Treffer in TOKEN.DB als gleichartige Tokenregistrierungen gezählt werden. Die Tokenzeichenfolge allein reicht nicht zur Klassifikation eines Datensatzes.

## 4. Wiederholte Bereiche innerhalb desselben VM-Blocks

Drei Bereiche zeigen sehr starke Byteähnlichkeit:

| Erster Bereich | Vergleichsbereich | Länge | Gleiche Bytes an gleicher Position |
|---:|---:|---:|---:|
| `0180h` | `6980h` | 288 | 84 |
| `0A40h` | `7240h` | 384 | 32 |
| `0BF0h` | `73E0h` | 256 | 34 |

Ein SequenceMatcher-Vergleich findet in allen drei Paaren einen zusammenhängenden Matching-Block von fast der gesamten Länge; der Versatz beträgt jeweils vier Bytes bzw. beim dritten Vergleich 20 Bytes. Das zeigt, dass die Datenbereiche sehr ähnlich wiederholt oder in leicht verschobener Form abgelegt sind. Die Bereiche sind jedoch nicht byteidentisch, und die vier-/zwanzig Byte Abweichungen dürfen nicht ohne weitere Erklärung als bloße Header interpretiert werden.

## 5. Einordnung der Herstellerkennung

Bei den Beispielen `DP00/DDAT/PLNR/WP00/WDAT` stehen nach dem Token zwei Nullbytes. Bei `gDOC` und `PAPR` stehen dort `FF 00`, also der bereits aus den Provider-Geodes bekannte Herstellerwert 255.

Das stimmt mit den Headerbefunden aus den Geodes `PAPR.000` und `GDOC.000` überein. Es ist damit eine konsistente Bytekorrelation zwischen Provider-Dateikopf und TOKEN.DB-Einträgen. Der genaue Zweck des anschließenden `74 00` und des Kennwerts bleibt offen.

## 6. Grenzen der Aussage

**Nachgewiesen:**
1. Im VM-Block `0080h` existiert ein wiederkehrendes Rohmuster aus Token, Herstellerwort, `74 00` und einem 16-Bit-Kennwert.
2. Die genannten GeoWrite-/GeoDraw-/GeoPlanner-Kennungen tragen Kennwerte im Abstand von vier.
3. Provider-Tokens tragen in den gezeigten Fällen Herstellerkennung 255.
4. Einige große Bereiche innerhalb des Blocks sind strukturell stark ähnlich, aber nicht byteidentisch.
5. Andere Tokenstring-Vorkommen haben eine abweichende Struktur und dürfen nicht mit diesen Einträgen vermischt werden.

**Nicht nachgewiesen:**
1. Die semantische Bedeutung von `74 00`.
2. Ob der Kennwert eine Token-ID, einen Index, einen Handle oder einen Zeiger darstellt.
3. Ob die wiederholten Bereiche alternative Tabellen, Kopien, Versionsdaten oder Suchstrukturen sind.
4. Welche Felder auf die Moniker-/Icon-Blöcke zeigen.
5. Wie GeoManager diese Strukturen zur Laufzeit durchsucht.

## 7. Nächster Schritt (2425)

1. Die vier-Byte- und zwanzig-Byte-Abweichungen der wiederholten Bereiche gezielt lokalisieren.
2. Alle Token-Datensatzkandidaten mit `74 00` innerhalb des Blocks erfassen, nicht nur die bekannten Namen.
3. Kennwerte und nachfolgende Felder über viele Einträge hinweg statistisch vergleichen.
4. Die Kandidaten gegen die VM-Blockhandles und die bekannten Icon-Monikerblöcke testen, ohne aus Zahlenähnlichkeit allein eine Referenz abzuleiten.
5. Erst nach reproduzierbarem Strukturmodell die Verknüpfung für GEOTEST ableiten.

## 8. Sicherheit und Reproduzierbarkeit

Die Originaldatei wurde nur gelesen. TOKEN.DB und GEOS.INI wurden nicht verändert; es wurde kein Provider installiert, kein GEOTEST-Build erstellt und kein Laufzeiterfolg behauptet.
