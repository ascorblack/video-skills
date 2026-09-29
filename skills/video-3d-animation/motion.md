# Animation: poses, paths, pushing apart

## Smoothing and blending [3D]

- Since the render runs in several processes and frames are computed in any order, smooth the poses baked: go through all frames without rendering, smooth the raw positions and heading with a Gaussian whose width grows near jumps, and give the page the ready corrections in JSON (we needed about 14,000 frame-characters of them).
- Blend angles only by the short path (`lerpAng`): a plain `lerp` of heading between −π and π turns the character by 2–3 rad in 0.3 s.
- Make any change of pose ("looks at the camera", "holds a card", "at the board") by weight with blending over 0.25–0.6 s: each `if (t > a)` switch gives a jerk of the heading or the hand for one frame.
- Start the next animation block from the position where the previous one ended, not from a point of the path: it was exactly at block boundaries that teleports of 0.7–2.8 m were found.
- Compute the turn to the camera and the start of walking from a smoothed speed (Gaussian about 0.12 s), otherwise in the first frame of movement the heading switches instantly.

## Hands and grip

- [3D] Lead a hand that turns by more than 140° through an intermediate pose ("handshake"): `slerp` of almost opposite quaternions changes the path from frame to frame and flips the hand in a frame.
- [3D] When the arm releases a moving object (the handle of a swinging door), freeze the grip point at the moment of release, otherwise the hand is dragged after the leaf and the arm stretches to 1.45×.
- [Научпоп] Bind the hand on a door handle to the handle itself and lead it together with the handle's turn and with the turn of the door: a hand animated separately slides off the handle within a few frames.
- [Научпоп] Turn the thumb in the order "rotation around the finger axis → bend to the palm → abduction": with another order it stuck out to the side of the handle, and this was noticeable at once.

An object in the hand and an object passing between supports — `body-and-hands.md`.

## Characters in a crowd and the path

- [3D] Make the pushing apart of characters a soft offset from the path: no faster than 0.7 m/s, with decay back, and at a head-on meeting — a step to the right. A hard projection at a head-on meeting changes side in a frame, and the character jumps by 0.3–0.6 m.
- [Научпоп] Separate running figures with a smooth pushing away from each other in every frame, and from furniture — by pushing out of rectangles with a margin greater than the figure's radius (about 0.1 m): otherwise they run through tables and through each other.
- [Научпоп] Compute the figure's path in advance at a rate of 240 samples per second, and take the step of the legs from the distance traveled, not from time: otherwise the legs slide on the floor during acceleration and braking.

## Life between remarks [3D]

- Life between remarks is given by cheap things with a different phase for each character: blinking once per 2.6–3.9 s, breathing, weight shift, diodes that blink during work, a screen that switches on with a strip over 0.35 s.
