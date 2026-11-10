# Basebox-SVGA-Ensemble12 – technischer Audit (2373)

Stand: 2026-11-10

## Gegenstand und Prüfmethode

Geprüft wurde das vom Nutzer bereitgestellte Archiv `Basebox-SVGA-Ensemble12.zip`.

- Archivgröße: 834.927 Bytes
- SHA-256: `1b3c0b5830d53dfd2fc3d5e387cd78f4687d151d33ce700c2cd4aa51f0689bfd`
- 192 ZIP-Einträge, davon 191 Einträge im mitgelieferten SHA256-MANIFEST.
- Alle 191 manifestierten Dateien wurden gegen ihre SHA-256-Werte geprüft: 191/191 stimmen; keine fehlende oder abweichende Datei.
- Der enthaltene Build wurde in einem entpackten Arbeitsverzeichnis erneut ausgeführt. GNU-as/ld/objcopy-Build war erfolgreich; alle vier resultierenden GEO-Dateien hatten exakt dieselben SHA-256-Werte wie die gelieferten Binärdateien.
- Die Installer-Tests liefen erneut: 5 Tests, 0 Fehler.
- Die nativen Instruktionstests konnten hier nicht erneut ausgeführt werden, weil das Python-Modul `unicorn` in der Arbeitsumgebung fehlt. Die mitgelieferte `NATIVE-RESULTS.json` dokumentiert 187 bestandene Fälle und 0 Fehler; das ist ein archivierter Testbericht, kein hier wiederholter Test.
- Die dokumentierten Basebox-Laufzeittests wurden nicht erneut ausgeführt. Die mitgelieferten Logs, Konfigurationen, Prüfergebnisse und Bildschirmaufnahmen wurden als Archivinhalt geprüft.

## Einordnung für GeoWorks / PC/GEOS 1.x

Das Paket zielt ausdrücklich auf Ensemble / GeoWorks Pro 1.2, Kernel-Protokoll 622.3 und Video-Protokoll 601.0. Die gelieferten Treiber sind native GEOS-1.x-Geodes.

Wesentlich ist die Architektur: Der ursprüngliche native Renderer aus `S16_1280.GEO` bleibt erhalten. Ein neu gebauter 16-Bit-Adapter ergänzt Moduserkennung, VBE-Prüfung und – bei den Basebox-Varianten – den synchronen HostIf-Aufruf. Es wird weder ein moderner Kernel vorausgesetzt noch die moderne HostIf-Bibliothek eingebunden.

Der HostIf-/DPI-Teil wurde aus dem mitgelieferten modernen `pcgeos-master`-Quellbaum hergeleitet und als eigenständiger Adapter in den nativen 1.x-Treiber portiert. Der moderne Quellbaum selbst ist deshalb nicht als 1.x-ABI-Referenz zu behandeln. Für die 1.x-Kompatibilität maßgeblich sind der unveränderte native Renderer, die nativen Protokollwerte und die konkrete Adapter-Integration.

## Gelieferte Treiber

| Datei | Zweck | Größe | SHA-256 |
|---|---|---:|---|
| `BB72_64.GEO` | Basebox 72 DPI, RGB565 | 35.010 | `694efa06840e605e214c39b20f4ee2a5ebafa4e290d45edc3cbe323aedb9317a` |
| `BB96_64.GEO` | Basebox 96 DPI, RGB565 | 35.010 | `8bfb2d12e512b50d00909fc6f58522b053e0ca556eb7275e0d87f4aa085b4ab1` |
| `BB120_64.GEO` | Basebox 120 DPI, RGB565 | 35.010 | `e78e91aacc8e9bd24e931ef78f72c0bf42e886003a1b75e2c36ba7c3e1593d05` |
| `V16_0720.GEO` | VESA 1280×720, RGB565 | 34.962 | `7b26608d30869235766384c8a2034a8ad653c738ad27e29cee4b80a78c53d20c` |

Alle vier Adapter beginnen in Ressource 1 bei Offset `7B20h`. Die drei Basebox-Adapter sind jeweils 1.102 Bytes lang; der feste VESA-Adapter ist 1.056 Bytes lang. Die Build-Manifeste weisen denselben beibehaltenen Renderer-Hash für alle vier Treiber aus: `721a06747b766e61616aa4db3c2939c998568f780a5883f72035a17132c24aef`.

## Dokumentiertes Laufzeitverhalten

Die Paketdatei `RUNTIME-RESULTS.md` und `TEST-RESULTS.json` dokumentieren für die mitgelieferte Basebox-BLD285-Umgebung und GeoWorks Pro 1.2:

| Treiber | dokumentierte tatsächliche Auflösung | Farbfeldprüfung |
|---|---:|---:|
| `BB72_64.GEO` | 960×540, 16 Bit RGB565 | 4.096/4.096 Farbzentren korrekt |
| `BB96_64.GEO` | 1280×720, 16 Bit RGB565 | 4.096/4.096 Farbzentren korrekt |
| `BB120_64.GEO` | 1600×900, 16 Bit RGB565 | 4.096/4.096 Farbzentren korrekt |
| `V16_0720.GEO` | 1280×720, 16 Bit RGB565 | 4.096/4.096 Farbzentren korrekt |

Die 4.096 Werte sind eine gezielte RGB565-Farbprobe, nicht die vollständige Prüfung aller 65.536 möglichen RGB565-Werte. Die Paketberichte nennen für alle akzeptierten Hauptläufe null Abweichungen. Ein zusätzlicher Clamp-Lauf dokumentiert 2040×1147 als vom Emulator tatsächlich zurückgegebene Geometrie nach einer größeren Anforderung.

Die dokumentierten Laufzeitergebnisse gelten für die konkrete mitgelieferte Basebox-BLD285-Version. Sie beweisen keine Kompatibilität mit realen SVGA-Karten oder anderen Emulatoren.

## Relevanz für die geplanten drei festen SVGA-Modi

Die früher festgelegten Zielmodi für den SVGA16.GEO-Treiber (16 Farben = 4 Bit pro Pixel, nicht 16 Bit pro Pixel) waren 1024×768, 1280×1024 und 1280×720.

**Wichtige Formatabgrenzung:** Das Archiv baut 16-Bit-RGB565-Treiber mit 65.536 möglichen Farbwerten. Das ist nicht dasselbe wie das frühere Ziel `SVGA16.GEO` mit 16 Farben (4 bpp). Die BIOS-Probe ist dennoch besonders wertvoll, weil sie sowohl passende 4-bpp-Modi als auch getrennte 16-bpp-Modi ausweist.

### VBE-Modi für das frühere 16-Farben-Ziel (4 bpp)

Die BIOS-Probe `probe01/probe-results.json` enthält diese beiden passenden 4-bpp-Modi:

| Auflösung | VBE-Modus | Pitch | VBE-Speichermodell | Status / Attribute |
|---|---:|---:|---|---|
| 1024×768×16 Farben | `0104h` | 128 Bytes | Planar, 4 bpp, Modell 3 | `004Fh` / `001Bh` |
| 1280×1024×16 Farben | `0106h` | 160 Bytes | Planar, 4 bpp, Modell 3 | `004Fh` / `001Bh` |

Beide Modi werden auch in der erweiterten `vesa_modes=all`-Probe aufgeführt. Die Probe meldet für beide 64-KiB-Fenster und 64-KiB-Granularität. Das ist ein positiver BIOS-Probe-Befund für die bereitgestellte Basebox-Konfiguration, aber noch kein Laufzeittest mit einem angepassten 4-bpp-GeoWorks-Treiber.

Ein Standard-VBE-Modus 1280×720×4 bpp ist in den dokumentierten normalen und erweiterten Moduslisten nicht enthalten. Der im Paket verwendete Basebox-Modus `089Ah` ist dagegen 16-bpp-RGB565; er ist deshalb kein Ersatz für einen 1280×720-Modus mit 16 Farben. Eine Lösung für 1280×720×4 bpp benötigt eine separate VBE-/Emulator- oder Hardware-Unterstützung.

### Getrennte 16-bpp-RGB565-Modi des gelieferten Pakets

Die Probe führt außerdem folgende Modi auf, die für den 64K-Farb-Treiber aus diesem Archiv relevant sind:

| Auflösung | VBE-Modus | Pitch | Modell / Maske |
|---|---:|---:|---|
| 1024×768, 16 bpp | `0117h` | 2.048 Bytes | Direct Color, 5:6:5, Positionen 11/5/0 |
| 1280×1024, 16 bpp | `011Ah` | 2.560 Bytes | Direct Color, 5:6:5, Positionen 11/5/0 |

Die Probe meldet für beide Modi Status `004Fh`, Attribute `009Bh`, 64-KiB-Fenster und 64-KiB-Granularität. Auch das ist zunächst ein BIOS-Probe-Befund und kein Laufzeittest dieser beiden Modi mit einem angepassten GEOS-Treiber.

1280×720×16 bpp wird in den dokumentierten normalen VBE-Moduslisten nicht als Standardmodus gefunden. Der Paketadapter löst genau diesen Fall über die Basebox-HostIf-API und prüft danach die tatsächlichen VBE-Daten des vom Host bereitgestellten Modus `089Ah`.

### Grenzen der Übertragbarkeit

Die statische Renderer-Prüfung des Pakets nennt für den enthaltenen **16-bpp-RGB565-Renderer** Obergrenzen von 2040×1536, maximal 4080 Bytes Pitch und ein 64-KiB-Bankfenster. Diese Analyse beweist nicht dieselben Grenzen für einen anderen 4-bpp-Renderer wie den früheren `SVGA8004.GEO`. Dessen eigene Puffer, Zeilenadressierung, Bankumschaltung und Modustabellen müssen separat geprüft werden.

## Abgleich mit dem ursprünglichen 16-Farben-Treiber

Zusätzlich wurde das bereits bereitgestellte `GEOWORKS.zip` read-only geprüft. Darin liegt `GEOWORKS/SYSTEM/SVGA8004.GEO`:

- Größe: 18.950 Bytes
- SHA-256: `476bb8e84bc80f1922e0cb11540aa2e61869e44cf577f6c92adcc062b066cf2c`
- GEOS-1.x-Geode, Release 1.2.8.2
- Kernel-Protokoll 622.3, Geode-Protokoll 1.0
- drei Ressourcen, keine Imports oder Exports
- Ressource 2 enthält 19 lesbare Gerätebezeichnungen; alle bezeichnen den Modus 800×600 mit 16 Farben. Darunter sind der generische VESA-kompatible Eintrag und herstellerspezifische Varianten wie Everex, Headland/Video 7, Oak, ATI, SOTA, Genoa, Paradise, Cirrus Logic und Trident.

Damit ist `SVGA8004.GEO` – nicht der 16-bpp-`S16_1280.GEO`-Renderer aus dem Basebox-Paket – das passende originale 1.x-Ausgangsartefakt für die Untersuchung des früheren 16-Farben-Ziels. Die 19 Namen sind zunächst nur nachgewiesene Geräte-/Modusbezeichnungen; welche Erkennungs- und Setup-Pfade dahinter liegen und welche davon auf Basebox funktionieren, muss durch Disassemblierung und Laufzeittests getrennt festgestellt werden.

Die Basebox-Probe zeigt für 1024×768×16 Farben den VBE-Modus `0104h` und für 1280×1024×16 Farben den VBE-Modus `0106h`. Das sind genau die beiden 4-bpp-Modi, die in der obigen Tabelle stehen. Die 16-bpp-Modi `0117h` und `011Ah` gehören dagegen zum anderen RGB565-Treiberpfad.

## Statische Erstaufnahme von SVGA8004.GEO

Die Ressource 1 der originalen `SVGA8004.GEO` beginnt bei Datei-Offset `013Eh` und ist 17.504 Bytes lang. In dieser Ressource wurden zwei Tabellen mit je 19 WORD-Einträgen identifiziert:

- Ressourcen-relative `013Fh`: 19 Probe-/Erkennungs-Callbacks
- Ressourcen-relative `0165h`: 19 Setup-Callbacks

Die Reihenfolge stimmt mit den 19 Geräte-Strings in Ressource 2 überein. Der erste Eintrag ist `VESA Kompatible Super VGA: 800x600 16 Farben`; seine Callback-Paare lauten Probe `2C40h` und Setup `2C96h`. Die zugehörigen Datei-Offsets sind `027Dh`, `02A3h`, `2D7Eh` und `2DD4h` für die genannten Ressourcenpositionen, wobei die letzten beiden Werte die Callback-Ziele innerhalb der Datei bezeichnen.

Der Probe-Callback bei Ressourcen-Offset `2C40h` führt BIOS `INT 10h`, Funktion `4F00h`, aus, prüft den Rückgabewert `004Fh` und die Signatur `VESA`. Danach durchsucht er die VBE-Modusliste ausdrücklich nach Modus `0102h` (800×600×16 Farben).

**Noch offene und wichtige Abweichung:** Der zugehörige Setup-Callback `2C96h` setzt `AH=00h`, liest `AL` aus einer Tabelle ab `2CA8h` und ruft anschließend `INT 10h` auf. Der erste Tabellenwert an `2CA8h` ist `6Ah`, nicht `02h`. Der Probe-Code sucht also VBE-Modus `0102h`, während der Setup-Code für den ersten Geräte-Eintrag den BIOS-Moduswert `006Ah` anfordert. Ob dies ein vom BIOS unterstützter OEM-Alias ist oder ob weitere Vorbedingungen die Interpretation verändern, ist noch nicht verifiziert. Diese Differenz darf beim Umbau nicht übergangen werden.

Die Einträge 2 und 3 verwenden eigene Setup-Routinen (`2D1Eh` bzw. `2D50h`); zahlreiche weitere Einträge teilen sich den generischen Setup-Callback `2C96h`. Das bestätigt, dass die Geräteliste nicht bloß eine Liste von Auflösungen ist: Sie verknüpft die auswählbaren Geräte mit jeweils eigenen Erkennungs- und Initialisierungsroutinen.

## Wichtige Abweichung vom ursprünglichen Ein-Treiber-Ziel

Das Paket liefert vier getrennte GEO-Dateien. Jede Datei enthält nur einen Geräte-/Moduseintrag. Es erfüllt daher noch nicht das frühere Ziel, **einen einzigen SVGA-Treiber mit drei auswählbaren festen Auflösungen** bereitzustellen.

Der vorhandene Adapter ist dennoch eine belastbare technische Grundlage:
1. 1024×768 und 1280×1024 können über die VBE-Modusliste gesucht und anhand der tatsächlichen VBE-Modusinformationen validiert werden.
2. 1280×720 benötigt in der getesteten Basebox-Umgebung den bereits vorhandenen HostIf-Fallback.
3. Für einen einzigen Treiber muss zusätzlich die native Geräteauswahl in Ressource 2 und die Zuordnung jedes Geräte-/Moduseintrags zur gewünschten Geometrie untersucht und erweitert werden. Das darf nicht durch bloßes Umbenennen oder durch einen angenommenen Index erfolgen.

## Offene Punkte / nächster Arbeitsschritt

1. Die Geräteauswahl und Callback-Kette des nativen `S16_1280.GEO` vollständig rekonstruieren; insbesondere die Bedeutung der Geräte-Handles in Ressource 2.
2. Einen experimentellen Adapter für 1024×768 und 1280×1024 auf Basis der bestätigten VBE-Modi erzeugen, ohne die Originaldatei zu verändern.
3. Die drei festen Modi zunächst als getrennte Testvarianten strukturell validieren und anschließend unter der konkreten Basebox-/GeoWorks-1.2-Installation testen.
4. Erst danach die drei Einträge in einem einzigen nativen GEO-Treiber zusammenführen.
5. Textausgabe, Mauszeiger, Fensteroperationen, Scrollen, Linien/Polygone und Bankgrenzen bei jeder Zielauflösung separat testen.

## Unveränderte Originale und Grenzen

Das Originalarchiv wurde nicht verändert. Die Prüfung und der erneute Build erfolgten in einem entpackten Arbeitsverzeichnis. Es wurden keine GEO-Dateien in eine produktive Installation kopiert. Proprietäre Originaldateien und fertige GEO-Binärdateien werden mit diesem Bericht nicht in das Repository übernommen.

Die Ergebnisse sind als Paket-Audit und Arbeitsgrundlage zu verstehen, nicht als Freigabe des noch nicht gebauten Ein-Treiber-/Drei-Modus-Ziels.
