#!/usr/bin/env python3
"""Real FFmpeg CLI regressions; fixtures and measurements are retained on disk."""

from __future__ import annotations

import argparse
import array
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave


ASSEMBLER = Path(__file__).resolve().parents[1] / "skills/produce-brand-film/scripts/assemble_film.py"
RATE = 48000
FPS = 24


def command(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, check=True, timeout=60)


def write_tone(path: Path, frequency: int, amplitude: float, duration: float = 3,
               pulse: tuple[float, float] | None = None) -> None:
    samples = array.array("h")
    for index in range(round(duration * RATE)):
        time = index / RATE
        active = pulse is None or pulse[0] <= time < pulse[1]
        samples.append(round(32767 * amplitude * math.sin(2 * math.pi * frequency * time)) if active else 0)
    if sys.byteorder != "little":
        samples.byteswap()
    with wave.open(str(path), "wb") as output:
        output.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        output.writeframes(samples.tobytes())


def decode_audio(path: Path) -> array.array:
    result = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-ac", "1",
         "-ar", str(RATE), "-f", "f32le", "-"],
        check=True, capture_output=True, timeout=60,
    )
    values = array.array("f", result.stdout)
    if sys.byteorder != "little":
        values.byteswap()
    return values


def rms(samples: array.array, start: float = 0, end: float | None = None) -> float:
    window = samples[round(start * RATE):round(end * RATE) if end is not None else None]
    if not window:
        raise AssertionError("empty measurement window")
    return math.sqrt(sum(value * value for value in window) / len(window))


def tone_amplitude(samples: array.array, frequency: int, start: float, end: float) -> float:
    """Measure a known fixture frequency, without a numerical dependency."""
    window = samples[round(start * RATE):round(end * RATE)]
    if not window:
        raise AssertionError("empty frequency measurement window")
    step = 2 * math.pi * frequency / RATE
    real = sum(value * math.cos(step * index) for index, value in enumerate(window))
    imaginary = sum(value * math.sin(step * index) for index, value in enumerate(window))
    return 2 * math.hypot(real, imaginary) / len(window)


def marker_center(samples: array.array, frequency: int) -> tuple[float, float]:
    # Non-overlapping 20 ms windows have whole cycles for every fixture tone.
    # The centroid is an absolute output timestamp, not correlation similarity.
    windows = []
    for index in range(len(samples) // 960):
        start = index * 0.02
        amplitude = tone_amplitude(samples, frequency, start, start + 0.02)
        if amplitude > 0.02:
            windows.append((start + 0.01, amplitude * amplitude))
    if not windows:
        raise AssertionError(f"missing {frequency} Hz marker")
    mass = sum(weight for _, weight in windows)
    return sum(time * weight for time, weight in windows) / mass, math.sqrt(max(weight for _, weight in windows))


class AssemblerCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            raise RuntimeError("ffmpeg and ffprobe are required; this suite does not install them")
        supplied = os.environ.get("EVE_FILM_TEST_OUTPUT")
        cls.root = Path(supplied).resolve() if supplied else Path(tempfile.mkdtemp(prefix="eve-film-cli-"))
        if supplied:
            cls.root.mkdir(parents=True, exist_ok=False)
        cls.assembler = Path(os.environ.get("EVE_FILM_ASSEMBLER", str(ASSEMBLER))).resolve()
        cls.metrics = {
            "scope": "synthetic final CLI audio/timeline regressions; no film-quality or release verdict",
            "assembler": str(cls.assembler),
            "assembler_sha256": hashlib.sha256(cls.assembler.read_bytes()).hexdigest(),
            "ffmpeg": command(["ffmpeg", "-version"]).stdout.splitlines()[0],
            "measurements": {},
        }
        cls.fixtures = cls.root / "fixtures"
        cls.fixtures.mkdir()
        cls.clips = []
        for index, color in enumerate(("0xff0000", "0x00ff00", "0x0000ff")):
            tone = cls.fixtures / f"marker-{index}.wav"
            write_tone(tone, 500 * (index + 1), 0.12, pulse=(0.7, 0.9))
            clip = cls.fixtures / f"source-{index}.mkv"
            cls.make_video(clip, color, 2, tone)
            cls.clips.append(clip)
        cls.short = cls.fixtures / "one-second-video-three-second-audio.mkv"
        cls.make_video(cls.short, "white", 1, cls.fixtures / "marker-0.wav")
        cls.no_audio = cls.fixtures / "no-audio.mp4"
        cls.make_video(cls.no_audio, "white", 2)
        cls.still = cls.fixtures / "still.png"
        command(["ffmpeg", "-v", "error", "-n", "-f", "lavfi", "-i",
                 "color=c=white:s=96x64", "-frames:v", "1", str(cls.still)])
        cls.voice = cls.fixtures / "voice.wav"
        cls.music = cls.fixtures / "score.wav"
        cls.silence = cls.fixtures / "silence.wav"
        write_tone(cls.voice, 2000, 0.05)
        write_tone(cls.music, 3000, 0.04)
        write_tone(cls.silence, 0, 0)
        print(f"Retained evidence: {cls.root}", flush=True)

    @classmethod
    def make_video(cls, path: Path, color: str, duration: float, audio: Path | None = None) -> None:
        args = ["ffmpeg", "-v", "error", "-n", "-f", "lavfi", "-i",
                f"color=c={color}:s=96x64:r={FPS}:d={duration}"]
        if audio:
            args += ["-i", str(audio), "-c:a", "pcm_s16le"]
        args += ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "10", "-pix_fmt", "yuv420p", str(path)]
        command(args)

    @classmethod
    def tearDownClass(cls) -> None:
        (cls.root / "measurements.json").write_text(json.dumps(cls.metrics, indent=2) + "\n")

    def render(self, name: str, scenes: list[dict], audio: dict | None = None,
               success: bool = True) -> tuple[Path, dict]:
        folder = Path(tempfile.mkdtemp(prefix=name + "-", dir=self.root))
        output = folder / "film.mp4"
        manifest = {"width": 96, "height": 64, "fps": FPS, "scenes": scenes}
        if audio is not None:
            manifest["audio"] = audio
        manifest_path = folder / "timeline.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        result = subprocess.run(
            [sys.executable, str(self.assembler), "--manifest", str(manifest_path),
             "--output", str(output), "--work-dir", str(folder / "render")],
            capture_output=True, text=True, timeout=60,
        )
        (folder / "stdout.txt").write_text(result.stdout)
        (folder / "stderr.txt").write_text(result.stderr)
        self.metrics["measurements"][name] = {"exit_code": result.returncode, "artifacts": str(folder)}
        if not success:
            self.assertNotEqual(result.returncode, 0, f"invalid manifest accepted: {manifest_path}")
            self.assertFalse(output.exists(), "invalid timeline produced a delivery file")
            return output, {}
        self.assertEqual(result.returncode, 0, f"CLI failed; see {folder / 'stderr.txt'}\n{result.stderr[-2000:]}")
        report = json.loads(result.stdout)
        self.metrics["measurements"][name]["reported_duration"] = report["duration_seconds"]
        return output, report

    def scene(self, index: int = 0, **fields) -> dict:
        return {"source": str(self.clips[index]), "start": 0.5, "duration": 1, **fields}

    def picture(self, output: Path, frames: int, report: dict) -> list[tuple[int, int, int]]:
        info = json.loads(command([
            "ffprobe", "-v", "error", "-count_frames", "-show_entries",
            "stream=codec_type,nb_read_frames,duration,avg_frame_rate", "-of", "json", str(output),
        ]).stdout)
        video = next(stream for stream in info["streams"] if stream["codec_type"] == "video")
        self.assertEqual(int(video["nb_read_frames"]), frames)
        self.assertEqual(video["avg_frame_rate"], "24/1")
        self.assertAlmostEqual(float(video["duration"]), frames / FPS, delta=0.000002)
        self.assertAlmostEqual(report["duration_seconds"], frames / FPS, delta=0.000002)
        raw = subprocess.run([
            "ffmpeg", "-v", "error", "-i", str(output), "-map", "0:v:0",
            "-vf", "scale=1:1", "-pix_fmt", "rgb24", "-f", "rawvideo", "-",
        ], capture_output=True, check=True, timeout=60).stdout
        return [tuple(raw[index:index + 3]) for index in range(0, len(raw), 3)]

    def assert_color(self, value: tuple[int, int, int], channel: int) -> None:
        self.assertGreater(value[channel], 180, value)
        self.assertTrue(all(component < 45 for index, component in enumerate(value) if index != channel), value)

    def test_invalid_source_ranges_rejected(self) -> None:
        cases = [("start", -0.1), ("start", "nan"), ("start", "inf"), ("start", "-inf"),
                 ("duration", -1), ("duration", 0), ("duration", "nan"),
                 ("duration", "inf"), ("duration", "-inf")]
        for index, (field, value) in enumerate(cases):
            with self.subTest(field=field, value=value):
                self.render(f"invalid-{index}", [self.scene(**{field: value})], success=False)

    def test_video_range_uses_video_not_longer_audio_or_container(self) -> None:
        probe = json.loads(command(["ffprobe", "-v", "error", "-show_format", "-show_streams",
                                    "-of", "json", str(self.short)]).stdout)
        self.assertGreater(float(probe["format"]["duration"]), 2.9)
        for start, duration in ((0, 1.25), (0.75, 0.5), (1.25, 0.25)):
            with self.subTest(start=start, duration=duration):
                self.render(f"past-video-{start}", [self.scene(source=str(self.short), start=start, duration=duration)], success=False)
        output, report = self.render("exact-video-end", [self.scene(source=str(self.short), start=0.5, duration=0.5)])
        self.picture(output, 12, report)

    def test_still_image_holds_declared_duration(self) -> None:
        for motion in (None, "push"):
            with self.subTest(motion=motion):
                scene = {"source": str(self.still), "duration": 1.375}
                if motion:
                    scene["motion"] = motion
                output, report = self.render(f"still-{motion}", [scene])
                self.picture(output, 33, report)

    def test_default_source_mute_and_explicit_keep_requires_audio(self) -> None:
        output, _ = self.render("default-mute", [self.scene()])
        level = rms(decode_audio(output))
        self.metrics["measurements"]["default-mute"]["rms"] = level
        self.assertLess(level, 0.0001)
        self.render("missing-source-audio", [self.scene(source=str(self.no_audio), source_audio="keep")], success=False)

    def test_voice_gain_and_silent_music_do_not_change_speech_level(self) -> None:
        levels = {}
        for music in (False, True):
            for gain in (0, 1):
                with self.subTest(music=music, gain=gain):
                    name = f"voice-gain-{gain}-music-{music}"
                    audio = {"voice": str(self.voice), "voice_volume": gain}
                    if music:
                        audio.update(music=str(self.silence), music_volume=1)
                    output, _ = self.render(name, [self.scene()], audio)
                    levels[(music, gain)] = rms(decode_audio(output), 0.1, 0.9)
                    self.metrics["measurements"][name]["rms"] = levels[(music, gain)]
                    if gain == 0:
                        self.assertLess(levels[(music, gain)], 0.0001)
                    else:
                        self.assertGreater(levels[(music, gain)], 0.025)
        ratio = levels[(True, 1)] / levels[(False, 1)]
        self.metrics["measurements"]["speech-with-silent-music-ratio"] = ratio
        self.assertAlmostEqual(ratio, 1, delta=0.03)

    def test_silent_voice_does_not_change_default_music_gain(self) -> None:
        levels = []
        for include_voice in (False, True):
            name = f"default-music-silent-voice-{include_voice}"
            audio = {"music": str(self.music)}
            if include_voice:
                audio.update(voice=str(self.voice), voice_volume=0)
            output, _ = self.render(name, [self.scene()], audio)
            level = rms(decode_audio(output), 0.1, 0.9)
            levels.append(level)
            self.metrics["measurements"][name]["rms"] = level
            self.assertGreater(level, 0.005)
        ratio = levels[1] / levels[0]
        self.metrics["measurements"]["music-with-silent-voice-ratio"] = ratio
        self.assertAlmostEqual(ratio, 1, delta=0.03)

    def test_silent_scene_before_kept_audio_preserves_track_timing(self) -> None:
        for explicit_mute in (False, True):
            name = f"silent-before-keep-{explicit_mute}"
            first = self.scene(source=str(self.no_audio))
            if explicit_mute:
                first = self.scene(source_audio="mute")
            output, report = self.render(name, [first, self.scene(1, source_audio="keep", transition="cut")])
            self.picture(output, 48, report)
            samples = decode_audio(output)
            silent_rms = rms(samples, 0.05, 0.95)
            actual, amplitude = marker_center(samples, 1000)
            self.metrics["measurements"][name].update(silent_rms=silent_rms, marker_seconds=actual, marker_amplitude=amplitude)
            self.assertLess(silent_rms, 0.0001)
            self.assertAlmostEqual(actual, 1.3, delta=0.02)
            self.assertAlmostEqual(amplitude, 0.12, delta=0.02)

    def test_both_cut_spellings_preserve_all_frames_and_marker_times(self) -> None:
        for cut in ({"transition": "cut"}, {"transition_duration": 0}):
            with self.subTest(cut=cut):
                name = "exact-cuts" if "transition" in cut else "zero-duration-cuts"
                scenes = [self.scene(source_audio="keep"), self.scene(1, source_audio="keep", **cut),
                          self.scene(2, source_audio="keep", **cut)]
                output, report = self.render(name, scenes)
                colors = self.picture(output, 72, report)
                for frame, channel in ((23, 0), (24, 1), (47, 1), (48, 2), (71, 2)):
                    self.assert_color(colors[frame], channel)
                samples = decode_audio(output)
                observed = []
                for frequency, expected in ((500, 0.3), (1000, 1.3), (1500, 2.3)):
                    actual, amplitude = marker_center(samples, frequency)
                    observed.append({"hz": frequency, "expected_seconds": expected, "observed_seconds": actual, "amplitude": amplitude})
                    self.assertAlmostEqual(actual, expected, delta=0.02)
                    self.assertAlmostEqual(amplitude, 0.12, delta=0.02)
                self.metrics["measurements"][name].update(frames=len(colors), markers=observed)

    def test_mixed_cut_and_fade_have_frame_exact_overlap_and_marker_times(self) -> None:
        for fade, overlap_frames, fade_first in ((0.25, 6, False), (0.13, 3, False), (0.25, 6, True)):
            with self.subTest(fade=fade, fade_first=fade_first):
                name = "mixed-fade-then-cut" if fade_first else f"mixed-fade-{fade}"
                transitions = [{"transition": "cut"}, {"transition": "fade", "transition_duration": fade}]
                if fade_first:
                    transitions.reverse()
                scenes = [self.scene(source_audio="keep"), self.scene(1, source_audio="keep", **transitions[0]),
                          self.scene(2, source_audio="keep", **transitions[1])]
                output, report = self.render(name, scenes)
                colors = self.picture(output, 72 - overlap_frames, report)
                cut_frame = 48 - overlap_frames if fade_first else 24
                self.assert_color(colors[cut_frame - 1], 1 if fade_first else 0)
                self.assert_color(colors[cut_frame], 2 if fade_first else 1)
                self.assert_color(colors[-1], 2)
                fade_end = 24 if fade_first else 48
                blend = colors[fade_end - overlap_frames + overlap_frames // 2]
                self.assertGreater(blend[0 if fade_first else 1], 45, blend)
                self.assertGreater(blend[1 if fade_first else 2], 45, blend)
                samples = decode_audio(output)
                observed = []
                middle = 1.3 - overlap_frames / FPS if fade_first else 1.3
                for frequency, expected in ((500, 0.3), (1000, middle), (1500, 2.3 - overlap_frames / FPS)):
                    actual, amplitude = marker_center(samples, frequency)
                    observed.append({"hz": frequency, "expected_seconds": expected, "observed_seconds": actual, "amplitude": amplitude})
                    self.assertAlmostEqual(actual, expected, delta=0.02)
                    self.assertGreater(amplitude, 0.08)
                self.metrics["measurements"][name].update(frames=len(colors), markers=observed)

    def test_source_score_and_voice_mix_at_requested_gain(self) -> None:
        for gain in (0, 1):
            name = f"source-score-voice-{gain}"
            output, _ = self.render(name, [self.scene(source_audio="keep")], {
                "music": str(self.music), "music_volume": 1,
                "voice": str(self.voice), "voice_volume": gain,
            })
            samples = decode_audio(output)
            amplitudes = {frequency: tone_amplitude(samples, frequency, 0.24, 0.36) for frequency in (500, 2000, 3000)}
            self.metrics["measurements"][name]["amplitudes"] = amplitudes
            self.assertAlmostEqual(amplitudes[500], 0.12, delta=0.015)
            self.assertAlmostEqual(amplitudes[3000], 0.04, delta=0.006)
            self.assertAlmostEqual(amplitudes[2000], 0.05 * gain, delta=0.006 if gain else 0.0005)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="New evidence directory; default: a retained mkdtemp directory")
    parser.add_argument("--assembler", type=Path, help="Optional assembler revision for a baseline comparison")
    args, unittest_args = parser.parse_known_args()
    if args.output:
        os.environ["EVE_FILM_TEST_OUTPUT"] = str(args.output)
    if args.assembler:
        os.environ["EVE_FILM_ASSEMBLER"] = str(args.assembler)
    unittest.main(argv=[sys.argv[0], *unittest_args], verbosity=2)
