# GEOTEST – TOKEN.DB: Feldvergleich der frühen Tokenfolge und Provider-Daten (2426)

Stand: 2026-11-12  
Geltungsbereich: originales GeoWorks / PC/GEOS 1.x; ausschließlich statische Analyse.  
Datei: `GEOWORKS/SYSTEM/TOKEN.DB`  
Größe: 952.688 Byte  
SHA-256: `c7fa3d51c9bdce14b988d20fd8ed57ac7da9837803090ac858990613ec53ae35`

## 1. Ziel

Untersuchung 2425 zeigte, dass die Einträge im VM-Block `0080h` nicht alle gleich weit auseinanderliegen. Diese Untersuchung vergleicht daher nicht nur Tokenanfänge, sondern die konkreten Bytes hinter den Tokens. Ziel ist, den gemeinsamen Eintragskopf von den variablen Nutzdaten zu trennen.

## 2. Gemeinsamer Eintragskopf

Für die frühen Einträge und die Provider-Tokens ist das folgende acht Byte lange Muster reproduzierbar:

| Relativer Bereich | Länge | Beobachtung |
|---|---:|---|
| +0 bis +3 | 4 | Tokenzeichen |
| +4 bis +5 | 2 | Herstellerwort (z.B. 0000h oder 00FFh) |
| +6 bis +7 | 2 | konstantes Wort `0074h` (Bytes `74 00`) |

Unmittelbar danach folgt ein 16-Bit-Kennwert. Beispiele:

- `DP00 00 00 74 00 36 00`
- `DDAT 00 00 74 00 3A 00`
- `WP00 00 00 74 00 46 00`
- `WDAT 00 00 74 00 4A 00`
- `gDOC FF 00 74 00 9C 01`
- `PAPR FF 00 74 00 DC 01`

Das Wort `0074h` ist in diesen Beispielen konstant. Seine Bedeutung ist weiterhin offen. Es wird deshalb hier neutral als **Konstantfeld 0074h** bezeichnet, nicht als Handle, Größe oder Typ-ID.

## 3. Variable Nutzdaten nach dem Kennwert

Nach dem Kennwert unterscheiden sich die folgenden Bytes deutlich. Einige Beispiele aus dem Rohdatenstrom:

### 3.1 Generische Einträge

`DESK` bei Blockoffset `0060h`:

```
44 45 53 4B 00 00 74 00 0E 00
00 00 00 00 00 00 00 00 00 00 ...
```

`FILE` bei `00ACh`:

```
46 49 4C 45 00 00 74 00 16 00
00 00 00 00 00 00 00 00 00 00 ...
```

Diese beiden Beispiele enthalten nach dem Kennwert zunächst überwiegend Nullbytes.

### 3.2 Anwendungsspezifische Einträge

`DP00` bei `018Ch`:

```
44 50 30 30 00 00 74 00 36 00
00 00 00 00 FF FF FF FF D2 38 00 00
98 00 01 00 05 00 F8 00 FD 1F 00 00 ...
```

`WDAT` bei `0216h`:

```
57 44 41 54 00 00 74 00 4A 00
00 00 00 00 00 32 00 00 00 00 00 00
C0 34 01 00 05 00 28 01 FD 1F 00 00 ...
```

Die variablen Felder enthalten nicht nur Nullbytes. Ohne Kenntnis des Datensatzschemas werden die 16-Bit-Werte nicht als Ressourcenhandles oder Offsets benannt.

### 3.3 Provider-Einträge

`gDOC` bei `0A58h`:

```
67 44 4F 43 FF 00 74 00 9C 01 00 00
00 0C 0C 00 0C 0F 07 70 00 7F FC FF 00 00 ...
```

`PAPR` bei `0BF6h`:

```
50 41 50 52 FF 00 74 00 DC 01 00 00
00 1E 00 1A 0C 02 30 00 1E 00 01 11 00 00 ...
```

Die Nutzdaten dieser Provider-Einträge unterscheiden sich sichtbar von den weitgehend leeren generischen Einträgen. Die Bytes enthalten wiederkehrende kleine Werte und Muster, die mit Grafik-/Monikerdaten vereinbar sein können. Das ist aber noch keine Dekodierung: Weder Pixelraster noch Bilddimensionen oder ein Verweis auf einen externen VM-Block sind für diese Nutzdaten hier bewiesen.

## 4. Wichtige Folgerung

Der Datensatz kann nicht als bloße Liste aus Token + ID behandelt werden. Hinter dem gemeinsamen Kopf folgen variable Daten, die je nach Eintrag sehr unterschiedlich ausfallen. Bei Provider-Einträgen ist der Nutzdatenbereich deutlich gefüllt; bei generischen Einträgen ist er teilweise weitgehend null.

Das eröffnet zwei mögliche Untersuchungsrichtungen, ohne eine davon vorwegzunehmen:

1. Die Daten nach dem Kennwert könnten den Token direkt beschreibende Metadaten enthalten.
2. Ein Teil der Daten könnte eingebettete Icon-/Monikerinformationen oder Verweise auf solche Daten enthalten.

Beides muss durch Feldgrenzen, bekannte Formatheader und Vergleich mit den zugehörigen Provider-Geodes belegt werden.

## 5. Keine vorschnelle Deutung des Kennwerts

Die Folge `0036h, 003Ah, 003Eh, 0042h, 0046h, 004Ah` und später `0160h, 0164h, 0168h...` zeigt regelmäßige +4-Schritte. Das ist ein starker Hinweis auf eine geordnete Kennung oder Indexfolge. Es beweist aber nicht, dass diese Werte Handles oder Zeiger auf Icon-Ressourcen sind.

Die bisherigen VM-Blockhandles der Moniker-Kandidaten (u.a. `00BCh`, `03D4h`, `0470h`, `0DF4h`) stimmen nicht einfach mit den hier sichtbaren Kennwerten überein. Eine direkte Gleichsetzung ist deshalb nicht gerechtfertigt.

## 6. Nächster Schritt (2427)

1. Provider-Geodes `PAPR.000` und `GDOC.000` mit den zugehörigen TOKEN.DB-Nutzdaten vergleichen.
2. Prüfen, ob die Nutzdaten im Datenbankblock mit den bekannten Moniker-Headern (CGA/HGC/EGA-Merkmale, 48×14 bzw. 48×30) übereinstimmen.
3. Den Datenbereich jedes Eintrags bis zum nächsten sicher identifizierten Eintragsanfang abgrenzen.
4. Nach internen Längen-/Formatkennungen suchen, statt die Daten pauschal als Pixel oder Handles zu behandeln.
5. Erst bei bytegenauer Übereinstimmung oder einer bestätigten Referenzregel eine Icon-Verknüpfung behaupten.

## 7. Sicherheit / Reproduzierbarkeit

Die Untersuchung basiert auf Rohbytes der unveränderten TOKEN.DB mit dem oben genannten Hash. Die Datei wurde nicht verändert. Keine GEOS.INI-Änderung, kein Provider-Installationsversuch, kein GEOTEST-Build und kein Laufzeittest wurden durchgeführt.
