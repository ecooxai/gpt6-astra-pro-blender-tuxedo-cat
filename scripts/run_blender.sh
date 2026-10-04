#!/usr/bin/env bash
set -euo pipefail
resource_root=/home/dev/.local/sysroot/usr/share/blender
if [[ -d "$resource_root/scripts" ]]; then
 export BLENDER_SYSTEM_SCRIPTS="$resource_root/scripts"
 export BLENDER_SYSTEM_DATAFILES="$resource_root/datafiles"
fi
export LP_NUM_THREADS=${LP_NUM_THREADS:-4}
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-4}
if [[ -S /tmp/.X11-unix/X93 ]]; then export DISPLAY=${DISPLAY:-:93}; fi
export LIBGL_ALWAYS_SOFTWARE=${LIBGL_ALWAYS_SOFTWARE:-1}
if [[ -z "${DISPLAY:-}" ]] && command -v xvfb-run >/dev/null; then
 exec xvfb-run -a blender -b -t "$OMP_NUM_THREADS" "$@"
fi
exec blender -b -t "$OMP_NUM_THREADS" "$@"
