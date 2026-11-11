# GEOTEST – TOKEN.DB: Token-Datensätze im VM-Block 0080h (2423)

Stand: 2026-11-12  
Geltungsbereich: originales GeoWorks / PC/GEOS 1.x, ausschließlich statische Analyse.  
Datei: `GEOWORKS/SYSTEM/TOKEN.DB`  
Größe: 952.688 Byte  
SHA-256: `c7fa3d51c9bdce14b988d20fd8ed57ac7da9837803090ac858990613ec53ae35`

## 1. Korrektur zur inneren Struktur aus Untersuchung 2422

Der VM-Block mit Handle `0080h` liegt bei Dateioffset `DAB50h`, hat 56.864 Byte und ist im VM-Verzeichnis mit Flag `01FFh` markiert.

Der bisher verwendete allgemeine LMem-Parser liest die ersten Headerfelder dieses Blocks nicht konsistent mit den anderen klar erkennbaren LMem-Blöcken. Die im Block bei Offset `000Ah` stehende Handle-Anzahl ist zwar `0020h`, aber die nachfolgenden Werte ab `0014h` ergeben bei Anwendung des bisherigen Standard-LMem-Layouts keine gültige Folge von Chunk-Payload-Offets. Der Parser findet dadurch nur einen scheinbaren Chunk.

**Korrektur:** Block `0080h` wird in dieser Untersuchung als VM-Datenblock mit Token-Datensatzbereichen bezeichnet. Die Bezeichnung „zentraler LMem-Block“ aus der vorherigen Arbeitsnotiz ist nicht als bestätigt zu übernehmen. Die innere Blockstruktur muss separat rekonstruiert werden.

## 2. Bytegenau bestätigte Tokenpositionen

Die folgenden Positionen wurden erneut direkt in den Blockdaten gesucht. Der Dateioffset ergibt sich aus Blockbasis `DAB50h` plus Blockrelativoffset.

| Token | Blockrelativoffset | Dateioffset |
|---|---:|---:|
| `DP00` | `018Ch` | `DACDCh` |
| `DDAT` | `01AEh` | `DACFEh` |
| `WP00` | `01FCh` | `DAD4Ch` |
| `WDAT` | `0216h` | `DAD66h` |
| `gDOC` | `0A58h` | `DB5A8h` |
| `PAPR` | `0BF6h` | `DB746h` |
| `DP00` | `0DE6h` | `DB936h` |
| `DDAT` | `0E3Ch` | `DB98Ch` |
| `DP00` | `0E9Eh` | `DB9EEh` |
| `DP00` | `134Eh` | `DBE9Eh` |
| `gDOC` | `725Ch` | `E1DACh` |
| `PAPR` | `73FAh` | `E1F4Ah` |
| `DP00` | `6990h` | `E14E0h` |
| `DDAT` | `69B2h` | `E1502h` |
| `DP00` | `75EAh` | `E213Ah` |
| `DDAT` | `7640h` | `E2190h` |
| `DP00` | `76A2h` | `E21F2h` |
| `DP00` | `7B52h` | `E26A2h` |
| `WP00` | `6A00h` | `E1550h` |
| `WDAT` | `6A1Ah` | `E156Ah` |

Die Positionen stimmen mit der Suche über die gesamte Datei aus Untersuchung 2421 überein. Sie sind hier zusätzlich als relative Positionen innerhalb desselben VM-Blocks dokumentiert.

## 3. Zusammengehörige Einträge und sichtbare Nachbarschaft

### 3.1 GeoWrite

Die beiden ersten Kennungen stehen im Abstand von `1Ah` Bytes:

- `WP00` bei Blockoffset `01FCh`
- `WDAT` bei Blockoffset `0216h`

Dasselbe Muster wiederholt sich bei:

- `WP00` bei `6A00h`
- `WDAT` bei `6A1Ah`

Die Wiederholung der Paarung ist nachgewiesen. Ob beide Paare dieselbe Datenbankfunktion erfüllen, ist noch nicht geklärt.

### 3.2 GeoDraw

Ein frühes Paar liegt bei:

- `DP00` bei `018Ch`
- `DDAT` bei `01AEh`

Ein weiteres Paar liegt bei:

- `DP00` bei `6990h`
- `DDAT` bei `69B2h`

Weitere `DP00`-Vorkommen erscheinen bei `0DE6h`, `0E9Eh`, `134Eh`, `75EAh`, `76A2h` und `7B52h`; weitere `DDAT`-Vorkommen bei `0E3Ch`, `7640h`.

Die unterschiedlichen Abstände und Nachbarschaften zeigen, dass nicht jedes Vorkommen einfach als identischer Datensatz mit fester Länge behandelt werden darf.

### 3.3 Icon-Provider

Für `gDOC` liegen Vorkommen bei `0A58h` und `725Ch`; für `PAPR` bei `0BF6h` und `73FAh`.

Im unmittelbaren Bytekontext der untersuchten Provider-Treffer folgt auf den vierstelligen Token jeweils `FF 00`. Das entspricht der Herstellerkennung 255, die auch in den Geode-Köpfen von `GDOC.000` und `PAPR.000` festgestellt wurde.

## 4. Was aus diesen Befunden folgt – und was nicht

**Gesichert:**
1. Die genannten Tokens befinden sich im VM-Block `0080h`.
2. GeoWrite-App- und Dokumenttoken erscheinen in zwei gleich aufgebauten Tokenpaaren mit einem Abstand von 26 Byte.
3. GeoDraw-App- und Dokumenttoken kommen in mehreren Bereichen vor; mindestens zwei Vorkommen bilden ein enges Paar.
4. Provider-Tokens `gDOC` und `PAPR` sind ebenfalls in diesem Block vorhanden; die Herstellerkennung 255 ist im Kontext sichtbar.
5. Der allgemeine LMem-Parser liefert für Block `0080h` keine belastbare Chunk-Auflösung.

**Nicht gesichert:**
1. Die Bedeutung der Wörter und Zeiger unmittelbar vor und nach jedem Token.
2. Die Zahl der logischen Token-Datensätze.
3. Die Bedeutung der Wiederholungen.
4. Die Verbindung zwischen einem Token-Datensatz und den Moniker-Blöcken `00BCh`, `0470h`, `03D4h` und `0DF4h`.
5. Der genaue native GeoManager-Ladepfad.

## 5. Nächste Schritte (2424)

1. Die Headerstruktur des Blocks `0080h` anhand seiner tatsächlichen Felder und der VM-Relocation-/Handleinformationen neu bestimmen.
2. Die wiederkehrende Bytefolge `74 00` und die benachbarten 16-Bit-Felder über mehrere bekannte Tokens hinweg vergleichen.
3. Die Struktur mit bekannten TOKEN.DB-Blöcken anderer Typen vergleichen, insbesondere mit eindeutig als LMem erkennbaren Blöcken.
4. Erst nach einer validierten Datensatzgrenze mögliche Handle-/Monikerreferenzen auswerten.
5. Keine TOKEN.DB-Änderung und keine GEOTEST-Registrierung vornehmen, bevor die Feldsemantik nachgewiesen ist.

## 6. Reproduzierbarkeit

Alle Offsets wurden aus der unveränderten Datei `TOKEN.DB` mit dem oben genannten SHA-256 ermittelt. Es wurden keine Datenbankbytes geändert, keine GEOS.INI angepasst, kein Provider installiert und kein Laufzeittest durchgeführt.
