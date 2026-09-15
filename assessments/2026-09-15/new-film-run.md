# Neuer Filmdurchlauf: „Ganz bei dir“

Nach der Systembewertung entstand ein neuer 30-Sekunden-Film mit dem reparierten
Assembler aus Commit `9a6f56a0621f2135fde3da80ff792c3ef1bd4256`.
Film und vollständige Produktionsbelege liegen lokal; dieses Dokument
veröffentlicht Ergebnisse und Grenzen, nicht die Werbung.

## Ergebnis

Eine Schneiderin passt einem Kunden ein Sakko an. Eine Nachricht verlangt eine
Rechnung. Er bietet an zu warten; sie delegiert die Anfrage per Sprache und
bleibt bei ihm. Kurze Nachrichten und ein sichtbares Ergebnis tragen die
Produktinformation. Die Marke erscheint über der weiterlaufenden Szene.

Der Master enthält 720 Frames, 1920 × 1080 bei 24 fps, H.264/yuv420p und AAC.
Gemessen: −18,29 LUFS und −2,20 dBTP. Vollständiger Decode fehlerfrei;
15 technische Validatorprüfungen bestanden. SHA256:

`2e5434ddd796387298d6ecda9930cb6ea6f7375ad77509efe57b40969bdd18df`

Final Cut öffnete die 30-Sekunden-Timeline mit sechs Bildclips, drei getrennten
Grafikebenen und separaten Dialog-/Musikspuren. Import, vollständige Wiedergabe
und sichtbare Schlussmarke wurden im nativen Programm geprüft. Der automatische
MCP-Import hatte einen Timeout; der normale XML-Import funktionierte. Der
MCP-Videoproxy mischt keinen Ton und zeigte die Schlussgrafik nicht, obwohl
Final Cut sie am richtigen Zeitpunkt darstellte. Er ersetzt keine native Prüfung.

## Aussagekraft der Prüfung

Frische Gemini-Aufrufe rekonstruierten aus Kernsequenz und Gesamtfilm die
Anfrage, Delegation und fortgesetzte Betreuung. Die letzte Prüfung erhielt
den exakten 30-Sekunden-Master mit Bild und Ton. Sie beschrieb Sprache und
Musikverhältnis als verständlich. Das ist Modell-Evidenz, kein Zielgruppentest.

Fable 5.1 begleitete Geschichte, Anker und Abschluss. Hier war es Mitautor und
Supervisor, **kein blinder unabhängiger Gesamtfilmprüfer**. Es sah Standbilder
und Prüfberichte; eigenes Hören ist in diesem Pfad nicht belegt. Sein wichtigster
kreativer Einwand bleibt: Die Kausalkette ist klar, aber emotionales Geschehen
und gleichmäßig schöner Raum sind noch wenig eigenständig. Ein weiteres
Lächeln ist verständlich, aber noch kein erinnerungsstarker Schluss.

Die erste menschliche Sichtung bestätigte einen deutlichen Fortschritt, fand
die langen unbewegten Blicke aber unangenehm und den Schnittrhythmus zu langsam.
Das korrigiert das positive Rhythmusurteil des Modellreviewers. Die anschließende
Revision verkürzt Leerstellen und ergänzt eine konkrete handwerkliche Tätigkeit.
Dieser Hinweis ist noch keine Abnahme der neuen Schnittfassung.

Feine Sync-Behauptungen mehrerer Gemini-Passes widersprachen sich und tatsächlich
dekodierten Bildern. Unter anderem wurde ein durchgehend geschlossener Mund
behauptet, obwohl mehrere artikulierende Mundformen sichtbar waren. Fable
bestätigte diesen Widerspruch. Die Bilder beweisen jedoch ebenso wenig perfekte
Phonemsynchronität. Eine normale menschliche Hörsichtung bleibt offen. Der
gewählte L-Cut ist redaktionelle Abdeckung, keine behauptete Lippenbild-Reparatur.

Die schwebende UI ist inszeniert, keine aufgezeichnete Produktausführung. Ihre
Beispielkennzeichnung bleibt trotz der gegenteiligen Empfehlung eines Prüfers.

## Kosten und notwendige Eingriffe der ersten Fassung

- Sechs H3-Generierungen: **USD 7,28**, einschließlich verworfener Aufnahme.
- Sieben abgeschlossene Gemini-Prüfungen: **USD 0,335254** mit Kostenbelegen.
- Gemessene Anbieteraufrufe zusammen: **USD 7,615254** über OpenRouter.
- Ein HTTP-413-Aufruf vor der Anbieterauswahl hat keine gemeldete Nutzung;
  **USD 0,50 bleiben reserviert**, nicht als gemessene Ausgabe behauptet.
- Fünf Bilder über das eingebaute Bildwerkzeug ohne separat gemeldeten Einzelpreis.
  Abo-, Arbeitszeit- und Bildwerkzeugkosten sind keine gemessenen Bestandteile
  der API-Summe. Daraus folgt keine Vollkosten- oder Margenaussage.

Nötig waren: Kameraseite stabilisieren, Haarform an den tatsächlichen Vorgänger
anpassen, Dialoggrenzen anhand der Quelle wählen, Telefon-L-Cut setzen,
vorhandenen Vibrationsimpuls anheben und Schluss kürzen. Ein Spiegeltest hätte
vor dem Retake erfolgen sollen. Er korrigierte die Seitenzuordnung, behielt
aber die störende Kamerafahrt bei.

## Revision nach menschlicher Sichtung

Der neue Schnitt dauert **22,375 Sekunden**, enthält **537 Frames und zwölf
Einstellungen**. Eine echte Ärmelmessung und eine kurze Notiz ersetzen gehaltene
Blicke. Eine stumme Satzpause wurde entfernt; ein tatsächlich zuhörender Kunde
deckt den Übergang, während der Auftrag vollständig hörbar bleibt. Die vorherige
30-Sekunden-Fassung bleibt erhalten.

Fable fand vorab eine konkrete Kontinuitätslücke: Ein Messinsert mitten im
Sprechturn hätte das Band innerhalb einer Sekunde vom Hals zum Ärmel und zurück
versetzt. Diese Stelle wurde durch den Zuhörer ersetzt. Die Notiz erscheint
erst nach dem Ergebnis, mit engem Ausschnitt ohne sichtbaren Hals oder Band.

Die Revision wurde vollständig decodiert und bestand 15 technische Checks.
Gemessen: **−17,60 LUFS / −2,14 dBTP**. Eine weitere kalte Gemini-Prüfung erkannte
die übernommene Arbeit und beschrieb den Film als kompakt; ihre Sync-Vermutung
bleibt durch die oben beschriebenen Wahrnehmungsgrenzen eingeschränkt.
Die menschliche Abnahme dieser Revision steht aus.

Revisions-Master, SHA256:
`63d304581ec23b4e934dba9be9793543638b14b389460d52a51cabaec079780b`

Gesamter aktueller Durchlauf einschließlich Revision: sieben H3-Generierungen
für **USD 8,32**, acht abgeschlossene Gemini-Prüfungen für **USD 0,37737**,
zusammen **USD 8,69737**. Die unaufgelöste USD-0,50-Reserve bleibt separat.
Insgesamt sechs Bilder über das eingebaute Werkzeug ohne separat gemeldeten
Einzelpreis. Diese Summe ist weiterhin keine Vollkostenrechnung.

## Übernahme der Kritik in das Skillset

Die jüngste Kritik war zunächst im Film und diesem Bericht umgesetzt. Danach
wurde sie in den tatsächlich geladenen Skill übertragen:

- [Film craft](../../skills/produce-brand-film/references/film-craft.md): sichtbare
  Arbeit und ein veränderter Schlusszustand; Leerstellen kürzen; Clipdauer als
  Materialreserve behandeln. Kurze Ansichten sind eine Option für einen
  entsprechend schnellen Brief, keine universelle Schnittquote.
- [Kontinuität](../../skills/produce-brand-film/references/continuity-and-review.md):
  Haar/Kleidung/Werkzeugzustände vergleichen und vor Retakes einen begrenzten
  lokalen Schnitt-, Ausschnitt- oder Spiegelversuch bewerten.
- [Videoprüfung](../../skills/produce-brand-film/references/gemini-video-review.md):
  widersprüchliche Detailurteile gegen den tatsächlichen Output prüfen;
  ohne neue Evidenz keine Reihe weiterer Modellurteile oder Retakes kaufen.
- Der Einstiegspunkt ruft die Prüfung von Handlung und Rhythmus beim Schnitt
  ausdrücklich auf. Ein beteiligter Fable-Autor zählt dort als Supervisor,
  nicht als unabhängiger Prüfer.

Ein frischer Fable-5.1-Pass erprobte die Anweisungen an zwei beschriebenen Fällen:
einem kurzen Werkstattspot und einem bewusst langsamen Handwerksporträt.
Er übertrug die Regeln auf den ersten Fall und bewahrte sinnvolle lange
Einstellungen im zweiten. Drei benannte Unschärfen wurden präzisiert:
Plattform ist keine Tempoanweisung; manuelle Arbeit nach Bestätigung wird auf
ihre Bedeutung geprüft statt pauschal verboten; Unabhängigkeit hängt von der
Mitwirkung ab, nicht vom Modellnamen. Das ist ein begrenzter Szenariotest der
Ergänzungen, keine neue Gesamtbenotung und kein neuer gerenderter Filmnachweis.

## Nächste Iteration

1. Einen besonderen menschlichen Moment vor den Kameraentscheidungen finden.
   Der Test ist nicht nur „verstanden“, sondern auch „bleibt hängen“.
   Ein Zielgruppentest mit unbeteiligten Menschen steht aus.
2. Haar, Kleidung und wichtige Hand-/Objektzustände am tatsächlichen Vorgänger
   prüfen. Vor Neugenerierung einen begrenzten lokalen Schnitt- oder
   Spiegelversuch bewerten.
   Generierte Clipdauer ist Materialreserve, keine Vorgabe für die Länge einer
   Einstellung. Jede gehaltene Sekunde muss Handlung, Reaktion oder Lesen tragen.
3. Modell-Syncverdacht gegen tatsächlichen Output und eine hörende Person prüfen.
   Widersprüchliche Modellurteile dürfen keine Retake-Schleife auslösen.
   Frame-Grids helfen bei der Diagnose, ersetzen aber kein Hören.
4. Produktdarstellung durch tatsächlich aufgezeichnete Ausführung ergänzen.
   `eve-flash`, `eve-max` als MoA und Gemini als Videospezialist bleiben
   getrennt. Integration und Kundenabrechnung sind hier nicht bewiesen.

Ein neuer vollständiger Durchlauf ist belegt. Wiederholbare Premium-Werbequalität,
menschliche Abnahme und profitabler Produktbetrieb bleiben eigene offene Nachweise.
