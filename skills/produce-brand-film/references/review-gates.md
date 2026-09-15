# Review Gates

For the first integrated review or a rejected film, use the compact
[creative failure rubric](film-craft.md#diagnose-creative-failure-without-laundering-a-technical-pass).
Apply the relevant checks below to the exact delivered master. Record technical
results, creative observations, product/claim evidence and the user's acceptance
separately; no combined PASS or ungrounded numeric quality claim follows from them.

## Stage and evidence

For connected narrative scenes, use [continuity-and-review.md](continuity-and-review.md):
review the finished storyboard, the ordered actual reference images, and the
actual takes with their neighbours before promoting each stage. Begin the
scene/film review with an unprompted account of what was understood; reveal
the script only afterward. State when only frames, metadata or ASR were
available. Such evidence does not establish full audiovisual comprehension.

## Story Gate

- The opening establishes an intelligible human situation or dramatic question.
- Motivations, relationships and shared knowledge make everyday sense without
  invented offscreen backstory; possible is not the same as adequately established.
- Escalation adds pressure instead of repeating the same failure.
- The product appears as the causal turn, not as an unexplained logo reveal.
- Proof shows mechanisms the product actually supports.
- At least one human or visual motif returns after the turn.

## Brand And Claim Gate

- Logo, approved colors, product stage, and UI are source-backed.
- Exact copy is deterministic and readable.
- No real customer is depicted without supplied consented assets.
- No invented testimonial, metric, partnership, integration, or competitor
  failure claim appears.
- Aspirational scenes are clearly product vision or generic narrative, not fake
  live evidence.

## Picture Gate

- No broken anatomy, identity drift presented as continuity, accidental logos,
  unreadable generated text, or unsafe screen content. Preserve required native
  provenance marks; reject unexpected marks and never crop, alter, or obscure a
  provider watermark.
- Cuts are motivated and every shot earns its duration.
- Actual outgoing/incoming gaze, hands, props and action states connect, or a
  deliberate offscreen change/time ellipse is understandable. Check the join
  in motion; matching identity portraits alone do not prove continuity.
- The grade has an intentional before/after arc.
- UI is readable long enough to understand but not exposed as private data.

## Graphics-in-context Gate

- Graphic form communicates its chosen function: input, message, artifact,
  status, editorial context or brand statement.
- Titles and proof inserts share the film's light, material, palette and pace.
- A neutral placeholder or default rounded panel has not been silently promoted
  into the final design. Minimal white imagery remains a valid deliberate choice.
- Check a dialogue frame, a proof frame and a title frame side by side, plus the
  actual entry, readable hold and exit of each graphic treatment.
- Variable-font axes and weight are explicitly set in the renderer. A correct
  font family alone does not establish the intended appearance.
- Generated lettering passes whole-shot spelling, value and temporal-stability
  checks; otherwise use a clean plate and an exact text/brand layer.

## Kinetic Type Gate

- If `text_policy` is `kinetic_only`, no scene contains a static `overlay`,
  lower-third panel, or persistent caption strip.
- Every visible phrase has a motivated entrance or transformation and a clean
  settle; motion supports hierarchy instead of animating every letter for its
  own sake.
- Copy, manifest, font, frame-count, alpha-format, decode, and motion-proof
  checks pass in every `scene-XX-kinetic-receipt.json`.
- Enter-middle, settled, and exit-middle proof frames are inspected at full
  resolution. Automated receipts prove motion and determinism; a human still
  judges rhythm, legibility, and whether the result feels current.

## Sound Gate

- Generated picture inserts and title/proof intermediates do not replace or
  double master audio. Inspect returned tracks, not only the no-audio request.
- Dialogue or voice is intelligible on laptop speakers.
- Music supports the turn and never masks words.
- No clipping, long digital silence, abrupt tail, or unlicensed source.
- The film still communicates when muted.

## Technical Gate

- Final duration matches the brief.
- H.264/yuv420p/AAC master decodes from start to finish.
- Resolution, frame rate, aspect ratio, and audio sample rate are stable.
- `faststart` is enabled for web playback.
- Contact sheet and validation receipt match the delivered master.
- A `kinetic_only` delivery was validated with both `--manifest` and
  `--render-dir`; a plain MP4 probe is not sufficient.

## Creative Acceptance

- The actual integrated master was watched at normal speed with sound and muted;
  an animatic, contact sheet or intermediate is identified as such.
- Report the viewer's understood cause, action and outcome, plus any failed
  dimension/timecode. Do not infer comprehension from a successful export.
- Preserve a user's rejection or rating as their judgment until they assess a
  revision. A technical repair is evidence of that repair, not creative acceptance.
