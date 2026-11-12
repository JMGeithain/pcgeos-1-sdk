# GEOTEST – Untersuchung 2480
## KLIB.GEO: Format-1-Struktur, Ressourcen, Exporte und Relokationen

Stand: 12.11.2026

## 1. Untersuchungsgrundlage

Datei: `GEOWORKS/SYSTEM/KLIB.GEO` aus dem vom Nutzer bereitgestellten `GEOWORKS.zip`.

- Größe: 55.478 Bytes
- SHA-256: `f7465303446b677690209972caca66fcd83c7651c0dbe74559319ad4053bf90a`
- Signatur: `C7 45 CF 53` (GEODE Format 1)

Der vorhandene Repository-Parser `pcgeos1/geode.py` wurde unverändert angewendet. Er prüft Tabellen- und Ressourcen-Grenzen, Relokationsrecord-Grenzen, Export-Ressourcen-IDs und überlappende Ressourcenspannen.

## 2. Header- und Modulidentität

| Feld | Wert |
|---|---|
| Long name | Kernel Library |
| Permanent name | klib |
| Permanent extension | lib |
| Release | 1.2.8.2 |
| Library protocol | 611.0 |
| Kernel protocol | 622.3 |
| Headerposition | 0xC8 |
| Tabellenende | 0x50A |
| Ressourcentabelle | 0x366 |

## 3. Tabellenumfang

- 42 Ressourcen
- 1 importierte Library
- 142 Exporte
- 1.067 Relokationsrecords

Einziger Import:

| Index | Name | Attribute | Protokoll |
|---:|---|---:|---:|
| 0 | im | 0x4000 | 601.0 |

## 4. Relokationsverteilung

| source | type | Anzahl |
|---:|---:|---:|
| 0 | 0 | 743 |
| 0 | 1 | 94 |
| 0 | 2 | 95 |
| 1 | 4 | 3 |
| 2 | 2 | 46 |
| 2 | 3 | 28 |
| 2 | 4 | 58 |
| **Summe** | | **1.067** |

Die 743 Records mit `source=0/type=0` sind dieselbe Rohwertkombination, die in den Untersuchungen 2469–2474 über viele GeoWorks-1.x-Dateien hinweg unmittelbar auf CALL-FAR-Offsetoperanden abgebildet wurde. Für KLIB.GEO bestätigt die Anwendung des Repository-Parsers 743 solcher Records. Das allein benennt weder die Zielroutine noch die semantische API-Funktion.

## 5. Ressourcenübersicht

| Ressource | Größe | Relokationen | source0/type0 | Exporte | Flags |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | 0x0880 |
| 1 | 368 | 0 | 0 | 0 | 0x0080 |
| 2 | 368 | 23 | 15 | 2 | 0x0A72 |
| 3 | 848 | 15 | 10 | 0 | 0x0A72 |
| 4 | 1472 | 16 | 4 | 2 | 0x0A72 |
| 5 | 2784 | 17 | 13 | 1 | 0x0A72 |
| 6 | 768 | 16 | 14 | 2 | 0x0A72 |
| 7 | 192 | 4 | 4 | 1 | 0x0A72 |
| 8 | 96 | 0 | 0 | 2 | 0x0A72 |
| 9 | 960 | 6 | 3 | 1 | 0x0A72 |
| 10 | 2464 | 81 | 81 | 13 | 0x0A72 |
| 11 | 400 | 16 | 16 | 5 | 0x0A72 |
| 12 | 2304 | 25 | 16 | 1 | 0x0A72 |
| 13 | 4016 | 41 | 22 | 4 | 0x0A72 |
| 14 | 3632 | 2 | 2 | 1 | 0x0A72 |
| 15 | 2096 | 12 | 10 | 4 | 0x0A72 |
| 16 | 416 | 16 | 9 | 2 | 0x0A72 |
| 17 | 4096 | 255 | 71 | 4 | 0x0A72 |
| 18 | 1344 | 43 | 43 | 6 | 0x0A72 |
| 19 | 304 | 4 | 2 | 1 | 0x0A72 |
| 20 | 304 | 20 | 17 | 5 | 0x0A72 |
| 21 | 544 | 33 | 33 | 3 | 0x0A72 |
| 22 | 2672 | 38 | 35 | 1 | 0x0A72 |
| 23 | 1408 | 32 | 26 | 1 | 0x0A72 |
| 24 | 3104 | 61 | 47 | 15 | 0x0A72 |
| 25 | 656 | 12 | 10 | 3 | 0x0A72 |
| 26 | 992 | 4 | 4 | 0 | 0x0A72 |
| 27 | 864 | 14 | 14 | 9 | 0x0A72 |
| 28 | 544 | 25 | 25 | 3 | 0x0A72 |
| 29 | 1216 | 6 | 6 | 1 | 0x0A72 |
| 30 | 496 | 13 | 12 | 2 | 0x0A72 |
| 31 | 1248 | 34 | 30 | 12 | 0x0A72 |
| 32 | 864 | 18 | 18 | 9 | 0x0A72 |
| 33 | 768 | 15 | 14 | 5 | 0x0A72 |
| 34 | 960 | 20 | 14 | 1 | 0x0A72 |
| 35 | 944 | 46 | 32 | 2 | 0x0AC0 |
| 36 | 704 | 24 | 22 | 3 | 0x0A72 |
| 37 | 528 | 5 | 5 | 10 | 0x0A72 |
| 38 | 448 | 27 | 24 | 4 | 0x0A72 |
| 39 | 800 | 26 | 20 | 1 | 0x0A72 |
| 40 | 384 | 1 | 0 | 0 | 0x08C8 |
| 41 | 544 | 1 | 0 | 0 | 0x087A |

Ressource 17 ist mit 4.096 Bytes die größte einzelne Ressource und enthält 255 Relokationsrecords, davon 71 source=0/type=0. Ressource 10 enthält 81 Relokationen, alle 81 source=0/type=0. Ressource 24 enthält 61 Relokationen, davon 47 source=0/type=0. Diese Kennzahlen priorisieren mögliche Codebereiche, identifizieren aber noch keine Geode-Management-Funktion.

## 6. Exporttabelle – Grenzen der Symbolzuordnung

Die Exporttabelle enthält 142 Einträge. Jeder Eintrag liefert nur Exportordinal, Offset und Ressource; symbolische Funktionsnamen sind im Format-1-Exportdatensatz nicht enthalten.

Exportverteilung nach Ressource:

- R2: 2 Export(e), Ordinale 66–67
- R4: 2 Export(e), Ordinale 2–3
- R5: 1 Export(e), Ordinale 4–4
- R6: 2 Export(e), Ordinale 0–1
- R7: 1 Export(e), Ordinale 5–5
- R8: 2 Export(e), Ordinale 59–60
- R9: 1 Export(e), Ordinale 6–6
- R10: 13 Export(e), Ordinale 7–23
- R11: 5 Export(e), Ordinale 12–24
- R12: 1 Export(e), Ordinale 25–25
- R13: 4 Export(e), Ordinale 29–32
- R14: 1 Export(e), Ordinale 33–33
- R15: 4 Export(e), Ordinale 34–37
- R16: 2 Export(e), Ordinale 38–39
- R17: 4 Export(e), Ordinale 40–43
- R18: 6 Export(e), Ordinale 47–53
- R19: 1 Export(e), Ordinale 46–46
- R20: 5 Export(e), Ordinale 54–58
- R21: 3 Export(e), Ordinale 44–52
- R22: 1 Export(e), Ordinale 61–61
- R23: 1 Export(e), Ordinale 62–62
- R24: 15 Export(e), Ordinale 68–82
- R25: 3 Export(e), Ordinale 26–28
- R27: 9 Export(e), Ordinale 83–91
- R28: 3 Export(e), Ordinale 92–94
- R29: 1 Export(e), Ordinale 139–139
- R30: 2 Export(e), Ordinale 138–140
- R31: 12 Export(e), Ordinale 106–119
- R32: 9 Export(e), Ordinale 63–123
- R33: 5 Export(e), Ordinale 95–99
- R34: 1 Export(e), Ordinale 100–100
- R35: 2 Export(e), Ordinale 101–102
- R36: 3 Export(e), Ordinale 103–105
- R37: 10 Export(e), Ordinale 124–133
- R38: 4 Export(e), Ordinale 134–137
- R39: 1 Export(e), Ordinale 141–141

Die nicht zusammenhängenden Ordinalbereiche je Ressource zeigen, dass eine Zuordnung allein über die Ressourcennummer nicht genügt. Die Funktionsnamen GeodeLoad, GeodeLoadResourceAt, GeodeLockResource und GeodeFreeDriver aus der historischen Systemübersicht können daher nicht ohne weitere Evidenz auf konkrete Ordinale gelegt werden.

## 7. Bedeutung für die Suche nach dem GEODE-Lader

KLIB.GEO ist nun strukturell als eigenständige GeoWorks-1.x-Kernel-Library bestätigt. Es besitzt 42 Ressourcen, einen Import (`im`, Protokoll 601.0), 142 Exporte und 1.067 Relokationsrecords. Der Parser hat die Datei ohne Fehler akzeptiert.

Das ist ein belastbarer Kandidat für die weitere Untersuchung der in der historischen PC/GEOS-Systemübersicht getrennt aufgeführten Geode-Management-Funktionen. Noch nicht bewiesen ist, dass die gesuchten Funktionen in KLIB.GEO implementiert sind oder welche Exportordinalen ihnen entsprechen.

Die nächste technische Aufgabe ist, die Exportziele in KLIB.GEO mit den tatsächlichen Codebereichen zu verknüpfen und die Ressourcen mit besonders vielen CALL-FAR-Relokationen zu untersuchen. Parallel muss die eine importierte Library `im` im Archiv identifiziert und ihr Protokoll-/Exportbezug geprüft werden. Funktionsnamen werden erst nach Kontrollfluss- und Aufrufkontextabgleich vergeben.

## 8. Antwort zur Neubaufrage: GEOTEST.GEO kann bereits gebaut werden

Der SDK-README und `docs/GEOTEST_RUNTIME_TEST.md` dokumentieren bereits einen erfolgreichen Build und einen erfolgreichen Starttest:

- GEOTEST.GEO wurde am 09.11.2026 in GeoWorks 1.2 gestartet.
- Dateigröße: 70.794 Bytes.
- SHA-256: `9ace19da2535a1f05875f891876417bc8adafbdbce2b32540131fa85f638408b`.
- Hauptfenster und Help-Dialog sind im Nutzer-Screenshot sichtbar; der Nutzer meldete „es geht alles“.
- Das Projekt liegt in `examples/geotest/`; Projektdatei und C-Quelltext sind im Repository vorhanden.

Daher lautet die präzise Antwort: Ein neues GEOTEST.GEO mit dem bestehenden Funktionsumfang kann jetzt erneut gebaut werden. Die vollständige GEODE-Laderanalyse ist dafür keine Voraussetzung.

Wenn mit „neue GEO“ die nächste Version gemeint ist, die ein echtes Dokument erzeugt und diesem ein eigenes Icon zuordnet, ist dieser Funktionsumfang noch nicht fertig. Dafür fehlen weiterhin ein nachgewiesener Dokument-Erzeugungs-/Speicherpfad und die verifizierte Dokumenttyp-/Icon-Provider-Zuordnung. Der nächste sinnvolle Build ist ein kleiner Zwischenschritt: bestehende GEOTEST-Anwendung reproduzierbar neu bauen, danach einen isolierten Dokument-Erzeugungstest ergänzen, und erst anschließend das Dokument-Icon einbinden.

## 9. Änderungen und Tests

- Keine Änderung an KLIB.GEO oder am GEODE-Parser.
- Keine Änderung an SDK-Quellcode.
- Kein neuer Build in dieser Untersuchung.
- Kein GeoWorks-Laufzeittest in dieser Untersuchung.
- Statische Format-1-Prüfung mit dem vorhandenen Repository-Parser erfolgreich.

## 10. Versionsabgrenzung

Nur GeoWorks 1.x / PC/GEOS 1.x. Die Datei besitzt Format-1-Signatur `C7 45 CF 53` und Kernel-Protokoll 622.3. PC/GEOS 2.x-/FreeGEOS-Implementierungen wurden nicht als Belege herangezogen.
