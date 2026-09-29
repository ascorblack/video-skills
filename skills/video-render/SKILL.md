---
name: video-render
description: Rules for rendering and optimizing videos made of HTML/browser frames — pitfalls of frame-by-frame rendering with seeking (tweens, CSS animations, transform, aspect-ratio, SVG use, heavy layers), determinism and repeatability, where render time goes, encoding on NVENC with a bitrate, workers, a render detached from the session, muxing in the sound without re-rendering the picture, checking the finished file (ffprobe) and keeping versions. Use when rendering, speeding up, encoding, reassembling or delivering a finished video.
---

# Rendering and optimization

Every rule is taken from the lessons of past videos; the source is in square brackets (legend at the bottom).
Where the sources disagree, both pieces of advice are given, with a note on which case each applies to.

## Short rules

1. The render takes a frame by time, and does not play the animation through: one property — one animation, pulsations — by tweens, not `@keyframes`. [Visual]
2. Put external scripts and fonts into the project, and do not pull them during the render. [Visual] [Popsci]
3. Compute the grain noise from the frame number, not from a random generator [Popsci]; preserve the generator's sequence of random numbers and check that earlier versions reassemble byte for byte the same [Audio].
4. Before speeding up, check where the time goes. [3D]
5. Encoding — on NVENC together with a bitrate limit; compare the codec's quality by PSNR on one piece. [3D]
6. Launch the render detached from the session; two versions — sequentially, not simultaneously onto one video card. [3D]
7. After moving to the render machine, compare the checksums of the files. [3D]
8. Keep the picture and the sound separate: mux the sound in by copying the video stream, without re-encoding the picture. [Video] [Visual] [3D]
9. Before delivery — ffprobe and a check that the page serves exactly the new file. [Video]
10. Do not delete earlier versions. [Video] [Audio]

## Details

- `seek-render.md` — pitfalls of frame-by-frame rendering with seeking, determinism.
- `performance.md` — where the time goes, encoding, workers, launching the render.
- `mux-and-delivery.md` — muxing in the sound, checking the finished file, versions.

## Sources

- [Audio] — archive lessons on sound and voiceover of promo videos and presentations.
- [Video] — archive lessons on video: interface recordings, pace, transitions.
- [Visual] — archive lessons on the visuals of promo videos made of schematic frames (HTML frames → frame-by-frame render with seeking).
- [3D] — lessons of a three-dimensional first-person video in the browser (three.js → frame-by-frame render).
- [Popsci] — lessons of a video in the style of Soviet popular science and early-70s filmstrips.
