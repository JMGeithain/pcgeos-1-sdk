# Untersuchung 2428 – Ressourcen-Offsettabelle in GDOC.000 und PAPR.000

## Ziel

Die interne Geode-Struktur von `GDOC.000` und `PAPR.000` wurde neu ausgerichtet. Entscheidend war, zwischen dem 256 Byte langen äußeren GEOS-Dateikopf und dem danach beginnenden Geode-Inhalt zu unterscheiden.

## Dateien und Prüfsummen

- `GDOC.000`: 2.256 Byte, SHA-256 `fe19cbcb46c2a92cf02da64c963facb8decb95d7e60bca34eb0d1c5e00b01733`
- `PAPR.000`: 2.208 Byte, SHA-256 `30b08761294ccd7762c686ca3d477e509cb454f56b6c7db5aa2b1497efbabfbe`

Beide Dateien beginnen mit der GEOS-Dateikennung `C7 45 CF 53`. Der Geode-Inhalt beginnt nach dem 256-Byte-Dateikopf bei Dateioffset `0x100`.

## Wichtige Korrektur zur vorherigen Offset-Interpretation

Die zuvor betrachteten Offsets `0xCC` und `0xD0` liegen innerhalb des äußeren 256-Byte-GEOS-Dateikopfs. Sie dürfen daher nicht als Felder des internen Geode-Headers bezeichnet werden.

Der interne Geode-Inhalt beginnt bei `0x100`. Dort stehen die Tokens:

- `GDOC.000`: `gDOC`, Hersteller `00FFh`
- `PAPR.000`: `PAPR`, Hersteller `00FFh`

Im internen Geode-Header ist bei Dateioffset `0x118` der 16-Bit-Wert `0007h` zu sehen. Das stimmt mit der zuvor ermittelten Zahl von sieben Ressourcen überein.

## Ressourcen-Offsettabelle

Ab Dateioffset `0x13C` folgen sieben 32-Bit-Werte (little-endian), die in beiden Dateien gleich sind:

| Tabelleneintrag | Relativer Wert | Dateioffset bei Geode-Basis 0x100 |
|---:|---:|---:|
| 1 | `0x00000174` | `0x274` |
| 2 | `0x00000174` | `0x274` |
| 3 | `0x000001DC` | `0x2DC` |
| 4 | `0x000002B0` | `0x3B0` |
| 5 | `0x000003F4` | `0x4F4` |
| 6 | `0x00000498` | `0x598` |
| 7 | `0x0000059C` | `0x69C` |

Die Werte sind relativ zur Geode-Basis `0x100` angegeben; die letzte Spalte zeigt die daraus berechneten absoluten Dateioffsets.

**Beobachtung:** Die Tabelle enthält sieben Einträge, aber nur sechs unterschiedliche Offsetwerte, weil Eintrag 1 und 2 denselben Wert `0x174` besitzen. Die Bedeutung dieser doppelten Referenz ist noch nicht geklärt. Sie wird nicht ohne weitere Prüfung als Fehler oder als zwei getrennte Ressourcen interpretiert.

## Erste Bytes an den referenzierten Positionen

Die Anfangsbytes an den sechs unterschiedlichen Positionen stimmen zwischen `GDOC.000` und `PAPR.000` weitgehend überein:

- `0x274`: `44 00 00 00 08 00 00 00 ...`
- `0x2DC`: `08 00 00 03 02 02 02 00 ...`
- `0x3B0`: `28 00 00 40 C6 10 22 00 ...`

Ab `0x4F4` unterscheiden sich die Daten deutlich. Das ist ein erster Hinweis darauf, dass beide Provider einen gemeinsamen strukturellen beziehungsweise ausführbaren Teil und danach unterschiedliche Inhalte besitzen. Die genaue Ressourcenzuordnung der einzelnen Offsetpositionen ist damit noch nicht bewiesen.

## Einordnung anhand externer Formatdokumentation

Die Dokumentation zu GeoDump beschreibt Geodes als Dateien mit zusätzlichem Header, Bibliotheksliste, Exportinformationen und einer Tabelle von Segmenten/Ressourcen, auf die die einzelnen Ressourcen folgen. Sie weist außerdem darauf hin, dass Ressourcen unter anderem Code, Daten und visuelle Moniker enthalten können. Quelle: [Marcus Gröber – About GeoDump](https://www.mgroeber.de/geodump-documentation.html).

Die PC/GEOS-Dokumentation zum Resource Editor beschreibt Ressourcen ebenfalls als Bereiche, die Code, Daten, Strings oder Bitmaps enthalten können. Diese Dokumentation ist eine allgemeine Strukturhilfe; sie ersetzt keinen Nachweis der exakten Feldsemantik in den hier untersuchten GeoWorks-1.x-Dateien. Quelle: [FreeGEOS Documentation – Resource Editor](https://bluewaysw.github.io/pcgeos/Tools/tresed.html).

## Ergebnis

Gesichert durch die Binärdaten:

1. Der Geode-Inhalt beginnt bei Dateioffset `0x100`.
2. Der interne Header enthält den Wert `7` bei `0x118`.
3. Ab `0x13C` liegen sieben aufeinanderfolgende 32-Bit-Offsetwerte.
4. Die Offsetwerte sind in beiden Provider-Dateien identisch.
5. Die Tabelle enthält sechs unterschiedliche Positionen, da die ersten beiden Einträge denselben Offset besitzen.
6. Die Daten an den Positionen ab `0x4F4` unterscheiden sich zwischen den Dateien.

Noch nicht bewiesen:

- die vollständige Semantik aller Headerfelder;
- ob jeder Tabelleneintrag genau einer eigenständigen Ressource entspricht;
- die Interpretation der doppelten ersten beiden Offsets;
- welche der Ressourcen Moniker-/Bitmap-Daten enthalten;
- eine direkte Verbindung zu den Zusatzbytes der TOKEN.DB-Einträge `gDOC` und `PAPR`.

## Nächster Schritt

Die sechs unterschiedlichen Zielpositionen werden anhand ihrer internen Ressourcenheader und ihrer Endgrenzen untersucht. Dabei ist besonders zu prüfen, ob die Daten ab `0x4F4`, `0x598` und `0x69C` tatsächlich Grafik-/Monikerressourcen sind und ob sich ihre Header mit den zuvor identifizierten CGA-, HGC- und EGA-Moniker-Kandidaten decken.

## Methodik und Grenzen

- Ausschließlich statische, lesende Analyse der Archivdateien.
- Keine Änderungen an `TOKEN.DB`, `GEOS.INI` oder Provider-Dateien.
- Kein Laufzeittest in GeoWorks.
- Die Ergebnisse gelten für die vorliegenden Dateien aus dem untersuchten GeoWorks-Archiv.
