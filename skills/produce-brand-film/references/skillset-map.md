# Film and motion skillset

Start at `produce-brand-film` for a new brand/product film or a substantial
creative revision. Keep its existing story, provenance and review owners.
For a footage-only edit, go directly to the relevant editing skill. This map
selects capabilities; it does not install runtimes or require loading every skill.

## Existing capabilities

| Work | Existing skill or module | Use it when |
| --- | --- | --- |
| Film direction, story, production and delivery | `produce-brand-film`; [film craft](film-craft.md) and [storyboard](storyboard-contract.md) | The deliverable is a complete film or a substantial creative revision. |
| Story logic, character continuity, cold comprehension and review | [continuity and review](continuity-and-review.md), [review gates](review-gates.md), [Gemini audiovisual review](gemini-video-review.md) | A rendered sequence needs examination; declare actual image/motion/audio perception. |
| Code-rendered motion and repeatable production | [motion studio](motion-studio.md) | Build or revise deterministic UI, type, diagram, data, brand motion or a hybrid film. |
| Character design and visual development | [character look development](character-lookdev.md) | Recurring people/mascots need a convincing design or a rejected look needs revision. |
| Narrator and voice production | [narration production](narration-production.md), [sound craft](film-craft.md#one-soundtrack-owner) | Spoken material is part of the brief; a soundtrack alone does not fulfil it. |
| Raster concepts, character references, textures and image edits | `imagegen` | Generate bitmap assets; use its built-in path by default and respect an explicitly chosen provider route. |
| HTML compositions | `hyperframes-core` | HyperFrames is the selected runtime; load its composition and determinism contract before authoring. |
| Choreography and runtime adapters | `hyperframes-animation` | Design movement in HyperFrames or use its supported animation adapter. |
| HyperFrames snapshots, checks, previews and exports | `hyperframes-cli` | Operate that runtime; read only the reference for the command being used. |
| React-based video | `remotion-best-practices` | Remotion is selected or an existing Remotion project should be continued. |
| Editable local motion scenes and overlays | `tesseract:tesseract-motion` | Build native Tesseract motion; verify its supported schema and runtime. |
| Local footage editing in Tesseract | `tesseract:tesseract-video` | Cut existing footage, preserve dialogue and mix sound in that editor. |
| Static editable designs/posters | `tesseract:tesseract-design` | The requested output is a still design, not a full moving film. |
| Existing editor, Final Cut and generated inserts | [video-editing](../../video-editing/SKILL.md) | Work in the user's existing editor and project; discover the connected tools. |
| Explicit local/offline image or video generation | `lokal-bild`, `lokal-video` | The user asks for that local route; check model, hardware and tool readiness. |

The names above are discoverable skills in the inspected environment. Check
the current host's skill catalog and the selected executable/tool before use;
an installed skill file is not proof that its runtime, account or media model
is available. Keep vendor skills at their own maintained owners.

Before writing Tesseract timing, inspect the installed schema and the actual
project: some inspected 0.3.1 references disagree about placement through `activeRange`
versus `playback.inputRange` and its mapping. This concerns placement, not an
instruction to remove the source range. Do not choose a field from conflicting
examples by guess; verify the native contract and a small playback join. This map
records that unresolved vendor-doc issue rather than inventing a replacement schema.
The film workflow's restriction on procedural fallback music does not prohibit
appropriate short effects inside an agreed sound direction; listening remains required.

An explicitly selected image provider needs its own verified, exposed route.
The `imagegen` fallback CLI is not a generic client for every media provider.

## Compose the smallest useful route

- Small UI/type film: film brief and exact assets → one existing code runtime
  → motion/frame checks → sound if requested → delivery.
- Character/story film: story → character/style studies → a connected moving
  passage → footage/generated shots or a proven code style → exact brand/UI
  overlays → edit and sound → review.
- Existing interview: editing skill → source-aware picture/dialogue edit →
  review. Add a motion or image skill only for an actual insert/overlay need.

Choose code, footage, generated media or a mixture for the required result.
The user's selected model, editor and creative freedom remain in force. Quality
milestones are internal checks, not automatic requests for user confirmation
before every scene. A new paid route, external action or publication still
needs its separately applicable authorization.

## Ownership and reuse

Keep the film's decisions in its existing production folder: brief, style guide
when useful, storyboard/shot plan, source timeline, approved assets, review
records and exports. Reuse `production/storyboard.md` for story and review;
do not introduce a parallel shot-list or approval ledger solely for this map.
Keep editable source at the current renderer's owner. Store source/media
provenance, selected font/brand assets and requested-format contact sheets.

The method incorporates the read article
[Motion Engineering: Build a Video Studio Around Opus 5.5](https://x.com/0xwhrrari/article/2105643919119696297)
(2026-10-01; inspected 2026-10-05). Its examples are method references, not
permission, model benchmarks or a requirement to use Opus or a particular renderer.
