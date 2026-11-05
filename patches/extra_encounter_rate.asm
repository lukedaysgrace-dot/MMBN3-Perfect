// ---------------------------------------------------------------------------
// Optional extra (NOT in either original version): random encounters halved.
//
// The overworld encounter check (0x080146BC) runs every 64 units of movement
// and starts a battle when (random & 0x1F) < threshold, where the threshold
// comes from the area's tier and how far you've walked since the last battle
// (table at 0x0800D26C, values 0-28). Masking with 0x3F instead rolls 0-63
// against the same thresholds, so every check has exactly half the vanilla
// chance (e.g. 37.5% -> 18.75%). Nothing else about encounters changes.
// ---------------------------------------------------------------------------
.org 0x0801472A
    mov r1,#0x3F                // was #0x1F
