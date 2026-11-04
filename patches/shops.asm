// ---------------------------------------------------------------------------
// Shops, BugFrag shops and Higsby's Chip Order
//
// All 23 shop inventories live in one ROM pool (0x08044BB0, 8 slots of
// 8 bytes per shop; shop 22 = Higsby's 320-entry Chip Order) that is copied
// into save RAM (0x020035E0) on New Game.  Both versions use the same layout;
// only the items differ.
//
// Only chip+code combinations that White sells and that cannot be obtained
// anywhere in Blue (incl. the new drop-table mix) are added.  They go into an
// empty slot of the *same* shop with White's original price and stock.  Where
// the Blue shop is already full, the item goes to Higsby's Chip Order instead
// (13 unused entries at the end of the list).  No Blue item is moved or
// replaced.
//
// NOTE: the pool is copied to RAM on New Game, so these additions appear in
// new save files.
// ---------------------------------------------------------------------------

.definelabel SHOP_POOL, 0x08044BB0

.macro shop_chip, shop, slot, chip, code, stock, price
    .org SHOP_POOL + ((shop*8)+slot)*8
    .byte 2, stock
    .halfword chip
    .byte code, 0
    .halfword price
.endmacro

// shop, slot, chip, code, stock, price (x100 zenny / BugFrags)
// Values are White's own entry for the same shop.
shop_chip 0, 6, 0x0AD, 11, 3, 5       // Barrier L
shop_chip 0, 7, 0x079, 26, 3, 5       // Recov10 *
shop_chip 1, 6, 0x081, 11, 3, 6       // PanlGrab L
shop_chip 1, 7, 0x0B5, 26, 3, 10      // GrassStg *
shop_chip 3, 7, 0x08F, 0, 3, 10       // Wind A
shop_chip 4, 6, 0x0B3, 26, 1, 80      // LavaStge *
shop_chip 4, 7, 0x0AE, 26, 1, 50      // Barr100 *
shop_chip 8, 7, 0x0B7, 18, 1, 28      // MetlStge S
shop_chip 10, 6, 0x130, 26, 1, 200    // NavRcycl *  (UN2 BugFrag shop, next to FoldrBak)
shop_chip 10, 7, 0x040, 26, 1, 20     // Hammer *
shop_chip 13, 7, 0x0B1, 25, 1, 130    // NrthWind Z

// DeltaRay Z (Blue) and Balance Y (White) are, in vanilla, only obtainable as
// the fallback prize of a *link* battle (0x08008400).  Single-player route:
// sold in the Undernet 6 BugFrag shop, the BugFrag shop that has room,
// at the same 300 price both versions list for them in the Chip Order data.
// Shop 12 - Undernet 6 BugFrag shop
shop_chip 12, 6, CHIP_DELTARAY, CODE_Z, 1, 300
shop_chip 12, 7, CHIP_BALANCE,  CODE_Y, 1, 300

// Higsby's Chip Order (shop 22), first unused entry is #307.  These White
// shop items had no free slot in the matching Blue shop.
shop_chip 22, 307, 0x097, 13, 1, 50   // Pawn N      (White: shop 11)
shop_chip 22, 308, 0x07F, 22, 1, 100  // Recov200 W  (White: shop 11)
shop_chip 22, 309, 0x026, 4, 1, 80    // VarSwrd E   (White: shop 13)
shop_chip 22, 310, 0x098, 21, 1, 100  // Knight V    (White: shop 13)
shop_chip 22, 311, 0x063, 12, 1, 60   // TimeBomb M  (White: Higsby's shop 18)
shop_chip 22, 312, 0x02A, 17, 1, 140  // AirSwrd R   (White: Higsby's shop 18)
