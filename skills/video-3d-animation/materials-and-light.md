# Textures and light

## Glow and post-processing [3D]

- Make the glow selective: an ordinary frame, then only the glowing materials, and everything else black (furniture blocks the glow), blur at 1/2 and 1/4 resolution and additive overlay, and without screens and text, otherwise the interface is blurred. The frame-capture time barely grew (11:49 versus 11:29).
- Do not take a ready post-processing composer if the screens have `toneMapped: false`: the tone mapping of the output pass will lie over the whole frame, and the white interface will turn gray and drift together with the scene's exposure.
- Make the spotlight beam in the air a cone with a shader (brightness by Fresnel, falloff toward the floor, multiplication by the source's strength) with an intensity of about 0.07, otherwise the frame turns murky.

## Groundedness and materials [3D]

- The most "groundedness" for the minimum price is given by contact shadows — a soft dark disc under the furniture and under each character, lightening as they rise. Without them characters far from light sources hover.
- Build procedural wood from the rings of a log: arcs, an uneven ring spacing, narrow late wood, long fibers and a seam between boards. A single sinusoid gives a "striped oilcloth", which is visible at first glance.
- Round the edges by 0.5–1.2 cm on tabletops, monitor frames and stands: the light lays a highlight on the edge, and realism grows noticeably without changing the pipeline.

## Screens and text in the scene

- [3D] Lay a very faint diagonal glare over a switched-off screen (4–5 % with additive blending), otherwise instead of glass the viewer sees a black rectangle in the air.
- [3D] For Cyrillic connect separate font files with `unicode-range` and pass a Cyrillic sample to `document.fonts.load`: the Latin subset silently goes to the system font, and the canvas draws someone else's.
- [Научпоп] Keep the canvases that go as a texture into the 3D frame in CPU memory: a texture from a canvas in video card memory came in torn or black in some frames during frame capture.
