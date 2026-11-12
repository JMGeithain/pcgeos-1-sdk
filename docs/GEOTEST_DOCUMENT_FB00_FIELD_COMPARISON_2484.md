# GEOTEST – Untersuchung 2484

**Feldvergleich der FB00-Zielstruktur in GeoWorks-1.x-Dokumenten**  
Stand: 12.11.2026  
Datenbasis: `GEOWORKS.zip`, `GEOWORKS/DOCUMENT/*.000`  
Zielprofil: ausschließlich GeoWorks / PC-GEOS 1.x

## 1. Ziel und Methode

Untersuchung 2483 identifizierte in 418 Dateien eine interne Zielstruktur, auf die das DWORD bei Dateioffset `0xCC` zeigt. An der Zielposition beginnt `FB 00`; bei relativem Offset `+0x28` steht erneut der absolute Dateioffset der Zielstruktur.

Diese Untersuchung vergleicht die ersten `0x40` Bytes ab dieser Zielposition feldweise. Die Werte werden zunächst neutral als relative WORD-Felder bezeichnet. Es werden keine symbolischen Feldnamen vergeben, solange die Kernel-/Library-Semantik nicht belegt ist.

## 2. Datenbestand

418 Dateien erfüllten alle folgenden Bedingungen:

- Pfad unter `GEOWORKS/DOCUMENT/`
- Endung `.000`
- GEODE-Signatur `C7 45 CF 53`
- Marker `EB AD` bei Dateioffset `0xC8`
- DWORD bei `0xCC` zeigt auf mindestens `0x2C` verfügbare Bytes innerhalb derselben Datei.

Typ-/Creator-Gruppen:

| Type / Creator | Anzahl |
|---|---:|
| WDAT/WP00 | 198 |
| DDAT/DP00 | 153 |
| scbk/Scrp | 54 |
| adbk/ADBK | 8 |
| plnr/PLNR | 2 |
| TMPL/Null-Creator | 2 |
| TOOL/Scrp | 1 |
| **Summe** | **418** |

## 3. Gemeinsame Signatur und wiederkehrende WORD-Felder

Über alle 418 Dateien sind folgende relative WORD-Felder konstant:

- `+0x00 = 0x00FB` (Bytefolge `FB 00`)
- `+0x12 = 0x0000`
- `+0x14 = 0x0044`
- `+0x1E = 0x0000`
- `+0x22 = 0x00FF`
- `+0x24 = 0xADEB` (Bytefolge `EB AD`)

Weitere Felder mit kleiner Wertemenge:

- `+0x16`: `0x0046` in 400 Fällen; `0x5A60` in 18 Fällen. Die 18 abweichenden Fälle liegen in der Gruppe scbk/Scrp.
- `+0x1C`: `0xFFFC` in 198 Fällen, `0xFFF8` in 153, `0xFFC8` in 59, `0xFF48` in 8.
- `+0x2E`: `0x01FF` in 198 Fällen, `0x00FF` in 179, `0x0000` in 41.
- `+0x30`: `0x0000` in 239 Fällen, `0xFFFF` in 161, `0x0001` in 18.
- `+0x36`: `0x0000` in 409 Fällen; die übrigen Werte `0x0001`/`0x0003`/`0x0005`/`0x000A` treten zusammen neunmal auf.
- `+0x3A`: `0x01FF` in 352 Fällen, `0x0000` in 38, `0x00FF` in 27, `0x03FD` in einem Fall.

Diese Werte sind Rohbeobachtungen. Ihre Semantik ist nicht geklärt.

## 4. Rückreferenz bei +0x28

In allen 418 Dateien gilt:

`DWORD(Zielstruktur + 0x28) = Dateioffset der Zielstruktur`.

Damit ist die Rückreferenz über den gesamten geprüften Bestand bestätigt. Die Bytes `+0x24..+0x25` sind in allen 418 Dateien `EB AD`; die Bytes `+0x00..+0x01` sind `FB 00`.

## 5. Unterschiede nach Dokumenttyp

Die Struktur ist nicht byteidentisch über alle Dokumenttypen hinweg:

- WDAT und DDAT haben unterschiedliche konstante Werte an `+0x1C` (WDAT `FFFC`, DDAT `FFF8`) und deutlich unterschiedliche Verteilungen bei `+0x2E`.
- scbk zeigt größere Varianz in mehreren Feldern, insbesondere `+0x16`, `+0x1C`, `+0x2E`, `+0x30`, `+0x32` bis `+0x3E`.
- adbk und plnr haben kleine Stichproben; aus acht bzw. zwei Dateien sind keine weitreichenden typischen Aussagen zulässig.
- Die zwei TMPL-Dateien und die einzelne TOOL-Datei sind ebenfalls zu kleine Gruppen für Verallgemeinerungen.

## 6. Feldorientierte Referenzbeispiele

Die ersten `0x40` Bytes wurden für WDAT, DDAT, scbk, adbk und plnr einzeln verglichen. Die folgenden Eigenschaften sind in den Referenzbeispielen sichtbar:

- `FB 00` am Anfang.
- `00 44 00 46` in den WORD-Feldern `+0x14/+0x16` (Ausnahme: 18 Scrapbook-Dateien besitzen an `+0x16` den anderen Wert `0x5A60`).
- `EB AD` bei `+0x24`.
- Absolute Rückreferenz bei `+0x28`.

Weitere WORD-Felder enthalten je nach Dokument und Typ stark variable Werte und/oder `0xFFxx`-Muster. Ohne Code-Referenz werden sie nicht als Dateigrößen, Handles, Flags oder Zeiger benannt.

## 7. Konsequenz für GEOTEST

Ein zukünftiger Strukturprüfer kann nach Bounds-Prüfung die folgenden invarianten Bytes/Werte als Plausibilitätsmerkmale verwenden:

- `Zielstruktur[0:2] == FB 00`
- `WORD(Zielstruktur+0x12) == 0`
- `WORD(Zielstruktur+0x14) == 0x0044`
- `WORD(Zielstruktur+0x1E) == 0`
- `WORD(Zielstruktur+0x22) == 0x00FF`
- `WORD(Zielstruktur+0x24) == 0xADEB`
- `DWORD(Zielstruktur+0x28) == Zieloffset`

Diese Merkmale sind Archivbeobachtungen, keine vollständige Formatvalidierung.

Nicht implementieren:

- keine Interpretation der variablen Felder als symbolische Strukturmember;
- keine Erzeugung eines FB00-Blocks aus einem geratenen Template;
- keine Behauptung, dass der Block allein ein vollständiges VM-Dokument darstellt.

## 8. Offene Fragen und nächster Schritt

Offen bleiben:

- Welche Funktion hat der Block im VM-/Dokumentformat?
- Welche Bedeutung haben die Felder `+0x06/+0x08`, `+0x0C/+0x0E/+0x10`, `+0x18/+0x20`, `+0x26` und `+0x2C` ff.?
- Sind die Werte bei `+0x1C` und `+0x2E` typabhängige Flags, Längen, Relativwerte oder etwas anderes?
- Welche Routine erzeugt, aktualisiert und lädt diese Struktur?

Nächste Untersuchung 2485: die FB00-Zielstruktur gegen den ursprünglichen GeoWorks-1.x-Kernel und die relevanten Bibliotheken/Anwendungen abgleichen; insbesondere nach Bytefolgen/Offsets und Datei-/VM-Aufrufpfaden suchen. Keine Semantik aus bloßen Zahlenwerten ableiten.

## 9. Grenzen

Statische Byteanalyse des bereitgestellten GEOWORKS.zip. Keine Änderung an Quelldateien oder GeoWorks-Dokumenten. Kein Laufzeittest im Emulator. Keine neue GEOTEST.GEO gebaut. Die Analyse belegt die wiederkehrende Struktur und die Rückreferenz, nicht die vollständige Bedeutung des Formats.
