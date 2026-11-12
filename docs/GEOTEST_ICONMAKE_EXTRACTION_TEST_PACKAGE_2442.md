# Untersuchung 2442 – Reproduzierbares ICONMAKE-Extraktionstestpaket

## Ziel

Ein kleines, getrenntes Testpaket wurde aus unveränderten Kopien der Originaldateien vorbereitet. Damit kann der dokumentierte ICONMAKE-Extraktionsmodus in einer DOS-Umgebung ausgeführt werden, ohne die GeoWorks-Installation oder die Originaldateien anzufassen.

## Paket

Datei: `ICONMAKE_Extraktionstest_2442.zip`

Enthalten sind:

- `ICONMAKE.EXE` – 19.477 Byte
- `ICONMAKE.ENG` – 6.234 Byte
- `GDOC.000` – 2.256 Byte
- `PAPR.000` – 2.208 Byte
- `README_TEST_2442.txt` – Testanleitung und Prüfsummen

Die beiden Provider-Dateien stammen aus `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/` im Archiv `GEOWORKS.zip`. Sie sind Kopien und wurden nicht verändert.

## Prüfsummen

| Datei | SHA-256 |
|---|---|
| ICONMAKE.EXE | `72960ca2c01ca1b42813ed530d26a95e1e568d64c954f51ba363261732252933` |
| ICONMAKE.ENG | `4e0042838c448e769480d131cd34d869e96cf9086a0f4365b841260c3f403fbd` |
| GDOC.000 | `fe19cbcb46c2a92cf02da64c963facb8decb95d7e60bca34eb0d1c5e00b01733` |
| PAPR.000 | `30b08761294ccd7762c686ca3d477e509cb454f56b6c7db5aa2b1497efbabfbe` |

## Ausführung

In DOSBox oder einer anderen geeigneten DOS-Umgebung in den entpackten Testordner wechseln und nacheinander ausführen:

```dos
ICONMAKE x GDOC.000
ICONMAKE x PAPR.000
```

Laut ICONMAKE.ENG extrahiert der Modus `x` die Icon-Definitionen aus bestehenden GeoWorks-Programmen beziehungsweise Icon-Dummy-Dateien in PCX-Dateien. Die konkreten Ausgabedateinamen und -anzahlen müssen nach dem Lauf festgehalten werden.

## Sicherheit und Grenzen

- Das Testpaket enthält nur Kopien aus dem Archiv.
- Es wird keine Token-Installation vorgenommen.
- `TOKEN.DB` und `GEOS.INI` werden nicht benötigt und dürfen für diesen Test nicht verändert werden.
- Die Testbefehle wurden in dieser Untersuchung nicht ausgeführt; es liegen daher noch keine PCX-Ergebnisse vor.
- In der aktuellen Analyseumgebung war keine DOS-Laufzeitumgebung verfügbar.

## Nächster Schritt

Der Nutzer führt die beiden Befehle in seiner DOSBox-/BaseBox-Umgebung aus und stellt anschließend die erzeugten PCX-Dateien oder einen Screenshot der Ausgabe bereit. Danach können Header, Maße, Farbtiefe und Pixeldaten mit den in Untersuchungen 2438–2440 lokalisierten Deskriptoren verglichen werden.
