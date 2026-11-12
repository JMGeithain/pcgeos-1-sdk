# GEOTEST / PC-GEOS 1.x – Untersuchung 2466
## DBASE: Referenzzähler, aktive Liste und Freiliste
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Quellenprüfung
Originaldatei aus `GEOWORKS.zip`:
- `GEOWORKS/SYSTEM/DBASE.GEO`
- 2.930 Byte
- SHA-256 `209d45d361cff3daeb982c07d8faa4fbd3b7f86b4fbba1d18a54a78b44ed12cd`
- GEODE-Format 1, fünf Ressourcen, 23 Exporte, keine Imports.

R2: Dateioffset `0x01BE`, 1.664 Byte. R4: Dateioffset `0x0A3E`, 256 Byte.
Statische Disassemblierung mit GNU objdump (`i8086`, Intel-Syntax). Kein Laufzeittest.

## 2. Entscheidender Befund: DBASE verwaltet zwei getrennte verkettete Listen
Die Untersuchung der Routinen R2+`0x0000` bis `0x00F8` zeigt zwei Listenfelder im DBASE-Datenbereich:
- `DS:0006`: aktive Liste von Knoten.
- `DS:000A`: Freiliste wiederverwendbarer Knoten.

### 2.1 Freiliste: Entnahme R2+0x008A
R2+`0x008A` prüft `DS:000A`.
- Ist der Kopf ungleich null, wird der erste Knoten entnommen und `DS:000A` auf dessen Folgezeiger gesetzt.
- Ist die Freiliste leer, wird ein neuer Block über einen internen Speicher-/Segmentpfad angefordert und eine Reihe von Knoten vorbereitet.
- Die neu vorbereiteten Knoten werden in eine verkettete Freiliste eingehängt; `DS:000A` erhält den neuen Kopf.

Damit ist `DS:000A` der Kopf einer Knoten-Freiliste.

### 2.2 Freiliste: Rückgabe R2+0x00E2
R2+`0x00E2`:
- sichert AX und BP;
- lädt den bisherigen Freilistenkopf aus `DS:000A`;
- schreibt ihn in `[DI]`;
- setzt `DS:000A=DI`;
- lädt den BP-Kontext aus `DS:0002` und ruft die interne Kontext-Hilfsroutine auf.

Das ist die Rückgabe eines Knotens an die Freiliste. Der aktive Listenentferner R2+`0x0191` ruft diese Routine nach dem Entfernen des Knotens auf.

## 3. Aktive Liste und Knotenlayout
R2+`0x0136` hängt einen frisch entnommenen Knoten an die aktive Liste:
- liest `DS:0006`;
- schreibt den bisherigen Kopf nach `[DI]`;
- setzt `DS:0006=DI`;
- schreibt den gespeicherten Wert nach `[DI+2]`;
- initialisiert `[DI+4]=0`.

R2+`0x0191` entfernt einen Knoten aus der aktiven Liste:
- traversiert ab `DS:0006` über `[node+0]`;
- aktualisiert Vorgänger oder Kopf;
- ruft anschließend den Rohzielbereich `R2+0x018A` auf;
- gibt den Knoten über R2+`0x00E2` an die Freiliste zurück.

Belegtes Knotenlayout:

| Offset | Funktion |
|---|---|
| +0 | nächster Knoten in der aktiven Liste bzw. Freiliste |
| +2 | gespeicherter Wert/Segment- oder Handle-Kandidat; genaue Semantik offen |
| +4 | Referenz-/Nutzungszähler |

## 4. Referenzzähler: Initialisierung, Erhöhung und Verringerung
### 4.1 Initialisierung
R2+`0x0155` schreibt `0` nach `[DI+4]`, wenn ein Knoten neu in die aktive Liste eingehängt wird.

### 4.2 Erhöhung R2+0x01C0
- lädt `SI` aus `ES:0012`;
- führt `INC WORD PTR [SI+4]` aus;
- ruft danach Kontext-Hilfsroutinen R4+`0x004C` und R4+`0x0023` auf.

Zwei direkte Aufrufstellen in R2:
- R2+`0x0396`: nach dem Erzeugen/Einrichten eines neuen Knotens in der Operation ab R2+`0x035C`.
- R2+`0x043E`: nach dem Kopier-/Duplizierungspfad in R2+`0x03C5`.

### 4.3 Verringerung R2+0x01D5
- lädt `SI` aus `ES:0012`;
- führt `DEC WORD PTR [SI+4]` aus;
- bei Nichtnull: Kontextpfad R4+`0x0023`, Carry wird gelöscht;
- bei null: Kontextpfad R4+`0x004C`, BP-Kontext laden, R2+`0x0187` aufrufen, anschließend R2+`0x0191`; Carry wird gesetzt.

Zwei direkte Aufrufstellen:
- R2+`0x044C`: nach dem Erzeugen einer Ersatz-/Kopie-Version im Pfad R2+`0x03C5`.
- R2+`0x04B1`: in der allgemeinen Freigabe-/Verwaltungsroutine ab R2+`0x048B`.

### 4.4 Bedeutung
Die Kombination aus Nullinitialisierung, Erhöhung, Verringerung und Entfernen bei Zählerstand null belegt einen Referenz-/Nutzungszähler mit hoher Sicherheit.
R2+`0x03C5` prüft zusätzlich `[SI+4]` gegen 1, bevor es einen Kopierpfad auswählt. Das ist stark konsistent mit einer Shared-Resource-/Copy-on-write-Strategie. Die genaue Semantik der Anwendung und die Bedeutung des Carry-Ergebnisses sind noch anhand der Aufrufer zu bestätigen.

## 5. Wichtige Korrektur zu R2+0x018A
Die vorherige Untersuchung hatte R2+`0x018A` als Freigabe-/Verarbeitungsroutine behandelt. Die erneute Byteprüfung zeigt:
- bei R2+`0x0189` beginnt die Instruktion `MOV SI,DI` (`8B F7`);
- R2+`0x018A` liegt auf dem zweiten Byte dieser Instruktion und ist kein regulärer Instruktionsanfang.

Der Far-Aufruf auf `0000:018A` in R2+`0x01B3` darf daher nicht als normaler Funktionsaufruf interpretiert werden. Seine genaue Bedeutung hängt von den Relokations-/Laderregeln ab und bleibt offen.
Die eigentliche Rückgabe des Knotens an die Freiliste erfolgt klar erkennbar durch den anschließenden Near-Aufruf R2+`0x00E2`.

## 6. Konsequenz für die Rekonstruktion
Die DBASE-Verwaltung ist mehr als eine einzelne Liste:
- aktive Knoten werden über `DS:0006` verwaltet;
- freie, wiederverwendbare Knoten über `DS:000A`;
- Knoten werden zwischen diesen Listen verschoben;
- ein Zähler in `+4` steuert, wann ein aktiver Knoten endgültig aus der aktiven Liste entfernt und recycelt wird;
- `+2` enthält einen zusätzlichen Wert, der beim Entfernen über einen noch ungeklärten Rohaufruf verarbeitet wird.

Analytische Layout-Notiz, keine bestätigte originale C-ABI:
```c
struct DBaseNode {
    uint16_t next;          /* +0: link in active/free list */
    uint16_t value_handle;  /* +2: exact type not yet established */
    uint16_t ref_count;     /* +4: increment/decrement/test */
};
```

## 7. Nicht bewiesen
- exakter Typ und Lebenszyklus des Feldes +2;
- genaue Semantik des Far-Aufrufs auf R2+`0x018A`;
- vollständige Bedeutung der Carry-Rückgabe aus R2+`0x01D5`;
- ob alle Anwendungen die Struktur identisch verwenden;
- Laufzeitverhalten unter GeoWorks 1.2.8.

## 8. Nächster Schritt 2467
1. Die Exportaufrufer von DBASE-Exporten 0x08, 0x0C, 0x0D und 0x0E mit den Referenzzählerpfaden korrelieren.
2. R2+`0x03C5` als Ganzes analysieren, um die Shared-Resource-/Kopierentscheidung zu präzisieren.
3. Den Rohaufruf `0000:018A` anhand der Relokationsrecords und weiterer gleichartiger Aufrufmuster untersuchen.
4. Erst danach eine SDK-Notiz zu DBASE-Knoten aufnehmen; keine ABI-Namen oder Funktionssignaturen erfinden.

## 9. Änderungsstatus
- Originalarchiv und DBASE.GEO nur gelesen.
- UI.GEO, ICON-ED.GEO und TOKEN.DB nicht verändert.
- SDK-Quellcode und GEOTEST.GEO nicht verändert.
- Kein Build, kein Emulator-Laufzeittest.
