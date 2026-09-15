# Timeline Manifest

`assemble_film.py` reads one JSON object. All paths may be absolute or relative
to the process working directory. Use an explicit brand font file whenever text
overlays are present.

## Optional kinetic policy

`text_policy: kinetic_only` is an explicit opt-in restriction on manifest-authored
typography, not the default for filmic graphics. It rejects every non-empty
scene `overlay` field. Validation also requires at least one `kinetic_text`
scene and its render receipts; omitting/nulling the policy skips those kinetic
checks. A scene cannot combine non-empty `overlay` and `kinetic_text` blocks.

A readable settled hold after entrance and before an optional exit is supported;
"kinetic" does not require movement in every frame. There are no composer,
message or result exceptions in this schema, and no native bubble/composer
primitive. The check does not classify writing already present in source media.
Choose functional UI with the existing editor or a verified source/composite,
and check it against the brief separately. Do not use source-baked text to
bypass an explicit creative restriction or claim that the validator saw it.

## Minimal example

```json
{
  "width": 1920,
  "height": 1080,
  "fps": 24,
  "font": "/System/Library/Fonts/SFNS.ttf",
  "body_font": "/System/Library/Fonts/SFNS.ttf",
  "scenes": [
    {
      "source": "/absolute/path/problem.mp4",
      "start": 1.2,
      "duration": 3.5,
      "grade": {
        "contrast": 1.08,
        "brightness": -0.04,
        "saturation": 0.72
      },
      "overlay": {
        "label": "THE PROBLEM",
        "headline": "Work is still stuck.",
        "subline": "Exact copy is rendered outside the video model."
      }
    },
    {
      "source": "/absolute/path/product.png",
      "duration": 4.0,
      "motion": "push",
      "transition": "fade",
      "transition_duration": 0.25,
      "overlay": {
        "layout": "center",
        "headline": "The product changes the system.",
        "headline_size": 64,
        "subline": "Evidence, not a logo-only reveal.",
        "subline_size": 32
      }
    }
  ],
  "audio": {
    "music": "/absolute/path/score.wav",
    "music_volume": 0.35,
    "voice": "/absolute/path/voice.wav",
    "voice_start": 0.25,
    "voice_volume": 1.0
  }
}
```

Run:

```bash
python3 scripts/assemble_film.py \
  --manifest /absolute/path/timeline.json \
  --output /absolute/path/final/film-master.mp4 \
  --work-dir /absolute/path/work/render
```

## Top-level fields

| Field | Required | Default | Meaning |
|---|---|---|---|
| `scenes` | yes | none | Ordered non-empty scene array. |
| `width` | no | `1920` | Output width. |
| `height` | no | `1080` | Output height. |
| `fps` | no | `30` | Constant output frame rate. Prefer 24 or 30. |
| `font` | no | `/System/Library/Fonts/SFNS.ttf` | Exact TTF/OTF display font used for labels and headlines. Must exist when overlays are used. |
| `body_font` | no | same as `font` | Exact TTF/OTF font used for sublines. |
| `audio` | no | silent stereo | Music and/or voice mix definition. |
| `text_policy` | no | none | Set to `kinetic_only` to forbid static overlays and require the kinetic renderer for manifest text. |
| `output` | conditional | none | Used only when `--output` is omitted. |

## Scene fields

| Field | Required | Default | Meaning |
|---|---|---|---|
| `source` | yes | none | Video or image path. Supported images: JPG, PNG, WebP, TIFF. |
| `duration` | yes | none | Positive scene duration in seconds. |
| `start` | video only | `0` | Trim-in point in seconds. |
| `fit` | no | `cover` | `cover`, `contain`, or `contain_blur`. |
| `canvas` | no | `0x0b1220` | Letterbox color used by `contain`. |
| `motion` | images only | static | `push` adds a restrained center zoom. |
| `transition` | no | `fade` | Any transition supported by FFmpeg `xfade`. |
| `transition_duration` | no | `0.28` | Crossfade duration; subtracted from total runtime. Use `0` for an approximately hard cut. |
| `crf` | no | `18` | Normalized scene H.264 quality. |
| `grade` | no | neutral | `contrast`, `brightness`, and `saturation` values for FFmpeg `eq`. |
| `overlay` | no | none | Deterministic text layer described below. |
| `kinetic_text` | no | none | Frame-exact animated typography described below. Cannot be combined with `overlay`. |

## Overlay fields

| Field | Required | Default | Meaning |
|---|---|---|---|
| `layout` | no | `lower` | `lower` panel or `center` scrim. |
| `label` | no | none | Small orange kicker. |
| `headline` | no | none | Primary exact copy. |
| `headline_size` | no | `72` | Headline pixel size. |
| `subline` | no | none | Supporting exact copy. |
| `subline_size` | no | `34` | Subline pixel size. |

The renderer wraps text approximately by character count. Insert explicit line
breaks when brand copy requires exact wrapping, then inspect the contact sheet.
For every overlay scene it also writes `scene-XX-font-receipt.json`; delivery QA
must confirm those receipts resolve to the exact manifest font files.

## Kinetic text fields

Use explicit lines and bounded presets. The renderer intentionally provides no
local panel or lower-third background; an optional `scrim` always covers the
full frame.

```json
{
  "text_policy": "kinetic_only",
  "font": "/absolute/path/display.ttf",
  "body_font": "/absolute/path/body.ttf",
  "scenes": [
    {
      "source": "/absolute/path/new-ui.mp4",
      "duration": 3.2,
      "kinetic_text": {
        "scrim": {"color": "#071018", "opacity": 0.18},
        "tracks": [
          {
            "id": "hook",
            "lines": ["MEHR KI.", "MEHR ARBEIT?"],
            "font_role": "display",
            "font_size": 144,
            "line_height": 0.96,
            "x": 960,
            "y": 430,
            "anchor": "middle",
            "fill": "#fbfcfe",
            "tracking_px": {"from": 14, "to": -1},
            "enter": {
              "preset": "line_mask_rise",
              "start": 0.12,
              "duration": 0.52,
              "stagger": 0.08,
              "distance_px": 44,
              "scale_from": 0.96,
              "ease": "out_cubic"
            },
            "exit": {
              "preset": "fade_rise",
              "start": 2.6,
              "duration": 0.35,
              "ease": "in_cubic"
            }
          }
        ]
      }
    }
  ]
}
```

Every track requires a stable `id`, one or more explicit `lines`, and an
`enter`. Supported enter presets are `word_fade`, `line_mask_rise`,
`line_mask_left`, `block_scale_tracking`, and `fade_rise`. Supported easings
are `linear`, `out_cubic`, `in_cubic`, and `in_out_cubic`. `tracking_px`,
`x`, `y`, `anchor`, `font_size`, `line_height`, `fill`, and `weight` are
optional deterministic style fields. An optional `exit` fades and rises the
track; it never creates a static panel.

For each kinetic scene the renderer writes a transparent QTRLE/ARGB movie,
four or more motion-proof frames, and
`scene-XX-kinetic-receipt.json`. Validate those artifacts with:

```bash
python3 scripts/validate_film.py /absolute/path/film-master.mp4 \
  --manifest /absolute/path/timeline.json \
  --render-dir /absolute/path/work/render \
  --contact-sheet /absolute/path/film-contact-sheet.jpg \
  --json-out /absolute/path/validation.json
```

## Audio fields

| Field | Required | Default | Meaning |
|---|---|---|---|
| `music` | no | none | Loopable music or score file. |
| `music_volume` | no | `0.42` with voice, `0.58` alone | Linear music gain. |
| `voice` | no | none | Voice-over file. |
| `voice_start` | no | `0` | Voice delay in seconds. |
| `voice_volume` | no | `1.0` | Linear voice gain. |

The assembler limits peaks but does not promise a delivery loudness target.
Measure the master and apply loudness normalization appropriate to the channel
before final validation.
