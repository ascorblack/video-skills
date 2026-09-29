# First-person hands and body, contact with objects

## Sleeve, cuff, wrist [3D]

- Make the forearm sleeve a bending tube: a Bézier curve from the elbow along the forearm axis to the cuff along the hand axis, rebuilt every frame. A straight cylinder, when the hand bends, pulls away from the cuff, and skin is visible in the gap.
- Hold the cuff strictly along the hand axis: the hand model below the joint has about 6 cm of "wrist", and if the cuff is tilted to the forearm by 15–25° it comes out through its wall by 2–4 cm.
- Limit the bend of the wrist to 45–50°, directing the poking finger halfway along the arm, not perpendicular to the screen: at 85–118° no sleeve looks plausible.

## Arm length and close screens [3D]

- Do not tear the shoulder off the body: if the target is farther than the arm's length, move the shoulder forward by no more than 12 cm (a "torso lean") and pull in the target itself. Arm stretch of more than 3–5 % the viewer sees as a hanging hand.
- Keep a close screen (phone, tablet) no closer than 35 cm from the eyes and below the line of sight: at 22 cm the forearm strikes diagonally across the frame, and the camera's near plane cuts the sleeve and shows it from inside.
- [Popsci] Place first-person hands in a body system that turns only by heading, not together with the tilt of the head: otherwise, when looking down, the hands drift after the camera.

## Body in the scene [3D]

- Keep the hands, torso, legs and shoes in the scene permanently, and do not switch them on when the camera looks down, otherwise the body appears in a single frame.

## Contact with surfaces and devices

- [3D] Raise the hand on a mouse, keyboard or table exactly enough for the lower fingertip to lie on the surface, otherwise the fingers go into the tabletop by about 4 cm; key travel on a press — 2–4 mm.
- [3D] Build the path of the hand to the device and back as an arc (to the device first up, then forward, back — the opposite): linear interpolation from a lowered hand cuts the edge of the tabletop.
- [Popsci] Lower the figure's feet 0–6 mm below the surface, not above: even a millimeter gap over the floor or a palm the viewer sees as hovering.

## Characters and furniture [3D]

- Place a character at a screen so that 1–4 cm to the glass remain from its back face, counting by the real depth of the head (ours is 18 cm), not by the center of the model, otherwise the screen passes through the middle of the body.
- Break a jump onto furniture and off it into a vertical and a horizontal curve with a shift of 0.15–0.25 s, otherwise with one common curve the character passes through the wall of the cabinet or the glass of the kiosk.

## Object in the hand

- [3D] Hold an object in a character's hand through a contact solution: after the pose move the whole character so that the mitten lands on the target point, otherwise it "holds" only by eye, and in fact hangs centimeters from the object.
- [Popsci] Attach an object that the figure holds to the hand, not to the body: with separate animation of hands and object the hands do not touch it, and it "hangs in the air".
- [Popsci] When the hands must reach an object, put the hand at the grip point and compute the elbow from the shoulder: hands with set angles miss the object with any change of pose.
- [Popsci] An object passing from one support to another (from the table into the hands) lead smoothly between the two attachment points over 0.3–0.35 s with a lift of a few centimeters: an instant change of support looks like teleportation.
- [Popsci] Give a figure on a thread or a rod a visible support at the level of the hands or belt: with the thread at the feet the figure looks as standing on the thread, not holding on to it.

## Skinning [3D]

- Take the vertices of a skinned mesh only after `skeleton.update()`: without a render the bone matrices lag by a frame, and the check gives hundreds of false intersections.
