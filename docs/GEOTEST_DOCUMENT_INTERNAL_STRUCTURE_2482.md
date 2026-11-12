# GEOTEST – Untersuchung 2482

## Dateierzeugung und interne Dokumentstruktur in GeoWorks 1.x

**Stand:** 12.11.2026

### 1. Ziel

Untersucht wird, welche Dateistruktur GEOTEST.GEO mindestens berücksichtigen muss, wenn es ein eigenes GeoWorks-1.x-Dokument erzeugen soll. Die Analyse bleibt strikt bei GeoWorks/PC-GEOS 1.x und dem Archiv `GEOWORKS.zip`.

### 2. Quellen

Archiv: `/mnt/data/GEOWORKS.zip`

Referenzdateien:
- `GEOWORKS/DOCUMENT/NEUES_DO.000`
- `GEOWORKS/DOCUMENT/TESTWRIT.000`
- `GEOWORKS/DOCUMENT/TESTDRAW.000`
- `GEOWORKS/DOCUMENT/NEUE_ZEI.000`
- `GEOWORKS/DOCUMENT/DEFAULT_.000`
- `GEOWORKS/DOCUMENT/TESTICON.000`

Zusätzlich wurden alle Dateien unter `GEOWORKS/DOCUMENT/` mit Endung `.000` und GEODE-Signatur `C7 45 CF 53` inventarisiert.

### 3. Gesicherte Dateikopf-Felder

Bei den untersuchten GeoWrite-/GeoDraw-Dokumenten:
- Offset `0x00`: Signatur `C7 45 CF 53`.
- Offset `0x14`: vier Byte Type-Token, z. B. `WDAT` bzw. `DDAT`.
- Offset `0x1A`: vier Byte Creator-Token, z. B. `WP00` bzw. `DP00`.
- Offset `0x20`: langer Dateiname, nullterminiert.

Diese Felder sind bereits in Untersuchung 2481 anhand von `DOS_ICON.TXT` und realen Dokumenten belegt.

### 4. Neue Beobachtung: Marker EB AD ab Offset 0xC8

Bei 419 von 426 inventarisierten `.000`-Dateien mit GEODE-Signatur stehen an Offset `0xC8` die Bytes `EB AD`. Die sechs Icon-Dateien und eine weitere Datei verwenden an dieser Stelle ein anderes Muster (bei den sechs Icon-Dateien `00 96`).

Das ist eine beobachtete Strukturunterscheidung; die genaue symbolische Bedeutung des Markers `EB AD` ist noch nicht durch Kernel- oder Laufzeitnachweis bestätigt.

### 5. Felder unmittelbar nach EB AD

Bei den EB-AD-Dateien:
- Offset `0xCA`: 16-Bit-Wert, der je Datei variiert.
- Offset `0xCC`: 32-Bit-Wert, der bei vielen Dateien in Beziehung zur Dateigröße steht.

Prüfung über alle 419 EB-AD-Dateien:
- In 372 Fällen gilt exakt: Wert(`0xCC`) = Dateigröße - Wert(`0xCA`).
- In 47 Fällen gilt diese Gleichung nicht.

Aufschlüsselung:
- DDAT/DP00: 142 von 154 passend.
- WDAT/WP00: 178 von 198 passend.
- scbk/Scrp: 40 von 54 passend.
- adbk/ADBK: 7 von 8 passend.
- TMPL/Null-Creator: 2 von 2 passend.
- TOOL/Scrp: 1 von 1 passend.
- plnr/PLNR: 2 von 2 passend.

Die Beziehung ist stark genug, um sie als belastete Strukturhypothese weiterzuverfolgen, aber nicht als allgemeine Regel zu implementieren. Die 47 Gegenbeispiele müssen zuerst erklärt werden. Insbesondere darf Wert bei `0xCA` noch nicht ohne weitere Belege als Headerlänge oder Wert bei `0xCC` als Nutzdatenlänge bezeichnet werden.

### 6. Konkrete Referenzwerte

| Datei | Dateigröße | Marker | Wert 0xCA | DWORD 0xCC | Prüfung |
|---|---:|---|---:|---:|---|
| NEUES_DO.000 | 2352 (0x930) | EB AD | 0x00B0 | 0x00000880 | 0x930 - 0xB0 = 0x880 |
| TESTWRIT.000 | 2752 (0xAC0) | EB AD | 0x00B0 | 0x00000A10 | 0xAC0 - 0xB0 = 0xA10 |
| TESTDRAW.000 | 880 (0x370) | EB AD | 0x0080 | 0x000002F0 | 0x370 - 0x80 = 0x2F0 |
| NEUE_ZEI.000 | 608 (0x260) | EB AD | 0x0080 | 0x000001E0 | 0x260 - 0x80 = 0x1E0 |

### 7. Abgrenzung zu MiniCalc-Datei-I/O

Die MiniCalc-Referenz in `examples/minicalc/source-package/SRC/native.S` verwendet Kernel-Aufrufe für gewöhnliche Dateioperationen (open/create/read/write/close/rename/delete sowie Verzeichniswechsel). Die Adapterroutine `native_file` stellt vor dem Kernelaufruf den originalen GEOS-Stack wieder her und aktiviert Interrupts.

Die zugehörige `docs/FILE_IO_AND_DIALOGS.md` erklärt, dass die Basis-SDK-API diese Dienste noch nicht öffentlich bereitstellt und dass die Ordinale-/Error-Mappings erst nach echten GeoWorks-Laufzeittests als stabil gelten sollen.

MiniCalc speichert eigene `.MCS`- und `.WK1`-Dateien. Das ist kein Beleg dafür, dass damit bereits eine native VM-Dokumentdatei erzeugt wird. Die genaue VM-/Dokumentverwaltung und die Semantik der EB-AD-Struktur bleiben daher offen.

### 8. Konsequenzen für GEOTEST

Noch nicht implementieren:
- keinen eigenen Dokumentkopf allein aus den bisher beobachteten Feldern konstruieren;
- `EB AD` nicht als vollständig verstandenes VM-Format deklarieren;
- keine beliebige Datei mit `WDAT/GTD1` versehen und als gültiges GEOS-Dokument ausgeben;
- MiniCalc-Datei-I/O nicht mit VM-Dokumentverwaltung gleichsetzen.

Weiterer notwendiger Untersuchungsschritt:
- die 47 Gegenbeispiele klassifizieren;
- die Struktur ab Offset `0xC8` mit Block-/Verzeichnisstrukturen mehrerer Dokumenttypen vergleichen;
- Kernel-/Library-Aufrufe der GeoWorks-1.x-Dokumentverwaltung identifizieren;
- erst danach einen kontrollierten Erzeugungsprototyp entwerfen und in GeoWorks 1.2 testen.

### 9. Build-Status

Das bestehende GEOTEST-Grundprogramm wurde am 09.11.2026 in GeoWorks 1.2 gestartet; siehe `docs/GEOTEST_RUNTIME_TEST.md` im SDK-Repository. Das belegt nicht die neue Dokumentfunktion.

Das Grundprogramm kann unabhängig von dieser Dokumentformat-Untersuchung erneut gebaut werden. Eine GEOTEST-Version, die ein gültiges natives Dokument erzeugt und ein eigenes Dokument-Icon besitzt, ist noch nicht fertig.

### 10. Status

Ergebnis 2482: Die Dokumentdateien zeigen einen konsistenten EB-AD-Marker an Offset `0xC8` und eine auffällige Größenbeziehung zwischen den Feldern `0xCA/0xCC`. Die Beziehung trifft 372/419 untersuchte EB-AD-Dateien, aber nicht alle. Das ist ein neuer belastbarer Analyseansatz, noch keine fertige Formatdefinition und keine Laufzeitbestätigung.
