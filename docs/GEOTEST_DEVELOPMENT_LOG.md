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

Vor der Fortsetzung bleibt noch die Adressnotation der Arbeitsnotiz 2245 zu klären. Im reproduzierten Disassembly erscheinen die korrespondierenden Stellen als `10B20h`, `10B6Fh`, `10CAC h` und `10CC5h`; `10BD0h` liegt innerhalb einer Instruktion und ist kein Instruktionsanfang. Deshalb dürfen die verkürzten Angaben `0B20h`, `0BD0h`, `0CACh` und `0CC5h` nicht ungeprüft als gleichbedeutende Labels verwendet werden. Insbesondere ist `10B20h` zunächst nur ein Disassembly-Offset; seine Funktion als Code oder Daten muss anhand der Aufrufer und Kontrollflussreferenzen bestimmt werden. Der konkrete Bytekontext zeigt bei `10B18h` ein `ret`; ab `10B1Ah` folgen zunächst Wortwerte (`22 12`, `2B 12`, `34 12`, `3D 12`) und anschließend ASCII-ähnliche Dateinamenfragmente (`dos2.geo`, `dos3.geo`, `dos4.geo`, `dos5.geo`, `drdos.geo`). Die lineare x86-Disassemblierung ab `10B20h` interpretiert diese Daten zwangsläufig als Instruktionen; `10B20h` darf daher nicht ohne Kontrollflussbeleg als Codeeinstieg gelten. Bei `10B6Fh` liegt ein fünf Byte langer Far-Aufruf (`lcall $0x0,$0x399`), danach folgt bei `10B74h` `mov $0x19,%ax`; die frühere Notiz „elf Bytes kopiert“ ist durch diesen Ausschnitt nicht bestätigt und muss separat geklärt werden. Die inklusive Spanne `10B6Fh–10B75h` umfasst sieben Bytes, nicht elf. `10BD0h` liegt innerhalb der Instruktion ab `10BCFh` (`lcall *0x5b8`) und ist kein gültiger Instruktionsanfang.

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
| Untersuchungsnotiz 2245 | teilweise korrigiert durch Untersuchung 2246; `10B20h` als Codeeinstieg verworfen |
| Originalkernel-Body | aus `GEOWORKS/KERNEL.OLD` extrahiert; SHA-256 exakt bestätigt |
| Originaldisassemblierung | mit objdump neu erzeugt; SHA-256 exakt bestätigt; 53/53 Anker vorhanden |
| Untersuchung 2246 | Daten-/Codegrenze und Codekandidat `10B53h–10BD6h` statisch untersucht; Funktionsvertrag offen |
| Untersuchung 2247 | Querverweise und Aufrufziele `0399h`, `2588h`, `101CBh` untersucht; DS-Segmentkorrektur dokumentiert |
| Untersuchung 2248 | Wiederholte `05B8h`-Far-Aufrufe verglichen; gemeinsame Dispatch-Schnittstelle als Hypothese markiert |
| GEOTEST-Projektdateien | noch nicht erzeugt |
| GEOTEST.GEO | noch nicht gebaut |
| strukturelle GEO-Prüfung | ausstehend |
| Start in GeoWorks 1.2 | ausstehend |


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
