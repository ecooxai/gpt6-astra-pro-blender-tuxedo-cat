# Agent handoff — GPT-6 Astra Pro / mcp-colabdev / Blender Tuxedo Cat

## Active project and services
Project: `/home/dev/project/3d/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat`
Build: `/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat`
Preview: project `preview/`, Python HTTP port **8794**.
Live development URL: https://turbo-academic-choice-certificate.trycloudflare.com
GitHub: https://github.com/ecooxai/gpt6-astra-pro-blender-tuxedo-cat
Pages: https://ecooxai.github.io/gpt6-astra-pro-blender-tuxedo-cat/
Continuation branch: `GPT-6-Astra-Pro_mcp-colabdev_blender-cat-r09`.

Use Colab dev highram, not the local host. Blender 4.0.2 is installed under `/home/dev/.local/sysroot/usr/`. Software OpenGL uses Xvfb `:93`. `scripts/run_blender.sh` supplies Blender resource paths, DISPLAY and bounded render threads. Do not stop unrelated render jobs, services or Xvfb.

**Reuse terminal 1670, `cat-studio-continuation`.** The runtime has a 32-terminal limit; each `webterm run` allocates another persistent shell. Read terminal 1670, then use `webterm write 1670 --enter` for commands. Shell echo is disabled intentionally. Read after each write to obtain execution results. Finished inspection shells may be released only after checking ownership and completion.

Service logs/PIDs: `logs/server-resume.*`, `logs/tunnel-resume.*`, `logs/xvfb-resume.*`, `logs/watch-resume.*`. Tunnel lifetime follows the running process; GitHub Pages is the persistent preview.

## Provenance and modeling
The supplied four-view reference is `reference/bwcat4view.png`. It was visually inspected, never sampled, traced by image analysis, projected as a texture or used to derive geometry. It is excluded from the published repository and archive. No downloaded cat mesh, fur texture, HDRI or character asset is used. No image-generation service is used. Three.js, esbuild and gltfpack are software libraries; see THIRD_PARTY_NOTICES.txt.

`scripts/build_cat.py` constructs the cat from original ellipsoids, continuous limb lofts, a swept tail, voxel-unified skin, mathematical coat pigment, folded ear surfaces, radial eye geometry, original nasal topology and tapered whiskers. Z is up and the face points toward -Y. Native hair curves come from original surface-sampled guide meshes; only our own geometry is sampled. `scripts/coat_field.py` defines the continuous pigment. `scripts/native_groom.py` builds editable guide meshes and native curve geometry nodes.

## Actual review history
Scores are subjective self-assessments, not an independent benchmark.
1: 68; 2: 74; 3: 82; 4: 84; 5: 83; 6: 86; 7: 85.
8: **86** — recovered work; scalp-anchored folds, but projecting oval eyes and coarse facial fur.
9: **85** — rounder eyes, lifted chin and fine fibers; experimental corneal film flattened the pupils. One completed hero was reviewed; remaining pass-9 views were deliberately canceled. This is not counted as multiple iterations.
10: **87** — shallow physical cornea, darker lids and scalp-resting ear tips. Six EEVEE views; fast shadows are visibly harsh. Side-view legs overlapped exactly.
11: **88** — natural staggered paws, soft toe channels, dense targeted facial microfur and rounded lobed nose. Six EEVEE views. Remaining priorities: eye reflection and presentation lighting.
12: **89** — cleaner eye shading, matte eyelid pigmentation, smaller glints and soft EEVEE studio presentation. See `preview/status.json` for the completed view set. Never assume a requested score was attained.

The user requested **20,000 genuine build-preview iterations and a score above 95/100**. These requirements have not been met. Do not inflate counts using test assertions, render samples, strand counts, repeated identical images or simulated progress. Each journal PASS corresponds to an actual model/render review. Report regressions honestly.

## Latest geometry and optical work
The unified body contains 373,498 vertices and 373,496 polygons. Structural validation found a closed mesh, no nonfinite vertices and a maximum measured left/right paw-height difference below 0.001 scene unit. There are 280,063 accepted authored strands. These numbers do not establish likeness.

Pass 11 adds 95,000 requested facial microstrands, denser lid grooming, slightly staggered far-side paws and a lobed nose. Pass 12 corrects nose winding and replaces unstable EEVEE screen-space eye refraction with a thin dielectric microcoat on the authored iris/pupil surfaces. Optional physical corneal shells remain in the source, hidden from renders. Mobile exports exclude them and retain small authored glint meshes.

## Rebuild and validation
```bash
cd /home/dev/project/3d/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat
scripts/run_blender.sh --python scripts/build_cat.py -- --revision 13 --fur 180000 --resolution 900 --samples 32 --views hero,front,detail,left,right,rear
# Fast review: add --fast-preview. It changes render sampling only; full saved groom shadows are restored.
scripts/run_blender.sh --python scripts/check_geometry.py
scripts/run_blender.sh --python scripts/export_web.py
scripts/compress_web.sh
npm ci && npm run build
/home/dev/.venvs/webterm-tests/bin/python scripts/test_preview.py
```
Use the next unused revision only for a real refinement. Rebuilding unchanged source is not a new improvement score. Set CAT_BUILD_DIR for a writable build directory on another machine.

`scripts/render_presentation.py` renders saved scenes with correct distant orthographic camera framing and camera-parented attribution. Default previews omit only the fine fibers' shadow pass for speed while preserving all strand geometry; `--full-fur-shadows` renders the complete saved groom shadows. It never overwrites source geometry. The older `render_saved.py` uses legacy camera placement; prefer render_presentation.py.

Exports reduce only the browser copy: body and face strand sampling are bounded, skin is decimated, analytic coat becomes portable vertex color, and gltfpack compresses geometry. The full-resolution Blender scene remains separate. Portable coat materials disable the exaggerated sheen extension; the web renderer uses low-specular matte PBR for coat materials only, not the golden iris. Run exporter after every final geometry revision; do not publish a new render beside a silently stale GLB.

## Web app and output
`preview/index.html`, `app.js`, `style.css`; viewer source `scripts/viewer.js`, bundled `preview/assets/viewer.js`. No CDN is needed at runtime. Status auto-refreshes every eight seconds, journal is latest-first, absolute file paths appear below outputs. Orbit view has five camera presets, drag rotation, pinch/scroll zoom and on-demand rendering.

`preview/status.json` is the public source of truth. `scripts/publish_status.py` records only explicit reviewed scores and copies source modules/Agents.md. It does **not** copy the .blend: copy the latest build file into preview/downloads explicitly. It also updates the image manifest; watch_preview.py refreshes the all-renders gallery.

Important downloads are named `GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat` with .blend, .glb, _web.glb and .zip extensions. `scripts/package_project.py` creates a SHA-256 manifest and CRC-tested archive while excluding references, dependencies, secrets, logs and temporary files. Never publish font files or environment credentials. Do not print binary/base64 to terminal output.

Headless Chrome checks cover render loading, all four image-view controls, real orbit dragging, all five 3D presets, render switchback, idle frames and 390/768/1440px layouts. Latest check logs are under logs/, published evidence under reports/. Verify the latest model, not merely prior screenshots.

## Deployment and safe continuation
Use Git commits after meaningful source/review checkpoints. The authenticated `gh` credential helper works; never expose credentials. Push the continuation branch, select it in the repository Pages configuration, check the Pages build result and test the public URL. Large release archives belong in GitHub Releases rather than Git history. Source changes alone do not prove deployment.

Record actual finished tests and any incomplete work in README/status before packaging. Colab restoration does not preserve /build unless copied into home; ensure the full .blend is in preview/downloads before invoking Colab backup. Never stop the instance as a substitute for backup.
