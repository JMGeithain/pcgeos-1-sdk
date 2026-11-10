# GEOTEST.GEO – Entwicklungsprotokoll

**Projekt:** erste ausführbare Testanwendung für GeoWorks 1.2 / PC/GEOS 1.x  
**SDK:** `JMGeithain/pcgeos-1-sdk`, Zweig `main`, SDK 0.1  
**Protokollstand:** 2026-11-09  
**Status:** `GEOTEST.GEO` wurde am 09.11.2026 vom Nutzer erfolgreich in GeoWorks 1.2 gestartet. Hauptfenster und Help-Dialog sind sichtbar; der Nutzer bestätigt ausdrücklich: „es geht alles“. Der Laufzeittest ist damit für den gezeigten Funktionsumfang bestätigt. Vollständige Quellbyteidentität mit GitHub-HEAD und automatisierte Wiederholbarkeit des Builds bleiben davon getrennte, weiterhin offene Punkte. Eine zwischenzeitlich vermutete Farzeiger-Fehlordnung wurde in Untersuchung 2274 durch erneuten Byteabgleich widerlegt; der ursprüngliche Packer entspricht den beiden untersuchten Vorlagen.

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

Die Adressprüfung hat zwei getrennte Bereiche ergeben, die in der Arbeitsnotiz 2245 zunächst vermischt wurden:

- **Offsetbereich `0B20h` bis `0B86h`:** `0B20h` ist eine echte Codeadresse. Die Routine wird von `0A2Bh` aus aufgerufen. Sie initialisiert einen zuvor angeforderten 16-Byte-Block. Innerhalb dieser Routine liegt der 11-Byte-Kopiervorgang bei `0B6Fh–0B75h`; Einzelheiten sind in Untersuchung 2255 dokumentiert.
- **Offsetbereich `10B1Ah` bis `10BD6h`:** Dies ist ein anderer, eigenständiger Bereich. `10B1Ah–10B52h` enthält Tabellenwerte und Dateinamenfragmente (`dos2.geo`, `dos3.geo`, `dos4.geo`, `dos5.geo`, `drdos.geo`). Der Codekandidat beginnt erst bei `10B53h`. Bei `10B6Fh` liegt hier ein fünf Byte langer Far-Aufruf (`lcall $0x0,$0x399`), gefolgt von `mov $0x19,%ax` bei `10B74h`. `10BD0h` liegt innerhalb der Instruktion ab `10BCFh` (`lcall *0x5b8`) und ist kein gültiger Instruktionsanfang.

**Korrektur:** Die frühere Notiz „11 Bytes kopiert“ ist für `0B20h` richtig und durch den tatsächlichen `rep movsb`-Befehl bestätigt. Sie ist nicht auf `10B6Fh–10B75h` zu beziehen. Die Adressen `0B20h` und `10B20h` sowie `0B6Fh` und `10B6Fh` bezeichnen unterschiedliche Offsets und dürfen nicht gleichgesetzt werden.

## 4. Nächste Arbeitsschritte

### Untersuchung 2246 – Quellenidentität und Reproduzierbarkeit
1. Original-`KERNEL.OLD` und den extrahierten Kernel-Body aus dem bereitgestellten Archiv sichern.
2. Dateigrößen und SHA-256 erfassen; Extraktion und Disassemblierung reproduzieren.
3. Offsets im vollständigen Disassembly gegen Instruktionsgrenzen und Kontrollfluss prüfen.
4. Datenbereich `10B1Ah–10B52h` von anschließendem Codekandidaten `10B53h` trennen.
5. Registerein-/ausgänge, Stackdelta, Segmentannahmen, Speicherzugriffe und Rücksprungpfade des Blocks `10B53h–10BD6h` dokumentieren.
6. Die verkürzte Adressnotation aus der Arbeitsnotiz 2245 nicht weiterverwenden, solange ihr Bezugssegment bzw. ihre Basis ungeklärt ist.
7. Beobachtung, Ableitung und offene Hypothese getrennt kennzeichnen.

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
| Untersuchungsnotiz 2245 | Adressvermischung in Untersuchung 2255 korrigiert; `0B20h` und `10B20h` getrennt, 11-Byte-Kopie bestätigt |
| Originalkernel-Body | aus `GEOWORKS/KERNEL.OLD` extrahiert; SHA-256 exakt bestätigt |
| Originaldisassemblierung | mit objdump neu erzeugt; SHA-256 exakt bestätigt; 53/53 Anker vorhanden |
| Untersuchung 2246 | Daten-/Codegrenze und Codekandidat `10B53h–10BD6h` statisch untersucht; Funktionsvertrag offen |
| Untersuchung 2247 | Querverweise und Aufrufziele `0399h`, `2588h`, `101CBh` untersucht; DS-Segmentkorrektur dokumentiert |
| Untersuchung 2248 | Wiederholte `05B8h`-Far-Aufrufe verglichen; gemeinsame Dispatch-Schnittstelle als Hypothese markiert |
| Untersuchung 2249 | Schreibzugriffe auf `05B8h/05BAh` vollständig verglichen; Offset-/Segment-Paar nachgewiesen |
| Untersuchung 2250 | DI-Aufrufvarianten und unterschiedliche Rückgabekanäle verglichen; keine einheitliche Callback-Signatur unterstellt |
| Untersuchung 2251 | Überlappende Segmentladehelfer analysiert; DS/ES in den untersuchten Callback-Pfaden auf `0E35h` zurückgeführt |
| Untersuchung 2252 | Listenanker `05AEh`, Kopf-Link `05B2h`, Statusfelder und zweites Far-Zeigerpaar untersucht |
| Untersuchung 2253 | Knotenlayout der Liste und beide direkten Aufrufer von `11CBh` untersucht |
| Untersuchung 2254 | 26-Byte-Indexdatensätze und Herkunft des Knotenfeldes `+06h` verfolgt |
| Untersuchung 2255 | Routine `0B20h`, 16-Byte-Block und 11-Byte-Kopie vollständig bestätigt |
| Untersuchung 2256 | Status-/Konfigurationspfad `0BD0h` und Datenquelle `[0192h]` untersucht |
| Untersuchung 2257 | Semaphore- und kontextabhängige Synchronisationswrapper identifiziert |
| Untersuchung 2258 | Warte-/Aufweckpfade und Scheduler-Wartelisten statisch untersucht |
| Untersuchung 2259 | Objektliste, Speicherfreiliste und Scheduler-Warteliste strukturell getrennt; unterschiedliche Linkfelder belegt |
| Untersuchung 2260 | Synchronisationsobjekte anhand konkreter Aufruferprofile zugeordnet; Startwerte weiterhin offen |
| Untersuchung 2261 | MZ-Header und Relokation `CS:962Eh` ausgewertet; Segmentnotation präzisiert |
| Untersuchung 2262 | GEOWORKS.zip auf SDK-Pfade, Hashes, Formate und Protokolle geprüft; direkt nicht kompatibel, Profilpfad möglich |
| Untersuchung 2263 | Tatsächlich verwendete UI-Template-Ressourcen und Handles strukturell verglichen; Referenzmerkmale reproduziert |
| Untersuchung 2264 | Erster experimenteller Host-Build von GEOTEST.GEO erzeugt und strukturell geprüft |
| Untersuchung 2265 | GEOTEST-Quellprojekt und Zielarchiv-Vorbereitung veröffentlicht |
| Untersuchung 2266 | Byteidentitätsprüfung deckt Abweichungen zwischen lokalem Build-Unterbau und GitHub-HEAD auf; Reproduzierbarkeit ausdrücklich nicht bestätigt |
| Untersuchung 2267 | Test-Gates und Selftest-Annahmen gegen das deutsche Zielprofil geprüft; Standard-Selftest scheitert erwartungsgemäß an strikten Referenzhashes |
| Untersuchung 2268 | Zielprofil-Integrität geprüft: `allow_unknown_target` umgeht den Hashschutz vollständig; abgesicherter Profilvertrag erforderlich |
| Untersuchung 2269 | Rückwärtskompatibles Zielprofil-Design festgelegt; Hashprüfung wird pro benanntem Profil statt per globalem Bypass ausgewählt |
| Untersuchung 2270 | Explizite Hash-gepinnte Zielprofile im Buildsystem implementiert; Unit-Tests für Profilgrenzen ergänzt; Laufzeittest noch ausstehend |
| Untersuchung 2271 | Neun Profil-/Bypass-Unit-Tests, Parser-Absatzregression und realer deutscher Profil-Parse erfolgreich ausgeführt |
| Untersuchung 2272 | GitHub Actions testet den aktuellen Repository-Checkout erfolgreich: Python-Compile, Profiltests und GEODE-Absatzregression PASS |
| Untersuchung 2273 | Build mit rekonstruierter GitHub-Quellfassung wiederholt; identischer GEO-Hash, Quellbyteidentität weiterhin offen |
| Untersuchung 2274 | Erste Farzeiger-Fehlinterpretation durch korrekte Tabellenposition widerlegt; ursprüngliche Reihenfolge des Packers bestätigt |
| Untersuchung 2275 | Korrekte Farzeiger-Serialisierung in Hilfsfunktion gekapselt; Offset/Resource- und Relokationsregression ergänzt |
| Untersuchung 2276 | Acht Prozessmethoden und ihre Eintrittspunkte statisch gegen Original-1.x-Code und Nachrichtenvertrag geprüft; Help-Nachricht 0C0Ah intern abgeglichen |
| Untersuchung 2277 | Superclass-Aufrufe 01E9h und Help-ObjMessage-Pfad 0096h/00A9h mit Originalcode und SDK-Aufrufen abgeglichen |
| GEOTEST-Projektdateien | experimentelles Projekt im lokalen Build-Arbeitsverzeichnis erzeugt; noch nicht als SDK-Projekt committen |
| GEOTEST.GEO | erster Host-Build erfolgreich; SHA-256 `9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b` |
| strukturelle GEO-Prüfung | Parserprüfung erfolgreich: Format 1, 12 Ressourcen, 41 Relokationen, Kernel 622.3, UI 693.0 |
| Start in GeoWorks 1.2 | **erfolgreich vom Nutzer bestätigt am 09.11.2026**; Hauptfenster und Help-Dialog sichtbar; siehe Untersuchung 2278 |




## 6. Änderungs- und Belegregel

Jeder weitere Untersuchungsabschnitt erhält eine fortlaufende Nummer, Datum, Quellenidentität/Hashes, konkrete Instruktionsbereiche, Register- und Stacktabellen, Befunde, offene Fragen und eine klare Aussage, ob Dateien verändert oder Builds/Laufzeittests tatsächlich ausgeführt wurden. Keine Kernel- oder Treiberdatei wird ohne ausdrückliche Freigabe gepatcht.


## 7. Untersuchung 2246 – Daten-/Codegrenze und Block 10B53h–10BD6h

**Quelle:** derselbe reproduzierte Disassembly-Stand aus `GEOWORKS/KERNEL.OLD`; Kernel-Body SHA-256 `948324ccd5fac49172548209c8137530dbdee6e3a64c81e2c52c503f5d85552d`; Disassembly SHA-256 `9356bbc05b83106f1e72f47ec6cb75163b1d1e5ed73152507203ead542d71461`. Die Untersuchung ist statisch; kein Kernel wurde verändert oder ausgeführt.

### 7.1 Datenbereich `10B1Ah–10B52h`

Nach `10B18h` (`jmp 10B11h`) folgt kein plausibler linearer Instruktionsfluss. Der Bereich enthält:
- vier 16-Bit-Werte bei `10B1Ah`, `10B1Ch`, `10B1Eh` und `10B20h`: `1222h`, `122Bh`, `1234h`, `123Dh` (Little Endian);
- ab `10B23h` die nullterminierten Zeichenketten `dos2.geo`, `dos3.geo`, `dos4.geo`, `dos5.geo` und `drdos.geo`;
- die Zeichenketten enden bei `10B52h`; der nächste disassemblierte Block beginnt bei `10B53h`.

**Befund:** `10B20h` liegt innerhalb der vier-Wort-Tabelle und ist kein belegter Codeeinstieg. Die ab `10B20h` angezeigten x86-Instruktionen sind eine Fehlinterpretation der Tabellen-/Stringbytes durch lineare Disassemblierung. Die Werte `1222h` bis `123Dh` sehen wie Offsets aus, aber ihre genaue Referenzbasis und Funktion sind noch nicht nachgewiesen.

### 7.2 Codekandidat `10B53h–10BD6h`

Der Bereich ab `10B53h` ist syntaktisch plausibler 16-Bit-Code. Er besitzt in der linearen Disassemblierung keinen direkten eingehenden relativen Sprung aus dem unmittelbar vorhergehenden Bereich; ein indirekter Einstieg oder eine externe Referenz ist damit nicht ausgeschlossen. Eine vollständige Funktionszuordnung ist noch offen.

| Offset | Beobachteter Befehl / Effekt | Register- und Speicherbefund |
|---|---|---|
| `10B53h` | `mov %bx,%ds` | DS wird aus BX geladen; BX muss zu diesem Zeitpunkt bereits einen gültigen Segmentwert enthalten. |
| `10B55h` | `mov $1246h,%si` | SI erhält einen konstanten Offset. |
| `10B58h` | `cmpb $0,05B1h` | prüft ein Byte im Datensegment; bei ungleich null Sprung nach `10B90h`. |
| `10B5Fh` | `mov 05ABh,%bl`; `xor %bh,%bh` | BL wird aus Speicher geladen, BH auf null gesetzt; BX ist danach nullerweitertes Byte. |
| `10B65h–10B6Ah` | setzt `[0046h]=4`; `sub $2,%bx` | Bytezustand wird vorübergehend auf 4 gesetzt; BX wird um 2 vermindert. |
| `10B6Dh` | `jae 10B77h` | bei BX >= 2 wird der erste Fehler-/Fallback-Aufruf übersprungen. |
| `10B6Fh` | `lcall 0000h:0399h`; danach `AX=0019h` | fünf Byte langer Far-Aufruf, gefolgt von AX-Ladebefehl; kein elf Byte langer Kopiervorgang. |
| `10B77h` | setzt `[0046h]=0` | setzt den zuvor auf 4 gesetzten Status zurück. |
| `10B7Ch–10B86h` | vergleicht BX mit 4; ggf. Far-Aufruf `0000h:0399h`, danach `AX=0019h` | zweiter Fehler-/Fallback-Pfad. |
| `10B89h–10B8Bh` | `shl $1,%bx`; lädt `CS:[121Ah+BX]` nach SI | BX wird als Worttabellenindex (Byteoffset nach Verdopplung) verwendet; SI erhält den ausgewählten Tabellenwert. |
| `10B90h–10B96h` | DI aus `[0044h]`; DS=CS; near call `101CBh` | Aufruf mit SI/DI und Code-Segment als DS; genaue Parameterbedeutung von `101CBh` separat zu untersuchen. |
| `10B99h–10BA0h` | bei Carry Far-Aufruf `0000h:0399h`, danach `AX=000Fh` | Fehler-/Fallback-Pfad; anschließend ES=AX. |
| `10BA5h` | speichert BX nach `[0609h]` | sichert den ausgewählten Indexwert. |
| `10BA9h–10BAFh` | DS sichern; Far-Aufruf `0000h:2588h`; liest zwei Worte von DS:SI; DS wiederherstellen | AX/BX werden aus `[SI]` und `[SI+2]` geladen. |
| `10BB5h–10BB8h` | speichert AX/BX nach `[05B8h]`/`[05BAh]` | legt offenbar einen später verwendeten Far-Zeiger in zwei benachbarten Worten ab; Interpretation als Funktionszeiger ist durch den späteren indirekten Aufruf gestützt. |
| `10BBCh–10BC2h` | testet Bit `10h` in `ES:[0003h]`; ggf. Rücksprung | bedingter Zusatzpfad. |
| `10BC4h–10BD6h` | liest ES:[0040h], sichert BX, liest Byte über DS:BX, setzt DI=14h, führt `lcall DS:[05B8h]` aus, stellt DI wieder her und schreibt BL nach DS:DI | `10BCFh` ist Beginn der vier Byte langen indirekten Far-Aufrufinstruktion. `10BD0h` liegt mitten in ihr und ist kein Instruktionsanfang. |

**Wichtige Einschränkung:** Die Tabellenbasis `CS:121Ah`, die Bedeutung von `[05ABh]`, `[05B1h]`, `[0044h]`, `[0046h]` und die Verträge der Far-Aufrufe `0000h:0399h` / `0000h:2588h` sind noch nicht geklärt. Deshalb ist `10B53h` vorerst ein *Codekandidat*, kein abschließend bewiesener öffentlicher Routineeinstieg. Auch die Registerwerte beim Eintritt sind unbekannt.

### 7.3 Nachbarstellen

- `10BD7h` enthält `call 10BDBh`; `10BDBh` beginnt mit `cli`, sichert SI und ES, bearbeitet anschließend 16 IVT-Einträge ab physischer Adresse `0000:0200h` und endet mit `sti; ret` bei `10C05h`. Diese Routine ist separat zu analysieren, insbesondere wegen der Interruptsperre und der gespeicherten Vektoren.
- `10CACh` ist zwar eine Instruktionsgrenze (`pop es`), steht aber direkt nach zwei `push ds` bei `10CAAh`/`10CABh`; das allein beweist keinen Routinenanfang.
- `10CC5h` ist eine Instruktionsgrenze (`push cs`), aber Teil einer fortlaufenden Sequenz ab `10CC4h` (`push ds`) und `10CC6h` (`pop ds`); auch das ist kein Beleg für einen eigenständigen Einstieg.
- `10BD0h` ist definitiv keine Instruktionsgrenze im vorliegenden linearen Disassembly.

### 7.4 Ergebnis von Untersuchung 2246

1. Die vier Werte bei `10B1Ah–10B20h` und die DOS-Dateinamen bei `10B23h–10B52h` sind als Datenbereich zu behandeln.
2. `10B20h` ist als Codeeinstieg verworfen.
3. `10B53h–10BD6h` ist ein plausibler Codeblock mit einem indirekten Far-Aufruf über den zuvor gespeicherten Zeiger `DS:[05B8h]`; die Eintrittsbedingungen und Gesamtfunktion bleiben offen.
4. Die alte Notiz „elf Bytes kopiert bei `0B6Fh–0B75h`“ wird nicht übernommen: der sichtbare Code an `10B6Fh` ist ein Far-Aufruf und die inklusive Spanne `10B6Fh–10B75h` umfasst sieben Bytes.
5. `10BD0h` ist als Instruktionsanfang ausgeschlossen; `10CACh` und `10CC5h` sind zwar Instruktionsanfänge, aber keine belegten Routineeinstiege.

**Nächster Schritt 2247:** Querverweise auf Datenoffsets `121Ah`, `1246h`, `05ABh`, `05B1h`, `05B8h`, `05BAh`, `0044h`, `0046h`, `0609h` systematisch sammeln; danach die aufgerufenen Kernelziele `0399h`, `2588h` und Near-Routine `101CBh` mit vollständigem Aufrufer-/Aufrufkontext untersuchen.


## 8. Untersuchung 2247 – Querverweise und aufgerufene Hilfsroutinen

**Quelle und Methode:** vollständige Datei `kernel_original_body.dis`, erzeugt aus dem unveränderten `GEOWORKS/KERNEL.OLD`-Kernel-Body. Es wurden alle Vorkommen der relevanten absoluten Offsets und Aufrufziele im linearen Disassembly gesucht und die Zielbereiche im Kontext gelesen. Die Suche findet nur im disassemblierten Byte-Image statt; segmentabhängige Laufzeitdaten können dadurch nicht vollständig aufgelöst werden.

### 8.1 Daten-/Statusoffsets

- `05ABh`: Im vorliegenden Disassembly ist ein direkter Zugriff bei `10B5Fh` (`mov 05ABh,%bl`) und ein weiterer bei `110E` (`cmpb $3,05ABh`) sichtbar. Damit ist `05ABh` kein isolierter lokaler Wert dieses Blocks; die genaue Bedeutung des Bytes ist noch offen.
- `05B1h`: Der hier untersuchte Block liest den Wert bei `10B58h` und verzweigt bei ungleich null nach `10B90h`. Weitere direkte Vorkommen wurden im Disassembly nicht gefunden.
- `05B8h`: Das Wort wird bei `10BB5h` geschrieben und bei `10BCFh` indirekt als Far-Ziel aufgerufen. Es gibt mehrere weitere indirekte Aufrufe über denselben Offset im Kernel, u. a. bei `0E7Dh`, `0F20h`, `0F3Bh`, `0F4Eh`, `0F76h`, `1189h`, `129Bh`, `1321h` und `13A8h`. Der Operand ohne Segmentpräfix verwendet DS; die frühere Formulierung `0000:[05B8h]` war falsch und ist korrigiert. Die tatsächliche Segmentbasis hängt vom jeweiligen Aufrufer ab.
- `05BAh`: Der Block speichert bei `10BB8h` das zweite Wort neben `05B8h`. Das passt zu einem Far-Pointer-Paar (Offset/Segment), ist aber allein noch kein Beweis für die Bedeutung jedes Wortes.
- `0044h`: Dieses Wort wird im Kernel an zahlreichen Stellen gelesen und geschrieben. Der Zugriff bei `10B90h` lädt es nach DI; weitere Verwendungen zeigen, dass es sich um einen übergreifenden Laufzeit-/Stack-/Segmentzustandswert handeln kann. Die genaue Struktur ist noch zu ermitteln.
- `0046h`: Dieses Byte/Wort wird ebenfalls an vielen Stellen verwendet. Der untersuchte Block setzt es vorübergehend auf `04h` und danach auf `00h`; andere Routinen testen bzw. verändern Bits dieses Feldes. Es ist daher ein gemeinsames Status-/Flags-Feld und nicht einfach eine lokale Kopiervariable.
- `0609h`: `10BA5h` speichert BX hier; Routine `25A5h` liest den Wert später nach DX. Der gespeicherte Wert ist der zuvor verdoppelte Index aus BX. Eine weitergehende semantische Benennung ist noch nicht gesichert.
- `CS:[121Ah+BX]`: Einziger direkter Fund dieses indizierten Lesezugriffs. Die Tabelle wird mit dem aktuellen BX-Index angesprochen. Der Tabelleninhalt und seine Basis müssen bytegenau untersucht werden; die einfache lineare Disassemblierung kann überlagerte Daten nicht zuverlässig klassifizieren.
- `SI=1246h`: Die Konstante wird bei `10B55h` geladen. Offset `1246h` ist im linearen Disassembly zugleich das `ret` am Ende eines anderen Codeblocks. Da SI anschließend durch die Hilfsaufrufe verändert werden kann und die Segmentwerte wechseln, darf aus dem numerischen Gleichstand keine Funktionsbeziehung abgeleitet werden.

### 8.2 Ziel `0000:2588h` – Objekt-/Zeigerauflösung

Die Routine bei `2588h` besteht aus:

- Near-Aufruf `9630h`;
- `mov (%bx),%ds` – DS wird aus dem durch BX adressierten Wort geladen;
- `mov 28h,%si` – SI wird aus Offset `28h` im nun gewählten Segment geladen;
- `mov 2Ah,%ds` – DS wird anschließend aus Offset `2Ah` desselben Segments geladen;
- `lret`.

**Belegter Effekt:** Die Routine liefert durch Änderung von DS und SI einen Segment:Offset-Kontext zurück. Der untersuchte Aufrufer `10BA9h–10BB8h` liest anschließend zwei Worte aus DS:SI und legt sie bei `05B8h`/`05BAh` ab. Dies stützt die Interpretation, dass dort ein später verwendeter Far-Zeiger vorbereitet wird. Die genaue Struktur des durch BX adressierten Objekts und die Bedeutung der Felder `28h`/`2Ah` bleiben offen.

### 8.3 Ziel `0000:0399h` – Fehler-/Abbruchpfad

`0399h` springt nach `039Ch`. Dort werden BP, SI, DS und AX gesichert, Interrupts gesperrt und ein Stackframe aufgebaut. Der Code kann über den gesicherten Stack einen Segment:Offset-Kontext laden, liest einen Wortwert, aktualisiert Status bei `0046h` und führt umfangreiche globale Aufräum-/Abbruchschritte aus. Später wird SS:SP auf einen internen Stack umgestellt; mehrere globale Routinen werden aufgerufen. Je nach Status endet der Pfad u. a. mit DOS-Funktionsaufruf `int 21h`/`4C00h` oder einem Far-Rücksprung.

**Sicherer Befund:** `0399h` ist kein gewöhnlicher Rückgabewert-Lieferant, sondern ein globaler Fehler-/Abbruchpfad mit Interrupt- und Stackmanipulation. Welche Fehlercodes und Zustände er konkret behandelt, muss aus seinen Aufrufern und den nachfolgenden Pfaden abgeleitet werden. In `10B6Fh`, `10B81h` und `10B9Bh` wird er jeweils als Fehlerbehandlung aufgerufen; anschließend wird AX explizit auf `0019h` bzw. `000Fh` gesetzt.

### 8.4 Ziel `101CBh` – Initialisierungs-/Setup-Hilfsroutine

Der Block `101CBh–101EFh` ruft nacheinander `1531h`, setzt AX auf `3`, ruft `15A0h`, löscht AX/BX/CX/DX, ruft `1970h`, setzt DI auf `0E35h`, lädt DS mit `0E35h`, ruft `156Ch` und kehrt zurück. Es gibt lokale Wrapper bei `101B4h` und `101BCh`; der untersuchte Block `10B90h` ruft `101CBh` direkt auf.

**Sicherer Befund:** `101CBh` ist eine Setup-Sequenz mit mehreren Kernel-Far-Aufrufen und einem am Ende explizit gesetzten DS=`0E35h`. Das ist für den folgenden Zugriff auf `DS:[05B8h]` im untersuchten Pfad relevant. Die semantischen Verträge der Unteraufrufe `1531h`, `15A0h`, `1970h` und `156Ch` sind noch nicht entschlüsselt.

### 8.5 Ergebnis und Korrektur

1. `05B8h` wird im Kernel mehrfach als Speicheroperand indirekter Far-Aufrufe verwendet; im Block `10BCFh` ist es `DS:[05B8h]`, nicht `0000:[05B8h]`.
2. `2588h` liefert einen geänderten DS:SI-Kontext; der Aufrufer speichert zwei daraus gelesene Worte als Paar bei `05B8h`/`05BAh`.
3. `0399h` ist ein globaler Fehler-/Abbruchpfad, der Interrupts und Stack aktiv manipuliert. Seine Aufrufe dürfen nicht als normale Funktionsrückkehr interpretiert werden.
4. `101CBh` setzt DS am Ende auf `0E35h`; im untersuchten Ablauf wird danach `DS:[05B8h]` vorbereitet bzw. verwendet.
5. Die Semantik der Indextabelle `CS:[121Ah+BX]`, der Objektfelder `28h`/`2Ah` und der Statusfelder `05ABh`/`05B1h` ist noch offen.

**Nächster Schritt 2248:** Den Ablauf um `05B8h` in den weiteren Aufrufern (insbesondere `0E7Dh–0F76h`, `1189h`, `129Bh`, `1321h`, `13A8h`) vergleichen, um die Struktur und Segmentbasis des gespeicherten Far-Zeigers zu bestimmen. Parallel die Routine `2588h`-Aufrufer und das Objektformat mit konkreten DS-/BX-Werten aus den statischen Datenbereichen rekonstruieren.


## 9. Untersuchung 2248 – Vergleich der Far-Aufrufe über `05B8h`

**Ziel:** Prüfen, ob `05B8h` nur im Block `10B53h–10BD6h` verwendet wird oder eine gemeinsame indirekte Schnittstelle darstellt.

### 9.1 Vergleichte Aufrufstellen

Im Disassembly gibt es neben `10BCFh` weitere Aufrufe über denselben Offset:

| Offset | Operand / DI | Kontext vor dem Aufruf | Beobachtung |
|---|---|---|---|
| `0E7Dh` | `DS:[05B8h]`, DI=`18h` | CX aus `[01A0h]`, DX=0; Register werden gesichert | Aufruf einer indirekten Far-Funktion mit Selektor `18h`. |
| `0F06h–0F0Ah` | setzt `[05BAh]=0` | DS wird über `9630h` vorbereitet | löscht das zweite Wort des Zeigerpaares; möglicherweise Deaktivierung/Invalidierung, genaue Semantik offen. |
| `0F12h–0F2Dh` | `ES:[05B8h]`, DI=`12h` | ES/DI gesichert; Hilfsroutinen `172Fh`, `15EBh` davor und `1628h`, `1736h` danach | explizit ES-basierter Aufruf; Segmentbasis unterscheidet sich vom DS-Fall. |
| `0F2Eh–0F42h` | `DS:[05B8h]`, DI=`06h` | BL aus `(BX)` geladen; Flags gesichert | Aufruf mit Byteparameter und DI-Selektor `06h`. |
| `0F43h–0F55h` | `DS:[05B8h]`, DI=`08h` | Flags gesichert; DS gesichert | weiterer Selektor-Aufruf, Flags werden über den Aufruf hinweg erhalten. |
| `0F6Dh–0F7Eh` | `ES:[05B8h]`, DI=`16h` | ES/DI/BX gesichert; `9636h` davor | ES-basierter Aufruf mit Selektor `16h`. |
| `1189h` | `DS:[05B8h]` | liegt im Umfeld eines I/O-/Dateioperationen-Blocks | bestätigt weitere Verwendung des DS-basierten Zeigers. |
| `129Bh` | `DS:[05B8h]`, DI=`0Ah` | AL und CL aus zwei verketteten Strukturen geladen; Flags danach mit `sahf` ausgewertet | Rückgabestatus/Flags des indirekten Aufrufs beeinflussen die Verzweigung. |
| `1321h` | `ES:[05B8h]`, DI=`04h` | ES-Zeiger über `9636h`; AX wird zuvor gesichert | ES-basierter Aufruf mit Selektor `04h`. |
| `13A8h` | `DS:[05B8h]`, DI=`0Ch` | AL aus `(BX)` geladen; anschließend weitere Strukturfelder gelesen | DS-basierter Aufruf mit Selektor `0Ch`. |

### 9.2 Gesicherte Schlüsse

1. `05B8h` ist ein wiederholt verwendeter indirekter Far-Aufrufoperand. Die Aufrufer wählen unterschiedliche DI-Werte (`04h`, `06h`, `08h`, `0Ah`, `0Ch`, `12h`, `16h`, `18h`) und reichen teils weitere Registerparameter weiter.
2. Sowohl `DS:[05B8h]` als auch `ES:[05B8h]` kommen vor. Das ist keine einheitliche absolute Adresse; die jeweilige Segmentbasis ist Teil des Aufrufvertrags.
3. Die Sicherung und Wiederherstellung von Flags an mehreren Stellen zeigt, dass der aufgerufene Code Statusflags als Rückgabekanal verwenden kann. Bei `129Bh` wird dies durch `sahf` explizit ausgewertet.
4. Das Löschen von `[05BAh]` bei `0F0Ah` betrifft nur das zweite Wort. Ob damit der Far-Zeiger deaktiviert wird, hängt von der konkreten Strukturkonvention ab und bleibt zunächst eine Hypothese.
5. Der Befund spricht für eine gemeinsame Callback-/Dispatch-Schnittstelle, beweist aber noch nicht, ob es sich um eine bestimmte Geräteklasse, einen Treibervertrag oder einen allgemeinen Kernel-Service handelt.

### 9.3 Offene Fragen und nächster Schritt

- Welche Routine initialisiert `05B8h`/`05BAh` in jedem Segmentkontext?
- Warum greifen manche Aufrufer über DS und andere über ES zu?
- Welche Bedeutung haben die DI-Selektoren und welche Register sind je Selektor Eingabe bzw. Ausgabe?
- Was liefert der Aufruf zurück (Carry, Zero, AL, andere Register)?

**Nächster Schritt 2249:** Die Aufrufpfade zu `0F06h`, `0F12h`, `0F2Eh`, `0F43h`, `0F6Dh`, `129Bh`, `1321h` und `13A8h` rückwärts verfolgen. Für jeden Pfad DS/ES vor dem Aufruf, DI, Registerparameter, Flag-Sicherung und unmittelbare Auswertung erfassen. Danach die Initialisierer der Zeigerworte `05B8h`/`05BAh` lokalisieren.

## 10. Untersuchung 2249 – Initialisierung und Speicherung des Far-Zeigers `05B8h/05BAh`

### 10.1 Vollständige direkte Schreibzugriffe im Disassembly

Die Suche nach direkten Speicher-Schreibbefehlen auf `05B8h` und `05BAh` ergibt im vorliegenden Kernel-Body:

| Offset | Befehl | Kontext / Wirkung |
|---|---|---|
| `0F0Ah` | `movw $0,05BAh` | setzt das Segmentwort des Zeigers auf null; DS wurde unmittelbar zuvor durch `9630h` vorbereitet und danach wiederhergestellt. |
| `FAD1h` | `mov CS,05BAh` | setzt das Segmentwort auf den aktuellen Code-Segmentwert. Im vorangehenden Block `FAC7h–FACBh` wird DS explizit auf `0E35h` gesetzt. |
| `10BB5h` | `mov AX,05B8h` | schreibt das Offsetwort. AX stammt aus dem bei `2588h` zurückgegebenen DS:SI-Objektkontext. |
| `10BB8h` | `mov BX,05BAh` | schreibt das zugehörige Segmentwort. BX stammt aus demselben zurückgegebenen Kontext. |

Im untersuchten vollständigen Disassembly wurde kein weiterer direkter Schreibzugriff auf `05B8h` gefunden. Die direkten Schreibzugriffe auf `05BAh` sind auf die drei oben genannten Stellen beschränkt.

### 10.2 Bedeutung des Wortpaares

Mehrere Instruktionen rufen `05B8h` mit `lcall` indirekt auf. Die Instruktion `lcall m16:16` liest dabei einen vier Byte langen Far-Zeiger aus dem durch DS bzw. ES bestimmten Speichersegment. Das unmittelbar benachbarte Wort bei `05BAh` ist somit das zweite Wort dieses Zeigers. Die Schreibfolge `AX -> 05B8h` und `BX -> 05BAh` bei `10BB5h–10BB8h` bestätigt diese Paarstruktur unmittelbar.

**Gesicherter Befund:** `05B8h/05BAh` bilden in dem jeweils adressierten Datensegment ein Offset-/Segment-Wortpaar für indirekte Far-Aufrufe. Welche konkrete Callback-Funktion dahinterliegt, hängt vom aktuellen Inhalt und von DS/ES des Aufrufers ab.

### 10.3 Initialisierungsvarianten

- `FAD1h`: setzt in DS=`0E35h` das Segmentwort `05BAh` auf CS. Das ist eine explizite Default-Segmentinitialisierung; das Offsetwort `05B8h` wird an dieser Stelle nicht geschrieben.
- `10BB5h–10BB8h`: überschreibt Offset und Segment mit den beiden Wörtern, die nach Aufruf `2588h` aus dem ausgewählten Objekt gelesen wurden.
- `0F06h–0F10h`: setzt das Segmentwort auf null. Das kann den Far-Zeiger deaktivieren bzw. als nicht verfügbar markieren; diese Wirkung ist plausibel, aber abhängig vom aufrufenden Segment und der weiteren Prüfung.

### 10.4 Konsequenz für die bisherigen Untersuchungen

1. Die Formulierung „gemeinsame Callback-/Dispatch-Schnittstelle“ aus Untersuchung 2248 ist nun stärker belegt: der gemeinsame Operand ist tatsächlich ein gespeicherter indirekter Far-Zeiger.
2. Die Segmentpräfixe sind wesentlich: `DS:[05B8h]` und `ES:[05B8h]` adressieren jeweils ein Wortpaar im aktuellen DS- bzw. ES-Segment. Die Datenadresse ist daher nicht global konstant.
3. Die genaue Callback-API ist noch nicht bestimmt. Die unterschiedlichen DI-Selektoren und Registerparameter müssen pro Aufrufer ausgewertet werden.
4. Die Default-Initialisierung bei `FAD1h` erklärt, warum `05BAh` zunächst auf CS gesetzt werden kann, während spätere Setup-Pfade das Zeigerpaar durch einen aus einem Objekt gelesenen Zeiger ersetzen.

**Nächster Schritt 2250:** Den Initialisierungspfad ab `FAC7h` und die Auswahl-/Ersetzungssequenz `10B53h–10BB8h` als zusammenhängenden Lebenszyklus modellieren. Anschließend für jeden DI-Selektor die konkreten Parameter und Rückgabeflags aus den Aufrufern tabellarisch rekonstruieren.

## 11. Untersuchung 2250 – DI-Selektoren und Rückgabekanäle der Callback-Aufrufe

**Methode:** Die direkten Aufrufstellen von `lcall DS:[05B8h]` und `lcall ES:[05B8h]` wurden jeweils mit den unmittelbar davor- und danachliegenden Instruktionen geprüft. Die Tabelle beschreibt nur Register und Flags, die aus dem lokalen Maschinencode sicher ablesbar sind; sie weist keine nicht belegten semantischen Namen zu.

### 11.1 Aufrufvertrag je Fundstelle

| Aufrufstelle | Segmentbasis | DI beim Aufruf | Vorher erkennbare Parameter | Direkt danach ausgewerteter Rückgabekanal |
|---|---|---:|---|---|
| `0E7Dh` | DS | `18h` | `CX=[01A0h]`, `DX=0`; zuvor `CB3h`, `9630h` | kein unmittelbarer Test; danach `CBAh` |
| `0F20h` | ES | `12h` | `9636h`, danach `172Fh` und `15EBh`; DI wird explizit gesetzt | danach `1628h`, `1736h`; kein unmittelbarer Carry-Test |
| `0F3Bh` | DS | `06h` | `BL=[BX]`, `BH=0`; Flags werden vor dem Callback gesichert | Flags werden unmittelbar danach mit `popf` wiederhergestellt; Ergebnisflags des Callbacks werden damit absichtlich verworfen |
| `0F4Eh` | DS | `08h` | DI wird auf `08h` gesetzt; `9630h` liefert BX-Kontext | Flags werden mit `pushf`/`popf` über den Callback hinweg bewahrt; Ergebnisflags werden nicht ausgewertet |
| `0F76h` | ES | `16h` | `9636h`; BX, DI und ES werden gesichert | Rückkehr ohne unmittelbaren Flag-Test; Register werden wiederhergestellt |
| `1189h` | DS | nicht lokal gesetzt | AL wird aus dem Byte bei DS:BX geladen; DI stammt aus dem Aufruferkontext | kein unmittelbarer Rückgabewerttest; DS wird wiederhergestellt |
| `129Bh` | DS | `0Ah` | AL=`[BX]`, CL=`[SI]` | unmittelbar `SAHF` aus AH; danach `JE`. Der Callback liefert hier erkennbar einen AH-Statuscode, dessen gesetzte Statusbits in FLAGS übertragen werden |
| `1321h` | ES | `04h` | AX wird vor dem Aufruf gesichert | unmittelbar `POP CX` (ändert FLAGS nicht), danach `JB`: Carry-Flag des Callback-Aufrufs wird ausgewertet; bei Carry Sprung, sonst Aufruf `11CBh` |
| `13A8h` | DS | `0Ch` | AL wird aus `[BX]` geladen; DS und weitere Register sind gesichert | AL wird direkt danach mit `FFh` überschrieben; später werden Strukturbytes bei BX+2/BX+3 ausgewertet. Kein direkter AL-Rückgabewertbeleg |
| `10BCFh` | DS | `14h` | BX wird aus `ES:[0040h]` geladen, das Byte `[BX]` wird nach BL übernommen | danach wird DI aus Stack restauriert und BL nach DS:DI geschrieben; Carry/AH werden hier nicht explizit ausgewertet |

### 11.2 Präzisierung der Rückgabeflags

Die Aufrufstellen zeigen unterschiedliche Konventionen und dürfen nicht zu einem einzigen Rückgabeprotokoll zusammengezogen werden:

- Bei `0F3Bh` und `0F4Eh` werden die Prozessorflags über den Callback mit `PUSHF`/`POPF` gesichert. Ein Ergebnis in CF oder anderen FLAGS-Bits wird an diesen Stellen bewusst nicht übernommen.
- Bei `129Bh` wird nach dem Callback `SAHF` ausgeführt. Damit werden Statusbits aus AH in FLAGS übertragen; danach prüft `JE` das Zero-Flag. Der unmittelbar sichtbare Rückgabekanal ist hier also AH, nicht einfach das durch den Far-Aufruf hinterlassene FLAGS-Register.
- Bei `1321h` wird nach dem Callback lediglich `POP CX` ausgeführt. `POP` verändert die Statusflags nicht; `JB` wertet deshalb das vom Callback hinterlassene Carry-Flag aus.
- Bei `10BCFh` wird das von der Callback-Funktion möglicherweise veränderte BL anschließend in eine Speicherstelle geschrieben. Das ist ein sichtbarer Datenrückkanal; eine allgemeine Bedeutung von BL ist noch nicht bekannt.
- Die übrigen Aufrufstellen belegen im unmittelbaren Nachlauf keinen spezifischen Rückgabekanal. Daraus folgt nicht, dass sie keine Rückgabe liefern, sondern nur, dass der lokale Code sie nicht direkt auswertet.

### 11.3 Wichtige Korrektur zur Schnittstellenhypothese

Die wiederholte Verwendung desselben Far-Zeigers und der DI-Werte belegt eine gemeinsame indirekte Aufrufstelle bzw. Dispatch-Mechanik. Sie beweist jedoch **keine einheitliche Callback-Signatur**. Segmentbasis, DI, Eingaberegister, Registererhaltung und Rückgabekanal variieren. Für eine belastbare API-Rekonstruktion muss jeder DI-Selektor separat behandelt werden.

### 11.4 Initialisierungsbefunde – engere Formulierung

- `FAD1h` schreibt CS nach `DS:[05BAh]`, nachdem DS in `FAC8h–FACBh` explizit auf `0E35h` gesetzt wurde. Das setzt nur das Segmentwort; ein dazugehöriger Schreibzugriff auf `05B8h` ist an dieser Stelle nicht vorhanden.
- `0F0Ah` schreibt null nach `DS:[05BAh]`, nachdem `9630h` den DS-Kontext vorbereitet hat; DS wird danach wiederhergestellt.
- `10BB5h–10BB8h` schreibt beide Wörter nach `DS:[05B8h]` und `DS:[05BAh]`. Das Datenpaar stammt aus dem Objektkontext, den der Aufruf `0000:2588h` in DS:SI zurückgibt.
- Die lineare Disassemblierung enthält keinen direkten Near-CALL auf `FAC7h` oder `FAD1h`. Deshalb ist `FAC7h` zwar ein sichtbarer Codeblock, aber der genaue externe Einstieg/Aufrufer ist mit dieser einfachen direkten Referenzsuche nicht bestimmt.

### 11.5 Ergebnis Untersuchung 2250

1. Der gemeinsame Operand `05B8h` ist ein Callback-/Dispatch-Zeiger, aber die Aufrufkonvention ist selektorabhängig.
2. DI-Werte `04h`, `06h`, `08h`, `0Ah`, `0Ch`, `12h`, `14h`, `16h`, `18h` sind belegt; `1189h` verwendet DI aus dem Aufruferkontext.
3. `129Bh` verwendet AH als Statuswort für `SAHF`/`JE`; `1321h` wertet CF direkt aus; `10BCFh` verwendet BL als Datenrückkanal.
4. Bei `0F3Bh` und `0F4Eh` werden FLAGS über den Aufruf hinweg wiederhergestellt; die Callback-Flags sind dort nicht das Ergebnis.
5. Die bisherige Sammelbezeichnung „gemeinsame Callback-Schnittstelle“ ist auf „gemeinsame Dispatch-Mechanik mit mehreren selektorspezifischen Verträgen“ zu präzisieren.

**Nächster Schritt 2251:** Die Aufrufstellen nach DI-Selektor gruppieren und ihre übergeordneten öffentlichen Wrapper bzw. Entry-Points bestimmen. Danach die Datenstrukturen hinter BX/SI und die Hilfsfunktionen `9630h`/`9636h` untersuchen, um die Bedeutung der übergebenen Objektkontexte zu identifizieren.


## 12. Untersuchung 2251 – Segmentladehelfer `9630h` und `9636h`

### 12.1 Überlappende Eintrittspunkte

Der lineare Disassembler zeigt bei `962Eh` zunächst Bytes `35 0E 2E` als Teil einer vermeintlichen `xor`-Instruktion. Die zahlreichen relativen CALL-Ziele `9630h` und `9636h` springen jedoch absichtlich in diese Bytefolge hinein:

- Ab `9630h` werden die Bytes `2E 8E 1E 2E 96 C3` als `mov DS, CS:[962Eh] ; ret` ausgeführt.
- Ab `9636h` werden die Bytes `2E 8E 06 2E 96 C3` als `mov ES, CS:[962Eh] ; ret` ausgeführt.
- Die zwei Bytes an `CS:962Eh` sind `35 0E`, also der Wortwert `0E35h` in Little-Endian-Reihenfolge.

**Befund:** `9630h` lädt `DS=0E35h`; `9636h` lädt `ES=0E35h`. Es handelt sich um zwei absichtlich überlappende Einstiegspunkte, nicht um normale unabhängige Funktionen im linearen Disassembly. Die Bytes `35 0E` sind zugleich Daten (Segmentkonstante) und werden bei linearer Disassemblierung fälschlich als Beginn einer arithmetischen Instruktion gelesen.

### 12.2 Auswirkungen auf die bisherigen Callback-Aufrufstellen

- Bei Aufrufstellen, die unmittelbar zuvor `9630h` ausführen und DS danach nicht ändern, ist `DS=0E35h` vor dem Callback konkret belegt. Das betrifft u. a. `0E7Dh`, `0F3Bh`, `0F4Eh`, `1189h`, `129Bh` und `13A8h`.
- Bei Aufrufstellen, die unmittelbar zuvor `9636h` ausführen und ES danach nicht ändern, ist `ES=0E35h` belegt. Das betrifft `0F20h`, `0F76h` und `1321h`.
- Die Callback-Aufrufe verwenden somit in diesen Pfaden nicht irgendeinen beliebigen aktuellen Segmentwert, sondern gezielt den Segmentwert `0E35h` aus `CS:[962Eh]`.
- Der Block `10B53h–10BD6h` setzt DS zunächst aus BX (`10B53h`), führt später `DS=CS` aus (`10B94h–10B95h`) und ruft `101CBh` auf. Diese Setup-Routine setzt am Ende DS erneut auf `0E35h`. Der anschließende Zugriff `DS:[05B8h]` liegt daher ebenfalls im Segment `0E35h`.

### 12.3 Präzisierung der Zeigerinitialisierung

Die zuvor dokumentierte Schreibstelle `FAD1h` setzt in DS=`0E35h` das Wort `DS:[05BAh]` auf den aktuellen CS-Wert. Damit ist die Initialisierung des Segmentwortes im zentralen Segment `0E35h` bestätigt. `0F0Ah` löscht ebenfalls `DS:[05BAh]`, wobei `9630h` DS ausdrücklich auf `0E35h` setzt. Die Schreibsequenz `10BB5h–10BB8h` erfolgt nach `101CBh`, das DS auf `0E35h` setzt; sie überschreibt beide Wörter im selben zentralen Segment.

**Wichtige Korrektur:** Die frühere Formulierung, die Segmentbasis der Callback-Aufrufe sei jeweils allgemein vom gerade aktuellen DS/ES abhängig, war zu weit gefasst. Die Instruktion nutzt technisch DS bzw. ES, aber die untersuchten Wrapper laden diese Register unmittelbar davor gezielt mit `0E35h`. In diesen Fällen ist die konkrete Zeigeradresse `0E35h:05B8h`.

### 12.4 Konsequenz

Der Callback-/Dispatch-Zeiger ist für die untersuchten Kernelpfade zentral im Segment `0E35h` gespeichert. Der indirekte Aufruf über ES ist kein Hinweis auf einen zweiten, eigenständigen Callback-Speicherbereich, wenn ES zuvor durch `9636h` geladen wurde; er adressiert dann denselben Zeiger `0E35h:05B8h`.

**Nächster Schritt 2252:** Die Datensegmentkonstante `0E35h` und den Inhalt des Segmentes rund um `05A0h–0620h` anhand der Kernel-Initialisierung und aller Schreibzugriffe strukturieren. Insbesondere die benachbarten Werte `05ABh`, `05B1h`, `05B2h`, `05B4h`, `05B6h`, `05B8h`, `05BAh`, `05AEh` und `0609h` auf ihre Beziehungen untersuchen.


## 13. Untersuchung 2252 – Datenstrukturen im Segment `0E35h`

**Grundlage:** Quellidentität des Kernels unverändert; Analyse der absoluten Datenzugriffe im Disassembly. Die Segmentladehelfer aus Untersuchung 2251 belegen für die betreffenden Kernelpfade `DS=0E35h` bzw. `ES=0E35h`. Die Datei `KERNEL.OLD` enthält jedoch nicht den zur Laufzeit vollständig initialisierten Inhalt dieses Datensegments. Deshalb werden hier Strukturbeziehungen aus den Instruktionen abgeleitet, nicht vermeintliche Anfangswerte aus gleichnamigen Offsets im Kernel-Code-Image.

### 13.1 Verkettete Liste mit Kopfzeiger `05B2h`

Die Routine `11CBh` erzeugt einen Listenknoten:

1. `9630h` lädt DS auf `0E35h`.
2. Über `6DACh` wird Speicher angefordert; BX zeigt anschließend auf den neuen Knoten.
3. Der Code schreibt mehrere Felder relativ zu BX, u. a. Byte bei `BX+0`, Statusbyte bei `BX+1`, Bytes bei `BX+2`/`BX+3`, Wortfelder bei `BX+6`, `BX+0Ch` und `BX+0Eh`.
4. Bei `11F5h` wird der bisherige Kopf `[05B2h]` nach SI geladen und bei `[BX+4]` als Nachfolger gespeichert.
5. Bei `11FCh` wird BX als neuer Kopf nach `[05B2h]` geschrieben.

**Gesicherter Befund:** `0E35h:05B2h` ist der Kopfzeiger einer verketteten Liste; der Link des Knotens liegt bei Offset `+4`. Der genaue semantische Typ der Knoten ist noch offen.

### 13.2 Sentinel-/Ankerstruktur bei `05AEh`

Die Routine `1228h` setzt SI auf `05AEh` und untersucht wiederholt das Wort `[SI+4]`, bis es dem gesuchten BX entspricht. Danach kopiert sie den Nachfolger `[BX+4]` in `[SI+4]`. Da `05AEh+4=05B2h`, ist dies die passende Entfernung eines Knotens aus der Liste mit Kopfzeiger `05B2h`.

**Gesicherter Befund:** `0E35h:05AEh` ist ein Listenanker bzw. Sentinel; sein Linkfeld bei `+4` ist zugleich die globale Kopfzeigerzelle `05B2h`. `05B2h` ist damit nicht nur irgendein einzelner Pointer, sondern das Linkfeld des Ankerknotens.

### 13.3 Statusbyte `05ABh` und Initialisierungsflag `05B1h`

- `05ABh` wird in `10B5Fh` als Byte in BL geladen und in `110Eh` mit `03h` verglichen. Die genaue Codierung ist nicht geklärt.
- `05B1h` wird bei `10B13h` auf `FFh` gesetzt. `10B58h` prüft, ob es null ist; bei ungleich null wird ein alternativer Pfad nach `10B90h` genommen.
- Der Initialisierungs-/Auswahlblock verwendet `05B1h` daher als Zustandsschalter; eine präzisere Bedeutung (z. B. „nicht initialisiert“, „Treiber aktiv“ o. ä.) ist aus diesen Zugriffen allein nicht belegbar.

### 13.4 Separates Far-Zeigerpaar `05B4h/05B6h`

Die Routine `1849h` lädt nach `DS=0E35h`:
- `[05B6h]` in AX und speichert es als Segmentwort nach `SS:[0010h]`;
- `[05B4h]` in AX und speichert es als Offsetwort nach `SS:[000Eh]`.

Danach führt sie mit Interruptsperre `lcall SS:[000Eh]` aus und prüft anschließend den Wert bei `SS:[0010h]`. Das belegt ein zweites Offset-/Segment-Paar, getrennt von `05B8h/05BAh`. In der untersuchten Kerneldatei sind keine direkten Schreibzugriffe auf `05B4h` oder `05B6h` sichtbar; die Initialisierung kann daher außerhalb dieses Kernel-Codepfades erfolgen.

**Wichtig:** `05B4h/05B6h` darf nicht mit dem Callback-Paar `05B8h/05BAh` gleichgesetzt werden. Beide sind getrennte Wortpaare mit unterschiedlichen Aufrufpfaden.

### 13.5 `0609h` – gespeicherter Index

`10BA5h` speichert BX nach `0609h`. Die Routine `25A5h` liest diesen Wert später nach DX. In `10B89h` wird BX unmittelbar zuvor verdoppelt und als Index in `CS:[121Ah+BX]` verwendet. Der gespeicherte Wert ist damit der ausgewählte, bereits skalierte Tabellenindex. Eine höhere semantische Bedeutung ist noch nicht nachgewiesen.

### 13.6 Ergebnis Untersuchung 2252

1. `05B2h` ist der Kopf-Link einer verketteten Liste; `05AEh` ist ihr Sentinel/Anker.
2. Das Linkfeld jedes Knotens liegt bei `+4`; Einfügen und Entfernen sind im Code sichtbar.
3. `05ABh` ist ein Zustandsbyte mit mindestens zwei beobachteten Verwendungsweisen; genaue Codierung offen.
4. `05B1h` ist ein Schalter, der im untersuchten Initialisierungspfad zwischen zwei Kontrollflusswegen unterscheidet.
5. `05B4h/05B6h` bilden ein separates Far-Zeigerpaar, das `1849h` über einen Stack-basierten Aufruf verwendet.
6. `0609h` speichert den skalierten Tabellenindex des Blocks `10B53h–10BD6h`.

**Nächster Schritt 2253:** Den Knotenaufbau ab `11CBh` vollständig als Byte-Layout darstellen und die Verbraucher der Felder `+0`, `+1`, `+2`, `+3`, `+4`, `+6`, `+0Ch`, `+0Eh` verfolgen. Parallel die Herkunft der extern initialisierten Far-Zeiger `05B4h/05B6h` und `05B8h/05BAh` weiter eingrenzen.


## 14. Untersuchung 2253 – Knotenlayout der Liste ab `05AEh`

**Quelle:** reproduzierte Disassemblierung des unveränderten Load-Moduls aus `GEOWORKS/KERNEL.OLD`. Untersuchte Bereiche: `06DACh–06DE8h`, `0072Bh–00788h`, `011CBh–01246h`, Aufrufer `01329h` und `013BFh`, Verbraucher u. a. `00795h–007A3h`, `011A4h–011B8h`, `013A3h–01401h` und `01445h–01455h`.

### 14.1 Speicherbeschaffung und Feld `+08h`

`11CBh` lädt vor dem Aufruf von `6DACh` den Wert `SS:[0002h]` nach BX. Die Routine `6DACh` nimmt den bisherigen Freilistenkopf aus `0E48h`, entnimmt daraus einen Block und initialisiert dessen Wortfelder. Besonders wichtig ist die Instruktion `6DD4h: pop [BX+8]`: Der zuvor gesicherte ursprüngliche BX-Wert wird in das neue Blockfeld `+08h` geschrieben. Da BX unmittelbar vor dem Aufruf aus `SS:[0002h]` geladen wurde, enthält der neue Knoten an `+08h` den Wert von `SS:[0002h]`.

**Gesichert:** `+08h` ist bei dieser Erzeugung nicht uninitialisiert; es enthält den übernommenen Wert `SS:[0002h]`. Die genaue Bedeutung dieses globalen SS-Feldes ist noch offen. Es wird auch von weiteren Kernelroutinen als Kontextwert verwendet.

### 14.2 Byte-/Wortlayout des von `11CBh` angelegten Knotens

| Offset | Breite | Initialisierung / Beleg |
|---|---:|---|
| `+00h` | Byte | Caller-CL; wird nach Wiederherstellung von CX bei `11F3h` geschrieben. |
| `+01h` | Byte | Konstante `FDh` bei `11E9h`; mehrere Verbraucher prüfen genau diesen Marker. |
| `+02h` | Wort | Low-Byte = ursprüngliches CL bei `11DBh`; High-Byte wird zunächst durch `11E0h` auf null gesetzt und bei nichtnegativem AL durch `11E9h`/genauer `1204h` mit AL belegt. |
| `+04h` | Wort | Nächster Listenknoten; alter Kopf aus `05B2h` wird bei `11F9h` eingetragen. |
| `+06h` | Wort | Zunächst null; wenn AL nicht negativ ist, wird der von Hilfsroutine `72Bh` in BX gelieferte Wert hier bei `120Dh` gespeichert. |
| `+08h` | Wort | Wert aus `SS:[0002h]`, durch `6DACh` bei `6DD4h` übernommen. |
| `+0Ah` | Wort | Durch den Blockallocator `6DACh` zunächst auf null gesetzt; `11CBh` selbst ändert es nicht. |
| `+0Ch` | Wort | Zunächst null; wenn CH ungleich null ist, wird bei `121Dh` ein beim Durchlaufen der Liste gefundener Knoten-Zeiger gespeichert. |
| `+0Eh` | Wort | Konstante `0001h` bei `11EDh`; spätere Verwendungsweise ist noch nicht abschließend geklärt. |

**Präzisierung:** Die Bytes `+02h` und `+03h` bilden gemeinsam ein Wort. Die Instruktionen beschreiben sie zunächst getrennt; deshalb darf `+03h` nicht als unabhängiges 16-Bit-Feld behandelt werden.

### 14.3 Bedeutung des Markers `+01h = FDh`

Der Marker wird unter anderem an folgenden Stellen geprüft:

- `11A8h`: nur bei Marker `FDh` wird das Byte `+02h` geladen und mit `03h` maskiert.
- `0798h`: prüft denselben Marker; bei Treffer wird das Wort `+06h` nach BX geladen und auf null geprüft.
- `13AEh–13B8h`: prüft `+06h`; abhängig davon wird AL aus `+03h` oder auf `FFh` gesetzt, danach wird CL aus `+02h` gelesen.

**Gesichert:** `FDh` kennzeichnet diesen Knotentyp in mehreren Kernelpfaden. Die konkrete symbolische Bezeichnung des Typs ist im Disassembly nicht enthalten.

### 14.4 Die zwei direkten Aufrufer von `11CBh`

Die Disassemblierung enthält zwei direkte Near-Aufrufe:

**Aufrufer `1329h`:**
- Vorher erfolgt ein indirekter Aufruf über `ES:[05B8h]` mit `DI=04h`.
- Das zurückgegebene AX wird über `push AX / pop CX` nach CX übertragen.
- Bei nicht gesetztem Carry wird `11CBh` aufgerufen.
- Damit stammen CL und CH in diesem Pfad aus AL und AH des vorherigen Aufrufs. CH kann folglich die optionale Suche über `+0Ch` auslösen.

**Aufrufer `13BFh`:**
- Zuvor erfolgt ein indirekter Aufruf über `DS:[05B8h]` mit `DI=0Ch`.
- Danach werden Werte aus dem vorhandenen Knoten gelesen: `+06h` wird geprüft, AL wird aus `+03h` oder als `FFh` gesetzt, CL wird aus `+02h` geladen.
- CH wird in diesem lokalen Block nicht neu gesetzt; sein Wert stammt aus dem umgebenden Aufrufkontext. Daher ist die CH-abhängige Suche bei diesem Aufrufer nicht als immer aktiv zu behaupten.

### 14.5 Ergebnis und offene Punkte

1. Das Layout umfasst mindestens die belegten Offsets `+00h` bis `+0Eh`; die Erzeugungsroutine und der Blockallocator liefern dafür konkrete Schreibbelege.
2. `+04h` ist der Listenlink; `+01h=FDh` ist ein wiederholt geprüfter Knotentyp-Marker.
3. `+08h` enthält nachweislich den Wert aus `SS:[0002h]`.
4. `+02h/+03h` sind gemeinsam ein Wort, dessen High-Byte abhängig vom Vorzeichen von AL gesetzt wird.
5. `+06h` erhält bei nichtnegativem AL einen Rückgabewert der Hilfsroutine `72Bh`; deren höhere fachliche Bedeutung ist noch offen.
6. `+0Ch` kann einen Zeiger auf einen anhand CH gefundenen Knoten enthalten; spätere Routinen ändern dieses Feld ebenfalls.
7. `+0Eh` wird mit eins initialisiert und später als Wort gelesen bzw. weitergereicht. Eine eindeutige Bezeichnung als Referenzzähler wäre auf Basis der bisher untersuchten Pfade verfrüht.
8. Die genaue Bedeutung der Knoten (z. B. konkrete Objekt-/Geräteklasse) ist weiterhin nicht bewiesen.

**Nächster Schritt 2254:** Die Hilfsroutine `72Bh` und die Verbraucher der Felder `+06h`, `+0Ch` und `+0Eh` gezielt auf dieselbe Knotentypfamilie zurückverfolgen. Dabei besonders prüfen, welche Daten `CC5h` und `E37h` liefern und ob sich daraus ein belastbarer Typname ableiten lässt.


## 15. Untersuchung 2254 – Herkunft des Feldes `+06h` und Index-Tabelle

**Quelle:** reproduzierte Disassemblierung des unveränderten `KERNEL.OLD`; Kontrollfluss ab `072Bh`, `0CC5h`, `0E37h`, `0EBBh` und die Tabellenzugriffe in `072Bh–0788h`. Diese Untersuchung beschreibt nur die im Kernel-Code belegten Abläufe; der zur Laufzeit aufgebaute Inhalt des Datensegmentes `0E35h` liegt nicht als fertige Datensegment-Abbildung in `KERNEL.OLD` vor.

### 15.1 Indexberechnung in `0EBBh`

`0EBBh` verwendet AL als Index:
1. AL wird nach BL übertragen; BH wird auf null gesetzt.
2. Die Schiebe-/Addierfolge berechnet aus dem Index den 26-fachen Byteabstand.
3. `9630h` lädt DS auf `0E35h`.
4. BX wird um `021Ch` erhöht.

Damit lautet die berechnete Datensatzadresse:

`DS:BX = 0E35h:(021Ch + AL * 1Ah)`

**Gesichert:** Die von `0EBBh` adressierte Tabelle beginnt bei `0E35h:021Ch`; der Abstand zwischen zwei Indexeinträgen beträgt `1Ah` = 26 Bytes. Das ist eine aus den Maschineninstruktionen abgeleitete Datensatzgröße, keine Schätzung.

### 15.2 Gültigkeitsprüfung durch `0CC5h`

- AL muss kleiner als `1Ah` sein; sonst setzt die Routine Carry.
- Für einen zulässigen Index wird die Tabellenbasis über `0EBBh` berechnet.
- Das erste Byte des Datensatzes wird nach AH geladen.
- Bit `80h` dieses Bytes wird geprüft; ist es nicht gesetzt, wird Carry gesetzt.

Die Routine liefert damit einen Statusbytewert in AH und einen Carry-Status. Eine symbolische Bedeutung der Bits ist im Kernel nicht hinterlegt.

### 15.3 Zusätzliche Prüfung in `0E37h`

`0E37h` berechnet denselben Datensatzanfang, addiert `0Eh` zum Datensatzoffset und prüft anschließend das Wort `0FB8h` im Datensegment. Ist dieses Wort ungleich null, springt der Code in den Kernelpfad `971Dh`; andernfalls kehrt er zurück. Die Routine stellt DS vorübergehend auf `0E35h` und stellt das ursprüngliche DS anschließend wieder her.

**Gesichert:** `0E37h` ist eine zusätzliche globale Zustandsprüfung im Zusammenhang mit dem indizierten Datensatz. Welche fachliche Bedeutung `0FB8h` besitzt, bleibt offen.

### 15.4 Verhalten der Hilfsroutine `072Bh`

Der Ablauf lässt sich statisch wie folgt rekonstruieren:

1. `CC5h` prüft AL und liefert das Statusbyte in AH. Bei gesetztem Carry endet `72Bh` ohne den normalen Cachepfad.
2. `E37h` führt die zusätzliche Zustandsprüfung aus.
3. Der Index AL wird verdoppelt und als Wortindex für zwei Tabellenbereiche verwendet:
   - Zeigerfeld ab `0E35h:01DFh)
   - Zeit-/Markierungsfeld ab `0E35h:01ABh)
4. Wenn Bit `40h` in AH nicht gesetzt ist, wird der gespeicherte Zeiger aus `[01DFh + 2*Index]` gelesen. Ist er ungleich null, wird er als Rückgabewert in BX verwendet.
5. Wenn Bit `40h` gesetzt ist, wird `[105Ah]` mit dem gespeicherten Wert aus `[01ABh + 2*Index]` verglichen. Liegt die Differenz unter `5Ah` (= 90), wird ebenfalls der vorhandene Zeigerpfad benutzt.
6. Andernfalls folgen weitere Kernelaufrufe zur Beschaffung bzw. Erneuerung des Eintrags. Bei erfolgreichem Pfad wird BX in `[01DFh + 2*Index]` gespeichert und der aktuelle Wert aus `[105Ah]` in `[01ABh + 2*Index]` abgelegt.
7. Vor der Rückkehr wird `E51h` aufgerufen; die Routine stellt danach CX wieder her.

**Gesichert:** `72Bh` liefert im erfolgreichen Pfad einen BX-Zeiger, der indexabhängig aus dem Bereich `01DFh` gelesen oder nach einem Erneuerungspfad dort gespeichert wird. Der Bereich `01ABh` enthält den zugehörigen Vergleichswert. Der Schwellwert beträgt exakt `5Ah` Einheiten des Wertes `[105Ah]`; ob diese Einheiten Systemticks, Zeitstempel oder etwas anderes sind, ist anhand dieses Ausschnitts allein nicht bewiesen.

### 15.5 Konsequenz für Knotenfeld `+06h`

Die Routine `11CBh` speichert den von `72Bh` zurückgegebenen BX-Wert in `+06h), sofern AL nicht negativ ist. Die Verbraucher bestätigen, dass dieses Feld als Zeiger-/Gültigkeitswert behandelt wird:

- `0795h–07A3h`: nach Prüfung des Markers `FDh` wird `+06h` nach BX geladen und auf null geprüft.
- `13AEh–13B8h`: `+06h` wird geprüft; abhängig davon wird AL aus `+03h` oder als `FFh` gesetzt.
- `13FBh–1401h`: das Wort `+06h` wird beim Kopieren eines Knotens in einen anderen Datensatz übernommen.

**Gesicherter Zusammenhang:** `+06h` enthält in diesem Knotentyp einen indexabhängig beschafften oder zwischengespeicherten Zeiger. Eine präzise Objektbezeichnung (z. B. Datei, Gerät, Treiber oder Ressourcenobjekt) ist noch nicht belegt.

### 15.6 Ergebnis Untersuchung 2254

1. Die Index-Tabelle bei `0E35h:021Ch` besitzt Datensätze im Abstand von 26 Bytes.
2. AL ist der Tabellenindex; `CC5h` begrenzt ihn auf Werte kleiner `1Ah` und prüft Bit `80h` des ersten Datensatzbytes.
3. `72Bh` verwendet zwei indexbezogene Worttabellen bei `01DFh` und `01ABh`.
4. Der Erneuerungspfad wird bei gesetztem Statusbit `40h` und einer Differenz von mindestens `5Ah` durchlaufen.
5. Der erfolgreiche Rückgabewert in BX wird vom Knotenaufbau `11CBh` im Feld `+06h` gespeichert.
6. Die fachliche Bedeutung der Datensatztypen und die Einheit von `[105Ah]` bleiben offen.

**Nächster Schritt 2255:** Die Rückgabepfade und Datenzugriffe der Hilfsroutinen `0BD0h`, `0C97h`, `0CAC h`, `0A20h` und `0A3C h` im Zusammenhang mit `72Bh` verfolgen. Ziel ist, den erzeugten bzw. wiederverwendeten Zeiger genauer zu klassifizieren, ohne aus den Offsets allein einen Objektnamen zu erfinden.


## 16. Untersuchung 2255 – Verifikation der Routine `0B20h` und des 11-Byte-Kopierens

**Ausgangsfrage:** Die Arbeitsnotiz 2245 nannte `0B20h` als Routine und `0B6Fh–0B75h` als Kopierstelle mit elf Bytes. Die frühere Prüfung des davon verschiedenen Bereichs `10B20h` hatte diese Notiz fälschlich mit dem Code bei `10B53h` vermischt. Diese Untersuchung trennt die beiden Offsetbereiche und verifiziert den ursprünglichen Befund.

### 16.1 Aufrufkette und Blockgröße

Bei `0A20h` beginnt eine Far-Routine:
- `0A25h`: BX wird auf `0010h` gesetzt.
- `0A28h`: Aufruf von `6DACh`, dem Kernel-Blockallocator.
- `0A2Bh`: Near-Aufruf von `0B20h`.
- Bei Carry wird der angeforderte Block über `6E2Fh` freigegeben, BX auf null gesetzt und Carry gesetzt.
- Die Routine stellt ihre gesicherten Register wieder her und kehrt mit Far Return zurück.

Der einzige direkte Aufruf von `0B20h` im untersuchten Kernel-Disassembly liegt bei `0A2Bh`.

### 16.2 Initialisierung bei `0B20h`

Die Routine beginnt mit `call 29DCh` und schreibt anschließend `F5h` nach `[BX+1]`. Der Kontrollfluss hängt danach unter anderem davon ab, ob CX null ist:

- Bei CX ungleich null wird ein Statusbyte aus `[01A6h]` gebildet, mit dem unteren Nibble maskiert und abhängig von CL-Bit `10h` um Bit `80h` ergänzt. Dieses Byte wird bei `0B38h` nach `[BX]` geschrieben.
- `CC5h` prüft den durch AL bezeichneten Index; abhängig von Bit `40h` des zurückgegebenen Statusbytes wird Bit `40h` im Blockstatus gesetzt.
- Danach folgen weitere Prüfungen über `0B0Eh`, gegebenenfalls `0A8Eh` und `0AB4h`.
- Bei CX gleich null wird zunächst `0BD0h` aufgerufen. Bei gesetztem Carry endet der Initialisierungspfad mit Fehler; andernfalls wird der Statusaufbau erneut durchlaufen.

Die genaue fachliche Bedeutung des Markers `F5h` und der Statusbits ist noch nicht belegt.

### 16.3 Exakter 11-Byte-Kopiervorgang

Die entscheidende Instruktionsfolge lautet:

| Offset | Instruktion | Wirkung |
|---|---|---|
| `0B66h` | `push cx` | CX sichern |
| `0B67h` | `mov [bx+2],di` | DI als Wort bei `+2` speichern |
| `0B6Ah` | `mov [bx+4],dl` | DL bei `+4` speichern |
| `0B6Dh–0B6Eh` | `push ds / pop es` | ES = DS |
| `0B6Fh` | `lea di,[bx+5]` | Zieladresse = Blockanfang + 5 |
| `0B72h` | `mov cx,000Bh` | Kopieranzahl = 11 Bytes |
| `0B75h` | `rep movsb` | elf Bytes von DS:SI nach ES:DI kopieren |
| `0B77h` | `pop cx` | ursprüngliches CX wiederherstellen |

Damit werden genau die elf Bytes `DS:SI` bis `DS:SI+0Ah` nach `ES:(BX+5)` bis `ES:(BX+0Fh)` kopiert. Zusammen mit den vorherigen Feldern belegt die Routine damit den 16-Byte-Block von Offset `+0` bis `+0Fh`.

### 16.4 Rückgabe und Einordnung

- Nach dem Kopieren wird CL-Bit `20h` geprüft; bei gesetztem Bit folgt ein Aufruf von `1752h`.
- Danach folgt `0CAC h` und schließlich `ret` bei `0B86h`.
- Die aufrufende Routine `0A20h` übernimmt den Carry-Status und gibt den Block bei Fehler wieder frei.

**Gesicherter Befund:** `0B20h` ist eine echte Routine; sie initialisiert einen 16-Byte-Block und kopiert exakt elf Bytes an dessen Offset `+5`. Die ursprüngliche Notiz 2245 war in diesem Punkt richtig.

**Abgrenzung:** Der Bereich `10B1Ah–10BD6h` bleibt davon unabhängig. Die dortige Daten-/Codegrenze und der indirekte Aufruf bei `10BCFh` werden durch diese Korrektur nicht verändert.

### 16.5 Ergebnis Untersuchung 2255

1. Der 11-Byte-Kopiervorgang bei `0B6Fh–0B75h` ist bestätigt.
2. Zieladresse ist `BX+5`; Quelladresse ist DS:SI; die Kopieranzahl ist `000Bh`.
3. Der umgebende Allocatorpfad fordert zuvor einen 16-Byte-Block an.
4. `0B20h` wird direkt von `0A2Bh` aufgerufen und kehrt mit Carry-Status zurück.
5. Die getrennten Adressbereiche `0B20h` und `10B20h` dürfen nicht vermischt werden.

**Nächster Schritt 2256:** Den Pfad `0BD0h` im CX=0-Zweig von `0B20h` und im Erneuerungspfad von `72Bh` vergleichen. Dabei die Bedeutung der Statusbits `20h` und `40h`, die Rückgaberegister und die Übergabe an `0A3Ch` untersuchen.


## 17. Untersuchung 2256 – Status- und Konfigurationspfad `0BD0h`

**Ziel:** Den in Untersuchung 2255 ermittelten CX=0-Zweig von `0B20h` sowie den Aufruf von `0BD0h` aus der Cache-/Erneuerungsroutine `72Bh` vergleichen. Die Untersuchung bleibt bei belegten Register- und Speicheroperationen; die symbolische Bedeutung der Statusbits ist nicht aus den Offsets allein ableitbar.

### 17.1 Eingang und Statusentscheidung

`0BD0h` sichert AX, ES und DS und ruft `0CC5h` auf. `CC5h` interpretiert AL als Index in der Tabelle ab `0E35h:021Ch`, liefert das erste Datensatzbyte in AH und setzt Carry, wenn der Index ungültig ist oder Bit `80h` des Statusbytes fehlt.

Anschließend prüft `0BD0h` Bit `20h` in AH:

- **Bit `20h` gesetzt:** Es folgt `0CA5h`; CX wird auf 3, DX und DI auf null gesetzt. Das untere Nibble von AH wird geprüft. Bei Wert 4 wird CX auf 2 reduziert. Der Kontrollfluss springt anschließend in die gemeinsame Ergebnisaufbereitung ab `0C49h).
- **Bit `20h` nicht gesetzt:** CX wird null gesetzt und `0A3Ch` aufgerufen. Bei Erfolg wird CL-Bit `10h` gesetzt. Bei Fehler wird erneut `CC5h` aufgerufen und Bit `40h` von AH ausgewertet; abhängig davon wird die Schleife wiederholt oder mit Carry beendet.

**Gesichert:** Bit `20h` entscheidet zwischen einem direkten Statuspfad und einem Pfad, der zusätzliche Daten über `0A3Ch` einliest. Die genaue fachliche Bezeichnung dieses Bits bleibt offen.

### 17.2 Datenquelle von `0A3Ch`

Die Routine `0A3Ch`:
1. ruft `0CA5h` auf;
2. übernimmt DS nach ES;
3. lädt mit `LDS SI,[0192h]` einen Far-Zeiger aus dem Kernel-Datensegment;
4. ruft `06C6h` mit CS als zusätzlichem Segmentkontext auf;
5. liest bei erfolgreichem Rücklauf Daten relativ zu SI:
   - Byte `[SI+15h]` nach `[01A6h]`,
   - Wort `[SI+18h]` nach `[01A7h]`,
   - Wort `[SI+1Ah]` nach `[01A9h]`;
6. verlässt den geschützten Pfad über `0CAC h` und stellt ES/AX wieder her.

**Gesichert:** `0A3Ch` liest drei Felder aus einer über `[0192h]` referenzierten Struktur und übernimmt sie in globale Kernel-Datenfelder. Die Feldbedeutungen sind noch nicht bestimmt.

### 17.3 Gemeinsame Ergebnisaufbereitung

Im Pfad ab `0C1Bh` werden abhängig vom SI-Datensatz entweder Werte aus `[SI+03h]` und `[SI+05h]` übernommen oder – bei einem Marker `29h` an `[SI+26h]` – Werte aus `[SI+27h]` und `[SI+29h]`. Wenn `[SI+07h]` nicht `FFh` ist, wird zuvor `57Ah` aufgerufen; anschließend werden die beiden Werte aktualisiert und `[SI+07h]` auf `FFh` gesetzt.

Danach:
- CL erhält Bit `02h`;
- DX wird auf seine unteren zwei Bits maskiert;
- `0A6Ah` wird mit den aktuellen Registern aufgerufen;
- bei Erfolg werden weitere Statusbits in CL und DL gesetzt;
- AL wird dreimal nach links geschoben und mit DL verknüpft.

Bei einem Fehlerpfad wird abhängig von CL-Bit `10h` entweder direkt zurückgekehrt oder `0B87h` als zusätzlicher Prüfschritt aufgerufen.

**Gesichert:** Die Routine bildet aus Statusbyte, Tabellen-/Strukturfeldern und Rückgaben weiterer Kernelhelfer einen kombinierten Ergebniszustand in AL, CL und DL. Ohne Kenntnis der referenzierten Laufzeitdaten ist eine weitergehende semantische Benennung nicht belastbar.

### 17.4 Wrapper `0C97h`, `0C9Eh`, `0CA5h), `0CAC h`, `0CB3h`, `0CBAh`

Diese kurzen Routinen sichern BX, laden jeweils eine Konstante in BX und springen in gemeinsame Kernelpfade:

| Wrapper | BX-Konstante | Ziel |
|---|---:|---:|
| `0C97h` | `0186h` | `971Dh` |
| `0C9Eh` | `0186h` | `9754h` |
| `0CA5h` | `018Eh` | `9776h` |
| `0CAC h` | `018Eh` | `978Ch` |
| `0CB3h` | `0196h` | `971Dh` |
| `0CBAh` | `0196h` | `9754h` |

Die Konstanten und Sprungziele sind unmittelbar im Code belegt. Ob die Paare jeweils Eintritt/Austritt, Sperre/Freigabe oder andere Kerneloperationen darstellen, ist ohne Analyse der gemeinsamen Ziele `971Dh`, `9754h`, `9776h` und `978Ch` noch nicht abschließend geklärt.

### 17.5 Verbindung zum 11-Byte-Datensatz

Die Routine `0B20h` ruft `0BD0h` nur im Zweig auf, in dem CX bei Eintritt in `0B20h` null ist. Bei erfolgreichem Rücklauf springt sie zurück in den Statusaufbau ab `0B29h`; bei gesetztem Carry wird der Fehlerpfad bei `0B83h` erreicht. Der andere Aufruf aus `72Bh` liegt im Erneuerungspfad eines indexbezogenen Zeigereintrags.

**Gesichert:** `0BD0h` ist eine gemeinsam genutzte Status-/Konfigurationsroutine in zwei verschiedenen Kontrollflusskontexten. Ihre Ergebnisse beeinflussen sowohl die Anlage des 16-Byte-Blocks durch `0B20h` als auch die Erneuerung des indexbezogenen Zeigers aus `72Bh`.

### 17.6 Ergebnis Untersuchung 2256

1. `0BD0h` beginnt mit einer Index-/Statusprüfung über `0CC5h`.
2. AH-Bit `20h` entscheidet zwischen einem direkten Pfad und dem zusätzlichen Datenzugriff über `0A3Ch`.
3. `0A3Ch` liest aus der durch `[0192h]` referenzierten Struktur Byte `+15h`, Wort `+18h` und Wort `+1Ah).
4. Die Routine kombiniert anschließend Status- und Strukturwerte in AL, CL und DL.
5. `0B20h` nutzt `0BD0h` als Vorprüfung, bevor es den 16-Byte-Block weiter aufbaut.
6. Die symbolischen Bedeutungen der Statusbits und der externen Strukturfelder bleiben offen.

**Nächster Schritt 2257:** Die gemeinsamen Zielroutinen `971Dh`, `9754h`, `9776h` und `978Ch` untersuchen. Damit soll geklärt werden, welche Kerneloperationen die Wrapper-Konstanten `0186h`, `018Eh` und `0196h` tatsächlich auswählen.


## 18. Untersuchung 2257 – Synchronisationswrapper und Semaphorepfade

**Ziel:** Die gemeinsamen Ziele der Wrapper `0C97h`, `0C9Eh`, `0CA5h`, `0CAC h`, `0CB3h` und `0CBAh` untersuchen. Grundlage sind die Instruktionen `971Dh`, `9754h`, `9776h`, `978Ch` sowie die von ihnen aufgerufenen Kernelroutinen `9C8Bh` und `9C19h`.

### 18.1 Einfaches atomisches Zählerpaar `9776h/978Ch`

`9776h`:
- lädt DS auf `0E35h`;
- führt `LOCK DEC WORD PTR [BX]` aus;
- kehrt zurück, wenn das Ergebnis nicht negativ ist;
- ruft bei negativem Ergebnis `9C8Bh` auf.

`978Ch`:
- lädt DS auf `0E35h`;
- führt `LOCK INC WORD PTR [BX]` aus;
- kehrt zurück, wenn das Ergebnis positiv ist;
- ruft bei null oder negativem Ergebnis `9C19h` auf.

Das ist das typische Maschinenmuster eines atomaren Semaphore-P/V-Paares: Der Abstieg kann einen wartenden Aufrufer blockieren; der Anstieg kann einen wartenden Aufrufer aufwecken. Diese Einordnung stützt sich auf die tatsächlichen Vorzeichenverzweigungen und die Aufrufe der Warte-/Schedulerpfade, nicht allein auf die Wrappernamen.

### 18.2 Erweiterter Kontext-/Besitzerpfad `971Dh/9754h`

`971Dh` führt im Datensegment `0E35h` folgende Operationen aus:
1. AX erhält das Wort `[BX+06h]`; es wird mit `[0FB8h]` verglichen.
2. Wenn die Werte verschieden sind, wird das Wort `[BX]` dekrementiert. Bei negativem Ergebnis folgt `9C8Bh`.
3. Danach wird der aktuelle Wert `[0FB8h]` nach `[BX+06h]` geschrieben.
4. Das Wort `[BX+04h]` wird inkrementiert.

`9754h` führt den Gegenpfad aus:
1. `[BX+04h]` wird dekrementiert.
2. Wenn das Ergebnis nicht mehr positiv ist, wird `[BX+06h]` auf `FFFFh` gesetzt.
3. `[BX]` wird atomar inkrementiert.
4. Bei einem Ergebnis kleiner oder gleich null folgt `9C19h`.

**Gesichert:** Neben dem Zähler bei `[BX]` verwaltet dieses Paar einen zweiten Zähler bei `+04h` und einen Kontextwert bei `+06h`. Der Kontextwert wird mit dem globalen Wert `[0FB8h]` verglichen und bei Erwerb aktualisiert. Das ist ein erweiterter, kontextabhängiger Synchronisationspfad. Ob er im engeren Sinn als rekursiver Mutex oder als eine andere Kernel-Sperrstruktur bezeichnet werden soll, bleibt ohne Analyse aller Nutzer offen.

### 18.3 Zuordnung der sechs Wrapper

| Wrapper | BX-Wert | gemeinsames Ziel | belegte Funktion |
|---|---:|---|---|
| `0C97h` | `0186h` | `971Dh` | erweiterter Erwerb-/Kontextpfad |
| `0C9Eh` | `0186h` | `9754h` | erweiterter Freigabe-/Kontextpfad |
| `0CA5h` | `018Eh` | `9776h` | Semaphore-Abstieg / ggf. warten |
| `0CAC h` | `018Eh` | `978Ch` | Semaphore-Anstieg / ggf. aufwecken |
| `0CB3h` | `0196h` | `971Dh` | erweiterter Erwerb-/Kontextpfad |
| `0CBAh` | `0196h` | `9754h` | erweiterter Freigabe-/Kontextpfad |

Die Wrapper sichern BX, setzen die jeweilige Konstante und springen in die gemeinsamen Routinen. Diese Konstanten sind Offsets im zentralen Segment `0E35h`, weil die Ziele selbst DS über `9630h` auf dieses Segment setzen.

### 18.4 Bestätigung durch den Aufrufer `0A3Ch`

`0A3Ch` ruft `0CA5h` am Anfang auf und auf seinen Erfolgs- wie Fehlerpfaden `0CAC h` zum Verlassen des geschützten Bereichs. Damit ist für diesen konkreten Aufrufer die Paarung aus Semaphore-Abstieg und Semaphore-Anstieg direkt belegt.

Die Aufrufe von `0CA5h` in `0BD0h` verwenden denselben Synchronisationsoffset `018Eh`; der vollständige Freigabepfad muss dort weiterhin über die nachfolgenden Unterroutinen betrachtet werden.

### 18.5 Ergebnis Untersuchung 2257

1. `9776h/978Ch` bilden ein atomisches Semaphore-P/V-Paar mit bedingtem Warten bzw. Aufwecken.
2. `971Dh/9754h` verwalten zusätzlich zu einem Zähler einen zweiten Zähler bei `+04h` und einen Kontextwert bei `+06h`.
3. Die Wrapperkonstanten `0186h`, `018Eh` und `0196h` wählen drei getrennte Synchronisationsobjekte im Segment `0E35h) aus.
4. `0A3Ch` verwendet `0CA5h` und `0CAC h` als Eintritts-/Austrittspaar um den Zugriff auf die über `[0192h]` referenzierte Datenstruktur.
5. Die genauen symbolischen Namen der drei Synchronisationsobjekte sind nicht belegt.

**Nächster Schritt 2258:** Die drei Synchronisationsobjekte `0186h`, `018Eh` und `0196h` mit ihren Initialisierungs- und Aufrufstellen vergleichen. Zusätzlich die Schedulerpfade `9C19h` und `9C8Bh` so weit verfolgen, dass die Blockier-/Aufweckwirkung und die Bedeutung der jeweiligen Zählergrenzen vollständig belegt sind.


## 19. Untersuchung 2258 – Warte- und Aufweckpfade `9C8Bh/9C19h`

**Ziel:** Die in Untersuchung 2257 festgestellten Semaphore-Verzweigungen bis zu den Scheduler-/Kontextpfaden verfolgen. Grundlage sind die Routinen `9C19h`, `9C8Bh`, `9CF6h` und deren Übergänge zu `9B1Ah`/`9B1Bh).

### 19.1 Wartepfad `9C8Bh`

Die Routine sichert DS, SI, DI, CX, Flags, DX, ES und BP. Danach:
- DS wird über `9630h` auf `0E35h` gesetzt; ES wird aus dem übergebenen AX geladen.
- Der aktuelle Wert am Semaphore-/Synchronisationswort `ES:[BX]` wird gelesen.
- Ist eines der unteren vier Bits gesetzt, wird das Wort dekrementiert und der Kontrollfluss geht zum Schedulerpfad `9B1Ah) zurück.
- Andernfalls prüft die Routine globale Schedulerzustände bei `0FC8h) und den aktuellen Kontext bei `0FB8h).
- Im regulären Wartefall werden Kontextdaten gesichert: Rücksprung-/Stackinformationen erscheinen in den Feldern `+02h), `+04h) und `+06h) des Kontextknotens. Anschließend wird in den Schedulerstack gewechselt und der Schedulerpfad fortgesetzt.
- Ein alternativer Pfad verwendet globale Austauschfelder `0FC4h) und `0FC6h), setzt den Synchronisationswert vorübergehend auf `FFFFh) und wartet auf eine Änderung des globalen Signals `0FC3h).

**Gesichert:** `9C8Bh` ist kein gewöhnlicher Rückgabecode. Bei nicht verfügbarem Synchronisationsobjekt sichert sie den aktuellen Ausführungskontext und übergibt die Kontrolle an die Schedulerlogik.

### 19.2 Aufweck-/Freigabepfad `9C19h)

Die Routine sichert ebenfalls umfangreiche Register und Flags, lädt DS auf `0E35h), sperrt Interrupts und prüft den Zähler bei `ES:[BX]):

- Liegt der Wert unter `0010h), wird er erhöht und der Kontrollfluss geht zu `9B1Bh).
- Andernfalls wird `9CF6h` aufgerufen, um die mit dem Synchronisationsobjekt verbundene Warteliste zu bearbeiten.
- Die globale Liste wird über `0FC0h) verwaltet; `0FB8h) enthält den aktuellen Kontextzeiger.
- Die Routine vergleicht das erste Byte der Wartelisteneinträge und verfolgt deren Verknüpfung über das Wort bei `+06h). Der ausgewählte Eintrag wird aus der Liste gelöst bzw. der Kopfzeiger angepasst.
- Für einen Kontextwechsel werden Segment-/Stackwerte in den Eintragsfeldern `+02h) und `+04h) gespeichert; anschließend wird über den Schedulerpfad weitergeschaltet.

**Gesichert:** `9C19h` verwaltet nicht nur einen Zähler. Sie bearbeitet auch die Warteliste und den aktuellen Kontext; die Liste enthält verkettete Einträge und wird anhand eines Bytewertes sortiert bzw. ausgewählt.

### 19.3 Bedeutung der Zählergrenze

Die Grenze `0010h` wird in `9C19h` ausdrücklich geprüft. Sie ist damit eine reale Grenze der internen Zähler-/Wartelogik. Aus dem Ausschnitt allein folgt jedoch nicht, dass sie die maximale Anzahl gleichzeitig wartender Prozesse darstellt; dafür müsste die vollständige Datenstruktur einschließlich der Alternativpfade und globalen Schedulerzustände ausgewertet werden.

### 19.4 Initialisierung der Synchronisationsobjekte

Im linearen Kernel-Disassembly sind die Offsets `0186h`, `018Eh` und `0196h` als unmittelbare Operanden der Wrapperkonstanten sichtbar. Direkte absolute Initialisierungs-Schreibzugriffe auf genau diese drei Offsets wurden in den bisher untersuchten Codebereichen nicht gefunden. Da `0E35h` ein Laufzeit-Datensegment ist und seine vollständig initialisierte Abbildung nicht aus dem Load-Modul allein rekonstruiert werden kann, wäre die Behauptung, diese Objekte würden nie initialisiert, nicht gerechtfertigt.

**Offen:** Die Herkunft ihrer Anfangswerte muss über Segmentaufbau, Initialisierungstabellen oder indirekte Schreibpfade geklärt werden.

### 19.5 Ergebnis Untersuchung 2258

1. `9C8Bh` sichert im Wartefall den aktuellen Ausführungskontext und übergibt an den Scheduler.
2. `9C19h` bearbeitet den Zähler und die zugehörige Warteliste; dabei werden verkettete Kontexteinträge untersucht und angepasst.
3. Die Wartelisteneinträge verwenden mindestens die Felder `+02h), `+04h) und `+06h) für Kontext-/Verknüpfungsinformationen.
4. Die Zählergrenze `0010h` ist direkt belegt; ihre vollständige Kapazitätsbedeutung bleibt offen.
5. Die Anfangswerte der drei Synchronisationsobjekte bei `0186h), `018Eh) und `0196h) sind aus dem bisherigen Codeausschnitt nicht sicher rekonstruierbar.

**Nächster Schritt 2259:** Die Initialisierung von Datensegment `0E35h` und die indirekten Schreibpfade auf die Synchronisationsobjekte verfolgen. Parallel prüfen, ob die Knoten bei `05AEh/05B2h` und die Scheduler-Wartelisten denselben Allocator verwenden oder getrennte Datenstrukturen sind.


## 20. Untersuchung 2259 – Abgrenzung von Objektliste, Freiliste und Scheduler-Warteliste

**Quelle:** reproduzierte Disassemblierung von `KERNEL.OLD`; untersucht wurden `6DACh–6E67h), `11CBh–1227h), `9C19h–9D4Ah) sowie die Scheduler-Aufrufpfade `9B07h), `9B1Ah) und `9CF6h). Alle Segmentbezüge auf das zentrale Datensegment beruhen auf den in Untersuchung 2251 bestätigten Ladehelfern.

### 20.1 Speicherfreiliste bei `0E35h:0E48h`

Die Routine `6DACh` beschafft einen Block aus der globalen Freiliste:

1. Interruptsperre und Sicherung der Flags.
2. BX erhält den Kopfzeiger aus `[0E48h]`.
3. Bei vorhandenem Block wird dessen Nachfolger aus `[BX+6]` als neuer Kopf nach `[0E48h]` übernommen.
4. Die Wortfelder bei `+0), `+2), `+4), `+6), `+0Ah), `+0Ch) und `+0Eh) werden auf null gesetzt.
5. Das zuvor gesicherte BX-Eingangsargument wird nach `+08h` geschrieben.
6. Der freie Blockzähler `[0E4Ah]` wird dekrementiert.

Die Freigaberoutine `6E2Fh` prüft zunächst die Blockadresse: 16-Byte-Ausrichtung und zulässiger Adressbereich ab `15B0h) bis unter `[0E4Ch]). Danach setzt sie `[BX]` und `[BX+8]` auf null, schreibt den Marker `F3h` nach `[BX+1]), hängt den Block über `[BX+6]` an den bisherigen Kopf und setzt `[0E48h]=BX). Der freie Blockzähler `[0E4Ah]` wird erhöht.

**Gesichert:** Die Freiliste `0E48h` verkettet 16-Byte-Blöcke über Offset `+6). Der Marker `F3h` kennzeichnet den freigegebenen Block im untersuchten Pfad. Die Routine `6DACh` nimmt denselben Block wieder aus der Freiliste und löscht die Felder vor seiner erneuten Verwendung.

### 20.2 Objektliste bei `05AEh/05B2h)

Die in Untersuchung 2252 und 2253 rekonstruierte Routine `11CBh` fordert über `6DACh` einen 16-Byte-Block an und verwendet ihn als Objektknoten:
- `+01h = FDh) als Knotentypmarker;
- `+04h) als Verkettungsfeld zur Objektliste;
- `+06h) als indexabhängigen Zeigerwert;
- `+08h) als übernommener Kontextwert aus `SS:[0002h]);
- `+0Ch) als optionaler Verweis auf einen weiteren Knoten;
- `+0Eh = 0001h) als initialisierter Wortwert.

Der neue Knoten wird an den Kopf-Link `0E35h:05B2h) gehängt. Die Freiliste verwendet dagegen `+6) nur solange der Block frei ist. Nach der Entnahme aus der Freiliste wird dieses Feld von `11CBh) als Objekt-/Cachefeld neu belegt.

**Gesichert:** Objektliste und Freiliste verwenden dieselben 16-Byte-Blöcke, aber unterschiedliche Linkfelder und unterschiedliche Lebenszykluszustände. `+6) hat deshalb keine globale, für alle Zustände gleiche Bedeutung.

### 20.3 Scheduler-Warteliste bei `9C19h/9CF6h)

Die Scheduler-Warteliste ist eine dritte Struktur:

- `9C19h` erhält den Synchronisationsbereich über ES:BX. Wenn der Zähler unter `0010h` liegt, erhöht die Routine ihn und kehrt über den Scheduler-Wiederaufnahmepfad zurück.
- Bei erreichter Grenze ruft sie `9CF6h` auf.
- `9CF6h` liest den Wartelistenkopf aus `ES:[BX]`. Der Wert `FFFFh` steht für die leere Liste.
- Ein Wartelisteneintrag wird über das Byte bei `+0) nach einer Rang-/Prioritätsgröße verglichen. Die Routine durchläuft die Liste über den Zeiger bei `+6).
- Beim Einfügen wird der Vorgängerlink angepasst; der neue Kontext wird an der passenden Position eingehängt.
- Der aktuelle Kontext wird durch `[0FB8h]` referenziert. Die Schedulerpfade `9C8Bh` und `9C19h` speichern Stackoffset und Stacksegment in den Kontextfeldern `+2) und `+4); das Feld `+6) wird als Wartelistenlink benutzt.

Die Routine `9CF6h` erzeugt in diesem Pfad keinen neuen 16-Byte-Knoten über `6DACh`. Sie verknüpft bereits vorhandene Kontextobjekte des Schedulers.

**Gesichert:** Die Scheduler-Warteliste ist nach dem ersten Byte der Kontextobjekte geordnet und verwendet `+6) als Link. Die Elemente sind vorhandene Schedulerkontexte, nicht die über `11CBh` angelegten Objektknoten.

### 20.4 Vergleich der drei Listen

| Struktur | Kopf / Anker | Linkfeld | Elementtyp | Verwaltung |
|---|---|---:|---|---|
| Objektliste | `0E35h:05AEh`, Kopf-Link `05B2h` | `+4` | 16-Byte-Objektknoten mit Marker `FDh` | `11CBh` einfügen, `1228h` entfernen |
| Speicherfreiliste | `0E35h:0E48h` | `+6` | freie 16-Byte-Blöcke, Marker `F3h` | `6DACh` entnehmen, `6E2Fh` freigeben |
| Scheduler-Warteliste | Synchronisationsobjekt `ES:[BX]` | `+6` | bestehende Schedulerkontexte | `9CF6h` sortiert ein/entfernt; `9C8Bh/9C19h` schalten |

### 20.5 Ergebnis Untersuchung 2259

1. Die Freiliste `0E48h` und die Objektliste `05AEh/05B2h` verwenden denselben 16-Byte-Blockpool, aber verschiedene Linkfelder.
2. `6DACh` entfernt einen freien Block; `6E2Fh` hängt einen freigegebenen Block über `+6) wieder ein.
3. `11CBh` nutzt den entnommenen Block als Objektknoten und verwendet `+4) als Objektlistenlink.
4. Die Scheduler-Warteliste ist davon getrennt: Sie verwendet bestehende Kontextobjekte, deren `+6)-Feld als Link dient.
5. Die Schedulerliste wird nach dem Byte bei `+0) geordnet; dies ist ein belegtes Sortierkriterium, aber die exakte symbolische Prioritätsdefinition ist noch nicht dokumentiert.
6. Der identische Feldoffset `+6) bedeutet je nach Lebenszyklus und Struktur etwas anderes; künftige Dossierabschnitte müssen die jeweilige Struktur ausdrücklich nennen.

**Nächster Schritt 2260:** Die Initialisierung und Verwendung der Synchronisationsobjekte bei `0186h), `018Eh) und `0196h) im Datensegment `0E35h) weiter verfolgen. Zusätzlich den Erzeugungs- und Freigabepfad der Schedulerkontexte (insbesondere die Aufrufstellen von `9C8Bh), `9C19h) und die Felder `+0/+2/+4/+6)) anhand der Kernel-Taskverwaltung untersuchen.


## 21. Untersuchung 2260 – Aufruferzuordnung der Synchronisationsobjekte

**Ziel:** Die in Untersuchung 2257 ermittelten Synchronisationsoffsets `0186h`, `018Eh) und `0196h) nicht nur anhand der Wrapper, sondern anhand ihrer konkreten Aufrufer einordnen. Die folgenden Aussagen beziehen sich auf den beobachteten Schutzbereich der jeweiligen Aufrufe. Sie vergeben keine nicht belegten symbolischen Kernel-Namen.

### 21.1 Objekt `0E35h:0186h` – wiederkehrender geschützter Bereich

Die Wrapper `0C97h/0C9Eh` rufen den erweiterten Erwerbs-/Freigabepfad `971Dh/9754h` mit BX=`0186h` auf. Im Disassembly sind unter anderem folgende Aufrufer zu sehen:

| Aufrufer | Geschützter Abschnitt | Beleg |
|---|---|---|
| `0552h` | setzt `[0213h]` aus AH, ruft `72Bh`, löscht `[0213h]` wieder | `0553h`, `0565h` |
| `0595h` | ruft `0968h` | `0596h`, `059Fh` |
| `05C9h` | führt zwei Prüfungen über `09B6h` aus und setzt das Ergebnis | `05CAh`, `05E3h` |
| `05F0h` | ruft `0A3Ch`; der Aufrufpfad hat zusätzlich den Wrapper `0CAC h` für das innere Semaphoreobjekt | `05F3h), `0600h), `0603h` |
| `063Ch` | führt Prüfungen, Blockanlage und Kopie eines 16-Byte-Blocks aus | `063Fh), `0689h` |

**Gesichert:** `0186h` ist ein gemeinsam genutztes Synchronisationsobjekt für mehrere Kerneloperationen, darunter den indexbezogenen Cachepfad `72Bh`, Prüf-/Vergleichsroutinen und Speicher-/Blockoperationen. Die genaue fachliche Bezeichnung der Sperre ist aus den Aufrufern allein nicht zu bestimmen.

### 21.2 Objekt `0E35h:018Eh` – Synchronisation um Datenzugriff

Die Wrapper `0CA5h/0CAC h` führen den einfachen atomischen Semaphore-Abstieg/-Anstieg für BX=`018Eh) aus.

- `0A3Ch` ruft `0CA5h` vor dem Lesen der über `[0192h]` referenzierten Struktur.
- Der Pfad ruft `0CAC h` zum Freigeben des geschützten Bereichs auf.
- `0BD0h` ruft `0CA5h` im Statuszweig mit Bit `20h) auf; der weitere Kontrollfluss läuft über die gemeinsame Ergebnisaufbereitung.

**Gesichert:** `018Eh` wird als Zählsemaphore verwendet und schützt mindestens den Zugriffspfad von `0A3Ch`. Die genaue Ressource, deren Zugriff damit serialisiert wird, ist noch nicht benannt.

### 21.3 Objekt `0E35h:0196h` – Ressourcenzugriff und Statusprüfung

Die Wrapper `0CB3h/0CBAh` rufen den erweiterten Erwerbs-/Freigabepfad `971Dh/9754h` mit BX=`0196h) auf.

Belegte Aufrufer:
- `0B87h` ruft `0CB3h` vor der Auswertung von Index-/Statusdaten und dem Zugriff über den Zeiger `[019Eh]); am Ende ruft es `0CBAh`.
- `0E6Ah` ruft `0CB3h`, danach `0E71h) und einen indirekten Aufruf über `DS:[05B8h]) mit `DI=18h); anschließend erfolgt `0CBAh`.

**Gesichert:** `0196h) schützt mindestens zwei Pfade, die index-/ressourcenbezogene Daten bzw. einen Dispatch-Aufruf verwenden. Ein engerer Objektname wäre ohne weitere Aufruferanalyse spekulativ.

### 21.4 Warum die Initialwerte weiterhin offen sind

Die untersuchten Codeverweise setzen BX auf die drei Konstanten und rufen die gemeinsamen Synchronisationsroutinen auf. Im bisherigen Disassembly-Audit wurden keine direkten unmittelbaren Schreibinstruktionen gefunden, die die Anfangswerte an den Offsets `0186h), `018Eh) oder `0196h) setzen. Das schließt indirekte Initialisierung, Segmentabbild-/Loaderdaten oder Initialisierung durch einen anderen Kernelpfad nicht aus.

**Wichtige Abgrenzung:** Aus dem Fehlen eines direkten `mov [0186h],...`-Musters darf nicht gefolgert werden, die Synchronisationsobjekte seien uninitialisiert. Ihre Laufzeitinitialisierung muss über den Aufbau des Datensegments und indirekte Schreibpfade geprüft werden.

### 21.5 Ergebnis Untersuchung 2260

1. `0186h) ist ein gemeinsam genutztes erweitertes Synchronisationsobjekt, das mehrere Kernelbereiche schützt.
2. `018Eh) wird als einfacher Zählsemaphore verwendet; `0A3Ch` ist ein bestätigter Aufrufer.
3. `0196h) ist ein weiteres erweitertes Synchronisationsobjekt, das unter anderem `0B87h) und `0E6Ah) verwenden.
4. Die drei Offsets haben unterschiedliche Aufruferprofile; sie dürfen nicht als ein einziges Synchronisationsobjekt behandelt werden.
5. Die initialen Laufzeitwerte sind noch nicht aus dem statischen Codebestand belegt.

**Nächster Schritt 2261:** Den Erzeugungs-/Initialisierungspfad des Datensegments `0E35h) und seine Datenbereiche vor `021Ch) verfolgen. Ziel ist, die Startwerte der Synchronisationsobjekte und des Kontextzeigers `0FB8h) aus einem konkreten Initialisierungspfad nachzuweisen, nicht aus vermuteten Segmentdefaults abzuleiten.


## 22. Untersuchung 2261 – MZ-Relokation des Kernel-Datensegments

**Quelle:** unveränderte Datei `GEOWORKS/KERNEL.OLD` aus dem bereitgestellten Archiv. Geprüft wurden MZ-Header, Relokationstabelle und die Bytes im Load-Modul an den Offsets `962Eh), `9630h), `9636h) und `9AD6h–9AE6h).

### 22.1 MZ-Headerwerte

Die 13 ersten MZ-Wortfelder ergeben unter anderem:

| MZ-Feld | Wert | Bedeutung |
|---|---:|---|
| `e_crlc` | `0111h` = 273 | Anzahl Relokationseinträge |
| `e_cparhdr` | `0060h` = 96 | Headerlänge in Paragraphen = 1.536 Bytes |
| `e_ss` | `0E35h` | initialer SS-Absatzoffset relativ zum Ladeabsatz |
| `e_sp` | `15B0h` | initialer Stackpointer |
| `e_ip` | `02B1h` | initialer Instruction Pointer |
| `e_cs` | `0000h` | initialer CS-Absatzoffset relativ zum Ladeabsatz |
| `e_lfarlc` | `003Ch` | Beginn der Relokationstabelle |

Der MZ-Header ist 96 Paragraphen lang. Die Dateigröße beträgt 72.688 Bytes; die oben verwendete Disassemblierung beginnt deshalb bei Dateioffset 1.536 und bildet das Load-Modul ab.

### 22.2 Relokationseintrag für den Segmentladehelfer

Die Relokationstabelle enthält einen Eintrag:
- Offset `962Eh`
- Segment `0000h`
- Load-Modul-Adresse `0000:962Eh`

Im unveränderten Load-Modul stehen an diesem Offset die Bytes `35 0E`, also das Wort `0E35h`. Der MZ-Loader addiert bei diesem Relokationseintrag den tatsächlichen Ladeabsatz zum Wort. Der zur Laufzeit verwendete Wert ist daher nicht notwendigerweise das rohe Wort `0E35h), sondern der relocierte Segmentwert `Ladeabsatz + 0E35h`.

### 22.3 Verbindung mit `9630h) und `9636h)

Die beiden überlappenden Ladehelfer lauten im Load-Modul:

- `9630h`: Segmentpräfix `CS:`, dann `mov DS, CS:[962Eh]), anschließend `ret`.
- `9636h`: Segmentpräfix `CS:`, dann `mov ES, CS:[962Eh]), anschließend `ret`.

Damit laden beide Helfer zur Laufzeit den relocierbaren Segmentwert aus dem MZ-relokierten Wort. Dieser Wert entspricht dem initialen SS-Segmentwert des MZ-Headers, da `e_ss` ebenfalls `0E35h` beträgt.

**Gesichert:** In den durch `9630h)/`9636h) erreichten Pfaden werden DS bzw. ES auf das zur Laufzeit relocierte Segment gesetzt, das der MZ-Header als initiales SS-Segment beschreibt. Die frühere Kurzform „DS=0E35h“ bzw. „ES=0E35h“ beschreibt nur den rohen, vor Relokation im Load-Modul sichtbaren Wert.

### 22.4 Abgrenzung zum direkten Immediate-Wert bei `9AD6h)

Der Scheduler-Initialisierungspfad enthält:
- `9AD6h): `mov SS, CS:[962Eh]` – nutzt den relocierbaren Wert;
- `9ADBh): `mov SP,15B0h`;
- `9ADFh–9AE4h): `mov AX,0E35h`, danach `mov DS,AX` und `mov ES,AX`.

Für das Immediate-Wort `0E35h` bei `9AE0h) wurde kein MZ-Relokationseintrag gefunden. Es ist daher im Load-Modul ein nicht relocierter Literalwert. Ohne einen Beleg für die tatsächliche Ladeabsatz-/Ladeadresskonvention des GeoWorks-Kernel-Loaders darf dieser Pfad nicht mit dem relocierbaren Segmentwert des Helfers gleichgesetzt werden.

**Offen:** Ob der Kernel in der vorgesehenen Laufzeitumgebung stets an einem Ladeabsatz ausgeführt wird, bei dem der Literalwert `0E35h` mit dem relocierbaren SS-Segment zusammenfällt, ist durch die Kerneldatei allein nicht nachgewiesen. Das muss über den tatsächlichen GeoWorks-Loader bzw. einen Laufzeitdump geprüft werden.

### 22.5 Korrekturregel für frühere Untersuchungen

Für die bisherigen Abschnitte zu `05AEh), `05B2h), `05B8h/05BAh), `0E48h), `0FB8h) und den Synchronisationsobjekten gilt:

- Bei Zugriffen nach einem Aufruf von `9630h) oder `9636h) sind die Offsets als Offsets im relocierbaren Kernel-Datensegment zu lesen. Die Segmentbasis ist der zur Laufzeit aus `CS:[962Eh]` geladene Wert.
- Die Schreibweise `0E35h:Offset` in den vorherigen Untersuchungen ist als verkürzte Bezeichnung des im MZ-Header hinterlegten Segmentdisplacements zu verstehen, nicht als bewiesene absolute Laufzeitadresse.
- Direkte Segment-Immediate-Werte wie bei `9ADFH) sind getrennt zu behandeln und nur dann als identisch zu interpretieren, wenn die Loader-Ladeadresse verifiziert ist.

### 22.6 Ergebnis Untersuchung 2261

1. `KERNEL.OLD` hat MZ `e_ss=0E35h` und `e_sp=15B0h`.
2. Die MZ-Relokationstabelle enthält einen Eintrag für Load-Modul-Offset `962Eh`.
3. Der dortige rohe Wert `0E35h` wird zur Laufzeit vom MZ-Loader um den Ladeabsatz relocierbar angepasst.
4. Die Helfer `9630h) und `9636h) laden DS/ES aus genau diesem relocierbaren Wort.
5. Der direkte Immediate-Wert `0E35h` bei `9ADFH) ist nicht relociert und darf ohne Loaderbeleg nicht mit dem relocierbaren Wert gleichgesetzt werden.
6. Frühere Segmentangaben in diesem Dossier werden durch diese Präzisierung als Offset-/Displacement-Bezeichnungen interpretiert, sofern der Zugriff über die Segmentladehelfer erfolgt.

**Nächster Schritt 2262:** Den GeoWorks-Ladepfad bzw. Kernel-Startvertrag untersuchen, um die tatsächliche Ladeabsatzkonvention zu bestimmen und den direkten Immediate-Segmentwert bei `9ADFH) gegen den relocierbaren Wert zu prüfen. Danach kann die Segmentnotation im Dossier endgültig vereinheitlicht werden.


## 23. Untersuchung 2262 – Kompatibilitätsprüfung des bereitgestellten `GEOWORKS.zip` mit SDK 0.1

**Ziel:** Prüfen, ob das vom Nutzer bereitgestellte Archiv `GEOWORKS.zip` direkt als SDK-Zielarchiv verwendet werden kann. Grundlage sind die tatsächlichen ZIP-Mitglieder, ihre SHA-256-Prüfsummen, der Parser aus `pcgeos1/geode.py` sowie die verbindlichen Zielpfade und Hashes in `pcgeos1/target.py` und `docs/TARGET_COMPATIBILITY.md`.

### 23.1 Vom SDK erwartete Zielmitglieder

`pcgeos1/target.py` verlangt jeweils genau ein ZIP-Mitglied mit diesen Endungen:

| Template | erwartete Endung |
|---|---|
| SPINTEXT | `/WORLD/EXTRAS/SPINTEXT.GEO` |
| NOTEPAD | `/WORLD/NOTEPAD.GEO` |
| VIEWER | `/WORLD/VIEWER.GEO` |
| TERM | `/WORLD/TERM.GEO` |

Die Funktion `member()` bricht ab, wenn nicht genau ein passendes Mitglied gefunden wird. Erst danach erfolgt die SHA-256-Prüfung.

### 23.2 Tatsächliche Mitglieder im Nutzerarchiv

| Template | Archivpfad | Bytes | SHA-256 |
|---|---|---:|---|
| SPINTEXT | `GEOWORKS/WORLD/SPINTEXT.GEO` | 3.764 | `6a9ddda1c491438d29b10c044eb92e5b9e8bd701c922172dd6bb89988e2c1261` |
| SPINTEXT | `GEOWORKS/WORLD/PROGRAMM.E/SPINTEXT.GEO` | 3.748 | `18f2075c9d61fe7231b1dacae8c171e68c2028ef2fca6d40a6694158fdfcb9fd` |
| NOTEPAD | `GEOWORKS/WORLD/NOTEPAD.GEO` | 8.070 | `a1ebd0cb84712a126b1f67f5fd1ca6b57f8bda2e9038e9224ba16ebc008f9ea9` |
| NOTEPAD | `GEOWORKS/DOCUMENT/NOTEPAD.GEO` | 8.070 | `3d0bbaf6640eecca7c884a3351ddd957435096af6ff0b6b02793fa9eb7286b29` |
| VIEWER | `GEOWORKS/WORLD/VIEWER.GEO` | 59.984 | `c884b76cdc4f9119d4794f7830d5438e0abcc1d92d3cc248aa912bde85ed43e7` |
| TERM | `GEOWORKS/WORLD/TERM.GEO` | 63.718 | `a62ebc0fb3c01acb4b59c8172d20d520653822a6d42f0bec4831dfdb93e1cf3a` |

**Pfadbefund:** Im bereitgestellten Archiv gibt es kein Mitglied, das auf `/WORLD/EXTRAS/SPINTEXT.GEO` endet. Deshalb scheitert bereits die Mitgliederauflösung für SPINTEXT. Die übrigen erwarteten Endungen sind jeweils eindeutig vorhanden.

### 23.3 Vergleich mit den im SDK hinterlegten Hashes

Das SDK erwartet folgende SHA-256-Werte:

| Template | SDK-Hash | Nutzerarchiv |
|---|---|---|
| SPINTEXT | `848f5afb43a2184b01d2a4ad3231957b6ab9936006b23b4b2a260d1224d44370` | kein passender Hash |
| NOTEPAD | `edc48848ff4b9d2880e715bbb29532f14b3b54293c45159c467e33e2af841d1b` | kein passender Hash |
| VIEWER | `3d433a39c455a9cea242763dad0e3f681b4196fb7b1a75a08ca47e1aa8aa4a30` | kein passender Hash |
| TERM | `2d66ac2ff9fd24c4591303b2cba7cec6f40f0d52b4f3d75d9e0cdaa5fc1be542` | kein passender Hash |

Keines der passenden bzw. ähnlich benannten GEO-Mitglieder aus dem Nutzerarchiv besitzt den im SDK hinterlegten Hash.

### 23.4 Positiver Format- und Protokollbefund

Die sechs oben genannten Dateien wurden zusätzlich mit dem im Repository vorhandenen bounds-geprüften GEODE-Parser untersucht. Alle sechs Dateien lassen sich als GEOS-1.x-Format 1 parsen.

Für die ausgewählten Dateien aus `WORLD` ergeben sich:

| Datei | GEOS-Format | Release | Kernelprotokoll | UI-Protokoll |
|---|---:|---|---|---|
| SPINTEXT | 1 | 1.2.7.2 | 622.3 | 693.0 |
| NOTEPAD | 1 | 1.2.8.5 | 622.3 | 693.0 |
| VIEWER | 1 | 1.2.8.16 | 622.3 | 693.0 |
| TERM | 1 | 1.2.8.3 | 622.3 | 693.0 |

Damit ist die grundlegende Format- und Protokollfamilie mit dem im SDK dokumentierten Zielprotokoll vereinbar. Das beweist jedoch nicht, dass die privaten Objekt- und Ressourcenlayouts der vier Templates byte- oder ABI-kompatibel mit den im SDK erwarteten Vorlagen sind.

### 23.5 Warum `allow_unknown_target` allein nicht genügt

Das Projektfeld `allow_unknown_target=true` setzt beim Aufruf von `load_templates()` lediglich `strict=False` und schaltet damit die Hashprüfung ab. Die ZIP-Mitgliedersuche mit den fest codierten Endungen läuft unverändert weiter. Der fehlende Pfad `/WORLD/EXTRAS/SPINTEXT.GEO` bleibt deshalb ein unmittelbarer Abbruchgrund.

Eine temporäre Archivkopie mit angepasstem SPINTEXT-Pfad könnte diesen ersten Abbruch umgehen. Mit `allow_unknown_target=true` ließe sich dann ein experimenteller Host-Build versuchen. Das wäre aber kein bestätigter Zielprofil-Support: Die abweichenden Hashes und privaten Ressourcenlayouts müssten zuvor separat auditiert werden.

### 23.6 Konsequenz für den ersten `GEOTEST.GEO`-Build

**Gesicherter Befund:** Das bereitgestellte `GEOWORKS.zip` kann mit der unveränderten SDK-0.1-Zielauflösung nicht direkt als Buildziel verwendet werden. Es fehlen der erwartete SPINTEXT-Pfad und sämtliche vier exakten Template-Hashes.

**Positiver Befund:** Die vorhandenen Templates sind valide GEOS-1.x-Geodes mit Kernelprotokoll 622.3 und UI-Protokoll 693.0. Ein eigenes, ausdrücklich als experimentell gekennzeichnetes Profil für diese deutsche GeoWorks-1.2.8-Installation ist daher ein sinnvoller nächster Prüfpfad; Kompatibilität der UI-Templates ist damit noch nicht bestätigt.

**Keine Änderung vorgenommen:** Weder `target.py` noch die Originaldateien oder das Nutzerarchiv wurden verändert. Es wurde noch kein `GEOTEST.GEO`-Build ausgeführt.

### 23.7 Ergebnis Untersuchung 2262

1. Der unveränderte SDK-0.1-Loader findet im Nutzerarchiv kein passendes SPINTEXT-Mitglied am erwarteten Pfad.
2. Alle vier erwarteten Template-Hashes weichen von den vorhandenen Dateien ab.
3. Die vorhandenen Dateien sind parsebare GEOS-1.x-Geodes mit Kernel 622.3 und UI 693.0.
4. `allow_unknown_target=true` umgeht nur die Hashprüfung, nicht die Pfadauflösung.
5. Ein separates deutsches Zielprofil muss Pfade und Hashes ausdrücklich dokumentieren und die verwendeten UI-Ressourcen vor dem Build strukturell vergleichen.

**Nächster Schritt 2263:** Ein explizites Zielprofil `geoworks-1.2.8-de` für das Nutzerarchiv vorbereiten. Zunächst SPINTEXT-Ressourcen R03/R04 und VIEWER-Ressourcen R0C/R1C gegen die vom SDK erwarteten Objekt-/LMem-Annahmen prüfen; erst nach bestandener Prüfung die Pfadauflösung profilabhängig ergänzen. Das strikte Standardprofil bleibt unverändert.


## 24. Untersuchung 2263 – Strukturvergleich der tatsächlich verwendeten UI-Templates

**Ziel:** Nach dem Gesamtdatei-Hash-Audit aus Untersuchung 2262 nicht bei der Geode-Datei als Ganzes stehen bleiben. Der SDK-Build übernimmt aus SPINTEXT die Ressourcen R03/R04 und aus VIEWER R0C/R1C. Deshalb werden genau diese vier Ressourcen und alle vom aktuellen `build_basic_ui()` angesprochenen Handles im Nutzerarchiv geprüft.

### 24.1 Auswahl des SPINTEXT-Kandidaten

Das Nutzerarchiv enthält zwei SPINTEXT-Dateien. Für den Kandidaten `GEOWORKS/WORLD/PROGRAMM.E/SPINTEXT.GEO` ergeben sich:

| Ressource | Länge | Feld 08h | Feld 14h | Handle-Anzahl |
|---|---:|---:|---:|---:|
| R03 | `01E0h` | `01E0h` | `01E0h` | 16 |
| R04 | `0150h` | `014Ch` | `0150h` | 6 |

Diese Werte stimmen mit den Messwerten des Referenz-Audits vom 05.11.2026 überein. Auch die Handle-Flagfolgen stimmen exakt überein:

- R03: `00 02 03 02 03 02 07 02 02 07 02 07 02 03 02 07`
- R04: `00 03 02 02 02 00`

Die andere Datei `GEOWORKS/WORLD/SPINTEXT.GEO` hat bei R03 eine Ressourcenlänge von `01F0h` und zusätzliche 16 Bytes hinter dem bei `14h` angegebenen Wert. Ihre Handle-Flagfolge ist gleich, aber für die erste Profilbildung ist die Datei aus `PROGRAMM.E` der bessere Kandidat, weil Größe und beide Headerfelder dem Referenz-Audit exakt entsprechen.

### 24.2 SPINTEXT-Handles, die der SDK-Generator verwendet

Die aktuelle Funktion `build_basic_ui()` greift zu auf:

| Ressource | Handle | Flag | Chunk-Datenlänge | SHA-256 der Chunk-Daten |
|---|---:|---:|---:|---|
| R03 | `24h` | 03h | 21h | `a77f44d72ae4c9f2111cef3b71ea573535dd37f91e6b973730d5b68281cd1620` |
| R03 | `26h` | 02h | 08h | `7395b05d7f8c12284d825b3af6bc2619dd756b30233e2708dd373c498b9b369b` |
| R03 | `3Eh` | 07h | 47h | `69dbb0e67fddc64b0dd30b77622203e6c710d3be6c174aadb0bc6ad36fe38715` |
| R04 | `22h` | 03h | C6h | `625ad7d42b57ad99f0891f5615a2e6363d23707232b226f1cf862d515c66651f` |
| R04 | `24h` | 02h | 2Ah | `b363331aad64058ddf5cfb3a1304a83a72eefbd6617b5e5a9aea9fe1e648a865` |
| R04 | `26h` | 02h | 08h | `14130b018aef8b11e4d66efc55cfb98b4578d68a0c374f552faefcaba76d0229` |
| R04 | `28h` | 02h | 16h | `e8407786ed8b9de434e88f4793b4c2c40896f000d2a80556da6aa099bf599230` |

Die Handle-Offsets und Chunk-Längen liegen innerhalb der jeweiligen LMem-Ressourcen. Die Daten wurden mit der im Repository dokumentierten Handle-/Chunk-Auswertung ausgelesen.

### 24.3 VIEWER-Ressourcen

Für VIEWER R0C und R1C stimmen die Handle-Anzahlen und die im Referenz-Audit dokumentierten Flagfolgen exakt überein:

- R0C: 22 Handles; Flags `00 03 02 03 02 03 02 03 02 03 02 02 02 02 03 02 03 02 03 02 03 02`.
- R1C: 30 Handles; Flags `00 02 03 02 03 02 03 02 07 07 02 02 03 02 02 03 02 02 03 02 02 03 02 02 03 02 02 03 02 02`.

R0C besitzt im Nutzerarchiv eine größere rohe Ressourcengröße (`16A0h)) als die im Referenz-Audit gemessene LMem-Länge (`1440h)). Das Feld bei Offset `14h` enthält jedoch `1440h`; zusätzliche Daten liegen hinter dem LMem-Bereich. Der vom SDK verwendete Satz an Handles `22h), `32h), `36h), `3Ch), `44h), `48h) und `40h` liegt vor dem zusätzlichen langen Textchunk bei Handle `34h`. Der Generator verwendet Handle `34h` nicht.

R1C hat in der Nutzerdatei die Länge `02C0h`; die Felder bei `08h) und `14h` sind beide `02C0h), passend zum Referenz-Audit.

### 24.4 Bytevergleich der bereits dokumentierten Objektpaare

Zwei Bytevergleiche stimmen exakt mit den im Referenz-Audit dokumentierten Befunden überein:

**VIEWER R1C, Handles 0032h und 0038h:** Beide Chunks sind 29 Bytes lang. Unterschiede liegen ausschließlich bei:
- Offset `0Ch`: `38h` gegenüber `3Eh`
- Offset `12h`: `1Bh` gegenüber `19h`
- Offset `14h`: `34h` gegenüber `3Ah`
- Offset `18h`: `36h` gegenüber `3Ch`

**SPINTEXT R03, Handles 0032h und 0036h:** Beide Chunks sind 31 Bytes lang. Unterschiede liegen ausschließlich bei:
- Offset `0Ch`: `36h` gegenüber `2Dh`
- Offset `14h`: `34h` gegenüber `38h`
- Offset `1Dh) und `1Eh`: jeweils `FFh` gegenüber `00h`

Damit sind die im Referenz-Audit beschriebenen Strukturmerkmale in den deutschen Dateien reproduziert.

### 24.5 Aussagegrenze

Die vier Ressourcen besitzen die erwarteten Handle-Anzahlen und Flagfolgen; die zwei dokumentierten Objektpaare reproduzieren die Referenzunterschiede bytegenau. Das ist deutlich stärker als eine bloße Übereinstimmung der Protokollnummern.

Es ist dennoch kein vollständiger Bytevergleich gegen die ursprünglichen Referenzdateien, weil diese Referenzdateien hier nicht als Binärdateien vorliegen. Die neu berechneten Chunk-Hashes dokumentieren die konkrete deutsche Ausgangsbasis und können künftig als festes Zielprofil dienen. Die Laufzeitsemantik der kopierten privaten Objekt-Chunks ist damit nicht getestet.

### 24.6 Ergebnis Untersuchung 2263

1. `PROGRAMM.E/SPINTEXT.GEO` ist für R03/R04 der strukturell passende Kandidat; Größe, LMem-Headerwerte und Handle-Flags entsprechen dem Referenz-Audit.
2. VIEWER R0C/R1C besitzen die dokumentierten Handle-Anzahlen und Flagfolgen.
3. Die vom SDK verwendeten Handle-IDs sind vorhanden und ihre Chunkdaten wurden gehasht.
4. Die beiden bereits dokumentierten Bytevergleichspaare (VIEWER R1C und SPINTEXT R03) stimmen exakt mit den Referenz-Audit-Befunden überein.
5. Das deutsche Archiv ist daher ein plausibler Kandidat für ein separates SDK-Zielprofil, aber noch nicht als vollständig ABI-kompatibel oder laufzeitgetestet zertifiziert.

**Nächster Schritt 2264:** Einen separaten Zielprofil- und Archivadapter für `geoworks-1.2.8-de` entwerfen, ohne die strikten Standardhashes zu verändern. Vor einer Codeänderung werden die vom Generator verwendeten Chunk-Hashes und Metadaten als explizite Profil-Prüfwerte festgehalten. Anschließend erfolgt ein reiner Host-Build mit vollständigem Buildreport; die resultierende GEO-Datei wird nicht als laufzeitfähig bezeichnet, bevor der echte GEOS-Test erfolgt.


## 25. Untersuchung 2264 – Erster erfolgreicher Host-Build von `GEOTEST.GEO`

**Ergebnis:** Am 09.11.2026 wurde erstmals eine Datei `GEOTEST.GEO` aus dem SDK-0.1-Buildpfad erzeugt. Die Host-Kompilierung und das anschließende Packaging liefen ohne Fehler durch. Die Datei wurde danach erneut mit dem GEODE-Parser eingelesen und strukturell geprüft.

### 25.1 Verwendete Eingaben

- Projektname: `GeoWorks 1.x Test`
- permanent name: `geotest`
- application token: `GTS1`
- Ausgabe: `GEOTEST.GEO`
- Compiler: GCC 14.2.0, Linux, GNU binutils
- Projektquellen: minimales C-Testprogramm mit Init-, Draw-, Key- und Click-Callbacks; SDK-Runtime und nativer Adapter
- Zielvorlagen aus dem Nutzerarchiv:
  - SPINTEXT aus `GEOWORKS/WORLD/PROGRAMM.E/SPINTEXT.GEO`
  - NOTEPAD aus `GEOWORKS/WORLD/NOTEPAD.GEO`
  - VIEWER aus `GEOWORKS/WORLD/VIEWER.GEO`
  - TERM aus `GEOWORKS/WORLD/TERM.GEO`

Für den Host-Build wurde eine temporäre, normalisierte Kopie des Zielarchivs angelegt, die SPINTEXT unter dem vom SDK erwarteten Archivpfad `GEOWORKS/WORLD/EXTRAS/SPINTEXT.GEO` bereitstellt. Das Originalarchiv `GEOWORKS.zip` wurde nicht verändert. Im experimentellen Projekt war `allow_unknown_target=true` gesetzt, weil die vier Gesamtdatei-Hashes von den strikten SDK-0.1-Referenzhashes abweichen. Die in Untersuchung 2263 geprüften relevanten LMem-Ressourcen/Handles waren der Grund, diesen ausdrücklich experimentellen Versuch durchzuführen.

### 25.2 Wichtige Einschränkung der Reproduzierbarkeit

Die Buildlogik wurde anhand der im GitHub-Repository gelesenen SDK-0.1-Quelldateien in einem temporären lokalen Arbeitsverzeichnis rekonstruiert. Die Host-Toolchain und die Buildstufen entsprechen dem dokumentierten Ablauf (C nach Assembler, Instrumentierung, ELF-Objekte, nativer Adapter, Link, Ressourcenextraktion, Geode-Packaging und Reparse). Die temporär angelegten lokalen Dateien wurden jedoch nicht als byteidentischer Checkout des gesamten GitHub-Repositories verifiziert.

**Deshalb ist das Ergebnis ein erfolgreicher Host-Build mit der aus dem Repository rekonstruierten SDK-0.1-Buildlogik.** Ein erneuter Build aus einem byteidentischen Checkout des Repository-Commits ist noch offen. Es wurden keine SDK-Dateien im Repository verändert.

### 25.3 Buildresultat

| Eigenschaft | Ergebnis |
|---|---|
| Datei | `GEOTEST.GEO` |
| Dateigröße | 70.794 Bytes |
| SHA-256 | `9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b` |
| GEOS-Format | 1 |
| permanent name | `geotest` |
| Kernelprotokoll | 622.3 |
| UI-Import | `ui` 693.0 |
| Ressourcen | 12 |
| Relokationen | 41 |
| Code-Ressource | 1.397 Bytes |
| Engine-Nutzung | 7.692 Bytes |
| Toolchain | GCC 14.2.0 / GNU binutils |

Die 12 Ressourcen umfassen die vom SPINTEXT-Skelett übernommenen Ressourcen, die neu erzeugten UI-Ressourcen, die Code-Ressource und die angehängte Engine-Ressource. Der Parser hat die Ressourcen- und Relokationsgrenzen ohne Fehler akzeptiert.

### 25.4 Instrumentierungsbericht

| Quelldatei | Poll-Stellen | ursprüngliche Instruktionen | maximale lineare Lücke |
|---|---:|---:|---:|
| `app.c` | 12 | 42 | 8 |
| `sdk_runtime.c` | 33 | 124 | 8 |

Es wurden keine Repeat-Instruktionen aus dem C-Compiler-Ausgangscode expandiert.

### 25.5 Prüfergebnis und Aussagegrenze

**Bestätigt:**
1. Der C-Code ließ sich mit GCC in Assembler übersetzen.
2. Die instrumentierten Assemblerdateien ließen sich assemblieren.
3. Der native Adapter wurde assembliert.
4. Der ELF-Link und die Extraktion von Code-/Datenressourcen waren erfolgreich.
5. Der Geode-Packer erzeugte `GEOTEST.GEO`.
6. Der anschließende Parserlauf bestätigte Format 1, permanent name, Kernelprotokoll 622.3, UI-Import 693.0, zwölf Ressourcen und 41 Relokationen.

**Noch nicht bestätigt:**
- Der Build wurde noch nicht aus einem byteidentischen GitHub-Checkout wiederholt.
- Die Anwendung wurde noch nicht in GeoWorks 1.2 geladen.
- Fensteröffnung, Zeichenroutine, Tastatur, Maus, Help-Dialog, Schließen und erneuter Start wurden noch nicht getestet.
- Die private Runtime-/Scheduler-Brücke ist experimentell; der Host-Build beweist nicht ihre Laufzeitstabilität.

### 25.6 Artefakte und Schutz der Originaldateien

Die erzeugte Datei und Buildnachweise wurden im Arbeitsverzeichnis abgelegt:
- `GEOTEST.GEO`
- `GEOTEST_BUILD_REPORT.json`
- `GEOTEST_APP.map`
- `GEOTEST_SYMBOLS.txt`
- `GEOTEST_BUILD_EVIDENCE.zip`

**Die GEO-Datei und die Build-Evidence-ZIP werden nicht in das öffentliche GitHub-Repository hochgeladen**, weil die GEO-Datei UI-Vorlagenbytes aus der GeoWorks-Installation enthält. Das GitHub-Dossier enthält die Analyse, die Hashes und den Buildstatus, aber keine aus der proprietären Installation abgeleiteten Binärdateien.

**Nächster Schritt 2265:** Den Build aus einem byteidentischen Checkout des Repository-Standes reproduzieren und die Target-Profilprüfung in eine getrennte, explizite Profiloption überführen. Danach GEOTEST.GEO in einer gesicherten GeoWorks-1.2-Testinstallation starten und die Loader-/Laufzeitresultate protokollieren.


## 26. Untersuchung 2265 – GEOTEST-Quellprojekt und Zielarchiv-Vorbereitung veröffentlicht

Nach dem ersten Host-Build wurden die wiederverwendbaren, nicht-binären Projektbestandteile in das SDK-Repository aufgenommen.

### 26.1 Neu veröffentlichte Dateien

| Pfad | Inhalt |
|---|---|
| `tools/prepare_geoworks_1_2_8_de.py` | Prüft vier festgelegte Quell-GEO-Dateien anhand ihrer SHA-256-Werte und erstellt eine neue temporäre ZIP-Datei mit den vom SDK erwarteten Member-Pfaden. |
| `examples/geotest/project.json` | GEOTEST-Projektdefinition, permanent name `geotest`, Token `GTS1`. |
| `examples/geotest/src/app.c` | Minimale Anwendung mit Init-, Draw-, Key- und Click-Callbacks. |
| `examples/geotest/src/help.txt` | Help-Text der Testanwendung. |
| `examples/geotest/README.md` | Anleitung für Profilvorbereitung und Host-Build einschließlich der experimentellen Einschränkungen. |

Die Verzeichnisübersicht in der Repository-README wurde um `examples/geotest/` und `tools/` ergänzt.

### 26.2 Integritätsprüfung der veröffentlichten Quellen

Die lokalen Dateien für das Vorbereitungsskript, `project.json`, `app.c` und `help.txt` wurden mit Git-Blob-SHA-1 gegen die von GitHub zurückgelieferten Blob-SHAs verglichen. Alle vier Werte stimmen überein. Damit sind diese veröffentlichten Dateien byteidentisch mit den lokal getesteten Fassungen.

Die Vorbereitung wurde anschließend mit dem veröffentlichten Skript erneut ausgeführt. Es verifizierte die vier erwarteten SHA-256-Werte und erzeugte die normalisierte Zielarchivkopie. Ein erneuter Host-Build mit dieser Skriptausgabe ergab dieselbe GEOTEST-Dateigröße und denselben SHA-256-Wert wie der erste Versuch.

### 26.3 GitHub-Stand

Die neuen Dateien wurden einzeln auf `main` angelegt; die Repository-README wurde aktualisiert. Die Entwicklungsdokumentation bleibt unter:

`docs/GEOTEST_DEVELOPMENT_LOG.md`

Die erzeugte `GEOTEST.GEO`, die temporäre Zielarchivkopie und die Build-Evidence-ZIP wurden bewusst nicht in GitHub abgelegt. Die GEO-Datei enthält aus der GeoWorks-Installation übernommene UI-Vorlagenbytes.

### 26.4 Noch offene Reproduzierbarkeit

Die vier Projekt-/Vorbereitungsdateien sind byteidentisch bestätigt. Die übrigen lokal rekonstruierten Buildmodule (Parser, UI-Generator, Packer, Buildsystem und Runtime) wurden noch nicht als vollständiger byteidentischer Repository-Checkout nachgewiesen. Deshalb bleibt die Wiederholung des Builds mit einem unveränderten Checkout des GitHub-Repositorys der nächste zwingende Prüfschritt.

**Nächster Schritt 2266:** Die übrigen Buildmodule aus dem aktuellen GitHub-Stand byteidentisch in einer sauberen Arbeitskopie bereitstellen, ihre Git-Blob-SHAs gegen GitHub prüfen und den GEOTEST-Build erneut ausführen. Nur wenn der neue Build dieselbe strukturelle Prüfung besteht, wird der Host-Build als repository-reproduzierbar eingestuft. Danach folgt der Starttest in GeoWorks 1.2.


## 27. Untersuchung 2266 – Abgleich des ersten Host-Builds mit dem tatsächlichen GitHub-Quellstand

**Prüfziel:** Den in Untersuchung 2264 erzeugten Host-Build gegen den aktuellen Repository-Stand prüfen. Maßgeblicher Repository-Stand ist `main`, Commit `b57926472adc61f00d37091b192f0cb4080f3778`. Die GitHub-Blob-SHAs stammen aus dem rekursiven Git-Tree dieses Commits; lokale SHA-Werte wurden mit `git hash-object` aus den tatsächlich vorhandenen Dateien berechnet.

### 27.1 Projekt- und Hilfsdateien

Die folgenden Dateien sind byteidentisch mit dem veröffentlichten Repository:

| Datei | GitHub-Blob-SHA | Lokaler Git-Blob-SHA | Ergebnis |
|---|---|---|---|
| `examples/geotest/project.json` | `c3429f35346d472f149438ffac3b763bdfaf6d45` | `c3429f35346d472f149438ffac3b763bdfaf6d45` | identisch |
| `examples/geotest/src/app.c` | `c9d00f6447b2236007f660331be50e8d05a5cb2e` | `c9d00f6447b2236007f660331be50e8d05a5cb2e` | identisch |
| `examples/geotest/src/help.txt` | `77f4c315d6e7d7a4501b6804439f43e6e632a101` | `77f4c315d6e7d7a4501b6804439f43e6e632a101` | identisch |
| `tools/prepare_geoworks_1_2_8_de.py` | `2f1f4e68ba3b33534a830860c9ad5f6adedff91a` | `2f1f4e68ba3b33534a830860c9ad5f6adedff91a` | identisch |

Das belegt die Identität des veröffentlichten Projektbeispiels und des Zielarchiv-Vorbereitungsskripts. Es belegt noch nicht die Identität der Engine, die den ersten Build erzeugt hat.

### 27.2 Lokale Build-Engine gegenüber GitHub-HEAD

Die lokale Build-Arbeitskopie unter `/tmp/geotest-build` enthält mehrere Module, deren Git-Blob-SHAs von den Dateien im Repository abweichen:

| Datei | lokale Bytes | lokale SHA-1 | GitHub-Bytes | GitHub-Blob-SHA |
|---|---:|---|---:|---|
| `include/pcgeos1.h` | 937 | `36681d18efc8e7baea32d4a1bf14333a8228e968` | 1.259 | `517e32add9729a9dc3e3bc77a2b74a3acae3d611` |
| `pcgeos1/buildsys.py` | 3.853 | `432bd16526cdf441ab30c1e6514c4c724b0b4a97` | 4.285 | `583deef8ecc0d6adced661166671e8513d96eb01` |
| `pcgeos1/geode.py` | 3.966 | `0ee055adc9090b38f4b5dccb5c4c0397968c273b` | 5.535 | `dfbc196c8fa1a72115ffb1f920f6e3bc55276b95` |
| `pcgeos1/instrument.py` | 1.366 | `08514cc790575a2eb0a26523f759deb1b481675a` | 1.759 | `20ed6958a9c9fff84a5f81bc03a6feff847d2bf7` |
| `pcgeos1/packer.py` | 3.143 | `cd1ad6a86b27b7ca955f7e9ddca26563c2f03108` | 3.303 | `8f48c4f15c2ba86f8bf7ac3506445fe3e788d9b0` |
| `pcgeos1/target.py` | 1.728 | `eea4dee111f42b0bc8ed58699921324679d0ae44` | 1.986 | `f3b6a91470960dafbb7036832b32b7726daeef66` |
| `pcgeos1/toolchain.py` | 2.902 | `5dcb65c155eac6f338a5073748d3ffa3e1e9d65d` | 3.719 | `e1ec5ac88502107e5d75cac9489f9b4bc376b30b` |
| `pcgeos1/ui.py` | 3.238 | `ce1e8d8c7f695c91910b5d0651a3798373e47e1d` | 3.743 | `4a50f5e58cfc729c7eda993ab47461966862b51f` |
| `runtime/native.S` | 4.679 | `bdf6d851e2525661516d512257f27cf3057c2546` | 4.974 | `a561ab6b272ed1cd4f6674af5285a22030cbfc74` |
| `runtime/sdk_runtime.c` | 1.306 | `d0e4520817b6ad131b1b9a8c385327935bc08e29` | 1.342 | `0b8326d14ec284ea69d469f53f0189363896b297` |

Zwei weitere Dateien stimmen überein:
- `pcgeos1/__init__.py`: leer, Git-Blob-SHA `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`.
- `runtime/native.ld`: Git-Blob-SHA `26ed8ec12b705064eb8351647f4747ffe61bb4d8`.

### 27.3 Fehlende Bestandteile der lokalen Arbeitskopie

Im lokalen Arbeitsverzeichnis fehlen:
- `bin/sdkcli.py`, das vom veröffentlichten Starter `bin/pcgeos1` aufgerufen wird;
- `templates/basic_view/project.json`;
- `templates/basic_view/src/app.c`;
- `templates/basic_view/src/help.txt`.

Die veröffentlichten Dateien existieren im GitHub-Tree. Ihr Fehlen zeigt, dass `/tmp/geotest-build` kein vollständiger Checkout des Repositorys ist.

### 27.4 Abweichende tatsächlich kompilierte Anwendung

Die im Buildverzeichnis verwendete Datei `project/src/app.c` hat 498 Bytes und den Git-Blob-SHA `8dfc227e6b61888b568693c3e47dddf213a0c3d3`. Das veröffentlichte `examples/geotest/src/app.c` hat 519 Bytes und SHA `c9d00f6447b2236007f660331be50e8d05a5cb2e`.

Damit wurde beim ersten Host-Build nicht exakt die jetzt veröffentlichte Anwendungsquelldatei verwendet. Die veröffentlichte Projektdatei und Help-Datei sind zwar identisch, die C-Quelle ist es nicht.

### 27.5 Korrigierte Aussage zum ersten GEOTEST-Build

Der erste Build bleibt ein tatsächlich vorhandenes, 70.794 Bytes großes GEO-Artefakt mit dem in Untersuchung 2264 dokumentierten SHA-256. Seine strukturelle Prüfung bleibt ein gültiger Befund für genau diese Datei.

**Nicht belegt und ausdrücklich zurückgenommen ist die Aussage, der Build sei bereits aus dem aktuellen GitHub-Repository reproduzierbar.** Die lokale Engine, mehrere Runtime-Dateien, der Header, der UI-Generator und die tatsächlich kompilierte C-Datei weichen vom Repository-HEAD ab. Die Build-Arbeitskopie ist unvollständig.

Daher ist der erste Build als **experimenteller Vorab-Build mit einer lokalen SDK-Arbeitsfassung** zu kennzeichnen. Er darf nicht als Referenz-Build des veröffentlichten SDK gelten.

### 27.6 Keine Änderung an Originalen oder Binärartefakten

Bei dieser Untersuchung wurden weder `GEOWORKS.zip` noch `KERNEL.OLD`, die erzeugte `GEOTEST.GEO` oder die Dateien im GitHub-Repository verändert. Es wurden nur die Quellidentitäten und Dateigrößen geprüft. Die bereits veröffentlichten Quell-/Projektdateien bleiben unverändert.

### 27.7 Ergebnis Untersuchung 2266

1. Der veröffentlichte GEOTEST-Projektbaum und das Zielarchiv-Vorbereitungsskript sind byteidentisch mit den lokalen Projektfassungen.
2. Zehn zentrale Build-/Runtime-Dateien weichen vom GitHub-HEAD ab; zwei weitere stimmen überein.
3. Der lokale Build-Unterbau enthält nicht alle im Repository vorhandenen Dateien.
4. Die beim ersten Build verwendete C-Datei ist nicht identisch mit der veröffentlichten `examples/geotest/src/app.c`.
5. Der erste `GEOTEST.GEO`-Build ist real und strukturell geprüft, aber nicht als Build aus dem veröffentlichten Repository reproduzierbar.
6. Es ist erforderlich, eine saubere, vollständige Quellarbeitskopie aus Commit `b57926472adc61f00d37091b192f0cb4080f3778` aufzubauen und genau diese Buildkette erneut zu testen.

**Nächster Schritt 2267:** Die aktuelle Repository-Engine einschließlich `bin/sdkcli.py`, sämtlicher `pcgeos1/`-Module, `include/`, `runtime/` und `templates/basic_view/` als sauberen Quellstand bereitstellen. Danach `doctor`, Zielarchivvorbereitung, Parser-/Selftests und erst dann den GEOTEST-Build mit der veröffentlichten Projektdatei ausführen. Den alten GEO-Build getrennt als Vorab-Artefakt aufbewahren.


## 28. Untersuchung 2267 – Test-Gates und Selftest-Kompatibilität des deutschen Zielprofils

**Ziel:** Prüfen, ob die im Repository vorhandenen Tests mit dem in Untersuchung 2262/2263 ermittelten deutschen GeoWorks-1.2.8-Template-Satz arbeiten können. Maßgeblich sind `tests/selftest.py`, `tests/SELFTEST_RESULTS.json`, `pcgeos1/target.py`, `pcgeos1/buildsys.py` und die tatsächliche normalisierte Archivkopie `/tmp/geotest-build/GWP2-normalized-script.zip`.

### 28.1 Standard-Selftest verwendet strikt das bekannte Referenzprofil

Die veröffentlichte Funktion `tests/selftest.py:run()` ruft `load_templates(gwp)` ohne `strict=False` auf. Der Standardwert in `pcgeos1/target.py` ist `strict=True`. Anschließend wird das generische Beispiel `examples/hello` gebaut, dessen Projektdefinition keinen experimentellen Profilfreischalter setzt.

Der Standard-Selftest akzeptiert deshalb nur den in `KNOWN` festgelegten Vierer-Satz von Gesamtdatei-SHA-256-Werten. Er ist kein profilneutraler Parser- oder Laufzeittest.

### 28.2 Reproduzierter Hash-Gate-Test mit dem deutschen normalisierten Archiv

Die normalisierte Archivkopie enthält genau vier Mitglieder:

| Mitglied | Bytes | SHA-256 |
|---|---:|---|
| `WORLD/EXTRAS/SPINTEXT.GEO` | 3.748 | `18f2075c9d61fe7231b1dacae8c171e68c2028ef2fca6d40a6694158fdfcb9fd` |
| `WORLD/NOTEPAD.GEO` | 8.070 | `a1ebd0cb84712a126b1f67f5fd1ca6b57f8bda2e9038e9224ba16ebc008f9ea9` |
| `WORLD/VIEWER.GEO` | 59.984 | `c884b76cdc4f9119d4794f7830d5438e0abcc1d92d3cc248aa912bde85ed43e7` |
| `WORLD/TERM.GEO` | 63.718 | `a62ebc0fb3c01acb4b59c8172d20d520653822a6d42f0bec4831dfdb93e1cf3a` |

Der tatsächliche Aufruf von `load_templates()` mit Standardparametern bricht erwartungsgemäß beim ersten Template ab:

`Unsupported SPINTEXT.GEO: SHA-256 18f2075c...; SDK 0.1 knows 848f5afb...`

Der anschließende Aufruf mit `strict=False` parst alle vier Geodes erfolgreich; alle melden Kernelprotokoll `622.3`. Das ist eine Parser-/Formatprüfung, keine vollständige ABI-Freigabe.

### 28.3 Aussage der gespeicherten Selftest-Ergebnisse

`tests/SELFTEST_RESULTS.json` dokumentiert zwei Builds mit den vier unveränderten SDK-Referenzhashes:
- GCC 14.2.0: 70.954 Bytes, 12 Ressourcen, 41 Relokationen.
- Clang 17: 70.954 Bytes, 12 Ressourcen, 41 Relokationen.

Diese Ergebnisse sind wertvolle Referenzwerte für das Standardzielprofil. Sie sind nicht auf den deutschen Template-Satz übertragbar. Die erste GEOTEST-Datei mit 70.794 Bytes ist außerdem nicht mit diesen generischen Hello-Builds gleichzusetzen.

### 28.4 Absatz-/Relokationsregression

Das Repository enthält zusätzlich `tests/test_geode_alignment.py`. Der synthetische Test prüft, dass der Relokationsstrom nach der Absatzauffüllung und nicht direkt nach der unaufgefüllten Ressourcengröße gelesen wird. Er ist grundsätzlich unabhängig von den vier konkreten Template-Hashes.

**Prüfgrenze:** Der Test wurde in dieser Untersuchung nicht gegen einen byteidentischen Checkout des aktuellen Repositorys ausgeführt, weil die lokale Parserdatei laut Untersuchung 2266 nicht mit GitHub-HEAD übereinstimmt. Der Testcode und sein beabsichtigter Prüfgegenstand sind dokumentiert; ein bestandener Lauf des aktuellen HEAD wird hier nicht behauptet.

### 28.5 Konsequenz für ein sauberes Profil-Testdesign

Die Tests sollten künftig in drei Ebenen getrennt werden:

1. **Parser-/Formatregression:** synthetische GEODE-Header, Ressourcen- und Relokationsgrenzen; unabhängig vom Zielprofil.
2. **Profilintegrität:** exakte Vierer-Hashliste und Pfade für `geoworks-1.2.8-de`; Prüfung durch das bereits veröffentlichte Vorbereitungsskript.
3. **Build-/ABI-Test:** Build des GEOTEST-Projekts mit explizitem Profil und danach strukturelle Prüfung des Outputs. Die strikten Standard-Selftests bleiben unverändert auf dem bekannten Referenzprofil.

Ein globales Abschalten von Hashprüfungen ist ausdrücklich nicht vorgesehen. Der experimentelle GEOTEST-Projektparameter `allow_unknown_target=true` ist nur zusammen mit dem SHA-pinnenden Vorbereitungsprogramm akzeptabel.

### 28.6 Ergebnis Untersuchung 2267

1. Der Standard-Selftest ist absichtlich an die vier bekannten Referenzdatei-Hashes gebunden.
2. Das deutsche Zielarchiv scheitert deshalb erwartungsgemäß am strikten Hash-Gate.
3. Mit `strict=False` sind die vier normalisierten deutschen Geodes parsebar und melden Kernelprotokoll 622.3.
4. Die gespeicherten GCC-/Clang-Selftest-Ergebnisse gelten nur für das Standardzielprofil.
5. Der Absatz-/Relokationsregressionstest ist profilunabhängig, wurde hier aber nicht gegen einen byteidentischen GitHub-Checkout ausgeführt.
6. Standardprofil und deutsches Experimentalprofil müssen getrennte, ausdrücklich benannte Testpfade behalten.

**Nächster Schritt 2268:** Die vollständigen Quelltexte des aktuellen Repository-HEAD in einer sauberen Arbeitskopie bereitstellen und deren Git-Blob-SHAs vor dem Build prüfen. Dann zuerst den profilunabhängigen GEODE-Parser-Regressionstest und `doctor` ausführen, danach das deutsche Profil vorbereiten und den GEOTEST-Build mit exakt der veröffentlichten C-Quelle starten. Die Standard-Selftests bleiben unverändert und werden separat nur mit dem bekannten Referenzarchiv ausgeführt.


## 29. Untersuchung 2268 – Integritätsgrenze zwischen Zielarchiv-Vorbereitung und Buildsystem

**Ziel:** Prüfen, ob die in Untersuchung 2265 veröffentlichte Vorbereitung des deutschen Zielarchivs beim eigentlichen Build zwingend durchgesetzt wird oder nur eine dokumentierte Empfehlung ist. Untersucht wurden `tools/prepare_geoworks_1_2_8_de.py`, `examples/geotest/project.json`, `examples/geotest/README.md`, `pcgeos1/buildsys.py` und `pcgeos1/target.py` des GitHub-HEAD.

### 29.1 Schutzwirkung des Vorbereitungsskripts

Das veröffentlichte Skript prüft vor dem Schreiben:
- den exakten Archivmember für SPINTEXT unter `GEOWORKS/WORLD/PROGRAMM.E/SPINTEXT.GEO`;
- die drei festgelegten Mitglieder für NOTEPAD, VIEWER und TERM;
- den SHA-256-Wert jeder dieser vier Dateien.

Bei Abweichung bricht das Skript ab. Es schreibt anschließend eine neue ZIP-Datei mit den vom SDK erwarteten vier Zielpfaden. Das Originalarchiv wird nicht überschrieben.

**Gesichert:** Wird das Skript tatsächlich ausgeführt, ist die Eingabe der vier Templates auf die dokumentierten Hashes gepinnt.

### 29.2 Keine Verknüpfung zwischen Skript und Builder

Der Buildpfad in `pcgeos1/buildsys.py` ruft `load_templates(gwp, strict=not cfg.get('allow_unknown_target', False))` auf. Das Projekt `examples/geotest/project.json` setzt `allow_unknown_target=true`.

In `pcgeos1/target.py` bedeutet `strict=False), dass die SHA-256-Prüfung gegen `KNOWN` übersprungen wird. Der Builder prüft weiterhin:
- ob genau ein Archivmember pro erwarteter Endung vorhanden ist;
- ob die Geode-Datei vom Parser akzeptiert wird;
- ob ihre Strukturgrenzen plausibel sind.

Er prüft jedoch nicht, ob die vier Dateien zuvor vom veröffentlichten Vorbereitungsskript verifiziert wurden. Das Skript schreibt auch kein maschinenlesbares Profilmanifest in die ZIP-Datei, das der Builder anschließend validieren könnte.

### 29.3 Konsequenz

Die Dokumentation sagt, dass die Vorbereitungsroutine der erforderliche Eingangsschritt ist. Das Buildsystem erzwingt diesen Ablauf aber nicht. Wer `allow_unknown_target=true` verwendet, kann direkt ein beliebiges Archiv mit passenden Pfadnamen und parsebaren GEODE-Dateien übergeben.

Das ist keine Aussage, dass das aktuelle GEOTEST-Projekt tatsächlich mit beliebigen Dateien gebaut wurde. Es ist eine konkrete Integritätslücke in der technischen Durchsetzung der dokumentierten Profilregel.

### 29.4 Anforderungen an die Profilabsicherung

Ein sicherer Profilvertrag sollte mindestens enthalten:

1. **Profil-ID:** `geoworks-1.2.8-de`.
2. **Vier Quellpfade:** die tatsächlich geprüften Originalpfade.
3. **Vier SHA-256-Werte:** die Werte aus Untersuchung 2262.
4. **Vier normalisierte Zielpfade:** die vom Builder erwarteten Memberpfade.
5. **Parser-Mindestbedingungen:** GEOS-Format 1 und Kernelprotokoll 622.3; UI-Protokoll der tatsächlich verwendeten UI-Importe.
6. **Builder-Prüfung:** Der Build muss das Profilmanifest selbst lesen und alle Hashes erneut prüfen. Ein bloßer Schalter `allow_unknown_target` darf nicht als Ersatz dienen.
7. **Strikte Trennung:** Das unveränderte Standardprofil bleibt hashgebunden; das deutsche Profil wird als eigenes, explizit benanntes Experimentalprofil behandelt.

Ein Manifest kann als Sidecar-Datei oder als zusätzlicher Eintrag in der normalisierten ZIP-Datei abgelegt werden. Bei einer ZIP-internen Variante muss der Builder den Manifestinhalt selbst gegen einen im SDK hinterlegten erwarteten Profilhash prüfen, damit ein beliebig verändertes Manifest nicht als Vertrauensanker dient.

### 29.5 Ergebnis Untersuchung 2268

1. Das Vorbereitungsskript prüft die vier deutschen Template-Hashes korrekt, bevor es die normalisierte ZIP-Datei schreibt.
2. Der Builder weiß derzeit nicht, ob das Skript ausgeführt wurde.
3. `allow_unknown_target=true` schaltet die Template-Hashprüfung vollständig ab.
4. Die Build-README beschreibt einen zwingenden Vorbereitungsschritt, den die Build-Engine technisch nicht erzwingt.
5. Vor einer reproduzierbaren Freigabe des deutschen Zielprofils muss ein maschinenprüfbarer Profilvertrag in die Build-Engine integriert werden.
6. Die vorhandene GEOTEST-Datei bleibt ein experimenteller Vorab-Build; eine abgesicherte Profilprüfung ist noch nicht erfolgt.

**Nächster Schritt 2269:** Ein kleines, rückwärtskompatibles Design für `target_profile` erarbeiten: Standardprofil `geoworks-pro-1.2` bleibt unverändert; `geoworks-1.2.8-de` erhält eine eigene Hash-/Pfadmanifestdatei. Danach Unit-Tests für gültiges Profil, falschen Hash, fehlenden Member, doppelten Member und unbekannte Profil-ID ergänzen. Erst nach diesen Tests den deutschen GEOTEST-Build neu ausführen.


## 30. Untersuchung 2269 – Rückwärtskompatibles Design für explizite Zielprofile

**Ziel:** Aus der in Untersuchung 2268 festgestellten Integritätslücke einen konkreten, rückwärtskompatiblen Entwurf ableiten. Der Standardpfad für die bisherige GeoWorks-Pro-1.2-Referenz darf sich nicht ändern; das deutsche Zielarchiv erhält einen eigenen, expliziten Hashvertrag.

### 30.1 Projektkonfiguration

Das Projekt soll künftig ein benanntes Feld `target_profile` verwenden:

```json
{
  "sdk": "pcgeos1-sdk-0.1",
  "long_name": "GeoWorks 1.x Test",
  "permanent_name": "geotest",
  "token": "GTS1",
  "output": "GEOTEST.GEO",
  "target_profile": "geoworks-1.2.8-de"
}
```

Die bisherige Konfiguration ohne `target_profile` bleibt kompatibel und verwendet weiterhin das bisherige strikte Standardprofil. Das bisherige Feld `allow_unknown_target` darf künftig nicht mehr als Freischaltung für einen Build dienen. Für eine Übergangsphase muss es bei `true` mit einer eindeutigen Fehlermeldung abgelehnt werden, statt unbemerkt den Hashschutz zu umgehen.

### 30.2 Profilregister im SDK

Das SDK erhält ein zentrales, unveränderliches Profilregister:

| Profil-ID | Verwendungszweck | Hashprüfung |
|---|---|---|
| `geoworks-pro-1.2` | bisheriges SDK-0.1-Referenzset | vier bisherige `KNOWN`-Hashes |
| `geoworks-1.2.8-de` | deutsche GeoWorks-1.2.8-Installation | vier in Untersuchung 2262 verifizierte Hashes |

Beide Profile verwenden die vier vom Builder erwarteten normalisierten Memberpfade. Das Vorbereitungsskript für das deutsche Profil bleibt verantwortlich für die Auswahl der richtigen Originalpfade; der Builder kontrolliert danach die normalisierten Member anhand des Profilregisters erneut.

### 30.3 Prüfreihenfolge

Die Zielprofilprüfung muss vor Compilerstart und vor dem Erzeugen von Build-Artefakten erfolgen:

1. Projektdatei lesen und Profil-ID auflösen.
2. Unbekannte Profil-ID ablehnen.
3. Für jeden der vier erwarteten Member genau einen Archivtreffer verlangen.
4. SHA-256 jedes Members gegen den Hash des ausgewählten Profils prüfen.
5. GEODE-Datei parsen und GEOS-Format sowie Kernelprotokoll prüfen.
6. UI-Protokoll/Importe der tatsächlich verwendeten Ressourcen prüfen.
7. Erst nach erfolgreichem Abschluss die C-Kompilierung starten.

Damit kann ein falscher Hash nicht erst nach einem längeren Compilerlauf auffallen.

### 30.4 Keine frei editierbare Vertrauensliste im Projekt

Die Projektdatei darf keine beliebigen erwarteten Hashes definieren. Sonst könnte ein versehentlich oder absichtlich verändertes Projekt ein unbekanntes Template selbst als gültig erklären. Sie wählt nur eine Profil-ID; die zugehörigen Hashes liegen versioniert im SDK.

Das Vorbereitungsskript kann zusätzlich ein JSON-Protokoll ausgeben. Dieses dient der Nachvollziehbarkeit, ist aber nicht selbst die Vertrauensquelle. Die Build-Engine prüft die tatsächlichen ZIP-Mitglieder erneut gegen die im SDK hinterlegten Profilwerte.

### 30.5 Fehlerfälle und erwartete Reaktion

| Fehlerfall | Erwartetes Verhalten |
|---|---|
| Profil-ID fehlt | bisheriges striktes Standardprofil wählen |
| Profil-ID unbekannt | Build vor Compilerstart abbrechen |
| Member fehlt | Build vor Compilerstart abbrechen |
| doppelter Member-Endungstreffer | Build vor Compilerstart abbrechen |
| SHA-256 stimmt nicht | Build vor Compilerstart abbrechen |
| GEODE-Parserfehler | Build vor Compilerstart abbrechen |
| Kernelprotokoll ungleich 622.3 | Build vor Compilerstart abbrechen |
| altes `allow_unknown_target=true` | mit Migrationshinweis ablehnen |
| Standardprofil ausgewählt | bisherige Hashliste unverändert verwenden |

### 30.6 Testplan

Die Implementierung erhält profilbezogene Tests für:
- gültiges Standardprofil;
- gültiges deutsches Profil;
- falscher Hash im deutschen Profil;
- fehlendes Archivmitglied;
- doppeltes Mitglied;
- unbekannte Profil-ID;
- abweichendes Kernelprotokoll;
- Verbot des alten globalen Bypass-Feldes.

Zusätzlich bleiben die profilunabhängigen Parser-/Relokationsregressionen und die bestehenden Standard-Selftests erhalten.

### 30.7 Ergebnis Untersuchung 2269

1. Das bestehende Standardprofil bleibt der Default und wird nicht gelockert.
2. Das deutsche Zielset wird über die feste Profil-ID `geoworks-1.2.8-de` ausgewählt.
3. Hashwerte werden im SDK verwaltet, nicht in der Projektdatei.
4. Die Builder-Prüfung erfolgt vor Compilerstart und unabhängig davon, ob das Vorbereitungsskript zuvor ausgeführt wurde.
5. `allow_unknown_target` wird als globaler Hash-Bypass abgelöst und bei `true` künftig abgelehnt.
6. Die vier deutschen Hashes aus Untersuchung 2262 sind die vorläufigen Profilwerte; sie werden vor Implementierung noch einmal gegen das Nutzerarchiv und die normalisierte ZIP-Kopie geprüft.

**Nächster Schritt 2270:** Das Profilregister und die Prüfungen in `pcgeos1/target.py` implementieren, `buildsys.py` auf `target_profile` umstellen und `examples/geotest/project.json` aktualisieren. Dazu Unit-Tests für alle oben genannten Fehlerfälle ergänzen. Vor dem Commit muss der Testlauf mit dem echten deutschen Archiv bestanden sein; die unveränderte Standardhashliste ist als Regression zu sichern.


## 31. Untersuchung 2270 – Implementierung expliziter, hashgeprüfter Zielprofile

Die in Untersuchung 2269 festgelegte Profilarchitektur wurde im Repository umgesetzt.

### 31.1 Änderungen

- `pcgeos1/target.py`: Register mit `geoworks-pro-1.2` (Standard) und `geoworks-1.2.8-de` (experimentell) ergänzt. Beide Profile besitzen feste Hashlisten, GEOS-Format 1, Kernelprotokoll 622.3 und genau einen UI-Import mit Protokoll 693.0. `load_templates()` löst eine benannte Profil-ID auf und prüft jeden Memberhash sowie Format, Kernelprotokoll und genau einen UI-Import mit Protokoll 693.0.
- `pcgeos1/buildsys.py`: Projektfeld `target_profile` wird ausgewertet und im Buildbericht ausgewiesen. Das frühere `allow_unknown_target=true` wird mit einer Fehlermeldung abgelehnt.
- `examples/geotest/project.json`: Auswahl des deutschen Profils über `target_profile`; der globale Hash-Bypass ist entfernt.
- `examples/geotest/README.md`: Buildanleitung erklärt die doppelte Prüfung durch Vorbereitungsskript und Builder.
- `docs/TARGET_COMPATIBILITY.md`: Standard- und deutsches Profil sowie ihre Hashwerte dokumentiert.
- `tests/test_target_profiles.py`: acht Unit-Tests für gültiges Profil, falschen Hash, fehlendes/doppeltes Mitglied, unbekannte Profil-ID, falsches Kernelprotokoll, falsches UI-Protokoll und unveränderte Standardhashliste ergänzt.

### 31.2 Sicherheits- und Kompatibilitätsverhalten

Ein Projekt ohne `target_profile` verwendet weiterhin das bisherige strikte Standardprofil. Das deutsche Profil wird ausschließlich durch seine registrierte ID aktiviert. Die erwarteten Hashes können nicht aus der Projektdatei heraus überschrieben werden.

Die vier Dateien werden vor dem Start des Compilers geprüft. Das deutsche Vorbereitungsprogramm prüft weiterhin die Originalpfade; die Build-Engine prüft unabhängig davon die normalisierten Archivmember erneut.

### 31.3 Teststatus

Die acht Profiltests wurden in einer isolierten Testumgebung mit der exakt aus GitHub abgerufenen `target.py`- und Testdatei ausgeführt; alle acht Tests bestanden. Für diesen Unit-Testlauf wurde der GEODE-Parser bewusst gemockt, sodass er die Profilauflösung, Hash-/Member-Gates und Fehlerreaktionen isoliert prüft. Zusätzlich wurde die exakte GitHub-Fassung von `geode.py` in derselben Umgebung eingesetzt: Der reale normalisierte deutsche Archivsatz wurde mit dem echten Parser erfolgreich als GEOS-Format 1 mit Kernel 622.3 und genau einem UI-Import 693.0 je Datei durch das Profil `geoworks-1.2.8-de` geladen. Ein vollständiger Build aus einem byteidentischen Checkout des gesamten Repository-HEAD steht noch aus. Wegen der in Untersuchung 2266 festgestellten Abweichungen der vorhandenen lokalen Buildkopie wird kein bestandener Lauf behauptet.

**Nächster Schritt 2271:** Die neue Profilimplementierung aus dem GitHub-HEAD in eine saubere Arbeitskopie übernehmen und `tests/test_target_profiles.py`, `tests/test_geode_alignment.py`, `pcgeos1 doctor` sowie die deutsche Profilvorbereitung ausführen. Erst nach bestandenen Tests den GEOTEST-Build aus dem aktuellen Repository-Stand starten.


## 32. Untersuchung 2271 – Profiltests, Parserregression und reales deutsches Zielarchiv

Nach der Profilimplementierung wurden die neuen Prüfungen gezielt ausgeführt. Die Tests liefen mit den aus GitHub abgerufenen aktuellen Fassungen von `target.py`, `buildsys.py`, `geode.py` und `tests/test_target_profiles.py) in einer isolierten Arbeitsumgebung. Nicht benötigte Buildabhängigkeiten wurden für den Test des frühen Abbruchpfads durch Stubs ersetzt; es wurde damit kein vollständiger C-/GEO-Build ausgeführt.

### 32.1 Profil-Unit-Tests

**Ergebnis: 9 von 9 Tests bestanden.**

| Test | Ergebnis |
|---|---|
| Gültiges benanntes Profil | PASS |
| Falscher Template-Hash | PASS – wird abgelehnt |
| Fehlender Archivmember | PASS – wird abgelehnt |
| Doppelter Archivmember | PASS – wird abgelehnt |
| Unbekannte Profil-ID | PASS – wird abgelehnt |
| Falsches Kernelprotokoll | PASS – wird abgelehnt |
| Falsches UI-Protokoll | PASS – wird abgelehnt |
| Legacy-Bypass `allow_unknown_target=true` | PASS – Abbruch vor Archivzugriff und ohne Build-Ausgabeverzeichnis |
| Unveränderte Standardhashliste | PASS |

Der Test zum Legacy-Bypass importierte die aktuelle GitHub-Fassung von `buildsys.py`. Die Compiler-/Linkerabhängigkeiten wurden dabei absichtlich so gestubbt, dass jeder Aufruf dieser Komponenten den Test fehlschlagen lässt. Der Test beweist somit, dass die Legacy-Konfiguration vor Toolchain-Aufruf, Archivzugriff und Ausgabeerzeugung abgewiesen wird.

### 32.2 Parser-Absatz-/Relokationsregression

Der unveränderte Test `tests/test_geode_alignment.py` wurde mit der aus GitHub abgerufenen aktuellen `geode.py` ausgeführt:

`PASS: GEOS 1.x relocation stream starts after paragraph padding`

Damit ist der Regressionstest für die Absatzauffüllung im aktuellen Parser bestanden.

### 32.3 Reales deutsches Profil mit dem aktuellen Parser

Die aus GitHub gelesene aktuelle `target.py` wurde zusammen mit der aktuellen `geode.py` auf `/tmp/geotest-build/GWP2-normalized-script.zip` angewendet. Alle vier Dateien wurden gehasht und tatsächlich geparst:

| Datei | GEOS-Format | Kernel | UI-Import | Hashprüfung |
|---|---:|---:|---:|---|
| SPINTEXT.GEO | 1 | 622.3 | 693.0 | PASS |
| NOTEPAD.GEO | 1 | 622.3 | 693.0 | PASS |
| VIEWER.GEO | 1 | 622.3 | 693.0 | PASS |
| TERM.GEO | 1 | 622.3 | 693.0 | PASS |

Alle vier erwarteten SHA-256-Werte stimmten exakt mit dem registrierten Profil `geoworks-1.2.8-de` überein. Für jede Datei wurde genau ein UI-Import mit Protokoll 693.0 gefunden.

### 32.4 Grenzen dieses Testlaufs

- Die neun Unit-Tests decken Profilauflösung, Hash-/Memberfehler, Protokollprüfungen und den frühen Legacy-Abbruch ab.
- Der echte GEODE-Parser wurde zusätzlich auf alle vier Dateien des deutschen Zielarchivs angewendet.
- Der Parser-Absatzregressionstest ist bestanden.
- **Noch nicht ausgeführt** wurde der vollständige SDK-Build mit allen Buildmodulen aus dem aktuellen GitHub-HEAD. Die Abweichungen der früheren lokalen Buildkopie aus Untersuchung 2266 sind noch nicht vollständig beseitigt.
- Ein Start in GeoWorks 1.2 ist weiterhin offen.

### 32.5 Ergebnis Untersuchung 2271

1. Die neuen neun Profil-/Bypass-Unit-Tests bestehen.
2. Die Absatz-/Relokationsregression des aktuellen Parsers besteht.
3. Der aktuelle Parser akzeptiert alle vier echten deutschen Template-Dateien als GEOS-Format 1, Kernel 622.3 und UI 693.0.
4. Die Hashprüfung des deutschen Zielprofils stimmt für alle vier Mitglieder.
5. Der frühe Profil-/Legacy-Gate-Pfad ist getestet; die komplette Buildkette aus GitHub-HEAD ist noch nicht reproduziert.
6. Das Profil `geoworks-1.2.8-de` ist damit auf Ebene der vier geprüften Template-Dateien und des Parser-/Hash-Gates verifiziert, nicht aber als vollständige ABI- oder Laufzeitkompatibilität.

**Nächster Schritt 2272:** Den vollständigen GitHub-HEAD-Quellbestand in einer sauberen Arbeitskopie bereitstellen. Danach die echten Buildmodule ohne Stubs einbinden, `doctor` ausführen und einen Build mit `examples/geotest/project.json` plus dem frisch erzeugten Profilarchiv starten. Der resultierende GEO-Hash muss im Buildbericht und im Dossier festgehalten werden.


## 33. Untersuchung 2272 – GitHub-CI auf dem vollständigen Repository-Checkout

Zur Verifikation des tatsächlichen Repository-Stands wurde `.github/workflows/sdk-tests.yml` angelegt. Damit laufen die Quelltests direkt auf GitHub Actions gegen einen frischen Checkout des Repositorys und nicht gegen die frühere lokale Arbeitskopie.

### 33.1 Erster CI-Lauf und Korrektur

Der erste Lauf `42605385668` schlug beim Profiltest fehl, weil `tests/test_target_profiles.py` beim direkten Aufruf den Repository-Root nicht in `sys.path` eingetragen hatte. Die Python-Module selbst ließen sich kompilieren. Die Testdatei wurde daraufhin analog zu den übrigen Tests um die Root-Pfaderkennung ergänzt.

Der Fehler war ein Teststart-/Importpfadproblem, kein Fehler der Profilvalidierung.

### 33.2 Zweiter CI-Lauf

<badge color="success">GitHub Actions: success</badge>

- Workflow: `SDK source tests`
- Run-ID: `42605448481`
- Commit: `51ced54eb2b8e206aee07c706cc10861e6930491`
- Ergebnis: `completed / success`
- Lauf: https://github.com/JMGeithain/pcgeos-1-sdk/actions/runs/42605448481

Erfolgreiche Schritte:
1. Checkout des aktuellen Repository-Commits.
2. Python 3.12 bereitgestellt.
3. `python -m compileall -q pcgeos1 tests` – PASS.
4. `python tests/test_target_profiles.py` – PASS (neun Tests).
5. `python tests/test_geode_alignment.py` – PASS.

### 33.3 Aussagegrenze

Dieser CI-Lauf bestätigt, dass die aktuellen Python-Module syntaktisch kompilieren und die neun Profiltests sowie die Absatz-/Relokationsregression auf einem sauberen GitHub-Checkout bestehen.

Er baut noch keine `GEOTEST.GEO`-Datei. Das Workflow-Setup enthält absichtlich keine proprietäre GeoWorks-Zielinstallation und kann daher die vier deutschen Template-Dateien nicht bereitstellen. Die echte deutsche Profilprüfung wurde separat in Untersuchung 2271 mit dem Nutzerarchiv ausgeführt.

### 33.4 Ergebnis Untersuchung 2272

1. Die Testpipeline läuft auf dem tatsächlichen GitHub-Checkout.
2. Der anfängliche Importpfadfehler wurde behoben.
3. Der zweite CI-Lauf ist vollständig erfolgreich. Ein weiterer Lauf nach der Dossieraktualisierung war ebenfalls erfolgreich: Run-ID `42605505346`, Commit `4a7cf1a71313847bf9fb27ca645b850dbb34342b`.
4. Python-Compile, neun Zielprofiltests und GEODE-Absatzregression sind bestätigt.
5. Der vollständige Build der Anwendung mit dem gesamten aktuellen Repository-Stand und anschließend der Start in GeoWorks 1.2 bleiben die nächsten großen Meilensteine.

**Nächster Schritt 2273:** Den Build mit dem aktuellen GitHub-HEAD und dem frisch erzeugten Archiv `GWP2-profile-verified.zip` durchführen. Dafür muss der vollständige Quellbestand des Repositorys in der Buildumgebung liegen; die alte lokale SDK-Arbeitsfassung aus Untersuchung 2266 darf nicht wiederverwendet werden. Danach den resultierenden GEO-Hash, Ressourcen-/Relokationszahlen und alle Parserprüfungen protokollieren.


## 34. Untersuchung 2273 – Wiederholungsbuild mit rekonstruierter GitHub-Quellfassung

**Ziel:** Nach der Profil- und CI-Absicherung den ersten GEOTEST-Build erneut mit einer lokalen Arbeitsfassung aus den aktuell über GitHub gelesenen SDK-Quellen ausführen. Das deutsche Profilarchiv wurde zuvor frisch mit dem veröffentlichten Vorbereitungsskript erzeugt.

### 34.1 Verwendete Eingaben

- Projekt: `examples/geotest/project.json` aus GitHub, Profil `geoworks-1.2.8-de`.
- C-Quelle: veröffentlichte `examples/geotest/src/app.c`, 519 Bytes.
- Help-Datei: veröffentlichte `examples/geotest/src/help.txt`.
- Profilarchiv: frisch erzeugte `GWP2-profile-verified.zip`, vier Mitglieder mit den registrierten Hashes.
- Compiler: GCC 14.2.0 / GNU binutils.
- Build-Engine: aus den aktuellen GitHub-Dateiinhalten rekonstruierte lokale Arbeitsfassung.

### 34.2 Ergebnis des Wiederholungsbuilds

Der Build lief vollständig durch. Der Geode-Packer und der nachfolgende Parserlauf meldeten:

| Eigenschaft | Ergebnis |
|---|---|
| GEO-Dateigröße | 70.794 Bytes |
| SHA-256 | `9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b` |
| GEOS-Format | 1 |
| Kernelprotokoll | 622.3 |
| UI-Import | `ui` 693.0 |
| Ressourcen | 12 |
| Relokationen | 41 |
| Code-Ressource | 1.397 Bytes |
| Engine-Nutzung | 7.692 Bytes |

Der SHA-256-Wert ist exakt identisch mit dem ersten Host-Build aus Untersuchung 2264. Die aktualisierten Buildnachweise wurden in `/mnt/data/GEOTEST_BUILD_REPORT.json`, `GEOTEST_APP.map`, `GEOTEST_SYMBOLS.txt` und `GEOTEST_BUILD_EVIDENCE.zip` abgelegt. Der Bericht enthält nun ausdrücklich `target_profile=geoworks-1.2.8-de`.

### 34.3 Quellidentität – wichtige Einschränkung

Die lokalen Dateien wurden aus den über GitHub abgerufenen Quelltexten rekonstruiert. Beim abschließenden Git-Blob-Abgleich stimmten jedoch mehrere manuell übertragene Dateien nicht bytegenau mit ihren GitHub-Blob-SHAs überein. Das betrifft insbesondere die Engine-/Runtime- und Python-Moduldateien, bei denen Formatierung und Kommentare beim Übertragen verändert wurden. Die Projektdefinition, die C-Quelle, die Help-Datei und `runtime/native.ld` stimmten bytegenau überein.

**Folgerung:** Der identische GEO-Hash ist ein starker Reproduktionsbefund für die verwendete Buildlogik und die veröffentlichten GEOTEST-Eingaben. Er ist aber kein Beweis für einen Build aus einem byteidentischen GitHub-Checkout. Die Quellbyteidentität bleibt offen; der Build wird deshalb weiterhin als rekonstruierter experimenteller Host-Build gekennzeichnet.

### 34.4 CI-Stand

Der GitHub-Actions-Lauf auf dem aktuellen Repository-Checkout bleibt erfolgreich:
- Run `42605448481`: success, Commit `51ced54eb2b8e206aee07c706cc10861e6930491`.
- Run `42605505346`: success, Commit `4a7cf1a71313847bf9fb27ca645b850dbb34342b`.
- Run `42605807758`: success, Commit `8f312bfe027a5a32a955207d0393d6b5592e7cf7` (aktuellster Dossierstand).

Die CI führt Python-Compile, die neun Profiltests und die GEODE-Absatzregression aus. Sie führt keinen Build gegen die private GeoWorks-Installation aus.

### 34.5 Ergebnis Untersuchung 2273

1. Die frisch erzeugte Profilarchivkopie besteht die registrierte Hashprüfung.
2. Die veröffentlichte GEOTEST-Projektdefinition und die veröffentlichte C-/Help-Quelle wurden für den Wiederholungsbuild verwendet.
3. Der erzeugte GEO-Hash ist identisch mit dem ersten Build: `9ace19da...`.
4. Die strukturelle Prüfung bestätigt weiterhin 12 Ressourcen, 41 Relokationen, Kernel 622.3 und UI 693.0.
5. Die lokale Build-Engine ist noch nicht byteidentisch zum GitHub-HEAD; der Build gilt daher nicht als vollständig repository-reproduzierbar.
6. Ein Laufzeittest in GeoWorks 1.2 wurde weiterhin nicht ausgeführt.

**Nächster Schritt 2274:** Für die endgültige Quellreproduzierbarkeit muss eine echte, byteidentische Repository-Arbeitskopie bereitgestellt werden (z. B. durch einen vom Nutzer heruntergeladenen GitHub-Quellarchiv-Download). Danach alle Git-Blob-SHAs vor dem Build prüfen, den Build erneut ausführen und den resultierenden Hash mit `9ace19da...` vergleichen. Erst anschließend wird die GEOTEST-Datei in einer gesicherten GeoWorks-1.2-Installation gestartet.


## 35. Untersuchung 2274 – Korrektur der Prozessmethoden-Farzeiger-Auswertung

Ziel war, die Prozessmethodentabelle des SDK direkt mit BOUNCE.GEO und SPINTEXT.GEO aus GEOWORKS.zip zu vergleichen. Die erste Auswertung setzte den Beginn der Handler-Tabelle fälschlich zwei Bytes zu früh an. Dadurch wurde ein WORD aus dem vorangehenden Bereich als Teil des ersten Handlerdatensatzes fehlinterpretiert. Die daraus abgeleitete Änderung an pcgeos1/packer.py war falsch und wurde zurückgenommen.

### 35.1 Richtige Tabellenposition

Die Methodenzahl steht bei DGROUP+46h. Die Message-IDs beginnen bei DGROUP+52h. Der Handlerbereich beginnt unmittelbar danach bei:

pointer_table = 52h + 2 * method_count

Daraus folgt:

| Datei | Methodenanzahl | Handlerbereich | Erster Handler | Relokation |
|---|---:|---:|---|---:|
| BOUNCE.GEO | 7 | 0060h | 00 00 02 00 | 0062h |
| SPINTEXT.GEO | 8 | 0062h | 00 00 02 00 | 0064h |

Der erste Handlerdatensatz enthält zwei WORDs: Offset 0000h, danach Ressourcen-ID 0002h. Die Relokation 22 00 62 00 bei BOUNCE bzw. 22 00 64 00 bei SPINTEXT zeigt auf das zweite WORD, also die Ressourcen-/Segmentangabe.

Auch der jeweils nächste Handler bestätigt die Reihenfolge:
- BOUNCE: bei 0064h die Bytes 38 00 02 00; Relokation bei 0066h.
- SPINTEXT: bei 0066h die Bytes 38 00 02 00; Relokation bei 0068h.

Damit ist für diese beiden konkreten GeoWorks-1.x-Prozessklassen belegt: Offset-WORD zuerst, Ressourcen-WORD danach; Relokation auf das zweite WORD.

### 35.2 Bewertung des SDK-Packers

Der ursprüngliche SDK-Packer schrieb:
- zuerst den Codeoffset;
- danach Ressourcen-ID 2;
- die Relokation auf das zweite WORD.

Das entspricht exakt den beiden Originalvorlagen. Die in der ersten Fassung dieser Untersuchung behauptete Vertauschung war eine Folge der falschen Tabellenstartposition, nicht ein Fehler des Packers.

### 35.3 Zwischenzeitliche Änderung zurückgenommen

Die kurzzeitig eingebrachte Funktion write_process_methods() mit umgekehrter Wortreihenfolge wurde aus pcgeos1/packer.py entfernt. Der ursprüngliche Schreibpfad ist wiederhergestellt. Der zusätzlich angelegte Test tests/test_process_method_table.py prüfte die falsche Tabelleninterpretation und wurde deshalb entfernt. Der entsprechende CI-Schritt wurde ebenfalls zurückgenommen.

### 35.4 Build-Bewertung

Der Build mit SHA-256 3f72580d9a6f89bd2b99d01efb8fbc77f91bf49de520690c3a5c8b73759478aa wurde mit der falschen, zwischenzeitlichen Wortreihenfolge erzeugt und ist zu verwerfen.

Der frühere Build mit SHA-256 9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b wurde mit der ursprünglichen Packer-Reihenfolge erzeugt, die zum Bytebefund der beiden Originalvorlagen passt. Er bleibt der gültige experimentelle Host-Build-Kandidat, ist aber weiterhin nicht in GeoWorks 1.2 gestartet worden.

### 35.5 Ergebnis Untersuchung 2274

1. Die korrekte Position der Handler-Tabelle ist 52h + 2*method_count.
2. In BOUNCE.GEO und SPINTEXT.GEO ist der Handler als Offset-WORD, Ressourcen-WORD gespeichert.
3. Die Relokation liegt auf dem zweiten WORD.
4. Der ursprüngliche SDK-Packer entsprach diesem Layout; die zwischenzeitliche Korrektur war falsch.
5. Der Buildhash 3f72580d... wird verworfen.
6. Der Buildhash 9ace19da... bleibt als experimenteller Host-Build erhalten; Laufzeittest und byteidentischer GitHub-Build bleiben offen.

**Nächster Schritt 2275:** Den zurückgenommenen Packer-Stand und die CI-Datei im aktuellen Repository-HEAD prüfen, einen neuen CI-Lauf abwarten und anschließend die acht Handlerziele sowie den Einstiegspfad anhand der originalen Code-Ressourcen von BOUNCE.GEO und SPINTEXT.GEO weiter untersuchen.
 

## 36. Untersuchung 2275 – Regressionstest für die bestätigte Prozessmethoden-Struktur

Nach der Korrektur aus Untersuchung 2274 wurde die bestätigte Struktur nicht nur dokumentiert, sondern in eine kleine, direkt testbare Packer-Funktion überführt.

### 36.1 Implementierung

In pcgeos1/packer.py schreibt write_process_methods() nun die Prozessmethodentabelle:
- Methodenzahl nach DGROUP+46h;
- Message-IDs ab DGROUP+52h;
- Handler-Tabelle unmittelbar danach;
- pro Handler zuerst Codeoffset-WORD, danach Ressourcen-WORD (hier 2);
- Relokation 0x22 auf das zweite WORD jedes Handlerpaares.

Die Funktion weist fehlende Symbolnamen ab, bevor der Packer eine unvollständige Methodentabelle ausgibt.

### 36.2 Unit-Tests

tests/test_process_method_table.py prüft:
1. korrekte Methodenanzahl;
2. Message-ID-Werte und deren Position;
3. Handler-Pointer-Tabelle bei 52h + 2*method_count;
4. Reihenfolge (Codeoffset, Ressourcen-ID);
5. Relokation auf das zweite WORD;
6. Ablehnung eines fehlenden Handler-Symbols.

Der zuvor angelegte Test mit der falsch angenommenen Tabellenposition wurde entfernt. Der jetzt eingecheckte Test verwendet die in Untersuchung 2274 aus den Originaldateien abgeleitete Tabellenbasis.

### 36.3 Wiederhergestellter Host-Build

Die vorübergehend geänderte Wortreihenfolge wurde verworfen. Das ursprüngliche GEOTEST.GEO wurde aus der lokalen Arbeitskopie mit dem ursprünglichen Packer erneut als Referenz herangezogen und geprüft:

- SHA-256: 9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b
- Größe: 70.794 Bytes
- GEOS-Format: 1
- Kernel: 622.3
- UI-Import: ui 693.0
- Ressourcen: 12
- Relokationen: 41

Für alle acht Methoden wurde die tatsächliche Ausgabe geprüft. Die Handler-Tabelle beginnt bei 0062h; die Handlerzeiger enthalten jeweils Codeoffset, danach Ressourcen-ID 2. Die Relokation liegt jeweils auf dem Ressourcen-WORD, also beim ersten Eintrag bei 0064h. Alle acht Offsets liegen innerhalb der Code-Ressource mit 1.397 Bytes.

### 36.4 CI und Grenzen

Die GitHub-Actions-Pipeline wurde um tests/test_process_method_table.py ergänzt. Damit umfasst sie jetzt:
- Python-Compile;
- neun Zielprofiltests;
- zwei Prozessmethoden-Tests;
- GEODE-Absatz-/Relokationsregression.

GitHub Actions Run `42608173374` auf Commit `1b350e06e6d72cef80b47e207920d62e85572ac7` ist `completed / success`. Python-Compile, neun Zielprofiltests, zwei Prozessmethoden-Tests und GEODE-Absatz-/Relokationsregression bestanden. Ein weiterer Lauf auf dem aktuellen Dossier-Commit `329826541f6b21f5d31259df7379a3c5277f7578` (Run `42608436682`) ist ebenfalls `completed / success`. Der Host-Build ist weiterhin aus der rekonstruierten lokalen Buildkopie erzeugt; vollständige Byteidentität aller Quelldateien mit GitHub-HEAD ist nicht nachgewiesen. Ein echter Start in GeoWorks 1.2 steht weiterhin aus.

### 36.5 Ergebnis Untersuchung 2275

1. Die Prozessmethoden-Serialisierung ist nun gekapselt und unit-getestet.
2. Die geprüfte Struktur entspricht den Originaldateien BOUNCE.GEO und SPINTEXT.GEO.
3. Der alte Hash 9ace19da... bleibt der aktuelle experimentelle Host-Build.
4. Der zwischenzeitliche Hash 3f72580d... wird ausdrücklich verworfen.
5. Die CI prüft jetzt auch die Prozessmethoden-Struktur.
6. Die Anwendung ist noch nicht als startbar in GeoWorks 1.2 bestätigt.

**Nächster Schritt 2276:** Den CI-Lauf des aktuellen Repository-HEAD abwarten und danach die acht Handler-Eintrittspunkte sowie den Nachrichtenvertrag gegen die Disassemblierungen der originalen BOUNCE.GEO- und SPINTEXT.GEO-Code-Ressourcen vergleichen. Erst wenn diese Prüfung keine offenen ABI-Widersprüche zeigt, den Starttest in einer gesicherten GeoWorks-1.2-Installation vorbereiten.


## 37. Untersuchung 2276 – Statischer ABI-Abgleich der acht GEOTEST-Prozessmethoden

Ziel: Nach der bestätigten Farzeigerstruktur die acht in GEOTEST.GEO eingetragenen Message-IDs und Handler-Einstiegspunkte gegen die Originalanwendungen BOUNCE.GEO und SPINTEXT.GEO sowie die im SDK verwendeten 1.x-Nachrichtenverträge prüfen.

### 37.1 Referenzmethoden aus den Originaldateien

Die Methodeinträge von BOUNCE.GEO und SPINTEXT.GEO wurden aus DGROUP-Ressource 1 gelesen. Die jeweilige Code-Ressource ist Ressource 2. Die Einträge belegen die Lifecycle-/UI-Nachrichten:
- 0A01h – Open
- 0A03h – Close
- 0004h – Attach
- 0057h – View closed
- 0049h – Expose

Die Originaldateien enthalten darüber hinaus anwendungsspezifische Nachrichten 0C00h, 0C01h und in SPINTEXT 0C02h. Diese Werte sind nicht als allgemeine API-Nachrichten zu behandeln.

### 37.2 Weitere native Nachrichten

Der technische Bericht zum 1.x-Prozessklassenvertrag ordnet 007Bh der Tastaturbehandlung und 00C3h dem Start-Select-Pfad zu. Er beschreibt außerdem 0C00h ff. ausdrücklich als anwendungsspezifische Nachrichtengruppe, nicht als universelle API. ObjCallSuperNoLock ist im Zielkernel als Ordinal 01E9h dokumentiert; DS:DI bezeichnet die ClassStruct, AX die Nachricht. Die Close-Methode liefert CX=0, um keinen späteren State-Block in ein altes State-Format zu schreiben.

Diese Aussagen stützen die Auswahl der Message-IDs 007Bh und 00C3h im SDK. Die konkreten Registerübergaben bleiben zusätzlich anhand des jeweiligen Handlers und des tatsächlichen Laufzeitverhaltens zu prüfen.

### 37.3 GEOTEST-Methodentabelle

Die aktuelle GEOTEST-Datei enthält acht Einträge:

| Index | Message-ID | Handler | Codeoffset |
|---:|---:|---|---:|
| 0 | 0A01h | native_open | 002Fh |
| 1 | 0A03h | native_close | 0071h |
| 2 | 0004h | native_attach | 0068h |
| 3 | 0057h | native_view_closed | 0074h |
| 4 | 0049h | native_expose | 0089h |
| 5 | 00C3h | native_select | 00B1h |
| 6 | 007Bh | native_key | 00ECh |
| 7 | 0C0Ah | native_command | 0148h |

Alle acht Codeoffsets liegen innerhalb der 1.397 Bytes großen Code-Ressource. Die Methodentabelle verwendet die aus Untersuchung 2274 bestätigte Reihenfolge Offset-WORD, Ressourcen-WORD; alle Ressourcenrelokationen zeigen auf das zweite WORD.

### 37.4 Interner Abgleich des Help-Befehls

Die native Help-Trigger-Konstruktion in pcgeos1/ui.py setzt die Aktionsnachricht 0C0Ah. Der Prozesshandler native_command in runtime/native.S vergleicht AX ebenfalls mit 0C0Ah und führt nur für diesen Wert den Help-Aufruf aus.

Damit sind UI-Trigger und Prozesshandler auf denselben projektspezifischen Nachrichtenwert abgestimmt. Das bestätigt die interne Konsistenz der beiden SDK-Quellstellen. Ob der Nachrichtenempfänger und die konkrete UI-Interaktion im alten Laufzeitsystem korrekt sind, ist erst durch einen Starttest in GeoWorks 1.2 bewiesen.

### 37.5 ABI-Grenzen

- Die fünf Lifecycle-/View-Nachrichten werden durch die Originalanwendungen als native 1.x-Nachrichten belegt.
- Die Tastatur- und Start-Select-Nachrichten werden durch den dokumentierten 1.x-Prozessklassenvertrag gestützt.
- 0C0Ah ist eine private GEOTEST-Nachricht, die in UI-Trigger und Prozesshandler übereinstimmt; sie ist keine behauptete Standard-API.
- Die Methoden werden statisch an gültigen Codeoffsets gefunden. Das beweist weder, dass jede Methode im Laufzeitpfad aufgerufen wird, noch dass alle Register- und Superclass-Konventionen zur Laufzeit korrekt sind.
- Der native_open-Handler prüft CPU-Unterstützung und initialisiert den privaten Engine-Zustand; die Engine setzt 386+-Instruktionen voraus. Ein Lauf auf einem 8086/80286 ist nicht zugesichert.

### 37.6 Ergebnis Untersuchung 2276

1. Die acht GEOTEST-Handler sind in der Prozessmethodentabelle vorhanden und ihre Codeoffsets liegen innerhalb der Code-Ressource.
2. Die Lifecycle-/View-Message-IDs stimmen mit den untersuchten 1.x-Referenzanwendungen überein.
3. Tastatur 007Bh und Start Select 00C3h werden durch den dokumentierten 1.x-Prozessklassenvertrag gestützt.
4. Die private Help-Nachricht 0C0Ah ist zwischen UI-Trigger und Prozesshandler konsistent.
5. Die Farzeiger- und Relokationsstruktur entspricht den Originalvorlagen.
6. Die vollständige Nachrichten-ABI und der tatsächliche Fenster-/Input-Lebenszyklus bleiben bis zum GeoWorks-1.2-Lauftest offen.

**Nächster Schritt 2277:** Die vollständigen Methodenpfade von native_open, native_attach, native_view_closed und native_expose mit dem Originalkernel-Ordinal 01E9h und den Aufrufkonventionen abgleichen. Danach native_key und native_select einschließlich Rückgabewerten, Registererhalt und Superclass-Fallback prüfen. Die Laufzeitprüfung bleibt weiterhin zwingend.


## 38. Untersuchung 2277 – Superclass- und ObjMessage-Aufrufpfade

Ziel: Die in Untersuchung 2276 identifizierten Lifecycle- und Help-Handler auf die konkreten Kernelaufrufe zurückführen und gegen Originalcode aus GeoWorks 1.x vergleichen.

### 38.1 ObjCallSuperNoLock – Kernelordinal 01E9h

Der technische Bericht identifiziert ObjCallSuperNoLock im untersuchten 1.x-Zielkernel als Kernelordinal 01E9h. Der dokumentierte Aufrufvertrag verwendet DS:DI für die ClassStruct und AX für die Nachricht; die übrigen Nachrichtenargumente bleiben erhalten.

Im SDK-Assembler wird K 489 verwendet. 489 dezimal entspricht 01E9h. Die Handler native_open, native_attach und native_view_closed setzen DI auf 0040h und rufen anschließend diesen Kernelordinal auf.

Der Bytevergleich mit BOUNCE.GEO und SPINTEXT.GEO zeigt denselben Grundaufbau: DI wird auf 0040h gesetzt, danach folgt ein Far-Aufruf auf Kernelordinal 01E9h. Im Open-Pfad wird zuvor ES nach DS übernommen. Das SDK übernimmt diese Segmentvorbereitung ebenfalls in native_open. Damit ist der Superclass-Aufrufpfad nicht aus einer späteren GEOS-Version abgeleitet, sondern am Original-1.x-Code ausgerichtet.

Offen bleibt die Laufzeitbestätigung, dass DS beim Eintritt in native_attach und native_view_closed in allen relevanten Aufrufpfaden wie erwartet auf die Prozess-DGROUP zeigt. Die Originalhandler verwenden dieselbe implizite Segmentannahme; ein echter Starttest bleibt erforderlich.

### 38.2 Close-Rückgabe

native_close führt XOR CX,CX aus und kehrt mit RETF zurück. Der technische Bericht dokumentiert CX=0 für den alten Close-Handler als bewusste Begrenzung, damit kein späterer State-Block in ein altes State-Format geschrieben wird. Die Implementierung stimmt mit diesem dokumentierten 1.x-Verhalten überein.

### 38.3 Help-ObjMessage-Pfad

Der SDK-Help-Handler führt für Nachricht 0C0Ah folgende Folge aus:
1. SI erhält den Chunkoffset 00A0h (Help-Dialog).
2. AX erhält die UI-Nachricht 4197h.
3. BX wird mit 3 initialisiert (UI-Ressourcen-ID).
4. Kernelordinal 0096h wird aufgerufen.
5. DI erhält 8000h.
6. Kernelordinal 00A9h wird aufgerufen.

Der technische Bericht dokumentiert ObjMessage als Kernelordinal 00A9h und den synchronen Aufruf mit AX=Nachricht, BX=laufendem Blockhandle, SI=Chunk und DI=8000h. Das SDK folgt diesem dokumentierten ObjMessage-Aufbau.

Auch BOUNCE.GEO verwendet in seiner Code-Ressource die Sequenz BX=3, Kernelordinal 0096h, anschließend SI/AX setzen und Kernelordinal 00A9h aufrufen. Damit ist die zweistufige Auflösung der UI-Ressource vor ObjMessage im Original-1.x-Code belegt. Die genaue Semantik der UI-Nachricht 4197h und der Laufzeitempfänger des Help-Dialogs werden hier noch nicht als abschließend bewiesen bezeichnet.

### 38.4 Grenzen der Prüfung

- Der Aufruf von ObjCallSuperNoLock ist mit dem alten Kernelordinal und den Originalhandlern abgeglichen.
- Der Help-Aufruf verwendet die im 1.x-Bericht dokumentierte ObjMessage-Schnittstelle und eine auch in BOUNCE beobachtete Ressourcenauflösung.
- Die Nachrichten- und Registerwerte sind statisch nachvollzogen; Fensterlebenszyklus, GState-Gültigkeit, Fokus und tatsächliche Dialoganzeige wurden nicht zur Laufzeit beobachtet.
- Insbesondere native_select Rückgabewert AX=8000h und die vollständige Semantik der Start-Select-Nachricht bleiben Laufzeitprüfpunkte.
- Die 386+-Beschränkung der C-Engine bleibt bestehen; native_open überspringt die Engineinitialisierung, wenn die CPU-Prüfung fehlschlägt.

### 38.5 CI-Stand

GitHub Actions Run 42608561425 auf Commit e7c0fba03815d005db6f48e6c69350893ee530b2 ist completed / success. Python-Compile, neun Zielprofiltests, zwei Prozessmethodentests und die GEODE-Absatz-/Relokationsregression bestanden.

### 38.6 Ergebnis Untersuchung 2277

1. Die Superclass-Aufrufe der Lifecycle-Handler verwenden den für GeoWorks 1.x dokumentierten Kernelordinal 01E9h.
2. Der Open-/Attach-/View-Closed-Aufbau stimmt mit den untersuchten Originalhandlern überein.
3. Die Close-Rückgabe CX=0 entspricht dem dokumentierten alten Verhalten.
4. Der Help-Pfad verwendet ObjMessage über Kernelordinal 00A9h mit DI=8000h und die in BOUNCE beobachtete Ressourcenauflösung über 0096h.
5. Die konkrete Semantik von UI-Nachricht 4197h und die Laufzeitinteraktion bleiben offen.
6. Die Anwendung ist weiterhin nicht in GeoWorks 1.2 gestartet worden.

**Nächster Schritt 2278:** Die nativen Draw-/Expose-Aufrufe K 211, K 212, K 446 und K 447 sowie die in draw_native verwendeten Grafikordinale mit Original-1.x-Referenzcode abgleichen. Danach die Registerverträge von native_select und native_key einschließlich Rückgabewert und Superclass-Fallback prüfen. Erst danach ist ein kontrollierter Startversuch in der gesicherten GeoWorks-1.2-Installation sinnvoll.


## 39. Untersuchung 2278 – erster erfolgreicher GeoWorks-1.2-Laufzeittest

**Datum:** 2026-11-09  
**Testgegenstand:** `GEOTEST.GEO`, experimenteller Build mit SHA-256  
`9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b`  
**Testumgebung:** GeoWorks 1.x; im Screenshot sichtbare Titelleiste der Laufzeitumgebung: `KERNEL.EXE - 50000 Zyklen/ms - Übergangsloser Maus, Ctrl+F10 oder Mittelklick schaltet um`. Die genaue Kerneldatei-/Installationsvariante und deren Hash sind aus dem Screenshot allein nicht feststellbar.

### 39.1 Beobachtete Ergebnisse

Der Nutzer hat einen Screenshot aus dem laufenden GeoWorks-System übermittelt und den Test ausdrücklich mit „es geht alles“ bestätigt. Sichtbar sind:

1. Die GeoWorks-Arbeitsoberfläche mit geöffnetem Programmfenster `GeoWorks 1.x Test`.
2. Das GEOTEST-Hauptfenster mit schwarzem View-Bereich.
3. Der Menü-/Befehlseintrag `Help...`.
4. Der geöffnete native Help-Dialog mit Titel `Help for GeoWorks 1.x Test`.
5. Die Help-Inhalte:
   - `GEOTEST`
   - `Minimal GeoWorks 1.x SDK test application.`
   - `Click the view or press Enter to exercise an application callback.`
6. Die Dialogschaltflächen `Page Up`, `Page Down` und `Close` sind sichtbar.

### 39.2 Was damit als bestätigt gilt

- Die getestete `.GEO` wird vom vorliegenden GeoWorks-System geladen und gestartet.
- Die Anwendung erzeugt ein sichtbares Hauptfenster.
- Die native Help-Oberfläche wird geöffnet und zeigt den erwarteten Inhalt.
- Die sichtbare UI-Struktur und die Help-Texte stimmen mit dem vorgesehenen Minimaltest überein.
- Der Nutzer meldet, dass die Anwendung insgesamt funktioniert.

Dies ist der erste dokumentierte **erfolgreiche Laufzeittest einer mit diesem SDK erzeugten GEOTEST-Anwendung in GeoWorks 1.2**. Der Status wird damit von „nur Host-Build/strukturell geprüft“ auf „im Zielsystem gestartet und visuell bestätigt“ angehoben.

### 39.3 Was der Screenshot allein nicht beweist

Der Screenshot zeigt einen Zustand mit geöffnetem Help-Dialog. Er belegt für sich allein nicht jeden einzelnen Bedienpfad. Insbesondere sind folgende Einzelprüfungen nicht separat durch Video, Log oder weitere Screenshots dokumentiert:

- Klick in den View-Bereich und genauer Callback-Effekt;
- Enter-Taste und genauer Callback-Effekt;
- Page-Up-/Page-Down-Funktion;
- Schließen des Help-Dialogs über Close;
- Schließen der Hauptanwendung und saubere Rückkehr zum GeoManager;
- wiederholtes Öffnen/Schließen sowie Redraw nach Überdeckung.

Der Nutzer hat zwar insgesamt „es geht alles“ bestätigt; die obige Liste trennt dennoch die direkt sichtbaren Bildbelege von den nicht einzeln dokumentierten Interaktionen. Diese Punkte bleiben sinnvolle Regressionstestfälle für eine spätere, ausführlichere Testmatrix.

### 39.4 Artefakte und Lizenzgrenze

Der Test-Build besitzt weiterhin die oben genannte SHA-256-Prüfsumme und eine Dateigröße von 70.794 Bytes. Das SDK-Dossier und die Build-/Prüfberichte können die Struktur und Herkunft dokumentieren. Die proprietären GeoWorks-Templatebytes und die daraus abgeleitete `.GEO`-Binärdatei werden **nicht** in das öffentliche Repository eingecheckt. Das Repository erhält stattdessen Quellprojekt, reproduzierbare Buildanleitung, Prüfmetadaten und dieses Laufzeitprotokoll.

### 39.5 Korrigierter Gesamtstatus

| Prüfschritt | Status |
|---|---|
| Host-Build erzeugt | erfolgreich |
| GEODE-Struktur geprüft | erfolgreich: Format 1, 12 Ressourcen, 41 Relokationen, Kernel 622.3, UI 693.0 |
| Prozessmethodentabelle geprüft | erfolgreich; siehe Untersuchungen 2274–2275 |
| Hauptfenster in GeoWorks 1.2 | **erfolgreich sichtbar** |
| Help-Dialog in GeoWorks 1.2 | **erfolgreich sichtbar, erwarteter Text** |
| Nutzerbestätigung | **„es geht alles“ am 09.11.2026** |
| Byteidentität aller lokalen Buildquellen mit GitHub-HEAD | weiterhin nicht vollständig nachgewiesen |
| Vollständig reproduzierbarer Build aus sauberem GitHub-Checkout | weiterhin offen |
| Detaillierte Einzelprüfung aller Maus-/Tastatur-/Schließpfade | noch nicht separat protokolliert |

**Ergebnis:** GEOTEST 1.0 ist nicht länger nur ein experimenteller Host-Build. Der Nutzer hat die Anwendung erfolgreich in GeoWorks 1.2 gestartet und die sichtbare Hauptfenster-/Help-Funktion bestätigt. Die SDK-Dokumentation wird entsprechend aktualisiert; der Binärbuild selbst bleibt aus Lizenzgründen außerhalb des öffentlichen Repositories.

**Nächster Schritt 2279:** Die dokumentierte Laufzeitprüfung in eine reproduzierbare Test-Checkliste überführen. Danach gezielt View-Klick, Enter, Help-Schaltflächen, Dialog-Close und Anwendungs-Close prüfen und die Ergebnisse einzeln festhalten. Parallel die Quellbyteidentität des Builds mit einem sauberen GitHub-Checkout klären.


## 40. Untersuchung 2279 – GEOTEST-Programmsymbol (Token-Icon)

**Datum:** 2026-11-09  
**Eingabedatei:** `Testbild_48x30_16farben.pcx` (vom Nutzer bereitgestellt)  
**Bilddaten:** PCX, 48 × 30 Pixel, 16 Farben; verwendete Palettenindizes 0–15.  
**Zielanwendung:** `GEOTEST.GEO`, Token `GTS1`, Manufacturer-ID `0`.

### 40.1 Formatprüfung

Die PCX-Datei wurde gelesen und dekodiert. Das Bildmaß 48 × 30 und die 16-Farben-Palette entsprechen dem in der mitgelieferten GeoWorks-1.x-Dokumentation zu ICONMAKE beschriebenen EGA/VGA-Iconformat. Die PCX-Datei verwendet alle 16 Indizes. Deshalb wird bei der ICONMAKE-Konvertierung die Transparenz ausdrücklich ausgeschaltet (`m0`), damit kein tatsächlich verwendeter Farbindex ungewollt transparent wird.

### 40.2 Wesentliche Erkenntnis zur Einbindung

Das Programmsymbol wird bei GeoWorks 1.x nicht durch einfaches Anhängen einer PCX-Datei an die ausführbare `.GEO`-Datei eingebunden. Die sichtbaren Programm-Moniker werden über das Token-System bzw. die Token-Datenbank verwaltet. Die mit dem Nutzerarchiv vorhandene Dokumentation `ICONMAKE.DOC` (Marcus Gröber, ICONMAKE 1.0) beschreibt ausdrücklich den Erzeugungsweg über eine zusätzliche Token-Dummy-Datei. Die ebenfalls im Archiv enthaltene `ICONINST.TXT` bestätigt, dass eine solche Datei ein Token mit Icon bereitstellt und dass die Zuordnung über Token-Code und Manufacturer-ID erfolgt.

Die GEOTEST-Datei enthält bereits den Token-Code `GTS1` und die Manufacturer-ID `0` (Headerfelder ab Offset `0x14`). Daher muss das Icon für genau diesen Token erzeugt werden; ein anderes Token oder die Standard-ID 255 wäre nicht die korrekte Zuordnung.

### 40.3 Vorbereitete Konvertierung

Für das vom Nutzer bereitgestellte Bild wurden folgende Hilfsdateien erstellt:

- `GEOTEST_EGA.PCX` – unveränderte PCX-Bilddaten, umbenannt für den Konvertierungslauf;
- `ERZEUGE_ICON.BAT` – ruft `ICONMAKE m0 GTS1,0 GEOTEST_EGA.PCX` auf;
- `README_ICON_DE.txt` – beschreibt den 1.x-Tokenweg und die Installation;
- `GEOTEST.GEO` – unveränderte, zuvor erfolgreich getestete Anwendung.

Erwartete Ausgabe des originalen ICONMAKE-Programms ist `GTS10000.000` (Token `GTS1`, Manufacturer-ID 0). Diese Datei muss neben `GEOTEST.GEO` in den GeoWorks-WORLD-Ordner gelegt werden, damit GeoWorks den Token einlesen kann.

### 40.4 Status und offene Laufzeitprüfung

Die Bilddatei ist geprüft und die korrekte Token-Zuordnung aus dem GEOTEST-Header abgeleitet. Das Konvertierungs- und Installationspaket ist vorbereitet. **Die erzeugte `.000`-Token-Datei und die Anzeige des Icons im GeoManager sind noch nicht verifiziert**, da ICONMAKE hier nicht ausgeführt werden konnte. Deshalb wird nicht behauptet, dass das Icon bereits in GeoWorks angezeigt wird oder in die `.GEO`-Binärdatei selbst eingebettet wurde.

Nach Erzeugung der `.000`-Datei sind folgende Tests erforderlich:
1. Token-Dummy mit einem GEODE-Parser strukturell prüfen;
2. Datei neben `GEOTEST.GEO` in den Test-WORLD-Ordner kopieren;
3. GeoManager den Ordner neu einlesen lassen;
4. kontrollieren, ob das GEOTEST-Symbol im GeoManager angezeigt wird;
5. GEOTEST starten und prüfen, dass die Anwendung weiterhin unverändert funktioniert.

**Ergebnis:** Das Icon ist für das richtige GEOTEST-Token vorbereitet. Die abschließende Token-Erzeugung und der sichtbare GeoWorks-1.2-Nachweis stehen noch aus.


## 41. Untersuchungen 2360–2362 – ICONMAKE-Lookup und GEOTEST-LMem-Ressourcen

**Datum:** 10.11.2026  
**Geltungsbereich:** ausschließlich GeoWorks / PC/GEOS 1.x.  
**Eingabedatei:** Nutzerbereitgestellte `GEOTEST.GEO`, 70.794 Byte, SHA-256 `9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b`. Der Hash stimmt mit dem Buildbericht des Entwicklungspakets überein.

### 41.1 Untersuchung 2360 – ICONMAKE-Ressourcenblock-Lookup

Die Untersuchung der ICONMAKE-Seite ist bereits separat dokumentiert in [ICONMAKE_RESOURCE_BLOCK_LOOKUP_2360.TXT](ICONMAKE_RESOURCE_BLOCK_LOOKUP_2360.TXT). Sie belegt die Steuerkette aus den sechs Byte langen Datensätzen über Index und Zusatzoffset zur Lookup-Routine 1558h. Die konkreten 32-Bit-Tabelleneinträge und die daraus geladenen Bilddaten waren in dieser Untersuchung noch nicht vollständig aufgelöst.

### 41.2 Untersuchung 2361 – GEOTEST-Ressourcentabelle und Moniker-Kandidaten

Die GEOTEST-Ressourcentabelle enthält 12 Ressourcen. Für die Tabellenbereiche wurden folgende Startpositionen verifiziert:
- Größen: WORD-Feld ab 0x12E;
- Positionen: DWORD-Feld ab 0x146;
- Relokationsgrößen: WORD-Feld ab 0x176;
- Flags: WORD-Feld ab 0x18E.

Die Ressourcen 5–10 besitzen jeweils zwei LMem-Chunks. Ihre längeren Chunks beginnen mit:
- R5: `61 30 00 0E 00 1A`
- R6: `61 40 00 12 00 1A`
- R7: `41 30 00 1E 00 1A`
- R8: `46 30 00 1E 00 1A`
- R9: `41 40 00 28 00 1A`
- R10: `46 40 00 28 00 1A`

R7/R8 und R9/R10 bilden jeweils Paare mit gleichen dimensionartigen Zahlenfeldern. Die Zuordnung der Typbytes 0x41 und 0x46 zu Farbe bzw. Monochrom ist ausdrücklich noch nicht bewiesen. Details: [GEOTEST_UNTERSUCHUNG_2361.TXT](GEOTEST_UNTERSUCHUNG_2361.TXT).

### 41.3 Untersuchung 2362 – fünf LMem-Chunks in Ressource 4

Ressource 4 liegt bei Dateioffset 0x0D2E, ist 336 Byte groß und hat die Flags 0x145A. Ihre Handle-Tabelle enthält fünf Einträge:
- Handle 0x20 → Chunkoffset 0x2E, Länge 7;
- Handle 0x22 → Chunkoffset 0x36, Länge 200;
- Handle 0x24 → Chunkoffset 0xFE, Länge 44;
- Handle 0x26 → Chunkoffset 0x12A, Länge 10;
- Handle 0x28 → Chunkoffset 0x136, Länge 26.

Der letzte Chunk enthält den Text `GeoWorks 1.x Test`. Der 44-Byte-Chunk bei Handle 0x24 enthält sechs Vorkommen des WORD-Wertes 0x0022. Diese Werte sind lokale LMem-Chunk-Handles innerhalb von Ressource 4; Handle 0x22 verweist dort auf den 200-Byte-Chunk bei Offset 0x36. Sie sind keine Ressourcen-IDs 5–10.

Damit ist keine bytebelegte Referenzkette von Ressource 4 zu den sechs separaten Ressourcen 5–10 nachgewiesen. Die weiteren Felder des 44-Byte-Chunks bleiben semantisch unbenannt, bis eine passende GeoWorks-1.x-Strukturdefinition oder ein kontrollierter Vergleich vorliegt. Vollständige Bytebefunde: [GEOTEST_UNTERSUCHUNG_2362.TXT](GEOTEST_UNTERSUCHUNG_2362.TXT).

### 41.4 Status, Änderungen und nächste Schritte

- GEOTEST.GEO und die Originalarchive wurden nicht verändert.
- Quellcode und SDK-Generator wurden nicht geändert.
- Kein neuer Build und kein Laufzeittest im Rahmen dieser drei statischen Untersuchungen.
- TOKEN.DB blieb unangetastet.
- Die proprietäre GEOTEST.GEO-Binärdatei wird nicht in das öffentliche Repository übernommen.
- Die Untersuchungsprotokolle und die Zusammenfassung in `docs/GEOTEST_ICON.md` sind im Repository dokumentiert.

**Nächster Schritt 2363:** Die tatsächlichen ICONMAKE-Tabelleneinträge und die geladenen Datenblöcke vollständig rekonstruieren. Danach die native Moniker-Struktur der GEOTEST-Ressourcen 5–10 mit verifizierten GeoWorks-1.x-Referenzressourcen vergleichen. Erst auf dieser Grundlage die Farb-/Monochrom-Zuordnung und den tatsächlichen Auswahlpfad festlegen.


## 42. Untersuchung 2363 – Zuordnung der ICONMAKE-Provider-Iconvarianten

**Datum:** 10.11.2026  
**Geltungsbereich:** GeoWorks / PC/GEOS 1.x.

Die bereits extrahierten PAPR- und GDOC-Provider bestätigen unabhängig dieselbe Zuordnung ihrer Ressourcen R4–R6:

- R4: Präfixbyte 0x61, 48×14, PCX-Extraktion 1-Bit monochrom → CGA.
- R5: Präfixbyte 0x41, 48×30, PCX-Extraktion 1-Bit monochrom → HGC.
- R6: Präfixbyte 0x46, 48×30, PCX-Extraktion 4-Bit palettiert → EGA.

Die ICONMAKE-Datensätze übergeben die Tabellenindizes 6, 5 und 4 (jeweils mit Zusatzoffset 0x0022) an den Blocklader 1558h. Die Indizes sind mit der Reihenfolge der drei Providerklassen konsistent. Die unmittelbare 32-Bit-Tabellenauflösung zu absoluten Dateioffsets wurde in Untersuchung 2363 jedoch nicht erneut ausgeführt, da PAPR.000 und GDOC.000 in der aktuellen Arbeitsumgebung nicht als separate Originaldateien vorlagen. Die Index-zu-Klassen-Zuordnung wird daher als stark gestützt, aber noch nicht positionsgenau reproduziert geführt.

Wichtige Abgrenzung: GEODE-Ressourcenindex, ICONMAKE-Kontextindex und lokaler LMem-Chunk-Handle sind unterschiedliche Nummernräume. Die in GEOTEST.GEO untersuchten Ressourcen 5–10 dürfen nicht allein aufgrund ähnlicher Nummern oder Handlewerte als CGA/HGC/EGA klassifiziert werden.

Details und Beweisgrenzen: [ICONMAKE_PROVIDER_VARIANT_MAPPING_2363.TXT](ICONMAKE_PROVIDER_VARIANT_MAPPING_2363.TXT).

**Status:** Keine Originaldatei verändert, kein neuer Build, kein Laufzeittest, TOKEN.DB unverändert. Nächster Schritt 2364 ist die erneute Byteauflösung der absoluten Tabellenpositionen und geladenen Blöcke aus PAPR.000/GDOC.000; anschließend ist die unabhängige Dekodierung der GEOTEST-Ressourcen 5–10 fortzusetzen.


## 43. Untersuchung 2364 – PCX-Eingabedateien und Transparenzindizes

**Datum:** 10.11.2026  
**Geltungsbereich:** GeoWorks / PC/GEOS 1.x.

Die zwei vorbereiteten Dokumenticon-PCX-Dateien sind 48×30 Pixel, 1 Bit je Plane und vier Planes. Ihre vier Eckpixel tragen jeweils Palettenindex 14; damit passen die Eingabepixel zum dokumentierten Aufruf ICONMAKE M14, ohne dass die tatsächliche ICONMAKE-/GeoManager-Transparenz bereits getestet wäre.

Bei der älteren GTS1ICON.PCX liegt dagegen ein konkreter Widerspruch vor: Die vier Eckpixel tragen Index 13, während ERZEUGE.BAT ICONMAKE M14 aufruft. Die README behauptet zugleich, der Außenbereich sei Index 13 und werde transparent. Index 13 und 14 sind unterschiedliche Paletteneinträge. Die Datei wird nicht automatisch verändert; zuerst muss ICONMAKE 1.x auf einer gesicherten Kopie klären, welcher Index mit M14 tatsächlich transparent wird.

GEOTEST_EGA.PCX ist mit 8 bpp / einer Plane anders aufgebaut und hat keine einheitlichen Eckindizes (7 bzw. 9); laut README ist sie für den opaken M0-Weg vorgesehen.

Details: [GEOTEST_ICON_INPUT_AUDIT_2364.TXT](GEOTEST_ICON_INPUT_AUDIT_2364.TXT).

**Status:** Nur Eingabedateien gelesen und dekodiert. Keine PCX-/GEO-/Token-/TOKEN.DB-Änderung, kein ICONMAKE-Lauf, kein GeoWorks-Laufzeittest. Keine PC/GEOS-2.x- oder FreeGEOS-Definitionen verwendet.


## 44. Untersuchung 2365 – Widerspruch beim Transparenzindex

**Datum:** 10.11.2026  
**Geltungsbereich:** ausschließlich GeoWorks / PC/GEOS 1.x.

Die erneute PCX-RLE-Dekodierung ergab für `GTS1ICON.PCX` an allen vier Ecken den Palettenindex 13. Die Batchdatei ruft jedoch `ICONMAKE M14` auf; die zugehörige README behauptet zugleich, Index 13 werde transparent behandelt, während M14 Index 14 auswähle. Diese Angaben sind nicht widerspruchsfrei.

Die beiden Dokument-PCX-Dateien aus dem Paket 2305 haben an allen vier Ecken Index 14. Sie sind damit auf Dateiebene konsistent mit dem M14-Aufruf, was die tatsächliche Transparenzwirkung in ICONMAKE oder GeoManager aber noch nicht beweist. `GEOTEST_EGA.PCX` ist ein separates 8-bpp-/1-Plane-Format und wird laut Batchdatei mit M0 verarbeitet.

Original `ICONMAKE.EXE` liegt weiterhin nicht vor. Es wurde kein ICONMAKE-Lauf und kein GeoWorks-Laufzeittest durchgeführt. Keine PCX-, GEO-, Token- oder TOKEN.DB-Datei wurde verändert.

Details: [GEOTEST_ICON_TRANSPARENZ_WIDERSPRUCH_2365.TXT](GEOTEST_ICON_TRANSPARENZ_WIDERSPRUCH_2365.TXT).

**Nächster Schritt:** Original `ICONMAKE.EXE` aus der GeoWorks-1.x-Installation bereitstellen und M14/M0 an Kopien testen. Bis dahin keine Korrektur der Quelldatei oder Batchdatei vornehmen.


## 45. Untersuchung 2366 – exakte ICONMAKE-Providerblöcke und Transparenzparameter

**Datum:** 10.11.2026  
**Geltungsbereich:** ausschließlich GeoWorks / PC/GEOS 1.x.

Das erneut hochgeladene `GEOWORKS.zip` enthält die Originaldateien `ICONMAKE.EXE`, `PAPR.000` und `GDOC.000`. Der SHA-256-Wert von `ICONMAKE.EXE` stimmt mit dem zuvor analysierten Exemplar überein.

Die Disassemblierung bestätigt den Tabellenpfad: Routine 164Ch baut den Provider-Kontext und liest die Tabelle ab 012Eh; Routine 1758h löst den DWORD-Positionseintrag für den angeforderten Index auf, addiert den Zusatzoffset 0022h, liest den internen Offset 002Ah, die Blocklänge bei Basis+0028h und anschließend die Nutzdaten ab Basis+002Ah.

Exakte Tabellenbasen:
- PAPR.000: Index 4 = 03F4h, Index 5 = 0498h, Index 6 = 05ACh.
- GDOC.000: Index 4 = 03F4h, Index 5 = 0498h, Index 6 = 059Ch.

Die extrahierten Nutzdaten bestätigen:
- Index 4: CGA, Präfix 61h.
- Index 5: HGC, Präfix 41h.
- Index 6: EGA, Präfix 46h.

Damit ist die in Untersuchung 2363 noch offene absolute Offset-/Längenkette nun geschlossen. Die vollständigen sechs Blockpositionen, Längen und SHA-256-Werte stehen in [ICONMAKE_PROVIDER_EXACT_BLOCKS_2366.TXT](ICONMAKE_PROVIDER_EXACT_BLOCKS_2366.TXT).

Zusätzlich wurde der M-Modus untersucht: ICONMAKE liest den Dezimalwert hinter `M`; ohne Zahl wird 14 verwendet. Der Wert wird an die Iconvarianten-Erzeugung übergeben. Die vorhandene `GTS1ICON.PCX` hat jedoch Eckpixelindex 13, während `ERZEUGE.BAT` `M14` verwendet. Damit wählt der Batchaufruf nicht den tatsächlichen Randindex; für diese PCX-Eingabe wäre `M13` passend. Dies ist statisch aus Programmcode und PCX-Daten abgeleitet. Ein echter ICONMAKE-Lauf sowie die Anzeigeprüfung in GeoWorks 1.2 stehen noch aus. Batchdatei und README wurden deshalb nicht verändert.

**Status:** Originaldateien extrahiert und gehasht; sechs Providerblöcke positions- und längengenau aufgelöst. Keine PCX-, BAT-, README-, GEO- oder TOKEN.DB-Datei verändert. Kein ICONMAKE-Lauf und kein GeoWorks-Laufzeittest. Keine PC/GEOS-2.x- oder FreeGEOS-Definitionen verwendet.


## 46. Untersuchung 2367 – Prüfung der erzeugten GTS1-Token-Datei

**Datum:** 10.11.2026  
**Geltungsbereich:** ausschließlich GeoWorks / PC/GEOS 1.x.

Die vom Nutzer hochgeladene `GTS10000.000` ist 1.760 Byte groß (SHA-256: `7ea8625f66868038b3c1e7c99cc11c5134b8fa2b211b9b84c23767dd6e03b54f`). Der Header enthält Token `GTS1`, Manufacturer ID 0 und Creator `GEOS`; die Ressourcenzahl beträgt 7. Die Ressourcentabelle liegt vollständig innerhalb der Datei.

In den Ressourcen 4, 5 und 6 wurden die führenden Variantensignaturen 61h, 41h und 46h gefunden. Diese stimmen mit den in Untersuchung 2366 den Providerformaten CGA, HGC und EGA zugeordneten Signaturen überein. Ressourcen 4 und 5 sind jeweils nur 30h Byte groß; ohne vollständige Dekodierung werden sie nicht als vollständige Pixelbilder bezeichnet.

Die Datei enthält keinen erkannten eindeutigen Vermerk, ob sie mit M13 oder M14 erzeugt wurde. Deshalb lässt sich aus dieser Einzeldatei die verwendete Transparenzfarbe nicht sicher bestimmen. Für den Vergleich wird die zweite Token-Ausgabe aus dem jeweils anderen Testordner benötigt; außerdem muss bekannt sein, aus welchem Ordner die vorliegende Datei stammt.

Details: [ICONMAKE_TOKEN_OUTPUT_AUDIT_2367.TXT](ICONMAKE_TOKEN_OUTPUT_AUDIT_2367.TXT).

**Status:** Datei nur gelesen und gehasht. Keine Quelldatei, Token-Datei oder TOKEN.DB verändert. Kein Laufzeittest in GeoWorks 1.2.


## 47. Untersuchung 2368 – kontrollierter M13/M14-Tokenvergleich

**Datum:** 10.11.2026  
**Geltungsbereich:** ausschließlich GeoWorks / PC/GEOS 1.x.

Der Nutzer hat die Herkunft der beiden Token-Ausgaben bestätigt: `GTS10000(1).000` stammt aus dem M13-Testordner, `GTS10000(2).000` aus dem M14-Testordner.

Beide Dateien enthalten GTS1, Manufacturer ID 0, Creator GEOS und sieben Ressourcen. Die Ressourcen 1 bis 5 sind bytegenau identisch. Ausschließlich Ressource 6 (EGA-Payload) unterscheidet sich:
- M13: 0280h = 640 Byte
- M14: 02D0h = 720 Byte
- Differenz: M14 erzeugt 80 Byte mehr EGA-Payload.

Damit ist direkt belegt, dass der M-Parameter in diesen beiden Läufen den EGA-Ressourcenblock verändert. Zusammen mit dem zuvor statisch ermittelten Randindex 13 der Quelldatei ist M13 der passende Parameterkandidat für den transparenten Rand. Eine pixelgenaue Dekodierung und die sichtbare Transparenz in GeoManager sind damit noch nicht bestätigt.

**Status:** Beide Token-Dateien nur gelesen und verglichen. Keine PCX-, BAT-, README-, GEO- oder TOKEN.DB-Datei geändert. GeoWorks-1.2-Laufzeittest steht aus. Keine PC/GEOS-2.x- oder FreeGEOS-Definitionen verwendet.

Details: [ICONMAKE_M13_M14_TOKEN_COMPARISON_2368.TXT](ICONMAKE_M13_M14_TOKEN_COMPARISON_2368.TXT).


## 48. Untersuchung 2369 – Feldprüfung des EGA-Blocks

**Datum:** 10.11.2026  
**Geltungsbereich:** ausschließlich GeoWorks / PC/GEOS 1.x.

Ressource 6 beginnt in beiden Token-Dateien bei 03F4h; der EGA-Block beginnt ressourcenrelativ bei 002Ah. Die ersten sechs Blockbytes sind in M13 und M14 identisch (46 30 00 1E 00 1A). Das WORD bei Blockoffset +06h lautet bei M13 023Eh und bei M14 0290h (Differenz 82 Byte). Die äußeren Ressourcengrößen betragen 0280h bzw. 02D0h (Differenz 80 Byte).

Die beiden Längenfelder sind getrennt zu behandeln. Der Payload wurde noch nicht pixelgenau dekodiert; einzelne Bytes werden keiner Farb- oder Transparenzbedeutung zugeordnet. Dafür ist zunächst eine gesicherte PC/GEOS-1.x-Formatdefinition oder eine bestätigte Dekodierungsroutine erforderlich.

**Status:** Nur statische Byteprüfung. Keine Token-/GEO-/PCX-/BAT-/README-/TOKEN.DB-Datei geändert. Kein GeoWorks-Laufzeittest. Keine PC/GEOS-2.x- oder FreeGEOS-Definitionen verwendet.

Details: [ICONMAKE_EGA_BLOCK_FIELDS_2369.TXT](ICONMAKE_EGA_BLOCK_FIELDS_2369.TXT).
