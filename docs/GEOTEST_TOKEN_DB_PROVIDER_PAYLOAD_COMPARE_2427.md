# Untersuchung 2427 – TOKEN.DB: eingebettete Daten bei gDOC und PAPR

## Ziel

Die TOKEN.DB-Einträge der beiden Provider-Tokens `gDOC` und `PAPR` wurden mit den zugehörigen Provider-Geodes `GDOC.000` und `PAPR.000` verglichen. Ziel war festzustellen, ob die Bytes hinter dem bekannten Token-Kopf direkte Kopien von Daten aus den Provider-Dateien sind.

## Verwendete Dateien

Aus `GEOWORKS.zip` wurden ausschließlich lesend untersucht:

- `GEOWORKS/SYSTEM/TOKEN.DB` – 952.688 Byte
- `GEOWORKS/ICONS/GDOC.000` – 2.256 Byte
- `GEOWORKS/ICONS/PAPR.000` – 2.208 Byte

SHA-256:

- TOKEN.DB: `c7fa3d51c9bdce14b988d20fd8ed57ac7da9837803090ac858990613ec53ae35`
- GDOC.000: `fe19cbcb46c2a92cf02da64c963facb8decb95d7e60bca34eb0d1c5e00b01733`
- PAPR.000: `30b08761294ccd7762c686ca3d477e509cb454f56b6c7db5aa2b1497efbabfbe`

## TOKEN.DB-Einträge

Die bereits identifizierte VM-Datenregion beginnt bei Dateioffset `0xDAB50`. Innerhalb dieser Region wurden die folgenden Einträge erneut geprüft:

### gDOC

Beginn innerhalb der Region: `0x0A58`

Bytes bis zum nächsten Token-Eintrag `gEXE`:

```
67 44 4F 43 FF 00 74 00 9C 01
00 00 00 0C 0C 00 0C 0F 07 70 00 7F FC FF 00 00
```

Gesamtlänge: 26 Byte. Der gemeinsame Kopf umfasst 10 Byte; danach folgen 16 Byte zusätzliche Daten.

Der nächste erkannte Eintrag `gEXE` beginnt bei `0x0A72`.

### PAPR

Beginn innerhalb der Region: `0x0BF6`

Bytes bis zum nächsten Token-Eintrag `PCOK`:

```
50 41 50 52 FF 00 74 00 DC 01
00 00 00 1E 00 1A 0C 02 30 00 1E 00 01 11 00 00
```

Gesamtlänge: 30 Byte. Der gemeinsame Kopf umfasst 10 Byte; danach folgen 20 Byte zusätzliche Daten.

Der nächste erkannte Eintrag `PCOK` beginnt bei `0x0C14`.

## Vergleich mit den Provider-Dateien

Die vollständigen Provider-Dateien wurden auf Bytefolgen aus den zusätzlichen TOKEN.DB-Daten untersucht. Die einfachen Treffer bei sehr kurzen Bytefolgen sind nicht aussagekräftig: Nullen und andere häufige Bytes kommen in strukturierten Binärdateien vielfach vor.

Ein belastbarer Nachweis, dass die Zusatzdaten eine unveränderte Kopie einer Ressource aus `GDOC.000` oder `PAPR.000` darstellen, liegt daher nicht vor. Auch eine konkrete Zuordnung zu den früher untersuchten Ressourcen R4, R5 oder R6 ist weiterhin offen.

## Bewertung

Gesichert ist:

1. Die beiden Token-Einträge enthalten nach dem 10-Byte-Kopf zusätzliche, unterschiedlich lange Datenbereiche.
2. Die Eintragslängen sind nicht identisch: 26 Byte bei `gDOC`, 30 Byte bei `PAPR`.
3. Die Datenbereiche enden unmittelbar vor den jeweils folgenden erkannten Token-Einträgen.
4. Eine Bedeutung als Icon, Moniker, Grafikbeschreibung oder Verweisstruktur ist noch nicht nachgewiesen.

Nicht gesichert ist:

- dass die 16 bzw. 20 Zusatzbytes vollständige Bilddaten darstellen;
- dass sie direkt auf die Ressourcen R4/R5/R6 verweisen;
- dass das 16-Bit-Feld im gemeinsamen Kopf ein Ressourcenhandle, eine ID oder einen Offset bezeichnet.

## Konsequenz für GEOTEST

Für `GEOTEST.GEO` wird weiterhin kein Dokument-Token und keine Icon-Zuordnung aus diesen Befunden abgeleitet. Insbesondere werden `GTD1` und `.GTD` nicht als bestätigte Registrierung behandelt.

Der nächste sinnvolle Analyseschritt ist, die Ressourcenverzeichnisse und Ressourceninhalte von `GDOC.000` und `PAPR.000` unabhängig zu dekodieren und die resultierenden Moniker-/Bitmap-Strukturen mit den 16- bzw. 20-Byte-Bereichen zu vergleichen. Erst ein reproduzierbarer Struktur- oder Inhaltsabgleich darf als Zuordnung dokumentiert werden.

## Methodik und Grenzen

- Ausschließlich statische, lesende Analyse der Archivdateien.
- Keine Änderungen an `TOKEN.DB`, `GEOS.INI` oder Provider-Dateien.
- Kein Laufzeittest in GeoWorks.
- Der Block bei `0xDAB50` wird weiterhin neutral als VM-Datenblock `0080h` bezeichnet; seine Interpretation als gewöhnlicher LMem-Block ist nicht belegt.
