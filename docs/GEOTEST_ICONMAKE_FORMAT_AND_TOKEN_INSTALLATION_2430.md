# Untersuchung 2430 – ICONMAKE 1.0: belegte Icon-Formate und Token-Installationsweg

## Neue Primärquelle im GeoWorks-Archiv

Im untersuchten Archiv `GEOWORKS.zip` befinden sich die zeitgenössischen Dokumentationsdateien:

- `GEOWORKS/WORLD/PROGRAMM.E/G12/GEOTOOLS/ICONMAKE.DOC`
- `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/ICONMAKE.ENG`
- ergänzend: `GEOWORKS/ICONS/ICONINST.TXT`
- ergänzend: `GEOWORKS/ICONS/DOS_ICON.TXT`

Die deutsche und englische ICONMAKE-Dokumentation beschreiben ICONMAKE 1.0 von Marcus Gröber aus dem Jahr 1992. Die Aussagen unten stammen aus diesen Dateien im vorliegenden Archiv.

## Belegte Icon-Varianten

Für ein Token können bis zu drei Icon-Dateien bereitgestellt werden:

| Variante | Abmessungen | Farbtiefe |
|---|---:|---|
| CGA | 48 × 14 Pixel | monochrom |
| HGC / MCGA | 48 × 30 Pixel | monochrom |
| EGA | 48 × 30 Pixel | 16 Farben |

Die Dokumentation verwendet als Namensbeispiel `xxxx_CGA.PCX`, `xxxx_HGC.PCX` und `xxxx_EGA.PCX`.

Die Windows-ICO-Konvertierung kann laut Dokumentation in der Regel mehrere passende Varianten erzeugen. Für diese ICO-Konvertierung nennt die Dokumentation abweichend von den GEOS-Standardmaßen häufig 32 × 32 Pixel.

## Belegter Token-Aufbau und Installationsweg

ICONMAKE beschreibt Tokens als Kombination aus:

- vier Zeichen Token-Code;
- numerischer Hersteller-/Token-Komponente im Bereich 0 bis 65535;
- optional zugeordnetem Programmnamen;
- einem oder mehreren Icons für unterschiedliche Bildschirmtypen;
- gegebenenfalls dem Namen der erzeugenden Anwendung.

Die Dokumentation beschreibt folgenden Installationsmechanismus:

1. Eine kleine Dummy-Anwendung enthält das Token und die zugehörigen Icons.
2. Beim Öffnen eines Verzeichnisses liest GeoWorks Tokens aus Anwendungen ein, die dem System noch unbekannt sind.
3. Die neu erkannten Tokens werden in die interne Datei `TOKEN.DB` übernommen.

Die ergänzende Datei `ICONINST.TXT` bestätigt für die dort beschriebene Icon-Sammlung, dass die Dummy-Dateien kleine PC/GEOS-Anwendungen sind und dass der Dateiname den Token-Code liefert; die dortigen Sammlungstokens verwenden Hersteller-ID 255.

Wichtig: Die Hersteller-ID 255 gilt für die in ICONINST.TXT beschriebene Sammlung, nicht automatisch für jedes eigene GEOTEST-Token. Das vorhandene GEOTEST-App-Token `GTS1` wurde bisher mit Hersteller-ID 0 geführt.

## Abgleich mit Untersuchung 2428 und 2429

Die Ressourcenbereiche in `GDOC.000` und `PAPR.000` wurden bereits eingegrenzt:

- Die Offsettabelle enthält sieben Einträge und sechs unterschiedliche Zielpositionen.
- Die ersten drei unterschiedlichen Bereiche sind zwischen den beiden Dateien byteidentisch.
- Ab Dateioffset `0x4F4` unterscheiden sich die Daten.
- Die letzten Datenbereiche beginnen bei `0x69C` (GDOC) beziehungsweise `0x6AC` (PAPR).

Die ICONMAKE-Dokumentation liefert nun Sollmaße und Sollfarbtiefen, aber keine direkte Beschreibung dieser konkreten Ressourcenoffsets. Daher ist noch nicht bewiesen, welcher Bereich CGA, HGC oder EGA enthält. Auch ein bestimmtes Kompressionsformat ist noch nicht nachgewiesen.

## Bedeutung für GEOTEST

Für ein eigenes Dokument-Icon muss die spätere Implementierung mindestens die historischen Icon-Varianten und den Token-Mechanismus berücksichtigen. Die Dokumentation stützt die Architektur einer separaten Dummy-/Provider-Geode, die ein Token mit mehreren Monikern bereitstellt.

Noch offen bleibt, ob GEOTEST das Dokument-Token direkt in seiner eigenen Geode bereitstellen kann oder ob ein separater Provider-/Dummy-Geode-Aufbau für GeoWorks 1.2.8 die robustere Lösung ist. Diese Frage wird nicht allein durch ICONMAKE beantwortet.

## Nächster Analyseschritt

Die internen Ressourcen der Provider-Dateien werden gegen die drei dokumentierten Zielprofile geprüft:

- 48 × 14, 1 Bit pro Pixel;
- 48 × 30, 1 Bit pro Pixel;
- 48 × 30, 4 Bit pro Pixel.

Dabei müssen Ressourcenheader, tatsächliche Datenlänge, mögliche Planes und etwaige Kompression zusammenpassen. Eine bloße Übereinstimmung der Byteanzahl reicht nicht als Nachweis.

## Grenzen und Sicherheit

- Quelle sind die mitgelieferten Dokumentationsdateien aus dem untersuchten GeoWorks-Archiv; es wurde keine externe Formatbehauptung ergänzt.
- Die Dokumentation beschreibt ICONMAKE 1.0 von 1992 und ist zeitgenössisch, aber nicht automatisch eine vollständige Spezifikation jeder GeoWorks-1.x-internen Struktur.
- Nur statische, lesende Untersuchung.
- Keine Änderungen an `TOKEN.DB`, `GEOS.INI` oder Provider-Dateien.
- Kein Laufzeittest in GeoWorks.
