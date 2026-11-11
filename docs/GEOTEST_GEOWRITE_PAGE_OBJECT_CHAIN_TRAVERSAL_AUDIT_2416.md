# GeoWrite 1.x – Ablauf der Seitenobjektkette (Untersuchung 2416)

## Ziel

Den vom historischen 1.x-Konverter verwendeten Ablauf durch die Seitenobjekte nachvollziehen und klar trennen zwischen:
- direkt im Assembler belegter Traversierungslogik,
- durch weitere Definitionen erklärter Relokationsbehandlung,
- noch nicht geklärten konkreten Byteoffsets in den alten Objektinstanzen.

## Primärquellen

- `Source/showcase-format/public-source/convertGeoWrite.asm` (lokal gespiegelt unter `/mnt/data/audit2407/convertGeoWrite.asm`)
- `Source/showcase-format/public-source/convertText.asm` (lokal gespiegelt unter `/mnt/data/audit2407/convertText.asm`)
- `Source/showcase-format/public-source/convertText.def`
- `object.def`
- Originaldokumente `NEUES_DO.000`, `LEERER_B.000`, `TESTWRIT.000` als Binärvergleichsbasis.

Die Analyse ist statisch. Es wurde kein GeoWorks-Laufzeittest durchgeführt.

## 1. Tatsächlicher Ablauf in ConvertOldGeoWriteDocument

Die Routine `ConvertOldGeoWriteDocument` arbeitet pro Element der 1.x-Seitenarray-Struktur:

1. Sie liest aus dem Map-Block den VM-Blockhandle der Seite (`GW12_PAE_vmBlock`).
2. Sie sperrt diesen Seitenblock mit `ourVMLockDS`.
3. Sie liest aus dem Seitenblock den Chunk `GW12_PageContent`.
4. Sie addiert `Vis_offset` und liest aus `VCI_comp.CP_firstChild.offset` den ersten Kindzeiger. Der Kommentar im Code bezeichnet dieses Objekt als Header.
5. Beim ersten Seitenaufruf übergibt sie das Headerobjekt an `ConvertOldTextObject`.
6. Vom Headerobjekt liest sie nach Addition von `Vis_offset` das Feld `VI_link.LP_next.offset`; der Kommentar bezeichnet das Ziel als Footer.
7. Beim ersten Seitenaufruf wird auch dieses Footerobjekt an `ConvertOldTextObject` übergeben.
8. Danach folgt die Schleife für den Haupttext: Sie liest vom aktuellen Objekt den vollständigen `VI_link.LP_next`-Wert, entsperrt den alten VM-Block, prüft das Parent-Kennzeichen, löst andernfalls den VM-Relokationsindex auf, sperrt den referenzierten VM-Block und übergibt das Spaltenobjekt an `ConvertOldTextObject`.
9. Die Schleife wiederholt sich, bis das Parent-Kennzeichen gesetzt ist; danach beginnt die nächste Seite.

Der Code belegt also die logische Folge **PageContent → erstes Kind/Header → Footer → nachfolgende Spaltenobjekte → Parent-Endmarkierung**. Header und Footer werden nur einmal konvertiert (erste Seite); Spaltenobjekte werden innerhalb der Seitenschleife verarbeitet.

## 2. Offset- und Zeigerbehandlung

Der Code unterscheidet bewusst zwischen zwei Fällen:

- `CP_firstChild.offset` und `LP_next.offset` werden als Offset innerhalb des aktuellen gesperrten Seitenblocks verwendet.
- Das vollständige `LP_next`-Feld wird als DWORD in `ax:si` geladen. Nach dem Entsperren wird der VM-Relokationsindex über `RelocToVMBlock` in einen Eintrag der VM-Block-Handle-Tabelle umgesetzt.

Die Routine `RelocToVMBlock` in `convertText.asm` führt dabei exakt folgende Operationen aus:
- Nullwert bleibt Null.
- `RID_INDEX` wird aus dem Relocation-Identifier maskiert.
- Der Index wird mit `size VMBlockHandle` multipliziert.
- Dazu wird `offset VMH_blockTable` addiert.

Damit ist die im früheren Dossier verwendete Tabellenrechnung belegt. Die Routine allein erklärt aber nicht, welche Objektfelder in jedem Dokument welche Relocation-Quelle verwenden; dafür müssen Relocation-ID und Feldkontext gemeinsam betrachtet werden.

## 3. Bedeutung der Parent-Endmarkierung

Der Haupttext-Loop prüft nach dem Laden des nächsten Linkwerts:

```asm
test si, LP_IS_PARENT
jnz nextPage
```

Das ist ein expliziter Kontrollflussbeleg: Ein als Parent markierter Link beendet die Spaltenobjekt-Schleife. Der Konverter behandelt dieses Bit nicht als VM-Blockindex oder Chunkhandle. Die konkrete Semantik der gesamten Linkstruktur muss weiterhin aus der passenden 1.x-Definition stammen; die hier vorliegenden Quelltextstellen zeigen jedenfalls, wie der Konverter das Bit benutzt.

## 4. Was die Quelle nicht beweist

Die Routine belegt die Feldnamen und die Traversierungsreihenfolge, aber sie liefert nicht allein:
- die vollständigen Byteoffsets der Felder `CP_firstChild` und `LP_next` in jeder konkreten alten Instanz;
- eine vollständige Definition aller beteiligten `VisComp`- und `VisLink`-Strukturen;
- die genaue Semantik jedes weiteren Seitenchunks;
- dass ein beliebiger Seitenblock ohne die restlichen Objekt-/Layoutdaten gültig wäre.

Die im früheren Arbeitsstand beobachteten Relocation-IDs in Chunk `005Ch/0022h` sind deshalb nicht ohne zusätzliche Strukturzuordnung pauschal als `firstChild` oder `LP_next` zu etikettieren.

## 5. Konsequenz für GEOTEST

Ein sicherer Dokumentprototyp muss die bestehende Objektkette erhalten. Insbesondere:
- den Seiten-Content-Knoten,
- den Header- und Footer-Link,
- die Haupttext-/Spaltenobjekte,
- die vollständigen VM-Relokationskennungen,
- das Parent-Endkennzeichen.

Für den ersten GEOTEST-Prototyp ist das Kopieren eines verifizierten kleinen GeoWrite-1.x-Templates mit anschließender kontrollierter Änderung des Textstroms weiterhin risikoärmer als der Neuaufbau der Seitenobjektkette. Dabei müssen die zugehörigen RunArrays, Format-Elemente und VM-Referenzen konsistent bleiben.

## Nicht durchgeführt

- Kein neuer Dokumentgenerator erstellt.
- Keine Originaldatei verändert.
- Kein GeoWorks-Laufzeittest.
- Keine ungesicherten Byteoffsets für `CP_firstChild` oder `LP_next` behauptet.

## Reproduzierbarkeit

Die Traversierungsreihenfolge ist direkt in `ConvertOldGeoWriteDocument` in `convertGeoWrite.asm` nachlesbar. Die Relokationsindex-Umrechnung steht in `RelocToVMBlock` in `convertText.asm`. Die beschriebenen Grenzen folgen daraus, dass die vollständigen 1.x-Objektstrukturdefinitionen für alle Felder im derzeitigen Quellmaterial nicht vorliegen.
