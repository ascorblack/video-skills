# Stylization in the manner of Soviet popular science and filmstrips [Popsci]

Everything in this file is from a video in the style of popular-science and educational film of the early 70s: flat appliqué, a built set, program screens in the frame, a voice "from the archive". Each item was checked on the finished video or was redone because the viewer noticed it.

## Flat picture and style

- Keep the palette restrained: saturation about 14 % lower than the original, a slightly warm print (red ×1.03, blue ×0.94, black lifted by 1 %). Pure saturated colors read as a postcard; such a version was returned with the note "too colorful".
- Set the era with a recognizable interior detail, for example an institution wall in two paints (an oil-paint panel up to 1.5 m, a dark stripe, whitewash above): one such detail dates a frame more reliably than any filter.
- Put 4–6 household objects in the background (a clock, an educational chart, a radiator, a desk lamp, a chalk board): an empty background also looks like a postcard, and it was asked to be "worked out".
- Set titles in two typefaces — a narrow grotesque in capitals with letter-spacing for headings and a school serif in italics for explanations: one modern typeface at once gives away a fake.
- Embed fonts with Cyrillic into the project as files: they may be absent on the render machine, and the titles will quietly be substituted with someone else's font.
- The chapter title — as a small plate in the bottom corner for 3–4 seconds: a large caption covers the very subject of the showing.
- Program screens in the frame — in the `video-ui-capture` skill, file `framing.md`.

## Film effects

- Do not shake the camera and do not sway the frame: shake hinders reading the screens, in educational film the camera stands on a tripod.
- Make the grain fine: a swing of about ±1.4 % of brightness, grain of 2×2 pixels, new in every frame. Large or strong grain eats small text on the screens.
- Compute the grain noise from the frame number, not from a random generator: then a repeated render and a render on another machine give the same frame.
- Make the vignette no darker than 80 % brightness in the corners: a darker one hides the corners of the screen, where the interface has buttons and menus.
- Apply color, vignette and grain in one pass over the finished frame, and the grain — after conversion to the output color space, otherwise tone mapping flattens the grain in the dark areas.
- Do not add brightness flicker and scratches: next to the ban on shake they read as the same defect, not as "film".
- Cuts within a chapter — into the pauses of the narrator's speech; chapters — with a cross-dissolve of 0.5–1 s after the hold, not an iris (see `pacing-and-transitions.md`).

The sound part of the style (archive voice, ether interference) — in the `video-audio` skill, file `archive-voice.md`.
