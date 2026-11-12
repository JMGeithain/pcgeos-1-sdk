# GEOTEST / PC-GEOS 1.x – Untersuchung 2464
## DBASE-interne Kontrollfluss- und Segmentzugriffsanalyse
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Quellenprüfung
Untersucht wurde DBASE.GEO direkt aus dem vom Nutzer bereitgestellten GEOWORKS.zip:
- Archivpfad: GEOWORKS/SYSTEM/DBASE.GEO
- Größe: 2.930 Byte
- SHA-256: 209d45d361cff3daeb982c07d8faa4fbd3b7f86b4fbba1d18a54a78b44ed12cd
- GEODE-Format: 1
- Ressourcen: 5
- Imports: 0
- Exporte: 23

Die Prüfsumme stimmt mit den Untersuchungen 2462 und 2463 überein. R2 hat 1.664 Bytes; R4 hat 256 Bytes.
Die Disassemblierung erfolgte statisch mit GNU objdump im Binärmodus i8086 / Intel-Syntax. Kein Laufzeittest.

## 2. Präzisierung zu DBASE-Exporten 0x10 und 0x11
Die Exporttabelle weist aus:
- Export 0x10 -> R2+0x066E
- Export 0x11 -> R2+0x0674

Die Bytefolgen an diesen Exportstellen:
- R2+0x066E: `9A 8E 01 00 00 CB` – Far-Aufruf mit Rohziel 0000:018E, danach RETF.
- R2+0x0674: `9A 8F 01 00 00 CB` – Far-Aufruf mit Rohziel 0000:018F, danach RETF.

Die Zielpositionen sind keine unabhängig beginnenden Routinen:
- R2+0x018B: `5F 5D 5A 59 58 C3`
- R2+0x018E: `59 58 C3` = POP CX; POP AX; RET
- R2+0x018F: `58 C3` = POP AX; RET
- R2+0x0190: `C3` = RET

Diese Positionen liegen im gemeinsamen Rückkehr-/Registerwiederherstellungsbereich einer größeren Routine, deren Code bei R2+0x0136 beginnt. Die Exportziele 0x10 und 0x11 zeigen somit bytegenau in diesen Epilogbereich hinein. Die Exportnamen und die beabsichtigte ABI bleiben unbekannt. Die ungewöhnliche Far-Aufruf-/Rückkehrkombination wird nicht semantisch erklärt, solange die Relokations- und Loaderregeln dafür nicht vollständig geklärt sind.

## 3. R2 – zusammenhängender Ablauf R2+0x00F9 bis R2+0x01BF
Der Bereich zeigt mehrere zusammenhängende Operationen:

### 3.1 R2+0x00F9
- Sichert AX, CX, DX und DI.
- Lädt SI aus DS:0006.
- Ruft die R2-internen Rohziele 0x0195, 0x0197 und 0x0196 auf.
- Prüft in einer Schleife einen über SI referenzierten Eintrag und addiert eine Länge auf CX.
- Vergleicht die resultierende Größe mit 0x2000.
- Ruft je nach Pfad 0x0196 auf und kehrt zurück; bei leerem SI folgt zusätzlich ein Aufruf des lokalen Bereichs R2+0x0136.

Das ist ein nachvollziehbarer Ablauf mit einer verketteten Struktur und einer 0x2000-Grenzprüfung. Eine fachliche Bezeichnung der Struktur (z.B. Heap, Objektliste oder Speicherpool) wird daraus noch nicht abgeleitet.

### 3.2 R2+0x0136
- Sichert AX, CX, DX, BP und DI.
- Ruft R2+0x008A auf.
- Verknüpft den bisherigen Kopf bei DS:0006 mit einem neuen Eintrag.
- Setzt AX auf 0x3333 und CX auf 0x0100.
- Ruft den Rohzielbereich R2+0x0188 auf.
- Speichert AX und 0 in Feldern des Eintrags.
- Ruft R2+0x0186, setzt DS auf den zurückgegebenen Wert und ruft R2+0x0018 auf.
- Schreibt DS:0010 und DS:0012.
- Ruft R2+0x018B und R2+0x0187 auf.
- Setzt SI aus DI und erreicht den gemeinsamen Epilog ab R2+0x018B.

### 3.3 R2+0x0191
- Sichert AX, DI und BX.
- Liest den Kopfzeiger aus DS:0006.
- Durchläuft eine verkettete Folge, bis ein Eintrag mit SI übereinstimmt.
- Entfernt den gefundenen Eintrag aus der Verkettung bzw. aktualisiert DS:0006, wenn der Kopf betroffen ist.
- Lädt einen Wert aus [SI+2], ruft R2+0x018A und danach R2+0x00E2 auf.
- Stellt Register wieder her und kehrt zurück.

Die Pointer-Manipulation ist sichtbar. Die genaue Bedeutung des Knotens und der Felder bleibt unbestätigt.

## 4. R4 – Segment-/BP-Kontext-Hilfsroutinen
Die folgenden Bytes sind direkt belegt:

- R4+0x0016: PUSH BP; MOV BP, ES:[0000]; CALL FAR 0000:0187; POP BP; RETF.
- R4+0x0023: PUSH BP; MOV BP, ES:[0000]; CALL FAR 0000:018B; POP BP; RETF.
- R4+0x0030: sichert AX und BP, ruft R2+0x0186, setzt DS=AX, schreibt BP nach DS:0002, stellt BP und AX wieder her, RETF.
- R4+0x0040: lädt BP aus DS:0002, ruft R2+0x0187, stellt BP wieder her, RETF.
- R4+0x004C: lädt BP aus DS:0002, ruft R2+0x018B, stellt BP wieder her, RETF.
- R4+0x0058: sichert DS, ruft R4+0x0066 und R4+0x007B, liest AX aus DS:0008, stellt DS wieder her.
- R4+0x0066: sichert AX und BP, ruft R2+0x018C und R2+0x0186, setzt DS=AX, schreibt BP nach DS:0002, stellt Register wieder her.
- R4+0x007B: lädt BP aus DS:0002, ruft R2+0x0187, stellt BP wieder her.
- R4+0x0092: sichert DS und SI, ruft R4+0x0030, lädt SI und DI aus dem über DI adressierten Datenpaar, ruft R4+0x0000 und R4+0x0040, stellt SI und DS wieder her.
- R4+0x00E5: sichert BX und DS; setzt DS vorübergehend auf 1; lädt BX aus DS:0000; testet das WORD an SS:[BX] auf 0xFFFF; falls ungleich null, lädt es nach AX; stellt DS und BX wieder her.

Die Hilfsroutinen zeigen einen gespeicherten BP-Kontext bei DS:0002 und wiederholte Zugriffe auf einen über Segment 1 / DS:0000 gewonnenen Zeiger. Der semantische Name dieses Kontexts und der Zweck des Stack-Wertes bleiben offen.

## 5. Relokations-/ABI-Vorbehalte
- Die Rohziele 0x0186 bis 0x0197 werden nicht als symbolische Funktionsnamen behandelt.
- Mehrere Aufrufziele liegen mitten in Instruktionsfolgen oder gemeinsamen Epilogen. Ein Export- oder Funktionsbeginn darf nicht allein aus einem CALL-Ziel abgeleitet werden.
- Die CALL-FAR-Bytes und ihre Relokationseinträge sind getrennt zu betrachten. Ohne vollständige Relokationssemantik darf keine endgültige Aussage zur Laufzeit-Segmentauflösung gemacht werden.
- Es wurde keine neue API-Deklaration ins SDK übernommen.

## 6. Ergebnis
Gesichert:
1. DBASE R2+0x00F9 bis R2+0x01BF enthält einen Ablauf mit verketteten Einträgen, Feldzugriffen und einer 0x2000-Grenzprüfung.
2. R2+0x0136 verknüpft einen neuen Eintrag mit dem Kopfzeiger DS:0006 und erreicht den Register-Epilog ab R2+0x018B.
3. R2+0x0191 traversiert und aktualisiert eine verkettete Struktur.
4. DBASE R4-Routinen speichern und laden einen BP-Wert über DS:0002.
5. R4+0x00E5 liest einen Zeiger aus Segment 1 / DS:0000 und testet den über SS adressierten WORD-Wert.
6. DBASE-Exporte 0x10 und 0x11 zeigen auf R2+0x018E bzw. +0x018F, also auf POP-Instruktionen im gemeinsamen Epilog und nicht auf unabhängige Routineanfänge.

Nicht bewiesen:
- Namen und Zweck der verketteten Struktur;
- ob die Datenstruktur ein Speicherpool, Objektverzeichnis oder etwas anderes ist;
- symbolische API-Namen, Parameterlisten und Rückgabeverträge;
- vollständige Semantik der Far-Aufrufe und Relokationen;
- Laufzeitverhalten in GeoWorks.

## 7. SDK-Folgerung und nächste Runde 2465
Keine Änderung am SDK-Packer, keine Änderung an GEOTEST.GEO und kein Build.
Nächster Schritt:
A. Alle Aufrufstellen der R2-Bereiche 0x0136 und 0x0191 innerhalb von DBASE.GEO und UI.GEO sammeln.
B. Die Datenstruktur um DS:0006, Felder [SI], [SI+2] und [SI+4] mit allen Schreibe-/Lesezugriffen abgleichen.
C. R2+0x0186 bis 0x0190 anhand der vollständigen Aufrufkontexte und Relokationsrecords rekonstruieren.
D. Für die R4-Routinen DS:0002 und ES:[0000] alle aufrufenden Stellen erfassen, bevor ein ABI-Kandidat formuliert wird.

Änderungsstatus:
- GEOWORKS.zip ausschließlich gelesen.
- DBASE.GEO nicht verändert.
- UI.GEO und ICON-ED.GEO nicht verändert.
- TOKEN.DB nicht verändert.
- SDK-Quelldateien und GEOTEST.GEO nicht verändert.
- Kein Emulator-Laufzeittest.
