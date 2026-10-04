# Agent handoff — GPT-6 Astra Pro / mcp-colabdev / Blender Tuxedo Cat

## Project and deployment
- Project: `/home/dev/project/3d/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat`
- Build directory: `/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat`
- Preview: project `preview/`, served on port **8794**.
- Live tunnel: https://virtually-homework-arranged-suggests.trycloudflare.com
- GitHub: https://github.com/ecooxai/gpt6-astra-pro-blender-tuxedo-cat
- GitHub Pages: https://ecooxai.github.io/gpt6-astra-pro-blender-tuxedo-cat/
- Branch: `GPT-6-Astra-Pro_mcp-colabdev_blender-cat`
- Git authentication is local-repository HTTPS via `gh auth git-credential`; do not expose tokens.

## Environment
Colab dev highram is active, with Blender **4.0.2** and software OpenGL on shared Xvfb `:93`. This project uses the mcp_colabdev connector, not the local VM. A persistent WebTerm shell named `cat-studio`, terminal **1635**, avoids the runtime's 32-terminal limit. Read that terminal before sending input. Never stop unrelated render jobs, preview servers, or Xvfb. The terminal cap was resolved by releasing only confirmed-finished setup terminals.

## Original modeling approach
The supplied reference is `reference/bwcat4view.png`, downloaded only for direct visual inspection; it is not used as a texture, mesh, or image-derived geometry. It is excluded from Git. No pre-existing model, texture, environment map, or animal asset is used. No image-generation service is used. Preview images are actual Blender EEVEE renders.

`build_cat.py` constructs an anatomical voxel-unified sculpt from original ellipsoids and lofts; a swept curved tail; folded ear surfaces; analytically colored black/white coat patches; curved radial golden irises, pupils and reflections; tapered whisker curves; and explicitly modeled, surface-sampled fur strands. Coordinates: Z up, face toward -Y. Geometry sampling is of our own mesh, never the reference image. Three.js is a rendering library, not a downloaded scene asset.

## Rebuild
```bash
cd /home/dev/project/3d/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat
scripts/run_blender.sh --python scripts/build_cat.py -- --revision 3 --fur 85000 --resolution 850 --samples 40 --views hero,front,right,rear,left
scripts/run_blender.sh --python scripts/export_web.py
npm run build
python3 scripts/publish_status.py --revision 3 --score ACTUAL_REVIEW_SCORE --title 'Actual observed change' --notes 'Honest visual findings' --status 'Actual status'
/home/dev/.venvs/webterm-tests/bin/python scripts/test_preview.py
```
Use a new revision number for a genuine build-and-preview iteration. Visually inspect renders through `mcp_colabdev.get_image`. Do not invent iteration counts, claim automated checks are visual iterations, or claim the >95 target is met without a defensible visual comparison.

For local serving: `python3 -m http.server 8794 --directory preview`.
For an independent machine, Blender 4.0.2 and a working OpenGL/Xvfb setup are required. Set `CAT_BUILD_DIR` to a writable directory if `/build` is unavailable. `npm ci && npm run build` rebuilds the browser bundle; the deployed viewer already includes it and needs no CDN.

## Completed visual reviews
1. **68/100**, first full original sculpt and coat. Coat layout and raised tail recognizable. Eyes too protruding and too large; ears too arched; legs segmented; black fur rendered too gray; cap boundary rectangular in profile.

2. **74/100**, continuous limbs, darker coat, better tail. Eye occlusion by cheek geometry remains; correcting sockets and ear/toe detail. The web model was reduced from 24.4 MB to 11.0 MB and the viewer now renders on demand.

## Work in progress
Revision 3 is queued (`logs/build_r03.log`, `logs/build_r03.pid`) after the fast pass-2 set. It sculpts orbital depressions, reduces cheek bulging, tapers ear tips, separates toes, and adds shadowless frontal fill.

Revision 2 applied a continuous limb loft, smaller embedded eyes, a rounder pupil, flatter ear folds, an organic cap boundary, darker low-specular black coat, longer chest grooming, better tail placement, and brighter studio lighting. It is queued after revision 1 finishes all views. Inspect `logs/build_r01.log`, `logs/build_r02.log`, and the corresponding PID files before continuing. Review score must be assigned only after viewing the actual new renders.

## Honesty / target
The user requested at least **20,000** build-preview iterations and a score above **95/100**. Neither requirement has been met at this handoff state. The live journal records real completed reviews and self-assessed visual scores, not independent evaluation. Do not report a target score as an achieved result.

## Files and exports
- Full scene: build directory `GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend`.
- Latest original model generator: `scripts/build_cat.py`.
- Viewer source: `scripts/viewer.js`; bundled asset: `preview/assets/viewer.js`.
- Exporter: `scripts/export_web.py`; full Blender groom is preserved, exported groom retains complete sampled strands at reduced density.
- Journal and public state: `preview/status.json`, atomically updated by `scripts/publish_status.py`.
- Tests: `scripts/test_preview.py`; logs and screenshots are in `logs/` and `preview/renders/`.
- Renders use `rNN_view.png`; obsolete large multiview sets may be archived, retaining honest review evidence.
- Never publish font files, credentials, environment files, unrelated project content, or large base64 output.
