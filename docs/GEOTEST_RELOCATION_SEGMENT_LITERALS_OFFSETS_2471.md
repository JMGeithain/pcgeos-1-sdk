# GEOTEST / PC-GEOS 1.x – Untersuchung 2471
## Segmentliterale und Offsetwerte der CALL-FAR-Relokationen
Datum: 12.11.2026
Geltungsbereich: GeoWorks 1.2.8 / PC/GEOS 1.x

## 1. Ausgangsbasis
Fortsetzung von Untersuchung 2470. Grundlage ist ausschließlich das vom Nutzer bereitgestellte `GEOWORKS.zip` (22.190.788 Byte).

Im Archiv:
- 263 Pfade mit Endung `.GEO`;
- 253 Dateien konnten mit dem verwendeten GEODE-Format-1-Prüfer vollständig eingelesen werden;
- nach SHA-256-Deduplizierung: 221 unterschiedliche GEODE-1-Binärdateien;
- 7 weitere Dateien mit Format-1-Signatur benötigen eine gesonderte Parser-/Formatprüfung;
- 3 weitere GEO-Dateien besitzen eine andere Signatur und sind nicht Teil der GEODE-1-Statistik.

In den 221 unterschiedlichen Binärdateien wurden 35.250 Relokationen `source=0, type=0` gefunden. Alle 35.250 markieren das 16-Bit-Offsetfeld einer `CALL FAR`-Instruktion (Byte `0x9A` unmittelbar vor dem Operand).

## 2. Die 294 nichtnulligen Segmentliterale
Bei 294 der 35.250 Aufrufe ist das direkt nach dem Offsetoperand folgende 16-Bit-Segmentwort nicht null.

Diese 294 Einträge verteilen sich auf 56 verschiedene Segmentwortwerte.

Häufigste Werte:
| Segmentwort | Anzahl |
|---:|---:|
| `0x0E18` | 20 |
| `0x0E24` | 19 |
| `0x0DF4` | 15 |
| `0x0E0C` | 15 |
| `0x0E30` | 15 |
| `0x0E3C` | 15 |
| `0x0EA8` | 13 |
| `0x0E00` | 13 |
| `0x0E90` | 11 |
| `0x0EB4` | 10 |
| `0x0E84` | 10 |
| `0x0ECC` | 8 |

Die Werte sind auffällig gruppiert und wiederholen sich über verschiedene GEODE-Dateien. Das ist ein belastbarer Bytebefund, aber noch keine Erklärung der Werte.

### 2.1 Abgleich mit vorhandenen Tabellenwerten
Die 294 Segmentwörter wurden mit Ressourcenlängen, Ressourcen-Dateioffsets und Export-Offsets der jeweiligen GEODE-Datei verglichen:
- 285 Werte hatten keinen direkten Treffer in diesen drei Tabellenarten;
- 8 Werte entsprachen einer Ressourcenlänge;
- 1 Wert entsprach einem Export-Offset.

Keiner dieser Vergleiche beweist die Bedeutung des Segmentworts. Insbesondere darf ein Wert wie `0x0E18` nicht als tatsächliche Laufzeitsegmentadresse, Ressourcen-ID oder Exportnummer bezeichnet werden.

### 2.2 Beispielhafte Einordnung
Die wiederkehrenden Werte `0x0E18`, `0x0E24` usw. treten in mehreren System- und Anwendungsdateien auf, unter anderem CALCGCM.GEO, CALC.GEO, GROBJ.GEO, UI.GEO und CUA/MOTIF-Modulen. Mehrere dieser Module enthalten dieselben oder sehr ähnliche Codebereiche. Eine Korrelation kann daher auch durch gemeinsame Codevorlagen entstehen; sie ist kein Beweis für dieselbe Laufzeitadresse.

## 3. Die 500 Offsetwerte außerhalb der Quellressource
Bei 500 der 35.250 CALL-FAR-Offsetoperanden ist der 16-Bit-Wert numerisch größer oder gleich der Größe der Ressource, in der der Aufruf selbst liegt.

Das ist nicht automatisch ein Fehler. Ein Far-Aufruf kann auf eine andere Ressource oder einen anderen Segmentkontext zielen.

### 3.1 Größenabgleich mit den Ressourcen derselben GEODE
Für jeden dieser 500 Werte wurde geprüft, ob er kleiner als die Größe mindestens einer anderen Ressource derselben GEODE-Datei ist:
- 495 Werte passen größenmäßig in mindestens eine Ressource derselben GEODE;
- 5 Werte passen in keine Ressource der jeweiligen GEODE.

Dieser Test ist nur ein Größenplausibilitätstest. Er identifiziert nicht die Zielressource, weil mehrere Ressourcen dieselbe oder größere Länge besitzen können und der Relokationsrecord allein hier keinen eindeutigen Ressourcenindex liefert.

### 3.2 Fünf Fälle ohne passende Ressourcengröße
Die fünf Fälle stammen aus:
- ABSGEN.GEO: R3, Offsetoperand `0x022F`, Ressourcengrößen maximal `0x0170`;
- DISK.GEO: R3, Offsetoperanden `0x022E` und `0x022F`, Ressourcengrößen maximal `0x0110`;
- GENMOUSE.GEO: R3, Offsetoperand `0x022F`, Ressourcengrößen maximal `0x0200`;
- ICON.GEO (unter `WORLD/PROGRAMM.E/ICONEDIT.OR`): R2, Offsetoperand `0x0238`, Ressourcengrößen maximal `0x01C0`.

Die fünf Werte liegen außerhalb sämtlicher Ressourcengrößen der jeweiligen GEODE. Ihre Zielauflösung bleibt ungeklärt. Sie dürfen nicht als fehlerhafte Aufrufe oder als bestätigte externe Ziele klassifiziert werden, ohne den Loader-/Relokationsmechanismus zu kennen.

## 4. Was die Untersuchung aussagt
### Gesichert
1. Alle 35.250 Klasse-0/Typ-0-Records der 221 eindeutigen GEODE-1-Dateien markieren den Offsetoperand einer `CALL FAR`-Instruktion.
2. 294 dieser Aufrufe besitzen ein nichtnulliges Segmentliteral; es gibt 56 verschiedene Werte.
3. 500 Offsetwerte liegen numerisch außerhalb der Größe ihrer Quellressource.
4. 495 dieser 500 Werte passen größenmäßig in mindestens eine Ressource derselben GEODE; fünf passen in keine Ressourcengröße der jeweiligen Datei.
5. Segmentliterale und Offsetwerte allein reichen nicht aus, um ein eindeutiges Zielsegment bzw. eine Zielressource zu bestimmen.

### Nicht bewiesen
- die Laufzeitbedeutung der 56 Segmentwortwerte;
- die genaue Zielressource jedes der 500 Offsetwerte;
- ob die fünf Sonderfälle externe, spezielle oder anders aufgelöste Ziele sind;
- die konkrete Änderung, die der Loader an Offset- und Segmentoperand vornimmt;
- eine Zuordnung zu Exportordinals oder Kernel-APIs.

## 5. Konsequenz für SDK und GEOTEST
Noch keine Änderung an Parser oder Packer.
Eine spätere Diagnose kann die folgenden Merkmale getrennt ausweisen:
- Relokationsklasse/Typ;
- erkannter Maschinenopcode `CALL FAR`;
- Offsetoperand;
- Segmentliteral;
- Offset kleiner/größer als Größe der Quellressource;
- Anzahl möglicher Ressourcen, deren Größe den Offset zulässt.

Diese Angaben sind Analysehinweise, keine automatische Zielauflösung. Der Packer darf daraus keine Segmentwerte oder Zielressourcen erraten.

## 6. Nächste Untersuchung 2472
1. Die 56 Segmentwortwerte nach gemeinsamen Codevorlagen und Ressourcenkontexten gruppieren.
2. Für die fünf Fälle ohne passende Ressourcengröße die vollständigen CALL-Umgebungen und Import-/Exporttabellen untersuchen.
3. Die 495 größenmäßig passenden Kandidaten anhand von Kontrollfluss, Ressourcenflags und weiteren Relokationen eingrenzen.
4. Die sieben nicht vollständig parsebaren Format-1-Dateien separat prüfen.
5. Die tatsächliche Loaderauflösung erst dann formulieren, wenn ein unabhängiger Beleg aus Formatdokumentation, Loadercode oder einem kontrollierten Laufzeittest vorliegt.

## 7. Änderungsstatus
- `GEOWORKS.zip` nur gelesen.
- Keine GEO-Datei verändert.
- TOKEN.DB nicht verändert.
- SDK-Quelldateien und GEOTEST.GEO nicht verändert.
- Kein Build und kein Emulator-Laufzeittest.
