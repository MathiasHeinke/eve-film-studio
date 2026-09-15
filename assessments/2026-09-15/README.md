# Systembewertung — 15. September 2026

**EVE Film Studio ist als betreutes Arbeitswerkzeug brauchbar. Wiederholt
hochwertige Filme aus einem autonomen Gesamtablauf sind noch nicht belegt.**
Die größte Lücke liegt zwischen guter Anleitung und zuverlässiger Ausführung.

Bewertet wurde Commit [`519a7f0`](https://github.com/MathiasHeinke/eve-film-studio/tree/519a7f0abc954553c3f06ba90e6503e0d01b51ba).
Die hier veröffentlichten Berichte und der Reproduktionscode wurden danach
ergänzt. Die bewerteten Produktionshelfer wurden dabei nicht verändert.

Spätere Arbeit desselben Tages: [reparierter Ton- und Schnittpfad](audio-repair.md)
und [neuer vollständiger Filmdurchlauf](new-film-run.md). Die ursprünglichen
Noten und Befunde unten bleiben als Bewertung des damaligen Standes erhalten.

- [Codex-Selbstbewertung](codex.md): **6/10 als betreut nutzbares Werkzeug**.
- [Unabhängige Bewertung von Fable 5.1](fable.md): Methode überwiegend **5–7/10**,
  nachgewiesene Reife überwiegend **2–5/10**; Produktintegration nicht belegt.
- [Messwerte und Evidenzgrenzen](evidence.json).

Die Noten sind fachliche Einschätzungen, kein objektiver Benchmark und keine
Veröffentlichungsfreigabe für einen Film. Es gibt bewusst keinen gemittelten
Gesamtscore. Methodengüte und beobachtete Ausführungsreife sind getrennte Fragen.

## Vergleich auf acht Ebenen

| Ebene | Methode: Codex | Methode: Fable | Praktische Reife: Fable |
|---|---:|---:|---|
| Zielgruppe, Ideation, Story | 7 | 6 | 3 |
| Regie, Kontinuität, Rhythmus | 7 | 6 | 3 |
| Grafik und Produktbeleg | 7 | 7 | 4 |
| Audio und Synchronität | 6 | 5 | 2 |
| Unabhängige Prüfung | 7 | 7 | 4 |
| Technische Reproduzierbarkeit | 5 | 6 | 5 |
| Kostenkontrolle und Wirtschaftlichkeit | 7 | 5 | 3 |
| Command-EVE-Integration | 4 | 3 | nicht belegt |

Codex weist die aktuelle Story-/Regiereife als noch nicht belegt aus; Fable
ordnet sie aus dem bisherigen Nachweisstand niedrig ein. Das ist kein gemessener
Leistungsabfall nach dem Upgrade. Der vorhandene Pilot entstand vor den jüngsten
Korrekturen; danach wurde noch kein neuer vollständiger Film produziert.

## Übereinstimmung und Unterschiede

Beide Bewertungen sehen den Fortschritt bei Storyannahmen, Informationsrollen
und dem Umgang mit fehlerhaften Modellurteilen. Beide verlangen einen neuen
Durchlauf und technische Korrekturen, bevor weitere Reife behauptet wird.

Fable gewichtet die fehlende Gesamtwirtschaftlichkeit stärker. Codex bewertet
die vorhandenen Kostenbelege günstiger. Drei günstige Gemini-Aufrufe sind
nachgewiesen; Vollkosten pro akzeptiertem Film, Verkaufspreis und Marge sind
offen. Keiner der Berichte belegt bereits einen profitablen Produktbetrieb.

Fable möchte wiederverwendbare Grafikvorlagen und einen Bericht zu Sprachenden
an Schnitten. Das sind sinnvolle Kandidaten, wenn der nächste Durchlauf diese
Lücken bestätigt. Codex priorisiert zuerst den vorhandenen Ton-/Quellenpfad und
ein neues filmisches Ergebnis. Die direkte Editor-/SVG-Route bleibt zulässig;
aus fehlenden Message-Primitiven folgt kein Bedarf für ein weiteres Framework.

Folgende Präzisierungen verhindern, dass wir auch den Prüfer ungeprüft übernehmen:

- Quellton wird beim Normalisieren entfernt. **Stille wird nur ohne separate
  Sprach-/Musikdatei eingesetzt.** Diese bewusste Bildspurtrennung ist nicht in
  jedem Einsatz falsch. Es fehlt eine verlässlich nachvollziehbare Nutzung
  von Performance-Ton über die tatsächlichen Bildschnitte hinweg.
- Die Messungen beweisen Fehler bzw. uneinheitliches Verhalten der Helfer.
  Sie beweisen nicht, dass genau diese Helfer den Sync-Fehler des früheren
  Piloten verursacht haben. Fable kennzeichnet diese Ursache selbst als unbewiesen.
- Der Skill nennt bereits den lokalen Ort der Review-Records
  (`production/storyboard.md`) und Budgetanforderungen. Offen sind deren
  konkrete Produktintegration und Kundenabrechnung, nicht die Existenz dieser Regeln.
- Die gemessene Textmenge beträgt **14.314 Wörter in Markdown-Anleitungen**,
  davon **6.914 im Brand-Film-Skill**; alle 24 Dateien einschließlich Code
  enthalten 19.458 durch Leerraum getrennte Wörter. Das korrigiert die grobe
  Schätzung im Fable-Bericht. Es ist nicht die automatisch geladene Menge pro
  Auftrag: gezielte Referenzladung ist bereits vorgesehen.
- Fables starre Grenze „eine Textrevision pro Durchlauf“ wird nicht als neue
  Regel übernommen. Entscheidend sind begründete Änderungen und besseres
  Ergebnis. Ein ASR-Kandidat oder eine hohe Audiokorrelation allein beweist
  ebenfalls keine visuelle Lippensynchronität.

## Die nächsten Iterationen

Die Reihenfolge ist eine begründete Integrator-Empfehlung nach beiden Berichten,
kein vorgetäuschter gemeinsamer Konsens. Aufwand ist grob, Budget für neue
Generierung oder Produktbetrieb wurde durch diese Bewertung nicht vergeben.

| Reihenfolge | Ziel | Beobachtbares Abnahmekriterium | Aufwand / Grenze |
|---|---|---|---|
| 1 | Audioverhalten und Quellspannen am bestehenden Assembler korrigieren | `voice_volume=0` ist stumm; eine stille Musikspur verändert den vorgesehenen Sprachpegel nicht; ungültige Quellspannen werden vor dem Rendern abgewiesen oder ausdrücklich behandelt; angekündigte und tatsächliche Streamlängen stimmen. | Klein–mittel. Keine neue Audio-Engine. |
| 2 | Den Prüfer an bekannten gültigen und fehlerhaften Übergängen kalibrieren | Mindestens ein gültiger Off-/J-Cut und ein absichtlich vorgezogener Dialog werden auseinandergehalten. Bekanntes Audio-/Bildtiming statt allein ASR oder Korrelation als Referenz nutzen; Ungewissheit bleibt erkennbar. | Mittel. Zuerst vorhandene Timeline, Audio und Grenzframes; kein automatisches Qualitätsurteil aus einem Kandidatenbericht. |
| 3 | Einen vollständigen neuen Film mit aktueller Methode produzieren | Storyannahmen vorab fixieren; tatsächliche Bilder/Takes prüfen; fünf unbeteiligte Personen sehen den Film ohne Erklärung. Vorgeschlagene kleine qualitative Schwelle: vier erkennen die übernommene Arbeit und ihre menschliche Folge; keine ungelöste tragende Logiklücke. Kosten und notwendige Rettungseingriffe protokollieren. | Mittel plus separat freigegebenes Generierungsbudget. Kein statistischer Werbewirksamkeitsnachweis. |
| 4 | Wiederverwendbare Teile und Übertragbarkeit beweisen | Drei unterschiedliche Briefs mit derselben Methode; wiederkehrende Grafik-/Schnittprobleme am vorhandenen Owner lösen. Harte Schnitte gezielt unterstützen; Vorlagen nur bei belegter Wiederholung. Kosten und manuelle Eingriffe vergleichbar erfassen. | Mittel. Keine generische Studioplattform vor dem Nachweis. |
| 5 | Einen nativen Command-EVE-Durchlauf samt Abrechnung liefern | Anfrage → berechtigter Videoaufruf → Supervisorbewertung → verständliches Ergebnis → nachvollziehbare, einmalige Creditbelastung. Endkundenpreis, enthaltene Prüfungen und Marge ausdrücklich entscheiden. | Mittel–groß. Bestehende Hermes-, Provider- und Credit-Owner nutzen. |

Fable schlägt drei unbeteiligte Zuschauer vor, Codex fünf. Fünf sind hier eine
vorsichtige Wahl für den nächsten qualitativen Durchlauf, kein bereits getesteter
Standard. Scheitert derselbe tragende Ansatz zweimal, zuerst Prämisse, Staging
oder Werkzeugpfad ändern. Weitere Promptabsätze sind nicht automatisch die Lösung.

Der Integrationsrahmen lautet: `eve-flash` für Bearbeitung, `eve-max` als
MoA-Supervisor und Gemini für Video. Fable 5.1 ist Prüfer der Entwicklungsarbeit;
es ersetzt `eve-max` nicht. Diese Produktarchitektur wurde hier nicht zur Laufzeit geprüft.

## Technische Befunde reproduzieren

Die vier synthetischen Beobachtungen lassen sich ohne API und ohne private
Filmdatei erneut erzeugen. Voraussetzungen: Python 3, FFmpeg und ffprobe.
Im Repository ausführen und einen noch nicht vorhandenen Ausgabeordner wählen:

```sh
python3 assessments/2026-09-15/reproduce.py --output /tmp/eve-film-probes-unique
```

Optional prüft `--pilot /path/to/local-film.mp4` zusätzlich einen eigenen
20–90-Sekunden-Film mit dem technischen Validator. Das im Review verwendete
Pilotmedium wird hier nicht mitveröffentlicht. Die bekannte Sync-Beobachtung
ist daher ein berichteter Befund, kein öffentlich reproduzierbarer Blindtest.

Das Skript rendert fünf kleine synthetische Fälle, misst Streams und RMS und
schreibt `local-probes.json`. Es ist ein Reproduktionsskript für diesen
Bewertungsstand, keine vollständige Regressionstest-Suite. Ein später
korrigierter Assembler darf andere Ergebnisse oder einen frühen Fehler liefern;
zum Vergleich den oben genannten Source-Commit verwenden. Der portable
Reproduktionslauf lieferte dieselben vier synthetischen Ergebnisse wie der Erstlauf.

## Unabhängigkeit und Grenzen

Die Codex-Bewertung wurde vor Einsicht in Fables Antwort eingefroren. Fable
startete mit frischem Kontext, las alle 24 Skilldateien und dieselben neutralen
Probe-Ergebnisse, aber keine frühere Bewertung und keinen Codex-Bericht.
Beobachtete Datei-Leseaufrufe bestätigen diesen Umfang. Beide Urteile bleiben
Modellurteile; der Autor ist kein zweiter unabhängiger Prüfer.

Fable nutzte Claude Max. In dieser Systembewertung gab es keine neuen
bezahlten API-Aufrufe und keine Mediengenerierung. Nicht ausgeführt: neuer
vollständiger Film, Zielgruppentest, nativer Editor-/MCP-/Produkt-End-to-End-Test.
Alle noch offenen Befunde bleiben offen; ihre Dokumentation ist keine Reparatur.
