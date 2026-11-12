# GEOTEST / PC-GEOS 1.x – Untersuchung 2468
## DBASE: Segmentkontext, Größenfeld und interne Aufrufe
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Quellen und Methode
Untersucht wurde `GEOWORKS/SYSTEM/DBASE.GEO` aus dem bereitgestellten `GEOWORKS.zip`.
- Dateigröße: 2.930 Byte
- SHA-256: `209d45d361cff3daeb982c07d8faa4fbd3b7f86b4fbba1d18a78b44ed12cd`
- GEODE-Format 1; 5 Ressourcen; 23 Exporte; keine Imports.
- R2: Dateioffset `0x01BE`, 1.664 Byte, 109 Relokationseinträge.
- R4: Dateioffset `0x0A3E`, 256 Byte, 13 Relokationseinträge.

Disassemblierung: GNU objdump, Binärmodus i8086, Intel-Syntax. Zusätzlich wurden die Relokationsrecords mit dem im SDK vorhandenen GEODE-Parser-Schema neu ausgewertet. Kein Emulator- oder GeoWorks-Laufzeittest.

## 2. R2+03C5: Präzisierung des Größenvergleichs
Die Instruktionen R2+`0x03F2` bis `0x0409` lauten:
- `CMP CX,DX`; bei `CX <= DX` Sprung zum Pfad ohne Kopie.
- `CMP WORD PTR [SI+4],1`; bei Zählerstand 1 Sprung zum Pfad ohne Kopie.
- `BP = CX - DX`.
- `ADD BP, WORD PTR ES:[0008]`.
- `CMP BP,0x2000`; bei `BP <= 0x2000` Sprung zum Pfad ohne Kopie.

Damit ist die im Bericht 2467 beschriebene Bedingung bytegenau bestätigt. `ES:[0008]` ist ein einzelnes 16-Bit-Feld des über ES angesprochenen Kontextes/Deskriptors. DBASE verwendet es als Summanden der Schwellenwertberechnung. Die Bedeutung des Feldes ist nicht symbolisch bekannt. Es darf daher nicht ohne weitere Belege als „Heapgröße“, „Puffergröße“ oder „Dokumentlänge“ benannt werden.

## 3. ES-Kontext in R2+03C5
Unmittelbar vor der Größenentscheidung:
- R4+`0x00E5` wird aufgerufen.
- R4+`0x0030` wird aufgerufen.
- R2 lädt `SI=[DI]` und `AX=[DI+2]`.
- R4+`0x0000` wird aufgerufen.
- Der zurückgegebene AX-Wert wird nach BX übernommen.
- DBASE liest `ES:[BX]`. Wenn der Wert nicht `0xFFFF` ist, folgt ein weiterer indirekter Zugriff über `ES:[SI-3]`; danach werden zwei Bytes abgezogen, um den Wert in SI zu normalisieren.

Die anschließende Rechnung nutzt `ES:[0008]`. Damit ist ES in diesem Pfad ein wichtiger Kontext für indirekte Speicher-/Deskriptorzugriffe. Eine formale Strukturdefinition ist aus diesem einzelnen Pfad nicht möglich.

## 4. R4+0000: gespeicherten BP-Kontext in einem ES-Segment sichern
Instruktionsfolge:
- sichert AX, DX und BP;
- lädt AX aus `[SI+2]`;
- ruft den Rohzielbereich `0000:0186` auf;
- setzt ES auf das zurückgelieferte AX;
- schreibt BP nach `ES:[0000]`;
- stellt Register wieder her und kehrt zurück.

Gesichert ist: R4+`0x0000` verwendet den Wert aus Knotenfeld `+2`, ruft einen nicht aufgelösten Segment-/Kernel-Einstieg auf und speichert anschließend BP bei Offset 0 des resultierenden ES-Kontexts.

Nicht gesichert ist, ob `+2` ein Segment, Handle oder anderer Selektor ist und welche Funktion der Rohaufruf `0000:0186` genau hat.

## 5. R4+0030 / R4+0040 / R4+004C: BP-Kontext im DBASE-Datenbereich
- R4+`0x0030`: ruft `0000:0186` auf, setzt DS auf das Ergebnis und schreibt BP nach `DS:[0002]`.
- R4+`0x0040`: lädt BP aus `DS:[0002]` und ruft `0000:0187` auf.
- R4+`0x004C`: lädt BP aus `DS:[0002]` und ruft `0000:018B` auf.
- R4+`0x0066`: ruft `0000:018C` und danach `0000:0186` auf, setzt DS auf das Ergebnis und schreibt BP nach `DS:[0002]`.
- R4+`0x007B`: lädt BP aus `DS:[0002]` und ruft `0000:0187` auf.

Die Bytefolgen zeigen eine wiederkehrende Sicherung und Wiederherstellung von BP in zwei Kontextformen:
1. bei `ES:[0000]`;
2. bei `DS:[0002]`.

Die vier Rohziele `0000:0186`, `0187`, `018B` und `018C` bleiben unbenannt. Die Relokationsrecords weisen sie als Klasse 0 / Typ 0 aus. Aus diesen Werten allein folgt keine bestätigte Kernel-API-Signatur.

## 6. R4+00E5: Zugriff auf einen indirekten Stack-/Kontextwert
R4+`0x00E5`:
- sichert BX und DS;
- setzt DS auf den Wert 1;
- liest BX aus `DS:[0000]`;
- testet das WORD an `SS:[BX]`;
- wenn dieses WORD nicht null ist, lädt es nach AX;
- stellt DS und BX wieder her.

Der Relokationsrecord am DS-Segmentoperand ist Klasse 2 / Typ 2 mit Zielwert 1. Das ist ein konkreter Relokationsbefund. Die Rolle des Segmentes 1 und des über DS:0000 gewonnenen Zeigers ist damit noch nicht semantisch bestimmt.

Direkte Aufrufstellen in R2:
- R2+`0x03CA` innerhalb R2+`0x03C5`;
- R2+`0x04D3` innerhalb R2+`0x04C5`;
- R2+`0x056F` innerhalb R2+`0x056E`.

Weitere Aufrufe erfolgen aus R4-eigenen Export-/Hilfsroutinen, darunter R4+`0x0087`, `0x00A8` und `0x00B3`.

## 7. R2+0019, R2+001B und R2+001C: Relokationsvorbehalt
Im Kopierpfad stehen folgende Far-Aufrufe:
- R2+`0x041F`: `CALL FAR 0000:0019`
- R2+`0x0434`: `CALL FAR 0000:001B`
- R2+`0x0457`: `CALL FAR 0000:001C`
- R2+`0x04A6`: `CALL FAR 0000:001B`

Die Relokationseinträge an den jeweiligen Segmentfeldern sind jeweils `info=0x00`, also Quelle/Klasse 0 und Typ 0; die Offsetfelder enthalten `0x0019`, `0x001B` bzw. `0x001C`.

Wichtig: Diese Aufrufe dürfen nicht als normale Near-Aufrufe zu R2+0019/001B/001C interpretiert werden. Es handelt sich um Far-Aufrufe mit Segmentfeld 0 und Klasse-0/Typ-0-Relokationen. Die genaue Lader-/Laufzeitauflösung dieser Relokationsart ist noch offen. Daher werden die Zielroutinen weder benannt noch als lokale R2-Funktionen deklariert.

Der gleiche Relokationsrohwert Klasse 0 / Typ 0 kommt auch bei den R4-Aufrufen auf `0000:0186`, `0187`, `018B` und `018C` vor. Das stützt die Notwendigkeit, diese Relokationsklasse systematisch zu untersuchen, statt die Zielwerte als absolute Segmentadressen zu deuten.

## 8. ES:[0008] im Gesamtbefund
Im gesamten R2-Disassembly wurde genau ein direkter Operand `ES:[0008]` gefunden: R2+`0x0400`.
Seine nachgewiesene Rolle ist ein 16-Bit-Summand in der Bedingung für den Kopierpfad. Weitere Verwendungen oder ein symbolischer Feldname sind in DBASE.GEO nicht belegt.

## 9. Ergebnis
Gesichert:
1. R2+`0x0400` addiert das WORD `ES:[0008]` zu `CX-DX`; das Ergebnis wird mit `0x2000` verglichen.
2. R4+`0x0000` speichert BP in `ES:[0000]`, wobei ES aus einem nicht aufgelösten Aufruf `0000:0186` hervorgeht und AX zuvor aus `[SI+2]` geladen wird.
3. R4+`0x0030` speichert BP in `DS:[0002]`; R4+`0x0040`/`0x004C` stellen diesen Kontext über Rohaufrufe wieder her.
4. R4+`0x00E5` liest einen Zeiger aus dem relocationsbehafteten Segment 1 und prüft den Wert an `SS:[BX]`.
5. R2+`0x041F`, `0x0434`, `0x0457`, `0x04A6` und R4-Aufrufe auf `0000:0186` etc. verwenden Klasse-0/Typ-0-Relokationen. Ihre Zielauflösung ist weiterhin offen.

## 10. Offene Punkte und nächste Untersuchung 2469
- Relokationsklasse 0 / Typ 0 im GEODE-Format 1 anhand weiterer unabhängiger GeoWorks-1.x-Dateien untersuchen.
- DBASE-Rohziele `0000:0019`, `001B`, `001C`, `0186`, `0187`, `018B`, `018C` nur nach geklärter Relokationssemantik zuordnen.
- R2+`0x04C5` und R2+`0x056E` mit allen Lese-/Schreibzugriffen auf den ES-Kontext vergleichen.
- Die Bedeutung von `ES:[0008]` nur anhand weiterer bestätigter Verbraucher bestimmen.

## 11. Änderungsstatus
- Originalarchiv und DBASE.GEO nur gelesen.
- UI.GEO, ICON-ED.GEO und TOKEN.DB nicht verändert.
- SDK-Quellcode und GEOTEST.GEO nicht verändert.
- Kein Build und kein Laufzeittest.
