# "Stick to the plan": motivational reel (minimal line style)

`stick-to-the-plan-reel.mp4`: 1080x1920, 30 fps, 27.9 s, H.264 + AAC, -14 LUFS. No voice-over and no branding. Music starts right on the drop of the reference reel's song (its best, high-energy part) and stays there, looping that section seamlessly, then ends on the song's final hit at 26.2 s. Every scene change and text pop is timed to the beat. `cover.jpg` is a suggested cover frame.

| Time | Scene |
|---|---|
| 0.0–4.1 | (music opens on the drop) "Forget your mood. / Stick to the plan." on ruled lines, highlighter word by word |
| 4.1–8.1 | Line figure pushing a boulder uphill, one step per beat. "~~Not motivation.~~ Consistency." |
| 8.1–11.5 | Intensity arcs burn out, consistency arcs repeat |
| 11.5–17.2 | **Example**: Person A (7 workouts in week 1, then quits) vs Person B (3 a week, every week), then the 12-week progress chart. "B wins." |
| 17.2–20.1 | Runner on a road. "Do it tired. Do it alone. Do it scared. Keep going." |
| 20.1–22.4 | Toggles: Motivation off, Discipline on |
| 22.4–26.2 | **Comment section**: "Sticking to the plan? Comment PLAN". The comment is typed, posted and liked |
| 26.2–27.9 | On the final hit: "1% better every day." |

Instagram tip: to make sure the music isn't muted, upload with the original audio, or tap "Use audio" on the reference reel and pick the same song.

## Rebuilding (src/)
1. Put the reference song in `src/song_ref.m4a` (not committed), then run `python3 audio.py`.
2. `node render.js range 0 837` renders the frames from `reel.html` (or `node render.js preview 3.4 12.0` for stills).
3. `ffmpeg -framerate 30 -i frames/%05d.jpg -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -shortest out.mp4`
