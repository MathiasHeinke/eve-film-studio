# EVE Film Studio

Agent skills for developing a film from a human observation through story, direction, generated footage, editing and a reviewable master.

The workflow treats story quality, visual continuity, product truth and technical validation as separate questions. It supports cinematic interaction graphics and a prepared Final Cut Pro / FCPXML editing branch.

## Included skills

| Skill | Use it for |
|---|---|
| [produce-brand-film](skills/produce-brand-film/SKILL.md) | A complete 20–90 second brand, product or advertising film: ideation, story, critical review, script, scenes, typography, sound and delivery. |
| [video-editing](skills/video-editing/SKILL.md) | Existing-footage edits, transcript cuts, alternate angles, generated inserts and native editor handoff. |

The skills contain instructions, focused references and local Python helpers. They do not install an editor, grant provider access or create an autonomous production service.

## The production method

The workflow moves from human observations and competing story ideas to a
critically revised story, storyboard, reference images, generated takes and
assembled film. It keeps story assumptions and review decisions in the
existing storyboard. The operational rules live in
[continuity and review decisions](skills/produce-brand-film/references/continuity-and-review.md).

That method defines independent review, available perception, a neutral-input
comprehension pass and when production needs revision or remains unreviewed.

[Gemini audiovisual review](skills/produce-brand-film/references/gemini-video-review.md)
adds a tested OpenRouter request recipe, neutral first-pass prompt, targeted
excerpt checks, cost evidence and a critical handoff to the selected creative
reviewer. It processes the actual film with sound; precise sync and conflicting
observations still require checking against the material.

## Graphics follow their role

A floating composer can reveal what a person is typing. An assistant message can show a reply. Attachments and status elements can show a completed result. Lower thirds can provide context; free typography can carry a campaign statement.

Choose the form for the moment. Exact compositing and verified generated lettering are both supported approaches. See [cinematic graphics](skills/produce-brand-film/references/cinematic-graphics.md) and [continuity and staged review](skills/produce-brand-film/references/continuity-and-review.md).

## Install or use

Clone the repository:

```sh
git clone https://github.com/MathiasHeinke/eve-film-studio.git
```

Load the relevant `SKILL.md` in an agent that supports filesystem skills. For discovery in Codex, install both folders from this repository with its built-in skill installer:

```text
Install both skills from MathiasHeinke/eve-film-studio:
- skills/produce-brand-film
- skills/video-editing
```

Keep both skill folders side by side so their relative references resolve. Inspect and preserve any existing local versions when installing. For other hosts, use their supported skill-loading mechanism.

Example brief:

> Develop a 40 second film for this product. Start with three human observations and competing story premises. Critically revise the chosen story before planning scenes. Use our supplied brand assets and a maximum generation budget of $20. Deliver a local master and editable project; do not publish it.

## Tools and prerequisites

- Local assembly/validation helpers use Python 3, FFmpeg and ffprobe.
- SVG typography uses `rsvg-convert` and Fontconfig tools.
- Media generation needs a separately available, authorised provider. Discover current input support, pricing and limits before a run.
- The Final Cut branch needs macOS, Final Cut Pro and the separate [FCPXML MCP server](https://github.com/DareDev256/fcp-mcp-server). Setup and a tested dependency snapshot are in the [editing setup reference](skills/video-editing/references/setup.md).
- Inspect which viewing/listening capabilities your agent actually has. Frames, ASR and playback completion are useful evidence but are not a substitute for a full audiovisual review.

## Local helpers

```sh
python3 skills/produce-brand-film/scripts/assemble_film.py --help
python3 skills/produce-brand-film/scripts/validate_film.py --help
python3 skills/produce-brand-film/scripts/generate_score.py --help
```

Use the [timeline manifest guide](skills/produce-brand-film/references/timeline-manifest.md) before assembly. The existing-footage skill includes a synthetic FCPXML verification helper; use its [acceptance guide](skills/video-editing/references/acceptance.md) before running it.

## Status and boundaries

This is an evolving production method. It was refined against observed story, continuity, graphic and audio-review failures. It does not promise a numerical quality score, universal model reliability or an untested editor integration.

Host permissions and the user's budget still govern spending, uploads and publication. Staged product examples must not be presented as measured real execution.

Film assets, voices, music, customer material, credentials and local production reports are not included. [manifest.json](manifest.json) records the distributed skill files with relative paths and SHA256 hashes.

## License

MIT. See [LICENSE](LICENSE) and [THIRD_PARTY.md](THIRD_PARTY.md). Dependencies and referenced services retain their own licenses and terms.
