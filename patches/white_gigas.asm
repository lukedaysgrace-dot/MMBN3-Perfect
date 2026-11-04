// ---------------------------------------------------------------------------
// White-exclusive Giga chip acquisition
//
// Vanilla sources (identical code in both versions, only the chip differs):
//   FoldrBak / NavRcycl : Undernet 2 BugFrag shop            -> shops.asm
//   Bass+    / Bass     : BassGS drop table                  -> drop_tables.asm
//   DarkAura / Serenade : Serenade's gift for all timed-battle records
//   AlphArmO / AlphArmS : given by 0x08047E88 (7-star clear)
//   DeltaRay / Balance  : link-battle reward fallback only   -> shops.asm
//   BassGS              : common to both versions (unchanged)
// ---------------------------------------------------------------------------

// ---- AlphArm: give AlphArmS V alongside AlphArmO V -----------------------
// Original (0x08047E88):  ldr r0,=0x136 / mov r1,#0x17 / mov r2,#1 / bl GiveChip
// followed by setting flag 0x1A9 so it only happens once.
.org 0x08047E88
    bl      GiveBothAlphArms
    nop
    nop
    nop

.autoregion HOOK_SPACE, HOOK_SPACE_END
.align 2
GiveBothAlphArms:
    push    {r14}
    ldr     r0,=CHIP_ALPHARM_O  // vanilla Blue reward, same arguments
    mov     r1,#0x17
    mov     r2,#1
    bl      GiveChip
    ldr     r0,=CHIP_ALPHARM_S  // vanilla White reward (same arguments)
    mov     r1,#0x17
    mov     r2,#1
    bl      GiveChip
    pop     {r15}
    .pool
.endautoregion
