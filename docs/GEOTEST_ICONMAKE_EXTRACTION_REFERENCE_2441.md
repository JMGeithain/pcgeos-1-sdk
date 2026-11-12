# Untersuchung 2441 – ICONMAKE 1.0 als Extraktionsreferenz

## Ziel

Prüfung der originalen ICONMAKE-Dokumentation und der ausführbaren Datei aus dem GeoWorks-Archiv. Ziel ist, den dokumentierten Extraktionsweg zu bestätigen und eine belastbare Grundlage für einen späteren Vergleich der ausgegebenen PCX-Dateien mit den internen Provider-Daten zu schaffen.

## Originaldateien

Aus `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/` wurden gelesen:

- `ICONMAKE.EXE` – 19.477 Byte
- `ICONMAKE.ENG` – 6.234 Byte
- `ICONMAKE.DOC` – 6.855 Byte

Die EXE ist eine DOS-MZ-Datei. Die Dateien wurden ausschließlich gelesen und nicht verändert.

## Dokumentierter Funktionsumfang

Die englische Originaldokumentation `ICONMAKE.ENG` beschreibt drei Modi:

### 1. PCX-Dateien zu einem Token-Provider

Syntax laut Dokumentation:

```
ICONMAKE m[<transp_color>] [<path>]<tokn>[,<num>] {<PCX_file(s)>...}
```

Damit wird aus bis zu drei PCX-Dateien eine Dummy-Anwendung mit Token und Icons erzeugt. Die Dokumentation nennt die Standardprofile:

- `xxxx_CGA.PCX`: 48×14, monochrom;
- `xxxx_HGC.PCX`: 48×30, monochrom;
- `xxxx_EGA.PCX`: 48×30, 16 Farben.

Die Standard-Tokennummer ist 255, kann aber mit `,<num>` geändert werden.

### 2. Icons aus einer vorhandenen GeoWorks-Datei extrahieren

Syntax laut Dokumentation:

```
ICONMAKE x <filename>
```

Der Text erklärt ausdrücklich, dass Icon-Definitionen aus vorhandenen GeoWorks-Programmen oder Icon-Dummy-Dateien extrahiert und als PCX-Dateien ausgegeben werden. Die Dateinamen folgen dem CGA/HGC/EGA-Schema.

### 3. Windows-ICO-Datei zu einem Token-Provider

Syntax laut Dokumentation:

```
ICONMAKE w [<path>]<tokn>[,<num>] <ICO_file>
```

Der ICO-Modus versucht, geeignete Icon-Varianten für die drei Bildschirmtypen zu erzeugen.

## Bestätigung in der ausführbaren Datei

Die Datei `ICONMAKE.EXE` wurde als DOS-MZ-Executable identifiziert. Eine ASCII-String-Prüfung fand unter anderem:

- `_CGA`
- `_HGC`
- `_EGA`
- `IconMake 1.0 -=- by Marcus Gr`
- `Syntax: ICONMAKE x <geos_file>`
- `to extract icons to PCX files`
- `Syntax: ICONMAKE m <...>`
- `Syntax: ICONMAKE w <...>`
- `No images.`
- `Invalid command.`

Die Strings bestätigen, dass die Extraktions- und Erzeugungsmodi in der EXE vorgesehen sind. Ein Stringfund allein beweist allerdings nicht, dass ein bestimmter Eingabedatensatz erfolgreich verarbeitet wird.

## Wichtige technische Einordnung

Die Dokumentation sagt, dass ICONMAKE zur Konvertierung einen Codeabschnitt aus der ursprünglichen GeoWorks-Icon-Sammlung verwendet. Damit ist ICONMAKE eine besonders wertvolle zeitgenössische Referenz für den Provider-Aufbau und die Bildkonvertierung.

Sie ist aber keine vollständige schriftliche Spezifikation des internen Binärformats. Der zuverlässigste nächste Schritt ist deshalb ein tatsächlicher Extraktionstest mit einer bekannten Provider-Datei.

## Noch nicht ausgeführt

Der Aufruf

```
ICONMAKE x GDOC.000
```

wurde in dieser Untersuchung nicht ausgeführt. In der verfügbaren Analyseumgebung stand keine DOS-Laufzeitumgebung zur Verfügung. Es liegen deshalb aus dieser Untersuchung keine neu erzeugten PCX-Dateien vor.

Es wird ausdrücklich nicht behauptet, dass die Icon-Daten bereits dekodiert wurden.

## Geplanter reproduzierbarer Test

Sobald eine DOS-Umgebung verfügbar ist:

1. Eine unveränderte Kopie von `GDOC.000` in ein separates Testverzeichnis legen.
2. `ICONMAKE x GDOC.000` ausführen.
3. Die erzeugten Dateien und deren Abmessungen erfassen.
4. Den Vorgang mit `PAPR.000` und einem weiteren Provider wiederholen.
5. PCX-Header, Bildmaße, Bitplanes, Bits pro Pixel und Pixeldaten vergleichen.
6. Die PCX-Pixeldaten gegen die zuvor lokalisierten Provider-Bereiche abgleichen.

Das ist der Weg, um die tatsächliche Pixelkodierung und mögliche Kompression mit einem unabhängigen Referenzdecoder zu bestimmen.

## Konsequenz für GeoViewPlus und GEOTEST

Für GeoViewPlus ist ICONMAKE ein unabhängiger Referenzdecoder, dessen Ausgabe später mit einem eigenen Parser verglichen werden kann. Für GEOTEST liefert die Dokumentation den historischen Erzeugungsweg für Token-Provider.

Noch nicht entschieden ist, ob GeoViewPlus den ICONMAKE-Algorithmus direkt nachbilden muss oder ob ein kleiner eigenständiger Decoder für die relevanten Monikerstrukturen ausreicht.

## Methodik und Grenzen

- Statische Prüfung der Originaldokumentation und DOS-EXE aus `GEOWORKS.zip`.
- ASCII-Strings aus der EXE ausgelesen.
- Kein Aufruf der EXE und keine PCX-Ausgabe in dieser Untersuchung.
- Keine Änderungen an `TOKEN.DB`, `GEOS.INI` oder Provider-Dateien.
- Kein Laufzeittest in GeoWorks.
