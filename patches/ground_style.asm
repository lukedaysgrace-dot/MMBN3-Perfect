// ---------------------------------------------------------------------------
// Ground Style
//
// Blue and White run identical style-change code except for four spots where
// each version "switches off" the other version's style (style type 4 =
// Ground, 5 = Shadow).  Blue zeroes the Ground style points, clears the
// Ground battle counter and excludes type 4 from the random pick; White does
// the same for Shadow.  Removing Blue's exclusions and adding White's Ground
// point formula lets both styles coexist using each version's own original
// rules.  No probabilities or requirements are changed beyond that.
// ---------------------------------------------------------------------------

// 0x08015CA8 picks the next style. Blue clears the Ground entry of the
// "battles since" table before choosing (White clears Shadow). Keep both.
.org 0x08015CE6
    nop                         // was: mov r0,#0
    nop                         // was: strb r0,[r2,#4]

// ...and skips type 4 when collecting the candidates (White skips type 5).
.org 0x08015D0A
    nop                         // was: cmp r3,#4
    nop                         // was: beq skip

// 0x08015D60 tallies style points after a battle. Blue stores 0 for the
// Ground slot; White computes it from the terrain-chip counters (+0x12/+0x13,
// 70 points each).  Call White's formula instead.
.org 0x08015E2A
    bl      GroundStylePoints   // was: mov r0,#0 / str r0,[sp,#0x10]

// Same routine, "every style +1" branch: Blue clears the Ground counter.
.org 0x08015EAC
    nop                         // was: mov r0,#0
    nop                         // was: strb r0,[r2,#4]

.autoregion HOOK_SPACE, HOOK_SPACE_END
.align 2
GroundStylePoints:
    // Exactly White's instructions from 0x08015E2A (r3 = style stats).
    // Called with BL (no push) so [sp,#0x10] is the caller's frame slot.
    ldrb    r0,[r3,#0x13]
    mov     r1,#0x46
    mul     r0,r1
    ldrb    r1,[r3,#0x12]
    mov     r2,#0x46
    mul     r1,r2
    add     r0,r0,r1
    str     r0,[sp,#0x10]
    bx      lr
.endautoregion
