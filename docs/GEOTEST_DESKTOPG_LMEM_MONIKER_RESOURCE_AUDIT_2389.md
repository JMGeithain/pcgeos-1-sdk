# GEOTEST – DESKTOPG.GEO: LMem-Objektressourcen und Moniker-Kandidaten (2389)

Stand: 2026-11-10

## Ziel und Abgrenzung

Untersuchung ausschließlich GeoWorks / PC/GEOS 1.x. Ziel bleibt `GEOTEST.GEO` mit einem eigenen nativen Dokument und einem eigenen Dokument-Icon. Keine Treiberentwicklung. Die Originaldatei wurde nur lesend aus `GEOWORKS.zip` extrahiert.

Original:
- `GEOWORKS/SYSAPPL/DESKTOPG.GEO`
- 101.524 Bytes
- SHA-256: `82d547429705e9f9d838c444e9bef8faf493dada68721828dfdf2f373a6b1870`

## 1. Ressourceninventar – Trennung von Code, UI-Text und Grafikdaten

Die Geode-Ressourcentabelle enthält 51 Einträge. Für den hier relevanten Bereich ergibt sich:

| Ressource | Dateioffset | Größe | Flags | Rohbefund |
|---:|---:|---:|---:|---|
| 36 | `F2C0h` | 10.500 | `087Ah` | viele Fehlermeldungen |
| 37 | `11BC4h` | 292 | `087Ah` | UI-Texte, u.a. „VM-Datei“ |
| 38 | `11CE8h` | 212 | `1C7Ah` | kompakter LMem-/Objektblock mit „Datei-Verwalter“ |
| 39 | `11DBCh` | 12.820 | `1C7Ah` | große Grafik-/Moniker-Datenressource |
| 40 | `14FD0h` | 4.180 | `1C7Ah` | Grafikdaten; wiederkehrender 48×30-Pixel-Datensatz |
| 41 | `16024h` | 2.068 | `1C7Ah` | Grafikdaten; u.a. 48×14-Pixel-Datensatz |
| 42–50 | `16838h`–`184F8h` | variabel | `1C7Ah` | weitere kompakte Grafik-/Moniker-Daten |

Die Ressourcentyp-Flags werden hier als Rohwerte dokumentiert. Die genaue symbolische Bedeutung jeder Flagkombination wird nicht aus dem Zahlenwert allein abgeleitet.

## 2. Ressource 38: LMem-Chunk-Verzeichnis

Ressource 38 beginnt bei Dateioffset `11CE8h` und ist 212 Bytes lang. Ihr Anfang:

```
26 00 10 00 00 00 00 00 C4 00 08 00 00 00 00 00
22 00 36 00 4A 00 5E 00 76 00 9E 00 B2 00 00 00
```

Ab relativem Offset `0010h` stehen sieben Chunk-Offets:
`0022h, 0036h, 004Ah, 005Eh, 0076h, 009Eh, 00B2h`.

Vor jedem Chunk-Offet liegt ein 16-Bit-Längenwort. Die Nutzdaten beginnen an den Offsets im Verzeichnis. Die Chunk-Payloads haben in diesem Block folgende Struktur:

| Chunk-Payload ab | Längenwort davor | Länge | Auffälliger Inhalt |
|---:|---:|---:|---|
| `0022h` | `0020h` | 20 | mehrere 16-Bit-Werte, darunter `10C6h`, `0028h`, `102Dh`, `10C1h` |
| `0036h` | `0034h` | 20 | ähnlicher Datensatz mit Varianten `0026h` / `1026h` |
| `004Ah` | `0048h` | 20 | ähnlicher Datensatz mit Varianten `0024h` / `1024h` |
| `005Eh` | `005Ch` | 24 | enthält den nullterminierten Text `Datei-Verwalter` |
| `0076h` | `0074h` | 40 | weiterer Verweis-/Metadatensatz mit mehreren 16-Bit-Werten |
| `009Eh` | `009Ch` | 20 | weiterer strukturierter Datensatz |
| `00B2h` | `00B0h` | 20 | weiterer strukturierter Datensatz |

Das ist ein belastbarer Nachweis für ein LMem-Chunk-Verzeichnis und sieben zugehörige Chunks. Die Daten sind objekt-/UI-artig organisiert. **Die exakten Klassen- und Feldnamen sind damit noch nicht bestimmt.**

## 3. Relocation-Hinweis

Die Geode-Ressourcentabelle weist für Ressource 38 vier Relocation-Bytes aus, also einen Vier-Byte-Eintrag. Der Eintrag lautet roh:
`23 00 00 00`.

Die Quellposition `0023h` liegt innerhalb des ersten Chunk-Payloads (Beginn `0022h`). Das ist ein Hinweis, dass der erste Chunk einen relocierbaren Wert enthält. Ohne die genaue Relocation-Kodierung darf daraus noch keine konkrete Objektklasse oder Zielressource benannt werden.

## 4. Grafik-/Moniker-Kandidaten in Ressourcen 39–50

Die Ressourcen 39–50 enthalten wiederkehrende Bilddatenmuster und Größenfelder. Beispiele:

- Ressource 40: Chunk-Verzeichnis enthält u.a. einen Payload, dessen Anfang nach dem Längenwort die Werte `0030h` und `001Eh` enthält – 48 × 30.
- Ressource 41: ein Payload beginnt nach dem Längenwort mit `0030h` und `000Eh` – 48 × 14.
- In weiteren Ressourcen wiederholen sich strukturierte Bilddatenblöcke.

Das ist ein starker Hinweis, dass diese Ressourcen grafische Moniker-/Bitmap-Daten enthalten. Die konkrete Bildbedeutung (Ordner, Datei, Anwendung, Dokument, Laufwerk usw.) ist noch nicht durch Dekodierung oder Laufzeitdarstellung belegt. Die Ressourcen 39–50 werden daher zunächst als **Grafik-/Moniker-Kandidaten** geführt.

## 5. Verbindung zur Dateityp-Tabelle – derzeitiger Stand

Aus Untersuchung 2385 ist bekannt, dass die Dateityp-Initialisierung in Ressource 8 die allgemeinen Tokens `DESK`, `FLDR`, `FILE`, `gAPP`, `gDAT` und `gDOS` verarbeitet. Untersuchung 2387 zeigte, dass Ressource 2 daraus Objekt-/Datensatzwerte aufbaut.

Untersuchung 2389 ergänzt nun die Ressourcenebene:
- Ressource 38 enthält einen kleinen LMem-Chunk-Verbund mit UI-Text und strukturierten Werten.
- Ressourcen 39–50 enthalten wahrscheinliche grafische Moniker-/Bitmapdaten.
- Die Verbindung zwischen den generischen Tokens, den Chunks aus Ressource 38 und den Bildressourcen 39–50 ist noch nicht abschließend nachgewiesen.

Wichtig: `WDAT/WP00` und `DDAT/DP00` sind anwendungsspezifische Dokumenttokenpaare aus den nativen GeoWrite-/GeoDraw-Dokumentköpfen. Die hier untersuchten generischen Desktop-Tokens ersetzen diese Paare nicht.

## 6. Nächste Schritte

1. Die Relocation-Kodierung des Eintrags `23 00 00 00` anhand anderer Ressourcen mit bekannten Objekt-/Klassenreferenzen vergleichen.
2. Die sieben Chunks von Ressource 38 mit dem tatsächlichen LMem-/Objektformat von GeoWorks 1.x dekodieren.
3. Die Grafikdaten in Ressourcen 39–50 einzeln nach ihrem Bildformat und ihren Moniker-Abmessungen klassifizieren.
4. Die in Ressource 38 enthaltenen Referenzwerte gegen Chunk-Verzeichnisse der Grafikressourcen abgleichen.
5. Erst dann die Zuordnung „Dateityp → Moniker → GeoManager-Symbol“ als belegt dokumentieren.
6. Separat weiter nach dem Weg suchen, über den `WDAT/WP00` und `DDAT/DP00` in die Desktop-Dokumentdarstellung gelangen.

## Status

- Ressource 38 mit sieben LMem-Chunks identifiziert.
- UI-Text „Datei-Verwalter“ einem Chunk zugeordnet.
- Ein Relocation-Eintrag innerhalb des ersten Chunk-Payloads lokalisiert.
- Ressourcen 39–50 als Grafik-/Moniker-Kandidaten eingegrenzt; 48×30 und 48×14 Datenmaße aus Rohfeldern festgestellt.
- Exakte Klassenreferenz, Chunk-Semantik, Bildinhalt und Token-zu-Icon-Verknüpfung bleiben offen.
- Keine Originaldatei geändert; kein GEOTEST-Build erstellt; kein Laufzeiterfolg behauptet.
