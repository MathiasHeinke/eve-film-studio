# Modular editing toolbox

Choose modules from the actual material and the user's brief. EVE can notice
useful opportunities without being prompted, while the user decides the desired
result and which treatments belong in it. Do not impose a cinematic grade,
music, captions, AI shots or aggressive shortening on every video.

Use existing editor features, connected MCP operations and maintained helpers.
Read `community-sources.md` when a missing capability needs focused discovery.
A guide in this package is not proof that the corresponding tool is connected.

## Modules and decision rules

| Module | What EVE can prepare/do with the appropriate tool | What determines whether to use it |
|---|---|---|
| Transcript/story edit | Find whole statements, select takes, remove/reorder passages using word timestamps | Meaning, wording, narrative order and requested duration |
| Pauses, filler and retakes | Propose speech-boundary cuts and remove unwanted dead space or false starts | User's rhythm; breathing, emphasis, laughter and musical rests are not automatically defects |
| B-roll | Search provided assets or authorized stock; plan/generate a missing insert | What the audience needs to see at this exact point; existing suitable footage often suffices |
| Camera/coverage | Recommend and plan another viewpoint or a motivated reveal | Use `camera-direction.md`; choose the moment before the angle and rendering |
| Color correction | Match exposure, white balance and adjacent shots using the editor's color controls | Technical consistency before an optional creative look |
| Creative grading | Propose a coherent look and apply it on a recoverable version | Project tone and user preference, not a fixed preset |
| Speech/audio cleanup | Address noise, uneven levels and intelligibility with available audio tools | Listen first; retain a natural voice and intentional room sound |
| Music and sound design | Align music, use suitable ambience/SFX, balance or duck against speech | Existing recording, desired emotion, rights and actual delivery context |
| Captions | Produce time-aligned captions, names and optional readable styling | Whether requested/useful, target language and available screen space |
| Framing and stabilization | Reframe for a target aspect ratio, track the relevant subject, stabilize where helpful | Preserve the action and avoid excessive crop or distorted motion |
| Rhythm and transitions | Use motivated cuts, reaction shots or J/L audio transitions where appropriate | Beat, dialogue, continuity and user style; effects are optional |
| Export and versions | Deliver a preview, final media and editable project in the requested format | Actual codec, frame rate, aspect ratio, color and platform requirements |

## Text and silence cuts

Read the existing transcript or use the configured transcription path once,
then retain its source/time mapping. Inspect picture and sound at candidate
boundaries. Cut whole words and meaningful units, not arbitrary character spans.
Distinguish repeated takes and repeated phrases before removing anything.
Check grammar, intended meaning and the incoming/outgoing sound after a reorder.

Silence detection produces candidates. Preserve a deliberate pause, breath,
reaction or singing rest unless the brief calls for changing that rhythm. Do
not treat song phrasing as ordinary filler speech. Use suitable existing fades
or room-tone handling when needed, with real audio handles; a fixed fade on
every word boundary can damage speech. Verify the rendered cut for clicks and
missing consonants, not just the source waveform.

## Color and sound

Inspect the source and project color management before adjusting an image.
Correct unintended shot-to-shot differences first; apply a creative treatment
only when it serves the brief. Keep HDR/SDR intent and source files intact.
Do not force every project through the pilot's SDR working-copy settings or
assume a named LUT makes mixed footage consistent. Check faces, highlights,
shadows and neighboring shots in the actual result.

Keep the original performance as the sound owner for a picture-only insert.
For an authorized audio edit, compare the actual mix before/after for clipping,
noise pumping, abrupt level/ambience changes and synchronization. Use the target
delivery specification for loudness rather than hardcoding one value for every
platform. Do not synthesize a new voice, replace a song or add stock music merely
because an audio module is available.

## B-roll and generated material

Determine source/timeline in/out and the insert purpose first. Search existing
project footage before buying or generating material. Respect the media's
actual usage rights and the task's budget. Use `generated-inserts.md` only for
the generative branch; unrelated illustrative footage is not a synchronized
second camera. Place each accepted insert at its planned time marks and inspect
both cut boundaries with the original sound.

## Honest readiness

The package contains workflow knowledge and a tested FCPXML MCP fixture. The
completed pilot verifies synthetic phrase removal, real H3 generation, exact
two-second picture insertion, preserved audio timing and native FCP export.
It does not yet verify real transcription, a full color/audio finishing pass,
captions, real multicam or every alternate editor in the shipped EVE app.

At task start, distinguish a ready connected tool from available guidance and
missing setup. Prepare the missing connection through existing EVE owners;
never claim that a skill file alone installed an editor, transcription provider
or customer media service. Reuse the ordinary EVE permissions and budget, not
the developer's one-off credentials or prior pilot authorization.
