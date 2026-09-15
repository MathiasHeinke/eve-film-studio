#!/usr/bin/env python3
"""Generate an original tension-to-release stereo score using only stdlib."""

from __future__ import annotations

import argparse
import math
import random
import wave
from array import array
from pathlib import Path


def clamp(value: float, low: float = -0.98, high: float = 0.98) -> float:
    return max(low, min(high, value))


def envelope(phase: float, attack: float, decay: float) -> float:
    if phase < attack:
        return phase / max(attack, 1e-6)
    return math.exp(-(phase - attack) * decay)


def build_score(duration: float, transition: float, sample_rate: int, seed: int) -> array:
    total = int(duration * sample_rate)
    rng = random.Random(seed)
    pcm = array("h")
    bpm = 96.0
    beat = 60.0 / bpm
    notes = (146.83, 185.00, 220.00, 293.66)
    tick_times = []
    cursor = 0.45
    while cursor < max(0.0, transition - 0.35):
        progress = cursor / max(transition, 1.0)
        step = 0.72 - 0.38 * progress
        tick_times.append(cursor)
        cursor += step
    tick_index = 0

    for index in range(total):
        t = index / sample_rate
        left = 0.0
        right = 0.0

        if t < transition:
            ramp = 0.55 + 0.45 * (t / max(transition, 1.0))
            drone = (
                0.105 * math.sin(2 * math.pi * 73.42 * t)
                + 0.070 * math.sin(2 * math.pi * 110.00 * t + 0.3)
                + 0.035 * math.sin(2 * math.pi * 146.83 * t + 1.2)
            ) * ramp
            pulse_phase = (t % beat) / beat
            pulse = 0.065 * math.sin(2 * math.pi * 49.0 * t) * math.exp(-8.0 * pulse_phase)
            left += drone + pulse
            right += drone * 0.96 + pulse

            while tick_index + 1 < len(tick_times) and t > tick_times[tick_index + 1]:
                tick_index += 1
            if tick_times:
                dt = t - tick_times[tick_index]
                if 0.0 <= dt < 0.07:
                    tick = 0.11 * math.sin(2 * math.pi * 1650.0 * dt) * math.exp(-55.0 * dt)
                    left += tick
                    right += tick * 0.75
        else:
            local = t - transition
            phase = (local % beat) / beat
            beat_index = int(local / beat)
            note = notes[beat_index % len(notes)]
            pluck = 0.10 * math.sin(2 * math.pi * note * local) * envelope(phase, 0.03, 5.0)
            pad_fade = min(1.0, local / 2.0)
            pad = pad_fade * (
                0.085 * math.sin(2 * math.pi * 73.42 * t)
                + 0.055 * math.sin(2 * math.pi * 92.50 * t + 0.4)
                + 0.045 * math.sin(2 * math.pi * 110.00 * t + 0.9)
            )
            kick = 0.08 * math.sin(2 * math.pi * (58.0 - 18.0 * phase) * local) * math.exp(-10.0 * phase)
            pan = 0.28 * math.sin(2 * math.pi * local / (beat * 8.0))
            left += pad + kick + pluck * (1.0 - pan)
            right += pad * 1.02 + kick + pluck * (1.0 + pan)

        whoosh_dt = t - transition
        if -0.65 <= whoosh_dt <= 0.65:
            whoosh_env = math.sin(math.pi * (whoosh_dt + 0.65) / 1.3) ** 2
            noise = (rng.random() * 2.0 - 1.0) * 0.075 * whoosh_env
            left += noise
            right += noise * 0.85

        end_dt = duration - t
        if 0.0 < end_dt < 1.8:
            sting_env = math.sin(math.pi * (1.8 - end_dt) / 1.8) ** 2
            sting = 0.06 * sting_env * math.sin(2 * math.pi * 293.66 * t)
            left += sting
            right += sting
        if end_dt < 0.25:
            fade = max(0.0, end_dt / 0.25)
            left *= fade
            right *= fade

        pcm.append(int(clamp(left) * 32767))
        pcm.append(int(clamp(right) * 32767))
    return pcm


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, required=True)
    parser.add_argument("--transition", type=float, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sample-rate", type=int, default=48000)
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args()
    if args.duration <= 1 or not 0 < args.transition < args.duration:
        parser.error("transition must be inside a duration longer than one second")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    pcm = build_score(args.duration, args.transition, args.sample_rate, args.seed)
    with wave.open(str(args.out), "wb") as target:
        target.setnchannels(2)
        target.setsampwidth(2)
        target.setframerate(args.sample_rate)
        target.writeframes(pcm.tobytes())
    print(args.out.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
