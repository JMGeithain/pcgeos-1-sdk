# GEOTEST – DESKTOPG.GEO: Kreuzreferenzen der Callback-Ergebnisse in Ressource 2 (2387)

Stand: 2026-11-10

## Ziel / Abgrenzung

Fortsetzung der ausschließlich auf GeoWorks / PC/GEOS 1.x begrenzten Analyse der nativen Dokument-/Dateityp-Erkennung. Ziel bleibt GEOTEST mit eigenem nativen Dokument und eigenem Dokument-Icon. Keine Treiberentwicklung; keine Originaldatei geändert.

Untersuchte Originaldatei:
- `GEOWORKS/SYSAPPL/DESKTOPG.GEO`
- Größe: 101.524 Bytes
- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`

## 1. Neue Kreuzreferenz: Ressource 2 liest die 09xx-Speicherfelder

Die in Ressource 8 durch den Callback `0000:0073h` befüllten SS-relativen Speicherbereiche `099Ch–09B8h` werden in Ressource 2 wieder als Datenquellen verwendet.

Ressource 2:
- Datei-Offset: `0B60h`
- Größe: 8.704 Bytes
- Flags: `0A72h`
- Relocation-Bytes: `02B0h`
- Code-/Datenbereich vor Relocations: 8.016 Bytes

Die Ressource-2-Codeanalyse zeigt vier Wrapper-Routinen:

| Wrapper | Ressourcenoffset R2 | Datei-Offset | AX (ES-Quelloffset) | BX (SS-Quelloffset) |
|---|---:|---:|---:|---:|
| W0 | `0CEAh` | `184Ah` | `099Ch` | `09A0h` |
| W1 | `0CF4h` | `1854h` | `09A4h` | `09A8h` |
| W2 | `0D03h` | `1863h` | `09ACh` | `09B0h` |
| W3 | `0D0Dh` | `186Dh` | `09B4h` | `09B8h` |

Jeder Wrapper ruft die gemeinsame Hilfsroutine bei R2-Offset `0D17h` auf.

## 2. Gemeinsame Kopierroutine bei R2:0D17h

Die Routine führt folgende Operationen aus:

1. Sichert BP und DS.
2. Setzt DS gleich ES.
3. Übernimmt AX in BP.
4. Liest zwei Wörter aus `ES:[BP]` und `ES:[BP+2]` und schreibt sie in das Objekt bei `ES:[DI+7Ah]` und `ES:[DI+7Ch]`.
5. Liest zwei Wörter aus `SS:[BX]` und `SS:[BX+2]` und schreibt sie in das Objekt bei `ES:[DI+76h]` und `ES:[DI+78h]`.
6. Setzt die Bits `18h` im Objektbyte `ES:[DI+83h]`.
7. Stellt DS und BP wieder her.

Damit ist die Funktion der Wrapper auf Byte-/Registerebene klar: Sie kopieren je vier Bytes aus einem ES-relativen Quellbereich und vier Bytes aus einem SS-relativen Quellbereich in Felder eines Objekt-/Datensatzes.

Die Segmentunterscheidung ist wichtig. Ein numerisch gleicher Offset in ES und SS bezeichnet nicht automatisch dieselbe Speicherstelle. Deshalb werden die ES-Quellfelder nicht mit den durch Ressource 8 beschriebenen SS-Callback-Ausgaben gleichgesetzt.

## 3. Aufrufstellen und generische Tokenwerte

Ressource 2 ruft die Wrapper abhängig von Objektzustand und Kontrollfluss auf:

| R2-Codeoffset | Aufruf | Danach gesetzte Tokenhälften in AX/BX | Tokenbytes |
|---:|---|---|---|
| `0C9Fh` | W2 (`0D03h`) | AX=`4167h`, BX=`5050h` | `gAPP` |
| `0CADh` | W1 (`0CF4h`) | AX=`4C46h`, BX=`5244h` | `FLDR` |
| `0CBBh` | W3 (`0D0Dh`) | AX=`4467h`, BX=`5441h` | `gDAT` |
| `0CCEh` | W0 (`0CEAh`) | AX=`4946h`, BX=`454Ch` | `FILE` |

Die Wortwerte sind little-endian zu lesen: AX=`4167h` entspricht Bytes `67 41` (ASCII `gA`), BX=`5050h` entspricht `PP`; zusammen ergibt das `gAPP`. Entsprechend ergeben die anderen Paare `FLDR`, `gDAT` und `FILE`.

Der Code schreibt diese Tokenhälften danach in die Objektfelder `ES:[DI+44h]` und `ES:[DI+46h]`; außerdem schreibt er SI nach `ES:[DI+48h]`. Die Werte sind also Teil eines Dateityp-/Objekt-Datensatzes, nicht nur Debug-Strings.

## 4. Verbindung zu Ressource 8

Die Ressource-8-Tabelle mit acht Einträgen ruft `0000:0073h` auf und speichert die zurückgegebenen Register CX/DX in SS-relative Speicherfelder. Ressource 2 verwendet später vier dieser SS-Felder als Quellwerte in der gemeinsamen Kopierroutine.

Damit ist jetzt nachgewiesen:
- Ressource 8 richtet die Callback-Ausgaben in einem SS-Datenbereich ein.
- Ressource 2 liest einen Teil dieser Daten über SS-relative Zugriffe.
- Ressource 2 kombiniert diese Werte mit ES-relativen Daten und generischen Typ-Tokens.
- Die resultierenden Werte werden in Objekt-/Datensatzfelder übernommen.

Noch nicht bewiesen ist, welche konkrete Bedeutung die kopierten Wörter haben. Sie könnten z.B. Ressourcen-/Monikerreferenzen oder andere Dateityp-Metadaten sein; diese Begriffe werden hier nicht als Tatsache behauptet.

## 5. Bedeutung für die Icon-Frage

Der Befund ist ein direkter Schritt in Richtung Icon-/Monikerpfad: Die Dateityp-Objekte enthalten neben dem Tokenpaar zusätzliche Werte, die aus zwei Segmentbereichen in Objektfelder kopiert werden. Diese Werte könnten den späteren Dateityp-/Darstellungspfad speisen.

Es ist aber noch nicht nachgewiesen, dass die Felder `76h–7Ch` konkrete Icon-Moniker-Handles sind. Dafür müssen die späteren Leser dieser Objektfelder verfolgt und die Zielressourcen identifiziert werden.

Ebenso bleibt offen, wie die anwendungsspezifischen Dokumenttokens `WDAT/WP00` und `DDAT/DP00` dynamisch oder anderweitig in diesen allgemeinen Dateiverwalter gelangen. Die generischen Token `FILE`, `FLDR`, `gAPP` und `gDAT` sind nicht dasselbe wie die app-spezifischen Dokumenttypen.

## 6. Nächste Schritte

1. Alle Leser der Objektfelder `ES:[DI+76h]`, `+78h`, `+7Ah`, `+7Ch` und des Statusbytes `+83h` in DESKTOPG.GEO verfolgen.
2. Herausfinden, ob die Werte auf Ressourcenhandles, Monikerlisten, Callback-Handler oder andere Datenstrukturen zeigen.
3. Den Codepfad untersuchen, der die app-spezifischen Creator-/Dokumenttypen `WDAT/WP00` und `DDAT/DP00` dem Dateimanager verfügbar macht.
4. Erst nach Nachweis der Objektfelder den Icon-/Monikerpfad und die minimale GEOTEST-Registrierung ableiten.

## Status

- SS-Callback-Ausgaben aus Ressource 8 in Ressource 2 wiedergefunden.
- Vier Wrapper und ihre ES-/SS-Quellbereiche bytegenau identifiziert.
- Gemeinsame Kopierroutine und Zielobjektfelder `76h–7Ch` sowie Statusbyte `83h` rekonstruiert.
- Zuordnung der Wrapper zu den generischen Tokens `FILE`, `FLDR`, `gAPP`, `gDAT` bestätigt.
- Semantik der kopierten Werte und der tatsächliche Icon-/Monikerpfad noch offen.
- Keine Originaldatei geändert; kein GEOTEST-Build erstellt; kein Laufzeiterfolg behauptet.
