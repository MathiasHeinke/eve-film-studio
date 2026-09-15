# Acceptance before shipping

The supplied runner checks the real MCP protocol and XML edit engine against a
synthetic project. It does not open Final Cut, transcribe actual speech, connect
cloud EVE to the Mac, or call a video model. Inspect each reported check, not
only whether the MCP answered.

Run `scripts/verify_mcp.py --output <new-empty-run-path>` through the isolated
Python environment containing the pinned dependency set. It creates its own
color test video, supplied synthetic word timestamps and FCPXML; no real project
is read. It invokes discovery, timeline inspection and passage removal through
stdio MCP, then verifies exact source intervals, original hashes and a rejected
out-of-root read. Outputs are retained, never cleaned automatically.

## Observed result, 14 September 2026

The default guide passed six repository authoring checks and one native Hermes
skill-discovery/loading test. This does not prove live language-model selection.

With FCPXML MCP 0.25.0, MCP SDK 2.2.0 and Python 3.14.5, the synthetic 25 fps
case removed the complete supplied phrase at source seconds 2–5. Surviving
source intervals were 0–2 and 5–8, the content was five seconds, original hashes
were unchanged and an out-of-root read was rejected. However, the output XML
still declared eight seconds. The runner deliberately reports
`offline_mcp_findings` and exits 1 for this inconsistency; do not relax the check.

A separate native test imported both unchanged XML files into a fresh library
in Final Cut Pro 12.3 (build 450152), choosing “Keep Both”. Final Cut showed
eight seconds for the original and five seconds for the edit. Its exported
FCPXML 1.14 declared five seconds and preserved both exact source intervals.
Its native video render contained exactly 125 frames at 25 fps: 50 blue frames
followed by 75 green frames, zero red frames and no extra frames. All 125
rendered frames were decoded and classified, not just a thumbnail checked.

This is a successful native synthetic import/export case with an upstream XML
metadata finding, not general product acceptance. The transcript was supplied
and the audio silent. Real speech, multicam, other frame rates, live EVE/voice,
cloud-to-Mac transport and generated inserts remain untested.

## Real-footage pilot, 15 September 2026

One real-person reference clip reached H3 through an authorized private HTTPS
URL after Seedance rejected that input. H3 completed one generation for USD 0.78.
Its output had 158 frames at 24 fps and audio despite a six-second/no-audio
request. The user corrected the editorial method to cut-first, then separately
authorized reusing two seconds from the existing generation.

That reuse was verified in Final Cut 12.3: a video-only overlay at source/timeline
9.8–11.8 seconds, 120 frames at 60 fps, over an uninterrupted original AV clip.
Native export preserved 2158 frames (35.966667 seconds); a downscaled per-frame
comparison matched the expected original/insert picture sequence. Decoded audio
sample counts were equal with zero-lag correlation 0.99908. The earlier statement
that no generated insert had been tested is superseded for this narrow case.

This does not accept cut-first generation, exact likeness, synchronized new
camera performance, actual multicam, managed customer upload/billing, or EVE
voice/cloud execution. Those remain product cases below. Do not use the cost or
success of this one generation as a general provider guarantee.

The user subsequently accepted the completed H3/test-edit result, specifically
praising faces, clothing, poses and the environment. Record that as the human
visual acceptance of this pilot. It does not certify an unrun singing/aerial
case or authorize a product release. The user's additional requirement is to
select the meaningful scene first and choose a motivated camera treatment;
see `camera-direction.md`.

## Product cases still required

1. New account and upgraded existing EVE profile both discover the shipped skill
   from “EVE, lass uns Videos schneiden”, without a slash command or manual skill
   installation. Test in the actual cloud/local agent, not only the desktop UI.
   With a creative brief, the agent proactively identifies relevant moments
   and proposes/chooses specific camera or B-roll treatments from the catalog.
   The user must not need to name the technique or ask the agent to research it.
   A mechanical-only brief should remain within that narrower scope.
2. Existing editor setup is reused. Missing MCP, missing FCP and wrong host lead
   to the correct guided setup; no false ready status or cloud/local path mix-up.
3. Real transcript passage is removed without clipping remaining words; original
   media and project remain recoverable. Check the full resulting audio/video.
4. Repeat the edit with the project's fractional frame rate, retiming, nested
   clips and linked audio before claiming those cases are supported.
5. Real multicam edit keeps master audio and synchronizes selected camera angles.
6. One authorized generated insert passes full-clip visual checks and is placed
   at the intended timeline range without replacing original audio accidentally.
   The source/timeline slot, frame count, shot purpose and output-to-slot mapping
   must be fixed before generation. A camera replacement must match the same
   timed action; a generic new pose in the same setting fails. When a provider
   minimum is longer than the slot, verify the preplanned subrange and handles.
   Preserve both edit boundaries and the original timeline/audio duration.
   If the user specifies a singing scene or drone treatment, locate the actual
   singing and verify the chosen shot's narrative purpose, viewpoint and musical
   timing; selecting an unrelated attractive frame fails this case.
7. EVE remains conversational during a long job. Speech interruption, task stop,
   hangup and a correction each affect the intended operation only.
8. Final Cut opens the returned edit without missing media; a human watches the
   complete preview before the feature is described as release-ready.
9. Module selection respects the brief: test text/pause cuts with real speech,
   color matching, audio finishing and captions only through the connected
   module being claimed. For a singing scene preserve musical rests and timing.
   Verify rendering at cut boundaries; do not infer finishing capability merely
   from `editing-toolbox.md` being present.

For immediate app import use the selected provider's normal preview/review
contract. Do not set an unreviewed-override flag merely to make a test pass.
