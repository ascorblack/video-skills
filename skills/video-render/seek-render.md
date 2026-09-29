# Frame-by-frame rendering with seeking

## Pitfalls [Visual]

The render takes a frame by time, and does not play the animation through. Therefore:

- **Several animations of one property in a row may not survive seeking**: only the first is applied. Make a path of several segments with one proxy tween that computes the position from progress and writes a separate property (for example, `translate`) that does not conflict with scale.
- **Disable the "lazy" first render of tweens** if the engine has one: otherwise the values do not have time to be applied by the moment of the frame snapshot.
- **Do not mix an element's CSS transform and an animation of the same property.** Move a rotation or shift from the layout into the initial state of the animation.
- **CSS animations (`@keyframes`) in frame-by-frame rendering are not controlled by the video's time.** Make pulsations and blinking with tweens with a finite number of repeats.
- A container with `aspect-ratio` from which children overflow grows along with them unless `min-height: 0` is set. Otherwise the marks in percent drift.
- An SVG symbol via `<use>` is drawn from zero, not from its own `viewBox`. Set `x/y/width/height` explicitly, otherwise the sign slides off.
- Keep heavy layers (blur, gradients, `clip-path`) in separate subcompositions per scene: dozens of such layers in one file give black frames at capture.
- Put external scripts into the project, and do not pull them from the network during the render.

## Frame capture and resources

- [Popsci] Keep the canvases that go as a texture into the 3D frame in CPU memory: a texture from a canvas in video card memory came in torn or black in some frames during frame capture.
- [Popsci] Embed fonts with Cyrillic into the project as files: they may be absent on the render machine, and the titles will quietly be substituted with someone else's font.
- [3D] For Cyrillic connect separate font files with `unicode-range` and pass a Cyrillic sample to `document.fonts.load`: the Latin subset silently goes to the system font.

## Determinism and repeatability

- [3D] Since the render runs in several processes and frames are computed in any order, smooth the poses baked: go through all frames without rendering, smooth and give the page the ready corrections in JSON (in detail — the `video-3d-animation` skill, `motion.md`).
- [Popsci] Compute the grain noise from the frame number, not from a random generator: then a repeated render and a render on another machine give the same frame.
- [Audio] If the generation depends on random numbers, preserve their sequence; after any edits of the generator, check that earlier versions reassemble byte for byte the same.
- [Video] With frame-by-frame browser capture by virtual time a repeated take matches the previous one frame for frame (the `video-ui-capture` skill).
