# Assembler CLI regressions

Run with Python 3, FFmpeg (including libx264) and ffprobe already installed:

```bash
python3 tests/test_assemble_film_cli.py
```

The suite invokes the actual assembler CLI with tiny synthetic fixtures. It
checks usable video ranges, still holds, source-audio policy, voice gain,
mix levels, exact 24 fps cuts and fades, and absolute audio-marker positions.
These are technical media checks, not a creative-quality or release verdict.

Fixtures, manifests, output films, command logs and `measurements.json` remain
in the printed temporary directory. No artifacts are automatically removed.
Use `--output /absolute/new-directory` for a chosen evidence location. An
existing directory is rejected. `--assembler /path/to/assemble_film.py` can
exercise a prior revision that has its normal sibling imports available.
Standard unittest names/options can select individual checks.
