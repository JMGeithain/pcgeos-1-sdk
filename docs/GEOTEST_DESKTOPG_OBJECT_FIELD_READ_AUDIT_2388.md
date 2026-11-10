# GEOTEST – DESKTOPG.GEO: Leserprüfung der Dateityp-Objektfelder (2388)

Stand: 2026-11-10

## Ziel / Abgrenzung

Fortsetzung der GeoWorks-/PC/GEOS-1.x-Analyse für das native GEOTEST-Dokument. Keine Treiberentwicklung. Die Originaldatei `DESKTOPG.GEO` wurde ausschließlich lesend untersucht.

## 1. Untersuchungsumfang

Die Geode enthält 51 Ressourcen. Die Ressourcenflags wurden aus der Geode-Ressourcentabelle gelesen. Insgesamt besitzen 16 Ressourcen die Flags `0A72h`, die in dieser Geode als ausführbare Code-Ressourcen klassifiziert sind.

Alle 16 Code-Ressourcen wurden separat aus dem Geode extrahiert und als 8086-Code disassembliert. Gesucht wurden direkte Speicheroperand-Zugriffe auf die in Untersuchung 2387 ermittelten Objektfelder:
- `+76h`
- `+78h`
- `+7Ah`
- `+7Ch`
- Statusbyte `+83h`

## 2. Direkte Referenzen auf +76h bis +7Ch

In den 16 Code-Ressourcen findet sich nur eine Stelle, an der die Felder `+76h`, `+78h`, `+7Ah` und `+7Ch` direkt beschrieben werden: die gemeinsame Kopierroutine in Ressource 2 bei Offset `0D17h`.

Dort werden die vier Wörter wie folgt in ein Objekt geschrieben:

| Quelle | Zielobjektfeld | Operation |
|---|---|---|
| `ES:[BP]` | `ES:[DI+7Ah]` | Wortkopie |
| `ES:[BP+2]` | `ES:[DI+7Ch]` | Wortkopie |
| `SS:[BX]` | `ES:[DI+76h]` | Wortkopie |
| `SS:[BX+2]` | `ES:[DI+78h]` | Wortkopie |

In den übrigen disassemblierten Code-Ressourcen wurde kein direkter Lesezugriff auf diese vier Objektfelder mit diesen konstanten Displacements gefunden.

Das ist eine begrenzte, aber wichtige Aussage: Innerhalb der untersuchten DESKTOPG-Code-Ressourcen wird der Feldsatz an dieser Stelle aufgebaut. Ein späterer direkter Verbraucher ist in diesen 16 Code-Ressourcen nicht als Zugriff mit genau diesen festen Feldoffsets sichtbar.

Mögliche Gründe (noch nicht entschieden):
- die Felder werden von einer importierten UI-/Objektklasse interpretiert;
- ein allgemeiner Dispatcher verarbeitet sie indirekt;
- die Werte werden an eine andere Geode/Bibliothek weitergegeben;
- ein späterer Zugriff verwendet einen dynamischen Basiszeiger oder eine andere Strukturansicht.

Keine dieser Möglichkeiten wird derzeit als erwiesene Erklärung ausgegeben.

## 3. Statusbyte +83h

Das Statusbyte `ES:[DI+83h]` wird dagegen an vielen Stellen in den Code-Ressourcen verwendet. Sichtbare Bitoperationen betreffen mindestens:
- Bit `02h`
- Bit `04h`
- Bit `18h` (wird durch die Kopierroutine gemeinsam gesetzt)
- Bit `20h`
- Bit `40h`

Es gibt außerdem Maskierungen wie `AND 7Fh` und `AND BFh`. Die Bedeutung der einzelnen Bits ist ohne Klassen-/Strukturdefinition weiterhin offen.

Die häufigen Tests und Änderungen des Statusbytes zeigen, dass das umgebende Objekt aktiv in Zustands- und Kontrollflussentscheidungen einbezogen wird. Sie beweisen nicht, dass die vier kopierten Wörter selbst Icon-Handles sind.

## 4. Einordnung

Der aktuelle Befund trennt zwei Dinge:
1. **Objektaufbau:** Ressource 2 kopiert zusätzliche Daten aus ES und SS in die Objektfelder `76h–7Ch`.
2. **Objektzustand:** Das Statusbyte `83h` wird an mehreren Codepfaden geprüft und verändert.

Der Icon-/Monikerpfad ist damit noch nicht gefunden. Die Felder `76h–7Ch` bleiben Kandidaten für zusätzliche Dateityp-Metadaten, aber ihre Bedeutung muss durch die importierte Objektklasse, die Objektressource oder die nachgelagerte Bibliothekslogik bestätigt werden.

## 5. Nächste Schritte

1. Die Klassen-/Objektidentität des ES:DI-Datensatzes ermitteln, dessen Felder ab `44h`, `76h` und `83h` beschrieben werden.
2. Die LMem-/Objektressourcen von DESKTOPG auf Klassenreferenzen und Objektinstanzen untersuchen, die zu diesem Datensatz passen.
3. Die von DESKTOPG importierten UI-Klassen und Protokolle der passenden GeoWorks-1.2-Installation identifizieren.
4. Die allgemeine UI-/Objektlogik verfolgen, die Felder `76h–7Ch` auswertet.
5. Den separaten Pfad für app-spezifische Dokumenttypen `WDAT/WP00` und `DDAT/DP00` verfolgen.

## Status

- 16 Code-Ressourcen mit Flags `0A72h` disassembliert.
- Direkte Schreibstelle der Felder `76h–7Ch` in Ressource 2 bestätigt.
- Kein direkter Lesezugriff auf diese vier Felder mit denselben konstanten Displacements in den untersuchten Code-Ressourcen gefunden.
- Statusbyte `83h` wird mehrfach für Kontrollfluss-/Zustandsbits verwendet.
- Objektklasse, semantische Feldnamen und Icon-/Monikerverwendung bleiben offen.
- Keine Originaldatei geändert; kein GEOTEST-Build erstellt; kein Laufzeiterfolg behauptet.
