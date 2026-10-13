"""Generate one cached English lesson MP3 using open-source Piper TTS."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
text_path = root / "assets" / "listening.txt"
model_path = root / "models" / "en_US-lessac-medium.onnx"
output = root / "assets" / "listening.mp3"
paragraphs = [p.strip() for p in text_path.read_text(encoding="utf-8").split("\n\n") if p.strip()]
if not paragraphs:
    raise SystemExit("Lesson text is empty")
with tempfile.TemporaryDirectory() as temporary:
    tmp = Path(temporary)
    wavs = []
    for index, paragraph in enumerate(paragraphs):
        wav = tmp / f"part-{index:02d}.wav"
        subprocess.run(["piper", "--model", str(model_path), "--output_file", str(wav)],
                       input=paragraph + "\n", text=True, check=True)
        wavs.append(wav)
    concat = tmp / "concat.txt"
    concat.write_text("".join(f"file '{wav.as_posix()}'\n" for wav in wavs))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(concat), "-codec:a", "libmp3lame", "-q:a", "3",
                    str(output)], check=True)
print(f"Created {output} ({output.stat().st_size} bytes)")
