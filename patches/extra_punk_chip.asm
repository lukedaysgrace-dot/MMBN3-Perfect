// ---------------------------------------------------------------------------
// OPTIONAL (cut content, not obtainable in vanilla Blue or White) - enabled
// at the owner's request
//
// The "Punk P" Mega chip (0x110) exists in the ROM with full data, art and
// attack, but nothing ever gives it and the library code deliberately skips
// it.  Punk is fought in three levels from his rematch NPC (conversation
// battles 0x21/0x22/0x23 -> enemies 0xD4 Punk, 0xD5 Punk alpha, 0xD6 Punk
// beta; selected by flags 0x127/0x128 like every other Navi).  All three only
// drop Zenny.
//
// Punk's drop tables are given the same layout every Navi uses (BowlMan as
// the template):
//   * Punk       (0xD4): unchanged, Zenny only      (= BowlMan V1, 0xE0)
//   * Punk alpha (0xD5): Punk P only in the top busting-level slots (10-13 of
//                        each half - where BowlMan beta gives his V4); Punk
//                        alpha's own Zenny everywhere else.
//   * Punk beta  (0xD6): Punk P in every slot where BowlMan beta (0xE2) gives
//                        a BowlMan chip (5, 7, 9-13); Punk's own Zenny elsewhere.
// Punk P is V3/V4-strength (180 dmg, 92 MB), so - unlike a V1 chip - it is
// not handed out on every alpha win.  Punk has only one chip, so there are
// no V2-V5 versions.
// The patch is applied to both Blue's table and the White copy used by
// drop_tables.asm, so the 50/50 table mix doesn't hide it.
//
// Library: the two "skip chip 0x110" checks are removed so Punk is listed
// and counted as a Mega chip once obtained (this raises the Mega total).
// ---------------------------------------------------------------------------

.definelabel PUNK_P, (15 << 9) | 0x110      // code P, chip 0x110

.macro punk_tables, base
    // Punk alpha (0xD5): slots 10-13 of each half (highest busting levels)
    .org base + 0xD5*0x38 + 10*2
    .halfword PUNK_P, PUNK_P, PUNK_P, PUNK_P
    .org base + 0xD5*0x38 + (14+10)*2
    .halfword PUNK_P, PUNK_P, PUNK_P, PUNK_P
    // Punk beta (0xD6): slots 5,7,9-13 of each half, as BowlMan beta
    .org base + 0xD6*0x38 + 5*2
    .halfword PUNK_P
    .org base + 0xD6*0x38 + 7*2
    .halfword PUNK_P
    .org base + 0xD6*0x38 + 9*2
    .halfword PUNK_P, PUNK_P, PUNK_P, PUNK_P, PUNK_P
    .org base + 0xD6*0x38 + (14+5)*2
    .halfword PUNK_P
    .org base + 0xD6*0x38 + (14+7)*2
    .halfword PUNK_P
    .org base + 0xD6*0x38 + (14+9)*2
    .halfword PUNK_P, PUNK_P, PUNK_P, PUNK_P, PUNK_P
.endmacro

punk_tables BLUE_DROP_TABLE
punk_tables WhiteDropTable

// Library: owned-Mega count (0x08001794) and Mega list (0x080365D8) both
// compare against 0x110 and skip it.  Point the comparison at an impossible
// chip number instead.
.org 0x080017D4
    .word 0xFFFF
.org 0x08036698
    .word 0xFFFF

// The game hard-codes the Mega library total as 85 (= the 86 Mega chips
// minus Punk; note this already includes both BowlMan and MistMan, which is
// why vanilla Blue alone could never reach it).  With Punk counted the
// total is 86.
.org 0x08001B04
    cmp     r0,#0x56        // completion star: owned Megas >= total
.org 0x08030512
    cmp     r0,#0x56        // library: show "n/total" when complete
.org 0x080368E6
    cmp     r0,#0x56        // library: same check, list screen
.org 0x0803D54A
    cmp     r0,#0x56        // other "all Megas" check
