# Blender as an offline asset generator [Toolkit]

Real light, glass, shatter, smoke, cloth and volumetrics are beyond a browser scene. Blender (5.2 LTS at the time of writing, GPL) renders them headless; its frames enter the backbone as an image sequence or a video layer. That does not break "one backbone" — Blender produces footage, the backbone still owns the timeline, the text and the sound.

Use it when the look needs it, not by default: a Blender shot costs minutes per frame and cannot be adjusted from the composition.

## Rendering from the command line

```bash
blender -b scene.blend --python-exit-code 1 -P setup.py \
  -o //frames/shot_##### -F PNG -x 1 \
  -s 1 -e 240 -a -- --cycles-device OPTIX
```

- Arguments run left to right: `-o`, `-F`, `-s`, `-e` must come **before** `-a` (or `-f`), which starts the render.
- `-P script.py` builds or adjusts the scene with `bpy` before rendering; `--python-exit-code 1` makes a Python error fail the command instead of rendering the unmodified file.
- Cycles device options go after `--`: `CPU`, `CUDA`, `OPTIX`, `HIP`, `ONEAPI`, `METAL`.
- Parallel: split the frame range between machines or processes (`-s`/`-e`, or `-j` frame jump); `-f` accepts lists and ranges (`-f 1,5,10..20`) for re-rendering the frames a review rejected.
- Cycles renders without a display. EEVEE needs a GPU context (headless through EGL on NVIDIA) — check it on the render machine before planning a shot around it.

## Determinism

- Set `scene.cycles.seed` explicitly. Leave `scene.cycles.time_limit` at 0: a time limit makes the noise depend on how fast the machine was.
- One denoiser setting for the whole video (OIDN or OptiX, with albedo and normal passes). Denoised noise that changes every frame shimmers; render a strip of consecutive frames (`scripts/sheet.sh`) and look before rendering everything.
- Rigid bodies, cloth, particles, fluids: frame N depends on frames 0…N−1. **Bake** before any frame is rendered out of order or in parallel: point-cache simulations (rigid body, cloth, particles) with `bpy.ops.ptcache.bake_all(bake=True)`; fluids and smoke (Mantaflow) do not use the point cache — bake the configured domain with `bpy.ops.fluid.bake_all()` into its cache directory. Check that the cache files exist on disk where every render process can read them; do not assume saving the `.blend` carries the cache. The most robust option for rigid bodies is to bake the simulation to keyframes.
- Fracture: the Cell Fracture extension (Blender 4.2+, GPL) or Geometry Nodes; fix its seed.

## Getting the result into the video

- **As footage (default):** a PNG sequence (8- or 16-bit; RGBA with Film → Transparent for an overlay) or ProRes 4444 with alpha; the composition shows it as a video layer at the same fps. Render at the video's fps — no retiming afterwards.
- **As motion for a browser scene:** export per-frame object matrices of the baked simulation to JSON and replay them in Three.js (`InstancedMesh` for many shards). The browser keeps crisp text and interactivity; Blender only computed the physics. A glTF round trip of the whole scene loses the look — do not use it as the default.
- **Colour:** Blender's default view transform is AgX; to match brand colours exactly use `Standard`. Display `sRGB`, so PNGs are ready for video encoding. Decide once per video.
- Record Blender and every add-on, model, HDRI and texture in the asset list with its licence.
