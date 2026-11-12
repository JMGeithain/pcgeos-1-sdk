# Untersuchung 2443 – ICONMAKE-Extraktion der GDOC- und PAPR-Provider erfolgreich

Datum: 2026-11-12

## Ergebnis

Der in Untersuchung 2442 vorbereitete ICONMAKE-Test wurde vom Nutzer in der DOS-/GeoWorks-Umgebung ausgeführt. Die sechs erwarteten PCX-Dateien liegen vor und wurden hier technisch eingelesen. Alle sechs Dateien werden von einer PCX-Bibliothek fehlerfrei erkannt.

Damit ist die praktische Extraktion der Icon-Provider GDOC.000 und PAPR.000 mit ICONMAKE 1.0 belegt. Die in den vorherigen Untersuchungen aus Provider-Deskriptoren abgeleiteten Icon-Abmessungen werden durch die tatsächlich ausgegebenen PCX-Dateien bestätigt.

## Extrahierte Dateien

| Datei | Größe in Bytes | Pixelmaß | Bildmodus |
|---|---:|---:|---|
| PAPR_CGA(1).PCX | 231 | 48 × 14 | 1 Bit, monochrom |
| PAPR_HGC(1).PCX | 334 | 48 × 30 | 1 Bit, monochrom |
| PAPR_EGA(1).PCX | 967 | 48 × 30 | palettiert |
| GDOC_CGA(1).PCX | 234 | 48 × 14 | 1 Bit, monochrom |
| GDOC_HGC(1).PCX | 309 | 48 × 30 | 1 Bit, monochrom |
| GDOC_EGA(1).PCX | 916 | 48 × 30 | palettiert |

## Sichtbefund

- **PAPR:** Das extrahierte Motiv stellt ein Blatt bzw. Dokument dar. Die CGA- und HGC-Varianten sind monochrom; die EGA-Variante ist farbig.
- **GDOC:** Das extrahierte Motiv zeigt die Buchstaben „DOC“ in einem gerahmten Symbol. CGA und HGC sind monochrom; EGA verwendet eine grüne Darstellung auf hellem Grund.
- Die sechs Bilder entsprechen den erwarteten Profilgrößen: CGA 48 × 14 Pixel, HGC und EGA jeweils 48 × 30 Pixel.

Die EGA-Dateien liegen als palettierte PCX-Bilder vor. Einzelne Paletteinträge bzw. Hintergrundfarben sind nicht ohne Weiteres als transparente Bildbereiche zu interpretieren; dafür wäre eine gesonderte Auswertung des PCX-Paletten-/Darstellungskontexts nötig.

## Prüfsummen

SHA-256:

- PAPR_CGA(1).PCX: `f4cf994249a93c9d3f95617e1d4cce84b52b3c04caf3d2d33f2959fa785d5fa4`
- PAPR_EGA(1).PCX: `897b20853b05d19cd51d1fc78d2e37d8b9e009eb44057a74692a2e0fcf12e1e0`
- PAPR_HGC(1).PCX: `c9d98d2f96d0b91e3e7d0836a6e12bb816b33b1e37f4425ca644930b95b635b5`
- GDOC_CGA(1).PCX: `86e9c89eb37b4e894f910666e144ccdc44a6747fa5573d254ddf8213c8727b06`
- GDOC_EGA(1).PCX: `046b2a9064548b52def856aa46f701c7c547bf55085dc6b84ce04e5030620c3e`
- GDOC_HGC(1).PCX: `b1ea27e764fb6b803f4d91107433dcb43fec6639e075881e8da872d995eace68`

## Bedeutung für das GEOTEST-Projekt

1. ICONMAKE 1.0 kann aus den untersuchten Provider-Dateien die Icon-Grafiken praktisch extrahieren.
2. Die Profilzuordnung aus Untersuchung 2439 (CGA 48 × 14; HGC/EGA 48 × 30) ist durch die PCX-Ausgaben bestätigt.
3. Die Dokument-Provider enthalten tatsächlich unterscheidbare, für den Dateimanager bestimmte Bildmotive.
4. Die Bilder allein beweisen noch nicht, wie GeoWorks 1.x ein neu erzeugtes eigenes Dokument-Token registriert oder wie ein eigener GEOTEST-Dateityp in TOKEN.DB eingebunden werden muss. Diese Frage bleibt getrennt zu untersuchen.
5. Es wurde keine originale TOKEN.DB, GEOS.INI oder GeoWorks-Programmdatei verändert.

## Nächster sinnvoller Schritt

Die sechs PCX-Dateien pixelgenau vergleichen und anschließend den Erzeugungsweg mit ICONMAKE im Modus `m` (PCX zu Dummy-Provider) prüfen. Dabei zunächst ausschließlich in einem separaten Testverzeichnis arbeiten. Das Ergebnis darf erst dann als eigener GEOTEST-Dokument-Provider übernommen werden, wenn Dateiaufbau, Token und GeoWorks-Laufzeitverhalten separat bestätigt sind.

## Bezug

Vorbereiteter Test: `docs/GEOTEST_ICONMAKE_EXTRACTION_TEST_PACKAGE_2442.md`
