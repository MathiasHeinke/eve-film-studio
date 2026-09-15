# Generated inserts from original material

Reuse a configured reference-video/editing provider or existing VFX skill.
Hermes `video_generate` already knows Seedance 2.5 and Veo 3.1 in the inspected
FAL catalog, but that does not make an original-video editing endpoint available.
The inspected tool rejects `video_url`/`operation` and directs edit/extend to
provider-specific tools. Discover actual capabilities before selecting a model.

## Find the edit point first

The workflow starts with the original edit, not with video generation. Watch
the relevant footage and listen to the original audio. Identify where a cut
improves the story: a speaker or gesture change, a useful detail, a jump cut to
cover, a camera movement to conceal, or a deliberate change of visual emphasis.
Choose a specific slot and decide what it needs before spending a render.
For scene selection and camera treatment, use `camera-direction.md`: a
user-highlighted singing moment should drive the shot, not an arbitrary frame
or the first convenient technical defect. Specify why the chosen angle serves
that moment before choosing the model.

Use the project's existing markers, EDL or edit notes to bind:

- Source asset and source in/out, and separately the destination timeline in/out.
- The actual project timebase and exact required frame count.
- Purpose: parallel camera angle of the same action, or illustrative B-roll.
- Action, gaze, object state and sound at entry/exit that must remain continuous.
- Reference interval, requested generation duration, any justified extra handles,
  and the planned mapping from generated frames to that slot.

Keep these references in the existing project workflow; no second job ledger is
needed. If the user points to “here”, resolve the current playhead/selection
when they speak. Do not substitute a later playhead position.

## Route the planned shot

- **New perspective or changed original shot:** inspect a video-to-video or
  reference-video tool. Pika's existing `vfx`/`4k-vfx` skills and Runway Aleph
  are candidates; exact model version, access and pricing need a current check.
- **A new shot from selected reference frames:** the configured image-to-video
  route may suffice. This does not preserve an original performance by itself.
- **Reframe:** a crop or resize can be a normal editor operation and does not
  require generative video.

A parallel camera angle changes viewpoint while preserving the same moment,
participants, action order and timing. A new pose in a similar scene does not
pass that test. B-roll can illustrate the ongoing dialogue without depicting
the same timed gesture, but must be chosen for that purpose before generation.
An unfaithful camera replacement must not silently be relabeled as B-roll.

## Derive duration and reference from the slot

Required insert duration comes from the planned timeline interval, not a
provider default. Derive the matching source interval through the existing
edit/retiming map; send enough adjacent frames to understand entry and exit.
Ask the model for the same timed action from the specified new camera position.
Describe what happens when, not just who and what appears in the scene.

When the provider's minimum duration exceeds the insert, choose the smallest
supported generation that contains the planned slot and any needed handles.
Define which part will be used before submitting. For example, a 2-second slot
at 24 fps needs 48 inserted frames. If a model requires 5 seconds, a planned
1.5-second lead handle + 2-second insert + 1.5-second tail handle is acceptable;
map output [1.5, 3.5) to the chosen timeline slot. Those numbers are an example,
not defaults. Do not stretch a clip to fill a slot or invent extra work merely
to consume the generated duration.

Probe the actual output: request duration and audio flags are not delivery
guarantees. Check the planned output subrange, frame-rate conversion and timed
action before insertion. If it cannot match the slot, report the failure and
prepare a revised shot within the user's scope/budget; do not move the cut to
make an unrelated generation appear successful.

## Keep the edit grounded

Use the smallest source interval needed for the requested shot. Bind source
asset/time range, intended timeline range, what may change, what must remain,
and the user's actual budget/data-transfer authority. A long project is not
permission to upload all footage or generate unlimited variants.

Keep the original recorded audio unless changing it was requested. Review the
entire output for identity, anatomy, object shape, motion, eyeline, screen
direction, light, text/logos and the incoming/outgoing cut. A generated angle
invents unseen detail; it is not a recovered second camera recording.

Use the provider's existing job ID/progress/resume behavior. Reconcile an
uncertain job before retrying so a timeout does not become another paid render.
Put accepted footage into a recoverable edit version and preserve its provenance.
Do not describe a preview or pending job as a finished shot.

## OpenRouter reference-video branch

OpenRouter's maintained `openrouter-video` skill and asynchronous video API are
the existing provider workflow to reuse. The model catalog was queried on
14 September 2026: `bytedance/seedance-2.5` takes video references; the Veo 3.1
route takes image references. Recheck the live catalog for a new setup.

Use `input_references` with a `video_url` entry for original footage. Do not add
`frame_images` to this request: that changes the generation mode. Discover
supported duration, resolution and ratio before submission. The generic
Hermes `video_generate` tool is not proof that this reference-video API is wired.

The tested OpenRouter generation request rejected an inline video data URL
with HTTP 400: “Only HTTPS URLs are allowed”. No job ID was created. Chat video
input and generation reference input have different transport restrictions.
An OpenRouter uploaded file is not a substitute for a downloadable HTTPS URL.
Use an already authorized private media store with a time-limited read URL;
never put private footage in a public application-download bucket. The expiry
must cover queueing and generation. A signed URL expires access, not storage.

The measured catalog rate for Seedance 2.5 with video input was
USD 0.0000064 per video token. Estimate both reference and output duration:
`(input_seconds + output_seconds) * width * height * 24 / 1024 * rate`.
A six-second 1280×720 reference and six-second output estimate USD 1.65888.
Use the live rate and actual dimensions; reconcile the final reported charge.
An admission reservation is not the final bill. Retain a received job ID and
resume it rather than submitting a second paid job after an uncertain response.

## Phone-footage preparation observed in the pilot

A rotated 4K/60 iPhone HLG clip imported through Final Cut's normal media path,
but a reconstructed FCPXML reference failed with mismatched video frame rates.
Changing just the source frame-duration field did not repair it. The working
route was a new native 1080p/60 Rec.709 project using the already imported media,
followed by a native H.264 export. The exported file was probed as 1920×1080,
60 fps and BT.709. Only then was a six-second, 720p/24, silent reference derived.
The user's source and original project were retained. This is a tested fallback
for this footage, not a reason to transcode every project to those settings.

Synthetic imagery may invent unseen geometry, so even a timed camera replacement
is generated footage, not a recovered second camera recording.

## Provider rejection observed, 15 September 2026

After the private HTTPS transfer was verified, OpenRouter/Seedance 2.5 rejected
the supplied real-person clip with HTTP 400 and
`InputVideoSensitiveContentDetected.PrivacyInformation`. No job ID or generated
video was returned. This is a provider/input restriction, not an FCP or MCP
failure. Do not promise that arbitrary customer footage can use this route.

Check the provider's supported, consented real-person workflow before treating
it as available. Do not repeatedly resend the same input, conceal the rejection,
or replace people's identities to manufacture a successful test. Google's
current Veo 3.1 documentation limits person generation for image/reference
inputs to adults; do not assume it is an equivalent route for a family clip.
When a provider restriction changes the intended shot, offer a concrete
alternative such as a person-free environmental cutaway or another authorized
reference. Keep that change explicit and within the original spending limit.

## MiniMax H3 candidate

When requested or suitable for the actual input, inspect the current
`minimax/hailuo-3` route rather than assuming every provider shares Seedance's
input restriction. MiniMax documents reference-to-video; OpenRouter's current
model metadata lists image, audio and video inputs, 2K output, 5–15-second
durations and USD 0.13 per output second. Input/reference charges and current
pricing must be checked too. H3 and H3 Max are different catalog entries.

The pilot's H3 job completed with the real-person video reference after
Seedance's rejection, costing USD 0.78. Requested: 6 seconds without audio.
Delivered: 2560×1440, 24 fps, 158 frames (6.583 seconds) and an AAC audio track.
The result showed a different wider viewpoint with four people and one dog,
with synthesized facial/scene details. Probe and strip unwanted generated audio;
preserve the original recorded sound. This is a single transport/generation
proof, not a general likeness or synchronized-camera quality guarantee.

**The user rejected the pilot's generation-first workflow.** Selecting an
insert range after generating a generic new view is not acceptance of the
cut-first process above. The first A/B/A assembly remains a technical draft.
The user subsequently authorized reusing two seconds of that generated sample.
Those two seconds were placed as a connected video-only clip over the full
original at 9.8–11.8 seconds in a 60 fps project. The original AV clip stayed
continuous; generated audio was removed and the selected 24 fps range was
conformed to 120 frames at 60 fps without changing its duration.

Final Cut 12.3 imported and exported this separate version. The full render
retained 2158 frames and 35.966667 seconds; a per-frame comparison verified the
120-frame insert at the planned range and the original picture elsewhere.
Source/render audio had equal decoded sample counts and zero-lag correlation
0.99908 after the native encode. This proves the authorized reuse/placement,
not a newly generated frame-synchronous parallel-camera performance. A new
cut-first generation case must still pass its planned action/boundary checks.

The tested placement reused `generate` → `import_edl_json` and `edit` →
`add_connected_clip`. The latter connects an existing library asset to a
specified parent clip, lane, offset and duration. Preserve the full original
AV clip as the audio owner when an overlay is sufficient; there is no need to
cut and reassemble its soundtrack. Inspect the actual imported offset/duration
and native render rather than trusting XML metadata or a tool success message.
Do not lower the identity/scene checks or automatically cycle through providers
after a refusal; distinguish permitted alternative capabilities from retries
that attempt to hide an input restriction. Reuse the existing asynchronous job
and progress path so the live conversation need not wait for rendering.

## Existing references

- https://github.com/Pika-Labs/Pika-Plugins/tree/main/skills/vfx
- https://academy.runwayml.com/tutorial/generate-new-angles-with-aleph
- https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5
- https://ai.google.dev/gemini-api/docs/veo
- https://github.com/OpenRouterTeam/skills/tree/main/skills/openrouter-video
- https://openrouter.ai/blog/insights/seedance-2-5-review/
- https://openrouter.ai/api/v1/videos/models
- https://www.minimax.io/blog/minimax-h3
- https://platform.minimax.io/docs/api-reference/video-generation-v2-create
- https://openrouter.ai/minimax/hailuo-3

These are candidates and source documentation, not installed EVE dependencies
or a measured quality guarantee.
