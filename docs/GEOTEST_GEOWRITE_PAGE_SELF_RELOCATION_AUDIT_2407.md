# GeoWrite 1.x – Auflösung aller Seiten-Relokationen (Untersuchung 2407)

## Kernergebnis

Alle drei variablen Relokationsfelder je GeoWrite-Seitenblock in `SOLAR_DE.000` lösen auf genau denselben VM-Block auf, in dem das jeweilige Feld gespeichert ist. Es handelt sich um Selbstreferenzen auf den eigenen Seitenblock.

Dies wurde für alle 21 Seiten durch Berechnung des VM-Blocktabellen-Offsets und anschließenden Vergleich mit dem jeweiligen Seiten-VM-Handle geprüft.

## Verwendete Definition

Die historische Routine `RelocToVMBlock` in `convertText.asm` führt aus:

```asm
and ax, mask RID_INDEX
mov dx, size VMBlockHandle
mul dx
add ax, offset VMH_blockTable
```

Im untersuchten VM-Header beginnt die Blocktabelle bei Offset `002Ch`. Die Größe eines VM-Blocktabelleneintrags beträgt 12 Bytes. Damit gilt für diese Datei:

`VM-Blocktabellen-Offset = 002Ch + RID_INDEX * 0Ch`.

Die so berechnete Position ist zugleich das VM-Blockhandle (Tabellenoffset), das in der Seitenliste gespeichert ist.

## Vollständige Prüfung

| Seite | Seiten-VM-Handle | RID-Wert (alle 3 Felder) | RID_INDEX | berechneter Tabellenoffset | Ergebnis |
|---:|---:|---:|---:|---:|---|
| 1 | `005Ch` | `7004h` | `004h` | `005Ch` | Selbstreferenz |
| 2 | `0380h` | `7047h` | `047h` | `0380h` | Selbstreferenz |
| 3 | `0398h` | `7049h` | `049h` | `0398h` | Selbstreferenz |
| 4 | `03B0h` | `704Bh` | `04Bh` | `03B0h` | Selbstreferenz |
| 5 | `03C8h` | `704Dh` | `04Dh` | `03C8h` | Selbstreferenz |
| 6 | `03E0h` | `704Fh` | `04Fh` | `03E0h` | Selbstreferenz |
| 7 | `03F8h` | `7051h` | `051h` | `03F8h` | Selbstreferenz |
| 8 | `0410h` | `7053h` | `053h` | `0410h` | Selbstreferenz |
| 9 | `0428h` | `7055h` | `055h` | `0428h` | Selbstreferenz |
| 10 | `0440h` | `7057h` | `057h` | `0440h` | Selbstreferenz |
| 11 | `0458h` | `7059h` | `059h` | `0458h` | Selbstreferenz |
| 12 | `0470h` | `705Bh` | `05Bh` | `0470h` | Selbstreferenz |
| 13 | `0488h` | `705Dh` | `05Dh` | `0488h` | Selbstreferenz |
| 14 | `04A0h` | `705Fh` | `05Fh` | `04A0h` | Selbstreferenz |
| 15 | `04B8h` | `7061h` | `061h` | `04B8h` | Selbstreferenz |
| 16 | `04D0h` | `7063h` | `063h` | `04D0h` | Selbstreferenz |
| 17 | `04E8h` | `7065h` | `065h` | `04E8h` | Selbstreferenz |
| 18 | `0500h` | `7067h` | `067h` | `0500h` | Selbstreferenz |
| 19 | `0518h` | `7069h` | `069h` | `0518h` | Selbstreferenz |
| 20 | `0530h` | `706Bh` | `06Bh` | `0530h` | Selbstreferenz |
| 21 | `0548h` | `706Dh` | `06Dh` | `0548h` | Selbstreferenz |

Die drei Felder pro Seite befinden sich bei:
- Chunk `0022h`, Payload-Offset `0x4C`
- Chunk `0022h`, Payload-Offset `0x56`
- Chunk `0030h`, Payload-Offset `0x17`

Für jede Seite wurden die drei WORD-Werte identisch gelesen. Alle 63 Relokationsfelder (21 Seiten × 3 Felder) ergeben die oben gezeigte Selbstreferenz.

## Technische Bedeutung

Die vorher unbekannten Werte sind damit nicht Verweise auf andere Seiten oder andere VM-Blöcke. Sie sind `ORS_NON_STATE_VM`-Relokationskennungen, deren Index jeweils den eigenen Seitenblock bezeichnet.

Das erklärt auch, weshalb sich der Index zwischen den Seiten ändert: Jeder Seitenblock hat einen anderen Eintrag in der VM-Blocktabelle. Die Werte sind deshalb an die konkrete VM-Blocktabellenanordnung des Dokuments gebunden.

## Konsequenz für GEOTEST.GEO

Ein Generator darf diese Werte nicht aus `SOLAR_DE.000` unverändert übernehmen, wenn er eine andere VM-Blocktabellenanordnung erzeugt. Für jede Seite müssen die drei Selbstreferenzen aus dem tatsächlichen VM-Blockhandle bzw. dessen Tabellenindex neu gebildet werden.

Das ist eine wichtige konkrete Generatorregel. Noch nicht geklärt sind die Bedeutungen der übrigen Bytes in den Chunks `0022h` und `0030h`, insbesondere die vollständige Objektstruktur und die Rolle der zusätzlichen Felder.

## Reproduzierbarkeit und Grenzen

- Eingabe: `SOLAR_DE.000` aus `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`.
- Parser: `vm1.py` aus demselben Archiv.
- Quelltext: `convertText.asm`, Routine `RelocToVMBlock`; `object.def`, Definition `ObjRelocationID`.
- Geprüft: 21 Seiten-VM-Handles, drei Relokationsfelder je Seite, 63 erfolgreiche Selbstzuordnungen.
- Methode: statische Byte- und Tabellenanalyse. Kein GeoWrite-Laufzeittest.
