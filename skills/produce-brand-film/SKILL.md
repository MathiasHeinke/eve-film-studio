---
name: produce-brand-film
description: Create or repair complete 20-90 second brand, product, launch and advertising films from a brief and real assets. Use for story, art direction, footage generation, edit, typography and sound through a reviewable master. For an existing-footage edit without a campaign brief, use video-editing.
---

# Produce Brand Film

Own the film from brief to a reviewable master. Use the existing editor and
media pipeline; this skill does not add agents, providers or permission systems.
For native editing and generated inserts in existing footage, use the sibling
[video-editing](../video-editing/SKILL.md) skill for those operations.

## Workflow

1. **Resolve the actual brief and sources.** Read current positioning, release
   stage and offer boundaries. Inventory approved logo artwork, UI, fonts,
   colors, footage and audio. Record audience, desired takeaway, delivery and
   the user's creative choices in the project. Locale, setting and style are
   campaign choices; do not infer permanent preferences from one film.
   Customer anecdotes are problem evidence, not testimonials. Use fictional
   people unless consented likeness assets were supplied. Distinguish a private
   experiment, review draft, paid ad and public launch; authorization is scoped.

2. **Resolve meaning before selecting scenes.** Answer the human want,
   contradiction, dramatic question, discovery and causal product contribution.
   If these remain open, work on the concept; do not start a footage batch.
   Develop human observations into a story, critique and revise it, then write
   the script and choose scenes before detailed camera, edit and music. Read
   [film-craft.md](references/film-craft.md) and use the existing
   [storyboard contract](references/storyboard-contract.md). Connect a concrete
   need, the product's action, its visible result and a human consequence.
   Use [continuity and staged review](references/continuity-and-review.md)
   to challenge everyday plausibility and the finished storyboard before staging.
   Define shot purpose, source/timeline ranges, continuity, copy, sound and
   transitions. Make a small rough sequence with the hardest causal turn and
   adjacent shots; a collection of attractive keyframes cannot prove the edit.

3. **Design information inside the film.** For messages, product proof and
   titles, read [cinematic-graphics.md](references/cinematic-graphics.md).
   Choose the graphic grammar by its narrative function: input composer,
   assistant message, artifact/status, editorial context or brand statement.
   Review the ordered actual anchor images and a human/proof/end frame together
   before rendering a dependent scene or its text sequence. Use the approved logo asset, explicitly instantiate
   font weight/axes and compose the ending over the actual final moving shot.
   Use `text_policy: kinetic_only` only when the brief actually requires that
   restriction. A request for filmic integration does not forbid a readable
   composer, message bubble or appropriate lower third.

4. **Generate only footage needed by the planned cut.** Prefer real UI and
   product media for proof. For new generation, confirm the available tool,
   auth lane, quota and output with one authorized scoped shot before a batch.
   For Grok Build, read [grok-media-routing.md](references/grok-media-routing.md);
   a consumer subscription does not imply API credits. Preserve identity with
   references or one continuous arc; reject drift presented as continuity.
   Generate connected action/eyeline shots in sequence from the predecessor
   ending actually accepted; independent shots may still run in parallel.
   Keep logos, URLs, values, status and critical copy exact. A requested
   generative headline needs whole-shot spelling/stability inspection.

5. **Edit picture and sound deliberately.** Read the rhythm/audio sections of
   [film-craft.md](references/film-craft.md). Reuse the current native editor or
   `scripts/assemble_film.py --manifest <timeline.json>`; the
   [manifest reference](references/timeline-manifest.md) owns its schema.
   Keep source files unchanged, generated visual inserts silent and master
   dialogue/music on their own tracks. Probe delivered media before insertion.
   Use `scripts/generate_score.py` when an original score suits the brief;
   inspect its musical quality instead of treating a generated WAV as finished.
   With FFmpeg assembly, verify Python 3, `ffmpeg`, `ffprobe`, `rsvg-convert`,
   `fc-scan` and `fc-match`. Typography uses render-local Fontconfig and exact
   SVG layers; kinetic text also produces alpha, motion and decode receipts.
   For Final Cut handoffs retain the FCPXML declaration/DOCTYPE and existing
   asset UIDs, then verify native import. XML parsing alone is not that proof.

6. **Judge the delivered film.** Use [review-gates.md](references/review-gates.md)
   and its failure-rubric link. Watch the complete master at normal speed with
   sound and muted, including real-size legibility and the final sound tail.
   Run `scripts/validate_film.py` and create a matching contact sheet. For
   `kinetic_only`, pass `--manifest` and `--render-dir` as well. Let a reviewer first describe the actual connected sequence without the
   explanatory script, then compare it with the intended story. Technical
   validation, creative assessment, product truth and the user's acceptance
   are separate outcomes. Do not invent a quality score or call an unaccepted
   revision an 8/10 because it exports successfully. Address the specific
   observed failure before increasing scope, generations or tool count.

## Output Contract

Use a durable output folder:

```text
<film-root>/
  final/<slug>-master.mp4
  final/<slug>-contact-sheet.jpg
  production/storyboard.md
  production/timeline.json
  production/prompts-and-provenance.md
  production/validation.json
  sources/
  work/
```

Keep the `sources/` originals unchanged. The master defaults to H.264, yuv420p,
AAC, 1920x1080, 24 or 30 fps, and `faststart` unless the user names another
target.

Report the exact reviewed version, checks actually run, unresolved creative
issues and acceptance state. A staged product result remains an illustrative
example; neither an attractive film nor technical PASS establishes that the
product executed the depicted workflow or that publication is authorized.
