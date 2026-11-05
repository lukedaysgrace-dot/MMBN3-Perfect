// MMBN3 Perfect - Blue + White definitive edition
// Build with armips (https://github.com/Kingcom/armips):   armips main.asm
// Requires the two original US ROMs in the mmbn3/ folder (see README).

.gba
BLUE_ROM equ "mmbn3/Mega Man - Battle Network 3 - Blue Version (USA).gba"
WHITE_ROM equ "mmbn3/Mega Man - Battle Network 3 - White Version (USA).gba"

.open "mmbn3/Mega Man - Battle Network 3 - Blue Version (USA).gba", "MMBN3 - Perfect Version.gba", 0x08000000

.include "patches/common.asm"
.include "patches/ground_style.asm"
.include "patches/giga_legality.asm"
.include "patches/white_giga_art.asm"
.include "patches/white_gigas.asm"
.include "patches/drop_tables.asm"
.include "patches/shops.asm"
.include "patches/serenade_gift.asm"
.include "patches/mistman.asm"
.include "patches/title_screen.asm"

// ---- Optional extras (NOT vanilla Blue/White) - comment out to disable ----
.include "patches/extra_equipless_programs.asm"
.include "patches/extra_punk_chip.asm"
.include "patches/extra_encounter_rate.asm"


.close
