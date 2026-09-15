# Review gates

Start by declaring the available image, motion and audio perception as defined
in [continuity-and-review.md](continuity-and-review.md#reviewer-and-perception).
A sound-dependent check without hearing is `not reviewed`, not passed through
ASR or meters. That file owns reviewer selection, cold comprehension, stage
records and progression decisions. Apply the relevant checks below to an exact
material version; use the [craft rubric](film-craft.md#diagnose-creative-failure-without-laundering-a-technical-pass)
when deciding which failure needs repair.

## Story

- The opening establishes a recognisable situation or dramatic question.
- Essential assumptions in the storyboard are supported; the turn follows from
  the product's contribution and an intelligible human choice.
- The cold response satisfies the frozen essential meaning under the review
  protocol. Record absent or contradicted essentials instead of explaining them away.

## Brand and claims

- Original logo artwork, approved colors and product stage are accurate.
- Actual product UI claims have a reference. Generated or conceptual UI follows
  [UI provenance and claim class](cinematic-graphics.md#ui-provenance-and-claim-class).
- Exact wording and values are legible; staged results are clearly examples.
- No unsupported testimonial, metric, partnership or real customer depiction.

## Picture and graphics

- Identity, anatomy, objects, eyelines and action states hold across the actual
  joins, within the continuity method's allowance for motivated offscreen change.
- Each cut and held shot serves the scene; performances convey the needed change.
- Graphic form makes its role and speaker clear; check entrance, readable hold,
  state transition and exit beside the human action at delivery size.
- Effective font axes/weight, contrast, safe area and face/gesture clearance work.
- Generated lettering stays correct throughout its used interval. Retain required
  source provenance marks; reject unexpected marks rather than hiding them.

## Sound — only with qualified hearing

- Complete dialogue is understandable at the intended playback level.
- Music supports the scene and does not mask speech; edits and the tail sound natural.
- Selected source sound does not duplicate or replace the separate master tracks.
- A muted pass tests visual comprehension separately; optional captions are identified.

## Technical checks

- Duration, dimensions, frame rate, audio sample rate and channel layout match delivery.
- H.264/yuv420p/AAC master decodes fully and has faststart for web playback.
- Contact sheet and source/timeline mapping belong to the delivered version.
- For the explicitly selected [kinetic policy](timeline-manifest.md#optional-kinetic-policy),
  provide manifest and render directory. Check receipts for copy/font hashes,
  frame counts, alpha and motion evidence. This checks the manifest path, not
  every visible text surface in the finished film; readable holds are supported.

## Handoff

Keep the technical validator output separate from storyboard review records.
Report unresolved or unreviewed checks and the user's actual acceptance state.
Technical results cannot substitute for creative acceptance or publication authority.
