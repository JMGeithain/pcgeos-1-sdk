# GEOTEST / PC-GEOS 1.x – Untersuchung 2470
## Breiter GEODE-1-Vergleich: Klasse 0 / Typ 0 über das GEOWORKS-Archiv
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Ziel
Die in Untersuchung 2469 festgestellte Zuordnung der Relokationsrecords `source=0, type=0` zu CALL-FAR-Offsetoperanden sollte über weitere Original-GEODEs des Archivs überprüft werden. Zusätzlich sollte verhindert werden, dass mehrfach vorhandene Kopien derselben Datei die Gesamtzahlen künstlich erhöhen.

## 2. Archivumfang und Prüfverfahren
Archiv: vom Nutzer bereitgestelltes `GEOWORKS.zip`, 22.190.788 Byte.
Im Archiv wurden 263 Dateipfade mit Endung `.GEO` gefunden.

Prüfung:
- GEODE-Format-1-Signatur `C7 45 CF 53`;
- Header-, Ressourcen- und Relokationstabellen nach dem im Repository vorhandenen Parser-Schema ausgelesen;
- Relokationsrecord `info=0x00` als `source=0`, `type=0` ausgewählt;
- für jeden Treffer wurde das Byte unmittelbar vor dem 16-Bit-Offsetoperand kontrolliert;
- Datei-Duplikate anhand SHA-256 zusammengefasst.

Ergebnis der Dateiprüfung:
- 253 Dateipfade ließen sich mit dem hier verwendeten Format-1-Prüfer vollständig parsen.
- 221 unterschiedliche Binärdateien (SHA-256) sind darunter enthalten.
- 7 weitere Dateien mit Format-1-Signatur wurden wegen nicht erfüllter Tabellen-/Ressourcen-/Relokationsgrenzen nicht in die Statistik aufgenommen. Das bedeutet nicht automatisch, dass die Dateien defekt sind; sie benötigen eine gesonderte Format-/Parserprüfung.
- 3 weitere `.GEO`-Pfade besitzen nicht die Format-1-Signatur und wurden nicht als GEODE-1-Dateien gezählt.

Die Statistik umfasst somit ausschließlich die 221 eindeutig unterschiedlichen, erfolgreich geprüften GEODE-1-Binärdateien.

## 3. Gesamtergebnis über eindeutige Binärdateien
In den 221 unterschiedlichen geprüften GEODE-1-Dateien wurden gefunden:
- 79.138 Relokationsrecords insgesamt;
- 35.250 Records mit `source=0, type=0`.

Bei **allen 35.250 von 35.250** Treffern liegt die Relokationsstelle unmittelbar hinter dem Opcode `0x9A`. Das ist die Offsetposition im Maschinenformat `CALL FAR ptr16:16`.

Der Befund aus 2469 wird damit auf eine breite Stichprobe aus dem GEOWORKS-Archiv ausgeweitet. Es ist kein Einzelfall von DBASE.GEO, UI.GEO oder ICON-ED.GEO.

## 4. Repräsentative System- und Anwendungsdateien
Beispiele aus dem geprüften Archiv:
| Datei | Klasse 0 / Typ 0 |
|---|---:|
| DBASE.GEO | 67 |
| UI.GEO | 1.125 |
| ICON-ED.GEO (separat geprüfte Kopie aus 2469) | 48 |
| KLIB.GEO | 743 |
| GROBJ.GEO | 813 |
| EGA.GEO | 45 |
| SVGA8004.GEO | 45 |
| DOS5.GEO | 130 |
| GEOPLAN.GEO | 673 |
| WRITE.GEO | 833 |
| VIEWER.GEO | 562 |

Die Tabelle ist eine Auswahl von Beispielen, keine vollständige Dateiliste. Manche Dateinamen liegen in mehreren Archivpfaden; die Gesamtstatistik verwendet SHA-256-Deduplizierung.

## 5. Wichtige Einschränkung: Offset und Segment sind getrennte Operanden
Die Analyse bestätigt die Position des Records, aber sie beweist nicht, dass der Aufruf stets in dieselbe Ressource oder dasselbe Segment zeigt.

Innerhalb der 35.250 Klasse-0/Typ-0-Records der 221 eindeutigen Binärdateien:
- 34.750 Offsetwerte liegen numerisch unterhalb der Größe der Quellressource.
- 500 Offsetwerte liegen nicht unterhalb der Größe der Quellressource.
- 294 Far-Aufrufe besitzen an ihrem Segmentwort einen nichtnulligen Literalwert.

Diese Zahlen sind reine Byte-/Tabellenbefunde. Ein Offsetwert außerhalb der Größe der Quellressource ist nicht automatisch ungültig: Das Ziel kann zu einem anderen Segment-/Ressourcenkontext gehören. Ebenso darf ein nichtnulliges Segmentliteral nicht als absolute Laufzeitadresse interpretiert werden, solange die Loaderregeln nicht geklärt sind.

## 6. Interpretation – belastbare und offene Aussagen
### Belastbar
1. Im untersuchten Bestand markiert `source=0, type=0` durchgängig das 16-Bit-Offsetfeld einer `CALL FAR`-Instruktion.
2. Der Befund wurde in 221 unterschiedlichen GEODE-1-Binärdateien und 35.250 Relokationsrecords bestätigt.
3. Das Segmentwort ist ein separater Operand und wird durch diese Records nicht separat markiert.
4. Die Zielauflösung kann nicht allein aus dem 16-Bit-Offsetwert abgeleitet werden.

### Weiterhin offen
- Welche konkrete Veränderung der Loader am Offsetoperand vornimmt;
- wie das Segmentwort zur Laufzeit festgelegt oder interpretiert wird;
- ob die Relokationsquelle `0` in anderen Code-/Datenkontexten eine weitere Bedeutung besitzt;
- wie die 7 nicht vollständig parsebaren Format-1-Dateien zu behandeln sind;
- welche Beziehung zwischen diesen Far-Aufrufen, Exporttabellen und Ressourcensegmenten besteht.

Daher wird `source=0, type=0` noch nicht als „interner Aufruf“, „Kernel-Aufruf“ oder „Exportaufruf“ benannt. Bewiesen ist nur die Maschinenoperand-Position.

## 7. Konsequenz für das SDK
Für den GEODE-Parser ist eine optionale Diagnose sinnvoll:
- wenn `source=0, type=0` und das Byte bei `offset-1` gleich `0x9A` ist, kann der Report den Fund als `CALL FAR offset operand` markieren;
- wenn die Byteprüfung nicht passt, bleibt der Record neutral und wird nicht semantisch umgedeutet.

Diese Regel ist eine statische Annotation, keine neue Loadersemantik. Der Parser und Packer wurden in dieser Untersuchung nicht geändert.

## 8. Nächste Untersuchung 2471
1. Die 294 nichtnulligen Segmentliterale aus den eindeutigen Dateien extrahieren und nach wiederkehrenden Werten, Ressourcen und Modulen gruppieren.
2. Die 500 Offsetwerte außerhalb der Größe ihrer Quellressource einzeln klassifizieren.
3. Exporttabellen und Ressourcen-IDs der betroffenen GEODEs vergleichen.
4. Die 7 nicht vollständig parsebaren Format-1-Dateien gesondert prüfen.
5. Erst danach eine engere Hypothese zur Relokationswirkung formulieren.

## 9. Änderungsstatus
- `GEOWORKS.zip` nur gelesen.
- Keine GEO-Datei im Archiv verändert.
- TOKEN.DB nicht verändert.
- SDK-Quelldateien und GEOTEST.GEO nicht verändert.
- Kein Build und kein Emulator-Laufzeittest.
