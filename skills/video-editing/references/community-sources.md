# Focused community sources

Checked 15 September 2026 by reading original source and GitHub metadata.
These are targeted reuse candidates, not installed dependencies or runtime
certifications. Recheck the relevant source/version before adopting executable
code. Preserve EVE's existing agent, permissions, media and billing owners.

## DirectorSKILL — film direction reference

- Source: https://github.com/wuwangzhang1216/DirectorSKILL
- Reviewed commit: `c65ae0d14457053efb1e354c7e7f7e120d97fad1`; MIT; 91 stars at inspection.
- Relevant files: `SKILL.md`, `references/cinematic-language.md`,
  `references/production-workflow.md`.
- Useful for motivated shot selection, staging, continuity and shot-plan structure.
  It also routes to sound, color and editing references for later focused review.
- Prefer selected references when the short EVE camera catalog is insufficient.
  Its full production workflow is heavier than a two-second insert. Do not
  import every style module, its defaults or mandatory planning phases blindly.
  Small adoption footprint: source-reviewed candidate, not broadly proven here.

## browser-use/video-use — editing decisions and helpers

- Source: https://github.com/browser-use/video-use
- Reviewed commit: `9575612f066aa517354790a645fd90f9f95a743b`; MIT; 24,881 stars.
- The skills.sh listing showed 3.7K installs; that count is not tied to this commit.
- Relevant source: `SKILL.md`; it names transcript, EDL, timeline-view and render helpers.
- Strong fit for time-aligned speech cuts and inspecting audio/picture around
  edit boundaries. It also covers grading, captions and overlays.
- Our tested FCPXML MCP already exposes `generate` → `import_edl_json` for this
  EDL shape. Reuse that connection for editable Final Cut delivery.
- Review individual helpers before reuse; they were not installed/executed in
  this research. Do not force ElevenLabs, an extra renderer, mandatory per-cut
  approvals or fixed fade/grade/caption defaults into an otherwise working EVE
  path. Use the configured transcription/editor route where sufficient.

## Generative-Media-Skills — secondary prompt vocabulary

- Source: https://github.com/SamurAIGPT/Generative-Media-Skills
- Reviewed commit: `5519622e885abc60217a65c8e090bcb1d9830746`; MIT; 4,272 stars.
- Reviewed file: `library/motion/cinema-director/SKILL.md`.
- Has a compact intent-to-framing/movement table. Its execution path is tied
  to muapi.ai, and its model-preference claims need independent current checks.
  Consider vocabulary selectively; it is not a reason to add another provider
  or duplicate the already working OpenRouter job path.

## cinematic-ui — the user's example, different domain

- Source: https://github.com/akseolabs-seo/cinematic-ui
- Reviewed commit: `24a66c1d6140c21ec0d0e4d9ef663a97264003de`.
- The skill translates film references into website layout and motion. It is
  not a footage-editing or camera-control skill. Its research-first idea is
  relevant; do not load its website questionnaire, HTML/CSS output or host
  configuration as the video's workflow.

Popularity informs discovery, not correctness. Install counts were not verified
for these exact skill versions. Read only the needed reference, prepare a
bounded use case and retain the actual result/limitations before calling a
newly adopted capability tested.
