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

Die BIOS-Probe `probe01/probe-results.json` enthält bereits konkrete VBE-Modusbeschreibungen für zwei der drei Zielauflösungen:

| Auflösung | VBE-Modus | Pitch | Modell / Maske |
|---|---:|---:|---|
| 1024×768×16 | `0117h` | 2.048 Bytes | Direct Color, 5:6:5, Positionen 11/5/0 |
| 1280×1024×16 | `011Ah` | 2.560 Bytes | Direct Color, 5:6:5, Positionen 11/5/0 |

Die Probe meldet für beide Modi Status `004Fh`, Attribute `009Bh`, 64-KiB-Fenster und 64-KiB-Granularität. Das ist ein positiver BIOS-Probe-Befund für die bereitgestellte Basebox-Konfiguration. Es ist noch kein Laufzeittest dieser beiden Modi mit einem angepassten GEOS-Treiber.

1280×720×16 wird in den dokumentierten normalen VBE-Moduslisten nicht als Standardmodus gefunden. Der Paketadapter löst genau diesen Fall über die Basebox-HostIf-API und prüft danach die tatsächlichen VBE-Daten des vom Host bereitgestellten Modus `089Ah`.

Die statische Renderer-Prüfung des Pakets nennt Obergrenzen von 2040×1536, maximal 4080 Bytes Pitch und ein 64-KiB-Bankfenster. Diese Grenzen lassen 1024×768 und 1280×1024 grundsätzlich innerhalb der geprüften festen Array-Grenzen liegen. Vor einer Freigabe sind trotzdem die vollständigen Modusdaten, der verfügbare Videospeicher, Bankgrenzen und tatsächliche GEOS-Laufzeit zu prüfen.

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
