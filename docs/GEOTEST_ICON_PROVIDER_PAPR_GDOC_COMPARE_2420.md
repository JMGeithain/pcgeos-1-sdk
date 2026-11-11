# GEOTEST – Icon-Provider PAPR/GDOC Vergleich (2420)

Stand: 2026-11-12  
Geltungsbereich: ausschließlich originales GeoWorks / PC/GEOS 1.x  
Quelle: vom Nutzer bereitgestelltes `GEOWORKS.zip`, Mitglieder `GEOWORKS/ICONS/PAPR.000`, `GDOC.000`, `ICONINST.TXT` und `DOS_ICON.TXT`.

## 1. Ergebnis in Kürze

`PAPR.000` und `GDOC.000` sind strukturell nahezu identische kleine GeoWorks-1.x-Anwendungs-Geodes. Beide haben sieben Ressourcen, genau einen Import (`ui`, Protokoll 693.0), keine Exporte und jeweils denselben kleinen UI-/Programmrahmen. Die Unterschiede konzentrieren sich auf die Geode-Kennung und drei Moniker-/Grafikressourcen.

Das bestätigt den historischen Icon-Provider-Ansatz als **kleine Geode mit eigenem Dateityp-Token und eingebetteten Icon-Varianten**. Es beweist aber noch nicht, dass diese DOS-Dateierweiterungs-Zuordnung automatisch für native GEOS-Dokumente mit numerischer DOS-Endung funktioniert.

## 2. Header- und Geode-Metadaten

| Merkmal | PAPR.000 | GDOC.000 |
|---|---:|---:|
| Dateigröße | 2.208 Byte | 2.256 Byte |
| SHA-256 | `30b08761294ccd7762c686ca3d477e509cb454f56b6c7db5aa2b1497efbabfbe` | `fe19cbcb46c2a92cf02da64c963facb8decb95d7e60bca34eb0d1c5e00b01733` |
| GEOS-Signatur | `C7 45 CF 53` | `C7 45 CF 53` |
| Dateityp bei 0014h | `PAPR` | `gDOC` |
| Manufacturer-ID bei 0018h | 255 | 255 |
| Creator bei 001Ah | `GEOS` | `GEOS` |
| langer Name ab 0020h | `PAPR` | `gDOC` |
| Ressourcen | 7 | 7 |
| Imports | 1 | 1 |
| Exports | 0 | 0 |
| Import | `ui`, 693.0 | `ui`, 693.0 |

Die Headerbytes zeigen direkt, dass der vierstellige Token und die Manufacturer-ID getrennte Felder sind: Dateityp bei 0014h, Manufacturer-ID bei 0018h, Creator bei 001Ah.

## 3. Ressourcenvergleich

Die Ressourcenpositionen und -größen wurden anhand der GeoWorks-1.x-Geode-Tabellen gelesen. Die Ressourcen 0 bis 2 sind identisch.

| Ressource | PAPR Größe | GDOC Größe | Vergleich / Befund |
|---|---:|---:|---|
| R0 | 0 | 0 | identisch leer |
| R1 | 96 | 96 | byte-identisch |
| R2 | 208 | 208 | byte-identisch; enthält u.a. sichtbaren Text `Exit` |
| R3 | 320 | 320 | gleicher Aufbau; Tokenbytes und einzelne Felder unterscheiden sich |
| R4 | 160 | 160 | verschieden; Moniker-/Grafikdaten |
| R5 | 272 | 256 | verschieden; Moniker-/Grafikdaten |
| R6 | 752 | 816 | verschieden; Moniker-/Grafikdaten |

R3 enthält in beiden Dateien den sichtbaren Text `Icon Maker`. Im eingebetteten Datenbereich steht bei PAPR das Token `PAPR` plus Manufacturer-ID 255, bei GDOC `gDOC` plus 255. Das verbindet die Tokenkennung im Geode-Header mit dem zugehörigen Ressourceninhalt. Die exakte Objektklasse und jedes Feld der UI-Ressource sind damit noch nicht vollständig semantisch dekodiert.

R1 und R2 sind byte-identisch. Der gemeinsame Rahmen importiert nur die UI-Bibliothek. Die Provider unterscheiden sich vor allem durch die Ressourcen, die den jeweiligen Token und die Icon-Grafiken enthalten.

## 4. Icon-Varianten in den Ressourcen 4 bis 6

Die Ressourcen 4, 5 und 6 beginnen jeweils mit einer wiederkehrenden Moniker-Kopfstruktur und den folgenden Kennungen:

| Ressource | PAPR-Kennung | GDOC-Kennung | Abmessungen im Kopf | bisherige Formatkorrelation |
|---|---|---|---|---|
| R4 | `61` | `61` | 48×14 | CGA, 1-Bit |
| R5 | `41` | `41` | 48×30 | HGC, 1-Bit |
| R6 | `46` | `46` | 48×30 | EGA, 4-Bit |

Diese Kennungs-/Formatkorrelation stimmt mit den früheren PAPR-/GDOC-Extraktionsbefunden 2363 überein. Die vorliegende Untersuchung bestätigt sie durch den direkten Vergleich beider originaler Providerdateien. Eine vollständige pixelgenaue Dekodierung der Ressourcen wird hier nicht behauptet.

## 5. Was die Originaldokumentation tatsächlich belegt

`ICONINST.TXT` erklärt ausdrücklich, dass die Providerdateien kleine PC/GEOS-Anwendungen sind und ihr DOS-Dateinamensstamm als Tokenname verwendet wird. Das Beispiel ordnet eine DOS-Erweiterung über `[fileManager] filenameTokens` zu, z.B. `*.BAT = "nBAT",255`.

`DOS_ICON.TXT` unterscheidet davon die Tokenfelder einer GEOS-Datei:
- Dateityp bei Offset 0014h,
- Manufacturer-ID bei Offset 0018h,
- Creator bei Offset 001Ah,
- langer Name ab Offset 0020h.

Es nennt `WDAT` und `DDAT` als native GeoWrite-/GeoDraw-Dokumenttypen, die nur in `TOKEN.DB` vorhanden sind. Das ist ein wichtiger Hinweis: Die gezeigte `filenameTokens`-Zuordnung für DOS-Dateiendungen ist nicht automatisch der Nachweis für die Zuordnung eines nativen GEOS-Dokuments mit numerischer DOS-Endung wie `.000`.

## 6. Konsequenz für GEOTEST

Gesichert:
1. Ein eigener Icon-Provider ist eine kleine GeoWorks-1.x-Geode.
2. Der Provider verwendet einen vierstelligen Dateityp-Token und eine Manufacturer-ID; die Beispiele verwenden 255.
3. Der Provider enthält Icon-Varianten als eigene Ressourcen.
4. Der gemeinsame UI-/Programmrahmen von PAPR und GDOC kann als strukturelle Referenz für die weitere Analyse dienen.

Noch offen:
1. Wie GeoManager den Provider-Token für **native GEOS-Dokumentdateien** anhand von Dateityp und Manufacturer-ID auflöst.
2. Ob und wie ein eigener Eintrag in `TOKEN.DB` erforderlich ist.
3. Ob die Provider-Geode allein genügt oder zusätzlich eine `filenameTokens`-Zuordnung benötigt wird.
4. Wie eine eigene GEOTEST-Dokumentdatei vom File-Manager als GEOS-Dokument erkannt wird.

**Wichtige Korrektur:** Aus dem DOS-Dateierweiterungsbeispiel in `ICONINST.TXT` darf nicht abgeleitet werden, dass `*.GTD = "GTD1",255` bereits die richtige Lösung für native GEOTEST-Dokumente ist. Native GEOS-Dateien haben typischerweise numerische DOS-Endungen; ihr eigener GEOS-Dateikopf enthält Typ und Creator. Die beiden Zuordnungswege müssen getrennt untersucht werden.

## 7. Nächster Schritt

Untersuchung 2421 soll den tatsächlichen File-Manager-/TOKEN.DB-Auflösungspfad in der originalen GeoWorks-1.2-Installation verfolgen: Welche Tokenfelder werden für native GEOS-Dateien gelesen, wie wird der Hersteller berücksichtigt, und wie wird ein passender Moniker aus TOKEN.DB bzw. einer Provider-Geode geladen? Erst wenn dieser Pfad belegt ist, legen wir den GEOTEST-Dokumenttyp und Provider-Token fest.

## 8. Reproduzierbarkeit

Die Header-, Ressourcen- und Größenwerte wurden direkt aus den vier genannten ZIP-Mitgliedern bzw. den beiden Geodes ausgelesen. Originaldateien wurden nicht verändert. Es wurde kein Provider installiert, keine GEOS.INI geändert, keine TOKEN.DB verändert und kein Laufzeittest ausgeführt.
