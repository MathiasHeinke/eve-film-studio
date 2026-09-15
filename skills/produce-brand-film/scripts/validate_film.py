#!/usr/bin/env python3
"""Validate a delivery MP4 and optionally render a deterministic contact sheet."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import struct
import subprocess
from pathlib import Path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=True)


def mp4_top_level_atoms(path: Path) -> list[tuple[str, int]]:
    atoms: list[tuple[str, int]] = []
    file_size = path.stat().st_size
    with path.open("rb") as source:
        offset = 0
        while offset + 8 <= file_size:
            source.seek(offset)
            header = source.read(8)
            if len(header) != 8:
                break
            atom_size, atom_type = struct.unpack(">I4s", header)
            header_size = 8
            if atom_size == 1:
                extended = source.read(8)
                if len(extended) != 8:
                    break
                atom_size = struct.unpack(">Q", extended)[0]
                header_size = 16
            elif atom_size == 0:
                atom_size = file_size - offset
            if atom_size < header_size or offset + atom_size > file_size:
                break
            atoms.append((atom_type.decode("latin-1"), offset))
            offset += atom_size
    return atoms


def stream_fps(stream: dict) -> float:
    value = stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "0/1"
    try:
        return float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        return 0.0


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_kinetic_text(manifest: dict, render_dir: Path | None) -> tuple[dict, dict]:
    policy = manifest.get("text_policy")
    scenes = manifest.get("scenes") or []
    kinetic_indices = [index for index, scene in enumerate(scenes) if scene.get("kinetic_text")]
    static_indices = [index for index, scene in enumerate(scenes) if scene.get("overlay")]
    details: dict = {
        "policy": policy,
        "kinetic_scene_indices": kinetic_indices,
        "static_overlay_scene_indices": static_indices,
        "receipts": [],
    }
    checks: dict[str, bool] = {}
    if policy is None:
        return details, checks
    checks["text_policy_supported"] = policy == "kinetic_only"
    if policy != "kinetic_only":
        return details, checks

    checks["kinetic_policy_no_static_overlays"] = not static_indices
    checks["kinetic_policy_has_animated_text"] = bool(kinetic_indices)
    checks["kinetic_render_dir_present"] = render_dir is not None and render_dir.is_dir()
    if render_dir is None or not render_dir.is_dir():
        return details, checks

    for index in kinetic_indices:
        kinetic = scenes[index]["kinetic_text"]
        receipt_path = render_dir / f"scene-{index:02d}-kinetic-receipt.json"
        prefix = f"kinetic_scene_{index:02d}"
        checks[f"{prefix}_receipt_present"] = receipt_path.is_file()
        if not receipt_path.is_file():
            continue
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            checks[f"{prefix}_receipt_parse"] = False
            continue
        checks[f"{prefix}_receipt_parse"] = True
        details["receipts"].append({"path": str(receipt_path.resolve()), "receipt": receipt})

        normalized = json.dumps(
            kinetic,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        tracks = kinetic.get("tracks") or []
        copy_payload = json.dumps(
            [{"id": track.get("id"), "lines": track.get("lines")} for track in tracks],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        checks[f"{prefix}_engine"] = receipt.get("engine") == "svg-frames-v1"
        checks[f"{prefix}_manifest_hash"] = receipt.get("manifest_hash") == sha256_bytes(normalized)
        checks[f"{prefix}_copy_hash"] = receipt.get("copy_hash") == sha256_bytes(copy_payload)
        checks[f"{prefix}_frames_exact"] = (
            int(receipt.get("expected_frames", -1)) == int(receipt.get("actual_frames", -2))
            and int(receipt.get("expected_frames", 0)) > 0
        )
        checks[f"{prefix}_real_motion"] = int(receipt.get("unique_frame_hashes", 0)) > 1
        checks[f"{prefix}_alpha_format"] = (
            receipt.get("alpha_codec") == "qtrle" and receipt.get("alpha_pix_fmt") == "argb"
        )
        checks[f"{prefix}_alpha_decode"] = receipt.get("alpha_decode_pass") is True
        checks[f"{prefix}_proof_frames"] = len(receipt.get("proof_frames") or []) >= 4

        for role in ("display_font", "body_font"):
            font_info = receipt.get(role) or {}
            font_path = Path(str(font_info.get("file", "")))
            checks[f"{prefix}_{role}_present"] = font_path.is_file()
            checks[f"{prefix}_{role}_hash"] = (
                font_path.is_file() and font_info.get("sha256") == sha256_file(font_path)
            )
    return details, checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("film", type=Path)
    parser.add_argument("--min-duration", type=float, default=20.0)
    parser.add_argument("--max-duration", type=float, default=90.0)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=float, choices=(24.0, 25.0, 30.0, 50.0, 60.0))
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--render-dir", type=Path)
    args = parser.parse_args()
    if not args.film.is_file() or args.film.stat().st_size == 0:
        raise SystemExit(f"missing or empty film: {args.film}")

    probe = json.loads(run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(args.film),
    ]).stdout)
    video = next((s for s in probe["streams"] if s.get("codec_type") == "video"), None)
    audio = next((s for s in probe["streams"] if s.get("codec_type") == "audio"), None)
    duration = float(probe["format"].get("duration", 0.0))
    atoms = mp4_top_level_atoms(args.film)
    atom_offsets = {name: offset for name, offset in atoms}
    faststart = (
        "moov" in atom_offsets
        and "mdat" in atom_offsets
        and atom_offsets["moov"] < atom_offsets["mdat"]
    )
    fps = stream_fps(video or {})
    fps_match = (
        abs(fps - args.fps) < 0.01
        if args.fps is not None
        else any(abs(fps - supported) < 0.01 for supported in (24.0, 30.0))
    )
    decode = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(args.film), "-f", "null", "-"],
        text=True,
        capture_output=True,
    )
    video_duration = float((video or {}).get("duration") or 0.0)
    audio_duration = float((audio or {}).get("duration") or 0.0)
    duration_tolerance = max(0.1, 2.0 / fps) if fps > 0 else 0.1
    checks = {
        "duration_in_range": args.min_duration <= duration <= args.max_duration,
        "video_present": video is not None,
        "audio_present": audio is not None,
        "dimensions_match": bool(video) and video.get("width") == args.width and video.get("height") == args.height,
        "video_codec_h264": bool(video) and video.get("codec_name") == "h264",
        "pixel_format_web_safe": bool(video) and video.get("pix_fmt") == "yuv420p",
        "frame_rate_match": bool(video) and fps > 0 and fps_match,
        "audio_codec_aac": bool(audio) and audio.get("codec_name") == "aac",
        "audio_sample_rate_48000": bool(audio) and int(audio.get("sample_rate", 0)) == 48000,
        "audio_stereo": bool(audio) and int(audio.get("channels", 0)) == 2,
        "video_duration_matches_container": bool(video) and abs(video_duration - duration) <= duration_tolerance,
        "audio_duration_matches_container": bool(audio) and abs(audio_duration - duration) <= duration_tolerance,
        "faststart": faststart,
        "full_decode": decode.returncode == 0,
        "file_nonzero": args.film.stat().st_size > 100_000,
    }
    kinetic_details = None
    if args.manifest:
        if not args.manifest.is_file():
            raise SystemExit(f"missing manifest: {args.manifest}")
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        kinetic_details, kinetic_checks = validate_kinetic_text(manifest, args.render_dir)
        checks.update(kinetic_checks)
    receipt = {
        "film": str(args.film.resolve()),
        "duration_seconds": duration,
        "bytes": args.film.stat().st_size,
        "video": video,
        "audio": audio,
        "fps": fps,
        "top_level_atoms": atoms,
        "decode_stderr": decode.stderr.strip(),
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
    }
    if kinetic_details is not None:
        receipt["kinetic_text"] = kinetic_details

    if args.contact_sheet:
        args.contact_sheet.parent.mkdir(parents=True, exist_ok=True)
        interval = max(duration / 9.0, 0.5)
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(args.film), "-vf",
            f"fps=1/{interval:.6f},scale=480:-2,tile=3x3:padding=8:margin=8:color=0x0b1220",
            "-frames:v", "1", str(args.contact_sheet),
        ])
        receipt["contact_sheet"] = str(args.contact_sheet.resolve())

    rendered = json.dumps(receipt, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
