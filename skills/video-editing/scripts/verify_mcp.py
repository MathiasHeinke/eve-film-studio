#!/usr/bin/env python3
"""Exercise the installed FCPXML MCP with synthetic media, never a user's project."""

from __future__ import annotations

import argparse
import asyncio
from fractions import Fraction
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seconds(value: str) -> Fraction:
    return Fraction(value.removesuffix("s"))


def create_fixture(project: Path) -> tuple[Path, Path]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("The synthetic media check requires ffmpeg on PATH")
    media = project / "source.mp4"
    video = (
        "color=c=blue:s=320x180:r=25:d=2[b];"
        "color=c=red:s=320x180:r=25:d=3[r];"
        "color=c=green:s=320x180:r=25:d=3[g];"
        "[b][r][g]concat=n=3:v=1:a=0"
    )
    subprocess.run(
        [ffmpeg, "-hide_banner", "-loglevel", "error", "-n", "-f", "lavfi",
         "-i", video, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono",
         "-t", "8", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(media)],
        check=True, timeout=30,
    )
    words = []
    for start, end, phrase in [
        (0, 2, "Intro bleibt hier"),
        (2, 5, "Diesen ganzen Absatz entfernen"),
        (5, 8, "Schluss bleibt hier"),
    ]:
        tokens = phrase.split()
        for index, word in enumerate(tokens):
            words.append({"word": word, "start": start + (end-start)*index/len(tokens),
                          "end": start + (end-start)*(index+1)/len(tokens)})
    (project / "source_transcript.json").write_text(
        json.dumps({"source": media.name, "language": "de", "words": words,
                    "fixture_note": "Synthetic supplied transcript; not speech recognition."}, indent=2),
        encoding="utf-8",
    )
    root = ET.Element("fcpxml", version="1.10")
    resources = ET.SubElement(root, "resources")
    ET.SubElement(resources, "format", id="r1", name="Fixture25", frameDuration="1/25s",
                  width="320", height="180", colorSpace="1-1-1 (Rec. 709)")
    asset = ET.SubElement(resources, "asset", id="r2", name="source", start="0s", duration="8s",
                          hasVideo="1", format="r1", hasAudio="1", audioSources="1",
                          audioChannels="1", audioRate="48000")
    ET.SubElement(asset, "media-rep", kind="original-media", src=media.as_uri())
    library = ET.SubElement(root, "library")
    event = ET.SubElement(library, "event", name="Synthetic verification")
    project_el = ET.SubElement(event, "project", name="Passage fixture")
    sequence = ET.SubElement(project_el, "sequence", format="r1", duration="8s", tcStart="0s",
                             tcFormat="NDF", audioLayout="stereo", audioRate="48k")
    spine = ET.SubElement(sequence, "spine")
    ET.SubElement(spine, "asset-clip", ref="r2", name="Fixture Interview", offset="0s",
                  start="0s", duration="8s", format="r1")
    timeline = project / "original.fcpxml"
    ET.ElementTree(root).write(timeline, encoding="utf-8", xml_declaration=True)
    return timeline, media


async def verify(output: Path) -> dict:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    output.mkdir(parents=True, exist_ok=False)
    project = output / "project"
    project.mkdir()
    original, media = create_fixture(project)
    before = {"original": sha256(original), "media": sha256(media)}
    forbidden = output / "outside.fcpxml"
    forbidden.write_bytes(original.read_bytes())
    edited = project / "edited.fcpxml"
    env = {
        "PATH": os.environ.get("PATH", ""),
        "FCP_PROJECTS_DIRS": str(project),
        "FCP_PROJECTS_DIR": str(project),
        "FCP_MCP_INDEX": "off",
        "FCP_MCP_JOURNAL": str(project / ".journal"),
    }
    calls = []
    server = StdioServerParameters(command=sys.executable, args=["-I", "-m", "server"], env=env)
    with (output / "server.log").open("w", encoding="utf-8") as log:
        async with stdio_client(server, errlog=log) as streams:
            async with ClientSession(*streams) as client:
                await client.initialize()
                listing = await client.list_tools()
                names = {tool.name for tool in listing.tools}
                if not {"inspect", "transcript"}.issubset(names):
                    raise RuntimeError("The installed MCP does not expose the tested tool groups")
                (output / "tools.json").write_text(listing.model_dump_json(by_alias=True, indent=2))

                async def call(name: str, arguments: dict):
                    result = await client.call_tool(name, arguments)
                    payload = result.model_dump(mode="json", by_alias=True, exclude_none=True)
                    calls.append({"name": name, "arguments": arguments, "result": payload})
                    return payload

                await call("inspect", {"action": "list_clips", "args": {"filepath": str(original)}})
                await call("transcript", {"action": "edit_by_transcript", "args": {
                    "filepath": str(original), "phrases": ["Diesen ganzen Absatz entfernen"],
                    "mode": "remove", "clip_name": "Fixture Interview", "padding": 0,
                    "backend": "local", "output_path": str(edited),
                }})
                outside = await call("inspect", {"action": "list_clips", "args": {"filepath": str(forbidden)}})
    (output / "calls.json").write_text(json.dumps(calls, ensure_ascii=False, indent=2), encoding="utf-8")
    if not edited.exists():
        raise RuntimeError("MCP did not produce the requested edited timeline; inspect calls.json")
    tree = ET.parse(edited)
    clips = tree.findall(".//sequence/spine/asset-clip")
    ranges = [(seconds(clip.get("start", "0s")), seconds(clip.get("duration", "0s"))) for clip in clips]
    declared_duration = seconds(tree.find(".//sequence").get("duration"))
    content_duration = sum((duration for _, duration in ranges), Fraction(0))
    outside_text = " ".join(str(item.get("text", "")) for item in outside.get("content", []))
    checks = {
        "expected_source_ranges": ranges == [(Fraction(0), Fraction(2)), (Fraction(5), Fraction(3))],
        "content_duration_correct": content_duration == 5,
        "declared_duration_correct": declared_duration == 5,
        "source_hashes_unchanged": sha256(original) == before["original"] and sha256(media) == before["media"],
        "out_of_root_read_rejected": "escapes the allowed roots" in outside_text.lower(),
    }
    return {
        "status": "offline_mcp_pass" if all(checks.values()) else "offline_mcp_findings",
        "checks": checks, "package": importlib.metadata.version("fcp-mcp-server"),
        "mcp_sdk": importlib.metadata.version("mcp"), "python": sys.version.split()[0],
        "tools_discovered": sorted(names), "content_seconds": str(content_duration),
        "declared_seconds": str(declared_duration),
        "surviving_source_ranges": [[str(start), str(duration)] for start, duration in ranges],
        "frame_rate_tested": "25/1", "real_speech_transcription_tested": False,
        "final_cut_opened": False, "live_voice_tested": False, "paid_render_calls": 0,
        "limitations": ["Synthetic transcript and media", "No native FCP import or preview",
                        "No multicam, fractional-rate or generative-video acceptance"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New output directory; existing paths are refused")
    output = parser.parse_args().output.resolve()
    if output.exists():
        parser.error("Output already exists; choose a new directory")
    try:
        result = asyncio.run(asyncio.wait_for(verify(output), timeout=60))
    except Exception as error:
        result = {"status": "failed", "error": f"{type(error).__name__}: {error}"}
    if output.is_dir():
        (output / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "offline_mcp_pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
