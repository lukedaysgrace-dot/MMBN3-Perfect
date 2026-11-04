// ---------------------------------------------------------------------------
// Shared definitions
// ---------------------------------------------------------------------------

// Vanilla Blue routines
.definelabel SetFlag,        0x08021CF0   // r0 = flag >> 8, r1 = flag & 0xFF
.definelabel ClearFlag,      0x08021D0C
.definelabel CheckFlag,      0x08021D28   // returns Z set when flag is clear
.definelabel GiveChip,       0x08011280   // r0 = chip, r1 = code, r2 = amount

// Free space.
// 0x08235154-0x08235EFF is 0xFF padding inside the original ROM and is in
// BL range of all game code, so small hooks/veneers go there.
.definelabel HOOK_SPACE,     0x08235200
.definelabel HOOK_SPACE_END, 0x08235F00
// Larger data is appended after the original 8 MB ROM.
.definelabel EXPANSION_START, 0x08800000

// Chip IDs
.definelabel CHIP_DELTARAY,  0x12E
.definelabel CHIP_FOLDRBAK,  0x12F
.definelabel CHIP_NAVRCYCL,  0x130
.definelabel CHIP_ALPHARM_S, 0x131
.definelabel CHIP_BASS,      0x132
.definelabel CHIP_SERENADE,  0x133
.definelabel CHIP_BALANCE,   0x134
.definelabel CHIP_DARKAURA,  0x135
.definelabel CHIP_ALPHARM_O, 0x136
.definelabel CHIP_BASS_PLUS, 0x137
.definelabel CHIP_BASS_GS,   0x138

// Chip codes (A = 0 ... Z = 25, * = 26)
.definelabel CODE_A, 0
.definelabel CODE_S, 18
.definelabel CODE_V, 21
.definelabel CODE_X, 23
.definelabel CODE_Y, 24
.definelabel CODE_Z, 25
.definelabel CODE_STAR, 26

.defineregion HOOK_SPACE, HOOK_SPACE_END-HOOK_SPACE, 0xFF
.defineregion EXPANSION_START, 0x100000
