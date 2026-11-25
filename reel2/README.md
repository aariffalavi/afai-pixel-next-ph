# Afai Pixel reel: "Stick to the plan"

Based on the structure of the reference reel you supplied (typed hook, intensity-vs-consistency line chart, push-uphill line art, Motivation/Discipline toggles, "1% better every day", logo hit on the impact). Redrawn in a minimal line style for Afai Pixel.

- `afaipixel-stick-to-the-plan.mp4`: 1080x1920, 30 fps, 45.6 s, H.264 + AAC, -14 LUFS. Voice-over plus the reference reel's song.
- `afaipixel-stick-to-the-plan_voice-only.mp4`: the same video with voice only. Use this one on Instagram and add the song with "Use audio" / the audio picker so it's properly licensed.
- `cover.jpg`: suggested cover frame (3.0 s).

| Time | Scene | Voice-over |
|---|---|---|
| 0.0–4.0 | Ruled-paper hook, green highlighter | Forget your mood. Stick to the plan. |
| 4.0–8.1 | Line-art figure pushing a boulder up a slope, one step per beat | Your business won't grow on motivation. It grows on consistency. |
| 8.1–13.3 | Beat drop. Intensity arcs fade, consistency arcs repeat | Big bursts burn out. Small steps, every week, add up. |
| 13.3–26.3 | **Example**: Business A (10 posts then quiet) vs B (2 a week), then a reach chart | Here's an example. ... B is the one customers remember. |
| 26.3–33.0 | **Real video**: live screen recording of afaipixel.com in a line-drawn phone | That's how we work at Afai Pixel. A clear plan, then steady work, week after week. |
| 33.0–36.2 | Toggles: Motivation off, Discipline on | Less motivation. More discipline. |
| 36.2–41.3 | **Comment section**: "Comment PLAN", typed comment posts, heart fills | Want a plan for your business? Comment PLAN below. |
| 41.3–45.6 | "1% better every day." then logo + afaipixel.com on the song's impact | One percent better, every day. |

Suggested pinned comment: "Comment PLAN and we'll get back to you 👇"

## Rebuilding (src/)
1. `python3 vo.py` creates the voice-over (edge-tts, en-GB-RyanNeural) with word timings. Then run `python3 timeline.py`.
2. `node cap.js` records the live site, frame by frame, into `rec/`.
3. `python3 audio.py` extends the song with a seamless 2-bar loop (9.70–14.28 s), ducks it under the voice and normalises the mix.
4. `node render.js range 0 1368` renders frames. Then: `ffmpeg -framerate 30 -i frames/%05d.jpg -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -shortest out.mp4`.
