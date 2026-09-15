---
name: video-editing
description: Edit footage with the available video editor.
version: 0.1.2
author: Mathias Heinke (FYN Labs)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: creative
    tags: [video, videoschnitt, final-cut, fcpxml, transcript, multicam]
    related_skills: []
---

# Video Editing Skill

Help the user edit real footage in their available editor, including whole
spoken passages, camera choices, B-roll, color, audio and generated inserts. Discover the environment
first; reuse connected tools and Hermes tasks rather than assuming Final Cut.

## When to Use

- “EVE, lass uns Videos schneiden”, “schneide das Interview” or equivalent.
- Final Cut, DaVinci Resolve, CapCut, transcript edits or creative cutaways.
- Continue a previous edit or explain how to prepare the editing environment.

## Prerequisites

- A selected project or footage folder and permission to use it.
- An installed editor or an existing project format that available tools support.
  Respect the user’s choice; use detected software rather than requiring a switch.
- For the prepared Final Cut branch, the `fcpxml` MCP server handles structured
  timeline work; see `references/setup.md`. Native FCP preview/import needs a Mac.
- The Hermes agent can run elsewhere, but tools and media must resolve to the
  intended editing computer.
- A separate configured video-generation tool only when requested. Read
  `references/generated-inserts.md` for this branch.

## How to Run

On a natural-language editing request, start the workflow. Do not require the
user to know a slash command, skill name, MCP or provider name.

Use `references/editing-toolbox.md` to select relevant modules: transcript and
pause editing, B-roll, color, audio, captions, framing and delivery. The package
offers these capabilities; it does not apply them all automatically. Respect
the user's chosen scope and preferences, and expose actual tool readiness.

For creative editing, automatically load `references/camera-direction.md`
during the first editorial pass. Inspect picture and sound for moments worth
emphasizing, choose relevant treatments and turn them into concrete timed cut
ideas. The user should not have to request a drone shot, name a camera technique
or ask EVE to research possibilities. Execute within the current brief, product
permissions and budget; a strictly mechanical edit does not require extra effects.

First use `tool_search` to discover the connected editor's current tools. Use
`search_files` and `read_file` within the selected workspace for the project,
media and any prior edit notes. Do not silently choose another computer.

Match the requested/project editor to available capabilities first. For Resolve,
use its connected MCP/scripting interface when present. For CapCut or another
editor, discover the actual supported integration or use permitted UI control;
do not guess undocumented project-file mutations. Load an existing specialized
skill when helpful. New software is a setup choice, not an automatic requirement.

If the project is clear and tools are ready, inspect it and begin the authorized
work. Otherwise ask only for the missing choice: for example, “Welche Aufnahme
möchten Sie bearbeiten?” Prepare available setup steps rather than handing the
user a generic installation checklist. Reuse existing permissions and accounts.

## Quick Reference

The prepared Final Cut branch uses grouped tools in FCPXML MCP 0.25.0. A
synthetic passage-removal/import/export case was verified in Final Cut 12.3;
that is not acceptance of arbitrary projects. Discover schemas before calling
tools; prefixes may differ by MCP registration.

| Need | Tool group and action |
|---|---|
| Inspect clips | `fcpxml` → `inspect`, `action: list_clips` |
| Remove a spoken passage | `fcpxml` → `transcript`, `action: edit_by_transcript` |
| Construct a selects reel | `fcpxml` → `generate`; choose an available action |
| Preview or import | `fcpxml` → `preview` / `deliver`; respect their review checks |

Action arguments belong under `args`. A successful tool response is not proof
that the intended clip, timing or visual result is correct.

## Procedure

1. **Establish the target.** Identify project, media locations, frame rate,
   selected clips and edit intent. Distinguish the editing computer from the
   cloud runtime. Prefer the installed/requested editor. Explain the Mac
   requirement only when Final Cut is actually the chosen target.
2. **Reuse prior work.** Read existing transcript, markers, shot index and edit
   notes before recomputing them. If transcribing is needed, prefer the already
   configured local path; cloud analysis is a separate data transfer.
3. **Choose the cut before generating anything.** Inspect the footage and audio
   to find the meaningful moment, especially one the user highlighted, such as
   a singing passage. Do not substitute a convenient still or a technical flaw
   for the scene the user wants to emphasize. For camera/shot decisions load
   `references/camera-direction.md`. Decide whether the slot needs another view of the same
   timed action or illustrative B-roll. Bind source and timeline in/out points,
   frame rate, required frame count and incoming/outgoing action to the existing
   markers or edit notes. Only then select the corresponding reference interval
   and request the footage required for that slot. Follow
   `references/generated-inserts.md`; never generate an attractive clip first
   and search for somewhere to put it afterward. For transcript edits, bind the
   whole passage to its exact source range; repeated phrases may match twice.
4. **Create a recoverable version.** Use the editor's existing version/undo or
   new-output mechanism. Preserve originals and master audio. For multicam,
   verify synchronization and the mapping between speakers, audio and angles.
5. **Execute the planned edit.** Insert the selected source/output range at the
   planned timeline interval, keeping the original audio and timeline duration
   unless the user requested otherwise. A camera replacement must match the
   same action at the same time; scene resemblance alone is insufficient.
   Prefer structured MCP operations. Use
   `computer_use` only for uncovered interface actions and visible verification.
   “Hier schneiden” needs a resolved playhead/timecode, not a later guessed frame.
6. **Keep the conversation available.** Use existing Hermes background-work and
   progress facilities for long analysis or rendering. A speech interruption is
   not a request to cancel the edit. Report actual task state and preserve the
   target of corrections.
7. **Check and deliver.** Inspect the changed ranges and full preview; import
   into the intended editor/project when authorized. Return the editable
   result, media references and a concise account of the changes.
8. **Reuse a proven procedure.** Record a useful project-specific edit convention
   through existing Hermes memory/skill tools when appropriate. Do not create a
   new “learning” store or promise that a model has trained itself.

## Pitfalls

- A Mac path in a Linux MCP configuration does not connect the user's Mac.
- The older `FCP_PROJECTS_DIR` setting limits listing, not all file reads. Use
  `FCP_PROJECTS_DIRS` for the intended roots; keep output and journal scoped too.
- Final Cut's accessibility tree can be sparse. Repeated coordinate guessing is
  not a substitute for a known editing command and a fresh observation.
- SpliceKit uses a modified Final Cut copy; XML tooling does not require that
  mechanism. Do not install or patch one merely because the other is absent.
- Preserve fractional frame rates, retiming, linked audio and compound/multicam
  structure. The accompanying offline proof is not an FCP-version certification.
- FCPXML MCP 0.25.0 leaves stale sequence-duration metadata after the tested
  passage removal. Final Cut 12.3 recalculated it correctly on import, including
  the native video export. Check the actual target editor and duration; do not
  silently accept the stale value in other consumers or patch complex XML blindly.
- Do not bypass a provider's preview/review gate to obtain a success message.
- Phone footage may be HDR, rotated and variable-frame-rate. If XML import
  rejects its frame rate, use the editor's native media import/conform for a
  separate working copy rather than repeatedly guessing replacement metadata.
  Inspect the derivative's color space, orientation and timing before sending
  it as a generation reference.

## Verification

- Correct project, source clip and requested passage changed; originals remain.
- Timing is on the project's frame grid, audio stays synchronized and remaining
  words are intact. Check the actual output, not only the tool's summary.
- For generated footage, check the whole inserted shot and retain its source
  and provider provenance. Verify placement and duration against the cut plan
  made before generation, plus action/sound continuity at both cut boundaries.
- The selected editor opens the result without missing media before delivery.
- An unavailable tool, offline simulation or pending render is stated as such.

Maintainer checks and the harmless MCP fixture runner:
`references/acceptance.md`, `scripts/verify_mcp.py`.
