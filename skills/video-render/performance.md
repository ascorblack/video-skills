# Render speed and encoding [3D]

The figures in this file are measurements of one 3D video in headless Chrome.

## Measure first

- Before speeding up, check where the time goes: WebGL in headless Chrome already ran on the video card ("hardware gpu" in the log), and the time was eaten by frame capture (12 min) and software encoding (4 min).

## Encoding

- Switch encoding to NVENC (`--gpu`) together with `--video-bitrate 32M`: it sped up 2.6 times (4:03 → 1:32). Without a bitrate limit the stream is 2.6 times heavier (78 Mbit/s), and with it PSNR is 50.9 dB against 50.0 dB for x264 at the same file size.
- Compare the codec's quality on one and the same 2-second piece, shot both ways, by PSNR against the high-bitrate variant: by eye this cannot be proved, and the trial costs 20 seconds.

## Workers

- Do not count on six workers instead of four: frame capture sped up only from 12:03 to 11:40, because the bottleneck is frame copying and CPU, not the number of processes.

## Launching the render

- Launch the render detached from the session (through WMI or an equivalent and with the "detached" variable of the renderer): an ssh disconnect kills a many-minute render.
- Put two versions into one script sequentially, not simultaneously onto one video card: each takes 13 minutes and does not interfere with the other.
- After moving to the render machine, compare the checksums of all files except the recording frames: one forgotten edit costs 13 minutes of re-rendering.
- Run the detectors of intersections and jerks before the full render: a pass costs minutes, a render — from 13 minutes (the `video-3d-animation` skill, `frame-checks.md`).
- If between versions only the sound changes, do not re-render the picture — see `mux-and-delivery.md`.
