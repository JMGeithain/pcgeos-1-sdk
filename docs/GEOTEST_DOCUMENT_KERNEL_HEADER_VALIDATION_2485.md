# GEOTEST – Untersuchung 2485

**Abgleich der Dokumentstruktur mit dem originalen GeoWorks-1.x-Kernel**  
Stand: 12.11.2026  
Primärquelle: `GEOWORKS/KERNEL.OLD` aus `GEOWORKS.zip`  
Zielprofil: ausschließlich GeoWorks / PC-GEOS 1.x

## 1. Ergebnis in Kürze

Im originalen deutschen GeoWorks-1.x-Kernel wurde ein Dateiprüfpfad gefunden, der die in den Untersuchungen 2482–2484 beobachtete Struktur direkt verwendet.

Der Kernel liest zunächst den 0xD0-Byte-Dateikopf. Er prüft:

- die Kennung `EB AD` bei Dateioffset `0xC8`;
- einen nicht-null WORD-Wert bei `0xCA`;
- einen DWORD-Wert bei `0xCC` als Dateioffset;
- anschließend 0x2C Bytes ab diesem Offset.

In diesem 0x2C-Byte-Block vergleicht er die Felder bei relativ `+0x26`, `+0x28` und `+0x2A` mit den drei WORDs aus dem Dateikopf bei `0xCA`, `0xCC` und `0xCE`. Damit ist die Rückreferenz bei Block+`0x28` nicht nur ein Muster aus Beispieldateien: Der Originalkernel prüft sie ausdrücklich gegen den Headerwert.

## 2. Primärquelle und Adressierung

Archivdatei: `GEOWORKS/KERNEL.OLD`  
Dateigröße: 72.688 Bytes  
MZ-Header: 0x600 Bytes

Die nachfolgenden Disassemblierungsadressen sind Dateioffsets. Der entsprechende Offset im MZ-Ladeabbild ist jeweils Dateioffset minus 0x600. Die Disassemblierung erfolgte als 8086-Code (`objdump -b binary -mi8086`). Die Befunde sind statische Codeanalyse, kein Laufzeit-Tracing.

## 3. Kernel-Prüfroutine bei Dateioffset 0xB62D

Der Code bei `0xB62D` reserviert einen lokalen Puffer und liest 0xD0 Bytes ab Dateiposition 0. Danach:

- ruft `0xB5E4` zur Prüfung der führenden Datei-Signatur/Versionsfelder auf;
- prüft WORD [Puffer+`0xC8`] auf `EB AD`;
- prüft WORD [Puffer+`0xCA`] auf ungleich 0;
- verwendet DWORD [Puffer+`0xCC`] als Position und liest ab dort `0x2C` Bytes;
- verlangt, dass WORD [Block+`0x18`] und WORD [Block+`0x1A`] zusammen nicht 0 sind;
- vergleicht WORD [Block+`0x26`] mit WORD [Header+`0xCA`];
- vergleicht WORD [Block+`0x28`] mit WORD [Header+`0xCC`];
- vergleicht WORD [Block+`0x2A`] mit WORD [Header+`0xCE`].

Bei Fehler setzt die Routine Carry und kehrt zurück.

Wichtige Disassembly-Auszüge (Dateioffsets):

```asm
0xB653: 81 7E F8 EB AD       cmp word [bp-08],0xADEB
0xB65A: F7 46 FA FF FF       test word [bp-06],0xFFFF
0xB675: 8B 56 FC             mov dx,[bp-04]
0xB678: 8B 4E FE             mov cx,[bp-02]
0xB680: 8D 96 04 FF          lea dx,[bp-00FC]
0xB684: B9 2C 00             mov cx,0x002C
0xB68E: 8B 86 1C FF          mov ax,[bp-00E4]
0xB692: 0B 86 1E FF          or ax,[bp-00E2]
0xB6A6: 8B 46 FA             mov ax,[bp-06]
0xB6A9: 8B 56 FC             mov dx,[bp-04]
0xB6AC: 8B 4E FE             mov cx,[bp-02]
0xB6AF: 3B 86 2A FF          cmp ax,[bp-00D6]
0xB6B5: 3B 96 2C FF          cmp dx,[bp-00D4]
0xB6BB: 3B 8E 2E FF          cmp cx,[bp-00D2]
```

Die lokalen Offsets ergeben sich aus dem Pufferlayout der Routine: Der 0xD0-Byte-Headerpuffer beginnt bei BP-0xD0; der 0x2C-Byte-Zielblock beginnt bei BP-0xFC. Die Vergleiche entsprechen daher Zielblock+`0x26`, +`0x28` und +`0x2A`.

## 4. Zusammenhang mit den Dokumentdateien

Die in Untersuchung 2484 festgestellte Struktur passt exakt zu den Kernel-Prüfungen:

- Dateikopf+`0xC8` enthält `EB AD`.
- Dateikopf+`0xCA` enthält den nicht-null WORD-Wert.
- Dateikopf+`0xCC` enthält den DWORD-Dateioffset des Zielblocks.
- Zielblock+`0x28` enthält denselben Offset (untere WORD-Hälfte).
- Zielblock+`0x2A` enthält die obere WORD-Hälfte (bei den bisher betrachteten kleinen Dateien typischerweise `0000`).
- Zielblock+`0x26` spiegelt den WORD-Wert aus Dateikopf+`0xCA`.

Die 418 gültigen Archivfälle aus Untersuchung 2483 zeigen diese Rückreferenz bereits in den Bytes; der Kernelcode bestätigt, dass sie aktiv geprüft wird.

## 5. Kernel-Erzeugungspfad bei Dateioffset 0xB6D5

Im selben Codebereich liegt eine Routine ab `0xB6D5`, die eine neue interne Struktur initialisiert. Der Code:

- reserviert/initialisiert einen Bereich;
- schreibt `FB 00` an den Anfang;
- schreibt `0x46` in das WORD-Feld bei relativ +`0x16`;
- setzt das Byte bei relativ +`0x1C` auf 0;
- ruft weitere interne Routinen auf;
- schreibt `EB AD` in das WORD-Feld bei relativ +`0x24`;
- aktualisiert einen Zähler bei DS:`0x10`.

Ein weiterer Pfad ab `0xB76F` setzt Felder zurück und schreibt ebenfalls `EB AD` bei relativ +`0x24`. Das ist ein deutlicher Hinweis, dass FB00/EBAD zu einer vom Kernel verwalteten Struktur gehören. Die exakte Bedeutung der Struktur und ihrer Felder ist mit diesem Ausschnitt noch nicht vollständig bestimmt.

Auszug:

```asm
0xB6EB: C7 06 00 00 FB 00   mov word [0],0x00FB
0xB6F4: B8 46 00            mov ax,0x0046
0xB6FB: A3 16 00            mov [0x16],ax
0xB6FE: C6 06 1C 00 00      mov byte [0x1C],0
0xB709: 89 35               mov [di],si
0xB70B: C7 45 04 EB AD      mov word [di+4],0xADEB
0xB7DE: C7 06 24 00 EB AD   mov word [0x24],0xADEB
```

## 6. Was jetzt als gesichert gelten kann

- `EB AD` bei Header+`0xC8` ist ein vom Kernel ausdrücklich geprüfter Marker.
- DWORD bei Header+`0xCC` wird als Dateiposition verwendet, von der `0x2C` Bytes gelesen werden.
- Zielblock+`0x28`/+`0x2A` muss exakt auf den Header-DWORD zurückverweisen.
- Zielblock+`0x26` muss den Header-WORD bei +`0xCA` spiegeln.
- Der Kernel enthält einen Initialisierungspfad, der `FB 00` und `EB AD` in einer internen Struktur schreibt.

## 7. Was weiterhin offen ist

- Symbolischer Name und vollständige Semantik der Struktur.
- Bedeutung von Header-WORD+`0xCA` (es wird als nicht-null geprüft und in Block+`0x26` gespiegelt).
- Bedeutung von Blockfeldern +`0x18`/+ `0x1A` (nur gemeinsam auf nicht-null geprüft).
- Bedeutung der Felder +`0x14`, +`0x16`, +`0x1C`, +`0x24` und der weiteren Variablenfelder.
- Ob und wie die Initialisierungsroutine bei `0xB6D5` unmittelbar einen neuen Dokument-/VM-Header erzeugt oder Teil eines größeren Kernel-Objektpfads ist.
- Welche weiteren Schritte erforderlich sind, um daraus eine vollständige, gültige Datei zu erzeugen.

## 8. Konsequenz für GEOTEST

Die bisherige Annahme, dass der DWORD bei Header+`0xCC` eine Länge sein könnte, ist endgültig zu verwerfen: Der Kernel behandelt ihn als Dateiposition und liest dort den Zielblock.

GEOTEST darf den Header nicht mit einem geratenen Block erzeugen. Der sichere nächste Schritt ist, den Aufrufer-/Funktionskontext der Kernelroutinen und die weiteren Routinen um `0xB62D`/`0xB6D5` zu verfolgen, um den vollständigen Erzeugungs- und Schreibpfad zu verstehen.

Noch kein Dokument-Erzeugungscode und keine neue GEOTEST.GEO wurden gebaut.

## 9. Nächster Schritt 2486

Untersuchen, welche Kernel-Aufrufer die Prüfroutine bei `0xB62D` und den Initialisierungspfad bei `0xB6D5` aufrufen. Dazu Call-Sites im Originalkernel erfassen und den umgebenden Dateiverwaltungs-/VM-Pfad weiterverfolgen. Anschließend mit GeoWrite-/GeoDraw-Programmcode vergleichen, ohne PC/GEOS 2.x-Semantik zu übernehmen.

## 10. Grenzen

Statische Disassemblierung des originalen deutschen `KERNEL.OLD` aus dem bereitgestellten `GEOWORKS.zip`. Keine dynamische Tracing-Sitzung, kein Eingriff in das Originalarchiv, kein Laufzeittest und keine neue GEOTEST.GEO.
