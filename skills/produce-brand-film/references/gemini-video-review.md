# Gemini audiovisual review

Use Gemini to inspect an actual film with its soundtrack at low cost. This is
the perception branch of the [staged review method](continuity-and-review.md),
not a separate production system or an automatic quality approval.

## Route and cost

The tested route is OpenRouter → `google/gemini-3.1-pro-preview` → standard
Google Vertex. Recheck the current model's audio/video input modalities,
endpoint, prices, limits and request syntax before use. An available model or
credential does not grant spending or upload permission. Use the task's existing
authorization and remaining budget; do not request approval again for the same
authorized package or reuse a past package's allowance for a new one.

One measured 40-second film plus two detail excerpts cost **USD 0.182638** in
three requests on 2026-09-15. This is an example, not a fixed price or quality
benchmark. At that run the standard rates below 200k input tokens were USD 2/M
input and USD 12/M output including thinking; the higher tier was USD 4/M and
USD 18/M. Estimate uncached input plus output/thinking and reserve headroom for
each request before sending. Count retries too. An uncertain request retains
its reservation until actual cost is known; never retry it blindly. A local
budget estimate is not a provider-enforced account spending limit.

Use a currently available native API client. Supply the approved video as a
base64 data URL; a public upload is unnecessary. The tested Chat Completions
request shape was:

```json
{
  "model": "google/gemini-3.1-pro-preview",
  "provider": {
    "only": ["google-vertex/global"],
    "allow_fallbacks": false,
    "max_price": {"prompt": 4, "completion": 18}
  },
  "messages": [{"role": "user", "content": [
    {"type": "video_url", "video_url": {"url": "data:video/mp4;base64,<video bytes>"}},
    {"type": "text", "text": "<neutral review brief below>"}
  ]}],
  "max_tokens": 12000,
  "reasoning": {"effort": "high", "exclude": true},
  "stream": true
}
```

Send to `https://openrouter.ai/api/v1/chat/completions`; keep credentials in the
host's normal credential mechanism, out of prompts, files and reports.
`max_price` limits token rates, not total cost. Adapt the example's output limit
and reservation to the approved budget. Do not switch provider/model or priority
tier silently. Keep streaming output observable and save the completed answer;
an error, truncated response or absent completion is not a completed review.
Read usage from the final stream event; current OpenRouter responses include it
automatically. The tested run's older `include_usage` flag is now unnecessary.

## Neutral first pass

Send only the exact neutral-named film and a short brief such as:

> Review this film independently using its actual picture and sound. First:
> what happened, who initiated the change, what changed for the people, and
> what remains unclear? Then quote the audible dialogue with approximate times
> and speaker attribution; describe music, sound and the interaction of acting,
> pauses, cuts and graphics. List the strongest moments and at most five useful
> improvements. Separate observation, interpretation and uncertainty. Do not
> invent offscreen history, demand pictures for every anecdote, or assume every
> cut must land on a beat. For each suspected sync issue distinguish the audible
> voice, person visible, whether that person's mouth is visible, and what happens
> in the next shot. If there is no audible soundtrack, say so instead of
> inventing sound. Declare perception limits and end with REVIEW_COMPLETE.

Use the film's language. Do not supply the script, previous verdicts, intended
interpretation or a transcript in this first pass. Freeze its verbatim response
before comparing it with story essentials or author feedback.
For intentionally silent work, state that context and review its visual intent;
distinguish an absent soundtrack from audio that the provider failed to process.

## Detail checks and critical handoff

Select short excerpts only for a concrete unresolved question. Retain original
speed and sound, record original in/out times, and require original timecodes
in the reply. These are focused checks, not extra blind votes on the whole film.
Use neutral excerpt names too; put the question in the prompt, not the filename.
For example: "Who is visible and audible before and after this cut? Does visible
speaking continue after the spoken line has ended?" Use exact adjacent frames
and a qualified viewer for details beyond the model's temporal sampling.

Review the whole phrase and adjoining shots together. A line heard offscreen
may be a valid sound bridge while the subsequent silent mouth movements still
reveal a real offset. A mistaken model timecode does not by itself disprove the
underlying defect. Preserve a user's direct observation and correct the narrow
finding rather than discarding it wholesale.

Give the original answers, selected media evidence and limitations to the
independent creative reviewer selected for the task (for example Fable). The
reviewer must distinguish Gemini's observations from their own perception,
check conflicts against the material, and revise prior conclusions when needed.
Contradictory voice/music descriptions remain unresolved until checked; model
agreement alone is not proof. No rule requires adopting every proposed repair.

## Evidence and limits

Before sending each file, probe its streams, for example:
`ffprobe -v error -show_entries stream=codec_type -of json review.mp4`.
If an expected soundtrack disappeared while preparing an excerpt, repair that
excerpt before review. For the tested route, a sound-bearing input should yield
positive `audio_tokens`. Missing or zero audio usage leaves sound checks
`not reviewed` until ingestion is verified; omitted usage is unknown, not zero.
An intentionally silent film needs no dialogue, and a silent encoded audio
stream can still consume audio tokens. Neither case permits invented sound.

Link the following from the existing storyboard's Review records:

- Exact master/excerpt hash and source time range; request prompt and timestamp.
- Requested and returned model/provider; preserved answer and completion state.
- Usage, audio/video token details when supplied, and actual cost. Verify the
  generation receipt via `GET /api/v1/generation?id=<id>`; retain estimates as
  estimates if billing or modality details are unavailable.
- Findings with original times, evidence owner, unresolved conflicts, user
  corrections and the creative reviewer's disposition.

Audio/video tokens establish ingestion, not correct hearing or every-frame
perception. Default video sampling can miss mouth phases and quick cuts; higher
sampling must be supported and actually delivered by the selected route, not
merely requested in prose. Do not certify exact lip sync, cut timing, instrument
identity or small text when the evidence cannot establish them. Keep technical
validation, creative judgment and publication authority separate.

## Current documentation

- [OpenRouter video input and provider differences](https://openrouter.ai/docs/guides/overview/multimodal/videos)
- [Model and pricing](https://openrouter.ai/google/gemini-3.1-pro-preview)
- [Google video processing and temporal sampling](https://ai.google.dev/gemini-api/docs/video-understanding)
- [OpenRouter usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting)
