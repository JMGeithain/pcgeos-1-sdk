# Untersuchung 2446 – Icon-Deskriptoren in den ICONMAKE-Dummy-Providern

## Ziel

Die von ICONMAKE 1.0 erzeugten Dateien `GTI1FFFE.000` und `GTI2FFFD.000` wurden auf wiederkehrende Deskriptor-Signaturen untersucht und mit den Original-Providern `GDOC.000` und `PAPR.000` verglichen.

Alle Offsets in dieser Dokumentation sind absolute Dateioffsets, sofern nicht ausdrücklich anders angegeben.

## 1. Vier Deskriptoren mit Signatur `23 00 00 00`

In allen vier Dateien wurden die folgenden Einträge gefunden:

| Typfeld | GTI1-Offset | GTI2-Offset | GDOC-Offset | PAPR-Offset |
|---|---:|---:|---:|---:|
| 03 | `0x2AC` | `0x2AC` | `0x2AC` | `0x2AC` |
| 04 | `0x3F0` | `0x3F0` | `0x3F0` | `0x3F0` |
| 05 | `0x494` | `0x494` | `0x494` | `0x494` |
| 06 | `0x598` | `0x5A8` | `0x598` | `0x5A8` |

Die Signatur allein ist kein Beweis für die vollständige Semantik des Datenformats. Die Typwerte 04, 05 und 06 sind aber in allen vier Dateien an den aus der vorherigen Untersuchung bekannten Stellen wiederzufinden.

## 2. Abmessungsfelder

Die 16-Bit-Werte an den relativen Deskriptorpositionen +0x36 und +0x38 ergeben folgende Maße:

| Typ | +0x36 | +0x38 | Abmessung |
|---|---:|---:|---:|
| 04 | 48 | 14 | 48 × 14 Pixel |
| 05 | 48 | 30 | 48 × 30 Pixel |
| 06 | 48 | 30 | 48 × 30 Pixel |

Diese Werte stimmen mit den tatsächlich von ICONMAKE extrahierten PCX-Dateien überein:
- CGA: 48 × 14, monochrom
- HGC: 48 × 30, monochrom
- EGA: 48 × 30, palettiert

Damit ist die Zuordnung der drei Deskriptortypen zu den drei Größenprofilen in den vier untersuchten Providerdateien konsistent. Die Bildschirmtyp-Zuordnung stützt sich zusätzlich auf die ICONMAKE-Dokumentation und die verwendeten Dateinamen; die numerischen Typwerte selbst sind damit noch nicht semantisch vollständig entschlüsselt.

## 3. Format-/Kennfeld +0x3A

| Typ | GTI1 | GTI2 | GDOC | PAPR |
|---|---:|---:|---:|---:|
| 04 | `0x0001` | `0x0001` | `0x0001` | `0x0001` |
| 05 | `0x0001` | `0x0001` | `0x0001` | `0x0001` |
| 06 | `0x1101` | `0x1101` | `0x1101` | `0x1101` |

Die Unterscheidung zwischen den Werten 0001h und 1101h ist reproduzierbar. Eine genaue Interpretation aller Bits wird hier nicht behauptet. Dass Typ 06 das EGA-Farbprofil repräsentiert, ist durch die korrespondierenden PCX-Extraktionen und die ICONMAKE-Dokumentation gestützt.

## 4. Weitere variierende Felder

Das Wort bei +0x0C ist je nach Provider und Typ unterschiedlich:

| Typ | GTI1 | GTI2 | GDOC | PAPR |
|---|---:|---:|---:|---:|
| 04 | `0x0094` | `0x0098` | `0x0094` | `0x0098` |
| 05 | `0x00F4` | `0x010C` | `0x00F4` | `0x010C` |
| 06 | `0x0330` | `0x02F0` | `0x0330` | `0x02F0` |

Diese Werte könnten relative Verweise oder Größen-/Positionsangaben sein. Ihre Bezugsbasis und genaue Funktion sind mit diesem Vergleich allein nicht geklärt. Sie dürfen daher noch nicht als Dateioffsets oder Ressourcennummern interpretiert werden.

Auch die Felder +0x3C und +0x3E variieren. Sie wurden erfasst, aber nicht semantisch benannt.

## 5. Ressourcenzuordnung: was bereits feststeht

- Die Deskriptoren 04 und 05 liegen im gemeinsamen Ressourcenbereich, der bei allen vier Dateien bei `0x3B0` beginnt.
- Bei GDOC/GTI1 liegt der Deskriptor 06 bei `0x598`; bei PAPR/GTI2 liegt er bei `0x5A8`.
- Die unterschiedlichen Startpositionen ergeben sich aus den unterschiedlichen Längen der vorangehenden Bereiche.
- Die Dateien haben weiterhin sieben Ressourceneinträge und sechs unterschiedliche Ressourcenstarts.

Die bloße Lage eines Deskriptors in einem Ressourcenbereich beweist noch nicht, dass die zugehörigen Bitmapdaten in derselben Ressource liegen. Dazu muss der Verweis bei +0x0C anhand der tatsächlichen Bytebereiche und einer unabhängigen Formatdekodierung verfolgt werden.

## 6. Ergebnis

**Bestätigt:**
1. Drei wiederkehrende Deskriptortypen 04, 05 und 06 sind in beiden Original- und beiden Test-Providern vorhanden.
2. Die Felder +0x36/+0x38 liefern exakt die drei Größen 48×14, 48×30 und 48×30.
3. Das Feld +0x3A unterscheidet Typ 06 (1101h) von Typ 04/05 (0001h).
4. ICONMAKE erzeugt diese Deskriptoren auch für die benutzerdefinierten Tokens GTI1 und GTI2.

**Offen:**
1. Die Bedeutung und Bezugsbasis des Feldes +0x0C.
2. Die genaue Interpretation von +0x3C und +0x3E.
3. Der vollständige Datenpfad vom Deskriptor zu den Bitmapbytes.
4. Die tatsächliche Laufzeitdarstellung im GeoManager von GeoWorks 1.2.

## 7. Nächster Untersuchungsschritt

Als nächstes wird das Feld +0x0C gezielt verfolgt. Dazu werden die Werte gegen Ressourcengrenzen, Datenblöcke und Bytefolgen der jeweiligen Icon-Payloads geprüft. Bis dieser Zusammenhang eindeutig ist, werden keine Pointer- oder Handle-Bedeutungen angenommen.

## Quellen

- Nutzerdateien: `GTI1FFFE.000`, `GTI2FFFD.000`.
- Originaldateien aus `GEOWORKS.zip`: `GEOWORKS/ICONS/GDOC.000`, `GEOWORKS/ICONS/PAPR.000`.
- Nutzerbereitgestellte ICONMAKE-Extraktionen: CGA-, HGC- und EGA-PCX-Dateien für GDOC und PAPR.
- ICONMAKE 1.0 Dokumentation: `ICONMAKE.ENG`, `ICONMAKE.DOC`.
- Zahlen und Offsets wurden durch Little-Endian-Auswertung der Binärdateien berechnet.
