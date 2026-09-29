---
name: video-3d-animation
description: Rules of 3D animation for videos in the browser (three.js → frame-by-frame render) and for animating figures with objects — first-person hands and body, sleeve and cuff, contact of the hand with objects and surfaces, blending poses and angles, pushing characters apart, walking without sliding, glow, contact shadows, procedural materials, detectors of intersections and jerks. Use when building, animating or checking a 3D scene, characters, hands, objects in hands or light in a video.
---

# 3D animation

Every rule is taken from the lessons of past videos; the source is in square brackets (legend at the bottom).

## Short rules

1. Keep the hands, torso, legs and shoes in the scene permanently, and do not switch them on when the camera looks down. [3D]
2. Make any change of pose by weight with blending over 0.25–0.6 s, not with an `if (t > a)` switch. [3D]
3. Blend angles only by the short path (`lerpAng`). [3D]
4. Start the next animation block from the position where the previous one ended, not from a point of the path. [3D]
5. Hold an object in the hand through contact: move the character so that the hand lands on the point [3D]; attach the object to the hand, not to the body [Научпоп].
6. Lower the feet 0–6 mm below the surface, not above [Научпоп]; raise the hand on a surface exactly to the fingertip [3D].
7. Take the step of the legs from the distance traveled, not from time. [Научпоп]
8. In a multi-process render smooth the poses baked, in advance, and give the page the ready corrections. [3D]
9. Contact shadows give the most "groundedness" for the minimum price. [3D]
10. Run the detectors of intersections and jerks before the full render, but still look at full-size frames at the moments of actions with your eyes. [3D]

## Details

- `body-and-hands.md` — first-person hands and body, sleeve and cuff, contact with surfaces and furniture.
- `motion.md` — blending poses and angles, animation blocks, pushing apart, "life" between remarks, figures and objects.
- `materials-and-light.md` — glow, shadows, wood, rounding, screens, fonts, spotlight beam.
- `frame-checks.md` — detectors of intersections and jerks, what they do not see.

Rendering and speeding it up — the `video-render` skill; synchronizing the hands in the scene with an interface recording — the `video-ui-capture` skill.

## Sources

- [3D] — lessons of a three-dimensional first-person video in the browser (three.js → frame-by-frame render).
- [Научпоп] — lessons of a video in the style of Soviet popular science and early-70s filmstrips (animation of flat figures and objects).
