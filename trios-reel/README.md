# Top 10 Trios in Football History: chalkboard reel

`top10-trios-reel.mp4`: 1080x1920 vertical, 30 fps, 96.9 s, H.264 + AAC (-15 LUFS). For Instagram Reels, TikTok and YouTube Shorts. `cover.jpg` is a suggested cover (the #1 MSN frame).

**Music:** an original drift-phonk beat, synthesised in `src/phonk.py` at 140 BPM in F# minor: cowbell riff, distorted 808 with slides, hard kick and clap, triplet hat rolls. A filtered intro under the hook builds with a riser, and the beat drops on #10. It's royalty-free (no samples), and it's ducked under the voice-over.

Everything is drawn in chalk on a green board: hand-drawn player busts (with hairstyle, beard and kit colours for each player), a mini pitch with the trio's passing triangle, a stat box, and word-by-word captions. An eraser wipes the board between scenes.

## Countdown
| # | Trio | Board stat |
|---|---|---|
| 10 | Henry, Bergkamp, Pires (Arsenal 2003–04) | 26W 12D 0L: The Invincibles |
| 9 | Ronaldo, Rivaldo, Ronaldinho (Brazil 2002) | 7 games, 7 wins; 15 goals from the 3 R's |
| 8 | Best, Law, Charlton (Man United 1960s) | 3 Ballon d'Ors; European Cup 1968 |
| 7 | Xavi, Iniesta, Busquets (Barça & Spain) | 2009 sextuple; 2010 World Cup |
| 6 | Salah, Firmino, Mané (Liverpool) | UCL 2019; Premier League 2020 |
| 5 | Messi, Eto'o, Henry (Barça 2008–09) | 38 + 36 + 26 = 100 goals |
| 4 | Gullit, Van Basten, Rijkaard (AC Milan) | European Cups 1989 & 1990 |
| 3 | Di Stéfano, Puskás, Gento (Real Madrid) | 1960 final 7–3 (Puskás 4, Di Stéfano 3) |
| 2 | Bale, Benzema, Cristiano (Real Madrid) | 4 Champions Leagues: 2014, 2016, 2017, 2018 |
| 1 | Messi, Suárez, Neymar (Barça) | 122 goals in 2014–15 + the treble |

## Example (chalkboard replay)
2015 Champions League final, Berlin: Messi drives and shoots, Buffon parries, Suárez scores (2–1, 68'). Then Pedro squares for Neymar in stoppage time (3–1), and Barça win the treble.

## Comment section
"YOUR #1 TRIO?" with a chalk comment panel (sample comments), a comment box that types itself and a bouncing arrow. The voice-over says "Comment your number one trio below."
Suggested pinned comment: "Who's YOUR #1 trio? Drop it below 👇 Wrong answers only… or MSN."

## Rebuilding (src/)
1. `python3 vo.py`: voice-over (edge-tts, en-GB-RyanNeural) with word timings; long pauses are tightened.
2. `python3 build_timeline.py`: builds the scene timing, captions and the marks used to sync drawings to the words.
3. `python3 audio.py`: phonk bed (`phonk.py`), chalk/eraser/whistle/crowd SFX and the VO mix → `mix.wav`.
4. `node render.js range 0 2908` (split into parallel ranges if you like) renders frames. `node render.js preview 12.5 70` writes test stills.
5. Encode:
   `ffmpeg -framerate 30 -i frames/%05d.jpg -i mix.wav -af loudnorm=I=-14:TP=-1 -c:v libx264 -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest ../top10-trios-reel.mp4`

Fonts: Cabin Sketch, Permanent Marker, Caveat (SIL OFL, via @fontsource).
