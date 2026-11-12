# Untersuchung 2444 – ICONMAKE-Modus m: Testpaket für Dummy-Token-Geodes

**Status:** Testpaket erstellt; der DOS-Lauf steht noch aus.

## Ausgangslage

In Untersuchung 2443 wurden aus den Original-Providern `GDOC.000` und `PAPR.000` sechs PCX-Dateien extrahiert. Die Dateien wurden als PCX erkannt und besitzen die erwarteten Profile:

| Profil | Abmessungen | Bildmodus |
|---|---:|---|
| CGA | 48 × 14 | 1 Bit |
| HGC | 48 × 30 | 1 Bit |
| EGA | 48 × 30 | palettiert |

Die Dokumentation `ICONMAKE.ENG` und `ICONMAKE.DOC`, Abschnitt „Tokens from PCX files“, beschreibt den Modus `m` zum Erzeugen einer Dummy-Anwendung aus bis zu drei PCX-Icondateien.

## Testaufbau

Das Paket `ICONMAKE_DummyToken_Test_2444.zip` enthält die unveränderte ICONMAKE.EXE aus dem GeoWorks-Archiv sowie die sechs extrahierten PCX-Dateien. Die Testkennungen sind absichtlich vorläufig und von der endgültigen GEOTEST-Dokumentkennung getrennt:

```dos
ICONMAKE m GTI1,65534 GDOC_CGA.PCX GDOC_HGC.PCX GDOC_EGA.PCX
ICONMAKE m GTI2,65533 PAPR_CGA.PCX PAPR_HGC.PCX PAPR_EGA.PCX
```

Die Zahlen 65534 und 65533 sind isolierte Testwerte. Die Befehle müssen in einem separaten DOSBox-/BaseBox-Testverzeichnis ausgeführt werden.

## Sicherheit und Grenzen

- Keine Ausführung in der produktiven GeoWorks-Installation.
- Keine Änderung oder Löschung der produktiven `TOKEN.DB`.
- Keine Änderung an `GEOS.INI` oder Originaldateien.
- Der genaue Ausgabedateiname und die erzeugte Geode-Struktur werden erst nach dem DOS-Lauf als bestätigt dokumentiert.
- Der Test beweist noch nicht, dass ein mit ICONMAKE erzeugter Dummy bereits die richtige Dokumentdatei-Zuordnung für GEOTEST herstellt.

## Nächster Prüfschritt

Die beiden Befehle ausführen und die erzeugten `.000`-Dateien sowie mögliche Fehlermeldungen zurückgeben. Danach werden Geode-Header, Tokenname, Token-Nummer, Ressourcen und Iconvarianten statisch mit den Originalprovidern verglichen.

## Quelle

- `ICONMAKE.ENG` und `ICONMAKE.DOC`, GeoWorks-Archiv, Abschnitt „Tokens from PCX files“.
- Originalprogramm: `ICONMAKE.EXE`, 19.477 Bytes, SHA-256:
  `72960ca2c01ca1b42813ed530d26a95e1e568d64c954f51ba363261732252933`.
