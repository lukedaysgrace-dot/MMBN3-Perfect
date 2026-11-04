// ---------------------------------------------------------------------------
// Title screen: "BLUE + WHITE"
//
// The title screen is one 8bpp background: tiles LZ77 at 0x087FBC30 -> VRAM
// tile 0x38, 32x20 map at 0x087FF2B8, 224-colour palette at 0x087FBA30.
// tools/make_title.py builds a new tile set, map and palette from the user's
// two ROMs: the word "BLUE+WHITE" in Capcom's own logo letters, and the screen
// cut in half along the italic line through the "+" - Blue's title on the
// left, White's (grey plate and background) on the right. White's greys need
// extra palette entries, so 240 entries are loaded instead of 224 (slots
// 224-239 are unused on this screen), and the menu's dimming effect covers
// those 240 colours instead of the first 208.
// If build/ has not been generated, the vanilla title is kept.
// ---------------------------------------------------------------------------
.if fileexists("build/title_tiles.lz") && fileexists("build/title_map.bin") && fileexists("build/title_pal.bin")
.autoregion EXPANSION_START
.align 4
TitlePal:
    .incbin "build/title_pal.bin"
.align 4
TitleTiles:
    .incbin "build/title_tiles.lz"
.align 4
TitleMap:
    .incbin "build/title_map.bin"
.endautoregion
.org 0x08022614
    .word TitleTiles            // was 0x087FBC30
.org 0x08022664
    .word TitleMap              // was 0x087FF2B8
.org 0x080225C2
    mov r2,#0x1E                // palette size 0x1E0 (240 colours), was 0x1C
.org 0x0802263C
    .word TitlePal              // was 0x087FBA30
.org 0x08021F12
    .byte 0x0F                  // menu dims 15 palette banks (240 colours), was 13 (208)
.endif
