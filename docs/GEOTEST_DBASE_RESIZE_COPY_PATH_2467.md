# GEOTEST / PC-GEOS 1.x – Untersuchung 2467
## DBASE: Analyse des Resize-/Copy-Pfads R2+03C5
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Quellen und Prüfsumme
Untersucht wurde `GEOWORKS/SYSTEM/DBASE.GEO` aus dem bereitgestellten `GEOWORKS.zip`.
- Dateigröße: 2.930 Byte
- SHA-256: `209d45d361cff3daeb982c07d8faa4fbd3b7f86b4fbba1d18a54a78b44ed12cd`
- GEODE-Format 1; fünf Ressourcen; 23 Exporte; keine Imports.
- R2: Dateioffset `0x01BE`, Länge 1.664 Byte.

Die Analyse basiert auf statischer 8086-Disassemblierung (GNU objdump, Intel-Syntax). Kein Laufzeittest.

## 2. Einstieg und Parameterrahmen
DBASE-Export 0x07 liegt bei R2+`0x03BD` und ist ein dünner Wrapper:
- sichert AX und SI;
- ruft R2+`0x03C5` auf;
- stellt SI und AX wieder her;
- kehrt mit `RETF` zurück.

R2+`0x03C5` sichert CX, DX, BX, BP und DI und beginnt mit den R4-Hilfsroutinen R4+`0x00E5` und R4+`0x0030`. Anschließend:
- `SI = [DI]` – der bisherige Knoten-/Wertbezug aus dem DBASE-Kontext;
- `AX = [DI+2]` – der im Knoten gespeicherte Wert;
- R4+`0x0000` wird aufgerufen, danach wird der zurückgelieferte Wert über `BX` weiterverwendet;
- aus einem über ES adressierten Deskriptor wird eine Größeninformation in `DX` ermittelt.

Die exakte Typdefinition des Deskriptors und die formale Bedeutung aller Eingaberegister sind nicht bekannt. Deshalb werden CX und DX im Bericht nur als Größen-/Längenwerte im beobachteten Pfad beschrieben, nicht als bestätigte API-Parameter.

## 3. Die Entscheidung bei R2+03F2 bis 0409
Der zentrale Kontrollfluss lautet:
- `CMP CX,DX`; bei `CX <= DX` Sprung zum Pfad ohne Kopie.
- `CMP WORD PTR [SI+4],1`; bei Zählerstand 1 Sprung zum Pfad ohne Kopie.
- andernfalls wird `BP = CX - DX + WORD PTR ES:[0008]` berechnet.
- `CMP BP,0x2000`; bei `BP <= 0x2000` Sprung zum Pfad ohne Kopie.
- nur wenn alle drei Prüfungen den Kopierpfad zulassen, wird R2+`0x00F9` aufgerufen und eine neue Daten-/Knotenressource aufgebaut.

Damit ist die Entscheidung präziser als eine pauschale Copy-on-write-Regel:
1. Die angeforderte Größe muss größer als die bisherige Größe sein.
2. Der Knoten muss geteilt/genutzt sein (Zählerstand nicht 1).
3. Der aus Wachstum und `ES:0008` berechnete Summenwert muss über `0x2000` liegen.

Die dritte Bedingung ist ein echter Schwellenwerttest. Was `ES:0008` im übergeordneten Speicher-/Segmentkontext genau zählt, ist noch nicht abschließend bestimmt. Daher darf `0x2000` nicht ohne weitere Belege als generelle GEOS-Grenze oder maximale Dokumentgröße bezeichnet werden.

## 4. Kopierpfad R2+040B bis 044F
Im Kopierpfad:
- R2+`0x00F9` wird aufgerufen, um einen neuen Eintrag/Ressourcenbereich zu beschaffen.
- Der alte SI-Bezug wird in den neuen Eintrag geschrieben (`[DI]=SI`).
- Über R4+`0x0000` und einen Kernel-/Speicheraufruf wird ein neuer Speicherbereich eingerichtet.
- Die Routine richtet DS/ES und DI/SI für den Transfer ein.
- `CX` wird auf `DX` gesetzt; `REP MOVSB` kopiert genau DX Bytes aus dem bisherigen Bereich in den neuen Bereich.
- Nach dem Kopieren wird eine interne Routine R2+`0x001B` aufgerufen.
- R2+`0x01C0` erhöht den Zähler des neuen Knotens.
- R4+`0x0016` liefert/aktualisiert den zugehörigen Segmentkontext.
- `[DI+2]` wird mit dem neuen Wert beschrieben.
- R2+`0x01D5` vermindert den Zähler des alten Knotens und kann bei null dessen Entfernung aus der aktiven Liste auslösen.

Das belegt einen Pfad, der bei bestimmten Wachstumsbedingungen eine neue Kopie des bisherigen Dateninhalts anlegt und die Referenzierung vom alten Knoten auf den neuen umstellt. Die Daten werden dabei nicht einfach nur vergrößert: die beobachtete Kopie umfasst DX Bytes; die genaue Semantik des nachfolgenden Speicher-/Segmentaufrufs bleibt teilweise offen.

## 5. Pfad ohne Kopie R2+0451 bis 046A
Wenn eine der drei Bedingungen aus Abschnitt 3 zutrifft, wird kein neuer Kopierblock angelegt. Stattdessen:
- DS/ES werden für den vorhandenen Segmentkontext umgestellt;
- R2+`0x001C` wird aufgerufen;
- der aktuelle Kontext wird über R4+`0x0023`, R4+`0x0016` und R4+`0x0040` wiederhergestellt.

Das ist mit einer Anpassung/Erweiterung im bestehenden Speicherbereich vereinbar. Ob der Aufruf R2+`0x001C` selbst eine Reallokation durchführt, muss separat untersucht werden; aus diesem Kontrollfluss allein folgt es nicht.

## 6. Zweiter Aufrufer: R2+04C5
R2+`0x04C5` ist ein weiterer relevanter Aufrufer von R2+`0x03C5` (CALL bei R2+`0x0514`). Er berechnet zuvor zusätzliche Längenwerte, ruft R2+`0x03C5` auf und arbeitet anschließend mit R4+`0x0092` sowie einem Rückwärts-Kopierpfad (`STD` / `REP MOVSB`) und Nullfüllung (`REP STOSB`).

Dieser Aufrufer zeigt, dass R2+`0x03C5` in einen umfassenderen Größenänderungs-/Datenverschiebungsablauf eingebettet ist. Es ist nicht nur ein allgemeiner „Clone“-Aufruf, sondern ein Teil der Verwaltung eines Speicherbereichs, dessen Nutzdaten anschließend verschoben und/oder erweitert werden.

## 7. Vorläufige Einordnung
Durch die Kombination aus:
- Knoten-Referenzzähler bei `+4`,
- Prüfung auf Zählerstand 1,
- Größenvergleich `CX` gegen `DX`,
- Schwellenwertvergleich gegen `0x2000`,
- bedingtem Anlegen einer neuen Kopie und Umhängen der Referenz,

ist eine geteilte Speicherressource mit bedingter Kopie sehr gut gestützt. Der Begriff „Copy-on-write“ ist als technische Kurzbeschreibung plausibel, aber noch keine nachgewiesene originale API-Bezeichnung.

## 8. Wichtige offene Punkte
- Was genau bezeichnet `ES:0008`?
- Was ist die genaue Datenstruktur, die R4+`0x0000` über DI/AX/CX anspricht?
- Welche Operation führt R2+`0x001C` im Pfad ohne Kopie aus?
- Welche Funktion hat R2+`0x001B` nach dem Kopieren?
- Ist `0x2000` eine lokale Optimierungsschwelle, eine Segment-/Heap-Grenze oder etwas anderes?
- Wie verhalten sich die Aufrufer bei Fehlern und Carry-Rückgaben?

## 9. Konsequenz für das SDK / GEOTEST
Noch keine API-Deklaration oder C-Struktur in das SDK übernehmen. Insbesondere keine Funktion als `resize`, `clone` oder `copy_on_write` benennen, solange Exportnamen und ABI nicht bestätigt sind.

Nächste Untersuchung 2468:
1. R2+`0x001B` und R2+`0x001C` disassemblieren und ihre Aufrufkontexte vergleichen.
2. R4+`0x0000` und R4+`0x00E5` vollständig mit allen Callern analysieren.
3. Alle Zugriffe auf `ES:0008` in DBASE.GEO sammeln.
4. Die Kopier-/Erweiterungspfade in R2+`0x04C5` und R2+`0x056E` gegenüberstellen.

## 10. Änderungsstatus
- `GEOWORKS.zip` und `DBASE.GEO` nur gelesen.
- `UI.GEO`, `ICON-ED.GEO`, `TOKEN.DB` nicht verändert.
- SDK-Quellcode und `GEOTEST.GEO` nicht verändert.
- Kein Build, kein Emulator-Laufzeittest.
