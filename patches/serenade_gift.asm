// ---------------------------------------------------------------------------
// Serenade's gift for holding every timed-battle record (Secret Area)
//
// Text archive 0x087B2864, script 24 checks flag 0x125E ("this is Blue"):
// Blue jumps to script 27 and gives DarkAura A, White continues and gives
// Serenade S.  The combined script gives both, in one sitting, using the
// original command bytes of scripts 24 and 27 (Serenade S first, then
// DarkAura A); the one-time flag 0x09E4 and every other check are unchanged.
//
// The archive is uncompressed, so it is copied to expansion space with the
// new script appended and script 24's table entry pointed at it.  Only byte
// ranges are referenced here; the text itself comes from the user's ROM.
// ---------------------------------------------------------------------------

.definelabel TIMED_ARCHIVE,      0x7B2864   // file offset
.definelabel TIMED_ARCHIVE_SIZE, 0x861
.definelabel TA_S24, 0x63C                  // script 24 offset in archive
.definelabel TA_S27, 0x787                  // script 27 offset in archive

.autoregion EXPANSION_START
.align 4
TimedBattleArchive:
    .import BLUE_ROM, TIMED_ARCHIVE, TIMED_ARCHIVE_SIZE
    .align 4
TimedBattleScript24:
    .import BLUE_ROM, TIMED_ARCHIVE+TA_S24,        16       // flag 0x9E3 / 0x9E4 checks, set 0x9E4
    // (6-byte "checkFlag 0x125E -> script 27" dropped here)
    .import BLUE_ROM, TIMED_ARCHIVE+TA_S24+22,     136-22   // "...a gift from Serenade!" + Serenade S
    .import BLUE_ROM, TIMED_ARCHIVE+TA_S27+61,     114-61   // DarkAura A (from Blue's script 27)
    .import BLUE_ROM, TIMED_ARCHIVE+TA_S24+136,    180-136  // "Timed battles are available any time!"
.endautoregion

// script table entry 24 inside the relocated copy
.org TimedBattleArchive + 24*2
    .halfword TimedBattleScript24 - TimedBattleArchive

// repoint both references to the archive
.org 0x0812A34C
    .word TimedBattleArchive
.org 0x0812A570
    .word TimedBattleArchive
