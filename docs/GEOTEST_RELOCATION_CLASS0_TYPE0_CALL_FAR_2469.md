# GEOTEST / PC-GEOS 1.x – Untersuchung 2469
## Relokationsklasse 0 / Typ 0: Zuordnung zu CALL FAR-Offsetfeldern
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Fragestellung
Untersucht wurde, ob Relokationsrecords mit `source/class = 0` und `type = 0` in GeoWorks-1.x-GEODEs an wiederkehrenden Maschineninstruktionen auftreten. Vergleichsdateien:
- `GEOWORKS/SYSTEM/DBASE.GEO`
- `GEOWORKS/SYSTEM/UI.GEO`
- `GEOWORKS/WORLD/ICON-ED.GEO`

## 2. Quellenidentität
Alle drei Dateien wurden direkt aus dem bereitgestellten `GEOWORKS.zip` extrahiert.

| Datei | Größe | SHA-256 |
|---|---:|---|
| DBASE.GEO | 2.930 | `209d45d361cff3daeb982c07d8faa4fbd3b7f86b4fbba1d18a78b44ed12cd` |
| UI.GEO | 87.900 | `13a3a82ec3d4373b120890a11eb09b3a9f9ec456ca633819728f53c07883c73a` |
| ICON-ED.GEO | 47.648 | `afbbd1d8115c82162e8d3c9331c5d945e073e0823852bb5c68055ba6148df064` |

Alle Dateien besitzen die GEODE-Format-1-Signatur `C7 45 CF 53`.
Die Ressourcentabellen und Relokationsrecords wurden mit einem bounds-geprüften Parser nach dem im Repository vorhandenen `pcgeos1/geode.py`-Schema ausgewertet. Die Bytepositionen wurden zusätzlich direkt in den Ressourcendaten kontrolliert.

## 3. Häufigkeit
| Datei | Relokationen insgesamt | Klasse 0 / Typ 0 |
|---|---:|---:|
| DBASE.GEO | 125 | 67 |
| UI.GEO | 2.884 | 1.125 |
| ICON-ED.GEO | 124 | 48 |
| **Summe** | **3.133** | **1.240** |

Alle 1.240 Klasse-0/Typ-0-Records wurden einzeln auf ihre Position im Maschinencode geprüft.

## 4. Bytegenauer Befund
Bei **allen 1.240 von 1.240** Einträgen gilt:
- Das Relokationsziel zeigt auf das erste Byte des 16-Bit-Offsetoperanden einer `CALL FAR`-Instruktion.
- Unmittelbar ein Byte vor der Relokationsstelle steht der Opcode `0x9A`.
- Das Relokationsfeld enthält den 16-Bit-Offsetwert.
- Der nachfolgende 16-Bit-Wert ist das Segmentfeld der Far-Instruktion.

Das Maschinenformat lautet:

```text
9A  oo oo  ss ss
|  |     |
|  |     +-- 16-bit Segmentfeld
|  +-------- 16-bit Offsetoperand (Relokationsstelle)
+----------- CALL FAR opcode
```

Damit ist die konkrete Codeposition der Klasse-0/Typ-0-Relokation eindeutig: Sie markiert den Offsetoperand eines Far-Aufrufs und nicht dessen Segmentwort.

## 5. Ressourcendetails
### DBASE.GEO
- R2: 56 Klasse-0/Typ-0-Records
- R3: 2
- R4: 9
- Summe: 67

### UI.GEO
Die Records sind über 24 Ressourcen verteilt:
- R2 116, R3 110, R4 17, R5 69, R6 74, R7 77, R8 78, R9 65,
- R10 69, R11 111, R12 14, R13 4, R14 67, R15 11, R16 34,
- R17 3, R18 2, R19 32, R20 8, R21 76, R22 26, R23 50, R24 2, R26 10.
Summe: 1.125.

### ICON-ED.GEO
- R2: 48 Klasse-0/Typ-0-Records.
- Die übrigen Ressourcen enthalten keine Klasse-0/Typ-0-Records.
- Summe: 48.

## 6. Segmentfeld: wichtige Differenz
Das Segmentfeld der Far-Instruktion ist nicht durch einen unmittelbar benachbarten Relokationsrecord markiert. In DBASE.GEO und ICON-ED.GEO ist es bei allen erfassten CALL FAR-Beispielen null.

In UI.GEO sind 8 von 1.125 Fällen anders: Das Segmentfeld enthält einen nichtnulligen Literalwert. Die acht Fundstellen liegen in UI-Ressourcen R9, R10, R14, R16 und R19; die Literalwerte sind:
- R9+0x007A: Segment 0x0950
- R9+0x0088: Segment 0x0F20
- R10+0x1347: Segment 0x0E3C
- R14+0x00DC: Segment 0x0F68
- R14+0x038C: Segment 0x0E84
- R16+0x037D: Segment 0x0F98
- R19+0x020D: Segment 0x0F44
- R19+0x0266: Segment 0x0FA4

Die Werte sind im Binärbestand als Literalwerte vorhanden. Ihre Laufzeitbedeutung ist nicht geklärt; sie werden nicht als absolute Segmentadressen interpretiert.

Es wurde bei keinem der 1.240 Fälle ein separater Relokationsrecord genau auf dem Segmentwort (+2 relativ zum Offsetoperanden) gefunden.

## 7. Was damit bewiesen ist – und was nicht
### Bewiesen
1. Klasse 0 / Typ 0 markiert in allen drei geprüften GEODE-1-Dateien den Offsetoperanden einer CALL FAR-Instruktion.
2. Der Befund ist nicht auf DBASE.GEO beschränkt, sondern tritt in UI.GEO und ICON-ED.GEO wieder auf.
3. Insgesamt wurden 1.240 solche Stellen bytegenau bestätigt.
4. Das Segmentwort ist ein getrenntes Feld und besitzt in diesen Fällen keinen eigenen benachbarten Relokationsrecord.

### Nicht bewiesen
- die genaue Loader-/Linkeraktion, die der Relokationsrecord auslöst;
- ob und wie der Offset zur Ladezeit verändert wird;
- die allgemeine Bedeutung von source=0, type=0 außerhalb der untersuchten Far-Aufrufstellen;
- die Bedeutung der acht nichtnulligen UI-Segmentliterale;
- die symbolischen Namen oder ABI-Verträge der aufgerufenen Ziele.

Der Bericht beschreibt daher die nachgewiesene Platzierung des Records, nicht eine vollständige semantische Spezifikation der Relokationsart.

## 8. Konsequenz für GEOTEST und SDK
Der GEODE-Parser kann Klasse-0/Typ-0-Records künftig zusätzlich als „Relokation am CALL FAR-Offsetoperand“ annotieren, sofern die Byteprüfung `resource[offset-1] == 0x9A` erfüllt. Das wäre eine abgeleitete Diagnose, keine Änderung der Parsersemantik.

Noch keine Änderung am Parser oder Packer:
- keine Umdeutung des Records in einen benannten Import;
- keine automatische Segmentberechnung;
- keine Veränderung der Offsetwerte;
- keine neue ABI-Deklaration.

Für einen späteren Loader-/Packer-Schritt muss zuerst die tatsächliche Relokationswirkung geklärt werden.

## 9. Nächste Untersuchung 2470
1. Klasse-0/Typ-0-Records in weiteren GeoWorks-1.x-GEODEs vergleichen, insbesondere Kernel-/Treiberdateien aus demselben Archiv.
2. CALL-FAR-Offsetwerte und Exporttabellen der referenzierten GEODEs korrelieren, ohne daraus ungeprüft Exportordinale abzuleiten.
3. Die acht nichtnulligen UI-Segmentliterale separat untersuchen.
4. Prüfen, ob ein und derselbe Relokationsrecord im GEODE-Format in mehreren Kontexten auftreten kann.

## 10. Änderungsstatus
- `GEOWORKS.zip` nur gelesen.
- DBASE.GEO, UI.GEO und ICON-ED.GEO nicht verändert.
- TOKEN.DB nicht verändert.
- SDK-Quelldateien und GEOTEST.GEO nicht verändert.
- Kein Build und kein Laufzeittest.
