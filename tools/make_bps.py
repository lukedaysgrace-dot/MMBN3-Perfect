#!/usr/bin/env python3
"""Creates release/MMBN3-Perfect.bps (clean Blue (USA) ROM -> built ROM) and verifies it."""
import os, sys, zlib, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import paths

def vint(n):
    out = bytearray()
    while True:
        x = n & 0x7F; n >>= 7
        if n == 0:
            out.append(0x80 | x); return out
        out.append(x); n -= 1

def make(src, dst):
    p = bytearray(b'BPS1') + vint(len(src)) + vint(len(dst)) + vint(0)
    i = 0; n = len(dst)
    def same(k): return k < len(src) and src[k] == dst[k]
    while i < n:
        if same(i):
            j = i
            while j < n and same(j): j += 1
            p += vint(((j - i - 1) << 2) | 0)              # SourceRead
            i = j
        else:
            j = i
            while j < n:                                    # literal run until >=8 matching bytes follow
                if same(j) and all(same(k) for k in range(j, min(n, j + 8))): break
                j += 1
            p += vint(((j - i - 1) << 2) | 1) + dst[i:j]   # TargetRead
            i = j
    p += zlib.crc32(src).to_bytes(4, 'little') + zlib.crc32(dst).to_bytes(4, 'little')
    p += zlib.crc32(p).to_bytes(4, 'little')
    return bytes(p)

def apply(src, patch):
    assert patch[:4] == b'BPS1'
    pos = 4
    def rd():
        nonlocal pos
        data = 0; shift = 1
        while True:
            x = patch[pos]; pos += 1
            data += (x & 0x7F) * shift
            if x & 0x80: return data
            shift <<= 7; data += shift
    ss, ts, ms = rd(), rd(), rd(); pos += ms
    out = bytearray(); srel = trel = 0
    while pos < len(patch) - 12:
        d = rd(); cmd = d & 3; ln = (d >> 2) + 1
        if cmd == 0: out += src[len(out):len(out) + ln]
        elif cmd == 1: out += patch[pos:pos + ln]; pos += ln
        elif cmd == 2:
            o = rd(); srel += (-1 if o & 1 else 1) * (o >> 1); out += src[srel:srel + ln]; srel += ln
        else:
            o = rd(); trel += (-1 if o & 1 else 1) * (o >> 1)
            for _ in range(ln): out.append(out[trel]); trel += 1
    assert zlib.crc32(src) == int.from_bytes(patch[-12:-8], 'little'), 'wrong source ROM'
    assert zlib.crc32(out) == int.from_bytes(patch[-8:-4], 'little')
    return bytes(out)

if __name__ == '__main__':
    src = open(paths.BLUE, 'rb').read(); dst = open(paths.OUT_ROM, 'rb').read()
    assert hashlib.md5(src).hexdigest() == '6fe31df0144759b34ad666badaacc442', 'not a clean Blue (USA) ROM'
    patch = make(src, dst)
    assert apply(src, patch) == dst
    os.makedirs(os.path.join(paths.REPO, 'release'), exist_ok=True)
    out = os.path.join(paths.REPO, 'release', 'MMBN3-Perfect.bps')
    open(out, 'wb').write(patch)
    print('wrote %s (%d bytes); patched ROM md5 %s, crc32 %08X' % (out, len(patch), hashlib.md5(dst).hexdigest(), zlib.crc32(dst)))
