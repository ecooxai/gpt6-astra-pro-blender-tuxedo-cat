# Tuxedo Cat — GPT-6 Astra Pro · mcp-colabdev · Blender

An original procedural black-and-white folded-ear cat, modeled in headless Blender 4.0.2 and presented in a responsive, self-contained WebGL review studio.

**Persistent preview:** https://ecooxai.github.io/gpt6-astra-pro-blender-tuxedo-cat/

**Live development preview:** https://turbo-academic-choice-certificate.trycloudflare.com

## Current checkpoint
Revision **12**. **12 genuine reviewed passes**, including documented regressions. Latest subjective visual assessment: **89/100**. This is not an independent benchmark; the requested 20,000 iterations and score above 95 have **not** been achieved. The cat remains a stylized approximation rather than a photoreal or production-rigged animal.

The current scene has 373,498 unified body vertices and 280,063 original native fur strands. The coat, folded ears, yellow eyes, white blaze, flank patches, whiskers and raised tail are procedurally authored. Later passes refine facial microfur, ear attachment, a rounded nose, staggered feet, eye shading and soft studio presentation.

## Deliverables
The studio's download section provides:
- **`.blend`**: editable full scene with original skin geometry, native hair guides and geometry nodes, coat shader, eye components, cameras and lighting.
- **`.glb` / `_web.glb`**: portable 3D model and compressed browser version. Only the web copy reduces fur density and skin polygons.
- **Project archive**: generator, companion modules, viewer source and bundle, Blender scene, GLBs, renders, review journal, validation reports and agent handoff.

Every deliverable uses the basename `GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat`. Absolute project/output paths are shown inside the studio. The image gallery retains review evidence, with the latest work first. Historical experiments and browser QA captures are labeled separately.

## Build from original source
```bash
npm ci
npm run build
scripts/run_blender.sh --python scripts/build_cat.py -- \
  --revision 13 --fur 180000 --resolution 1000 --samples 32 \
  --views hero,front,detail,left,right,rear
scripts/run_blender.sh --python scripts/check_geometry.py
scripts/run_blender.sh --python scripts/export_web.py
scripts/compress_web.sh
python3 -m http.server 8794 --directory preview
```
Use a new revision only for a genuine reviewed refinement. Blender 4.0.2 and a functioning OpenGL/Xvfb setup are required; the runner supplies the restored Colab installation's resource paths. Set `CAT_BUILD_DIR` to a writable folder outside Colab. The deployed browser bundle requires no CDN.

For a fast EEVEE review, add `--fast-preview`; this changes only temporary rendering settings and restores full groom shadows in the saved scene. `scripts/render_presentation.py` renders existing scenes with correct orthographic framing and soft studio lights. Its default omits the fine fibers' shadow pass for speed while retaining every strand; `--full-fur-shadows` enables the complete shadow pass. The current optional physical corneal shells are preserved but hidden: visible eyes use original iris/pupil surfaces and dielectric coating to avoid screen-space-refraction artifacts.

## Validation
`check_geometry.py` verifies closed body edges and finite coordinates and reports paw heights and actual strand counts. It does not infer likeness. `test_preview.py` uses headless Chromium to check render loading, four view selections, real orbit dragging, five exact camera presets, render switchback, idle rendering and desktop/tablet/mobile overflow.

Published results are under `reports/`. The archive contains a per-file SHA-256 manifest; `package_project.py` checks the ZIP CRC before publishing.

## Provenance
The user-provided four-view reference was visually inspected only. No image analysis, image projection, downloaded animal mesh, texture, fur asset or HDRI is used. No image-generation service is used. The model is built from original mathematical geometry and materials. Three.js, esbuild and gltfpack are development libraries, not character assets; notices are in THIRD_PARTY_NOTICES.txt. The reference file, credentials, dependencies, temporary logs and font files are excluded from the distributable archive.

## Continuation
Project: `/home/dev/project/3d/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat`

Build: `/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat`

Branch: `GPT-6-Astra-Pro_mcp-colabdev_blender-cat-r09`

Read **Agents.md** before further edits. It records the current terminal, services, model decisions, real review history, rebuild commands and remaining quality gaps. Primary remaining likeness issues are eye realism, folded-ear silhouette, natural fur breakup and overall photoreal fidelity. No animation rig is claimed.
