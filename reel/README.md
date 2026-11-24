# Afai Pixel promo reel

`afaipixel-reel.mp4`: 1080x1920 vertical, 30 fps, 54.4 s, H.264 + AAC. Ready for Instagram Reels, TikTok and YouTube Shorts. `cover.jpg` is a designed cover (web elements, a WORLDWIDE badge, the real site in a browser and a phone). Upload it as the reel cover.

## Structure
| Time | Scene | Voice-over |
|---|---|---|
| 0.0–4.3 | Hook ("HEY!") | Hey! Is your website actually bringing you customers? |
| 4.3–11.1 | Original logo reveal + services + worldwide | Meet Afai Pixel. Web design, branding and digital marketing for businesses worldwide. |
| 11.1–17.3 | Real afaipixel.com homepage in a phone | This is the real site. Fast, clean, and built to turn visitors into enquiries. |
| 17.3–25.7 | Real services section scrolling | Websites, logos, branding, social media, Google Ads, hosting and custom systems. All under one roof. |
| 25.7–38.7 | Example: Global Supermarket EU case study (real page) | Here's a real example... we still run their marketing today. |
| 38.7–42.5 | Google reviews (5.0, 25 reviews) | Rated five stars from twenty-five Google reviews. |
| 42.5–49.4 | Comment section ("Comment WEBSITE") | Want a free quote? Comment WEBSITE below, and we'll reply within one working day. |
| 49.4–54.4 | Logo outro + afaipixel.com | Afai Pixel. Make your ideas a reality. |

Suggested pinned comment: "Comment WEBSITE and we'll send you a free, no-obligation quote 👇"

## Rebuilding (src/)
1. `node cap.js` records the live site frame by frame (mobile viewport; the cookie banner and the audit popup are dismissed).
2. `python3 vo.py` creates the voice-over (edge-tts, en-GB-RyanNeural) and word timings; `python3 timeline.py` builds `timeline.json`.
3. `python3 audio.py` synthesises the music bed and sound effects and mixes them with the voice-over.
4. `node render.js` renders `reel.html` into frames, then encode the frames with ffmpeg.
5. `node shotcover.js` renders `cover.html` into the cover image.
