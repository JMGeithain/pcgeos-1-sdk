# Untersuchung 2433 – Bytegenauer Korrekturaudit der Provider-Ressourcenbereiche

## Anlass und Korrektur

Die Aussage in Untersuchung 2432, die ersten drei Ressourcenbereiche seien über sieben Provider-Geodes vollständig byteidentisch, war zu pauschal und teilweise falsch. Eine erneute direkte Prüfung der Bytes aus `GEOWORKS.zip` korrigiert diesen Befund.

**Korrektur:** Nur der erste Bereich ist über alle sieben verglichenen Dateien vollständig byteidentisch. Der zweite Bereich ist fast identisch, der dritte Bereich ist deutlich providerabhängig.

Diese Korrektur ersetzt die entsprechende Aussage in Untersuchung 2432.

## Dateien und Verfahren

Verglichen wurden die Dateien aus `GEOWORKS/WORLD/PROGRAMM.E/ICONEDIT.OR/`:

- GDOC.000
- PAPR.000
- BEER.000
- BILL.000
- BUTN.000
- ZIPR.000
- GEXE.000

Die Ressourcenzielpositionen wurden aus den sieben 32-Bit-Tabelleneinträgen ab Dateioffset `0x13C` berechnet. Die Werte sind relativ zur Geode-Basis `0x100`. Verglichen wurden die drei Bereiche:

- Bereich 1: `0x274–0x2DB` (104 Byte)
- Bereich 2: `0x2DC–0x3AF` (212 Byte)
- Bereich 3: `0x3B0–0x4F3` (324 Byte)

Für jeden Bereich wurde die Anzahl der Bytes gezählt, die gegenüber dem entsprechenden Bereich von `GDOC.000` abweichen.

## Bytevergleich

| Datei | Bereich 1: Abweichungen | Bereich 2: Abweichungen | Bereich 3: Abweichungen |
|---|---:|---:|---:|
| GDOC.000 | 0 | 0 | 0 |
| PAPR.000 | 0 | 4 | 122 |
| BEER.000 | 0 | 4 | 118 |
| BILL.000 | 0 | 4 | 162 |
| BUTN.000 | 0 | 4 | 120 |
| ZIPR.000 | 0 | 4 | 132 |
| GEXE.000 | 0 | 3 | 154 |

## Interpretation

### Bereich 1 – gemeinsamer unveränderter Inhalt

Die 104 Bytes von `0x274` bis `0x2DB` sind in allen sieben Dateien byteidentisch. Das ist ein belastbarer gemeinsamer Abschnitt. Seine genaue semantische Rolle ist noch nicht bestimmt.

### Bereich 2 – fast gemeinsamer Inhalt

Bei PAPR, BEER, BILL, BUTN und ZIPR unterscheiden sich genau vier Bytes gegenüber GDOC. Bei GEXE sind es drei Bytes. Die erste Abweichung liegt jeweils im Bereichsindex 40 bis 43 (relativ zum Bereichsbeginn), bei GEXE im Bereichsindex 41 bis 43.

Das Muster spricht für einen weitgehend gemeinsamen Bereich mit wenigen providerabhängigen Feldern. Es ist noch nicht geklärt, ob diese Bytes Parameter, Verweise, Prüfsummen oder andere Metadaten enthalten.

### Bereich 3 – providerabhängiger Inhalt

Im 324-Byte-Bereich gibt es zwischen GDOC und den anderen Dateien zahlreiche Abweichungen: 118 bis 162 Bytes. Dieser Bereich kann deshalb nicht als vollständig gemeinsamer Inhalt beschrieben werden. Er könnte Code, Daten, Ressourcenmetadaten oder eine Mischung enthalten; die Klassifikation bleibt offen.

## Konsequenz für die Icon-Dekodierung

Die Korrektur verändert die Analysepriorität:

1. Bereich 1 bleibt als gemeinsamer Abschnitt markiert.
2. Bereich 2 sollte bytegenau auf die wenigen veränderlichen Felder untersucht werden.
3. Bereich 3 darf nicht pauschal als gemeinsames Grundgerüst ausgeblendet werden.
4. Die eigentlichen Icon-Kandidaten ab `0x4F4` müssen weiterhin unabhängig anhand ihrer Struktur dekodiert werden.

Die Abweichungszahlen allein identifizieren keine Bitmapressource und beweisen kein RLE-Format. Eine CGA-, HGC/MCGA- oder EGA-Zuordnung ist weiterhin nicht bestätigt.

## Konsequenz für GEOTEST

Für die Entwicklung einer eigenen Provider-Geode ist es wichtig, den gemeinsamen Teil nicht zu groß anzusetzen. Eine spätere Vorlage darf nicht einfach drei vermeintlich identische Bereiche übernehmen. Vor einer Konstruktion muss geklärt sein, welche Bytes strukturell zwingend sind und welche pro Token beziehungsweise Provider angepasst werden müssen.

## Methodik und Grenzen

- Direkter byteweiser Vergleich der Originaldateien aus `GEOWORKS.zip`.
- Ausschließlich lesende Analyse; keine Originaldatei wurde verändert.
- Kein Laufzeittest in GeoWorks.
- Die Zahlen geben Byteabweichungen gegenüber GDOC.000 an; sie sind keine semantische Dekodierung.
