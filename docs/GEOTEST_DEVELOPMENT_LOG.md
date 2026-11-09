# GEOTEST.GEO – Entwicklungsprotokoll

**Projekt:** erste ausführbare Testanwendung für GeoWorks 1.2 / PC/GEOS 1.x  
**SDK:** `JMGeithain/pcgeos-1-sdk`, Zweig `main`, SDK 0.1  
**Protokollstand:** 2026-11-09  
**Status:** Statische Analyse und Build-Vorbereitung; `GEOTEST.GEO` ist noch nicht erfolgreich kompiliert oder zur Laufzeit getestet.

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
| Untersuchung 2249 | Schreibzugriffe auf `05B8h/05BAh` vollständig verglichen; Offset-/Segment-Paar nachgewiesen |
| Untersuchung 2250 | DI-Aufrufvarianten und unterschiedliche Rückgabekanäle verglichen; keine einheitliche Callback-Signatur unterstellt |
| Untersuchung 2251 | Überlappende Segmentladehelfer analysiert; DS/ES in den untersuchten Callback-Pfaden auf `0E35h` zurückgeführt |
| Untersuchung 2252 | Listenanker `05AEh`, Kopf-Link `05B2h`, Statusfelder und zweites Far-Zeigerpaar untersucht |
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
