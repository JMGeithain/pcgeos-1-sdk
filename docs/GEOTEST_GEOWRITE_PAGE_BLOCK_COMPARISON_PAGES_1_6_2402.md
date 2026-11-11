# GEOTEST – Erweiterter GeoWrite-Seitenblockvergleich (Seiten 1–6) (2402)

Stand: 2026-11-11

## 1. Eingabe und Methode

- ZIP: `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`
- Dokument: `Showcase/Deutsch/GeoWrite/SOLAR_DE.000`
- VM-Map-Block: `0044h`
- PageArray: Map-LMem-Chunk `001Ah`
- PageArray-Header: 21 Elemente, 30 Byte je Element
- Seiten-VM-Handles 1–6: `005Ch`, `0380h`, `0398h`, `03B0h`, `03C8h`, `03E0h`

Die Originaldatei wurde erneut direkt aus dem ZIP extrahiert. Die VM- und LMem-Strukturen wurden mit dem beigefügten `vm1.py`-Parser gelesen. Für jeden Seitenblock wurden alle belegten Chunk-Payloads anhand der LMem-Handle-Tabelle extrahiert und byteweise verglichen.

## 2. Gemeinsamer Aufbau

Alle sechs Seitenblöcke haben:
- 848 Byte VM-Blockgröße
- VM-Flag `01FFh`
- LMem-Handle-Tabellenoffset `0020h`
- 38 Handle-Slots
- 18 belegte Chunk-Payloads

Alle 18 belegten Chunks besitzen auf allen sechs Seiten dieselben Längen.

## 3. Vergleich Seite 1 gegen Seiten 2–6

Nur drei Chunks unterscheiden sich gegenüber Seite 1. Die übrigen 15 Chunks sind auf allen sechs Seiten byteidentisch.

| Chunk | Größe | Unterschiede ggü. Seite 1 | Abweichende Bytepositionen |
|---:|---:|---:|---|
| `0022h` | 104 | 2 je Seite | `4Ch` und `56h` |
| `0030h` | 89 | 1 je Seite | `17h` |
| `0032h` | 28 | 1 je Seite | `17h` |

Positionen sind nullbasiert relativ zum Anfang der jeweiligen Chunk-Payload.

## 4. Exakte Werte der Abweichungen

| Seite | Seiten-VM-Handle | Chunk 0022h @ 4Ch und 56h | Chunk 0030h @ 17h | Chunk 0032h @ 17h |
|---:|---:|---|---|---|
| 1 | `005Ch` | `04h` / `04h` | `04h` | ASCII `1` |
| 2 | `0380h` | `47h` / `47h` | `47h` | ASCII `2` |
| 3 | `0398h` | `49h` / `49h` | `49h` | ASCII `3` |
| 4 | `03B0h` | `4Bh` / `4Bh` | `4Bh` | ASCII `4` |
| 5 | `03C8h` | `4Dh` / `4Dh` | `4Dh` | ASCII `5` |
| 6 | `03E0h` | `4Fh` / `4Fh` | `4Fh` | ASCII `6` |

Die beiden geänderten Bytes in Chunk `0022h` liegen an den Positionen `4Ch` und `56h`; beide tragen pro Seite denselben Wert. In Chunk `0030h` steht derselbe seitenabhängige Wert an Position `17h`. Die Werte für Seiten 2–6 sind die ungeraden ASCII-Codes `G`, `I`, `K`, `M`, `O`; Seite 1 enthält jeweils `04h`.

Diese Werte sind direkt beobachtet. Ihre semantische Bedeutung (z. B. Objektkennung, Seiten-/Ressourcenindex oder Koordinatenfeld) ist nicht geklärt und wird nicht behauptet.

Chunk `0032h` enthält weiterhin die Klartextkennzeichnung:
- `Unser Sonnensystem  |  1/21`
- `Unser Sonnensystem  |  2/21`
- `Unser Sonnensystem  |  3/21`
- `Unser Sonnensystem  |  4/21`
- `Unser Sonnensystem  |  5/21`
- `Unser Sonnensystem  |  6/21`

## 5. Was der erweiterte Vergleich belegt

1. Die ersten sechs Seiten verwenden dieselbe LMem-Chunk-Anordnung und dieselben Chunkgrößen.
2. 15 von 18 belegten Chunks sind über alle sechs Seiten byteidentisch.
3. Genau drei Chunks tragen die hier beobachteten seitenabhängigen Unterschiede.
4. Die drei veränderlichen Chunks enthalten jeweils dieselbe laufende Seitenkennung in unterschiedlicher Repräsentation: binäre Werte in `0022h` und `0030h`, ASCII-Ziffer in `0032h`.
5. Die Unterschiede wiederholen sich konsistent für Seiten 2 bis 6.

## 6. Was nicht belegt ist

- Die Feldnamen und Objektklassen von Chunk `0022h` und `0030h`.
- Ob die beobachteten Werte Handles, Kennungen, Indizes oder andere Felder sind.
- Ob alle 21 Seiten dieselbe Differenzstruktur haben.
- Ob die 15 identischen Chunks für ein eigenständiges GEOTEST-Dokument erforderlich sind.
- Ob die Seitenstruktur ohne GeoWrite-spezifische Objektklassen verwendbar ist.

## 7. Konsequenz und nächster Schritt

Die wiederkehrende Differenzstruktur über sechs Seiten ist ein starkes Muster für seitenabhängige Kennungs-/Referenzfelder. Der nächste Schritt ist die Prüfung weiterer Seiten (7–9 oder 7–21) sowie die Untersuchung der betroffenen Chunk-Bytes im Zusammenhang mit den tatsächlichen WRITE.GEO-Codepfaden.

Die identischen Chunks dürfen noch nicht als entbehrlich eingestuft werden. Für GEOTEST bleibt eine eigene Dokumentstruktur oder eine bewusst minimale, verifizierte Ableitung aus einer nativen Vorlage erforderlich.

## 8. Status

Statische Analyse der unveränderten nativen GeoWrite-1.x-Datei. Keine Änderungen an Showcase-Dokument, WRITE.GEO oder GEOTEST. Kein Laufzeittest und kein GEOTEST-Dokument erzeugt.
