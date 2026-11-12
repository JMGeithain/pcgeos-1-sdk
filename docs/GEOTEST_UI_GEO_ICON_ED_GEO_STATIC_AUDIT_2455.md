# GEOTEST / GeoWorks 1.x – Statische Erstprüfung von UI.GEO und ICON-ED.GEO (Untersuchung 2455)

Stand: 12.11.2026  
Quelle: `GEOWORKS.zip`, bereitgestellte GeoWorks-1.2.8-Installation  
Untersuchungsart: ausschließlich statische Dateiprüfung; keine Ausführung und kein Disassemblierungsnachweis

## Untersuchte Dateien

| Datei im Archiv | Größe | SHA-256 |
|---|---:|---|
| `GEOWORKS/SYSTEM/UI.GEO` | 87.900 Bytes | `13a3a82ec3d4373b120890a11eb09b3a9f9ec456ca633819728f53c07883c73a` |
| `GEOWORKS/WORLD/ICON-ED.GEO` | 47.648 Bytes | `afbbd1d8115c82162e8d3c9331c5d945e073e0823852bb5c68055ba6148df064` |

Beide Dateien wurden aus dem ZIP-Archiv unverändert in das Arbeitsverzeichnis extrahiert. Die ersten Bytes enthalten bei beiden Dateien eine PC/GEOS-Geode-Kennung und Metadaten. Die Prüfung hier interpretiert diese Felder nicht über die bekannten Grenzen hinaus.

## UI.GEO – bestätigte Befunde

Im Dateikopf stehen unter anderem:

- Geode-Token: `UI00` (Dateioffset `0x14`)
- Herstellerkennung als ASCII: `GEOS` (Dateioffset `0x1A`)
- langer Name: `Generic User Interface` (Dateioffset `0x20`)
- Copyright-Zeichenkette: `Copyright GeoWorks 1991` (Dateioffset `0xA8`)

Eine ASCII-Zeichenkette `TOKEN.DB` befindet sich bei Dateioffset `0x12BC`. Weitere lesbare Zeichenketten nennen unter anderem `specificUICompatible`, `GEOS.LOG`, `Specific UI`, `Token DB` und `Graphical Setup`.

**Einordnung:** Die Zeichenkette `TOKEN.DB` ist ein Hinweis, dass UI.GEO die Token-Datenbank zumindest namentlich referenziert. Eine Zeichenkette allein belegt nicht, dass UI.GEO die Provider-Bilddaten selbst dekodiert. In dieser Erstprüfung wurde keine belastbare Routineadresse und kein Codepfad für das Rendern von CGA-/HGC-/EGA-Providerdaten identifiziert.

## ICON-ED.GEO – bestätigte Befunde

Im Dateikopf stehen:

- Geode-Token: `ICED` (Dateioffset `0x14`)
- Herstellerkennung als ASCII: `twGEOS` (Dateioffset `0x18`)
- langer Name: `Symbol-Editor` (Dateioffset `0x20`)
- Copyright-Zeichenkette: `(c) T. Wachsmann 1993` (Dateioffset `0xA8`)

Weitere lesbare Zeichenketten nennen unter anderem:
- `Icon-Editor`
- `Version 0.6.0`
- `Thomas Wachsmann, 1993`
- `VGA-Symbol`
- `CGA-Symbol`
- `Monochrom-Symbol`
- `Install new Icon`

Die exakte Zeichenkette `TOKEN.DB` wurde in dieser Datei nicht gefunden.

**Einordnung:** Die Dateimetadaten und Texte identifizieren ICON-ED.GEO als Symbol-Editor von Thomas Wachsmann (1993), nicht als GeoWorks-Systembibliothek. Die Zeichenketten belegen, dass die Anwendung unterschiedliche Icon-Kategorien behandelt. Sie belegen nicht, dass sie die allgemeine GeoWorks-Provider-Dekodierroutine enthält oder dass ihr internes Format mit den Standard-Icon-Providern identisch ist.

## Grenzen dieser Prüfung

- Es wurde kein Disassemblerlauf durchgeführt.
- Es wurden keine Ressourcensegmente oder Prozeduren semantisch rekonstruiert.
- Aus String-Fundstellen wird keine Funktion einer Routine abgeleitet.
- Die bloße Erwähnung von `TOKEN.DB` in UI.GEO ist kein Nachweis, dass UI.GEO selbst die Bilddaten dekodiert.
- ICON-ED.GEO ist ein zusätzlicher Untersuchungsgegenstand, aber aufgrund seiner Identität als Symbol-Editor kein Ersatz für die Suche nach der zentralen GeoWorks-1.x-UI-/Grafikroutine.

## Ergebnis

1. `UI.GEO` ist anhand der Dateikopfzeichenketten als `UI00` / Generic User Interface identifiziert.
2. `UI.GEO` enthält bei Offset `0x12BC` die Zeichenkette `TOKEN.DB`; ein Bilddekodierpfad ist damit nicht nachgewiesen.
3. `ICON-ED.GEO` ist anhand der Metadaten als Symbol-Editor (ICED, Herstellerkennung `twGEOS`) identifiziert.
4. ICON-ED.GEO enthält Texte für VGA-, CGA- und Monochrom-Symbole, aber keine sichtbare Zeichenkette `TOKEN.DB`.
5. Keine der beiden Erstprüfungen liefert bislang eine nachgewiesene Dekodierroutine für die Icon-Payloads.

## Nächster Schritt

Für die nächste Stufe ist eine echte Ressourcen-/Codeanalyse erforderlich. Zuerst müssen die PC/GEOS-Geode-Ressourcentabellen dieser beiden Dateien zuverlässig geparst werden. Anschließend sind die passenden Code-Ressourcen zu disassemblieren und Aufrufstellen zu verfolgen, die Token- oder Moniker-Daten referenzieren. Ein Kandidat wird erst dann als Icon-Dekoder dokumentiert, wenn sein Datenzugriff und die Verarbeitung durch nachvollziehbaren Code belegt sind.

Originaldateien und installierte `TOKEN.DB`/`GEOS.INI` bleiben unverändert.
