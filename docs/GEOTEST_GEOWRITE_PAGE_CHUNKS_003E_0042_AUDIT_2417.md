# GeoWrite 1.x – Untersuchung der Seitenchunks 003Eh und 0042h (Untersuchung 2417)

## Ziel

Die zwei 143-Byte-Chunks `003Eh` und `0042h` des ersten Seitenblocks `005Ch` genauer vergleichen und prüfen, ob sie sich sicher Header, Footer oder Haupttextobjekten zuordnen lassen.

## Quellen und Methode

- Originaldateien `NEUES_DO.000`, `LEERER_B.000`, `_LEERER_.000` und `TESTWRIT.000` unter `/mnt/data/audit2409/`.
- Parser `/mnt/data/audit2407/vm1.py`.
- Die bereits dokumentierte Traversierungslogik in `convertGeoWrite.asm`.
- Hexdump- und ASCII-Ansicht der vollständigen LMem-Payloads von `005Ch/003Eh` und `005Ch/0042h`.
- Statische Analyse; keine Laufzeitprüfung.

## 1. Gemeinsamer Aufbau

In allen vier Dokumenten sind beide Chunks jeweils 143 Byte groß. Die ersten 27 Bytes sind bei `003Eh` und `0042h` weitgehend gleichartig aufgebaut und enthalten u. a. die wiederkehrenden Werte `001Ah`, `00FFh`, `007Fh` und `0027h`. Ab Payload-Offset `1Bh` beginnen die Daten, die sich zwischen den Dokumenten stark unterscheiden.

Die identische Länge ist ein Hinweis auf eine gemeinsame Objekt-/Datenstruktur oder einen festen Datenpuffer. Sie beweist keine bestimmte Objektklasse.

## 2. Chunk 003Eh

Die Payload von `NEUES_DO.000` enthält ab Offset `1Dh` lesbare Fragmente:
- `llkommen`
- `a#4`
- `Wählen`
- `ie aus dem N`
- `behör`

Das legt nahe, dass in diesem Chunk zumindest teilweise Zeichen- bzw. darstellungsbezogene Daten abgelegt sind. Die Zeichen sind jedoch nicht als ein einfacher fortlaufender ASCII-Textstrom organisiert: Zwischen den Fragmenten liegen zahlreiche Steuer-/Metadatenbytes und weitere Werte.

In `TESTWRIT.000` ist derselbe Chunk stark verändert und enthält vor allem Musterbytes und Zahlenwerte. In `LEERER_B.000` besteht er überwiegend aus wiederkehrenden `77h`-/`88h`-Mustern. In `_LEERER_.000` sieht die Payload eher wie strukturierte Maschinen-/Objektdaten aus. Daher ist eine pauschale Deutung als Headertext, Footertext oder Textcache nicht belegt.

## 3. Chunk 0042h

Chunk `0042h` enthält in `TESTWRIT.000` die sichtbare Zeichenfolge `Carta-Thiu` an Payload-Offset `0x5F`. In `NEUES_DO.000` steht an späterer Stelle die Bytefolge `ABCDEFG` und danach `JKLMNOPQRST`. Diese Fragmente könnten Test-/Moniker-/Zeichendaten sein; ihre genaue Funktion ist aus den Bytes allein nicht bestimmbar.

Die übrigen Bytes in `0042h` sind stark strukturiert und enthalten viele nichtdruckbare Werte. Der Chunk ist deshalb ebenfalls kein einfacher Textpuffer. In den anderen beiden Dokumenten unterscheiden sich seine Inhalte erheblich.

## 4. Abgleich mit der Objektverkettung

`convertGeoWrite.asm` belegt die logische Traversierung PageContent → Header → Footer → Spaltenobjekte. Die Quelle benennt dabei die Felder `CP_firstChild` und `LP_next`, aber das derzeit verfügbare Quellmaterial enthält nicht alle benötigten vollständigen 1.x-Strukturdefinitionen, um die 143-Byte-Payloads anhand ihrer Bytepositionen eindeutig einem konkreten Objekt in der Kette zuzuordnen.

Insbesondere wurde **kein** belastbarer Nachweis gefunden, dass Chunk `003Eh` der Header oder Chunk `0042h` der Footer ist – oder umgekehrt. Auch eine Zuordnung als Haupttext-/Spaltenobjekt wäre derzeit eine Vermutung.

## 5. Ergebnis

Gesichert:
- Beide Chunks sind in den vier untersuchten Dateien 143 Byte groß.
- Beide enthalten dokumentabhängige, strukturierte Daten.
- In einzelnen Beispielen kommen lesbare Zeichenfragmente vor, eingebettet in nichttextuelle Daten.
- Sie dürfen nicht als entbehrliche Cacheblöcke oder reine Textpuffer behandelt werden.
- Die Konverterquelle beschreibt eine Objektkette, liefert im vorhandenen Material aber keine vollständige Bytefeldzuordnung zu diesen Chunks.

Nicht gesichert:
- konkrete Objektklasse von `003Eh` und `0042h`;
- Zuordnung zu Header, Footer oder Spaltenobjekt;
- Bedeutung der lesbaren Zeichenfolgen;
- ob diese Bereiche beim Öffnen durch GeoWrite neu aufgebaut oder als persistente Objektdaten benötigt werden.

## Konsequenz für GEOTEST

Beide Chunks müssen in einem ersten Dokumentprototyp unverändert aus einer geprüften Originalvorlage übernommen werden. Sie dürfen nicht gelöscht, auf Null gesetzt oder mit eigenem Text überschrieben werden. Die nächste sinnvolle Untersuchung ist eine strukturierte Gegenüberstellung der kompletten Objekt-/Chunk-Relokationen im Seitenblock und der 1.x-Objektdefinitionen, nicht das Erraten der Chunkrolle anhand einzelner lesbarer Bytes.

## Nicht durchgeführt

- Kein Dokument erzeugt oder geändert.
- Kein GeoWorks-Laufzeittest.
- Keine Klassifikation der Chunks als Header/Footer/Spaltenobjekt.
- Keine Originaldatei verändert.

## Reproduzierbarkeit

Die Bytefolgen und Zeichenfragmente stammen aus den vollständigen 143-Byte-Payloads der genannten LMem-Chunks im VM-Block `005Ch`. Die Traversierungslogik stammt aus `ConvertOldGeoWriteDocument` in `convertGeoWrite.asm`.
