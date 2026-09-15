# Grok Media Routing

Treat the installed Grok Build version and current subscription auth as runtime
facts that can change. Verify before production.

Verified on 2026-07-17 with official `grok 0.2.103`: grok.com OAuth exposed
`image_gen`, `image_edit`, `image_to_video`, and `reference_to_video` without an
`XAI_API_KEY`. Re-check after CLI updates.

## Preflight

1. Record `grok --version` and `grok models`.
2. Confirm OAuth/login state without printing credentials.
3. Inspect the current tool registry or run one bounded media smoke.
4. Require a real local file, non-zero duration, decodable video stream, and a
   provenance record before declaring the route available.
5. Do not buy xAI API credits or add an API key merely because subscription
   generation is unavailable.

## Native Tool Preference

When exposed by the authenticated Grok Build lane, prefer:

1. `image_gen` for a clean character or scene anchor.
2. `reference_to_video` when identity, wardrobe, product, or composition must
   recur across shots.
3. `image_to_video` for one-shot motion from an approved still.

The verified headless allowlist includes the loader itself:

```bash
env -u XAI_API_KEY grok \
  --prompt-file /absolute/path/to/shot.md \
  --tools Skill,image_gen,image_to_video,reference_to_video \
  --permission-mode dontAsk \
  --no-subagents --disable-web-search --no-memory \
  --max-turns 12 --output-format json
```

Current verified limits: `image_to_video` accepts one opening-frame source,
6/10 seconds and 480p/720p; `reference_to_video` accepts 2-7 references,
6/10 seconds, 480p/720p and common landscape/portrait aspect ratios.

Ask Grok to save outputs under the declared work folder and return only the
absolute media paths plus a short receipt. Keep prompts free of exact copy and
third-party logos. Validate each clip with `ffprobe` before using it.

## Failure Modes

- Tool absent: use real footage, existing brand media, or still-plus-motion.
- OAuth blocked: stop the Grok lane; do not switch to paid API silently.
- Quota/rate limit: preserve completed clips and render a coherent fallback.
- Identity drift: reuse one arc clip in separate before/after timeline beats or
  use stable non-face continuity cues.
- Low resolution: upscale once during normalization; do not repeatedly encode.
- Garbled text: crop or cover it and add deterministic overlays.
- Native xAI provenance/watermark: preserve it. Do not remove, alter, crop out,
  or obscure it in the edit.
