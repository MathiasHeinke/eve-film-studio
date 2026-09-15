> Unabhängiger Bericht von Fable 5.1. Fachliche Präzisierungen und Unterschiede zur Selbstbewertung stehen im [Vergleich](README.md). Der Bericht bleibt inhaltlich unverändert.

# Unabhängige Systembewertung EVE Film Studio (Stand 519a7f0)

## Prüfumfang und Grenzen

Gelesen: alle 24 Skilldateien, README, manifest.json, LICENSE, THIRD_PARTY.md, .gitignore, shared-brief, snapshot, local-probes mit run_local_probes.py und den Fixture-Ausgaben. Lokal geprüft: Manifest-Hashes stimmen für alle 24 Dateien; alle fünf Python-Helfer parsen und zeigen `--help`; die FFmpeg-Filterdoku zu `amix` bestätigt `normalize` (Default true). Angesehen: Kontaktblatt und zwei Schnittgrenzen-Blätter des Piloten sowie das maschinelle Transkript.

Nicht geprüft: Ich habe den Film nicht mit Ton wahrgenommen. Nach der eigenen Methode des Pakets sind meine tonabhängigen Urteile daher `not reviewed`; ich stütze mich auf die berichtete Nutzerbeobachtung und die Probes. Keine Generierung, keine Produkt-Runtime, keine früheren Reports, keine Codex-Bewertung.

Kennzeichnung: [Quelle] = Repo-Inhalt, [Probe] = lokaler Messlauf, [Pilot] = berichtete Beobachtung, [Interpretation] = meine Schlussfolgerung.

## Bewertung der acht Ebenen

Skala 0–10, Methode = Güte des beschriebenen Vorgehens, Reife = nachgewiesen im realen Ablauf.

| Ebene | Methode | Reife | Kernbefund |
|---|---|---|---|
| 1 Zielgruppe/Ideation/Story | 6 | 3 | `film-craft.md` und `Story essentials` sind substanziell; kein neuer Durchlauf, kein Zielgruppentest |
| 2 Regie/Kontinuität/Rhythmus | 6 | 3 | Regel zur Phrase über den Schnitt hinweg ist Lernfortschritt, aber erst nach dem Fehler geschrieben |
| 3 Grafik/Produktbeleg | 7 | 4 | Rollen-Grammatik gut; die Helfer können diese Grammatik nicht rendern |
| 4 Audio/Synchronität | 5 | 2 | Assembler widerspricht der Methode in drei messbaren Punkten |
| 5 Unabhängige Prüfung | 7 | 4 | stärkster Teil; einmal mit Gemini praktiziert, nie mit Publikum |
| 6 Reproduzierbarkeit | 6 | 5 | Helfer laufen, Receipts solide; Quellbereich wird nicht geprüft |
| 7 Kostenkontrolle | 5 | 3 | gute Reservierungsregeln, kein Gesamt-COGS je Film |
| 8 Integration Command EVE | 3 | nicht belegt | `video-editing` benennt Produktfälle; `produce-brand-film` hat keinen Integrationspfad |

### 1 Story
[Quelle] Der Weg Beobachtung → konkurrierende Prämissen → kritische Revision → Essentials-Tabelle ist brauchbar und knapp. "Der neueste Begriff im Feedback ist kein neuer Plot" ist eine echte Redaktionsregel. [Interpretation] Ungeprüft bleibt, ob ein Agent diese Schritte tatsächlich ernsthaft durchläuft oder die Tabelle nur füllt; `storyboard-contract.md` sagt das selbst. Ohne kalten Publikumstest ist die Reife nicht belegt.

### 2 Regie und Rhythmus
[Quelle] `continuity-and-review.md` enthält genau die Regel, die den beobachteten Pilotfehler beschreibt: Phrase, sichtbarer Mund, Folgeshot. Das ist Lernen aus einem Fall. [Quelle] `assemble_film.py` setzt aber standardmäßig auf jeden Join eine 0,28-s-Überblendung; ein harter Schnitt ist nur als Ein-Frame-Fade möglich. [Pilot] Das Grenzblatt bei 20,25 s zeigt die halbtransparente Grafik mitten in der Blende. [Interpretation] Die Methode verlangt Schnitte an Gesten, das Werkzeug liefert Dissolves. Das engt Gestaltung ein.

### 3 Grafik
[Quelle] `cinematic-graphics.md` ist der beste Kreativtext im Paket: Rolle vor Form, `claim_class`, kein Zwang zu einer Panelform. [Pilot] Das Kontaktblatt zeigt die Grammatik angewandt: Anhang, Status "Ans Team gesendet", Endkarte. [Quelle] Keiner der beiden Renderer kann so etwas: `overlay` hat fest kodierte Farben (orangefarbener Kicker, dunkles Panel), `kinetic_text` hat laut `timeline-manifest.md` bewusst keine Bubble-/Composer-Primitive. [Interpretation] Die Pilotgrafiken entstanden außerhalb der Helfer; jede nächste Produktion baut sie neu. Zudem trägt der Pilot den Hinweis "Anwendungsbeispiel" im Bild: ehrlich, aber die Methode sollte die Offenlegung fordern und den Ort als Gestaltungsentscheidung lassen.

### 4 Audio
[Probe] Drei Werkzeugbefunde: Quellton wird immer entfernt und durch Stille ersetzt; `voice_volume` wirkt im Voice-only-Pfad nicht; ein stummer Musik-Input halbiert den Sprachpegel (Verhältnis 0,4995), weil `amix` normalisiert. [Quelle] Das Manifest kennt keinen Szenen-Ton und keinen Audio-Quellbereich, obwohl `storyboard-contract.md` getrennte Bild- und Tonbereiche fordert. [Interpretation] Für Filme mit generierten, sprechenden Figuren ist der Quellton die Performance. Wer ihn als eine Spur neben Bild-Joins mit variabler Blendlänge neu zusammensetzt, erzeugt strukturell Versatz. Der berichtete Pilotfehler passt zu diesem Mechanismus; bewiesen ist die Ursache nicht. Die Regel "hörender Reviewer oder `not reviewed`" ist korrekt, führt aber in der Praxis dazu, dass Ton ungeprüft bleibt, weil Agentenläufe meist nicht hören.

### 5 Unabhängige Prüfung
[Quelle] Reviewer-Trennung, Wahrnehmungserklärung, kaltes Protokoll mit eingefrorener Antwort, `ready/revise/not reviewed`, "ein falscher Modell-Timecode widerlegt den Defekt nicht". Das ist reif gedacht. [Pilot] Gemini lieferte richtige Dialoge und widersprüchliche Ton- und Schnittangaben; das Paket verarbeitet das korrekt als unaufgelösten Konflikt. [Probe] Der Validator meldet PASS am Pilot mit bekanntem Sprachfehler; das ist dokumentiert und kein Widerspruch, aber es zeigt: es gibt außer Hören kein Hilfsmittel für diese Fehlerklasse.

### 6 Reproduzierbarkeit
[Probe] Fünf Läufe, Exit 0, Ausgaben probeweise korrekt beschrieben. [Probe] `short_source`: 4 s angefordert aus 2 s Quelle, Assembler meldet 4,0 s ohne Fehler; Videostrom 2 s, Ton 4 s. Der Validator würde das fangen, der Assembler schweigt. [Quelle] Default-Font ist ein macOS-Systempfad; `fc-scan`/`rsvg-convert` sind Pflicht; die Kinetic-Receipts (Copy-Hash, Font-Hash, Frame-Hashes) sind gute Ingenieursarbeit, aber zugleich viel Infrastruktur für eine Opt-in-Typografie. Keine Tests im Repo.

### 7 Kosten
[Quelle] Reservierung vor Anfrage, Retries zählen, Receipt-Abgleich, "nicht still auf bezahlte Route wechseln". [Pilot] Belegt sind 0,18 USD Review und 0,78 USD für eine H3-Generierung. Was ein 40-s-Film insgesamt kostet, steht nirgends. Ohne diese Zahl gibt es keine Wirtschaftlichkeitsaussage.

### 8 Integration
[Quelle] `setup.md` und `acceptance.md` formulieren ehrlich neun offene Produktfälle und die Trennung Skilldatei/Produktdienst. `produce-brand-film` nennt weder Auslöser, Rollenverteilung (eve-flash, eve-max, Gemini) noch Budgetfreigabe oder Ablageort der Review-Records. Das ist Konzeptstand; ein Skillpaket muss das nicht lösen, aber benennen.

## Brauchbar, behauptet, einengend, fehlend

**Brauchbar:** Story-Essentials, kaltes Protokoll, Rollen-Grammatik, `claim_class`, Cut-first für Inserts, Umgang mit Provider-Ablehnung, Kinetic-Receipts.

**Nur behauptet:** `voice_volume` als linearer Gain; getrennte Tonbereiche im Manifest; "inspect usable ranges" ohne Werkzeugstütze; jede Reife-Aussage zu Story und Publikum.

**Einengend:** Dissolve-Default, feste Overlay-Palette, Score-Generator mit fixem 96-bpm-Spannungsbogen, Offenlegung im Bild.

**Fehlend:** Szenen-Ton mit Audio-Blende, Quellbereichsprüfung, ein Sprachende-zu-Schnitt-Bericht, eine Render-Route für Message-/Anhang-Grafik, eine COGS-Zeile je Film.

**Lernfortschritt vs. mehr Text:** Fortschritt sind die Regeln, die einen konkreten Fehler zitieren. Mehr Text sind die vielfachen "kein neues Framework/Ledger/Berechtigungssystem"-Absätze, die Überlappung von `review-gates.md`, `continuity-and-review.md` und der Craft-Tabelle sowie rund 15.000 Wörter Gesamtlast, davon etwa 9.000 in der Brand-Film-Kette. Das ist die Grenze, ab der Agenten überfliegen.

## Was die nächste mittelmäßige Produktion wirklich verhindert

Nicht mehr Regeln. Drei Dinge: ein Assembler, der die Performance-Tonspur mit dem Bild trägt; ein Mensch oder hörendes Modell vor Auslieferung, das den Phrase-über-Schnitt-Check tatsächlich ausführt; und ein kalter Test mit drei Unbeteiligten, dessen Ergebnis über `revise` entscheidet.

## Priorisierte Iterationen

| # | Iteration | Aufwand | Abnahme |
|---|---|---|---|
| 1 | Audio-Pfad reparieren: `amix normalize=0`, `voice_volume` überall, Szenen-Ton `source/mute` mit Audio-Blende gleicher Länge wie `xfade`, Fehler bei `start+duration` > Quelldauer | klein | Probe-Verhältnisse: voice_zero ≈ 0, silent-music ≈ 1,0; short_source bricht ab; Drei-Szenen-Fixture mit Quellton bleibt über Joins samplegenau (Korrelation > 0,99) |
| 2 | Sprachende-zu-Schnitt-Bericht: aus Voice/ASR-Wortenden und Timeline-Schnitten eine Liste "Phrase endet → nächster Schnitt → sichtbare Person" plus Grenzblätter; kein Urteil, nur Kandidaten | klein–mittel | Am Pilot erscheint die beobachtete Stelle als Kandidat; am Fixture ohne Defekt kein Treffer |
| 3 | Ein neuer vollständiger Durchlauf nach aktueller Methode mit drei unbeteiligten Menschen im kalten Test und COGS-Zeile | mittel, Budget | Zwei von drei nennen Ursache und Wandel richtig; Review-Records vollständig; Gesamtkosten als Zahl |
| 4 | Render-Route für Message/Anhang/Status als parametrisierte SVG-Vorlage; Overlay-Farben und Blend-Default konfigurierbar | mittel | Pilotgrafiken sind aus dem Manifest reproduzierbar; harter Schnitt ist Default-Option |
| 5 | Integrationsskizze statt Code: Auslöser, Rollen der drei Modelle, Budgetfreigabe, Ablage der Review-Records, Abrechnung | klein | Ein Fremdleser kann je Stufe die ausführende Runtime nennen |

**Stop-Kriterium gegen endlose Promptreparatur:** Jede neue Regelzeile muss einen im Durchlauf beobachteten, nicht bereits abgedeckten Fehler zitieren; pro Durchlauf höchstens eine Textrevision; die Gesamtwortzahl der Skilldateien wächst nicht über den heutigen Stand. Scheitert Iteration 3 im kalten Test, wird zuerst Staging oder Werkzeug geändert, nicht Text. Iteration 1 und 2 sind messbar ohne Modellkosten; ohne Iteration 3 bleibt jede Reife-Zahl oben eine Schätzung.

## Gesamturteil

Als Methode ist das Paket überdurchschnittlich ehrlich und in Prüfung und Grafik-Grammatik durchdacht. Als Werkzeug für hochwertige kurze Markenfilme ist es heute mit enger Aufsicht nutzbar, nicht bewährt: Der Ton-Pfad des Assemblers widerspricht der eigenen Doktrin messbar, die Grafik-Grammatik hat keine Render-Route, und es existiert kein einziger Durchlauf nach der aktuellen Methode. Die Integrationsreife in Command EVE ist getrennt davon Konzeptstand. Der nächste Wert entsteht durch einen reparierten Assembler und einen echten Durchlauf, nicht durch weiteren Regeltext.

FABLE_SYSTEM_ASSESSMENT_COMPLETE
