# GEOTEST – DESKTOPG.GEO: Zuordnung der Dateiverwalter-Strings zu Ressourcen und Code (2383)

Stand: 2026-11-10

## Ziel und Abgrenzung

Untersuchung ausschließlich GeoWorks / PC/GEOS 1.x. Ziel bleibt `GEOTEST.GEO` mit eigenem nativen Dokument, Speichern/Wiederöffnen und eigenem Dokument-Icon. Keine Grafiktreiberentwicklung. `DESKTOPG.GEO` wurde unverändert aus dem bereitgestellten `GEOWORKS.zip` extrahiert und nur lesend untersucht.

## 1. Geode-Identität

- Archivpfad: `GEOWORKS/SYSAPPL/DESKTOPG.GEO`
- Dateigröße: 101.524 Bytes
- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`
- App-Token im Header: `FCAB`
- Creator/Manufacturer-Feld: `GEOS`
- App-Name: `File Cabinet`
- Ressourcenanzahl aus dem Geode-Header: 51
- Importierte Bibliothek, die im Importbereich sichtbar ist: `ui`

## 2. Resource-Table-Zuordnung

Die Geode-Ressourcentabelle beginnt in dieser Datei bei Dateioffset `01D0h`. Die 51 Ressourceneinträge enthalten die Dateioffsets der Ressourcen. Die zugehörigen Flags stehen in der nachfolgenden Tabelle ab `0300h`.

Für die hier relevanten Ressourcen ergibt sich:

| Ressource | Datei-Offset | nächster Offset | Größe | Flags |
|---:|---:|---:|---:|---:|
| 8 | `56FCh` | `5FACh` | 2.224 Bytes | `0A72h` |
| 37 | `11BC4h` | `11CE8h` | 292 Bytes | `087Ah` |

Die Resource-8-Bytes beginnen mit ausführbarem 16-Bit-Code. Die Flags `0A72h` entsprechen dem Code-Ressourcentyp, wie er auch in den bereits untersuchten GeoWorks-1.x-Geodes vorkommt. Ressource 37 ist eine LMem-/Objektressource mit UI-Texten.

## 3. Dateiverwalter-Schlüsselwörter liegen in Ressource 8

Alle fünf Schlüsselwörter befinden sich innerhalb von Ressource 8:

| Zeichenfolge | Dateioffset | Ressourcenrelativer Offset |
|---|---:|---:|
| `fileManager` | `5BBBh` | `04BFh` |
| `filenameTokens` | `5BC7h` | `04CBh` |
| `tokenPathnames` | `5BD6h` | `04DAh` |
| `dosAssociations` | `5BE4h` | `04E8h` |
| `dosParameters` | `5BF2h` | `04F6h` |

Die Zeichenfolgen liegen in der Code-Ressource, nicht in einer separaten Objekt-/Monikerressource. Sie sind als ASCII-Namen vorhanden; ihre konkrete Laufzeitfunktion muss aus den Codeverwendungen abgeleitet werden.

## 4. Code unmittelbar nach den Schlüsselwörtern

Nach dem letzten Namen folgt ab Ressourcenoffset `0500h` wieder 8086-Code. Dieser Code greift auf Tabellenbereiche derselben Ressource zu:

- `CS:[DI+0538h]`
- `CS:[DI+0544h]`
- `CS:[DI+0550h]`
- `CS:[DI+055Ch]`

Er enthält zwei unmittelbare Far-Call-Operanden:
- Ressourcenoffset `0516h`, Dateioffset `5C12h`: `CALL FAR 0000:0072h`
- Ressourcenoffset `052Ah`, Dateioffset `5C26h`: `CALL FAR 0000:0071h`

Zwischen diesen Aufrufen liegen bedingte Sprünge und die Schleifensteuerung über `DI`; der Code erhöht `DI` um zwei und vergleicht es mit `000Ch`. Die Tabellen werden damit in einer Schleife verarbeitet.

Die Rohdatei enthält an diesen Stellen Segment-Nullwerte; die Segmentwortpositionen `0519h` und `052Dh` besitzen keinen Eintrag in der Relocation-Liste dieser Ressource. Ein dritter Aufruf `CALL FAR 0000:0073h` steht bei Ressourcenoffset `0581h` (Dateioffset `5C7Dh`); auch dessen Segmentwort bei `0584h` ist nicht relociert. Ohne die Auflösung dieser Low-Memory-Aufrufziele darf keiner der numerischen Offsets als Name einer bestimmten API-Funktion ausgegeben werden.

## 5. Tabelleninhalt

Der Tabellenbereich ab Ressourcenoffset `0538h` beginnt mit ASCII-Zeichenfolgen bzw. Zeichenfolgenfragmenten:

`DEFLFIgAgDgDSKDRLEPPATOS`

Danach folgen unter anderem wiederholte `26 00`-Paare und kleine Zahlenwerte. Ein weiterer tabellenartiger Bereich beginnt ab `059Ah` mit:

`FLFLFIGAgAgDgDDRL EPPPPATAT`

Die genauen Tabellenfelder und die Codierung der Token-/Pfadzuordnungen sind noch nicht vollständig dekodiert. Insbesondere ist nicht bewiesen, dass jedes dieser Fragmente direkt einem GEOS-Typ-/Creator-Token entspricht.

## 6. UI-Text „VM-Datei“ in Ressource 37

Der String `VM-Datei` befindet sich in Ressource 37:

- Dateioffset: `11BFAh`
- Ressourcenoffset: `0036h`
- Ressourcengröße: 292 Bytes
- Flags: `087Ah`

Er steht zusammen mit UI-Texten wie `Executable`, `Benennt ... um` und `Kopie von ...`. Das ordnet ihn dem Dateiverwalter-UI-/Dateiinformationsbereich zu. Es ist kein Beleg dafür, dass Ressource 37 die Typ-/Creator-Auswertung selbst implementiert.

## 7. Was jetzt belegt ist

1. `fileManager`, `filenameTokens`, `tokenPathnames`, `dosAssociations` und `dosParameters` liegen in DESKTOPG.GEO-Ressource 8.
2. Ressource 8 enthält ausführbaren 8086-Code und direkt anschließende tabellenartige Datenbereiche.
3. Der Code liest mehrere Tabellenadressen relativ zu CS und verarbeitet sie in einer Schleife.
4. Die Schleife enthält zwei Far-Calls mit den numerischen Offsets `0072h` und `0071h` (Instruktionsanfänge `0516h` und `052Ah`; die früher notierten Positionen `050Fh`/`0523h` waren Fehlzuordnungen zu den jeweils vorausgehenden MOV-Instruktionen).
5. `VM-Datei` liegt in einer separaten UI-/LMem-Ressource 37.

## 8. Noch nicht bewiesen

- Welche API-Funktionen hinter den Far-Calls `0072h` und `0071h` stehen.
- Ob die Tabellen `filenameTokens` / `tokenPathnames` die GEOS-Typ-/Creator-Paare, Dateiendungen oder andere Dateinamensregeln enthalten.
- Wo DESKTOPG den Typ-/Creator-Header einer VM-Datei einliest.
- Wie der Desktop aus der Erkennung den passenden Moniker bzw. das Dokument-Icon auswählt.
- Welche Registrierung GEOTEST für sein eigenes Dokumentformat benötigt.

## 9. Nächster Schritt

1. Für Ressource 8 die Relocationpositionen zu den drei Far-Calls `5C12h`, `5C26h` und `5C7Dh` exakt aus der Ressourcentabelle auslesen.
2. Die Aufrufkonventionen der Ziele `0000:0071h` bis `0000:0073h` anhand des Kernels und der Initialisierung rekonstruieren; erst dann prüfen, ob es UI-Bibliotheks-Exports, Kernelvektoren oder andere Low-Memory-Einsprünge sind.
3. Die Tabellen ab Ressourcenoffset `0538h` und `059Ah` strukturell dekodieren und die Schleife mit den konkreten Einträgen verbinden.
4. Danach den Codepfad verfolgen, der die Dateikopf-Typ-/Creator-Felder prüft und einen Moniker auswählt.

## Status

Ressourcen- und String-Zuordnung bestätigt. Code-/Tabellenbezug eingegrenzt. Numerische Far-Call-Offsets identifiziert, aber API-Namen und Semantik noch nicht aufgelöst. Keine Originaldatei geändert, kein GEOTEST-Build erzeugt, kein Laufzeiterfolg behauptet.
