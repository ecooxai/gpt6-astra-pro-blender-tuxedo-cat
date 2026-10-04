#!/usr/bin/env bash
set -euo pipefail
export BLENDER_SYSTEM_SCRIPTS=/home/dev/.local/sysroot/usr/share/blender/scripts
export BLENDER_SYSTEM_DATAFILES=/home/dev/.local/sysroot/usr/share/blender/datafiles
export DISPLAY=${DISPLAY:-:93}
export LIBGL_ALWAYS_SOFTWARE=1
export OMP_NUM_THREADS=4
exec blender -b -t 4 "$@"
