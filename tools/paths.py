# Shared paths for the analysis tools and tests (relative to the repo root).
import os
REPO  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BLUE  = os.path.join(REPO, 'mmbn3', 'Mega Man - Battle Network 3 - Blue Version (USA).gba')
WHITE = os.path.join(REPO, 'mmbn3', 'Mega Man - Battle Network 3 - White Version (USA).gba')
OUT_ROM = os.path.join(REPO, 'MMBN3 - Perfect Version.gba')
OUT = os.path.join(REPO, 'tools', 'out'); os.makedirs(OUT, exist_ok=True)
# external checkouts used by some analysis scripts
EXT = os.environ.get('MMBN3_EXT', os.path.join(REPO, 'tools', 'ext'))
