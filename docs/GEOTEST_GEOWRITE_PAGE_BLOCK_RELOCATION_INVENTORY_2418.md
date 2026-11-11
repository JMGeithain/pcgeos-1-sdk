# GeoWrite 1.x – Relokationsinventar des Seitenblocks 005Ch (Untersuchung 2418)

## Ziel

Systematische Sichtung der LMem-Chunks des ersten Seitenblocks `005Ch` auf Relocation-IDs und Abgrenzung echter Relokationsfelder von zufälligen 16-Bit-Treffern in Text-/Binärdaten.

## Quellen und Methode

- `NEUES_DO.000`, `LEERER_B.000`, `_LEERER_.000`, `TESTWRIT.000`.
- `vm1.py` und `LMem`-Parser aus `/mnt/data/audit2407/`.
- `object.def`, insbesondere `ObjRelocationID` und `ORS_NON_STATE_VM`.
- `convertText.asm`, insbesondere `RelocToVMBlock`.
- Alle aktiven LMem-Chunks im VM-Block `005Ch` wurden auf 16-Bit-Werte mit oberem Nibble `7h` gescannt. Anschließend wurden Treffer anhand ihrer Position, Wiederholung zwischen Dateien und Strukturkontext beurteilt.

## 1. Wichtige Warnung zum Suchverfahren

Ein Scan nach WORD-Werten mit oberem Nibble `7h` ist nur eine Kandidatensuche. Er findet auch zufällige Treffer in Zeichenfolgen oder sonstigen Nutzdaten. Beispielsweise enthält der Text-/Objektdatenbereich von Chunk `003Eh` druckbare Bytes, die paarweise als WORD einen Wert mit oberem Nibble `7h` ergeben. Solche Treffer sind nicht automatisch Relokationen.

Deshalb werden nur Felder als gesicherte Relokationskandidaten gewertet, wenn zusätzlich Feldkontext und die bekannte Objekt-/RunArray-Struktur passen.

## 2. Gesicherte Relokationsfelder im PageContent-Chunk 0022h

In allen vier Dokumenten enthält Chunk `005Ch/0022h` an Payload-Offsets:
- `004Ch`
- `0056h`

jeweils einen WORD-Wert aus dem Bereich `700xh`. Die Werte sind in den untersuchten Dateien `7004h`. In den früheren Showcase-Seiten wurde nachgewiesen, dass diese beiden Felder als `ORS_NON_STATE_VM`-Relocation-IDs auf den jeweils eigenen Seiten-VM-Block zeigen.

Diese zwei Felder sind daher im bekannten PageContent-Kontext gesicherte VM-Relokationsfelder. Sie dürfen nicht als gewöhnliche Chunknummern behandelt werden.

## 3. Relokationsfelder in den seitenlokalen RunArray-Köpfen

Die folgenden Chunks besitzen in allen vier Dokumenten eine 18- bzw. 14-Byte-Struktur, die dem in `convertText.def` beschriebenen 10-Byte-RunArray-Kopf plus Run-Eintrag/Terminator entspricht:

| Chunk | Länge | WORD bei Offset 2 | WORD bei Offset 6 | Interpretation |
|---|---:|---:|---:|---|
| `0028h` | 18 | `7002h` | `7006h` | RunArray-Kopf-Felder mit VM-Relocation-ID-Kandidaten |
| `002Ah` | 18 | `7001h` | `7006h` | RunArray-Kopf-Felder mit VM-Relocation-ID-Kandidaten |
| `002Ch` | 14 | `7007h` | `7006h` | RunArray-Kopf-Felder mit VM-Relocation-ID-Kandidaten |
| `0034h` | 18 | `7002h` | `7006h` | gleiche Struktur wie `0028h` |
| `0036h` | 18 | `7001h` | `7006h` | gleiche Struktur wie `002Ah` |
| `0038h` | 14 | `7007h` | `7006h` | gleiche Struktur wie `002Ch` |

Die Feldpositionen und die wiederholte RunArray-Form machen diese Werte zu strukturell begründeten Relokationskandidaten. Der genaue Ziel-VM-Block jedes einzelnen Kopf-Feldes muss durch Auflösung der Indizes gegen die VM-Handle-Tabelle des jeweiligen Dokuments verifiziert werden, bevor ein Generator diese Werte neu schreibt.

Hinweis: Die beiden Gruppen `0028h/002Ah/002Ch` und `0034h/0036h/0038h` sind im Binärblock getrennte Chunkgruppen. Sie dürfen nicht ohne weitere Objektzuordnung als Duplikate desselben logischen Objekts zusammengefasst werden.

## 4. Nicht als Relokation klassifizierte Treffer

Der automatische Scan findet weitere Werte mit oberem Nibble `7h`, u. a. in:
- Chunk `0020h`, inmitten von Zeichen-/Monikerdaten;
- Chunk `0024h` und `0030h`, die in Teilen strukturierte Seitendaten enthalten;
- Chunks `003Eh` und `0042h`, in denen druckbare Zeichenfolgen und nichttextuelle Bytes gemischt vorkommen.

Diese Treffer werden ausdrücklich **nicht** als Relokationen klassifiziert. Es fehlt der Nachweis, dass sie an einem von der Objektdefinition beschriebenen Relokationsfeld liegen. Das gilt insbesondere für Werte, die zufällig aus ASCII-Bytes wie `r`, `s`, `u` oder anderen druckbaren Zeichen zusammengesetzt werden.

## 5. Bedeutung der Relokations-ID und Auflösung

`object.def` definiert `ObjRelocationID` mit einem 4-Bit-Quellfeld und einem 12-Bit-Index. Für `ORS_NON_STATE_VM` ist der Index ein VM-Tabellenindex. `RelocToVMBlock` in `convertText.asm` maskiert den Index und adressiert den Eintrag der VM-Handle-Tabelle mit `size VMBlockHandle` (12 Byte) und dem Tabellenoffset.

Wichtig: Das bloße Vorkommen von `700xh` sagt nicht, dass das Feld auf denselben Block zeigt. Der Zielblock ergibt sich erst aus dem Index in der konkreten VM-Datei. Die Werte müssen dateispezifisch aufgelöst werden.

## 6. Ergebnis und Grenzen

Gesichert:
- Zwei Relokationsfelder in PageContent `0022h` an Offsets `004Ch` und `0056h`.
- Strukturbedingt weitere Relokations-ID-Kandidaten in den RunArray-Kopf-Chunks `0028h`, `002Ah`, `002Ch`, `0034h`, `0036h`, `0038h`.
- Ein rein numerischer WORD-Scan produziert Fehlalarme; Text-/Monikerdaten dürfen nicht als Relokationen missverstanden werden.
- Die VM-Relokations-ID muss über den 12-Byte-VM-Handle-Tabelleneintrag aufgelöst werden.

Noch offen:
- konkrete Ziel-VM-Handles sämtlicher RunArray-Kopf-Felder in jedem der vier Dokumente;
- die Objektrollen der beiden RunArray-Gruppen innerhalb der Seite;
- die semantische Zuordnung weiterer unbekannter Felder im PageContent-Chunk.

## Konsequenz für GEOTEST

Ein Dokumentgenerator muss bekannte Relokationsfelder als Relokations-IDs behandeln und darf sie nicht als normale Handles/Chunknummern kopieren oder neu berechnen, ohne die VM-Handle-Tabelle einzubeziehen. Unbekannte Treffer aus dem automatischen Scan bleiben unangetastet. Für den ersten Prototyp ist das unveränderte Übernehmen des vollständigen Seitenblocks aus einer Originalvorlage weiterhin der sichere Weg.

## Nicht durchgeführt

- Keine Laufzeitprüfung in GeoWorks.
- Keine Änderung an Originaldokumenten.
- Keine automatische Neuauflösung aller Kandidaten in einen neuen Dokumentcontainer.
- Keine Klassifikation der zufälligen WORD-Treffer in Nutzdaten als Relokationen.

## Reproduzierbarkeit

Die Kandidaten wurden durch Scan aller WORD-ausgerichteten Payload-Positionen in den LMem-Chunks des VM-Blocks `005Ch` gewonnen. Die Klassifikation stützt sich auf Chunkkontext, wiederkehrende Strukturen und die Definitionen in `object.def`/ `convertText.def`. Der reine Scan ist ausdrücklich nicht hinreichend für eine Relokationsbehauptung.
