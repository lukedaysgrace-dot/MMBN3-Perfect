// ---------------------------------------------------------------------------
// MistMan (White's Undernet Rank 2 Navi) alongside BowlMan
//
// Findings:
//  * Every MistMan text script is already in Blue: the BowlMan/MistMan area
//    (internet area 0x8C, sub-area 7) shares text archive 0x08761E00 between
//    versions and each script branches on flag 0x125E (set on New Game in
//    Blue, cleared in White).
//  * MistMan's AI, sprite (0x59), drop tables (enemy 0xDC-0xDF) and MistMan
//    Omega (already in Blue's Omega encounter lists) are all present.
//  * What White changes is data: the NPC sprite (0x58 -> 0x59) and the
//    battle definitions behind conversation battles 0x1E/0x1F/0x20.
//  * The rematch progress flags (0x12F-0x132) are shared by BowlMan in Blue
//    and MistMan in White.
//
// Implementation ("White mode" while talking to MistMan):
//  * A MistMan NPC is added next to BowlMan in this sub-area once the story
//    Rank 2 battle is over (progress >= 0x65, the same threshold the
//    original scripts use for the post-story dialogue).
//  * Talking to MistMan clears 0x125E and swaps the rematch flags with
//    MistMan's own copies (0x1F0-0x1F3), so White's original scripts,
//    branches, flag logic and texts run unmodified.
//  * While in White mode the area's battle selector uses three new
//    conversation-battle entries whose battle definitions are copied from
//    White (MistMan, MistMan alpha, MistMan beta; enemies 0x5DC-0x5DE).
//  * When the conversation, the battle and the post-battle text are all
//    finished (0x15B/0x15C clear, not talking) the flags are swapped back and
//    0x125E is set again, before the player regains control.  BowlMan's own
//    behaviour is untouched.
//
// NOTE: the private flags 0x1F0-0x1F3 are not referenced anywhere in either
// ROM (code or scripts) and are 0 in a completed save; existing save files
// therefore start with MistMan at V1.
// ---------------------------------------------------------------------------

.definelabel SetFlagIdx,    0x08021CF4   // r0 = flag
.definelabel ClearFlagIdx,  0x08021D10
.definelabel CheckFlagIdx,  0x08021D2C   // Z set when clear
.definelabel StartTextScript, 0x08026660
.definelabel StartCutscene, 0x0802ACD8   // r0 = handler, r1 = index
.definelabel ConvBattleHandler, 0x0812C209

.definelabel FLAG_BLUE,     0x125E
.definelabel FLAG_PENDING,  0x15C
.definelabel FLAG_RESULT,   0x15B
.definelabel FLAG_POSTGAME, 0xA00
.definelabel MM_FLAG_BASE,  0x1F0        // 0x1F0..0x1F3 <-> 0x12F..0x132

.definelabel GAME_STATE,    0x02001880   // +4 area, +5 sub-area, +6 progress
.definelabel INTERACTION,   0x02009480   // [sl+0x48]: nonzero while an interaction runs
.definelabel BOWL_AREA,     0x8C
.definelabel BOWL_SUBAREA,  7
.definelabel SPRITE_MISTMAN, 0x59

// ---- conversation battle table: relocate and add MistMan entries --------
.definelabel CONV_BATTLES,      0x0812BC98
.definelabel CONV_BATTLES_SIZE, 0x570       // 0x57 entries
.definelabel MM_BATTLE_V1,  0x57
.definelabel MM_BATTLE_V2,  0x58
.definelabel MM_BATTLE_V3,  0x59

.autoregion EXPANSION_START
.align 4
MistManBattleDefs:   // White's three entity lists (MistMan 0x5DC / 0x5DD / 0x5DE)
    .import WHITE_ROM, 0x1A748, 12
    .import WHITE_ROM, 0x1A754, 12
    .import WHITE_ROM, 0x1A760, 12
.align 4
ConvBattleTable:
    .import BLUE_ROM, CONV_BATTLES-0x08000000, CONV_BATTLES_SIZE
    // same parameters as Blue's BowlMan entries 0x1E-0x20 (and White's MistMan ones)
    .word MistManBattleDefs+0,  0
    .import BLUE_ROM, CONV_BATTLES-0x08000000+0x1E*16+8, 8
    .word MistManBattleDefs+12, 0
    .import BLUE_ROM, CONV_BATTLES-0x08000000+0x1F*16+8, 8
    .word MistManBattleDefs+24, 0
    .import BLUE_ROM, CONV_BATTLES-0x08000000+0x20*16+8, 8

// ---- MistMan NPC ---------------------------------------------------------
// Map-object script (interpreter 0x080F14A0).  Mirrors BowlMan's script at
// 0x0808FF51 with MistMan's sprite, his own position and text entry 9
// (an alias of the same script BowlMan uses, entry 10).
MistManNpc:
    .byte 0x05 :: .halfword 0x0919 :: .word MistManNpcHidden   // BowlMan's availability flag
    .byte 0x08
    .byte 0x18, 0x09                       // text script 9
    .byte 0x17, SPRITE_MISTMAN             // sprite
    .byte 0x14 :: .halfword 0x0076, 0xFFE4, 0x0000   // position
    .byte 0x16, 0x05
MistManNpcLoop:
    .byte 0x10, 0x01
    .byte 0x02 :: .word MistManNpcLoop
MistManNpcHidden:
    .byte 0x00                             // remove object
.align 4
BowlAreaNpcList:     // Blue's list 0x0808FE18 + MistMan
    .word 0x0808FE28, 0x0808FF51, 0x0808FF81, MistManNpc, 0xFF
.endautoregion

.org 0x0812C2BC
    .word ConvBattleTable
.org 0x0812C2C0
    .word ConvBattleTable

// ---- area init: choose the NPC list -------------------------------------
// Chapter-7 init handler for this sub-area is 0x0808FCE0 (10 table slots at
// 0x0808FC3C).  The wrapper only picks the NPC list, then continues in the
// original code.
.org 0x0808FC3C
.word BowlAreaInit|1, BowlAreaInit|1, BowlAreaInit|1, BowlAreaInit|1, BowlAreaInit|1
.word BowlAreaInit|1, BowlAreaInit|1, BowlAreaInit|1, BowlAreaInit|1, BowlAreaInit|1

// ---- area update: battle selector / White-mode exit ---------------------
.org 0x0808FD44
    .word BowlAreaUpdate|1

// ---- NPC talk: enter White mode when the NPC is MistMan -----------------
.org 0x080F145A
    bl      NpcTalkHook         // was: ldrb r0,[r5,#0x1C] / bl StartTextScript
    nop

.autoregion HOOK_SPACE, HOOK_SPACE_END
.align 2
BowlAreaInit:
    push    {r14}               // same prologue as 0x0808FCE0
    ldr     r7,=0x0808FE18      // vanilla NPC list
    push    {r0}
    ldr     r0,=GAME_STATE
    ldrb    r0,[r0,#6]          // progress
    cmp     r0,#0x65
    blt     @@vanilla
    ldr     r7,=BowlAreaNpcList
@@vanilla:
    ldr     r0,=0x0808FCE4|1    // continue with the original code
    mov     r12,r0
    pop     {r0}
    bx      r12
    .pool

// returns Z set if White mode is NOT active (i.e. flag 0x125E is set -> Blue)
IsBlueMode:
    push    {lr}
    ldr     r0,=FLAG_BLUE
    bl      CheckFlagIdx
    pop     {pc}

// swap flags 0x12F..0x132 with MM_FLAG_BASE..+3
SwapMistManFlags:
    push    {r4-r6,lr}
    mov     r4,#0
@@loop:
    ldr     r0,=0x12F
    add     r0,r0,r4
    bl      CheckFlagIdx
    add     r5,r0,#0                // nonzero = set
    ldr     r0,=MM_FLAG_BASE
    add     r0,r0,r4
    bl      CheckFlagIdx
    add     r6,r0,#0
    ldr     r0,=0x12F               // 0x12F+i := MistMan value
    add     r0,r0,r4
    cmp     r6,#0
    beq     @@clrA
    bl      SetFlagIdx
    b       @@doB
@@clrA:
    bl      ClearFlagIdx
@@doB:
    ldr     r0,=MM_FLAG_BASE        // MistMan copy := BowlMan value
    add     r0,r0,r4
    cmp     r5,#0
    beq     @@clrB
    bl      SetFlagIdx
    b       @@next
@@clrB:
    bl      ClearFlagIdx
@@next:
    add     r4,#1
    cmp     r4,#4
    blt     @@loop
    pop     {r4-r6,pc}
    .pool

NpcTalkHook:
    push    {lr}
    ldrh    r0,[r5,#0x3C]           // object sprite
    cmp     r0,#SPRITE_MISTMAN
    bne     @@talk
    ldr     r1,=GAME_STATE
    ldrb    r0,[r1,#4]
    cmp     r0,#BOWL_AREA
    bne     @@talk
    ldrb    r0,[r1,#5]
    cmp     r0,#BOWL_SUBAREA
    bne     @@talk
    bl      IsBlueMode
    beq     @@talk                  // already in White mode
    ldr     r0,=FLAG_BLUE
    bl      ClearFlagIdx
    bl      SwapMistManFlags
@@talk:
    ldrb    r0,[r5,#0x1C]
    bl      StartTextScript
    pop     {pc}
    .pool

BowlAreaUpdate:
    push    {lr}
    bl      IsBlueMode
    beq     @@white
    bl      0x0808FD48              // vanilla BowlMan battle selector
    pop     {pc}
@@white:
    ldr     r0,=FLAG_PENDING
    bl      CheckFlagIdx
    beq     @@maybe_exit
    // same selection logic as 0x0808FD48, MistMan battle entries
    mov     r6,#MM_BATTLE_V1
    ldr     r0,=0x12F
    bl      CheckFlagIdx
    beq     @@start
    mov     r6,#MM_BATTLE_V2
    ldr     r0,=FLAG_POSTGAME
    bl      CheckFlagIdx
    beq     @@start
    ldr     r0,=0x130
    bl      CheckFlagIdx
    beq     @@start
    mov     r6,#MM_BATTLE_V3
@@start:
    ldr     r0,=ConvBattleHandler
    add     r1,r6,#0
    bl      StartCutscene
    pop     {pc}
@@maybe_exit:
    ldr     r0,=FLAG_RESULT
    bl      CheckFlagIdx
    bne     @@stay
    ldr     r1,=INTERACTION
    ldrb    r0,[r1]                 // 1 while a text script / interaction runs
    cmp     r0,#0
    bne     @@stay
    bl      SwapMistManFlags        // leave White mode
    ldr     r0,=FLAG_BLUE
    bl      SetFlagIdx
@@stay:
    pop     {pc}
    .pool
.endautoregion
