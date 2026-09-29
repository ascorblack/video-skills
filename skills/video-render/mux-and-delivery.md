# Muxing in the sound and delivering the finished file

## Sound separate from the picture

- [Видео] Keep the picture and the sound separate. Mux the sound into the finished video without re-encoding the picture. A new track must not require a new render.
- [Визуал] The sound is muxed in separately, without re-rendering the picture: the video stream is copied, the track is replaced. Before muxing, compare the timecodes of the frame's events with the drops of the track and write the sound engineer the actual times if the discrepancy is more than a second. Do not touch the loudness, after muxing check the peak and the shift.
- [3D] If between versions only the sound changes, do not re-render the picture, but lay the track under the finished video by copying the stream (`-c:v copy`) — this is seconds instead of 13 minutes.
- [Звук] Lossy encoding raises peaks to 2–3 dB above the source: measure the true peak on the finished file. The encoder's service silence lengthens the file by tens of milliseconds (the `video-audio` skill, `mixing.md`).

## Checking before delivery [Видео]

- ffprobe: resolution, fps, duration, presence and length of the sound track.
- A snapshot of each slide at 70 % of its length, a sheet of frames by eye. Then an independent check by another model on the same frames: line breaks, cropping, overlaps, small text.
- Check that the page on which the video lies serves exactly the new file. Open it from the address from which it will be watched.
- [3D] Even after a clean detector, look at full-size frames of the finished file at the moments of actions.

## Versions

- [Видео] Do not delete earlier versions — only rename them, so that it is clear which is which.
- [Звук] Do not delete or replace earlier versions: every new version is a new file.
