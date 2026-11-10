# GEOTEST – DESKTOPG.GEO: Dekodierung der Dateityp-Token-Tabellen (2385)

Stand: 2026-11-10

## Ausgangspunkt

In Untersuchung 2383/2384 wurde in `DESKTOPG.GEO`, Ressource 8, Code gefunden, der vier CS-relative Tabellenbereiche verarbeitet. Die Schleife ab Ressourcenoffset `0500h` iteriert sechs Mal; die zweite Schleife ab `056Ch` iteriert acht Mal.

Originaldatei: `GEOWORKS/SYSAPPL/DESKTOPG.GEO`, 101.524 Bytes, SHA-256 `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`.

## 1. Erste Tabelle: sechs vierstellige Tokens

Der Code ab Ressourcenoffset `0500h` liest wortweise aus:
- `CS:[DI+0538h]`
- `CS:[DI+0544h]`
- `CS:[DI+0550h]`
- `CS:[DI+055Ch]`

`DI` läuft von 0 bis 10 in Zweierschritten, also über sechs Datensätze.

Die beiden Zeichenarrays bei `0538h` und `0544h` lassen sich paarweise zusammensetzen:

| Index | Array 0538h | Array 0544h | Zusammengesetztes Token |
|---:|---|---|---|
| 0 | `DE` | `SK` | `DESK` |
| 1 | `FL` | `DR` | `FLDR` |
| 2 | `FI` | `LE` | `FILE` |
| 3 | `gA` | `PP` | `gAPP` |
| 4 | `gD` | `AT` | `gDAT` |
| 5 | `gD` | `OS` | `gDOS` |

Die Bytes sind in der Ressource tatsächlich als sechs Zweiergruppen hintereinander gespeichert. Die Reihenfolge im Code lädt je Datensatz zwei 16-Bit-Werte und übergibt sie an den Far-Call bei Offset `050Fh` (numerischer Zieloffset `0072h`).

Die beiden weiteren Arrays enthalten:
- bei `0550h`: sechsmal den 16-Bit-Wert `0026h`;
- bei `055Ch`: die sechs 16-Bit-Werte `0018h, 0010h, 0012h, 001Ah, 001Ch, 0014h`.

Nach einem bedingten Sprung lädt der Code die beiden Werte des zweiten Arraysatzes und ruft den Far-Call bei `0523h` (numerischer Zieloffset `0071h`) auf. Die Bedeutung der Werte `0026h` und der sechs unterschiedlichen Werte ist noch nicht geklärt.

## 2. Zweite Tabelle: acht Token-Datensätze

Der Code ab Ressourcenoffset `056Ch` greift auf:
- `CS:[DI+059Ah]`
- `CS:[DI+05AAh]`
- `CS:[DI+05BAh]`
- `CS:[DI+05CAh]`

`DI` läuft von 0 bis 14 in Zweierschritten, also über acht Datensätze.

Die beiden Zeichenarrays ergeben:

| Index | Array 059Ah | Array 05AAh | Zusammengesetztes Token |
|---:|---|---|---|
| 0 | `FL` | `DR` | `FLDR` |
| 1 | `FL` | `DR` | `FLDR` |
| 2 | `FI` | `LE` | `FILE` |
| 3 | `FI` | `LE` | `FILE` |
| 4 | `gA` | `PP` | `gAPP` |
| 5 | `gA` | `PP` | `gAPP` |
| 6 | `gD` | `AT` | `gDAT` |
| 7 | `gD` | `AT` | `gDAT` |

Das zugehörige Wortarray bei `05BAh` lautet:
`0040h, 1040h, 0040h, 1040h, 0040h, 1040h, 0040h, 1040h`.

Das weitere Wortarray bei `05CAh` enthält acht Werte:
`09A4h, 09A8h, 099Ch, 09A0h, 09ACh, 09B0h, 09B4h, 09B8h`.

Der Code übergibt die Tokenhälften und das jeweilige Flagwort an einen Far-Call bei Ressourcenoffset `0580h` (numerischer Zieloffset `0073h`). Anschließend schreibt er zurückgegebene Registerwerte in die durch das letzte Array adressierten Speicherstellen. Die genaue Semantik des Aufrufs und der Zielstruktur ist noch nicht entschlüsselt.

## 3. Bedeutung für die Dokumenterkennung

Der Dateiverwalter enthält damit nachweislich statische Tabellen mit den generischen vierstelligen Tokens:
- `DESK`
- `FLDR`
- `FILE`
- `gAPP`
- `gDAT`
- `gDOS`

Die zweite Tabelle verarbeitet `FLDR`, `FILE`, `gAPP` und `gDAT` jeweils zweimal mit unterschiedlichen Flagwerten.

Die anwendungsspezifischen Dokumenttokens `WDAT` und `DDAT` stehen **nicht** in diesen beiden statischen Tokenlisten. Das bedeutet nur, dass sie nicht in diesen beiden Tabellen hartcodiert sind. Es beweist nicht, dass GeoManager sie ignoriert: die spezifischen Zuordnungen können über einen anderen Pfad, über den Creator-Token oder über dynamische Registrierung verarbeitet werden.

## 4. Was jetzt belegt ist

1. Die Schleife bei `0500h` verarbeitet sechs vierstellige Tokenwerte.
2. Die sechs Token lassen sich aus den Bytepaar-Arrays eindeutig als `DESK/FLDR/FILE/gAPP/gDAT/gDOS` rekonstruieren.
3. Die Schleife bei `056Ch` verarbeitet acht Tokenwerte: zweimal `FLDR`, zweimal `FILE`, zweimal `gAPP`, zweimal `gDAT`.
4. Die zweite Schleife verwendet abwechselnd die Flagwerte `0040h` und `1040h`.
5. Die beiden Schleifen rufen drei verschiedene numerische Offsets auf: `0072h`, `0071h`, `0073h`; ihre API-Namen sind weiterhin nicht aufgelöst.

## 5. Nächster Schritt

1. Die Daten-/Registerkonventionen der Calls `0071h`, `0072h` und `0073h` rekonstruieren.
2. Die Speicherstellen `099Ch–09B8h` in Ressource 8 mit den aufrufenden und lesenden Codepfaden verbinden.
3. Den Unterschied zwischen den Flagwerten `0040h` und `1040h` aus den aufrufenden/aufgerufenen Routinen herleiten.
4. Nach einem separaten dynamischen oder statischen Pfad für anwendungsspezifische Dokumenttokens wie `WDAT` und `DDAT` suchen.
5. Erst danach den Zusammenhang zu Dokumentmonikern und GeoManager-Icons bewerten.

## Status

Die generischen Token-Arrays sind bytegenau dekodiert. Die Bedeutung der drei Call-Ziele, der Flags, der Ergebnisfelder und der app-spezifischen Dokumentzuordnung bleibt offen. Keine Originaldatei geändert, kein GEOTEST-Build erstellt und kein Laufzeiterfolg behauptet.
