# Follow-up: source audio and exact cuts

This repair follows the system assessment at `5b06fc6`. It changes the existing
`normalize_scene → join_scenes → add_audio` owner, not the film's story or the
Command EVE product runtime. Earlier assessment results remain historical evidence.

## Changes

- Reject invalid or beyond-video source spans; container audio length cannot
  conceal a shorter video stream. Frame rounding is explicit.
- `source_audio: "keep"` carries the selected first source audio stream through
  the same picture cuts/fades. Default `mute` prevents unintended source sound.
- `transition: "cut"` and zero transition duration are exact cuts. Intentional
  positive fades remain available.
- Apply voice gain consistently, sum tracks without implicit normalization,
  and compensate limiter delay. Silent added tracks no longer alter another gain.
- Keep complete static-image and push durations.

Schema and migration notes are in
[the timeline manifest](../../skills/produce-brand-film/references/timeline-manifest.md).
Existing mixed manifests can become about6dB louder before limiting, and the old
standalone music default changes from0.58to0.42. Re-measure real master loudness.
For dialogue, select source-frame-aligned starts; arbitrary fractional starts
can produce up to one source frame of picture/audio quantization difference.

## Evidence

A worker implemented the change; a separate Fable5.1 reviewer read the frozen
diff, ran the CLI suite and added independent local probes. It found no code
blocker and requested the migration/timing clarifications above.

`python3 tests/test_assemble_film_cli.py` exercised10tests and32CLI invocations.
The retained final run passed all assertions in11.188s with FFmpeg8.1.1.
Known pulse positions measure absolute timing, not correlation alone.

- Silent voice gain: RMS0 in both paths.
- Silent added voice/music: other-track RMS ratio1.0.
- Exact cuts:72frames/3s. Mixed cut/fade and fade/cut:66frames/2.75s.
- Source audio marker deviation: at most3.43ms in the synthetic test.
- Source+score+voice amplitudes:0.119967/0.049922/0.039964 against0.12/0.05/0.04.
- A real32kHz AAC video source additionally passed a4s, frame-aligned keep
  roundtrip: measured audio lag0samples and correlation0.999970. This checks
  the transport of source audio, not whether generated lips match that audio.

Pre-edit symbol impacts were LOW. Final GitNexus diff mapping reported HIGH
across8local renderer/CLI flows; its old line mapping also included unchanged
font functions. An AST comparison restricted actual source changes to4existing
functions plus3small validation/probe helpers. Overlay and still/push paths were
exercised. This remains a central render-path change, not a blanket safety claim.

Remaining limits: only the first source audio stream; no proven old-FFmpeg minimum
version; packet-duration fallback can reject metadata-poor sources; native source
lip sync, film quality, audience understanding, loudness and actual editor delivery
require their own checks. The repair does not increase the assessment's film score
without a new completed, reviewed film.
