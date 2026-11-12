# Untersuchung 2479 – KLIB.GEO als Kernel Library identifiziert

**Stand:** 12.11.2026  
**Projekt:** GeoWorks 1.x / GEOTEST.GEO

## Ziel

Die Untersuchungen 2476–2478 verfolgten frühe Aufrufe im MZ-KERNEL.EXE. Der dort untersuchte Pfad betrifft Bootstrap, Dispatcher und Speicherblockverwaltung. Für die Suche nach Geode-Management-Routinen muss zusätzlich das eigenständige Kernel-Library-Modul geprüft werden.

## Fund in GEOWORKS.zip

Datei: `GEOWORKS/SYSTEM/KLIB.GEO`

- Größe: 55.478 Bytes
- SHA-256: `f7465303446b677690209972caca66fcd83c7651c0dbe74559319ad4053bf90a`
- Im Header stehen lesbar: permanenter Name `KLIB`, Token-Manufacturer `GEOS`, Beschreibung `Kernel Library`, Copyright `GeoWorks 1991`.

Damit ist KLIB.GEO ein eigenständiges GEODE-/Library-Modul im SYSTEM-Verzeichnis und nicht das MZ-KERNEL.EXE.

## Abgleich mit zeitgenössischer Dokumentation

Das Dokument „PC/GEOS System Software Overview“, Draft vom 10. November 1990, unterscheidet ausdrücklich Kernel und dynamisch geladene Libraries. Anhang C führt getrennte Größen auf:

- Kernel: 70,3 KB Dateigröße / 64,0 KB Codegröße
- Kernel Library: 52,6 KB Dateigröße / 47,4 KB Codegröße

KLIB.GEO ist 55.478 Bytes groß (ca. 54,2 KiB). Die Größenordnung passt zur historischen Angabe; der direkte Headername und die Beschreibung sind jedoch der stärkere Identitätsbeleg.

Anhang B führt unter „Geode (Executable File) Management Routines“ unter anderem `GeodeLoad`, `GeodeFreeDriver`, `GeodeLoadResourceAt` und `GeodeLockResource` auf.

Quelle: https://www.lyonlabs.org/commodore/onrequest/geos/PC-GEOS-System-Software-Overview.pdf  
Dokumentdatum 10.11.1990; Architekturabschnitt Seiten 2–3; Anhang B/C Seiten 52–55.

## Grenzen der Aussage

**Gesichert:**
- KLIB.GEO liegt im Archiv und ist im Header als „KLIB“ / „Kernel Library“ bezeichnet.
- Die historische Systembeschreibung unterscheidet Kernel und Kernel Library.
- Die historische API-Liste nennt gesonderte Geode-Management-Routinen.

**Noch nicht gesichert:**
- Dass `GeodeLoad`, `GeodeLoadResourceAt` oder `GeodeLockResource` in genau dieser KLIB.GEO-Version implementiert sind.
- Die Exportordinalen und Ressourcen-/Dateioffsets dieser Routinen.
- Ob Teile der Ladefunktion stattdessen im MZ-Kernel liegen.

Die Kernel-Aufrufziele `0000:0513`, `0000:6FD5` und `0000:6EDA` bleiben als Dispatcher-/Speicherblockpfad eingeordnet. Sie werden nicht ohne weitere Evidenz als GeodeLoad-Funktionen bezeichnet.

## Nächster Schritt: Untersuchung 2480

KLIB.GEO mit dem bereits verwendeten Format-1-Parser untersuchen:
1. Ressourcenanzahl und Attribute erfassen.
2. Import- und Exporttabellen extrahieren.
3. Exportordinalen auf Ressourcen und Offsets abbilden.
4. CALL-FAR-Einsprungpunkte und Ressourcen-Fixup-Tabellen untersuchen.
5. Nach Routinen suchen, die DOS-Dateizugriff, Ressourcenallokation und Fixup-Verarbeitung verbinden.

Erst danach kann eine symbolische Zuordnung zu GeodeLoad usw. geprüft werden.

## Änderungs- und Teststatus

- Keine Änderung am Parser oder SDK-Code.
- Kein GEOTEST.GEO-Build und kein Laufzeittest.
- KLIB.GEO wurde nur aus GEOWORKS.zip gelesen und anhand des Headers identifiziert.
- PC/GEOS-2.x-/FreeGEOS-Quellen wurden nicht als Implementierungsbeleg verwendet.
