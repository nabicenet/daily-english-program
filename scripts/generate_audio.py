"""Produce one MP3 in CI; Safari only downloads the final small audio file."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
text_path = root / "assets/listening.txt"
model = root / "models/en_US-lessac-medium.onnx"
config = root / "models/en_US-lessac-medium.onnx.json"
output = root / "assets/listening.mp3"
text = text_path.read_text(encoding="utf-8").strip()
if not text:
    raise SystemExit("Listening text is empty")
for path in (model, config):
    if not path.is_file() or path.stat().st_size < 1000:
        raise SystemExit(f"Missing/invalid model file: {path}")
with tempfile.TemporaryDirectory() as directory:
    wav = Path(directory) / "lesson.wav"
    print("Synthesizing AI speech...", flush=True)
    subprocess.run(
        ["piper", "--model", str(model), "--config", str(config), "--output_file", str(wav)],
        input=text + "\n", text=True, check=True,
    )
    if not wav.exists() or wav.stat().st_size < 1000:
        raise SystemExit("Piper did not produce a valid WAV")
    print(f"WAV created: {wav.stat().st_size} bytes", flush=True)
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "warning", "-i", str(wav),
         "-codec:a", "libmp3lame", "-q:a", "3", str(output)],
        check=True,
    )
if not output.exists() or output.stat().st_size < 1000:
    raise SystemExit("MP3 was not generated")
print(f"Created MP3: {output.stat().st_size} bytes", flush=True)
