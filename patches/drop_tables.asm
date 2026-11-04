// ---------------------------------------------------------------------------
// Virus / Navi drop tables (White-exclusive chip codes, Bass X)
//
// Both versions use the same drop-table format and the same lookup routine
// (GetDropTable, 0x08016098: table = 0x080160A8 + enemy * 0x38), but the
// table contents differ: ~150 chip+code combinations only drop in White
// (e.g. Cannon A/B, ShockWav H/L ...), and BassGS drops Bass+ X in Blue but
// Bass X in White.
//
// A battle's rewards are now rolled from either the Blue table (vanilla
// data, untouched) or a copy of White's table (imported from the White ROM
// at build time), chosen 50/50 per battle.  The choice is derived from the
// battle counter so it is stable for every lookup made while the reward for
// one battle is being computed.  Every Blue drop keeps its original busting
// level / slot; it is simply rolled from White's table on half the battles.
// ---------------------------------------------------------------------------

.definelabel BLUE_DROP_TABLE,  0x080160A8
.definelabel DROP_TABLE_SIZE,  0x3570       // 0xF4 enemies * 0x38
.definelabel BATTLE_COUNTER,   0x02001DCA   // halfword, +1 per battle

.autoregion EXPANSION_START
.align 4
WhiteDropTable:
    .import WHITE_ROM, BLUE_DROP_TABLE-0x08000000, DROP_TABLE_SIZE
.endautoregion

// GetDropTable(r0 = enemy) -> r0 = table pointer. Clobbers r1, r2 (as before).
.org 0x08016098
    ldr     r2,[pc,#8]          // literal below now holds the hook address
    bx      r2
.org 0x080160A4
    .word   GetDropTableHook|1

.autoregion HOOK_SPACE, HOOK_SPACE_END
.align 2
GetDropTableHook:
    mov     r1,#0x38
    mul     r0,r1
    ldr     r1,=BATTLE_COUNTER
    ldrh    r1,[r1]
    ldr     r2,=0x9E3779B1      // scramble so consecutive battles don't simply alternate
    mul     r1,r2
    lsr     r1,r1,#31
    beq     @@blue
    ldr     r2,=WhiteDropTable
    b       @@done
@@blue:
    ldr     r2,=BLUE_DROP_TABLE
@@done:
    add     r0,r0,r2
    mov     r1,#0x38            // leave r1/r2 as the original routine did
    bx      lr
    .pool
.endautoregion
