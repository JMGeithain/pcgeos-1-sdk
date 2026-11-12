# GEOTEST – Untersuchung 2477

## Kernel-Systeminitialisierung: Modulnamen und Initialisierungsaufrufe

Stand: 12.11.2026

### 1. Untersuchungsziel und Grundlage

Fortsetzung der Untersuchung 2476. Ziel war, den zweiten frühen Fernaufruf und den anschließenden Kernel-Initialisierungspfad weiter einzugrenzen und nach konkreten Hinweisen auf das Laden von GEODE-Modulen zu suchen.

Untersucht wurde das gepatchte `GEOWORKS/KERNEL.EXE` aus `GEOWORKS.zip`:

- Größe: 72.736 Bytes
- SHA-256: `c2cc8952cdb01d0f459bf281ee3b78f8ce9464aba0b58c3758f8c73e24fb6eb5`

`KERNEL.OLD` bleibt die separate originale deutsche Vergleichsdatei. In dieser Untersuchung wurden keine Dateien verändert.

### 2. Präzisierung zur Routine bei 0F93:01C7

Der frühe Fernaufruf `0F93:01C7` erreicht den Kernel-Initialisierungspfad. Der Code ab Datei-Offset `0x100F7` (MZ-Header `0x600` plus Offset `0xA0F7`) führt eine lange Folge interner Initialisierungsaufrufe aus.

Ein Teil dieser Folge ist konkret als Konfigurationsdateiverarbeitung erkennbar:

- Ein Unterprogramm öffnet eine Datei mit DOS-Funktion `INT 21h/AH=3Dh`.
- Es liest bis zu `0x1F40` Bytes mit `INT 21h/AH=3Fh`.
- Der gelesene Text wird zeilenweise verarbeitet; CR/LF, Kommentarzeichen und Trennzeichen werden ausgewertet.
- Die Daten werden anschließend in Kernelzustandsfelder übernommen.

Die Datei ist im Code über einen CS-relativen Zeiger referenziert. Die exakte Zuordnung des Zeigers zu einem sichtbaren Dateinamen ist aus dieser isolierten Disassemblierung nicht abschließend bestätigt. Die Routine ist deshalb als Konfigurationsparser beschrieben, nicht als GEODE-Lader.

### 3. Sichtbare GEODE-Modulnamen im Kernel

Im Kernel-Abbild wurden folgende nullterminierte ASCII-Namen mit der Endung `.geo` gefunden:

- `klib.geo`
- `vidmem.geo`
- `local.geo`
- `kbd.geo`
- `nimbus.geo`
- `disk.geo`
- `EMMXXXX0emm.geo`
- `extMem.geo`
- `xms.geo`
- `dos2.geo`
- `dos3.geo`
- `dos4.geo`
- `dos5.geo`
- `drdos.geo`

Außerdem wurde der Name `geos.ini` gefunden.

Die ersten sechs Namen treten in der Umgebung des frühen Initialisierungscodes auf. Die Namen `EMMXXXX0emm.geo`, `extMem.geo` und `xms.geo` liegen in einem anderen Code-/Datenbereich und passen zu Speicher-/DOS-Umgebungsprüfungen. Die `dos2.geo` bis `drdos.geo`-Namen liegen ebenfalls in einem gesonderten Bereich. Diese Einordnung folgt aus Fundposition und umgebendem Code; sie ist keine vollständige Funktionszuweisung der jeweiligen Module.

### 4. Frühe Initialisierungsaufrufe und Modulbezug

Im Bereich der Initialisierungsroutine liegen unter anderem Aufrufe zu folgenden Datei-Offsets:

- `0x104CE`: Code unmittelbar vor dem String `klib.geo`
- `0x104F0`: Code unmittelbar vor dem String `vidmem.geo`
- `0x10520`: Code unmittelbar vor dem String `local.geo`
- `0x1057B` und `0x10592`: weitere Initialisierungsabschnitte in der Nähe der Strings `kbd.geo`, `nimbus.geo` und `disk.geo`

Die Abschnitte verwenden wiederkehrende Hilfsroutinen im Bereich der Datei-Offsets `0x1077B` bis `0x1081F`. In diesem Bereich werden unter anderem CS-relative Zeiger eingerichtet, ein Kernel-Fernaufruf bei `0000:0513` ausgeführt und – bei Erfolg – ein weiterer Fernaufruf bei `0000:6FD5` ausgeführt. Danach wird DS aus AX übernommen und SI auf null gesetzt.

Die Aufrufsequenz ist ein belastbarer Hinweis auf eine zentrale Kernel-Hilfsfunktion, die im Rahmen der Initialisierung mit den benannten Modul-/Ressourcendaten arbeitet. Die Semantik der Fernaufrufe `0000:0513` und `0000:6FD5` ist mit den bislang vorliegenden Symbolinformationen jedoch nicht sicher benannt. Es wäre voreilig, diese Hilfsroutine bereits als vollständigen GEODE-Lader oder als Fixup-Verarbeiter zu bezeichnen.

### 5. Abgrenzung: was noch nicht nachgewiesen ist

Nicht gefunden bzw. nicht sicher zugeordnet:

- die vollständige Routine, die eine beliebige `.GEO`-Datei öffnet und den GEODE-Header auswertet;
- die Stelle, an der die Ressourcentabelle gelesen und Ressourcen in Speicherblöcke überführt werden;
- die Schleife, die die pro Ressource gespeicherten Fixup-Einträge abarbeitet;
- die konkrete Semantik der class0/type0-Relokationen aus den Untersuchungen 2462–2474.

Die Modulnamen allein beweisen nicht, dass die in ihrer Nähe liegenden Routinen bereits den vollständigen Ladevorgang enthalten. Ebenso beweist ein Kernel-Fernaufruf mit anschließender DS-Übernahme noch keine Fixup-Verarbeitung.

### 6. Nächste sinnvolle Untersuchung

Als nächstes sollte der wiederkehrende Hilfsroutinenpfad `0x1077B–0x1081F` samt den Zielen der Fernaufrufe `0000:0513`, `0000:6FD5` und `0000:6EDA` separat untersucht werden. Parallel sollte der Codebereich um die Moduleinträge `klib.geo`, `vidmem.geo` und `local.geo` verglichen werden. Ziel ist festzustellen, ob die gemeinsame Routine lediglich Speicherblöcke/Handles verwaltet oder tatsächlich eine GEODE-Datei lädt.

Danach sollte gezielt nach dem Code gesucht werden, der die Ressourcentabelle und die Fixup-Tabellen verarbeitet. Bis zu diesem Nachweis bleiben Parser und GEOTEST.GEO unverändert.

### 7. Quellen- und Versionshinweis

Die GeoDump-Dokumentation von Marcus Gröber beschreibt auf hoher Ebene den Aufbau eines GEODE mit Zusatzheader, Bibliotheksliste, Exportliste, Ressourcentabelle und ressourcenbezogenen Fixup-Tabellen. Sie dient hier nur als Formatkontext, nicht als Beweis für eine bestimmte Routine in diesem GeoWorks-1.x-Kernel:

https://www.mgroeber.de/geodump-documentation.html

PC/GEOS-2.x-/FreeGEOS-Dokumentation wurde nicht als Beleg für die konkrete GeoWorks-1.x-Kernelimplementierung verwendet.

### 8. Änderungsstatus

- Keine Änderung am GEODE-Parser.
- Keine Änderung am SDK-Code.
- Kein GEOTEST.GEO-Build.
- Kein Laufzeittest.
- Nur statische Untersuchung der vorhandenen Kerneldatei.
