---
name: produce-brand-film
description: Create, repair or review brand, product, launch and advertising films, including repeatable code-rendered motion studios and hybrid films. Use for creative direction, characters, footage, motion, narration and audiovisual delivery. For a footage-only edit without a campaign brief, use video-editing.
---

# Produce Brand Film

Own the film from brief to a reviewable master using the available editor and
media pipeline. The sibling [video-editing](../video-editing/SKILL.md) skill
supplies native editing operations; no second production system is needed.

## Choose the relevant parts of the skillset

Use [the skillset map](references/skillset-map.md) to select an existing authoring,
image or editing skill. Load only the branch the project needs; a film does not
need every renderer. For recurring people or mascots, use
[character look development](references/character-lookdev.md). For code-rendered
or hybrid motion work, use [the motion studio contract](references/motion-studio.md).
For spoken narration, use [narration production](references/narration-production.md).
These extend this film workflow; story and review remain with their existing owners.

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
   Derive concrete style choices from inspected references and prove the chosen
   character/material look and renderer settings on representative frames before
   a long export. Code, captured footage and generated media may coexist; choose
   them for the visual result, not because one renderer is already running.
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
   [manifest guide](references/timeline-manifest.md). Apply the
   [action and rhythm pass](references/film-craft.md#rhythm-belongs-to-action-and-sound)
   to the actual takes before settling their lengths. Keep dialogue, music and
   selected ambience separate from picture inserts. Probe delivered media;
   no-audio requests do not guarantee silence. Define the sound direction from
   the brief before selecting music: emotional movement, instrumentation, pace,
   space for speech, and the role of each effect. Reuse approved music or audition
   recorded tracks from a licensed library. With no existing library, start the
   search at [Mixkit](https://mixkit.co/free-stock-music/); existing Artlist or
   Epidemic Sound access is another option. Verify the selected asset's license
   for the actual delivery; do not assume catalog access permits redistribution
   or client advertising. Do not purchase a plan without authorization.
   For a new brand sound or a rejected soundtrack, present 2–3 short playable
   candidates against the same passage before committing the edit. Do not use
   `generate_score.py`, ad-hoc sine waves, drones or repetitive ticks as fallback
   music. Procedural music belongs only to an explicitly requested sound concept,
   with qualified listening. Short locally authored effects may serve the agreed
   sound direction; they still need hearing in the actual mix. If no suitable reviewed audio is available, deliver
   a clearly labeled silent picture draft and keep sound completion open.
   Local assembly uses Python 3, FFmpeg/ffprobe, librsvg and Fontconfig; kinetic
   text produces alpha, motion, font and decode receipts. For Final Cut retain
   FCPXML declaration/DOCTYPE and previously imported asset UIDs, then verify
   native import. Parsing XML is not that verification.

6. **Review and deliver the exact version.** Before assigning review checks,
   declare the reviewer's available image, motion and audio perception using
   the staged review method. For a low-cost audiovisual model pass, use
   [Gemini video review](references/gemini-video-review.md), then give its
   evidence and contradictions to a reviewer who did not write, generate or
   edit the film. The user's selected Fable model can fill that role only if
   uninvolved; otherwise label its contribution supervision and follow the
   staged method for the independent check. Missing hearing leaves sound-dependent checks
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
