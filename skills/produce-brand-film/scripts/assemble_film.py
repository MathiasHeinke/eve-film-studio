#!/usr/bin/env python3
"""Render a reproducible mixed-media brand film from a compact JSON timeline."""

from __future__ import annotations

import argparse
import html
import json
import os
import shlex
import shutil
import subprocess
import textwrap
from pathlib import Path

from kinetic_type import render_kinetic_scene


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}


def run(command: list[str], env: dict[str, str] | None = None) -> None:
    subprocess.run(command, check=True, env=env)


def scan_font_family(font: Path) -> str:
    result = subprocess.run(
        ["fc-scan", "--format", "%{family[0]}\n", str(font)],
        check=True,
        text=True,
        capture_output=True,
    )
    family = next((line.strip() for line in result.stdout.splitlines() if line.strip()), "")
    if not family:
        raise RuntimeError(f"could not resolve font family from {font}")
    return family


def fontconfig_environment(work: Path, font: Path, body_font: Path) -> tuple[dict[str, str], Path]:
    if not shutil.which("fc-scan") or not shutil.which("fc-match"):
        raise RuntimeError("fc-scan and fc-match are required for exact local typography")
    directories = sorted({font.resolve().parent, body_font.resolve().parent}, key=str)
    cache = work / "fontconfig-cache"
    cache.mkdir(parents=True, exist_ok=True)
    config = work / "brand-fonts.conf"
    dir_entries = "\n".join(f"  <dir>{html.escape(str(path))}</dir>" for path in directories)
    config.write_text(
        "<?xml version=\"1.0\"?>\n"
        "<!DOCTYPE fontconfig SYSTEM \"fonts.dtd\">\n"
        "<fontconfig>\n"
        f"{dir_entries}\n"
        f"  <cachedir>{html.escape(str(cache.resolve()))}</cachedir>\n"
        "</fontconfig>\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["FONTCONFIG_FILE"] = str(config.resolve())
    return env, config


def assert_font_match(env: dict[str, str], family: str, expected: Path) -> Path:
    result = subprocess.run(
        ["fc-match", "--format", "%{file}\n", family],
        check=True,
        text=True,
        capture_output=True,
        env=env,
    )
    resolved = Path(result.stdout.splitlines()[0]).resolve()
    if resolved != expected.resolve():
        raise RuntimeError(f"font mismatch for {family}: expected {expected}, got {resolved}")
    return resolved


def svg_text(
    value: str,
    x: int,
    y: int,
    size: int,
    color: str,
    weight: int,
    max_chars: int,
    font_family: str,
) -> str:
    lines: list[str] = []
    for explicit_line in value.splitlines() or [""]:
        lines.extend(textwrap.wrap(explicit_line, width=max_chars, break_long_words=False) or [""])
    spans = []
    line_height = int(size * 1.18)
    for line_index, line in enumerate(lines):
        dy = 0 if line_index == 0 else line_height
        spans.append(f'<tspan x="{x}" dy="{dy}">{html.escape(line)}</tspan>')
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="{font_family}, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" letter-spacing="-0.7">'
        + "".join(spans)
        + "</text>"
    )


def render_overlay(
    work: Path,
    scene_index: int,
    overlay: dict,
    width: int,
    height: int,
    font: Path,
    body_font: Path,
) -> Path:
    if not shutil.which("rsvg-convert"):
        raise RuntimeError("rsvg-convert is required for deterministic text overlays")
    if not font.is_file():
        raise FileNotFoundError(f"font file not found: {font}")
    if not body_font.is_file():
        raise FileNotFoundError(f"body font file not found: {body_font}")
    display_family = scan_font_family(font)
    body_family = scan_font_family(body_font)
    font_env, fontconfig = fontconfig_environment(work, font, body_font)
    display_resolved = assert_font_match(font_env, display_family, font)
    body_resolved = assert_font_match(font_env, body_family, body_font)
    layout = overlay.get("layout", "lower")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    ]
    if layout == "center":
        parts.append(
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="#0b1220" fill-opacity="0.62"/>'
        )
        x = width // 2
        anchor = ' text-anchor="middle"'
        label_y = 130
        headline_y = height // 2 - 15
        subline_y = height // 2 + 105
        headline_chars = 34
        subline_chars = 55
    else:
        parts.append(
            f'<rect x="70" y="{height - 360}" width="{width - 140}" height="285" rx="28" '
            'fill="#0b1220" fill-opacity="0.78"/>'
        )
        x = 110
        anchor = ""
        label_y = height - 310
        headline_y = height - 235
        subline_y = height - 120
        headline_chars = 40
        subline_chars = 65
    if overlay.get("label"):
        label = svg_text(str(overlay["label"]), x, label_y, 30, "#f97316", 700, 55, display_family)
        if anchor:
            label = label.replace("<text ", f"<text{anchor} ", 1)
        parts.append(label)
    if overlay.get("headline"):
        headline = svg_text(
            str(overlay["headline"]), x, headline_y,
            int(overlay.get("headline_size", 72)), "#ffffff", 700, headline_chars,
            display_family,
        )
        if anchor:
            headline = headline.replace("<text ", f"<text{anchor} ", 1)
        parts.append(headline)
    if overlay.get("subline"):
        subline = svg_text(
            str(overlay["subline"]), x, subline_y,
            int(overlay.get("subline_size", 34)), "#e2e8f0", 500, subline_chars,
            body_family,
        )
        if anchor:
            subline = subline.replace("<text ", f"<text{anchor} ", 1)
        parts.append(subline)
    parts.append("</svg>")
    svg_path = work / f"scene-{scene_index:02d}-overlay.svg"
    png_path = work / f"scene-{scene_index:02d}-overlay.png"
    svg_path.write_text("\n".join(parts), encoding="utf-8")
    run(["rsvg-convert", "-w", str(width), "-h", str(height), "-o", str(png_path), str(svg_path)], env=font_env)
    (work / f"scene-{scene_index:02d}-font-receipt.json").write_text(
        json.dumps({
            "fontconfig": str(fontconfig.resolve()),
            "display_family": display_family,
            "display_file": str(display_resolved),
            "body_family": body_family,
            "body_file": str(body_resolved),
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    return png_path


def normalize_scene(
    scene: dict,
    index: int,
    work: Path,
    width: int,
    height: int,
    fps: int,
    font: Path,
    body_font: Path,
) -> tuple[Path, float]:
    source = Path(scene["source"]).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    duration = float(scene["duration"])
    if duration <= 0:
        raise ValueError(f"scene {index} has non-positive duration")
    start = float(scene.get("start", 0.0))
    output = work / f"scene-{index:02d}.mp4"
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    is_image = source.suffix.lower() in IMAGE_SUFFIXES
    if is_image:
        command += ["-framerate", str(fps), "-i", str(source)]
    else:
        command += ["-ss", str(start), "-i", str(source)]

    fit = scene.get("fit", "cover")
    canvas = scene.get("canvas", "0x0b1220")
    if fit == "contain":
        chain = (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color={canvas}"
        )
    elif fit == "contain_blur":
        chain = (
            f"split=2[scene_bg][scene_fg];"
            f"[scene_bg]scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},gblur=sigma=28[scene_bg_ready];"
            f"[scene_fg]scale={width}:{height}:force_original_aspect_ratio=decrease[scene_fg_ready];"
            f"[scene_bg_ready][scene_fg_ready]overlay=(W-w)/2:(H-h)/2"
        )
    else:
        chain = (
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height}"
        )

    if is_image and scene.get("motion") == "push":
        motion_frames = max(1, int(round(duration * fps)))
        chain += (
            f",zoompan=z='min(zoom+0.00045,1.045)':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={motion_frames}:s={width}x{height}:fps={fps}"
        )

    grade = scene.get("grade", {})
    contrast = float(grade.get("contrast", 1.0))
    brightness = float(grade.get("brightness", 0.0))
    saturation = float(grade.get("saturation", 1.0))
    chain += f",eq=contrast={contrast}:brightness={brightness}:saturation={saturation}"
    if is_image and scene.get("motion") != "push":
        chain += f",tpad=stop_mode=clone:stop_duration={duration}"
    chain += f",fps={fps}"

    overlay = scene.get("overlay") or {}
    kinetic_text = scene.get("kinetic_text") or {}
    if overlay and kinetic_text:
        raise ValueError(f"scene {index} cannot combine static overlay and kinetic_text")
    if kinetic_text:
        kinetic_path = render_kinetic_scene(
            index,
            kinetic_text,
            duration,
            width,
            height,
            fps,
            font,
            body_font,
            work,
        )
        command += ["-i", str(kinetic_path)]
        filter_option = "-filter_complex"
        filter_value = (
            f"[0:v]{chain}[base];"
            f"[1:v]setpts=PTS-STARTPTS,fps={fps},format=argb[kinetic];"
            "[base][kinetic]overlay=0:0:alpha=straight:shortest=1:format=auto,"
            "format=yuv420p,setsar=1"
        )
    elif overlay:
        overlay_path = render_overlay(work, index, overlay, width, height, font, body_font)
        command += ["-framerate", str(fps), "-i", str(overlay_path)]
        filter_option = "-filter_complex"
        filter_value = (
            f"[0:v]{chain}[base];"
            f"[1:v]tpad=stop_mode=clone:stop_duration={duration},fps={fps}[overlay];"
            "[base][overlay]overlay=0:0,format=yuv420p,setsar=1"
        )
    else:
        filter_option = "-vf"
        filter_value = chain + ",format=yuv420p,setsar=1"
    command += [
        "-t", str(duration),
        filter_option, filter_value,
        "-an", "-r", str(fps), "-c:v", "libx264", "-preset", "medium",
        "-crf", str(scene.get("crf", 18)), "-pix_fmt", "yuv420p", str(output),
    ]
    run(command)
    return output, duration


def join_scenes(clips: list[Path], scenes: list[dict], durations: list[float], work: Path, fps: int) -> tuple[Path, float]:
    output = work / "picture-track.mp4"
    if len(clips) == 1:
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(clips[0]), "-an", "-c:v", "copy", str(output)])
        return output, durations[0]

    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for clip in clips:
        command += ["-i", str(clip)]
    transition_duration = 0.0
    result_duration = durations[0]
    filters = []
    previous = "[0:v]"
    for index in range(1, len(clips)):
        td = float(scenes[index].get("transition_duration", 0.28))
        td = max(0.0, min(td, durations[index] / 2.0, result_duration / 2.0))
        transition = scenes[index].get("transition", "fade")
        minimum_transition = (1.0 / fps) + 0.000001
        if td < minimum_transition:
            transition = "fade"
            td = minimum_transition
        offset = result_duration - td
        target = f"[xf{index}]"
        filters.append(
            f"{previous}[{index}:v]xfade=transition={transition}:duration={td:.6f}:offset={offset:.6f}{target}"
        )
        previous = target
        result_duration += durations[index] - td
        transition_duration += td
    command += [
        "-filter_complex", ";".join(filters), "-map", previous,
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ]
    run(command)
    return output, sum(durations) - transition_duration


def add_audio(picture: Path, manifest: dict, duration: float, output: Path) -> None:
    audio = manifest.get("audio") or {}
    music = Path(audio["music"]).expanduser().resolve() if audio.get("music") else None
    voice = Path(audio["voice"]).expanduser().resolve() if audio.get("voice") else None
    output.parent.mkdir(parents=True, exist_ok=True)
    if music and not music.is_file():
        raise FileNotFoundError(music)
    if voice and not voice.is_file():
        raise FileNotFoundError(voice)

    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(picture)]
    if music:
        command += ["-stream_loop", "-1", "-i", str(music)]
    if voice:
        command += ["-i", str(voice)]
    if music and voice:
        voice_index = 2
        delay = int(float(audio.get("voice_start", 0.0)) * 1000)
        filters = (
            f"[1:a]atrim=0:{duration:.6f},volume={float(audio.get('music_volume', 0.42))}[music];"
            f"[{voice_index}:a]adelay={delay}|{delay},volume={float(audio.get('voice_volume', 1.0))}[voice];"
            f"[music][voice]amix=inputs=2:duration=first:dropout_transition=0,alimiter=limit=0.95[aout]"
        )
        command += ["-filter_complex", filters, "-map", "0:v", "-map", "[aout]"]
    elif music:
        command += [
            "-filter_complex", f"[1:a]atrim=0:{duration:.6f},volume={float(audio.get('music_volume', 0.58))},alimiter=limit=0.95[aout]",
            "-map", "0:v", "-map", "[aout]",
        ]
    elif voice:
        delay = int(float(audio.get("voice_start", 0.0)) * 1000)
        command += [
            "-filter_complex", f"[1:a]adelay={delay}|{delay},apad,atrim=0:{duration:.6f},alimiter=limit=0.95[aout]",
            "-map", "0:v", "-map", "[aout]",
        ]
    else:
        command += ["-f", "lavfi", "-t", f"{duration:.6f}", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a"]
    command += [
        "-t", f"{duration:.6f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000", "-movflags", "+faststart", str(output),
    ]
    run(command)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--work-dir", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    width = int(manifest.get("width", 1920))
    height = int(manifest.get("height", 1080))
    fps = int(manifest.get("fps", 30))
    font = Path(manifest.get("font", "/System/Library/Fonts/SFNS.ttf"))
    body_font = Path(manifest.get("body_font", str(font)))
    scenes = manifest.get("scenes") or []
    if not scenes:
        raise SystemExit("manifest requires at least one scene")
    text_policy = manifest.get("text_policy")
    if text_policy not in (None, "kinetic_only"):
        raise SystemExit(f"unsupported text_policy: {text_policy}")
    if text_policy == "kinetic_only":
        static_scenes = [index for index, scene in enumerate(scenes) if scene.get("overlay")]
        if static_scenes:
            raise SystemExit(
                "text_policy kinetic_only forbids static overlay in scenes: "
                + ", ".join(str(index) for index in static_scenes)
            )
    output = (args.output or Path(manifest["output"])).expanduser().resolve()
    work = (args.work_dir or output.parent / ".brand-film-render").expanduser().resolve()
    work.mkdir(parents=True, exist_ok=True)

    normalized = [
        normalize_scene(scene, i, work, width, height, fps, font, body_font)
        for i, scene in enumerate(scenes)
    ]
    clips = [item[0] for item in normalized]
    durations = [item[1] for item in normalized]
    picture, duration = join_scenes(clips, scenes, durations, work, fps)
    add_audio(picture, manifest, duration, output)
    print(json.dumps({
        "output": str(output),
        "duration_seconds": duration,
        "scenes": len(scenes),
        "work_dir": str(work),
        "command_preview": shlex.join(["ffprobe", "-v", "error", str(output)]),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
