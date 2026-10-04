#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
name=GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat
node_modules/.bin/gltfpack -i "preview/downloads/$name.glb" -o "preview/downloads/.${name}_web.pending.glb" -cc -kn -km -vp 16 -vn 10 -vc 8 -r logs/mesh-compression.json
mv "preview/downloads/.${name}_web.pending.glb" "preview/downloads/${name}_web.glb"
ls -lh "preview/downloads/$name.glb" "preview/downloads/${name}_web.glb"
