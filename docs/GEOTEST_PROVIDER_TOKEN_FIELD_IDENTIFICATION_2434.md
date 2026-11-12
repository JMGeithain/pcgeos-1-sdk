# Untersuchung 2434 – Die Token-Kennung im Provider-Bereich identifiziert

## Ergebnis vorweg

Die vier abweichenden Bytes im zweiten Bereich sind keine unbekannten Parameter: Sie sind genau die vier ASCII-Zeichen des jeweiligen Provider-Tokens. Damit ist der Unterschied im zweiten Bereich erklärt.

Bei allen sieben untersuchten Provider-Dateien steht die Token-Kennung an derselben absoluten Dateiposition `0x304`. Direkt danach folgen die Bytes `FF 00 00 00`.

## Datenbasis und Methode

Untersucht wurden die sieben Dateien aus `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/`:

`GDOC.000`, `PAPR.000`, `BEER.000`, `BILL.000`, `BUTN.000`, `ZIPR.000`, `GEXE.000`.

Die Dateien wurden direkt aus `GEOWORKS.zip` gelesen. Es wurden die zuvor ermittelten Bereiche `0x2DC–0x3AF` und `0x3B0–0x4F3` byteweise verglichen.

## Auflösung des zweiten Bereichs

Bei allen sieben Dateien beginnt die Token-Kennung bei Dateioffset `0x304`:

| Datei | Bytes an 0x304 | ASCII |
|---|---|---|
| GDOC.000 | `67 44 4F 43` | `gDOC` |
| PAPR.000 | `50 41 50 52` | `PAPR` |
| BEER.000 | `42 45 45 52` | `BEER` |
| BILL.000 | `42 49 4C 4C` | `BILL` |
| BUTN.000 | `42 55 54 4E` | `BUTN` |
| ZIPR.000 | `5A 49 50 52` | `ZIPR` |
| GEXE.000 | `67 45 58 45` | `gEXE` |

Die vier Bytes an dieser Position erklären die zuvor gemessenen vier Abweichungen bei sechs Dateien. Bei `GEXE.000` ist das erste Byte ebenfalls `67h` (ASCII `g`), weshalb nur die letzten drei Zeichen vom `gDOC`-Referenzwert abweichen.

Unmittelbar nach der Token-Kennung stehen bei allen sieben Dateien dieselben Bytes:

```
FF 00 00 00
```

Damit ist der zweite Bereich bis auf den vierstelligen Token-Code byteidentisch. Die genaue Bedeutung der nachfolgenden Felder wird hier nicht überinterpretiert.

## Zusätzlicher Befund im dritten Bereich

In allen sieben Dateien findet sich bei Dateioffset `0x3DC` die ASCII-Zeichenfolge:

```
Icon Maker\0
```

Der String liegt in einem ansonsten weitgehend gemeinsamen Abschnitt des Bereichs `0x3B0–0x4F3`. Der dritte Bereich ist jedoch nicht insgesamt identisch: Die Bytes ab ungefähr `0x3FC` enthalten zahlreiche providerabhängige Unterschiede.

Die Zeichenfolge `Icon Maker` ist ein klarer Textbefund. Ob sie als sichtbarer Moniker, Ressourcenname, Entwickler-/Anwendungsbezeichnung oder Teil einer anderen Datenstruktur verwendet wird, ist durch den String allein nicht bewiesen.

## Bewertung der drei ersten Bereiche

1. **Bereich 1 (`0x274–0x2DB`, 104 Byte):** vollständig identisch in allen sieben Dateien.
2. **Bereich 2 (`0x2DC–0x3AF`, 212 Byte):** identisch bis auf den vierstelligen Token-Code bei `0x304`.
3. **Bereich 3 (`0x3B0–0x4F3`, 324 Byte):** enthält gemeinsamen Text und zahlreiche providerabhängige Binärdaten.

Damit ist die Struktur deutlich besser eingegrenzt: Bereich 2 enthält nachweislich die providerabhängige Token-Kennung; Bereich 3 ist nicht als bloßer gemeinsamer Codeblock zu behandeln.

## Konsequenz für GEOTEST

Der Fund ist für die spätere Konstruktion eines eigenen Icon-Providers wichtig: In den Originaldateien steht der jeweilige Token-Code an einer konstanten Position innerhalb des zweiten Bereichs. Das ist ein starker Hinweis auf eine standardisierte Provider-Struktur.

Es reicht jedoch noch nicht aus, eine Provider-Datei für GEOTEST sicher zu erzeugen. Die restlichen Felder, Ressourcenarten, Monikerformate und die Token-Aufnahme durch GeoWorks müssen weiterhin untersucht und später im echten GeoWorks 1.2.8 getestet werden.

Es wird weiterhin kein Token für ein GEOTEST-Dokument als bestätigt festgelegt und keine Originaldatei verändert.

## Korrekturhinweis zu Untersuchung 2433

Die Formulierung „vier unbekannte veränderliche Bytes“ war nur eine Beschreibung des Bytevergleichs, keine Deutung. Diese Untersuchung identifiziert die vier Bytes als ASCII-Token-Code. Die vorherige Abweichungszählung bleibt korrekt; ihre Bedeutung ist jetzt geklärt.

## Nächster Schritt

Den dritten Bereich ab `0x3B0` in Unterfelder zerlegen. Insbesondere ist zu prüfen, ob die Struktur ab `0x3F0` aus Ressourcen-/Monikerdeskriptoren und nachfolgenden Bilddaten besteht. Dazu werden die Feldgrenzen zwischen mehreren Providern verglichen und mit den dokumentierten Icon-Profilen 48×14 monochrom, 48×30 monochrom und 48×30 16 Farben abgeglichen.

## Methodik und Grenzen

- Statische, lesende Analyse der sieben Originaldateien aus dem Archiv.
- Keine Änderung an `TOKEN.DB`, `GEOS.INI` oder Provider-Geodes.
- Kein Laufzeittest in GeoWorks.
- Der String `Icon Maker` und die Token-Kennung sind direkt sichtbare ASCII-Daten; ihre genaue Laufzeitfunktion wird nicht allein aus ihrem Vorkommen abgeleitet.
