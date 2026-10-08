# Code and hybrid motion studio

Read for code-rendered or hybrid films. Story and quality progression belong to
[continuity and review](continuity-and-review.md); this reference adds medium
selection, render behaviour and reusable production decisions.

## Choose the visual route before committing to a renderer

| Need | Useful route | Prove early |
| --- | --- | --- |
| Exact UI, type, logo, chart or diagram | Code/vector/native motion | Source accuracy, readable state changes and deterministic seeking. |
| Expressive people, organic acting, tactile materials or photoreal scenes | Captured footage or generated image/video, or a demonstrably suitable character renderer | The actual face, body, motion and material look; an engine benchmark is insufficient. |
| A story with exact product proof | Hybrid: people/world footage with native/code UI and brand graphics | Identity/scene continuity and legible overlays in context. |

Canvas/SVG may be enough for a small piece. Existing Three.js, HTML/HyperFrames,
React/Remotion or Tesseract projects may already provide the complete path.
Choose one authoring owner and reuse it. Do not migrate frameworks because the
article names another one. If the user requires code-only work, test a suitable
intentional style within that constraint and explain a demonstrated limit
instead of silently introducing generated media.

## Make the visual grammar concrete

Inspect a relevant supplied reference, or select one within the granted
creative remit. Record useful observed traits in `production/style-guide.md`:
palette, type hierarchy, framing/density, meaningful pacing, motion character,
light/material/texture and the clichés to avoid. Separate actual observations
from interpretation; do not infer sound from stills. Translate the grammar into
original work while retaining exact approved brand/product assets.

Use the storyboard's existing shot plan. Every shot has a narrative job,
entry/exit state and source route. A list of zooms, particles and morphs is not
a substitute for what the viewer learns. A narrator, when required, is part of
that plan rather than a late decorative layer.

## Render contract

A frame should be obtainable as a query such as
`renderFrame(time, spec, assets, seed)`, or the chosen framework's equivalent.

- Derive the visible state from explicit time/frame number; support seeking
  directly to a later frame without first playing the preceding frames.
- Keep random variation seeded and inputs fixed. Wall clocks, live network
  data and accumulated animation state must not determine the rendered frame.
- Finish required asset/font loading before capture; use a fixed viewport,
  duration/frame rate and a known colour pipeline.
- Put animation, media placement and sound cues on one source timeline. Record
  real input/output ranges; time placement does not implicitly retime footage.
- Check the same frame through direct seeking, shuffled seeking and sequential
  playback. Compare actual outputs; distinguish a wrong visual state from
  documented codec/GPU rounding. A source hash alone does not prove determinism.

Follow the selected runtime's own contract and adapters. Do not invent SDK
fields or replace its native seeking/media ownership with another timer loop.

## Prove appearance and the export path before a long render

1. Inspect representative frames in the actual intended style, including the
   difficult human/product interaction. For recurring characters, use
   [look development](character-lookdev.md) first.
2. Render a short connected passage through the intended export settings.
   Compare final-quality frames with the accepted preview: brightness/colour,
   alpha, layering, font fit, shadows and motion must survive supersampling and
   motion blur. Verify accumulation/clear/blend behaviour where applicable.
3. Include required voice/music/cues in an early timed passage. A contact sheet
   tests layout; motion and sound require their own observed checks.
4. Record the largest evidenced defects and repair their owners. A systemic
   renderer fault invalidates dependent exports; a rejected character style
   needs design/medium work, not only more pixels or rescaled limbs.

Use the existing review records to state what was examined, by whom, with which
perception, and what remains open. Choose the smallest adequate sample rather
than automatically rendering a full film after each edit. The author may
prepare and repair; their judgement does not become independent acceptance.

## Motion, sound and formats

Give movement intent and hierarchy: small controls may be quick, large panels
may settle, cameras should preserve orientation, and important copy needs a
readable hold. Springs and overshoot are options, not a treatment for every
object. Review the rendered action at the expected viewing size.

Map action cues and chosen musical events to the same timeline. Follow
[film craft](film-craft.md#rhythm-belongs-to-action-and-sound); not every cut or
gesture needs to hit a beat. Hear the exported passage when sound quality is
being judged; meters and automatic beat detection are supporting evidence.

For requested aspect-ratio variants, recompose hierarchy, type, framing and
safe areas from the same story/source. A centre crop is adequate only when the
actual content demonstrably survives it. Check each requested version; do not
add unrequested formats or cloud rendering as automatic extra scope.

Keep the repeatable render command, editable source, style decisions, assets,
review evidence and exports together. Probe and fully decode final files;
provide practical web copies when needed while retaining the master. Report
actual quality/perception limits separately from successful encoding.
