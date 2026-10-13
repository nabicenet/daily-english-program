# Daily English Program

Mobile-first English lessons with free, **pre-generated** Piper AI speech (no text-to-speech model running on iPhone).

## How the audio system works

Each dated lesson page loads its own immutable `assets/audio/YYYY-MM-DD/manifest.json`. The root `assets/audio-manifest.json` is the latest active lesson input for the generator. Every entry contains an `id`, `section`, CSS `selector`, and `text`. GitHub Actions runs `scripts/generate_audio.py` to generate one MP3 per item under `assets/audio/<lesson-date>/<id>.mp3`. The website downloads MP3s from the repository only when requested. A shared bottom player controls speed, pause, stop and repeat. Safari native speech remains available as backup.

Current lesson: **2026-09-21 — Reporting Bugs and Test Results in MR Studio**. Its status remains **in progress**. Finishing the page alone never marks the lesson complete; completion requires explicit confirmation in ChatGPT.

## Creating the next lesson

1. **Wait for explicit completion** of the previous lesson ("çalışıldı", "ders bitti" etc.).
2. Prepare the next lesson in the same six-section format: Listening, Vocabulary, Shadowing, Speaking, Writing, Quick Review. Preserve the finished lesson in the archive before replacing the homepage.
3. Create a permanent lesson page `lessons/YYYY-MM-DD.html`, linked back to `../index.html`. Add a new entry to `lessons/catalog.json`, keep entries sorted newest-first, and set `current` to the active lesson date. Never replace an older lesson page.\n4. Update `assets/audio-manifest.json`: change `lesson` to the new date and replace all audio `items` with the matching text/sections/selectors. Use unique, stable IDs (letters/numbers/dashes/underscores).
5. Copy the lesson-specific manifest to `assets/audio/YYYY-MM-DD/manifest.json`, and make the dated lesson page load this immutable URL (not the ever-changing latest manifest). Keep shared audio player and controls.
6. Pushing a changed manifest or generation script triggers the **Generate free AI lesson audio** workflow. Check Actions and validate that each referenced MP3 exists in `assets/audio/<date>/`.
7. On iPhone Safari, verify the full Listening audio and at least one Shadowing, Vocabulary and Speaking item. GitHub Pages publication can lag behind the GitHub repository.

## Troubleshooting

- Workflow diagnostics are committed to `assets/audio-build-log.txt`; follow the most recent log. A successful run ends with `Generated N MP3 files for lesson YYYY-MM-DD`.
- An MP3 may exist on GitHub before Pages redeploys. The shared player loads the MP3 directly from `raw.githubusercontent.com`.
- Safari requires a tap before audio playback begins. The page will not autoplay.
- HTML, manifest and MP3 files are **public** in this GitHub Pages site. Do not include private data or API keys.

## Dependencies / license

Audio uses Piper TTS with the `en_US-lessac-medium` voice fetched from the public Piper voice collection, and FFmpeg on a GitHub Actions Ubuntu runner. Check individual model license terms before substituting voices.

## Archive navigation

`index.html` is the permanent lesson library homepage. Its dated, searchable menu is populated from `lessons/catalog.json`, which records each lesson's date, title, status, and permanent URL. Every lesson lives in `lessons/YYYY-MM-DD.html` and points back to the index page. When a new lesson is added, retain previous dated pages and audio clips, update the previous lesson's catalog status to `completed` only after explicit user confirmation, and set `catalog.current` to the active lesson. No lessons are generated merely by changing the homepage.
