---
name: produce-brand-film
description: Create or repair complete 20-90 second brand, product, launch and advertising films from a brief and real assets. Use for story, art direction, footage generation, edit, typography and sound through a reviewable master. For an existing-footage edit without a campaign brief, use video-editing.
---

# Produce Brand Film

Own the film from brief to a reviewable master using the available editor and
media pipeline. The sibling [video-editing](../video-editing/SKILL.md) skill
supplies native editing operations; no second production system is needed.

## Workflow

1. **Resolve the brief and sources.** Record audience, intended takeaway,
   delivery, current product/offer truth, approved logo, UI, fonts, footage and
   audio. Treat locale and style as campaign choices. Use fictional people
   unless consented likeness assets were supplied; anecdotes are not customer
   testimonials. Keep the user's actual spending and publication scope explicit.

2. **Develop meaning, then the story.** Use [film craft](references/film-craft.md)
   to explore human observations and competing premises. Critically revise the
   selected story before choosing scenes, detailed camera, edit or music.
   Record its essential relationships, knowledge and viewer inferences in the
   [storyboard](references/storyboard-contract.md). The
   [staged review method](references/continuity-and-review.md) owns plausibility,
   independent review and progression decisions. Prove the hardest causal turn
   in a short connected rough sequence before the dependent footage batch.

3. **Plan images and information.** Review the ordered actual anchor images
   against the storyboard's scene states. Separately choose graphic roles and
   review their human/proof/end frames using
   [cinematic graphics](references/cinematic-graphics.md). Instantiate font
   weight/axes, retain exact brand artwork and compose over the selected motion.
   Functional UI and editorial type need not share the same visual grammar.
   The optional [kinetic policy](references/timeline-manifest.md#optional-kinetic-policy)
   is a specific renderer contract, not the default meaning of "cinematic".

4. **Generate for the planned cut.** Prefer real product media where available.
   Verify the current provider, input support, output, auth and budget with a
   scoped authorized shot before a batch. For Grok Build, use
   [media routing](references/grok-media-routing.md). Follow the staged review
   method for dependent reference chains; preserve source files and inspect the
   actual usable ranges. Exact text, values and logos require verification;
   generated UI remains an illustrative representation, not recorded execution.

5. **Edit picture and sound.** Use the existing editor or
   `scripts/assemble_film.py --manifest <timeline.json>` with the
   [manifest guide](references/timeline-manifest.md). Keep dialogue, music and
   selected ambience separate from picture inserts. Probe delivered media;
   no-audio requests do not guarantee silence. Use `generate_score.py` only
   when an original procedural score serves the brief, then assess its quality.
   Local assembly uses Python 3, FFmpeg/ffprobe, librsvg and Fontconfig; kinetic
   text produces alpha, motion, font and decode receipts. For Final Cut retain
   FCPXML declaration/DOCTYPE and previously imported asset UIDs, then verify
   native import. Parsing XML is not that verification.

6. **Review and deliver the exact version.** Before assigning review checks,
   declare the reviewer's available image, motion and audio perception using
   the staged review method. Missing hearing leaves sound-dependent checks
   `not reviewed`; arrange a capable reviewer or leave a precise user handoff.
   Apply [review gates](references/review-gates.md), perform the qualified
   full-film viewing, and run `validate_film.py` with a matching contact sheet.
   For the explicit kinetic policy also supply `--manifest` and `--render-dir`.
   Resolve the observed failures at their owner before extending scope.

## Output

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

The storyboard holds story essentials and staged review records; validation.json
holds the technical validator output. Retain sources unchanged. Default master:
H.264/yuv420p/AAC, 1920x1080, 24 or 30 fps, faststart, unless the brief differs.
Report the reviewed version, actual evidence, unresolved checks and user's
acceptance separately. A technical PASS does not establish creative quality,
real product execution or permission to publish.
