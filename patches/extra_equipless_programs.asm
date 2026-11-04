// ---------------------------------------------------------------------------
// OPTIONAL (not part of vanilla Blue or White) - enabled at the owner's request
//
// Press and EngyChng work in the overworld when you merely *own* the
// NaviCust program, instead of only when it is installed in the NaviCust.
// Equipping them still works exactly as before.
//
// Every place that asks "is effect 0x28 (Press) / 0x24 (EngyChng) active?"
// via 0x08047334 for overworld gaps/barriers is redirected to a check that
// returns 1 if the effect is active OR the program is in the inventory
// (0x02001A80 + program*4, 4 colour counts; Press = 0x14, EngyChng = 0x15).
// Fixes the previous version of this patch, which compared the address of
// the counter instead of its value and executed a data word as code.
// ---------------------------------------------------------------------------

.definelabel NaviCustEffect, 0x08047334
.definelabel NCP_INV_PRESS,  0x02001AD0
.definelabel NCP_INV_ENGY,   0x02001AD4

// Each site is "mov r0,#effect / bl 0x08047334 / cmp r0,#1"; replace the
// first 6 bytes with "bl hook / nop".
.macro press_site, addr
    .org addr
    bl      PressAvailable
    nop
.endmacro
.macro engy_site, addr
    .org addr
    bl      EngyChngAvailable
    nop
.endmacro

press_site 0x0812D93A       // Press gap: shrink-and-pass
press_site 0x0812D980       // Press gap: alternate exit
engy_site  0x0802A392       // EngyChng barrier check
engy_site  0x080F546C       // map-object EngyChng checks
engy_site  0x080F54AE
engy_site  0x080F54FA

.autoregion HOOK_SPACE, HOOK_SPACE_END
.align 2
PressAvailable:
    push    {lr}
    mov     r0,#0x28
    ldr     r1,=NCP_INV_PRESS
    b       ProgramAvailable
EngyChngAvailable:
    push    {lr}
    mov     r0,#0x24
    ldr     r1,=NCP_INV_ENGY
ProgramAvailable:
    push    {r1}
    bl      NaviCustEffect      // original check (equipped)
    pop     {r1}
    cmp     r0,#1
    beq     @@done
    ldr     r0,[r1]             // any colour of the program owned?
    cmp     r0,#0
    beq     @@done              // r0 = 0
    mov     r0,#1
@@done:
    pop     {pc}
    .pool
.endautoregion
