# Blue vs White (USA): every difference found, with addresses

All addresses are Blue's (`0x08xxxxxx`). White's equivalents are given where they differ.
Method: both ROMs were aligned with unique 16-byte anchors (561 matched segments,
data shifts of −0x100…+0x6C bytes). Inside each aligned region, a word was counted as
*equal* when both versions' values are ROM pointers to corresponding locations,
or `BL` instructions whose targets correspond. What remains is listed below.
Text archives were compared after LZ10 decompression, and all of them are byte-identical.

## 1. Code (identical except these spots)
| Blue | What differs | Handled in |
|---|---|---|
| `0x080000A0` | header title/code (`BLA3XE` / `WHA6BE`) | – (kept Blue) |
| `0x08001A48` | Giga legality: Blue lists 0x130,131,133,134 + 0x132 Bass and gates 0x137 Bass+ on flag 0x1938; White lists 0x12E,12F,135,136 + Bass+ and gates Bass | giga_legality.asm |
| `0x0800467C` | New Game: Blue **sets** flag 0x125E, White **clears** it | – (this is the version flag) |
| `0x080084D2` | link-battle prize fallback: DeltaRay Z / Balance Y | shops.asm (single-player route) |
| `0x08015180/0x080151F8` | "got DeltaRay/Balance" flag 0x1AA | – |
| `0x08015CE8, 0x08015D0A, 0x08015E2A, 0x08015EAE` | Style change: Blue disables style type 4 (Ground), White disables type 5 (Shadow) | ground_style.asm |
| `0x0803F3CC` | link library-compare strip list (same lists as 0x08001A48) | giga_legality.asm |
| `0x08033E14, 0x0803F58C, 0x0803FF40, 0x08045EE4` | literal Bass+ (Blue) / Bass (White) in library, shop and trader code, all gated on flag 0x1938 | covered by legality gate |
| `0x08047EDC` | 7-star reward: AlphArmΩ / AlphArmΣ | white_gigas.asm |

## 2. Data
| Blue | What | Notes |
|---|---|---|
| `0x08013AE8-0x08013C0F` | Giga chip art pointers (+0x18/+0x1C) | everything else in chip data is identical |
| `0x080160A8` (0xF4 × 0x38) | drop tables | 157 chip+code pairs only in White; BassGS 0xF2: Bass+ X vs Bass X |
| `0x08044BB0` (0xF80) | shop pool / Chip Order (copied to RAM `0x020035E0`) | 9 shops and the Giga part of the Chip Order differ |
| `0x08019EA8-0x0801B200` | battle entity lists | `0x0801A73C/48/54` BowlMan 0x5E0-0x5E2 vs MistMan 0x5DC-0x5DE (fixed battle 0x21, conversation battles 0x1E-0x20). **MistMan Ω (0x5DF) and BowlMan Ω (0x5E3) exist in both.** |
| `0x0801B024-0x0801B128` etc. | virus formations | kept Blue |
| `0x0808FF5C, 0x0808FF70` | BowlMan-area NPC sprite 0x58 (BowlMan) vs 0x59 (MistMan) | mistman.asm adds a separate MistMan NPC |
| `0x0812A506` | timed-battle navi list: 0xE0 BowlMan vs 0xDC MistMan | not added (record slots are in save RAM) |
| `0x08043000-0x080A0000`, `0x08420000-0x084F0000`, `0x087B0000+` | map scripts, map graphics, palettes, decorations | cosmetic, kept Blue |

## 3. Flag-0x125E branches in the shared scripts (`F3 00 5E 12`)
* Examine text for decorations in Lan's house, school, Yai's house, DNN, hospital, etc. (decor differs per version)
* `0x08761E00` scripts 1-49: BowlMan (Blue) / MistMan (White) Rank 2 + rematches
* `0x087A356C` scripts 0-10: post-Rank-2 dialogue
* `0x087658FC #69, 0x087694B4 #57/#118, 0x0876DC80 #58/#61, 0x0876FF68 #31/#43, 0x08770A90 #31`: WWW-navi NPC battles (different formations)
* `0x087B2864 #11`: "copy of MistMan/BowlMan available for timed battle"; `#24`: Serenade S (White) vs DarkAura A (Blue)

## 4. Identical in both versions (checked)
Number Trader (`0x080478F8`), BugFrag/Chip traders (`0x08042658`), GMD tables (area scripts via `0x080287F8`),
all BMD/PMD/NPC/job item gives (text archives), chip data apart from art, Program Advances (`0x0800D564`),
NaviCust programs, starting/extra folders, enemy stats (`0x08019618`), MistMan/BowlMan drop tables (0xDC-0xE3).

## 5. Useful structures found along the way
* Flags: base `0x02000030`, MSB-first; `SetFlag 0x08021CF0`, `ClearFlag 0x08021D0C`, `CheckFlag 0x08021D28` (`r0`=hi, `r1`=lo); `+4` entry points take the full index.
* Library bits = flags `0x1800 + chip`.
* `GiveChip 0x08011280 (chip, code, count)`; pack counts at `0x02001F60 + chip*0x12`.
* Area handlers: init table `0x08029BD0`, update table `0x08029C28` (internet area − 0x80), indexed by chapter = progress >> 4, then sub-area.
* BowlMan area = internet 0x8C sub-area 7. Chapter-7 init `0x0808FCE0`, update `0x0808FD48`, NPC list `0x0808FE18`.
* Map object script interpreter `0x080F14A0` (opcode table `0x080F14C0`): 02 jump, 04/05 jump if flag set/clear, 06/07 set/clear flag, 14 position, 17 sprite, 18 text index, 10 wait, 00 remove.
* Conversation battles: table `0x0812BC98` (16-byte entries, 0x57 of them), start handler `0x0812C209`, post-battle handler `0x0812C579` with result table `0x0812C2C4` (win/lose text, flags).
* Interaction-active byte `0x02009480`.
