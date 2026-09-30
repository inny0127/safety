#!/usr/bin/env python3
"""Rewrite the RGB colours in a Chromium PDF as plain CMYK.

The accent (#FFF200) becomes pure yellow 0/0/1/0, every neutral becomes black ink only
(K = 1 - grey). Used for the two-ink print version so the printer never mixes inks.
    python3 cmyk.py in.pdf out.pdf
"""
import re
import sys

import pymupdf

ACCENT = (1.0, 242 / 255, 0.0)
OP = re.compile(rb'(?<![\w.])(-?\d*\.?\d+)\s+(-?\d*\.?\d+)\s+(-?\d*\.?\d+)\s+(rg|RG)\b')


def conv(m):
    r, g, b = (float(x) for x in m.group(1, 2, 3))
    op = b'k' if m.group(4) == b'rg' else b'K'
    if max(abs(r - ACCENT[0]), abs(g - ACCENT[1]), abs(b - ACCENT[2])) < 0.03:
        c = (0, 0, 1, 0)
    else:
        if max(r, g, b) - min(r, g, b) > 0.03:
            raise SystemExit(f'non-neutral colour left in PDF: {r:.3f} {g:.3f} {b:.3f}')
        c = (0, 0, 0, round(1 - (r + g + b) / 3, 4))
    return (' '.join(f'{v:g}' for v in c)).encode() + b' ' + op


def main(src, dst):
    doc = pymupdf.open(src)
    changed = 0
    for x in range(1, doc.xref_length()):
        if not doc.xref_is_stream(x):
            continue
        try:
            data = doc.xref_stream(x)
        except Exception:
            continue
        if data is None or (b' rg' not in data and b' RG' not in data):
            continue
        new, n = OP.subn(conv, data)
        if n:
            doc.update_stream(x, new)
            changed += n
    doc.save(dst, garbage=4, deflate=True)
    print(f'{changed} colour operators rewritten -> {dst}')


if __name__ == '__main__':
    main(*sys.argv[1:3])
