# Tuxedo Cat Studio
## GPT-6 Astra Pro · mcp-colabdev · Blender headless

An original procedural black-and-white cat, built in Blender from direct visual inspection of a supplied four-view reference. No downloaded animal mesh, texture, environment map, or character asset is used. The reference is not projected onto the model. All images are actual Blender renders or explicitly labeled browser checks.

**Persistent studio:** https://ecooxai.github.io/gpt6-astra-pro-blender-tuxedo-cat/

**Source repository:** https://github.com/ecooxai/gpt6-astra-pro-blender-tuxedo-cat

**Live Colab preview:** https://stable-know-groups-subdivision.trycloudflare.com (temporary tunnel)

The current review status, actual iteration count, and limitations are in `preview/status.json` and `Agents.md`. Scores are subjective visual self-assessments, not independent measurements. The requested 20,000 iterations and above-95 score must not be confused with completed work.

## Open the existing model

Open `preview/downloads/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend` in Blender **4.0.2**, the version used for this project. The file contains the continuous anatomical sculpt, procedural pigment field, editable native fiber centerlines, folded ears, eyes, whiskers, lights, camera, and rendered attribution. No external character files are required.

The portable `.glb` is a lower-density approximation for general viewers. The `_web.glb` adds Meshopt compression for the supplied web app. To reduce mobile rendering cost, the web copy uses sampled vertex pigment, a lighter tapered-tube groom, and small reflection meshes instead of the full Blender corneal optics.

## Serve the web studio

```bash
python3 -m http.server 8794 --directory preview
```

Visit `http://localhost:8794`. Choose a studio view or **Orbit in 3D**. Drag to rotate, scroll/pinch to zoom, and right-drag to pan. The viewer renders on demand rather than continuously while idle.

For automatic discovery of newly completed renders in the archive, run this in another terminal:

```bash
python3 scripts/watch_preview.py
```

The deployed viewer is already bundled and uses no CDN. To rebuild it:

```bash
npm ci
npm run build
```

## Rebuild the original Blender scene

A Linux installation of Blender 4.0.2 with working OpenGL is required. The wrapper supports Xvfb/software rendering and the Colab resource layout; no GPU was available for the validated build. Keep `build_cat.py`, `coat_field.py`, and `native_groom.py` together in `scripts/`.

```bash
export CAT_BUILD_DIR="$PWD/build"
mkdir -p "$CAT_BUILD_DIR"
scripts/run_blender.sh --python scripts/build_cat.py -- \
  --revision 9 --fur 280000 --resolution 1000 --samples 24 \
  --views detail,hero,front,right,rear,left
scripts/run_blender.sh --python scripts/export_web.py
scripts/compress_web.sh
```

Use a new revision number to avoid overwriting previous review images. A fast geometry preview can use `--fur 80000 --resolution 640 --samples 8 --views hero`.

The primary scene uses **EEVEE**. `render_beauty.py` is a separately labeled, optional **Cycles + Open Image Denoise** lighting comparison. It does not overwrite the main EEVEE scene and is not an image-generation service. It requires the official `oidnDenoise` utility; its path can be supplied through `OIDN_DENOISE`.

## Quality checks and packaging

```bash
scripts/run_blender.sh --python scripts/check_geometry.py
python3 scripts/test_preview.py
python3 scripts/package_project.py
```

Browser checks require Playwright and Chromium. `CHROMIUM_PATH` and `CAT_PREVIEW_URL` override the browser path and local server address. Reports distinguish structural checks, responsive/browser tests, and actual visual reviews; automated assertions are not counted as visual modeling iterations.

The archive excludes dependencies, reference downloads, credentials, logs, and temporary render buffers. It includes a SHA-256 manifest and is checked for ZIP CRC errors. Rendering-library notices are in `THIRD_PARTY_NOTICES.txt`.

## Working locations

Project: `/home/dev/project/3d/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat`

Build: `/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat`

Git branch: `GPT-6-Astra-Pro_mcp-colabdev_blender-cat`
