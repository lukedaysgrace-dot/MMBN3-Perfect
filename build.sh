#!/bin/sh
# Builds "MMBN3 - Perfect Version.gba" and release/MMBN3-Perfect.bps.
# Needs: armips; Python 3 with numpy, Pillow, scipy (for the title logo and .bps).
set -e
cd "$(dirname "$0")"
python3 tools/make_title.py || echo "(title logo step skipped - vanilla title will be used)"
armips main.asm
python3 tools/make_bps.py
