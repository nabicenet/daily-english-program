"""Reusable Piper voice renderer for one lesson audio manifest.

Each manifest item produces its own cached MP3 under assets/audio/<lesson>/.
Keep the manifest's ids stable: the web player uses them as file names.
"""
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "assets/audio-manifest.json").read_text(encoding="utf-8"))
lesson = manifest["lesson"]
outdir = ROOT / "assets/audio" / lesson
outdir.mkdir(parents=True, exist_ok=True)
model = ROOT / "models/en_US-lessac-medium.onnx"
config = ROOT / "models/en_US-lessac-medium.onnx.json"
for path in (model, config):
    if not path.is_file() or path.stat().st_size < 1000:
        raise SystemExit(f"Invalid Piper model file: {path}")
items = manifest["items"]
if not items or len({x["id"] for x in items}) != len(items):
    raise SystemExit("Manifest missing items or contains duplicate ids")
with tempfile.TemporaryDirectory() as temp:
    for index, item in enumerate(items, 1):
        ident = item["id"]
        if not ident or not all(c.isalnum() or c in "_-" for c in ident):
            raise SystemExit(f"Invalid audio id: {ident}")
        phrase = item["text"].strip()
        if not phrase:
            raise SystemExit(f"Empty text for {ident}")
        wav = Path(temp) / f"{ident}.wav"
        mp3 = outdir / f"{ident}.mp3"
        print(f"[{index}/{len(items)}] Generating {ident}", flush=True)
        subprocess.run(["piper", "--model", str(model), "--config", str(config),
                        "--output_file", str(wav)], input=phrase + "\n", text=True, check=True)
        if not wav.exists() or wav.stat().st_size < 1000:
            raise SystemExit(f"No WAV created for {ident}")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
                        "-codec:a", "libmp3lame", "-q:a", "4", str(mp3)], check=True)
        if not mp3.exists() or mp3.stat().st_size < 1000:
            raise SystemExit(f"No MP3 created for {ident}")
print(f"Generated {len(items)} MP3 files for lesson {lesson}", flush=True)
