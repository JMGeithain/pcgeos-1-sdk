# GEOTEST / PC-GEOS 1.x – Untersuchung 2465
## DBASE: Listenstruktur, Referenzzähler und Aufrufkontexte
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Quellen und Methode
Untersucht wurden die Originaldateien aus dem vom Nutzer bereitgestellten `GEOWORKS.zip`:
- `GEOWORKS/SYSTEM/DBASE.GEO`
- Größe: 2.930 Byte
- SHA-256: `209d45d361cff3daeb982c07d8faa4fbd3b7f86b4fbba1d18a54a78b44ed12cd`
- GEODE-Format 1, fünf Ressourcen, 23 Exporte, keine Imports.

Ressourcenbezug:
- R2 beginnt bei Dateioffset `0x01BE`, Länge 1.664 Byte.
- R4 beginnt bei Dateioffset `0x0A3E`, Länge 256 Byte.

Die Disassemblierung erfolgte mit GNU objdump, Binärmodus i8086, Intel-Syntax. Ausschließlich statische Analyse; kein Emulator- oder GeoWorks-Laufzeittest.

## 2. R2+0x0191: Listenentfernung und Aufrufer
R2+0x0191 entfernt einen Eintrag aus einer verketteten Struktur, deren Kopfzeiger bei `DS:0006` liegt:
- `0194`: `mov di, [0006]` – Listenanfang laden.
- `0198`: Vergleich des aktuellen Knotens mit `SI`.
- `019C–01A2`: Vorgänger in `BX` merken, Folgezeiger aus `[DI]` laden und weitersuchen.
- `01A4–01A8`: Folgezeiger des Vorgängers auf den Nachfolger setzen.
- `01AA–01AC`: falls der Knoten der Kopf ist, `DS:0006` auf den Nachfolger setzen.
- `01B0`: Wert aus `[SI+2]` laden.
- `01B3`: Aufruf R2+0x018A.
- `01B8–01BA`: `DI=SI`, anschließend Aufruf R2+0x00E2.
- `01BD–01BF`: Registerwiederherstellung und Rückkehr.

Direkte Aufrufstellen:
- R2+0x032A: Fehler-/Abbruchpfad einer größeren Operation, danach Fehlerwert `AX=0x0106` und Carry setzen.
- R2+0x034E: Pfad eines Export-Wrappers; danach Aufruf R4+0x00C3.

Die Aufrufkontexte stützen Listenentfernung und Freigabepfad. Ein symbolischer API-Name ist unbekannt.

## 3. Knotenlayout: belegte Felder
### Offset +0: Verkettungszeiger
- R2+0x0136 schreibt den bisherigen Kopf `DS:0006` nach `[DI]` und setzt danach `DS:0006=DI`.
- R2+0x0191 liest den Nachfolger aus `[DI]` und verändert beim Entfernen den Vorgängerzeiger.
- Damit ist `[node+0]` als Folgezeiger gesichert.

### Offset +2: gespeicherter Wert/Handle-Kandidat
- R2+0x0136 schreibt einen zurückgegebenen AX-Wert nach `[DI+2]`.
- R2+0x0191 liest `[SI+2]`, übergibt ihn an R2+0x018A und entfernt anschließend den Knoten über R2+0x00E2.
- Weitere DBASE-Routinen lesen `[DI+2]` bzw. `[SI+2]` zur Übergabe an interne Segment-/Kontext-Helfer.

Gesichert ist ein gespeicherter Wert, der beim Entfernen gesondert verarbeitet/freigegeben wird. Ob es exakt ein Segment, Handle oder anderer Ressourcenbezeichner ist, bleibt offen.

### Offset +4: Referenz-/Nutzungszähler-Kandidat
Drei Stellen verwenden dasselbe Feld:
- R2+0x01C6: `inc word ptr [si+4]`
- R2+0x01DC: `dec word ptr [si+4]`
- R2+0x03F6: `cmp word ptr [si+4], 1`

R2+0x01D5 dekrementiert `[SI+4]`. Bei Nichtnull folgt ein alternativer Rückkehrpfad; bei Null werden Kontext-/Listenoperationen ausgeführt und R2+0x0191 aufgerufen. Damit ist `[node+4]` mit hoher Sicherheit ein Referenz- oder Nutzungszähler. Die genaue Lebenszyklussemantik bleibt zu prüfen.

## 4. Referenzzähler-Kontext R2+0x01C0 / R2+0x01D5
### Erhöhung
R2+0x01C0:
- lädt `SI` aus `ES:0012`;
- erhöht `[SI+4]`;
- ruft R4+0x004C und R4+0x0023;
- stellt SI wieder her.

### Verringerung
R2+0x01D5:
- lädt `SI` aus `ES:0012`;
- dekrementiert `[SI+4]`;
- bei Nichtnull: ruft R4+0x0023 und kehrt mit gelöschtem Carry zurück;
- bei Null: ruft R4+0x004C, lädt BP aus `ES:0000`, ruft R2+0x0187 und danach R2+0x0191, und kehrt mit gesetztem Carry zurück.

Der Carry-Zustand unterscheidet die beiden Pfade. Ob er beim Aufrufer formal eine Freigabe-/Zerstörungsanzeige darstellt, muss anhand aller Aufrufer bestätigt werden.

## 5. Zusätzlicher Kontext R2+0x03C5 und R2+0x048B
R2+0x03C5 prüft `[SI+4]` gegen 1, bevor ein größerer Speicher-/Kopierpfad gewählt wird. In einem Pfad wird R2+0x00F9 aufgerufen. Das ist konsistent mit einer Entscheidung abhängig von der Zahl der Verwendungen, beweist aber keine konkrete Copy-on-write- oder Speicherverwaltungssemantik.

R2+0x048B lädt den Nachfolger aus `[DI]`, den gespeicherten Wert aus `[DI+2]` und verarbeitet beides mit R4-Hilfsroutinen.

## 6. Vorläufiges Layout
| Offset | Beobachtete Verwendung | Bewertung |
|---|---|---|
| +0 | Folgezeiger der Liste | gesichert |
| +2 | gespeicherter Wert, beim Entfernen an R2+0x018A übergeben | gesichert; Typ offen |
| +4 | INC, DEC und CMP gegen 1 | sehr wahrscheinlich Referenz-/Nutzungszähler |

Der Listen-Kopf liegt bei `DS:0006`.

## 7. Grenzen
Nicht bewiesen sind symbolische Namen, genauer Typ von `+2`, Initialwert und vollständige Lebenszyklussemantik von `+4`, vollständige Segment-/BP-Semantik sowie Laufzeitverhalten unter GeoWorks 1.2.8. Es werden keine unbestätigten API-Namen oder Strukturdefinitionen ins SDK übernommen.

## 8. Ergebnis und nächste Untersuchung 2466
1. DBASE verwaltet über `DS:0006` eine verkettete Liste.
2. Knotenfeld `+0` ist der Folgezeiger.
3. Knotenfeld `+2` enthält einen gesondert verarbeiteten Wert/Handle-Kandidaten.
4. Knotenfeld `+4` wird inkrementiert, dekrementiert und gegen 1 geprüft; Referenz-/Nutzungszähler ist die belastbare Arbeitshypothese.
5. Bei Zählerstand null wird der Knoten aus der Liste entfernt und der Wert aus `+2` gesondert verarbeitet.

Nächste Runde:
- alle DBASE-Aufrufer von R2+0x01C0 und R2+0x01D5 erfassen;
- Initialisierung und sämtliche Schreibstellen von `[node+4]` suchen;
- R2+0x018A und R2+0x00E2 genauer untersuchen;
- R4+0x00C3/0x00D4 im Aufrufer R2+0x034D klären;
- erst danach eine vorläufige C-Struktur oder ABI-Notiz formulieren.

## 9. Änderungsstatus
- `GEOWORKS.zip` nur gelesen.
- `DBASE.GEO`, `UI.GEO`, `ICON-ED.GEO` nicht verändert.
- `TOKEN.DB` nicht verändert.
- SDK-Quellcode und `GEOTEST.GEO` nicht verändert.
- Kein Build und kein Laufzeittest.
