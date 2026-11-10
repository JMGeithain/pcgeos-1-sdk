# GEOTEST – Token-Paar in GeoWrite/GeoDraw: LMem-Chunk-Prüfung (2376)

Stand: 2026-11-10

## Ziel und Abgrenzung

Weiterhin ausschließlich GeoWorks / PC/GEOS 1.x. Ziel ist die native Testanwendung `GEOTEST.GEO`, die ein eigenes natives Dokument erzeugt, speichert, schließt und wieder öffnet und dessen Datei im GeoManager ein eigenes Symbol erhält.

Kein Grafiktreiber wird entwickelt oder geändert. `NOTEPAD.GEO` bleibt wegen seiner DOS-ASCII-Dateien ausdrücklich keine Vorlage für native GEOS-Dokumente. Es wurden keine Originaldateien verändert und kein neuer GEOTEST-Build erzeugt.

## Untersuchungsgrundlage

Die folgenden Original-Geodes wurden read-only aus dem bereitgestellten GeoWorks-Installationsarchiv untersucht:

| Datei | Größe | SHA-256 | App-Token im Header |
|---|---:|---|---|
| `WRITE.GEO` | 73.110 Bytes | `0d2958b810948603d15e412a61598623b9a4ccb73cfeb9fbe08d50ee718a6fd0` | `WP00` |
| `DRAW.GEO` | 31.624 Bytes | `9b980dd04175d3c901835a96bc7b40f7a36f92f0b4fc66f0609300a11d04d70` | `DP00` |

Beide sind GEOS-1.x-Geodes. Die Analyse erfolgte über die Ressourcen- und Relocationtabellen sowie Byte-/Hex-Dumps der betreffenden Ressourcen.

## 1. Token-Paare liegen in LMem-Objektressourcen

Die Fundstellen aus Untersuchung 2375 wurden nun auf die Ressourcengrenzen und LMem-Struktur bezogen:

| Anwendung | Ressource | Ressourcentyp laut Flags | Datei-Offset des ersten Tokens | Token-Paar |
|---|---:|---|---:|---|
| GeoWrite | 9 | LMem, OBJECT, UI | `9A4Ch` | `WDAT 00 00 WP00 00 00` |
| GeoDraw | 6 | LMem, OBJECT, UI | `27DAh` | `DDAT 00 00 DP00 00 00` |

Die beiden Token-Paare liegen somit nicht in den ausführbaren Code-Ressourcen, sondern innerhalb von LMem-Objekt-/UI-Ressourcen.

Die Token beginnen innerhalb ihrer Ressource bei:
- WRITE.GEO, Ressource 9: relativ `035Eh`
- DRAW.GEO, Ressource 6: relativ `072Ah`

In beiden Fällen folgt auf das erste Vier-Byte-Token nach zwei Nullbytes das jeweilige App-Token, ebenfalls gefolgt von zwei Nullbytes.

## 2. Relocation-Befund – und seine Grenze

- WRITE.GEO, Ressource 9: Die Ressource besitzt laut geparster Relocation-Tabelle genau einen Relocation-Eintrag. Dessen Quellposition liegt am Ressourcenanfang (relativ `0000h`), nicht an der Token-Fundstelle.
- DRAW.GEO, Ressource 6: Die Ressource besitzt neun Relocation-Einträge. Keiner dieser Einträge liegt an den Bytes der Token-Paar-Fundstelle.
- Die Token-Paare sind damit im vorliegenden Rohdatenbefund keine unmittelbar relocierten 16-Bit-Zeigerfelder.

Wichtig: Aus diesem Befund folgt **nicht**, dass die Tokens unbenutzt sind. Ein Codepfad kann Ressourcen-/Chunkdaten zur Laufzeit durchsuchen oder über andere Objekt-/Chunkreferenzen erreichen. Der vorliegende Relocation-Scan allein beweist aber weder einen Aufruf noch eine Registrierung.

## 3. Was sich daraus ableiten lässt

Der Vergleich zweier unterschiedlicher nativer GeoWorks-1.x-Anwendungen zeigt dieselbe Anordnung:

- GeoWrite: App-Token `WP00`, zusätzliches Token `WDAT`
- GeoDraw: App-Token `DP00`, zusätzliches Token `DDAT`

Das stützt die Arbeitshypothese, dass das erste Token eine anwendungsspezifische Daten-/Dokumentkennung und das zweite Token die zugehörige Anwendung bezeichnet. Es ist eine strukturelle Korrelation über zwei Anwendungen, aber noch kein vollständiger semantischer Nachweis.

**Noch nicht bewiesen sind insbesondere:**
1. ob `WDAT` / `DDAT` tatsächlich die Dokumentdateitypkennung oder eine andere interne Kennung ist;
2. ob und wie diese Struktur vom GeoManager gelesen wird;
3. welche API oder Kernel-/UI-Routine die Dokumentkennung registriert;
4. ob das Dokument-Icon über diese Struktur, eine separate Moniker-/Dokumentklasse oder eine weitere Registrierung zugeordnet wird;
5. welche Dateikopfstruktur ein gültiges GeoWrite-Dokument auf der Platte besitzt.

Die Bezeichnung „Dokument-Token“ bleibt daher bis zur Code- oder Laufzeitbestätigung eine Hypothese.

## 4. Konsequenz für GEOTEST

Der vorhandene experimentelle Build `GEOTEST.GEO` trägt das App-Token `GTS1` im Geode-Header. In ihm wurde bisher kein entsprechendes, belegtes Gegenstück zu `WDAT` oder `DDAT` gefunden.

Es wird **noch kein Token wie `GDAT`, `GTD1` oder eine andere frei gewählte Kennung festgelegt**. Erst muss die tatsächliche Semantik und der benötigte 1.x-Registrierungsweg aus GeoWrite bzw. GeoDraw nachgewiesen werden.

## 5. Nächster notwendiger Schritt

Der nächste Durchgang muss vom vermuteten Dokumentobjekt aus in den ausführbaren Code führen:

1. LMem-Chunk-Tabelle und Chunk-IDs der Token-tragenden Bereiche exakt kartieren.
2. Die zugehörigen Objekt-/Klassenstrukturen identifizieren; insbesondere feststellen, ob der Token-tragende Chunk Teil eines Dokumentkontrollobjekts, eines Dokumentmonikers oder einer anderen UI-Struktur ist.
3. In den Code-Ressourcen die Erzeugungs-/Öffnungs-/Speicherpfade sowie Nachrichten an diese Objekte verfolgen.
4. Die dabei verwendeten UI-/Kernel-/Spool-Ordinale gegen die tatsächlich vorhandenen GeoWorks-1.2-Bibliotheken und Protokolle validieren.
5. Nach Möglichkeit eine echte, sicher identifizierte GeoWrite-Dokumentdatei untersuchen und Header-/Dateistruktur mit den Lade-/Speicherroutinen abgleichen.
6. Erst nach diesem Nachweis den minimalen nativen Dokument-Lifecycle in GEOTEST implementieren; Icon-Zuordnung separat anhand des belegten Monikerpfads ergänzen.

## Ergebnisstatus

- Token-Paare in zwei GeoWorks-1.x-Geodes bestätigt.
- Einbettung in LMem-Objekt-/UI-Ressourcen bestätigt.
- Direkte Relocation an den Tokenbytes nicht gefunden.
- Semantik der Tokens, Dokumentdateistruktur, Registrierungs-API und Icon-Pfad noch offen.
- Keine Änderungen an Originaldateien; kein Laufzeiterfolg behauptet.
