// ---------------------------------------------------------------------------
// Giga chip version-legality checks
//
// Each version carries a "no-no list" of the *other* version's Giga chips.
// It is used when building the library lists/counts (0x080017F6, 0x080366B8)
// and by the shop/trader stock check (0x08044B02).  Blue lists White's five
// Gigas; White lists Blue's.  Both versions also gate one Bass chip on flag
// 0x1938 (= BassGS 0x138 is in the library): Blue gates Bass+, White gates
// Bass.
//
// Combined rule: no Giga is version-illegal any more, and Bass / Bass+ both
// keep their own version's original BassGS gate.
//
// Return convention (unchanged): Z flag set = chip is hidden/invalid,
// r0/r1 preserved.
// ---------------------------------------------------------------------------

.org 0x08001A48
.area 0x08001AA0-0x08001A48, 0x00
    push    {r0,r1,r14}
    ldr     r1,=CHIP_BASS_PLUS
    cmp     r1,r0
    beq     @@gate
    ldr     r1,=CHIP_BASS
    cmp     r1,r0
    bne     @@exit              // Z clear -> valid
@@gate:
    push    {r0-r3}
    mov     r0,#0x19            // flag 0x1938: BassGS in library
    mov     r1,#0x38
    bl      CheckFlag
    pop     {r0-r3}
    bne     @@hidden
    mov     r0,#1               // Z clear -> valid
    pop     {r0,r1,r15}
@@hidden:
    mov     r0,#0               // Z set -> hidden
@@exit:
    pop     {r0,r1,r15}
    .pool
.endarea

// Link "library compare" (0x0803F348) strips the other version's Gigas out of
// the data received from the partner.  Point Blue's four White-Giga entries
// at 0x110 (already cleared by the same routine, so this is a no-op) so the
// White Gigas are no longer stripped.  Bass / Bass+ handling is unchanged.
.org 0x0803F3CC
    .word 0x110, 0x110, 0x110, 0x110
