# Untersuchung 2435 – Unterstruktur des Provider-Bereichs ab 0x3B0

## Ziel

Der Bereich `0x3B0–0x4F3` der sieben originalen Provider-Geodes wurde anhand der tatsächlichen Bytes weiter zerlegt. Schwerpunkt waren die gemeinsamen Felder vor den providerabhängigen Daten und die wiederkehrenden Strukturen ab `0x3F0`.

## Dateien

Untersucht wurden `GDOC.000`, `PAPR.000`, `BEER.000`, `BILL.000`, `BUTN.000`, `ZIPR.000` und `GEXE.000` aus `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/` im Archiv `GEOWORKS.zip`.

## Gemeinsame Struktur im Bereich 0x3B0–0x3EF

Bei allen sieben Dateien ist der Bereich `0x3B0–0x3EF` byteidentisch. Er enthält unter anderem:

- mehrere 16-Bit-Werte und wiederkehrende Muster `22 00`;
- die Bytes `13 00 01 00 00 00 00 FF`;
- ab `0x3DC` den ASCII-String `Icon Maker` einschließlich Nullterminierung;
- anschließend Padding-/Reservierungsbytes.

Der String beginnt bei Dateioffset `0x3DC`. Das ist ein direkter Bytebefund. Seine genaue Funktion innerhalb der Geode ist nicht allein durch das Vorkommen des Textes geklärt.

## Wiederkehrende Struktur ab 0x3F0

Bei allen sieben Dateien beginnt bei `0x3F0` ein gemeinsames Muster:

```
23 00 00 00 04 00 20 00 00 C0 02 00 ...
```

Die ersten 12 Bytes dieser Struktur sind bei allen sieben Dateien gleich. Danach folgen Felder, die zwischen Providern teilweise variieren. Beispielsweise steht bei GDOC an `0x3FC` der Wert `0x0094`, bei PAPR und BUTN `0x0098`, bei ZIPR `0x009C`, bei BILL und GEXE `0x0090`.

Bei `0x490` beginnt in GDOC/PAPR/BEER/ZIPR eine weitere ähnliche Struktur mit dem Präfix:

```
23 00 00 00 05 00 20 00 00 C0 02 00 ...
```

Bei BILL beginnt dieses Muster bereits bei `0x480`, bei GEXE ebenfalls bei `0x480`. Bei BUTN liegt die entsprechende Struktur bei `0x490`.

Das zeigt, dass die Bereiche nicht einfach als ein einzelner Bitmap-Blob gelesen werden dürfen. Es gibt wiederkehrende, strukturierte Unterbereiche mit Feldwerten und variierenden Abständen.

## Providerabhängige Daten nach den Strukturfeldern

In den Beispielen beginnen ab ungefähr `0x430` sichtbare providerabhängige Bytefolgen. Die Folgen sind nicht identisch. Einige weisen wiederkehrende Muster auf, zum Beispiel:

- GDOC: wiederholte Sequenzen mit `E1 05` und wechselnden Bytefolgen;
- PAPR: wechselnde Folgen mit `05 40`, `05 5E` und anderen Markern;
- BEER: wechselnde Folgen mit `05 00` und variierenden nachfolgenden Werten;
- BUTN/ZIPR: Folgen mit `05 00` und stark unterschiedlichen Datenbytes;
- GEXE: wiederholte Folgen mit `05 0E` und wechselnden Datenbytes.

Diese Muster sind Hinweise auf eine codierte Struktur, aber noch kein Beweis für ein bestimmtes RLE- oder Bitmapformat. Die Bytes dürfen nicht ohne Decoder als Pixelwerte ausgegeben werden.

## Bezug zu den dokumentierten Icon-Profilen

ICONMAKE 1.0 dokumentiert drei klassische Iconprofile:

- 48×14, monochrom;
- 48×30, monochrom;
- 48×30, 16 Farben.

Die Unterstrukturen ab `0x3F0` enthalten wiederkehrende Felder, die möglicherweise Größen-, Format- oder Längeninformationen repräsentieren. Die konkreten Werte sind bislang nicht vollständig semantisch entschlüsselt. Deshalb ist noch keine der Unterstrukturen sicher einem der drei Iconprofile zugeordnet.

## Korrektur und Abgrenzung

Die Token-Kennung wurde in Untersuchung 2434 bei `0x304` nachgewiesen. Sie liegt im vorherigen Bereich `0x2DC–0x3AF`, nicht in dem hier untersuchten Bereich.

Der Bereich ab `0x3B0` enthält den gemeinsamen Text `Icon Maker`, strukturierte Felder und providerabhängige Daten. Es ist nicht zulässig, den gesamten Bereich als Bilddaten zu bezeichnen.

## Ergebnis

Gesichert:

1. `0x3B0–0x3EF` ist über die sieben Provider-Dateien byteidentisch.
2. `Icon Maker` beginnt in allen sieben Dateien bei `0x3DC`.
3. Ab `0x3F0` treten wiederkehrende strukturierte Präfixe auf.
4. Mindestens zwei ähnlich aufgebaute Unterstrukturen beginnen je Datei an unterschiedlichen Positionen.
5. Die nachfolgenden Daten unterscheiden sich je Provider.

Noch offen:

- Feldsemantik der 16-Bit- und 32-Bit-Werte;
- genaue Grenzen und Anzahl der Unterstrukturen;
- ob die providerabhängigen Daten Moniker, Bitmaps, Ressourcenverweise oder andere Inhalte darstellen;
- Kompressionsverfahren und Pixelanordnung;
- Zuordnung zu CGA, HGC/MCGA und EGA.

## Nächster Schritt

Die Unterstrukturen ab `0x3F0` werden mit weiteren Provider-Dateien und den Ressourcen-/Monikerformaten aus dem GeoWorks-1.x-SDK verglichen. Danach ist ein Decoder-Prototyp nur dann sinnvoll, wenn die Feldgrenzen und Datenlängen nachvollziehbar sind. Als Kontrollziel dienen die ICONMAKE-Abmessungen und Farbtiefen.

## Methodik und Grenzen

- Ausschließlich statische, lesende Analyse der Dateien aus `GEOWORKS.zip`.
- Keine Änderungen an Originaldateien, `TOKEN.DB` oder `GEOS.INI`.
- Kein Laufzeittest in GeoWorks.
- Alle semantischen Deutungen, die über sichtbare Bytefolgen und Text hinausgehen, bleiben ausdrücklich Hypothesen.
