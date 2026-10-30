# Stage 2 — references and the style bible [Practice]

Without a visual grammar of its own, the model brings its own, and unrelated videos look related. Naming a style or showing one frame works better than any description.

## References

Kinds, from strongest to weakest:

1. **The person's own past work** — a library nobody else has; the strongest guard against the average look.
2. **A frame of a video they love** — one still says more than a paragraph.
3. **A short clip** — the agent cuts it into a sheet with `ffmpeg` / `video-toolkit/scripts/sheet.sh` and reads motion and pacing from consecutive frames.
4. **A named style** — "Swiss poster", "70s filmstrip" [Popsci], "Linear launch film", "risograph".
5. Where to look when there is nothing yet: launch-video galleries, motion collections, competitors' videos.

For each reference write one line in `production/brand/references/README.md`: what to take from it (palette, type, pacing, camera, texture) and what not to. A reference is a source of decisions, not something to copy: never reproduce another artist's work or a living person's likeness.

An unclear reference is resolved by a question or by **one test frame**, never by rendering 900 frames in a guessed direction [Practice].

## "What would the default version look like?"

Before proposing a direction, write down the version the model would make without guidance — and agree to avoid it. Typical defaults to name and replace:

- a centred gradient title on a dark background; glowing purple-blue gradients;
- glassmorphism cards floating in space; generic particle bursts on every reveal;
- an activity list instead of a story ("zoom in, morph, particles");
- every element moving at one brisk speed on one curve, nothing ever still;
- a whoosh on every cut; a stock riser before every title;
- the same sans-serif everywhere at one weight.

The list goes into `style.md` → "Anti-defaults", with what is done instead.

## Style frames

Render 2–3 **contrasting** directions as stills at the final aspect and resolution, with the real product or subject in them, from the real backbone (so the look is proven feasible, not only imagined). Show them side by side with one line each: what the direction is and what it costs (a Blender shot, a shader, a hand-drawn boil). The person picks one, mixes two, or rejects all — then one more round.

## `style.md` — the style bible (`production/brand/style.md`)

```markdown
# Style bible: <title>

## Direction
One sentence, plus the chosen style frame(s): references/style-a.png

## Palette
Background, ink, one accent that marks what changes, warning colour — hex values. Dark gradients: grain/dither against banding.

## Type
Families (licensed files in assets/fonts, Cyrillic if needed [Popsci]), weights, minimum sizes for this format, line length, how titles enter and leave.

## Motion grammar
- Springs by object class: small UI · panels · camera · titles · characters (values from video-toolkit/seekable-libraries.md)
- Easing for entrances, exits (shorter than entrances), state-to-state moves
- One transition for the whole video [Video] [Visual]; shader transitions only if the whole style is built on them
- Camera: tripod / slow glide / handheld — and where it is still
- Texture: grain, boil rate, film effects (or none)

## Layout
Safe areas of the platform; grid; where captions live; how much is on screen at once
(vertical → bigger type, fewer elements; square → tighter holds; wide → more spatial context).

## Sound palette
Instruments or synth character, SFX family, voice character.

## Anti-defaults
The default version, and what we do instead.
```

The style bible is read by every later stage and by every parallel worker; changes to it are logged in `decisions.md`.

## Formats from one timeline

When the video exists in several aspects (16:9 for the site, 9:16 for the feed), each aspect is its own layout of the same timeline and beat sheet — not a crop of the master. Vertical gets larger type and fewer elements per frame; square tighter holds; wide more context [Practice].
