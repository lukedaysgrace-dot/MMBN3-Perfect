# tools/

* `romdiff/` – the scripts used to compare the Blue and White ROMs
  (`align.py` → `diffmap.py` → `realdiff2.py`; `archives.py`/`tpdis.py` decode
  text archives using TextPet's `mmbn3.ini`; `dist.py` builds the chip+code
  distribution of both versions). Some need external checkouts in `tools/ext/`
  (Prof9/TextPet, ArchipelagoMW worlds/mmbn3, XKirby/MMBN3-Randomizer chip names).
* `tests/` – headless mGBA harness (`harness.c`, `emu.py`) and the automated
  checks: `t_units.py` (legality, drop hook, art, AlphArm, shops),
  `t_style.py` (Ground/Shadow selection), `mkarea.py` + `mm.py` (warps into the
  BowlMan/MistMan area using the repo's `MMBN3 - Perfect Version.ss3`
  savestate and drives the MistMan conversation/battle).
  Build the harness with `build_harness.sh` (Linux, needs mGBA 0.10 built as a library).
