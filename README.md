# MMBN3-Perfect

A ROM hack for **Mega Man Battle Network 3 – Blue (USA)** that adds the content
that was exclusive to **White** so a single Blue save can get everything from
both versions. Apart from those additions, the goal is to leave vanilla Blue
alone: no rebalancing, no quality-of-life changes and no custom content.

---

**Just want to play?** See [How to play](#how-to-play-patch-your-own-rom). **Where to find the White content:** [WHITE_CONTENT_GUIDE.md](WHITE_CONTENT_GUIDE.md).

---

## How to play (patch your own ROM)

You don't need to build anything to play. The ready-made patch is in
[`release/MMBN3-Perfect.bps`](release/MMBN3-Perfect.bps).

1. Get your own dump of **Mega Man Battle Network 3 – Blue Version (USA)**.
   It must be the clean US ROM:
   - MD5 `6fe31df0144759b34ad666badaacc442`
   - You can check it at [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/), which shows the hashes when you load a file.
   - Japanese, European or already-patched ROMs will not work. The patcher will warn or refuse, because a BPS patch checks the source ROM.
2. Apply the patch with either tool:
   - **In a browser:** open [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/), pick your Blue ROM as *ROM file* and `MMBN3-Perfect.bps` as *Patch file*, then click **Apply patch**.
   - **On Windows:** use [Floating IPS (Flips)](https://github.com/Alcaro/Flips/releases). Choose *Apply Patch*, select `MMBN3-Perfect.bps`, then your Blue ROM, then where to save the result.
3. The patched ROM should be:
   - MD5 `e2fb65181baa5e304da5563c5ef8d596`
   - CRC32 `1947216E`
   - 8,431,296 bytes
4. Play it in any GBA emulator (mGBA is recommended) or on a flash cart.

**Saves**

- **Start a New Game.** The shop additions are copied into your save when you press New Game, so an old Blue save won't have them.
- Everything else, including MistMan, the drop mix, Ground Style and the Giga chips, also works on an existing Blue save.
- The save type is unchanged, so rename your `.sav` to match the new ROM's file name if you're bringing one over.
- Don't load a White save. White's save has White's shops and version flag.

**What the patch includes:** all of the White content, the three optional extras
(Punk P chip, Press/EngyChng without installing, and calmer random encounters in the four busiest maps) and the "BLUE+WHITE" title
screen. Build it yourself (below) if you want it without the extras.

Where to find everything from White: [WHITE_CONTENT_GUIDE.md](WHITE_CONTENT_GUIDE.md).

---

## How to build

1. Put your own dumps of the two US ROMs in `mmbn3/`:
   - `mmbn3/Mega Man - Battle Network 3 - Blue Version (USA).gba` (MD5 `6fe31df0144759b34ad666badaacc442`)
   - `mmbn3/Mega Man - Battle Network 3 - White Version (USA).gba` (MD5 `68817204a691449e655cba739dbb0165`)
2. Install [armips](https://github.com/Kingcom/armips) (v0.11 or newer) and put it on your `PATH`.
3. Install Python 3 with `pip install numpy pillow scipy`. This is only needed for the title screen and the `.bps`.
4. From the repo root, run `build.bat` on Windows or `./build.sh` on Linux/macOS. It does three things:
   1. `python tools/make_title.py` builds the "BLUE+WHITE" title graphics into `build/` from the logos in both ROMs.
   2. `armips main.asm` writes `MMBN3 - Perfect Version.gba`.
   3. `python tools/make_bps.py` writes `release/MMBN3-Perfect.bps` and checks that it reproduces the ROM.

You can run `armips main.asm` on its own. If `build/` is missing, the title
screen is simply left as Blue's.

The White ROM is only read during the build. White-only data (Giga chip
art, White's drop tables, MistMan's battle definitions and the "WHITE" logo
letters) is copied out of your own ROM by `.import` or by `make_title.py`.
The source files in this repo contain no ROM data. As with any ROM-hack
patch, `release/MMBN3-Perfect.bps` does hold the bytes it adds, so it can only
be applied to a ROM you already own. `*.gba` and `build/` are gitignored. The
old `white_giga_chip_sprites.dat` is no longer used.

---

## What the Blue/White comparison showed

I aligned the two ROMs with relocation-aware matching (shifted data pointers
and `BL` offsets are treated as equal), then decoded and compared every text
archive, shop, drop table, trader table and battle table. The full list is in
[`notes/BlueWhiteDifferences.md`](notes/BlueWhiteDifferences.md). In short:

* **The two versions share their code and all 300+ text archives.** White-only
  dialogue, such as MistMan's, is already inside Blue. Scripts choose a version
  by checking flag `0x125E`, which is set on New Game in Blue and cleared in
  White.
* Only a handful of code spots actually differ. They cover Ground vs Shadow
  Style selection, the Giga "no-no" legality lists, the Bass / Bass+ check, the
  AlphArm reward, and the DeltaRay / Balance link-battle fallback.
* The data differences are the virus/navi drop tables (157 chip+code pairs drop
  only in White), 9 shop inventories, Higsby's Chip Order list, the BowlMan ↔
  MistMan battle definitions and NPC sprite, the timed-battle navi list, the
  WWW-navi NPC battle formations, and map graphics/decorations.
* **These are identical in both versions:** Number Trader, BugFrag Trader,
  Chip Traders, Green/Blue/Purple Mystery Data, NPC gifts, Job/BBS rewards,
  Program Advances, NaviCust programs, chip data (damage, codes, classes),
  enemy stats and AI.

---

## Feature checklist

✅ means implemented **and** verified in an emulator (see *Testing* below).
⚠️ means implemented with a documented trade-off. ❌ means not implemented.

### A. Ground Style
| | Item | How |
|---|---|---|
| ✅ | Ground Style can be obtained through the normal Style Change | `patches/ground_style.asm` removes Blue's four Ground exclusions and adds White's own Ground point formula (terrain-chip counters ×70). |
| ✅ | Shadow Style is unchanged | Blue's Shadow formula is kept. With Ground and Shadow tied, the game now picks randomly between them (test: vanilla 40/40 Shadow, patched 24 Shadow / 16 Ground). |
| ✅ | Ground behaviour (charge shot cracks panels, elements, NaviCust) | This code and data already exist in Blue and are untouched. HeatGrnd was checked on the status screen and in battle. |

### B. MistMan and BowlMan
| | Item | How |
|---|---|---|
| ✅ | BowlMan unchanged (story Rank 2 fight, V1-V3 rematches) | His NPC, scripts, flags and battles are untouched. Verified that he still uses Blue dialogue and flags. |
| ✅ | MistMan NPC in the same Undernet area after the story Rank 2 battle (progress ≥ 0x65) | `patches/mistman.asm` adds a new map object (sprite 0x59) and a new NPC list. |
| ✅ | MistMan's White dialogue and V1/V2/V3 rematches | While you talk to MistMan the game runs in "White mode": flag 0x125E is cleared and the rematch flags 0x12F-0x132 are swapped with MistMan's own copies at 0x1F0-0x1F3. White's scripts then run unmodified. Three new conversation-battle entries use White's battle definitions (enemies 0x5DC/0x5DD/0x5DE). Blue mode comes back automatically when the conversation, battle and result text are over. |
| ✅ | BowlMan and MistMan progress are independent | Verified: winning MistMan V1 sets only MistMan's flag, and BowlMan's flags are restored. |
| ✅ | MistMan chips | They come from his own drop tables (0xDD → MistMan M, 0xDE → V2-V4 by busting level), which are byte-identical in both versions. |
| ✅ (data) | MistMan Ω / BowlMan Ω | Both are already in Blue's vanilla Omega encounter lists (`0x0812E2A0`, `0x0812EDD0`). Nothing needed changing. |
| ❌ | MistMan "copy" in Secret Area timed battles | See Limitations. |

### C. Giga chips (all ten)
| | Chip | Route |
|---|---|---|
| ✅ | FoldrBak \* (Blue) / **NavRcycl \*** (White) | Undernet 2 BugFrag shop, 200 BF each, as in their own versions |
| ✅ (unit) | Bass+ X (Blue) / **Bass X** (White) | BassGS drops Bass+ X with Blue's table and Bass X with White's (see drop tables) |
| ✅ (script) | DarkAura A (Blue) / **Serenade S** (White) | Serenade's gift for holding every timed-battle record now gives both chips, using the original script bytes |
| ✅ (unit) | AlphArmΩ V (Blue) / **AlphArmΣ V** (White) | The 7-star clear reward now gives both |
| ⚠️ | DeltaRay Z (Blue) / **Balance Y** (White) | In vanilla both are only obtainable as a link-battle prize. Single-player route: Undernet 6 BugFrag shop, 300 BF each (the 300 price both versions list for them) |
| ✅ | BassGS X | Common to both versions, unchanged |
| ✅ | White Giga artwork | Imported from the White ROM. Library shows the real art. |
| ✅ | Legality / anti-cheat | No Giga is version-illegal any more. Bass and Bass+ both keep their version's original BassGS-library gate. The game's own anti-cheat/checksum code is **not** disabled. |
| ✅ | 5-Giga folder rule, Giga Folder NaviCust | Untouched |

### C/D. Standard chips, codes, shops
| | Item | How |
|---|---|---|
| ⚠️ | White-only virus drop codes (157 chip+code pairs, e.g. Cannon A/B, ShockWav H/L) | Each battle's reward is rolled from either Blue's table (untouched) or a copy of White's, 50/50 per battle. Every Blue drop keeps its busting level and slot but comes from Blue's table on about half of battles. This is the one deliberate rate change, and it is needed to merge the two tables. |
| ✅ | White-only shop chips (20 pairs) | Added to an empty slot of the same shop with White's own price and stock (shops 0, 1, 3, 4, 8, 10, 13). Six that don't fit (shops 11, 13, 18 are full in Blue) go into Higsby's Chip Order list instead. No Blue item is moved or removed. |
| ✅ (data) | Number Trader, BugFrag Trader, Chip Traders, GMD/BMD/PMD, NPC gifts, Jobs | Identical in both versions, so nothing to add |
| ✅ (data) | Program Advances, NaviCust programs, chip stats | Identical |

### Changes from the old Perfect patches that were removed
| Old patch | Status |
|---|---|
| `debug_utils.asm`: **every enemy's HP set to 1** | Removed |
| `equipless_convenience_programs.asm`: Press/EngyChng work without being equipped | Rewritten as the optional `extra_equipless_programs.asm` (see below). The old version compared the counter's *address* instead of its value, ran a data word as code, and missed 3 of the 6 checks. |
| `anti_anti_cheat.asm`: blanket removal of save checksum checks plus a 0xFF-filled legality list | Replaced by a targeted legality fix. Checksums work again. |
| `punk_chip.asm`: Punk drops his (cut) chip, plus library count hacks | Rewritten as the optional `extra_punk_chip.asm` (see below). The old version forced the Mega list to always return 86. |
| `battle_giga_chips.asm`: custom extra-reward screens for Bass/BassGS/AlphArm | Replaced by the vanilla routes above |
| `giga_chip_sprites.asm`, `nav_rcycl_chip.asm` | Reworked. Chip-data fields other than the art pointers are no longer changed, and NavRcycl no longer overwrites a slot past the shop list. |

The old files are kept in `patches/legacy_unused/` for reference and are not
assembled.

---

## Optional extras (not in either original version)

These are on by default at the repo owner's request. They are separate
from the Blue + White merge.

| | Extra | Details |
|---|---|---|
| ✅ | **Press / EngyChng work if you own them** (`patches/extra_equipless_programs.asm`) | All 6 overworld checks for effect 0x28 (Press) and 0x24 (EngyChng) return true if the program is installed *or* is in your NaviCust inventory. Installing it still works as before. |
| ✅ | **Punk P chip is obtainable** (`patches/extra_punk_chip.asm`) | The cut Mega chip 0x110 is fully present in the ROM, but in vanilla nothing gives it and the library skips it. Punk is fought in three levels: Punk, Punk α, Punk β. Their drop tables now follow the pattern every other Navi uses, with BowlMan as the template: plain Punk still drops only Zenny. **Punk α drops Punk P only at the highest busting levels** (the slots where BowlMan β gives his V4). **Punk β drops it more often**, in every slot where BowlMan β gives a BowlMan chip. Punk P is V3/V4-strength (180 damage, 92 MB, 4★), so it isn't handed out on every α win. Punk has only one chip, so there are no V2-V5 versions. The change is applied to both drop tables used by the 50/50 mix. The library now lists and counts Punk, and the hard-coded Mega total (85) is raised to 86 everywhere it is used (completion star, "n/total" display). |
| ✅ | **Busiest random-encounter maps calmed down** (`patches/extra_encounter_rate.asm`) | Same approach as MMBN2 Restored. Every 64 units you move, the game rolls `random & 0x1F` against a threshold from a curve (`0x0800D26C`), indexed by how many checks since the last battle and by the map's level (`0x0800D2F4`; 7 = no encounters, 6 = calmest). In vanilla the whole main Net (groups 0x80-0x83) is level 6 and the comp/object areas (0x88, 0x8A, 0x8C, 0x8D) are level 5. Only four real maps are busier, and only those change, to level 5: the red WWW area (0x83 sub-map 4, AlphaBug viruses) goes from 4 to 5, and three comps (0x8C sub-maps 13-15) go from 3 to 5. Average walking time between battles there goes from about 11-12 s to about 14.5 s, the same as the other comps. Every other level-3 entry is an unused slot with no map, so it is left alone. The curve and the check interval are unchanged, and the build stops if the original bytes aren't the expected ones. |
| ✅ | **"BLUE+WHITE" title screen** (`patches/title_screen.asm`, `tools/make_title.py`) | The logo reads *MEGA MAN BATTLE NETWORK 3 BLUE+WHITE*, and the screen is cut in half along the italic line through the "+". The left is Blue's title (blue stripes, navy plate) and the right is White's (grey stripes, grey plate). The word uses only Capcom's own lettering: Blue's "BLUE", and White's "WHIT" and final "E", narrowed at full height and at the original italic angle. The last E's arms still run into White's swoosh around the "3", and the plate, its border and the letter outlines are redrawn to match the originals. White's greys go in 32 palette slots that are empty on this screen (208-239). The title loads 240 colours instead of 224, and the menu's dimming covers 240 colours instead of 208, so the grey half dims like the blue half. "PERFECT BLUE" was considered, but the logo font has no P, R, F or C, so it would have needed invented letters. Delete `build/` or comment out the include to keep Blue's title. |

To get the pure merge, comment out the three `extra_*.asm` lines under *Optional extras* at the bottom of `main.asm` and the `title_screen.asm` line above them.

Note for the Mega library: vanilla's 85 already *included* MistMan's four
chips, which is why Blue alone could never reach it. With MistMan in the
game, 85 (or 86 with Punk) can now be reached on one save.

## Limitations (stated honestly)

* **Drop-rate merge.** A drop-table entry has room for exactly one chip+code.
  The only way to keep all of Blue's drops *and* add White's without new
  mechanics is to alternate between the two tables, so Blue codes drop on
  about half of battles where they used to drop on all of them. It's a single
  hook in `patches/drop_tables.asm`.
* **Six White shop chips are in Higsby's Chip Order** instead of their
  original shop, because those Blue shops have no free slot. The shop pool is
  part of save RAM, so growing a shop would break existing saves.
* **Shop additions only appear in new save files.** The shop pool is copied
  into RAM on New Game.
* **MistMan's timed-battle copy is not added.** Each version's record table
  (`0x0812A506`) has one slot that holds BowlMan *or* MistMan, and records live
  in save RAM. The Serenade S gift is still obtainable because Serenade gives
  both DarkAura A and Serenade S for completing Blue's record set.
* **White-only cosmetics are not added:** room decorations and their
  "examine" text, White's alternate formations for the five WWW-navi NPC
  battles, and Mr. Famous's hint-giving apprentice (White's replacement for
  Mr. Famous). Blue keeps its own versions so vanilla Blue stays unchanged.
  None of these affect chips, items or completion.
* MistMan's progress uses flags `0x1F0-0x1F3`. No code or script in either ROM
  references them, and they are zero in a finished save. On an existing save,
  MistMan starts at V1.
* White's "copies" of its own Gigas in the Chip Order list (all stock 0, which
  means they can't be ordered in either version) are not added.
* The output ROM grows to about 8.04 MB. New data goes after the original
  8 MB, and small hooks use 0xFF padding at `0x08235200` that is otherwise
  unused. No original Blue data is overwritten except the patched code and
  pointers listed in `notes/BlueWhiteDifferences.md`.

---

## Testing

Tests use a headless mGBA (libmgba 0.10.5) harness (`tools/tests/`). The ROM
itself has no emulator-specific code.

| Check | Method | Result |
|---|---|---|
| Changed bytes vs vanilla Blue | byte diff of the built ROM | 829 bytes inside the original 8 MB (the hooks, pointers and table entries described above), plus appended data |
| Giga legality for all 11 Gigas, with and without BassGS in the library | unit test calling `0x08001A48` | pass |
| Drop table hook stays stable within a battle, uses both tables ~50/50, Blue table untouched, White copy byte-exact, BassGS row = Bass X | unit test calling `0x08016098` | pass |
| White Giga art is byte-exact and shows in the Library | byte compare plus screenshot | pass |
| AlphArm reward gives both AlphArms | unit test | pass |
| Shops / Chip Order after New Game initialisation | unit test calling `0x08045BD0` | pass |
| Ground and Shadow both selectable | unit test of style pick `0x08015CA8` (vanilla vs patched) | pass |
| HeatGrnd style shown, Ground charge shot cracks panels | gameplay screenshots | pass |
| MistMan appears next to BowlMan postgame and uses White dialogue | gameplay | pass |
| MistMan V1 battle starts, can be won, progress saved separately, Blue mode restored | gameplay (`t_mistman.py`) | pass |
| MistMan V2 (1300 HP) and V3 "MistMan β" (1600 HP) load from the right flags | gameplay | pass |
| BowlMan still uses Blue dialogue and flags | gameplay | pass |
| New Game boots, flag 0x125E still set (Blue) | gameplay | pass |
| Press/EngyChng usable when owned (not installed), not usable when not owned | unit test | pass |
| Title screen reads BLUE+WHITE, split blue/white, emulator output matches the generated image pixel for pixel, palette RAM = built palette, grey half dims with the menu and fades out on New Game | emulator screenshots plus image compare | pass |
| `release/MMBN3-Perfect.bps` applied to clean Blue gives the built ROM | Floating IPS and the repo's own BPS decoder, MD5 compare | pass |
| Encounter levels: the game's own check called 2000 times per map, with random seeds, at a fixed step count | unit test (`t_encounters.py`): the four outliers drop from 31%/25% to 15.6% per check; five untouched maps (both Net groups and comps) give the same rate as vanilla | pass |
| Punk P: drop tables, library count +1, anti-cheat verify still passes, library shows 86/86 | unit test plus screenshot | pass |

**Not yet tested end-to-end in an emulator:** walking through a Press gap or EngyChng barrier in the overworld, actually defeating Punk α/β in-game, winning the MistMan V2/V3 fights
(the battles load; the win path is the same as V1), Serenade's double gift (the relocated
script was disassembled and checked), the DeltaRay/Balance purchase from the
UN6 shop UI, and a full new-game playthrough.

---

## Original notes from the previous author

The research notes in `notes/` are kept as they were.
