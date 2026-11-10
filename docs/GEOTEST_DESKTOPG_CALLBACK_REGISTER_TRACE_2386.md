# GEOTEST – DESKTOPG.GEO: Registerfluss und Kontrolllogik der Token-Aufrufe (2386)

Stand: 2026-11-10

## Ziel und Abgrenzung

Untersuchung ausschließlich GeoWorks / PC/GEOS 1.x. Ziel bleibt die native Testanwendung `GEOTEST.GEO` mit eigenem Dokument, Speichern/Wiederöffnen und eigenem Dokument-Icon. Keine Treiberentwicklung. `DESKTOPG.GEO` und die daraus extrahierte Ressource 8 wurden nur lesend untersucht.

Original:
- `GEOWORKS/SYSAPPL/DESKTOPG.GEO`
- 101.524 Bytes
- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`
- Ressource 8: Dateioffset `56FCh`, Länge 2.224 Bytes, Code-/Datenbereich bis relativ `075Fh`, Relocation-Bereich 336 Bytes.

## 1. Korrektur der Instruktionspositionen aus 2383–2385

Die Rohbytes wurden erneut direkt aus Ressource 8 disassembliert. Dabei fiel auf, dass die älteren Notizen die beiden ersten Far-Calls um sieben Bytes zu früh lokalisiert hatten: Die alten Positionen bezeichneten jeweils die vorhergehende MOV-Instruktion, nicht den CALL-Opcode.

Die tatsächlichen Instruktionsanfänge sind:

| Zweck | Ressourcenoffset | Datei-Offset | Bytes | Instruktion |
|---|---:|---:|---|---|
| Token-Callback A | `0516h` | `5C12h` | `9A 72 00 00 00` | `CALL FAR 0000:0072h` |
| Token-Callback B | `052Ah` | `5C26h` | `9A 71 00 00 00` | `CALL FAR 0000:0071h` |
| Token-Callback C | `0581h` | `5C7Dh` | `9A 73 00 00 00` | `CALL FAR 0000:0073h` |

Die jeweiligen Segmentwortfelder liegen bei `0519h`, `052Dh` und `0584h`. Keines dieser drei Felder besitzt einen Eintrag in der Relocation-Liste von Ressource 8.

Die Dokumente 2383, 2384 und 2385 wurden entsprechend korrigiert bzw. ergänzt. Die numerischen Ziele `0000:0071h`, `0000:0072h` und `0000:0073h` bleiben absichtlich unbenannt; ihre API-Semantik ist noch nicht nachgewiesen.

## 2. Erste Schleife: sechs generische Tokens

Der Kontrollfluss beginnt bei Ressourcenoffset `0507h`:

1. `DI` wird auf null gesetzt.
2. `AX` wird aus `CS:[DI+0538h]` geladen.
3. `BX` wird aus `CS:[DI+0544h]` geladen.
4. `SI` wird auf null gesetzt.
5. Aufruf `0000:0072h` bei `0516h`.
6. Danach folgt `JAE`: Wenn CF=0 ist, wird der zweite Aufruf dieses Durchlaufs übersprungen.
7. Nur wenn CF=1 ist, lädt der Code `CX=CS:[DI+0550h]`, `DX=CS:[DI+055Ch]`, setzt `BP=8000h` und ruft `0000:0071h` bei `052Ah` auf.
8. `DI) wird um zwei erhöht; bei `DI=000Ch` endet die Schleife.

Damit ist die Registerübergabe an den ersten Aufruf eindeutig:
- AX/BX: die zwei 16-Bit-Tokenhälften,
- SI: Null.

Der zweite Aufruf erhält:
- CX: in allen sechs Datensätzen `0026h`,
- DX: je Datensatz einer der Werte `0018h, 0010h, 0012h, 001Ah, 001Ch, 0014h`,
- BP: `8000h`.

Die Bedingung für Aufruf B hängt ausdrücklich vom Carry-Flag zurück aus Aufruf A ab. Das ist ein wichtiger Teil des Verhaltens; die Schleife ist nicht einfach eine unbedingte Registrierung aller sechs Tokens.

## 3. Zweite Schleife: acht Token-/Flag-Datensätze

Die zweite Schleife beginnt bei Ressourcenoffset `0568h`:

1. `DI=0`.
2. `AX=CS:[DI+059Ah]`.
3. `BX=CS:[DI+05AAh]`.
4. `BP=CS:[DI+05BAh]`.
5. `DH=SS:[0AC6h]` (Segmentpräfix `36h` = SS).
6. Aufruf `0000:0073h` bei `0581h`.
7. `BP=CS:[DI+05CAh]`.
8. `CX) wird nach `SS:[BP]` geschrieben und `DX) nach `SS:[BP+2]`.
9. `DI) wird um zwei erhöht; die Schleife endet bei `DI=0010h`.

Die acht Flagwerte in BP lauten abwechselnd `0040h` und `1040h`. Die acht Zieloffsets lauten:
`09A4h, 09A8h, 099Ch, 09A0h, 09ACh, 09B0h, 09B4h, 09B8h`.

Somit ist die Rückgabespeicherung nun exakt zugeordnet: Die Werte CX und DX aus Aufruf C werden paarweise in acht SS-relative Speicherbereiche geschrieben. Die Zieloffsets sind keine Dateioffsets und keine Ressourcenoffsets.

## 4. Was die Aufrufe derzeit beweisen

Belegt ist:
- Es gibt drei eigenständige Far-Call-Ziele bei den numerischen Adressen `0000:0071h`, `0000:0072h` und `0000:0073h`.
- Die erste Token-Tabelle wird in einer sechsmaligen Schleife verarbeitet.
- Aufruf B erfolgt nur, wenn Aufruf A CF=1 zurückgibt.
- Die zweite Token-Tabelle wird achtmal verarbeitet.
- Aufruf C erhält Tokenhälften, ein alternierendes Flagwort und einen zusätzlichen SS-Datenwert.
- Aufruf C liefert mindestens die Registerwerte CX und DX, die danach in SS-Datenfelder geschrieben werden.

Nicht belegt ist:
- ob diese Ziele Kernel-Callbacks, Systemvektoren, residente Routinen oder eine andere Low-Memory-Schnittstelle sind;
- ob Aufruf A einen Token sucht, registriert oder validiert;
- ob Aufruf B ein zweites Attribut, einen Dateityp oder eine Ressource zuordnet;
- ob Aufruf C Icon-Moniker, Dateinamensregeln, Dateitypflags oder andere Datenstrukturen liefert;
- ob und wie diese Routinen den GEOS-Dateikopf mit Typ-/Creator-Token lesen.

## 5. Warum die 09xx-Zieloffsets wichtig sind

Die zweite Schleife schreibt Rückgabewerte in SS-relative Speicherbereiche bei `099Ch–09B8h`. Das sind die ersten konkreten Datenziele, die wir mit dem dritten Callback verbinden können.

Der nächste Durchgang muss alle Lese- und Schreibreferenzen auf diese SS-Offets im gesamten DESKTOPG-Codebestand finden. Dadurch lässt sich feststellen, ob es sich um:
- registrierte Handler-/Callback-Adressen,
- Ressourcen-/Moniker-Handles,
- Tabellenzeiger,
- oder sonstige Laufzeitdaten handelt.

Ohne diese Kreuzreferenzen wäre jede Benennung spekulativ.

## 6. Nächste Schritte

1. Alle DESKTOPG-Ressourcen nach Zugriffen auf SS-Offsets `099Ch`, `09A0h`, `09A4h`, `09A8h`, `09ACh`, `09B0h`, `09B4h`, `09B8h` durchsuchen.
2. Den Aufrufkontext des Initialisierungscodes ermitteln: wer ruft die Routine mit den beiden Tabellen auf, wann und in welcher Startphase?
3. Die System-/Kernel-Initialisierung prüfen, die Low-Memory-Adressen `0071h–0073h` belegt oder bereitstellt.
4. Erst danach die Funktionen benennen und den Weg von GEOS-Typ/Creator zu Moniker/Icon weiterverfolgen.
5. Keine Änderung an GEOTEST, bis der Dokument- und Iconpfad nachvollziehbar ist.

## Status

- Exakte CALL-Instruktionsanfänge und Datei-Offsets korrigiert.
- Registereingaben und CF-Verzweigung der ersten Schleife rekonstruiert.
- Registereingaben und SS-relative Ergebnisablage der zweiten Schleife rekonstruiert.
- API-Namen und Zweck der Callbacks weiterhin offen.
- Keine Originaldatei geändert; kein GEOTEST-Build erstellt; kein Laufzeiterfolg behauptet.
