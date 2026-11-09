# GEOTEST 1.x – Programmsymbol einbinden

## Bilddatei

Die bereitgestellte Datei `Testbild_48x30_16farben.pcx` ist ein PCX-Bild mit 48 × 30 Pixeln und 16 Farben. Das ist das in der GeoWorks-1.x-Dokumentation zu ICONMAKE beschriebene EGA/VGA-Format.

Die GEOTEST-Anwendung enthält im GEODE-Header bereits den Token-Code `GTS1` und die Manufacturer-ID `0`. Das Symbol muss daher unter exakt diesem Token registriert werden.

## Warum nicht einfach in GEOTEST.GEO kopieren?

GeoWorks 1.x verwaltet Programm-Moniker über das Token-System. Die IconMake-Dokumentation im GeoWorks-Nutzerarchiv beschreibt die Erzeugung einer zusätzlichen Token-Dummy-Datei. Das Programm-Icon wird damit im Token-System registriert; es ist nicht einfach eine PCX-Datei, die an die ausführbare GEO-Datei angehängt wird.

## Konvertierung

Die vorbereitete Batchdatei ruft das mitgelieferte DOS-Programm ICONMAKE auf:

```bat
ICONMAKE m0 GTS1,0 GEOTEST_EGA.PCX
```

- `m0`: Transparenz deaktivieren, da die Grafik alle 16 Farbpalettenindizes verwendet.
- `GTS1`: Token-Code aus dem GEOTEST.GEO-Header.
- `0`: Manufacturer-ID aus dem GEOTEST.GEO-Header.

Erwarteter Dateiname: `GTS10000.000`.

## Installation

1. ICONMAKE.EXE aus der vorhandenen GeoWorks-Installation ausführen.
2. Die erzeugte `GTS10000.000` neben `GEOTEST.GEO` in den Test-WORLD-Ordner kopieren.
3. Den Ordner im GeoManager neu einlesen lassen oder GeoWorks neu starten.
4. Das Icon im GeoManager kontrollieren.

Die vorbereiteten Dateien liegen im separaten Paket `GEOTEST_ICON_Paket.zip` in der Arbeitsausgabe. Die PCX-Datei stammt vom Nutzer; ICONMAKE.EXE wird nicht ins öffentliche SDK kopiert.

## Status

Bildformat und Token-Zuordnung sind geprüft. Die eigentliche ICONMAKE-Konvertierung und der anschließende GeoWorks-1.2-Anzeigetest stehen noch aus. Die GEOTEST.GEO-Binärdatei wurde nicht verändert.

## Quellen / Grundlage

- Mitgelieferte GeoWorks-1.x-Datei `ICONMAKE.DOC` / `ICONMAKE.ENG`, ICONMAKE 1.0 von Marcus Gröber (1992): PCX-Formate, Token-Dummy-Konzept, Token-Code und Transparenzoption.
- Mitgelieferte `ICONINST.TXT`: Token-Dateien und Token-IDs.
- GEOTEST.GEO: Token-Code `GTS1`, Manufacturer-ID 0 im GEODE-Header.
