# Checking 3D frames [3D]

## Intersection detector

- Write an intersection detector that goes through all frames without rendering and checks the points of characters, hands and sleeves against every furniture box in its local coordinates (tolerance 4–6 mm) and against the planes of screens. 10,650 frames at 60 fps pass in about 25 minutes on CPU, and it finds what the eye on a contact sheet misses.
- For screens count as an error only the points within the thickness of the device (0–1.2 cm behind the glass), not everything behind it, otherwise a character holding a tablet gives hundreds of false findings.
- Check the hand separately against its own cuff: a detector against furniture does not see this, and "skin through the cuff" passed a whole version unnoticed.
- Add a check for clipping at the camera (hand points closer than 9 cm to the eye inside the field of view), otherwise the near plane cutting a sleeve cannot be caught.
- Mark decorative planes (shadows, glares, light strips) with a "not an obstacle" flag, otherwise the detector takes them for screens.
- Take the vertices of a skinned mesh only after `skeleton.update()`, otherwise hundreds of false intersections.

## Jerk detector

- The jerk detector raises a flag when the per-frame step in position or turn of the camera, hands, torsos, heads and mittens is greater than the threshold (3 cm or 0.15 rad) and 5 times greater than the median of its neighbors. It also marks arm stretch of more than 8 %. On contact sheets where everything looked normal it found 1453 jerks.

## When and with what to supplement

- Run the detector before the full render: a pass costs minutes, a render — from 13 minutes, and every finding before the render saves a re-render.
- Detectors do not see what is not an intersection or a jump: the interface being covered by a character, unreadable text, ugly light, an object hanging without contact and a wrong order of actions. Therefore still look at full-size frames at the moments of actions with your eyes.
- Even after a clean detector, look at full-size frames of the finished file at the moments of actions: some defects are visible only at a certain turn of the hand and in a single frame.
