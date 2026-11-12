# Untersuchung 2445 – ICONMAKE-Dummy-Provider GTI1/GTI2: Binärvergleich

## Ziel und Material

Untersucht wurden die beiden vom Nutzer in DOSBox/BaseBox mit ICONMAKE 1.0 erzeugten Dateien:

- `GTI1FFFE.000` – erzeugt aus den drei GDOC-PCX-Dateien, Token `GTI1`, Nummer 65534 (`FFFEh`)
- `GTI2FFFD.000` – erzeugt aus den drei PAPR-PCX-Dateien, Token `GTI2`, Nummer 65533 (`FFFDh`)

Als Referenzen dienten die unveränderten Originaldateien `GDOC.000` und `PAPR.000` aus `GEOWORKS.zip`, Verzeichnis `GEOWORKS/ICONS/`.

## Prüfsummen und Größen

| Datei | Größe | SHA-256 |
|---|---:|---|
| GTI1FFFE.000 | 2256 | `aa6e1f26aa88fcbc318f7527c5f8ebd690ad02e3cdb9a40441694e33fe5c8257` |
| GTI2FFFD.000 | 2208 | `865b8247eb60e1316aebab29656738d034b18a96c9061becc1bd447db491cae9` |
| GDOC.000 | 2256 | `fe19cbcb46c2a92cf02da64c963facb8decb95d7e60bca34eb0d1c5e00b01733` |
| PAPR.000 | 2208 | `30b08761294ccd7762c686ca3d477e509cb454f56b6c7db5aa2b1497efbabfbe` |

## 1. Token- und Dateikennung

Die äußere Datei-Kennung im Header bei Offset `0x14` enthält bei den erzeugten Dateien jeweils den erwarteten Vier-Zeichen-Token und die Nummer:

- GTI1: Bytes `47 54 49 31 FE FF` = `GTI1`, 65534
- GTI2: Bytes `47 54 49 32 FD FF` = `GTI2`, 65533

Der interne Geode-Header beginnt bei Dateioffset `0x100`. Dort wiederholen sich Token und Nummer. Der Hersteller-/Creator-Eintrag ist `GEOS`. Der im Header gespeicherte lange Name beginnt mit `GTI1` bzw. `GTI2`; die genaue Namensdarstellung sollte nicht ohne weitere Formatkenntnis interpretiert werden.

## 2. Ressourcenaufbau

Beide erzeugten Dateien besitzen dieselbe Gesamtgröße wie ihre jeweilige Referenz und dieselbe Zahl von sieben Ressourceneinträgen. Die Offsettabelle steht ab Dateioffset `0x13C`; die Werte sind relativ zum Geode-Basisoffset `0x100`.

| Ressource | GTI1 / GDOC absoluter Start | Länge | GTI2 / PAPR absoluter Start | Länge |
|---|---:|---:|---:|---:|
| 1 | `0x274` | 104 | `0x274` | 104 |
| 2 | `0x2DC` | 212 | `0x2DC` | 212 |
| 3 | `0x3B0` | 324 | `0x3B0` | 324 |
| 4 | `0x4F4` | 164 | `0x4F4` | 164 |
| 5 | `0x598` | 260 | `0x598` | 276 |
| 6 | `0x69C` | 564 | `0x6AC` | 500 |

Der Offsettabelleneintrag 1 und 2 ist jeweils doppelt (`0x174` relativ). Deshalb gibt es sieben Tabelleneinträge, aber sechs unterschiedliche Ressourcestartpositionen.

Die ersten 104 Bytes der ersten Ressource sind bei allen vier Dateien byte-identisch. Die übrigen Ressourcen sind nicht generell identisch; sie enthalten je nach Vorlage unterschiedliche Inhalte.

Besonderer Befund: Die letzte Ressource von `GTI2FFFD.000` ist byte-identisch mit der letzten Ressource von `PAPR.000` (500 Bytes). Bei GTI1 unterscheidet sich die entsprechende 564-Byte-Ressource von GDOC.

## 3. Binärvergleich mit den Original-Providern

- GTI1 hat 107 abweichende Bytes gegenüber GDOC.
- GTI2 hat 106 abweichende Bytes gegenüber PAPR.
- Die Abweichungen betreffen Token-/Namensfelder im äußeren und inneren Header sowie mehrere Ressourcenbereiche.
- Die Dateien sind also keine bloße Umbenennung der Originaldateien; ICONMAKE hat Ressourceninhalte aus den gelieferten PCX-Dateien bzw. seinem Provider-Grundgerüst erzeugt oder angepasst.

Die Byte-Differenzzahlen wurden durch direkten Vergleich der vollständigen Dateien gleicher Länge ermittelt.

## 4. Was ist damit nachgewiesen?

**Nachgewiesen:**

1. ICONMAKE 1.0 hat die beiden PCX-Sätze erfolgreich in zwei vollständige `.000`-Dateien umgesetzt.
2. Die erzeugten Dateien tragen die angegebenen Token und Nummern sowohl im äußeren Header als auch im internen Geode-Header.
3. Der Ressourcenaufbau entspricht dem Provider-Grundformat mit sieben Ressourceneinträgen und sechs unterschiedlichen Ressourcenstarts.
4. Die drei Iconvarianten lassen sich mit den zuvor extrahierten PCX-Dateien als Eingabe in Dummy-Provider umsetzen.

**Noch nicht nachgewiesen:**

1. Ob GeoWorks 1.2 diese Test-Token beim Öffnen eines Verzeichnisses tatsächlich in die produktive `TOKEN.DB` übernimmt.
2. Ob GeoManager die Test-Icons danach korrekt darstellt.
3. Welche konkrete Ressource intern welcher Bildschirmvariante zugeordnet ist. Die Bytebereiche sind vermessen, ihre vollständige Semantik ist damit noch nicht entschlüsselt.
4. Ob und wie ein solcher Provider als Dokumenttyp für ein von GEOTEST selbst erzeugtes Dokument verwendet werden kann. Der ICONMAKE-Test allein beweist noch keine vollständige Dokumentregistrierung oder Zuordnung zu einem GEOTEST-Dokument.

## 5. Nächster sicherer Schritt

Die beiden Dateien bleiben Testdateien. Keine produktive `TOKEN.DB` löschen oder verändern. Als nächstes sollten die Ressourcen von GTI1 und GTI2 mit einem unabhängigen Ressourcen-Parser bzw. mit dem vorhandenen GeoViewPlus untersucht werden. Erst danach folgt – in einer kopierten, isolierten GeoWorks-Testinstallation – ein kontrollierter Test, ob GeoManager die Test-Token erkennt und die Icons anzeigt.

## Quellen / Reproduzierbarkeit

- Eingabedateien: vom Nutzer bereitgestellte `GTI1FFFE.000` und `GTI2FFFD.000`.
- Referenzdateien: `GDOC.000` und `PAPR.000` aus dem vom Nutzer bereitgestellten `GEOWORKS.zip`.
- Befehlsbeschreibung: `ICONMAKE.ENG` und `ICONMAKE.DOC`, Abschnitt „Tokens from PCX files“.
- Prüfsummen und Offsets wurden direkt aus den vollständigen Binärdateien berechnet; es wurde kein GeoWorks-Runtime-Test aus dieser Analyse heraus behauptet.
