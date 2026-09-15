# Story logic, continuity and review decisions

This file owns staged review, cold comprehension checks and generation
sequence. Use the existing storyboard and editor; these internal checks do
not require a new user approval before each scene.

## Reviewer and perception

Choose someone who did not write, generate or edit the material: a fresh agent
session without the author's history, a separate model or an uninvolved person.
Use a different model family for independent model assurance when available;
follow any reviewer explicitly chosen by the user. An author checking their
own work does not satisfy this role. If no qualified reviewer is available,
record `not reviewed` and hold dependent production; continue useful independent
preparation. Do not silently replace the reviewer with the author.

Before review, record what the reviewer can actually inspect: still images,
continuous motion, audio, and the intended viewing size. Missing motion or
hearing leaves dependent checks `not reviewed`. Route those checks to a capable
reviewer or identify the exact remaining user handoff. ASR, frame samples and
meters support diagnosis; a player reaching the end proves playback, not
perception, lip sync, intelligibility or story understanding.

## Stage records and progression

Keep one `Review records` section in `production/storyboard.md`. Each record
contains: stage and exact material version; reviewer and allowed inputs;
perception available; observed understanding/findings with time/frame evidence;
`ready`, `revise` or `not reviewed`; and the specific fix or remaining check.
Preserve the cold response before adding the author's comparison. Long reports
may be linked from this record; no separate tracking system is required.

| Stage | Material | Decision needed before progressing |
|---|---|---|
| Storyboard | Complete story, essential assumptions and shot plan | Relationships, motivation and knowledge are adequately established; the turn is plausible and filmable. |
| Anchors | Ordered actual images, scene layout and adjacent boundaries | Required gaze, hands/props, action states and graphic roles connect. |
| Takes / edit | Actual clips with preceding/following context and original sound | Required meaning and continuity survive the delivered performance and cuts, within the declared perception scope. |

`ready` applies only to the stated stage and observed checks. A material failure
is `revise`; an absent check or capability is `not reviewed`. Neither becomes
ready because another dimension passed. Preserve a user's failed comprehension
as evidence even when an earlier model liked the written concept.

## Plausibility before staging

Use the storyboard's `Story essentials` section to state what the audience must
understand and where each needed relationship or piece of shared knowledge is
established. Check motivation, trust, elapsed time and everyday likelihood.
Possible is not the same as adequately established. A beat requiring invented
offscreen history is not ready. Simplify it or earn the missing information;
do not automatically repair it with more exposition. Irrelevant background
facts need not be established, and implication can be enough when supported.

## Cold comprehension protocol

1. Freeze the essential relationship, cause and turn in the storyboard before review.
2. Give a fresh reviewer only a neutral-named sequence and neutral delivery context.
3. Exclude script, prompts, narrative filenames/metadata, prior criticism and desired interpretation.
4. Ask for three short answers: what happened, who initiated it, and what changed; then uncertainties.
5. Save that response verbatim before exposing the storyboard or criticism for comparison.
6. Compare meaning, not exact wording, against the frozen essentials.
7. Missing or contradicted essential meaning is `revise`; no author explanation can convert that cold pass to success.
8. Repair the relevant story or staging and repeat with a fresh unprimed reviewer; absent perception/reviewer is `not reviewed`.

This protocol tests the rendered sequence. Storyboard criticism is a separate
stage that can read the script. Neither test requires a viewer to state every
intended emotional nuance, but the cause and change carrying the film must be
understood without the author's rescue explanation.

## Inspect anchors and actual joins

Use a simple room plan when geometry matters. Compare the previous ending and
next beginning for scene position, camera side, gaze target/height, relevant
hands and held objects, body posture, action phase and emotional state. Name
what remains continuous and what change or time ellipse is intended. Normal
movement during an offscreen reverse shot is allowed; not every pose change
is an error. A shared face reference protects identity, not all these states.

Inspect the actual last/first frames and a short moving interval on both sides
of every meaningful join. Retakes and source rearrangements require rechecking
the joins they affect. A pretty end-state portrait need not be a valid opening.

## Generate dependent shots in sequence

A shot is dependent when its start needs an earlier accepted action, prop,
gaze or pose. Produce and inspect that predecessor first. Where supported, use
its actual accepted boundary frame or short adjacent video as the next angle's
reference, keeping the identity reference separate. Bind the request to that
observed state, not a reset master portrait or hoped-for prompt ending.

Changing camera angle preserves world-space relationships and action phase,
not pixel coordinates. Verify current input support, transfer scope and budget;
neither an image nor video reference guarantees synchronous performance.
Independent settings and self-contained inserts may still run in parallel.
"Same room" alone does not establish independence.

## Keep repair proportionate

If several precise gestures, lines and emotional changes overload a shot,
simplify its staging before adding prompt instructions. Prove the hard turn
with a short connected sequence. A cutaway must belong to the story and cannot
by itself certify that an incoherent join is solved. Recheck the affected
stage, record the result and continue only within its supported scope.
