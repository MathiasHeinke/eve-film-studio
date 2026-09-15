# Codex: Selbstbewertung des EVE Film Studio

Bewerteter Stand: `519a7f0abc954553c3f06ba90e6503e0d01b51ba`, 2026-09-15.
Ich habe am System mitgearbeitet. Dies ist eine ausdrücklich verlangte
Selbstbewertung, kein unabhängiges Gütesiegel. Sie wurde gespeichert, bevor
ich Fables neue Bewertung gelesen habe. Die gemeinsamen technischen Versuche
sind in [evidence.json](evidence.json) dokumentiert.

## Gesamturteil

**6/10 als betreut nutzbares Film-Werkzeug.** Die Anleitung ist inzwischen
wesentlich klarer als die bisher nachgewiesene Ausführungsqualität. Sie ordnet
die richtigen Fragen vor der Generierung ein und behandelt Irrtümer genauer.
Ein reproduzierbarer Ablauf, der eigenständig hochwertige Werbefilme liefert,
ist noch nicht bewiesen. Der wichtigste nächste Schritt ist ein neuer
vollständiger Durchlauf mit beobachtbarer Verbesserung, nicht mehr Methodentext.

Die Zahlen sind begründete Einschätzungen, keine Benchmarkmessung. Der
Gesamteindruck ist kein Mittelwert der Tabelle. Bei der Methodengüte bewerte
ich Klarheit, Vollständigkeit und Verhältnismäßigkeit; bei der Ausführungsreife
zählen tatsächlich gelaufene Versuche. Der frühere Pilot entstand vor den
letzten Korrekturen und kann deren Wirkung daher nicht belegen oder widerlegen.

| Ebene | Methodengüte /10 | Nachgewiesene Ausführungsreife | Begründung |
|---|---:|---|---|
| Zielgruppe, Ideation, Story | 7 | Aktueller Stand nicht belegt | Menschliche Beobachtung, konkurrierende Ideen und Storyannahmen sind sinnvoll geordnet. Keine erneute Produktion und keine unvoreingenommene Zielgruppenprüfung nach dem Upgrade. |
| Regie, Kontinuität, Rhythmus | 7 | Aktueller Stand nicht belegt | Tatsächliche Nachbarzustände, bedingte sequenzielle Generierung und motivierte Schnitte sind beschrieben. Ob Figurenführung, Timing und Übergänge dadurch besser werden, muss ein neuer Film zeigen. |
| Grafik und Produktbeleg | 7 | 5/10, begrenzter Pilotnachweis | Eingabe, Antwort, Ergebnis und Werbetext sind klar unterschieden. Die alte Ergebnisgrafik wurde erkannt; sie zeigt eine illustrative Behauptung und keine nachgewiesene Produktausführung. |
| Audio und Synchronität | 6 | 3/10 | Die Regeln sind brauchbar, der geprüfte Helfer zeigt jedoch konkrete Pegel- und Quellenprobleme. Der Pilot enthält einen vom Zuschauer bestätigten Versatz über einen Schnitt. |
| Unabhängige Prüfung | 7 | 5/10 | Neutraler Erstcheck, Wahrnehmungsgrenzen und Korrekturverfahren sind vorhanden. Im tatsächlichen Ablauf wurde ein zutreffender Fehlerhinweis zunächst zu eng entkräftet; erst der Nutzer korrigierte das. |
| Technische Reproduzierbarkeit | 5 | 4/10 | Es gibt lauffähige Helfer und Dateiprüfungen, aber falsche Dauerzusagen und uneinheitliches Audioverhalten. Kein frischer Editor-/MCP-End-to-End-Nachweis auf fremdem Setup. |
| Kostenkontrolle und Wirtschaftlichkeit | 7 | 5/10 für Kostenbelege; Marge nicht belegt | Drei AV-Aufrufe sind exakt abgerechnet. Kein Vollkostenvergleich, keine Endkundenpreisregel und kein Nachweis profitabler Wiederholungen. |
| Command-EVE-Integration | 4 | Nicht implementiert/nicht belegt | Ein konkreter Handoff und Rollenrahmen sind vorhanden. Das portable Skillpaket ist noch kein nutzbares, abgerechnetes Produkttool. Diese Grenze ist kein Fehler des Skill-Formats. |

## Was bereits gut ist

Der Ablauf beginnt bei Bedeutung und Alltagserfahrung. Eine attraktiv generierte
Szene darf eine schwache Prämisse nicht ersetzen. Die Trennung von Geschichte,
Storyboard, tatsächlichen Bildern und tatsächlich geschnittenen Takes hilft,
Fehler früher und an der richtigen Stelle zu finden.
Siehe [Filmhandwerk](../../skills/produce-brand-film/references/film-craft.md)
und [Storyboard](../../skills/produce-brand-film/references/storyboard-contract.md).

Die Grafikmethode gibt Gestaltungsspielraum und erklärt die Informationsrolle.
Sie schreibt weder Chatblasen für alles vor noch verbietet sie frei schwebende
Elemente. Ebenso sinnvoll: Ein Film muss nicht auf jeden Beat schneiden und
eine Erzählung darf Ereignisse außerhalb des Bildes enthalten.
Siehe [Grafikmethodik](../../skills/produce-brand-film/references/cinematic-graphics.md).

Gemini schließt eine konkrete Wahrnehmungslücke zu geringen gemessenen
Modellkosten. Sein Bericht wird als prüfbare Evidenz behandelt. Das ist nützlicher
als ein Supervisor, der aus einem Transkript vermeintliche Klang- oder
Bewegungsurteile ableitet. Die tatsächlichen 0,182638 USD für drei Aufrufe sagen
jedoch nichts über vollständige Produktionskosten oder den späteren Verkaufspreis.

## Was die lokalen Versuche zeigen

Fünf synthetische Assemblerläufe nutzten ein zweisekündiges Testbildvideo und
einen 440-Hz-Testton bei 320×180 und 24 fps. Sie benötigen keine KI und testen
keine filmische Qualität.

1. **Zu kurze Quelle wird als Erfolg gemeldet.** Aus einer Quelle mit zwei
   Sekunden und deklarierter Szenendauer von vier Sekunden entsteht ein
   viersekündiger Container mit zwei Sekunden Video und vier Sekunden Audio.
   Exitcode ist 0 und der Assembler meldet vier Sekunden. Eine frühe Prüfung
   der verfügbaren Quellspanne fehlt. Der technische Validator enthält zwar
   einen Dauervergleich; das macht die Ausgabezusage des Assemblers nicht richtig.
2. **`voice_volume: 0` wird ohne Musik ignoriert.** RMS bei Lautstärke 1 und 0:
   jeweils 0,09274885. Ein auf null gesetzter Sprachpegel ist nicht stumm.
3. **Ein stiller Musikinput verändert den Sprachpegel.** RMS fällt von
   0,09274885 auf 0,04632490, Verhältnis 0,499466. Damit hängt die Lautheit
   trotz gleicher Sprachlautstärke davon ab, ob der Musikzweig benutzt wird.
4. **Quellton wird entfernt.** Ohne separat angegebene Sprach-/Musikdatei
   erhält das finale Video einen stummen Audiostream. Für einen bewusst
   getrennten Bildschnitt ist das legitim; für generierte Dialogtakes fehlt
   ein einfach nachprüfbarer Übergang vom Quellton zur richtigen Timelineposition.
   Ich werte das als Workflowlücke, nicht pauschal als Fehler jeder Tonentfernung.
5. **Ein technisch gültiger Film kann asynchron sein.** Der bisherige Pilot
   besteht alle 15 technischen Checks, obwohl der Zuschauer einen Versatz
   zwischen Sprache und anschließender sichtbarer Sprechbewegung feststellt.
   Der Validator erfüllt hier seinen Formatscope. Unzulässig wäre, sein PASS
   als kreative oder audiovisuelle Abnahme zu verwenden.

Verantwortliche Stellen: [Assembler](../../skills/produce-brand-film/scripts/assemble_film.py)
(`normalize_scene`, `add_audio`) und
[Validator](../../skills/produce-brand-film/scripts/validate_film.py)
(`main`). Das bestehende Soundmodell ist in
[timeline-manifest.md](../../skills/produce-brand-film/references/timeline-manifest.md)
beschrieben. Die Befunde wurden in dieser Bewertung nicht repariert.

## Wo ich selbst falsch gearbeitet habe

Ich habe zunächst den isolierten Off-Anfang einer Zeile betrachtet. Dass dort
kein sprechender Mund sichtbar ist, widerlegt aber nicht den Fehler im nächsten
Bild: sichtbares Sprechen nach Ende des Tons. Diese zu enge Entkräftung hätte
einen echten Fehler aus der Reparaturliste entfernt. Die Korrektur durch den
Nutzer gehört deshalb zur Evidenz und nicht nur zu einer Stilpräferenz.

Außerdem habe ich eine Supervisorwahl für die Entwicklungsarbeit fälschlich
als Produktmodellentscheidung weitergetragen. Das wurde berichtigt. Der
Integrationsrahmen bleibt: `eve-flash` für die Bearbeitung, `eve-max` als
MoA-Supervisor und Gemini für Video. Fable 5.1 ist hier Entwicklungsprüfer.
Eine Rollenbezeichnung ersetzt keine Prüfung des tatsächlich zuständigen Systems.

## Meine nächsten fünf Iterationen

1. **Audiopfad und Quellspannen reparieren — klein bis mittel.** Vor dem Rendern
   ungültige Spannen erkennen; Sprachlautstärke in allen Zweigen gleich anwenden;
   Mischung explizit definieren. Erfolg: dieselben synthetischen Fälle liefern
   die beabsichtigten Pegel und passende Streamlängen oder einen klaren frühen Fehler.
2. **Prüfung an einer kurzen zusammenhängenden Szene bewähren — mittel.** Ein
   gültiger Off-Übergang und ein bekannter vorgezogener Dialog dürfen nicht
   gleich bewertet werden. Erfolg: Der vorhandene Ablauf hält Fehler und
   absichtliche Tonbrücken auseinander; unzureichende Wahrnehmung bleibt offen.
   Keine neue Freigabedatenbank dafür bauen.
3. **Eine neue Geschichte vollständig durchlaufen — mittel.** Vor der Generierung
   die tragende Alltagssituation und den glaubwürdigen Produktbeitrag festhalten.
   Danach Menschen ohne Autoren-Erklärung sehen lassen. Vorschlag für die kleine
   qualitative Runde: mindestens vier von fünf erkennen die übernommene Arbeit
   und ihre menschliche Folge; Unklarheiten wörtlich festhalten. Das ist ein
   Verständnischeck, kein statistischer Wirksamkeitsnachweis.
4. **Übertragbarkeit auf drei verschiedene Briefs belegen — mittel.** Je ein
   anderer menschlicher Konflikt und andere Informationsaufgabe. Gleiche Methode,
   keine immer längeren Sonderregeln. Erfolg: weniger gezählte Rettungseingriffe
   und Nachgenerierungen bei erhaltener Verständlichkeit; Reparaturen und echte
   Gesamtkosten pro akzeptiertem Ergebnis dokumentieren.
5. **Ein vertikaler Produktdurchlauf mit Abrechnung — mittel bis groß.** Native
   Anfrage → Gemini-Prüfung → `eve-max`-Bewertung → verständliche Antwort und
   korrekte Belastung im bestehenden Creditsystem. Vor Verkauf Preis, enthaltene
   Prüfungen, Wiederholungen und Marge entscheiden; Bildgenerierung zum Vergleich
   des vorhandenen Spezialwerkzeugpfads heranziehen. Keine neue Supervisorplattform.

Wenn dieselbe grundlegende Fehlannahme nach zwei Reparaturen bestehen bleibt,
zuerst Geschichte, Zuständigkeit oder Toolpfad ändern. Nicht automatisch weitere
Promptregeln und Prüfer anhängen. Qualität muss sich am nächsten Ergebnis zeigen.

## Prüfumfang und Grenzen

Direkt gelesen: Skill-Einstieg, Kernreferenzen zu Story, Regie, Grafik,
Kontinuität, Gemini und Integration sowie die betreffenden Assembler- und
Validatorfunktionen. Ausgeführt: fünf synthetische Assemblerläufe, Audio-RMS-
und Streammessungen, technischer Validatorlauf am existierenden Pilot. Der
Gegenprüfer erhält dieselben technischen Resultate. Keine neue Mediengenerierung,
keine eigene aktuelle Hör-/Bewegtbildabnahme, kein MCP-/Editor-/Produkt-End-to-End-Test,
keine Zielgruppenforschung. Für ein belastbares Urteil über die nächste
Filmqualität fehlt der nächste tatsächliche Film.
