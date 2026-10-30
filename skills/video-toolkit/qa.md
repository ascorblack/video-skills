# Checking the video: automatic checks and the critic [Toolkit] [Practice]

The checks below catch what can be measured. They do not replace looking: full-size frames at every join and every action, and the whole video played through once with sound [Video] [3D].

## `scripts/qa.sh <video> [out-dir]`

One run, one folder of evidence:

| Output | What to look for |
|---|---|
| `summary.txt` | codec, size, fps, pixel format, video and audio length, loudness, counts of black and frozen segments |
| `probe.json` | the full ffprobe, for anything the summary does not show |
| `detect.log` | black segments ≥ 0.1 s (`blackdetect`). Expected: a fade to black planned in the shot table. Not expected: black at the very start or end, or a black flash at a join — a frame captured before the scene was ready |
| `detect.log` | frozen segments ≥ 0.5 s (`freezedetect`). Holds for reading are expected [Visual]; a freeze in the middle of an animated shot is a library that did not seek, an asset that had not loaded, or a transition fed with stills |
| `loudness.log` | EBU R128 integrated loudness, LRA, true peak — measured on the encoded file, because encoding raises peaks [Audio]. Targets — `video-audio`, `mixing.md` |
| `sheet.jpg` | 16 frames evenly over the video: the overall rhythm, a scene that never appeared, a frame in the wrong style |
| `first.png`, `last.png` | the opening and closing frames at full size: not black, not transparent, not half-loaded |

Then compare with the plan:

- size and fps as ordered (a vertical short is 1080×1920, not 1920×1080 rotated);
- `yuv420p` for anything that will be played on phones and in browsers;
- the audio track present and as long as the video (a difference of tens of milliseconds is the encoder's padding [Audio]);
- the video length equals the shot table's total.

## `scripts/compare-renders.sh <a> <b>`

Seek consistency: two renders of the same source from clean processes must decode to identical frames. The script first compares size, frame rate, frame count, duration and the presentation time of every frame (`TIMING DIFFERS` or `FRAME TIMES DIFFER` stops it), then checksums of decoded frames, lists the differing frame numbers and the minimum PSNR.

- `IDENTICAL` — the scene is deterministic.
- A handful of frames far below 50 dB — a leak: wall clock, unseeded randomness, a library with its own ticker, an asset that loads late. Look at the first listed frame; the frames after it inside the same GOP differ only because the encoder propagates the change.
- Every frame slightly different, PSNR above ~50 dB — usually a hardware encoder that is not bit-exact between runs; repeat with the same software encoder settings or render PNG frames to tell it from a leak.
- Run it once with the frames taken in a different order (another number of workers, or a range starting mid-shot): a state that accumulates from frame to frame passes the first comparison and fails this one.

## The critic: looking at frames with teeth [Practice]

An agent cannot watch a video; it can look at frames. Every viral code-made clip of the last months went through rounds of looking at its own frames and fixing them; it is the step most often skipped. Never report a video as done without having read the sheets.

**Evidence, not playback.** Do not re-watch the full export ten times; make sheets that answer a question:

```bash
scripts/sheet.sh out/v003.mp4 "0:62:2"                 # overview: every 2 s
scripts/sheet.sh out/v003.mp4 "11.8:12.4"              # strip: every frame around the join at 12 s
WIDTH=0 CROP=1080:420:0:1300 scripts/sheet.sh out/v003.mp4 "3,7.5,15"   # captions at native size
```

Every cell carries `t=` and the frame number, so a finding goes straight back to the timeline.

**Budget per pass** (from ClaudeAnimationBase's guide):

- at least one sheet per shot: its first and last frame and a few in between;
- a strip for every key motion, hit and transition — motion reads only across consecutive frames;
- a native-size crop of every face, caption and UI detail that carries the story;
- the junctions: boundary −0.1 s, boundary, +0.05 s, +0.3 s.

**What to hunt for** — write it down as a list of findings with `t=`, never as "looks good":

| Defect | Where it shows |
|---|---|
| Overlapping or clipped text, text in the safe-area margin, a corner label nobody asked for | overview sheet, native crops |
| Elements that **slide** at constant speed instead of easing in and settling | strips |
| Blurry type: text scaled up as a bitmap instead of rendered at size | native crops |
| A **dead beat**: a stretch where nothing changes and nothing is being read | overview sheet against the beat sheet |
| Two reads at once; a read that leaves before it can be finished | strips against the timing (`characters.md`, Timing for the viewer) |
| Twinning: parts or characters moving in unison | strips |
| A stutter or jump at a loop point or a join (state changes that are not part of the cut) | junction strips |
| Effect before its cause at a dissolve [Visual] | junction strips |
| Fake product UI, invented data, wrong figures | native crops against the asset list |
| Off-model characters | samples against the model sheet |
| Flicker of denoised or boiled textures that should be still | strips of a "static" moment |

**Stop criterion.** Fix, re-render the affected range, make the same sheets again. Stop when a full pass finds nothing — not after a fixed number of rounds. A second opinion helps: give another model (or a person) the same sheets and the list above, without your own conclusions.

**The blind test for sound** [Practice]: close your eyes — listen to the track alone. If the sound has no shape without the picture (no build, no hits, no release), the sound design is not finished. An agent cannot do this itself: give the person a clip and ask.

## Single commands, when a script is too much

```bash
# what the file is
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,pix_fmt -of json out/final.mp4
# one frame every 2 s for a quick look
ffmpeg -hide_banner -i out/final.mp4 -vf "fps=1/2,scale=320:-2" out/qa/sample_%03d.jpg
# three frames around a join at 12.4 s: end of shot, middle of the transition, start of the next [Visual]
for t in 12.0 12.4 12.8; do ffmpeg -hide_banner -loglevel error -ss $t -i out/final.mp4 -frames:v 1 out/qa/join_$t.png; done
# loudness and true peak of the encoded file
ffmpeg -hide_banner -nostats -i out/final.mp4 -vn -af ebur128=peak=true -f null - 2>&1 | tail -12
```

## What the automatic checks do not see

Clipped or unreadable text, a line through a block, a wrong figure, a caption that leaves before it is read, a cursor hesitating over the wrong button, out-of-sync speech, the effect before its cause at a join, a GPU texture that came out wrong only in some frames. These are checked by eye on full-size frames and on playback, and the rules for each are in `video-design`, `video-ui-capture`, `video-3d-animation` and `video-audio`. For WebGL scenes look at frames of the exported file, not at the interactive preview.
