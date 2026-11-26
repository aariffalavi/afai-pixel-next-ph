# Gordon vs Diomande reel

`../gordon-vs-diomande-reel.mp4`: 1080x1920 vertical, 30 fps, 83 s, H.264 + AAC. `../gordon-vs-diomande-cover.jpg` is a suggested cover frame.

| Time | Scene | Voice-over |
|---|---|---|
| 0–8 | Hook: Gordon vs Diomande (3D, centre circle) | Anthony Gordon versus Yan Diomande... who is the better winger right now? |
| 8–15 | Gordon card (25, England, Barcelona, €70m) | Twenty-five, English, and a seventy-million euro signing for Barcelona. |
| 15–21 | Diomande card (20, Ivory Coast, Real Madrid, Aug 2026) | Just twenty, Ivorian, and already scoring for Real Madrid. |
| 21–28 | Gordon goal 1: off the bench, 6–1 vs Alavés | |
| 28–38 | Gordon goals 2 & 3: rebounds, 4–1 at Sabah (30', 50') | |
| 38–45 | Diomande goal 1: cross-shot, 1–0 vs Villarreal (62') | |
| 45–50 | Diomande goal 2: late volley, 4–1 vs RB Leipzig (87') | |
| 50–56 | Diomande goal 3: volley, 3–0 at Racing (Goal of the Month nominee) | |
| 56–68 | Example: same chance, two styles | |
| 68–73 | Last 3 goals compared | |
| 73–80 | Comment section: "Comment GORDON or DIOMANDE" | |
| 80–83 | Follow outro + sources | |

All match scenes are illustrative 3D recreations (labelled on screen), not broadcast footage. Music is an original phonk beat synthesised in `audio.py` (no copyrighted samples).

## Rebuild
1. `npm i` (three.js), copy Inter + Noto Color Emoji fonts into `fonts/`.
2. `python3 vo.py` (edge-tts, en-GB-RyanNeural) then `python3 build_tl.py`.
3. `node render.js range 0 2498` (can be split across processes) → `frames/`.
4. `python3 audio.py` → `mix.wav` (uses `goals.json` for crowd roars).
5. `ffmpeg -framerate 30 -i frames/%05d.jpg -i mix.wav -c:v libx264 -crf 23 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest ../gordon-vs-diomande-reel.mp4`
