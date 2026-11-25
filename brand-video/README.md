# Afai Pixel international brand film (work in progress)

Script: 7 scenes, 75.75 s, premium cinematic, digital-only visuals. Rendered in both 9:16 (1080x1920) and 16:9 (1920x1080).

Status: finished. `afaipixel-brand-9x16.mp4` and `afaipixel-brand-16x9.mp4` (75.7 s) with covers `cover-9x16.jpg` and `cover-16x9.jpg`.

## Finish the render (from `brand-video/work/r5`)
```bash
python3 audio.py
ffmpeg -y -i vo.wav -i bed.wav -filter_complex "[1:a]aecho=0.8:0.6:80|160:0.28|0.15[b];[0:a]acompressor=threshold=-20dB:ratio=3:attack=5:release=80,aecho=0.9:0.3:35:0.06[v];[v][b]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -ac 2 mix_norm.wav
node render.js full 1080 1920 &  node render.js full 1920 1080 &  wait
ffmpeg -y -framerate 30 -i frames_1080x1920/%05d.jpg -i mix_norm.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart ../../afaipixel-brand-9x16.mp4
ffmpeg -y -framerate 30 -i frames_1920x1080/%05d.jpg -i mix_norm.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart ../../afaipixel-brand-16x9.mp4
```
`work/rec_case` and `work/r3/frames` are reduced-size copies of the Transfood recording and premium-film frames used inside the phone and the video-editor mock-up.
