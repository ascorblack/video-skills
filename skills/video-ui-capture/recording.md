# How to shoot the interface

## Frame-by-frame capture

- [Видео] Shoot only the real interface, frame by frame. The browser is driven by virtual time: advanced a frame, took a frame. Then 60 fps are honest under any load of the machine, and a repeated take matches the previous one frame for frame. A real-time screen recording tears frames and "drifts".
- [3D] Shoot the interface frame by frame in headless Chrome in a deterministic mode (`beginFrame` and virtual time of 1/60 s per frame): a 2560×1440 screencast gives about 23 fps with gaps, and frame-by-frame capture — exactly 60 frames per second of application time.

## Stand and data

- [Видео] The data in the frame — only invented, from the stand. No live projects, correspondence, names and paths of the owner. Before recording, page through every screen with your eyes: on a frame with such litter the video can be thrown away.
- [3D] Shoot only a demo stand where all API answers are supplied by a stub with invented data, so that nothing from a live installation is guaranteed to get into the frame.
- [Видео] The stand must be consistent with itself. If one screen shows that the tool is installed and logged in, the other screen that reads the same fact must say the same thing. A contradiction between two screens the viewer will notice before the author.

## Cursor

- [Видео] The cursor must go to the target, not past it. Hovering before a click — on the button that will be pressed. A cursor lingering on "Deny" before pressing "Allow" reads as doubt.
- [3D] Draw the cursor on the page itself from the same events that go into the application: then the click lands exactly where the viewer sees, and the cursor position is later restored from the frames to pixel accuracy.

## Marks and margins [Видео]

- Put marks right during recording ("click", "result", "answer arrived"). Hang captions and the camera on marks, not on seconds. Then a reshoot or speeding up of a take shifts everything together, and nothing drifts apart.
- Give margins of silence at the start and at the end of a take (a second to four without actions). Cutting the excess in editing is easy; shooting the missing tail afterward is not.

For a version in another language the length of the intro and the tail must match the original [3D] — see `languages-and-sync.md`.

## Checking a take [Видео]

- Look at every take after recording with a sheet of frames (a grid of 4–6 frames). Check: the action reached the result, the toast or the new row appeared, nothing is cropped, no other people's data.

## Recorder [Видео]

- The recorder must not wait endlessly. Any wait — with a timeout. Input that the browser will confirm later than one frame, move to the next frame, and do not hold the clock.
- Kill background processes by pid. A wait "while process X is alive" through a search by command line finds itself and never ends. Better to wait for a result file or an exit code.
