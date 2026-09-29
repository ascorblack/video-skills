# Interface recording in the video

## Trimming and speeding up

- [Видео] A recording longer than the slide — trim the window, then speed up. The window — from the first action to the visible result. If the window is still longer, play it evenly faster, but no more than twofold. Throwing out a click or its result is not allowed.
- [3D] Show screen recordings whole and up to the result of the action: a zoom into buttons and a freeze frame right after a click the viewer notices and does not accept.
- [3D] Cut the recording frames from RGB (`format=rgb24,crop=…`): in yuv420 ffmpeg rounds an odd offset to an even one, and the cut-out screen gets a white line along the edge.

## Push-ins and captions [Видео]

- A camera push-in — onto a whole block of the interface, not onto the middle. Lay the edge of the frame on the boundary of a column or window. Text cut in half looks like a defect. A form into which something is entered must come into the frame entirely, together with the button.
- In the frame — an honest note on the source: the real application, demo data.

## A program screen in a stylized frame [Научпоп]

- Shoot the program screen in close-up strictly head-on so that it occupies 85–90 % of the frame width: at an angle and smaller the interface text stops being readable.
- Lead the cursor by key points with smooth acceleration and braking and an arc of about 8 % of the length of the movement: a straight even motion looks mechanical.
- Take the interface captions from the program's real localization: invented captions on a screen familiar to the viewer jar the eye more than invented data.
- Vignette no darker than 80 % brightness in the corners and fine grain — so as not to hide buttons in the corners and not to eat small text (the `video-design` skill, `retro-style.md`).

## Where the sources disagree: real or drawn interface

- [Видео] — promos and presentations about a program: shoot only the real interface, frame by frame; do not draw interface mockups instead of recordings — a drawn screen always lies somewhere, and trust in the video falls as a whole.
- [Научпоп] — a stylized video in the manner of 70s educational film: the interface in the frame was redrawn at the video's resolution and in every frame, because in an inserted screen recording at 12 frames per second the cursor "teleports", and the viewer notices this. The captions were taken from the program's real localization.

## Where the sources disagree: how to lead the cursor

- [3D] — recordings shot frame by frame from the real application: the cursor is drawn on the page from the same events that go into the application.
- [Научпоп] — a drawn interface: the cursor is led by key points with acceleration, braking and an arc of about 8 % of the length of the movement.
