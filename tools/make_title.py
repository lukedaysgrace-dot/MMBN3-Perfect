#!/usr/bin/env python3
"""
Builds the "BLUE + WHITE" title screen logo for MMBN3 Perfect.

Reads the two original ROMs from mmbn3/ and rebuilds the big word as
"BLUE+WHITE" from Capcom's own pixel art: Blue's "BLUE", White's "WHIT" and
White's final "E", whose arms still run into the original swoosh around the
"3". The screen is cut in half along the italic line through the "+": Blue's
title on the left, White's (grey plate and stripes) on the right. Letters are narrowed at full height in a deslanted
space, so the italic angle is kept. The plate, its border and the letter
outlines are redrawn to match the original. Writes:
    build/title_tiles.lz   (LZ77 8bpp tiles, loaded to VRAM tile 0x38)
    build/title_map.bin    (32x20 tile map)
    build/title_pal.bin    (240-colour palette: Blue's + White's greys in 208-239)
patches/title_screen.asm picks these up if they exist; otherwise the vanilla
title screen is kept.

Requires: Python 3, numpy, Pillow, scipy.
"""
import os, sys, struct
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'romdiff'))
sys.path.insert(0, HERE)
import paths, lz10

# where the title BG (BG2, 8bpp) lives in each ROM
LAYOUT = {
    'blue':  dict(tiles=0x7FBC30, map=0x7FF2B8, pal=0x7FBA30),
    'white': dict(tiles=0x7FC0D0, map=0x7FF6C4, pal=0x7FBED0),
}
TILE_BASE = 0x38

def load(rom, lay):
    tiles = bytes(lz10.gba_decompress(bytearray(rom[lay['tiles']:lay['tiles'] + 0x8000])))
    m = struct.unpack_from('<640H', rom, lay['map'])
    pal = np.array([[(c & 31) << 3, ((c >> 5) & 31) << 3, ((c >> 10) & 31) << 3]
                    for c in struct.unpack_from('<224H', rom, lay['pal'])], np.uint8)
    img = np.zeros((160, 240), np.uint8)
    for ty in range(20):
        for tx in range(30):
            t = (m[ty * 32 + tx] & 0x3FF) - TILE_BASE
            img[ty*8:ty*8+8, tx*8:tx*8+8] = np.frombuffer(tiles[t*64:t*64+64], np.uint8).reshape(8, 8)
    return img, pal, m

# The big word sits in rows 70-91 of BG2, its outline in rows 69 and 92.
# Letters are italic with a slope of ~0.48 px/row; working in a "deslanted"
# space (each row shifted by round(SLANT*(91-y))) makes stems vertical, so the
# words can be narrowed without changing the italic angle or the letter height.
R0, R1 = 70, 92
SLANT = 0.48
NAVY = np.array([40, 32, 104], np.float32)      # plate fill
DARK = np.array([32, 24, 104], np.float32)      # plate under a gap, bottom row
RING = np.array([40, 48, 144], np.float32)      # 1px light outline round letters
RING_TOP = np.array([56, 72, 152], np.float32)  # outline above a letter
RING_BOT = np.array([160, 144, 40], np.float32) # olive edge under a letter (row 92)
LEFT = 37        # deslanted column where "B" starts (plate border is 33-36)
CUT = 166        # deslanted column where the original E's arms run on into the swoosh

def kshift(y):
    return int(round(SLANT * (91 - y)))

def deslant(a):
    out = np.zeros_like(a)
    for y in range(R0 - 1, R1 + 1):
        k = kshift(y)
        out[y, :a.shape[1] - k] = a[y, k:]
    return out

def warm_of(rgb):
    return ((rgb[..., 0] - rgb[..., 2]) > 40) & (rgb[..., 1] > rgb[..., 0] * 0.3)

def letters(rgb):
    lab, k = ndimage.label(warm_of(rgb)[R0:R1])
    comps = []
    for i in range(1, k + 1):
        ys, xs = np.where(lab == i)
        if len(ys) > 40:
            comps.append((xs.min(), i))
    return lab, comps

def word_mask(rgb, lo, hi):
    """Mask (full image size) of the big-word letter components starting in [lo, hi]."""
    lab, comps = letters(rgb)
    m = np.zeros(rgb.shape[:2], bool)
    m[R0:R1] = np.isin(lab, [i for (a, i) in comps if lo <= a <= hi])
    return m

def piece(d, m, x0, x1):
    """Colour (premultiplied) and alpha of deslanted columns [x0, x1) of the word rows."""
    a = m[R0:R1, x0:x1].astype(np.float32)
    return d[R0:R1, x0:x1] * a[..., None], a

def squeeze(col, a, sx):
    h, w = a.shape; nw = max(1, int(round(w * sx)))
    rs = lambda ch: np.array(Image.fromarray(ch.astype(np.float32), 'F').resize((nw, h), Image.BOX))
    return np.stack([rs(col[..., c]) for c in range(3)], 2), rs(a)

def compose(ib, pb, iw, pw, gap=2, plus_w=12, plus_bar=4):
    B = pb[ib].astype(np.float32); Wc = pw[iw].astype(np.float32)
    dB = deslant(B); dW = deslant(Wc)
    mB = deslant(word_mask(B, 38, 150).astype(np.uint8)).astype(bool)   # B, L, U, E(+swoosh)
    mW = deslant(word_mask(Wc, 40, 150).astype(np.uint8)).astype(bool)  # W, H, I, T, E(+swoosh)
    e0 = 142                                    # Blue's E stem (deslanted)
    t1 = 149                                    # end of White's T, start of its E
    p1 = piece(dB, mB, LEFT, CUT)               # "BLUE"
    p2 = piece(dW, mW, 36, t1)                  # "WHIT"
    p3 = piece(dW, mW, t1, CUT)                 # White's final "E", whose arms join White's swoosh
    room = CUT - LEFT - 2 * gap - plus_w - 1
    sx = room / (p1[1].shape[1] + p2[1].shape[1] + p3[1].shape[1])
    s1, s2, s3 = squeeze(*p1, sx), squeeze(*p2, sx), squeeze(*p3, sx)
    # lay out left to right in deslanted space; the last E ends exactly at CUT
    H = R1 - R0
    C = np.zeros((H, 240, 3), np.float32); A = np.zeros((H, 240), np.float32)
    def put(p, x):
        c, a = p; w = a.shape[1]
        C[:, x:x+w] = c + C[:, x:x+w] * (1 - a[..., None]); A[:, x:x+w] = a + A[:, x:x+w] * (1 - a)
        return x + w
    x = put(s1, LEFT)
    xp = x + gap
    x3 = CUT - s3[1].shape[1]
    x2 = x3 - 1 - s2[1].shape[1]
    put(s2, x2); put(s3, x3)
    xp = (x + x2 + 4 - plus_w) // 2            # centre the "+" between the words (W's left stroke leans in, hence +4)
    if os.environ.get('TITLE_DEBUG'): print('sx=%.3f word1 end=%d word2 start=%d plus=%d final E=%d..%d' % (sx, x, x2, xp, x3, CUT))
    # "+" in the letters' own per-row gradient
    wa = mB[R0:R1, LEFT:CUT]
    grad = (dB[R0:R1, LEFT:CUT] * wa[..., None]).sum(1) / np.maximum(wa.sum(1), 1)[:, None]
    mid0, mid1 = 79 - R0, 83 - R0              # same rows as the E's middle arm
    vx = xp + (plus_w - plus_bar) // 2
    for y in range(4, H - 4):
        xs = range(xp, xp + plus_w) if mid0 <= y < mid1 else range(vx, vx + plus_bar)
        for xx in xs:
            C[y, xx] = grad[y]; A[y, xx] = 1
    split = xp + plus_w // 2                   # deslanted column through the middle of the "+"
    solid = A > 0.5
    S = np.zeros((H + 2, 240), bool); S[1:H+1] = solid
    up = np.zeros_like(S); up[:-1] = S[1:]      # letter directly below
    dn = np.zeros_like(S); dn[1:] = S[:-1]      # letter directly above
    ring = ndimage.binary_dilation(S, structure=ndimage.generate_binary_structure(2, 1)) & ~S

    def build(base, dbase, sch):
        """Plate rebuilt in deslanted columns [LEFT, CUT), rows 69..93, letters on top."""
        band = np.empty((H + 2, 240, 3), np.float32)
        band[:] = sch['navy']
        band[0] = dbase[R0 - 1]
        old_ring = ((band[0] - sch['navy']) ** 2).sum(1) < 1e-3
        for c in sch['old_ring']:
            old_ring |= ((band[0] - c) ** 2).sum(1) < 1e-3
        band[0][old_ring] = sch['navy']         # outline of the old letters, not the "ball" emblem
        band[H + 1] = sch['dark']
        band[ring] = sch['ring']
        band[ring & up] = sch['ring_top']
        band[H + 1][dn[H + 1]] = sch['ring_bot']
        a = A[..., None]
        band[1:H+1] = C + (1 - a) * band[1:H+1]
        out = base.copy()
        for j, y in enumerate(range(R0 - 1, R1 + 1)):
            k = kshift(y)
            out[y, LEFT + k:CUT + k] = band[j, LEFT:CUT]
        # bottom border row 93 is a shade lighter under letters than under gaps
        for x in range(LEFT, CUT):
            if any((base[93, x] == c).all() for c in sch['row93']):
                out[93, x] = sch['row93'][0] if dn[H + 1, x] else sch['row93'][1]
        return out

    blue_sch = dict(navy=NAVY, dark=DARK, ring=RING, ring_top=RING_TOP, ring_bot=RING_BOT,
                    row93=[np.float32([104, 104, 128]), np.float32([80, 64, 80])],
                    old_ring=[c for c in np.unique(B[R0 - 1].reshape(-1, 3), axis=0)
                              if c[2] >= 120 and c[2] - c[0] >= 50])
    # White's equivalents: the colour White uses where Blue uses each plate colour
    wb = Wc[R0 - 1:R1 + 2, 30:236].reshape(-1, 3); bb = B[R0 - 1:R1 + 2, 30:236].reshape(-1, 3)
    nonwarm = ~warm_of(wb) & ~warm_of(bb)
    def wmap(c):
        sel = np.abs(bb - c).sum(1) == 0
        if (sel & nonwarm).any():
            sel &= nonwarm
        u, n = np.unique(wb[sel], axis=0, return_counts=True)
        return u[n.argmax()].astype(np.float32)
    white_sch = {k: (wmap(v) if not isinstance(v, list) else [wmap(c) for c in v]) for k, v in blue_sch.items()}
    if os.environ.get('TITLE_DEBUG'): print({k: (v.tolist() if not isinstance(v, list) else [c.tolist() for c in v]) for k, v in white_sch.items()})
    outB = build(B, dB, blue_sch)
    outW = build(Wc, dW, white_sch)
    # cut the whole screen in two along the italic line through the "+":
    # Blue's title on the left, White's on the right
    out = outB.copy()
    for y in range(160):
        xs = split + int(round(SLANT * (91 - y)))
        if xs < 240:
            out[y, max(xs, 0):] = outW[y, max(xs, 0):]
    # White's bottom border has cream/olive highlight segments that matched its
    # old letter spacing; on the cut-in-half title they show as a lighter bar
    # under "WHIT", so use the border's own orange/peach all the way to the swoosh
    for y, col in ((93, (248, 120, 32)), (94, (224, 192, 168))):
        xs = split + int(round(SLANT * (91 - y)))
        out[y, xs:182] = col
    return out

def quantize(out, ib, pb, free=range(208, 240)):
    """Map to Blue's title palette; colours it can't show (White's greys) go in unused slots.
    Slots 207-239 are empty on the title screen (the text layers use banks 0 and 15);
    patches/title_screen.asm loads 240 entries instead of 224 so 224-239 can be used."""
    used = np.unique(ib)
    pal = np.zeros((max(224, max(free) + 1), 3), np.float32); pal[:224] = pb
    cols, inv, cnt = np.unique(out.reshape(-1, 3), axis=0, return_inverse=True, return_counts=True)
    inv = inv.reshape(-1)
    d = lambda P: ((cols[:, None, :] - P[None]) ** 2).sum(2)
    err = d(pal[used]).min(1)
    slots = list(free)
    for slot in slots:                          # greedy: add the colour that removes the most error
        gain = (np.maximum(0, err[None, :] - d(cols).T) * cnt[None, :]).sum(1)
        best = gain.argmax()
        if gain[best] <= 0:
            break
        pal[slot] = cols[best]
        err = np.minimum(err, d(cols[best:best + 1])[:, 0])
    allowed = np.concatenate([used, np.array(slots)])
    choice = allowed[d(pal[allowed]).argmin(1)]
    new = choice[inv].reshape(out.shape[:2]).astype(np.uint8)
    # anything that matched exactly before must keep its original index
    same = (pb[ib].astype(np.float32) == out).all(2)
    new[same] = ib[same]
    return new, pal

def encode(img):
    tiles = []; index = {}; m = [0] * 640
    for ty in range(20):
        for tx in range(30):
            t = img[ty*8:ty*8+8, tx*8:tx*8+8].tobytes()
            if t not in index:
                index[t] = len(tiles); tiles.append(t)
            m[ty*32 + tx] = TILE_BASE + index[t]
    for ty in range(20):                         # off-screen columns 30/31: keep a blank-ish tile
        m[ty*32 + 30] = m[ty*32 + 31] = m[ty*32 + 29]
    assert TILE_BASE + len(tiles) <= 0x200, 'too many tiles (%d)' % len(tiles)
    return b''.join(tiles), struct.pack('<640H', *m), len(tiles)

def main():
    blue = open(paths.BLUE, 'rb').read(); white = open(paths.WHITE, 'rb').read()
    ib, pb, _ = load(blue, LAYOUT['blue']); iw, pw, _ = load(white, LAYOUT['white'])
    new, pal = quantize(compose(ib, pb, iw, pw), ib, pb)
    tiles, mp, n = encode(new)
    os.makedirs(os.path.join(paths.REPO, 'build'), exist_ok=True)
    open(os.path.join(paths.REPO, 'build', 'title_tiles.lz'), 'wb').write(bytes(lz10.gba_compress(bytearray(tiles))))
    open(os.path.join(paths.REPO, 'build', 'title_map.bin'), 'wb').write(mp)
    q = np.clip(pal, 0, 255).astype(int) >> 3
    open(os.path.join(paths.REPO, 'build', 'title_pal.bin'), 'wb').write(
        struct.pack('<%dH' % len(q), *[int(r | (g << 5) | (b << 10)) for r, g, b in q]))
    Image.fromarray(np.clip(pal, 0, 255).astype(np.uint8)[new]).resize((480, 320), Image.NEAREST).save(os.path.join(paths.REPO, 'build', 'title_preview.png'))
    print('title: %d tiles, written to build/' % n)

if __name__ == '__main__':
    main()
