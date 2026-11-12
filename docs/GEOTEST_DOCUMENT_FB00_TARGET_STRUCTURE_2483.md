# GEOTEST – Untersuchung 2483

Analyse der 47 Ausnahmen und des DWORD-Feldes bei 0xCC

Stand: 12.11.2026
Zielprofil: ausschließlich GeoWorks / PC-GEOS 1.x

## 1. Ausgangslage

Untersuchung 2482 wertete 426 Dateien unter GEOWORKS/DOCUMENT mit Endung .000 und Signatur C7 45 CF 53 aus. 419 Dateien besitzen EB AD bei Offset 0xC8. Bei 372 dieser Dateien galt die Beziehung DWORD(0xCC) = Dateigröße - WORD(0xCA). 47 Dateien erfüllten diese Gleichung nicht.

## 2. Neue Prüfung: DWORD bei 0xCC als Dateioffset

Die 419 EB-AD-Dateien wurden erneut geprüft:
- In 418 Dateien liegt der DWORD-Wert bei 0xCC innerhalb der Datei.
- An genau diesem Dateioffset beginnt in allen 418 Fällen die Bytefolge FB 00.
- 40 Bytes nach diesem Zieloffset steht in allen 418 Fällen erneut derselbe DWORD-Wert wie bei 0xCC.
- In einer Datei liegt der DWORD-Wert außerhalb der Dateigröße; dort kann die Zielstruktur nicht innerhalb der Datei geprüft werden.

Das Muster spricht dafür, dass das DWORD bei 0xCC ein absoluter Dateioffset auf eine interne Struktur ist, deren Anfang FB 00 lautet und die bei +0x28 eine Rückreferenz auf denselben Offset enthält. Die symbolische Bedeutung ist nicht identifiziert; neutraler Name: „FB00-Zielstruktur“.

## 3. Der bisherige Größenvergleich war irreführend

Die Gleichung DWORD(0xCC) = Dateigröße - WORD(0xCA) traf bei 372/419 Dateien zu. Die neue Untersuchung zeigt jedoch, dass der DWORD-Wert in praktisch allen Fällen ein Dateioffset ist. Die Übereinstimmung mit Dateigröße minus WORD(0xCA) darf deshalb nicht als allgemeine Längenformel interpretiert werden. Die 47 Abweichungen sind kein Beleg für beschädigte Dateien.

## 4. Einzige Datei mit Zieloffset außerhalb der Datei

GEOWORKS/DOCUMENT/GAGS/CHANGING.000:
- Dateigröße: 65.536 Bytes (0x10000)
- WORD bei 0xCA: 0x0CB0
- DWORD bei 0xCC: 0x000564B0
- Zieloffset 0x564B0 liegt außerhalb der 0x10000 Bytes großen Datei.

Ob dies eine beschädigte/stale Datei, ein Sonderfall, ein fehlerhafter Headerwert oder ein anders interpretierter Wert ist, bleibt offen.

## 5. Referenzbeispiele

| Datei | Größe | WORD(0xCA) | DWORD(0xCC) | FB00 am Ziel | Rückreferenz +0x28 |
|---|---:|---:|---:|---|---|
| NEUES_DO.000 | 0x930 | 0x00B0 | 0x880 | ja | 0x880 |
| FAMILIEN.000 | 0x3340 | 0x0240 | 0x1A60 | ja | 0x1A60 |
| DRAW_UNB.000 | 0x5A0 | 0x0080 | 0x320 | ja | 0x320 |

## 6. Verteilung der 47 Abweichungen

- WDAT/WP00: 20
- DDAT/DP00: 12
- scbk/Scrp: 14
- adbk/ADBK: 1

46 der 47 Ausnahmen weisen ebenfalls das vollständige FB00-/Rückreferenzmuster auf. Nur CHANGING.000 fällt durch den außerhalb der Datei liegenden Zielwert auf.

## 7. Konsequenz für GEOTEST

- DWORD bei 0xCC nicht als Länge interpretieren.
- Bei einer Parserprüfung bounds-checken: Zieloffset innerhalb der Datei und mindestens 0x2C Bytes ab Zieloffset verfügbar.
- Für gültige Fälle prüfen: Bytes am Zieloffset == FB 00 und DWORD am Zieloffset + 0x28 == Zieloffset.
- FB00-Struktur noch nicht benennen oder selbst erzeugen, bis Felder und Rolle von 0xCA geklärt sind.
- CHANGING.000 als Sonderfall separat halten.

## 8. Nächster Schritt

Untersuchung 2484: FB00-Zielstruktur über mehrere Dokumenttypen feldweise vergleichen, insbesondere Bytes 0x00–0x40 relativ zum Zieloffset, und nach entsprechenden Zugriffsmustern in GeoWorks-1.x-Dateiverwaltungs-/Dokumentverwaltungsroutinen suchen.

## 9. Grenzen

Statische Byteanalyse des bereitgestellten GEOWORKS.zip-Archivs. Keine Laufzeitprüfung, kein vollständig rekonstruiertes VM-Format und keine neue GEOTEST.GEO mit Dokumenterzeugung.
