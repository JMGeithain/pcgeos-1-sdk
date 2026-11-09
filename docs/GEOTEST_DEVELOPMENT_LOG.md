# GEOTEST.GEO – Entwicklungsprotokoll

**Projekt:** erste ausführbare Testanwendung für GeoWorks 1.2 / PC/GEOS 1.x  
**SDK:** `JMGeithain/pcgeos-1-sdk`, Zweig `main`, SDK 0.1  
**Protokollstand:** 2026-11-09  
**Status:** Vorbereitung und Quellenabgleich; noch kein Build und kein Laufzeittest von `GEOTEST.GEO`

## 1. Verbindliche Projektgrenzen

- Zielsystem ausschließlich GeoWorks Ensemble 1.2 / PC/GEOS 1.x.
- Keine Übernahme von PC/GEOS 2.x oder FreeGEOS als Implementierungsbeleg.
- Originalinstallation, Originalkernel und Original-GEO-Dateien bleiben unverändert.
- Tests erfolgen später ausschließlich in einer separaten bzw. gesicherten GEOS-Testinstallation.
- Ein erzeugtes GEO gilt erst nach erfolgreicher struktureller Prüfung und anschließendem Start in GeoWorks als belastbar getestet.

## 2. Bestätigter SDK-Stand

Das öffentliche Repository ist `https://github.com/JMGeithain/pcgeos-1-sdk`; der Standardzweig ist `main`. Für dieses Repository ist Schreibzugriff des verbundenen GitHub-Kontos bestätigt.

SDK 0.1 beschreibt folgenden Build-Ablauf:

1. Zielarchiv prüfen und benötigte native Vorlagen anhand bekannter SHA-256-Werte identifizieren.
2. Freestanding-C-Code mit GCC/binutils oder LLVM/Clang kompilieren.
3. Assembler-Zwischencode instrumentieren und ELF-Objekte erzeugen.
4. Native ABI-Brücke und Ressourcen-/UI-Vorlagen einbinden.
5. GEOS-1.x-Geode mit Ressourcen, Imports, Protokollen und Relokationen paketieren.
6. Das Ergebnis erneut parsen und strukturelle Prüfungen ausführen.

Wichtige Einschränkungen aus der SDK-Dokumentation:

- Der dokumentierte Zielstand ist GeoWorks Pro 1.2 mit Kernel-Protokoll 622.3 und UI-Protokoll 693.0.
- Der moderne C-Pfad benötigt einen 80386 oder neuer; `-m16` macht daraus keinen 8086-C-Compiler.
- Die SDK-UI-Erzeugung verwendet versionsspezifische native Vorlagen.
- Host-Prüfungen ersetzen keinen echten Starttest in GeoWorks.

Maßgebliche Repository-Dokumente:
- `README.md`
- `docs/GETTING_STARTED.md`
- `docs/SDK_MANUAL.md`
- `docs/BUILD_SYSTEM.md`
- `docs/TARGET_COMPATIBILITY.md`

## 3. Übernommener Untersuchungsstand 2245 – noch zu verifizieren

Aus dem Gesprächsübergang wurde als letzter Untersuchungsstand genannt:

- Routine bzw. Einstieg `0B20h)
- offene Nachbar-/Unterroutine-Adressen `0BD0h`, `0CACh` und `0CC5h`
- beobachteter Kopiervorgang bei `0B6Fh–0B75h` mit elf Bytes

**Beweisstatus:** Diese Angaben sind hier zunächst nur als übernommene Arbeitsnotiz festgehalten. Die zugrunde liegende vollständige `KERNEL_DIS.TXT` und der exakt zugehörige Kernel-Body liegen für diese Fortsetzung nicht als prüfbare Quelle vor. Deshalb werden daraus noch keine neuen Aussagen über Registerverträge, Kontrollfluss oder GEOTEST-ABI abgeleitet.

Vor einer Fortsetzung der Disassemblierungsanalyse müssen feststehen:
- genaue Kerneldatei und Version,
- SHA-256 des Kernel-Bodys,
- SHA-256 der Disassemblierung,
- eindeutige Zuordnung der Adressen zu Dateioffset, Kernel-Body-Offset oder Disassembler-Label.

## 4. Nächste Arbeitsschritte

### Untersuchung 2246 – Quellenidentität und Reproduzierbarkeit
1. Original-`KERNEL_DIS.TXT` und passenden Kernel-Body beschaffen.
2. Dateigrößen und SHA-256 erfassen.
3. Prüfen, ob die Offsets in der Disassemblierung zum bekannten Kernel-Body passen.
4. Erst danach `0B20h), `0BD0h`, `0CACh` und `0CC5h` mit vollständigem Instruktionskontext untersuchen.
5. Registerein-/ausgänge, Stackdelta, Segmentannahmen, Speicherzugriffe und alle Rücksprungpfade dokumentieren.
6. Beobachtung, Ableitung und offene Hypothese getrennt kennzeichnen.

### GEOTEST-Projekt – minimaler Buildpfad
1. SDK-Quellstand und Beispielprojekt `examples/hello` vollständig prüfen.
2. Den vom SDK vorgesehenen Projektgenerator verwenden, statt Projektdateien oder private UI-Strukturen zu erraten.
3. Ein minimales Projekt mit permanent name `geotest`, eindeutigem Vier-Zeichen-Token und Ausgabe `GEOTEST.GEO` erzeugen.
4. Zielarchiv mit dem dokumentierten kompatiblen GeoWorks-1.2-Vorlagensatz prüfen.
5. Zunächst unveränderten Minimaltest bauen; Build-Bericht, Map, Symbole und Zwischenartefakte sichern.
6. GEO-Datei mit dem SDK-Inspector prüfen: Format, Kernel-/UI-Protokolle, Ressourcen, Imports und Relokationen.
7. Erst nach bestandener Host-Prüfung in einer Wegwerf-/Snapshot-Installation starten.
8. Loader-Meldungen, Fensterdarstellung, Tastatur, Maus, Redraw und sauberes Beenden protokollieren.

## 5. Aktueller Status – keine unbelegten Erfolgsmeldungen

| Punkt | Status |
|---|---|
| Repository und Schreibberechtigung | bestätigt |
| SDK 0.1 Buildarchitektur | aus Repository-Dokumentation bestätigt |
| GeoWorks-1.2 Zielprotokolle | dokumentiert: Kernel 622.3, UI 693.0 |
| Untersuchungsnotiz 2245 | übernommen, Primärquelle fehlt |
| vollständige Kernel-Disassemblierung für 2246 | fehlt |
| GEOTEST-Projektdateien | noch nicht erzeugt |
| GEOTEST.GEO | noch nicht gebaut |
| strukturelle GEO-Prüfung | ausstehend |
| Start in GeoWorks 1.2 | ausstehend |

## 6. Änderungs- und Belegregel

Jeder weitere Untersuchungsabschnitt erhält eine fortlaufende Nummer, Datum, Quellenidentität/Hashes, konkrete Instruktionsbereiche, Register- und Stacktabellen, Befunde, offene Fragen und eine klare Aussage, ob Dateien verändert oder Builds/Laufzeittests tatsächlich ausgeführt wurden. Keine Kernel- oder Treiberdatei wird ohne ausdrückliche Freigabe gepatcht.
