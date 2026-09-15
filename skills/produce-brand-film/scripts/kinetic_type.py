#!/usr/bin/env python3
"""Render deterministic kinetic typography as a transparent alpha movie."""

from __future__ import annotations

import hashlib
import html
import json
import os
import shutil
import subprocess
from pathlib import Path


ENGINE_VERSION = "svg-frames-v1"
SUPPORTED_PRESETS = {
    "word_fade",
    "line_mask_rise",
    "line_mask_left",
    "block_scale_tracking",
    "fade_rise",
}
SUPPORTED_EASINGS = {"linear", "out_cubic", "in_cubic", "in_out_cubic"}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def command_version(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        combined = result.stdout.splitlines() + result.stderr.splitlines()
        return next((line.strip() for line in combined if line.strip()), "unknown")
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def scan_font(font: Path) -> dict[str, str]:
    result = subprocess.run(
        ["fc-scan", "--format", "%{family[0]}\n%{style[0]}\n%{weight}\n", str(font)],
        check=True,
        text=True,
        capture_output=True,
    )
    lines = [line.strip() for line in result.stdout.splitlines()]
    if not lines or not lines[0]:
        raise RuntimeError(f"could not resolve font metadata from {font}")
    return {
        "family": lines[0],
        "style": lines[1] if len(lines) > 1 and lines[1] else "Regular",
        "weight": lines[2] if len(lines) > 2 and lines[2] else "unknown",
    }


def font_environment(work: Path, fonts: list[Path]) -> tuple[dict[str, str], Path]:
    if not shutil.which("fc-scan") or not shutil.which("fc-match"):
        raise RuntimeError("fc-scan and fc-match are required for kinetic typography")
    directories = sorted({font.resolve().parent for font in fonts}, key=str)
    cache = work / "kinetic-fontconfig-cache"
    cache.mkdir(parents=True, exist_ok=True)
    config = work / "kinetic-fonts.conf"
    entries = "\n".join(f"  <dir>{html.escape(str(path))}</dir>" for path in directories)
    config.write_text(
        "<?xml version=\"1.0\"?>\n"
        "<!DOCTYPE fontconfig SYSTEM \"fonts.dtd\">\n"
        "<fontconfig>\n"
        f"{entries}\n"
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


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def ease(progress: float, name: str) -> float:
    progress = clamp(progress)
    if name == "linear":
        return progress
    if name == "out_cubic":
        return 1.0 - (1.0 - progress) ** 3
    if name == "in_cubic":
        return progress ** 3
    if name == "in_out_cubic":
        return 4.0 * progress ** 3 if progress < 0.5 else 1.0 - ((-2.0 * progress + 2.0) ** 3) / 2.0
    raise ValueError(f"unsupported easing: {name}")


def animation_progress(now: float, animation: dict, stagger_index: int = 0) -> float:
    start = float(animation.get("start", 0.0)) + stagger_index * float(animation.get("stagger", 0.0))
    duration = float(animation.get("duration", 0.45))
    if duration <= 0:
        raise ValueError("animation duration must be positive")
    easing = str(animation.get("ease", "out_cubic"))
    if easing not in SUPPORTED_EASINGS:
        raise ValueError(f"unsupported easing: {easing}")
    return ease((now - start) / duration, easing)


def track_opacity_and_exit(now: float, track: dict) -> tuple[float, float]:
    enter = track["enter"]
    enter_progress = animation_progress(now, enter)
    opacity = enter_progress
    exit_progress = 0.0
    if track.get("exit"):
        exit_progress = animation_progress(now, track["exit"])
        opacity *= 1.0 - exit_progress
    return clamp(opacity), clamp(exit_progress)


def svg_text_line(
    text: str,
    x: float,
    y: float,
    family: str,
    size: float,
    weight: int,
    fill: str,
    anchor: str,
    tracking: float,
    opacity: float,
    transform: str = "",
    clip: str = "",
) -> str:
    transform_attr = f' transform="{transform}"' if transform else ""
    clip_attr = f' clip-path="url(#{clip})"' if clip else ""
    return (
        f'<text x="{x:.3f}" y="{y:.3f}" text-anchor="{anchor}" '
        f'fill="{html.escape(fill)}" fill-opacity="{clamp(opacity):.6f}" '
        f'font-family="{html.escape(family)}, sans-serif" font-size="{size:.3f}" '
        f'font-weight="{weight}" letter-spacing="{tracking:.3f}"{transform_attr}{clip_attr}>'
        f'{html.escape(text)}</text>'
    )


def render_track(track: dict, now: float, width: int, height: int, display_family: str, body_family: str) -> tuple[list[str], list[str]]:
    enter = track.get("enter")
    if not enter:
        raise ValueError(f"kinetic track {track.get('id', '<unnamed>')} requires enter animation")
    preset = str(enter.get("preset", "line_mask_rise"))
    if preset not in SUPPORTED_PRESETS:
        raise ValueError(f"unsupported kinetic preset: {preset}")
    lines = track.get("lines")
    if not isinstance(lines, list) or not lines or not all(isinstance(line, str) for line in lines):
        raise ValueError(f"kinetic track {track.get('id', '<unnamed>')} requires explicit string lines")

    family = display_family if track.get("font_role", "display") == "display" else body_family
    font_size = float(track.get("font_size", 120))
    line_height = font_size * float(track.get("line_height", 1.05))
    x = float(track.get("x", width / 2))
    y = float(track.get("y", height / 2))
    anchor_map = {"left": "start", "middle": "middle", "right": "end", "start": "start", "end": "end"}
    anchor = anchor_map.get(str(track.get("anchor", "middle")))
    if not anchor:
        raise ValueError(f"unsupported text anchor: {track.get('anchor')}")
    fill = str(track.get("fill", "#ffffff"))
    weight = int(track.get("weight", 700 if track.get("font_role", "display") == "display" else 500))
    distance = float(enter.get("distance_px", 48))
    tracking_spec = track.get("tracking_px", {})
    tracking_from = float(tracking_spec.get("from", 0.0))
    tracking_to = float(tracking_spec.get("to", -1.0))
    scale_from = float(enter.get("scale_from", 0.96))
    opacity, exit_progress = track_opacity_and_exit(now, track)
    exit_distance = float((track.get("exit") or {}).get("distance_px", 32))

    definitions: list[str] = []
    elements: list[str] = []
    block_progress = animation_progress(now, enter)
    tracking = tracking_from + (tracking_to - tracking_from) * block_progress
    scale = scale_from + (1.0 - scale_from) * block_progress
    exit_dy = -exit_distance * exit_progress
    group_transform = ""
    if preset == "block_scale_tracking":
        group_transform = f"translate({x:.3f} {y:.3f}) scale({scale:.6f}) translate({-x:.3f} {-y:.3f})"
    if exit_dy:
        group_transform = (group_transform + f" translate(0 {exit_dy:.3f})").strip()
    if group_transform:
        elements.append(f'<g transform="{group_transform}">')

    for line_index, line in enumerate(lines):
        line_y = y + line_index * line_height
        progress = animation_progress(now, enter, line_index)
        line_opacity = opacity
        line_transform = ""
        clip_id = ""

        if preset == "word_fade":
            words = line.split(" ")
            spans = []
            for word_index, word in enumerate(words):
                word_progress = animation_progress(now, {**enter, "stagger": float(enter.get("word_stagger", 0.07))}, word_index)
                suffix = " " if word_index < len(words) - 1 else ""
                spans.append(f'<tspan fill-opacity="{word_progress * (1.0 - exit_progress):.6f}">{html.escape(word + suffix)}</tspan>')
            elements.append(
                f'<text x="{x:.3f}" y="{line_y:.3f}" text-anchor="{anchor}" xml:space="preserve" '
                f'style="white-space:pre" fill="{html.escape(fill)}" '
                f'font-family="{html.escape(family)}, sans-serif" font-size="{font_size:.3f}" '
                f'font-weight="{weight}" letter-spacing="{tracking:.3f}">' + "".join(spans) + "</text>"
            )
            continue
        if preset == "line_mask_rise":
            line_transform = f"translate(0 {distance * (1.0 - progress):.3f})"
            clip_id = f"clip-{html.escape(str(track.get('id', 'track')))}-{line_index}"
            box_height = font_size * 1.35
            top = line_y - font_size * 1.02 + box_height * (1.0 - progress)
            definitions.append(
                f'<clipPath id="{clip_id}"><rect x="0" y="{top:.3f}" width="{width}" height="{max(0.01, box_height * progress):.3f}"/></clipPath>'
            )
            line_opacity *= progress
        elif preset == "line_mask_left":
            clip_id = f"clip-{html.escape(str(track.get('id', 'track')))}-{line_index}"
            definitions.append(
                f'<clipPath id="{clip_id}"><rect x="0" y="{line_y - font_size * 1.05:.3f}" width="{max(0.01, width * progress):.3f}" height="{font_size * 1.4:.3f}"/></clipPath>'
            )
            line_opacity *= progress
        elif preset == "fade_rise":
            line_transform = f"translate(0 {distance * (1.0 - progress):.3f})"
            line_opacity *= progress

        elements.append(svg_text_line(
            line,
            x,
            line_y,
            family,
            font_size,
            weight,
            fill,
            anchor,
            tracking,
            line_opacity,
            transform=line_transform,
            clip=clip_id,
        ))

    if group_transform:
        elements.append("</g>")
    return definitions, elements


def render_frame_svg(
    kinetic: dict,
    now: float,
    width: int,
    height: int,
    display_family: str,
    body_family: str,
) -> bytes:
    all_definitions: list[str] = []
    all_elements: list[str] = []
    max_visibility = 0.0
    for track in kinetic.get("tracks") or []:
        definitions, elements = render_track(track, now, width, height, display_family, body_family)
        all_definitions.extend(definitions)
        all_elements.extend(elements)
        visibility, _ = track_opacity_and_exit(now, track)
        max_visibility = max(max_visibility, visibility)
    scrim = kinetic.get("scrim") or {}
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    if all_definitions:
        parts.append("<defs>" + "".join(all_definitions) + "</defs>")
    if scrim:
        parts.append(
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="{html.escape(str(scrim.get("color", "#0b1220")))}" '
            f'fill-opacity="{float(scrim.get("opacity", 0.0)) * max_visibility:.6f}"/>'
        )
    parts.extend(all_elements)
    parts.append("</svg>")
    return "\n".join(parts).encode("utf-8")


def render_png(svg: bytes, width: int, height: int, env: dict[str, str]) -> bytes:
    result = subprocess.run(
        ["rsvg-convert", "-w", str(width), "-h", str(height), "-f", "png"],
        input=svg,
        check=True,
        capture_output=True,
        env=env,
    )
    if not result.stdout.startswith(b"\x89PNG"):
        raise RuntimeError("rsvg-convert did not return a PNG frame")
    return result.stdout


def render_kinetic_scene(
    scene_index: int,
    kinetic: dict,
    duration: float,
    width: int,
    height: int,
    fps: int,
    font: Path,
    body_font: Path,
    work: Path,
) -> Path:
    if not shutil.which("rsvg-convert"):
        raise RuntimeError("rsvg-convert is required for kinetic typography")
    for candidate in (font, body_font):
        if not candidate.is_file():
            raise FileNotFoundError(candidate)
    tracks = kinetic.get("tracks") or []
    if not tracks:
        raise ValueError(f"scene {scene_index} kinetic_text requires tracks")
    if fps <= 0 or duration <= 0:
        raise ValueError("kinetic render requires positive fps and duration")

    font_meta = scan_font(font)
    body_meta = scan_font(body_font)
    env, fontconfig = font_environment(work, [font, body_font])
    display_resolved = assert_font_match(env, font_meta["family"], font)
    body_resolved = assert_font_match(env, body_meta["family"], body_font)
    frame_count = int(round(duration * fps))
    output = work / f"scene-{scene_index:02d}-kinetic.mov"
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "image2pipe", "-vcodec", "png", "-framerate", str(fps), "-i", "-",
        "-an", "-frames:v", str(frame_count), "-c:v", "qtrle", "-pix_fmt", "argb", str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.stdin is None:
        raise RuntimeError("failed to open ffmpeg image pipe")
    cache: dict[str, bytes] = {}
    frame_hashes: list[str] = []
    proof_indices = sorted({0, max(0, frame_count // 8), max(0, frame_count // 4), max(0, frame_count // 2), frame_count - 1})
    proof_paths: list[str] = []
    try:
        for frame_index in range(frame_count):
            now = frame_index / fps
            svg = render_frame_svg(kinetic, now, width, height, font_meta["family"], body_meta["family"])
            svg_hash = sha256_bytes(svg)
            png = cache.get(svg_hash)
            if png is None:
                png = render_png(svg, width, height, env)
                cache[svg_hash] = png
            frame_hashes.append(sha256_bytes(png))
            if frame_index in proof_indices:
                proof = work / f"scene-{scene_index:02d}-kinetic-proof-{frame_index:04d}.png"
                proof.write_bytes(png)
                proof_paths.append(str(proof.resolve()))
            process.stdin.write(png)
    finally:
        process.stdin.close()
    stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"ffmpeg kinetic alpha render failed: {stderr.strip()}")

    probe = json.loads(subprocess.run(
        [
            "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
            "-show_entries", "stream=codec_name,pix_fmt,nb_read_frames,r_frame_rate,duration",
            "-of", "json", str(output),
        ],
        check=True,
        text=True,
        capture_output=True,
    ).stdout)
    stream = probe["streams"][0]
    decode = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(output), "-f", "null", "-"],
        text=True,
        capture_output=True,
    )
    actual_frames = int(stream.get("nb_read_frames", 0))
    presets = sorted({str(track["enter"].get("preset", "line_mask_rise")) for track in tracks})
    if len(set(frame_hashes)) <= 1:
        raise RuntimeError(f"scene {scene_index} kinetic typography produced no visible motion")
    if stream.get("codec_name") != "qtrle" or stream.get("pix_fmt") != "argb":
        raise RuntimeError(f"unexpected kinetic alpha format: {stream.get('codec_name')}/{stream.get('pix_fmt')}")
    if actual_frames != frame_count or decode.returncode != 0:
        raise RuntimeError(f"kinetic alpha validation failed: frames={actual_frames}/{frame_count} decode={decode.returncode}")

    normalized = json.dumps(kinetic, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    copy_payload = json.dumps(
        [{"id": track.get("id"), "lines": track.get("lines")} for track in tracks],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    receipt = {
        "engine": ENGINE_VERSION,
        "scene_index": scene_index,
        "manifest_hash": sha256_bytes(normalized),
        "copy_hash": sha256_bytes(copy_payload),
        "track_ids": [str(track.get("id", "")) for track in tracks],
        "presets": presets,
        "fontconfig": str(fontconfig.resolve()),
        "display_font": {
            **font_meta,
            "file": str(display_resolved),
            "sha256": sha256_file(display_resolved),
        },
        "body_font": {
            **body_meta,
            "file": str(body_resolved),
            "sha256": sha256_file(body_resolved),
        },
        "versions": {
            "rsvg": command_version(["rsvg-convert", "--version"]),
            "fontconfig": command_version(["fc-match", "--version"]),
            "ffmpeg": command_version(["ffmpeg", "-version"]),
        },
        "fps": fps,
        "duration_seconds": duration,
        "expected_frames": frame_count,
        "actual_frames": actual_frames,
        "alpha_codec": stream.get("codec_name"),
        "alpha_pix_fmt": stream.get("pix_fmt"),
        "unique_frame_hashes": len(set(frame_hashes)),
        "alpha_decode_pass": decode.returncode == 0,
        "proof_frames": proof_paths,
        "output": str(output.resolve()),
    }
    (work / f"scene-{scene_index:02d}-kinetic-receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output
