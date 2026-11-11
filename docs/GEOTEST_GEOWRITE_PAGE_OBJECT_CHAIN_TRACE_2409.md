# GeoWrite 1.x – Ablauf der Seitenobjektkette im historischen Konverter (Untersuchung 2409)

## Fragestellung

Wie verarbeitet der historische GeoWrite-1.x-Konverter den visuellen Seiteninhalt? Welche Aussagen lassen sich über `CP_firstChild`, `VI_link.LP_next`, Relokationskennungen und das Ende der Kette sicher treffen?

## Primärquelle

`Source/showcase-format/public-source/convertGeoWrite.asm` aus `GeoWrite-GeoDraw-Enhanced-Colour-EN-DE.zip`, Abschnitt `pageLoop` bis `nextPage`, Quelltextzeilen 148–219.

Der Quelltext kommentiert in Zeile 160 ausdrücklich: `luckily Vis and VisComp are the same in 1.X and 2.0`. Das ist ein Hinweis des Konverterautors, dass er für die hier verwendeten Felder dieselbe Vis-/VisComp-Grundstruktur voraussetzt. Die Anwendung bleibt die Konvertierung eines GeoWrite-1.x-Dokuments.

## Ablauf im Detail

1. **Seitenblock laden:** Aus dem 30-Byte-Seiteneintrag wird `GW12_PAE_vmBlock` gelesen; `ourVMLockDS` sperrt den Seitenblock (Zeilen 154–157).
2. **PageContent holen:** `GW12_PageContent = 22h` wird als Chunk des Seiteninhalts geladen (Zeile 158).
3. **Erstes Kindobjekt bestimmen:** Der Code addiert `Vis_offset` und liest `VCI_comp.CP_firstChild.offset` (Zeilen 160–163). Der resultierende Chunk-/Objektzeiger wird im Kommentar als Header bezeichnet.
4. **Header verarbeiten:** Beim ersten Seitenaufruf wird dieses Objekt über `ConvertOldTextObject` in den Header-Ausgabepfad übergeben (Zeilen 165–175).
5. **Footer bestimmen:** Über `VI_link.LP_next.offset` wird das nächste Objekt ermittelt; der Kommentar bezeichnet es als Footer (Zeilen 178–180). Auch dieses Objekt wird beim ersten Seitenaufruf verarbeitet (Zeilen 181–189).
6. **Haupttext-/Spaltenkette durchlaufen:** Der Code liest das vollständige DWORD-Feld `VI_link.LP_next` (Zeilen 196–199), entsperrt den alten Block (Zeile 200) und prüft `LP_IS_PARENT` im Offset-Wort (Zeilen 201–202).
7. **Relokation auflösen:** Wenn das Link-Wort kein Parent-Link ist, ruft der Konverter `RelocToVMBlock` auf und sperrt anschließend den referenzierten VM-Block (Zeilen 203–204).
8. **Textobjekt konvertieren:** Das Objekt wird über `ConvertOldTextObject` verarbeitet; danach springt der Code zurück in die Kettenschleife (Zeilen 206–213).
9. **Seite abschließen:** Ein Parent-Link führt zu `nextPage`; dort wird der Seiteneintrag um `size GW12_PageArrayElement` (30 Bytes) weitergeschaltet (Zeilen 215–219).

## Verbindung zu den Bytebefunden

Untersuchungen 2406–2408 haben in den Seiten-Chunks folgende Fakten ermittelt:
- Drei WORD-Felder je Seite sind ObjRelocationIDs mit Quelle `ORS_NON_STATE_VM`.
- Alle drei lösen in `SOLAR_DE.000` auf den jeweiligen eigenen Seiten-VM-Block auf.
- In Chunk `0022h` stehen zwei dieser Werte bei Payload-Offsets `0x4C` und `0x56`.
- In Chunk `0030h` steht einer bei Payload-Offset `0x17`.
- Die beiden Relokationsfelder in Chunk `0022h` und das Feld in Chunk `0030h` stehen jeweils nach einem WORD `0022h`.

Der Konverterablauf belegt, dass Relokationen beim Verfolgen der Objektkette vorkommen. Er belegt jedoch nicht, dass jedes der drei in der Beispieldatei gefundenen Relokationsfelder genau einer der im Konverter gelesenen Link-Komponenten entspricht. Dazu fehlen noch die konkreten Strukturdefinitionen und ein Feld-für-Feld-Abgleich.

## Verfügbarkeitsgrenze der Definitionen

Im untersuchten ZIP-Archiv sind `convertGeoWrite.asm`, `convertText.asm` und `object.def` vorhanden. Eine Definition der Strukturen `VCI_comp`, `VI_link`, `CP_firstChild` und `LP_next` ist in den Archivdateien jedoch nicht enthalten. Die Suche über alle im ZIP enthaltenen `.def`, `.h`, `.asm` und `.goc` Dateien ergab keine weitere Deklaration dieser Feldnamen.

Daher werden in dieser Untersuchung keine Offsets oder Feldgrößen für diese Strukturen ergänzt, die nicht direkt aus den Quellen belegt sind.

## Konsequenz für GEOTEST

Ein nativer GeoWrite-Dokumentgenerator muss die Seitenobjektkette als Objektstruktur verstehen und ihre Relokationen korrekt auflösen. Aus dem Konverterablauf ergibt sich ein klarer Prüfpfad für eine spätere Minimaldatei: PageContent, erstes Kindobjekt, Header-/Footer-Verknüpfung, Haupttext-/Spaltenkette und Parent-Link-Ende.

Die genauen Strukturfelder und die Zuordnung der in `SOLAR_DE.000` gefundenen Selbstreferenzen zu diesen Feldern bleiben offen. Vor einem Generatorbau müssen passende 1.x-Strukturdefinitionen beschafft oder die Feldbelegung anhand weiterer unabhängiger nativer GeoWrite-Dokumente bestätigt werden.

## Status

Statische Quelltextanalyse; keine Laufzeittests, keine Binäränderungen und keine Änderung der Originaldokumente.
