// ---------------------------------------------------------------------------
// White-exclusive Giga chip artwork
//
// The chip data entries for NavRcycl/AlphArmS/Bass/Serenade/Balance are
// byte-identical in both ROMs except for the image/palette pointers, which in
// Blue point at the "no data" placeholder.  The original artwork is copied
// straight out of the user's White ROM at build time (nothing copyrighted is
// stored in this repository) and the two pointers are fixed up.  No other
// chip data field is touched.
// ---------------------------------------------------------------------------

.definelabel CHIP_DATA, 0x08011510       // 0x20 bytes per chip
.definelabel WHITE_GIGA_ART_SRC, 0x6F4460 // in the White ROM
.definelabel GIGA_ART_SIZE, 0x700
.definelabel GIGA_ART_STRIDE, 0x720      // image + 0x20 byte palette

.autoregion EXPANSION_START
.align 4
WhiteGigaArt:
    .import WHITE_ROM, WHITE_GIGA_ART_SRC, GIGA_ART_STRIDE*5
.endautoregion

.macro fix_white_giga_art, chip, index
    .org CHIP_DATA + chip*0x20 + 0x18
    .word WhiteGigaArt + GIGA_ART_STRIDE*index
    .word WhiteGigaArt + GIGA_ART_STRIDE*index + GIGA_ART_SIZE
.endmacro

fix_white_giga_art CHIP_NAVRCYCL,  0
fix_white_giga_art CHIP_ALPHARM_S, 1
fix_white_giga_art CHIP_BASS,      2
fix_white_giga_art CHIP_SERENADE,  3
fix_white_giga_art CHIP_BALANCE,   4
