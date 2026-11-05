// ---------------------------------------------------------------------------
// Optional extra (NOT in either original version): random-encounter outliers
// brought down to the normal rate. Same approach as MMBN2 Restored.
//
// Encounter check 0x080146BC: every 64 units of movement it starts a battle
// when (random & 0x1F) < curve[checks since last battle][area level]
// (curve 0x0800D26C, 17 x 8 bytes; area levels 0x0800D2F4, 16 bytes per Net
// group from 0x80, index (group-0x80)*16 + sub-map; level 7 = no encounters).
//
// Real maps in vanilla: the main Net (groups 0x80-0x83) is level 6 and the
// comp/object areas (0x88, 0x8A, 0x8C, 0x8D) are level 5. Only four real maps
// are busier, and only those are changed, to level 5:
//   0x83 sub-map 4      (red WWW area, AlphaBug viruses)   4 -> 5
//   0x8C sub-maps 13-15 (comps)                            3 -> 5
// All other level-3 entries are unused slots (no map handler) and are left
// alone. The curve and the check interval are unchanged.
// ---------------------------------------------------------------------------
ENC_LEVELS equ 0x0800D2F4

.macro set_level, group, sub, old, new
    .if readu8(BLUE_ROM, ENC_LEVELS - 0x08000000 + (group - 0x80) * 16 + sub) != old
        .error "extra_encounter_rate: unexpected original encounter level (not a clean US Blue ROM?)"
    .endif
    .org ENC_LEVELS + (group - 0x80) * 16 + sub
    .byte new
.endmacro

set_level 0x83,  4, 4, 5
set_level 0x8C, 13, 3, 5
set_level 0x8C, 14, 3, 5
set_level 0x8C, 15, 3, 5
