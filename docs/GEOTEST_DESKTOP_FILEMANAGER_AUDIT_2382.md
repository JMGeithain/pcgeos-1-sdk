# GEOTEST – GeoManager-/Dateiverwaltungs-Spur in DESKTOPG.GEO (2382)

Stand: 2026-11-10

## Ziel und Abgrenzung

Weiterhin ausschließlich GeoWorks / PC/GEOS 1.x. Ziel ist eine native GEOTEST-Anwendung mit eigenem Dokument, Speichern/Wiederöffnen und eigenem Dokument-Icon. Keine Treiberentwicklung. Die untersuchten Dateien wurden nur lesend aus `GEOWORKS.zip` extrahiert; keine Originaldatei wurde verändert.

## 1. Neue relevante Referenz: DESKTOPG.GEO

Die Systemanwendung `GEOWORKS/SYSAPPL/DESKTOPG.GEO` ist mit 101.524 Bytes im Archiv enthalten.

- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`
- ASCII-String `File Cabinet` bei Datei-Offset `0020h`
- ASCII-String `fileManager` bei `5BBBh`
- ASCII-String `filenameTokens` bei `5BC7h`
- UI-Text `VM-Datei` bei `11BFAh`

Diese Strings machen DESKTOPG zu einem konkreten Kandidaten für die weitere Untersuchung der GeoManager-Dateierkennung und Darstellung. Sie beweisen für sich allein noch nicht, welche Routine die Typ-/Creator-Tokens auswertet oder wie das Icon ausgewählt wird.

## 2. Token-Suche in DESKTOPG.GEO

In der gesamten Datei wurden die Bytefolgen `WDAT`, `DDAT`, `WP00` und `DP00` nicht gefunden.

Das bedeutet: Die vier anwendungsspezifischen Kennungen sind nicht als Klartextkonstanten in DESKTOPG.GEO enthalten. Der Dateimanager kann die Token daher beispielsweise über allgemeine Headerfelder, dynamische Tabellen oder Kernel-/Bibliotheksdienste verarbeiten; welche Möglichkeit zutrifft, ist noch offen.

Es wäre nicht zulässig, aus dem Fehlen der ASCII-Token zu folgern, dass DESKTOPG die Token nicht verarbeitet.

## 3. Vergleich mit Systembibliotheken

Zusätzlich wurden die Dateien `KLIB.GEO`, `UI.GEO`, `STREAM.GEO` und `SPOOL.GEO` auf dieselben vier Token sowie ausgewählte VM-/Datei-Strings geprüft.

| Datei | Größe | SHA-256 | Relevanter Rohbefund |
|---|---:|---|---|
| `KLIB.GEO` | 55.478 | `f7465303446b677690209972caca66fcd83c7651c0dbe74559319ad4053bf90a` | keine Token-ASCII-Treffer |
| `UI.GEO` | 87.900 | `13a3a82ec3d4373b120890a11eb09b3a9f9ec456ca633819728f53c07883c73a` | keine Token-ASCII-Treffer; ein Treiberfehlermeldungsstring |
| `STREAM.GEO` | 2.410 | `7632772554b8d6c5c7bb08d5c94f399de34de81674179ea2f8842d312a3f281c` | enthält `Stream Driver`; keine Token-ASCII-Treffer |
| `SPOOL.GEO` | 43.480 | `71f38fac43c75440299a954dd562a970ae4dd0cbc1d25143b98c79dddd983abb` | Druck-/Spool-UI; keine Token-ASCII-Treffer |

Die Strings in diesen Ressourcen sind kein vollständiger Ersatz für eine Analyse der Geode-Import-/Exporttabellen oder des ausführbaren Codes. Insbesondere ist der String `Stream Driver` kein Beweis für den VM-Dokumentdatei-Lifecycle.

## 4. GEODECK.VM

Die Datei `GEOWORKS/SYSTEM/GEODECK.VM` ist 188.556 Bytes groß und beginnt mit derselben GEOS-VM-Kennung `C7 45 CF 53`. Ihr Kopf enthält Typ-/Creator-Felder `DECK/CARD` und den Namen `GeoWorks Default Deck`.

Die vier Paare `WDAT`, `DDAT`, `WP00`, `DP00` sowie die Namen GeoWrite/GeoDraw wurden in dieser Datei nicht als ASCII-Zeichenfolgen gefunden. Die Datei ist daher kein unmittelbarer Nachweis der Dokumenttyp-/Iconregistrierung für GeoWrite/GeoDraw. Ihre Rolle als Deck-/Karten-Datei ist von der eigentlichen Dokumentregistrierung zu trennen.

## 5. Nächste technische Untersuchung

Die nächste Arbeit soll auf DESKTOPG.GEO fokussieren:

1. Geode-Header, Ressourcenverzeichnis und Import-/Exporttabellen der Desktop-Anwendung vollständig dekodieren.
2. Die Ressourcen identifizieren, die `fileManager` und `filenameTokens` enthalten.
3. Die betreffenden LMem-Chunks und ihre Objekt-/Klassenreferenzen zuordnen.
4. Von diesen Objekten in den Code springen und verfolgen, wie Dateiköpfe und Typ-/Creator-Informationen gelesen werden.
5. Erst danach den Moniker-/Icon-Auswahlpfad für unbekannte bzw. registrierte Dokumenttypen verfolgen.
6. Parallel die WRITE.GEO-Speicherpfade mit den gefundenen allgemeinen Datei-/VM-Aufrufen verbinden.

## Status

- DESKTOPG.GEO als konkrete GeoManager-/Dateimanager-Referenz identifiziert.
- Dateimanager-bezogene Strings und ihre Offsets bestätigt.
- Typ-/Creator-Token als ASCII nicht in DESKTOPG.GEO oder den vier geprüften Systembibliotheken gefunden.
- Keine konkrete Dateityp- oder Iconroutine identifiziert.
- Kein GEOTEST-Dokumentformat implementiert, keine Originaldatei verändert und kein Laufzeiterfolg behauptet.
