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

**Beweisstatus:** Diese Angaben sind hier zunächst nur als übernommene Arbeitsnotiz festgehalten. Die Datei `KERNEL_DIS.TXT` ließ sich laut Nutzer nicht erstellen. Die Quelle wurde deshalb aus dem nun bereitgestellten Archiv `GEOWORKS.zip` wiederhergestellt. Darin liegen `GEOWORKS/KERNEL.OLD` (72.688 Bytes) und `GEOWORKS/KERNEL.EXE` (72.736 Bytes). Verwendet wurde ausschließlich `KERNEL.OLD`; `KERNEL.EXE` blieb unangetastet. Der MZ-Header von `KERNEL.OLD` umfasst 96 Paragraphen = 1.536 Bytes. Der danach extrahierte Kernel-Body umfasst 71.152 Bytes und hat SHA-256 `948324ccd5fac49172548209c8137530dbdee6e3a64c81e2c52c503f5d85552d` – exakt den bereits im früheren Dossier dokumentierten Wert. Die Disassemblierung wurde reproduzierbar mit `objdump -D -b binary -m i8086 kernel_original_body.bin` erzeugt. Ihre SHA-256-Prüfsumme lautet `9356bbc05b83106f1e72f47ec6cb75163b1d1e5ed73152507203ead542d71461` und stimmt ebenfalls exakt mit dem früher dokumentierten Wert überein. Ein früherer Audit-Ankercheck wurde erneut ausgeführt: 53 von 53 Adressanker vorhanden. Damit ist die frühere Originalanalysegrundlage erfolgreich wiederhergestellt und unabhängig hashbestätigt. Die Originaldateien wurden nicht verändert; die Binärdateien werden aus Urheberrechtsgründen nicht in dieses öffentliche Repository hochgeladen.

Vor der Fortsetzung bleibt noch die Adressnotation der Arbeitsnotiz 2245 zu klären. Im reproduzierten Disassembly erscheinen die korrespondierenden Stellen als `10B20h`, `10B6Fh`, `10CAC h` und `10CC5h`; `10BD0h` liegt innerhalb einer Instruktion und ist kein Instruktionsanfang. Deshalb dürfen die verkürzten Angaben `0B20h`, `0BD0h`, `0CACh` und `0CC5h` nicht ungeprüft als gleichbedeutende Labels verwendet werden. Insbesondere ist `10B20h` zunächst nur ein Disassembly-Offset; seine Funktion als Code oder Daten muss anhand der Aufrufer und Kontrollflussreferenzen bestimmt werden.

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
| Untersuchungsnotiz 2245 | übernommen; Adressnotation wird gegen das wiederhergestellte Disassembly geprüft |
| Originalkernel-Body | aus `GEOWORKS/KERNEL.OLD` extrahiert; SHA-256 exakt bestätigt |
| Originaldisassemblierung | mit objdump neu erzeugt; SHA-256 exakt bestätigt; 53/53 Anker vorhanden |
| GEOTEST-Projektdateien | noch nicht erzeugt |
| GEOTEST.GEO | noch nicht gebaut |
| strukturelle GEO-Prüfung | ausstehend |
| Start in GeoWorks 1.2 | ausstehend |

## 6. Änderungs- und Belegregel

Jeder weitere Untersuchungsabschnitt erhält eine fortlaufende Nummer, Datum, Quellenidentität/Hashes, konkrete Instruktionsbereiche, Register- und Stacktabellen, Befunde, offene Fragen und eine klare Aussage, ob Dateien verändert oder Builds/Laufzeittests tatsächlich ausgeführt wurden. Keine Kernel- oder Treiberdatei wird ohne ausdrückliche Freigabe gepatcht.
