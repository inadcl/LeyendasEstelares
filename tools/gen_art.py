#!/usr/bin/env python3
"""Genera el pixel art placeholder de res://art/ sin dependencias (solo stdlib).

Uso: python3 tools/gen_art.py [directorio_salida]
Los PNG resultantes se pueden sustituir por arte de un artista sin tocar el código.
"""
import os
import struct
import sys
import zlib

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art")
os.makedirs(OUT, exist_ok=True)

CLEAR = (0, 0, 0, 0)


def write_png(name, px):
    h, w = len(px), len(px[0])
    raw = b"".join(b"\x00" + bytes(c for p in row for c in p) for row in px)

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    with open(os.path.join(OUT, name + ".png"), "wb") as f:
        f.write(png)


def rnd(x, y, seed=0):
    """Ruido determinista en [0, 1)."""
    n = (x * 374761393 + y * 668265263 + seed * 2147483647) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65536.0


def rgb(c, a=255):
    return (c[0], c[1], c[2], a)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


# ---------------------------------------------------------------- hexágonos
HW, HH = 32, 36


def hex_inside(dx, dy, inset=0.0):
    ax = abs(dx)
    return ax <= 16 - inset and abs(dy) <= 18 - inset - 0.5625 * ax


def make_hex(fill):
    px = []
    for y in range(HH):
        row = []
        for x in range(HW):
            dx, dy = x + 0.5 - HW / 2, y + 0.5 - HH / 2
            if not hex_inside(dx, dy):
                row.append(CLEAR)
            elif not hex_inside(dx, dy, 1.4):
                base = fill(x, y)
                row.append(rgb(shade(base, 0.55)))
            else:
                row.append(rgb(fill(x, y)))
        px.append(row)
    return px


def f_llanura(x, y):
    base = (78, 118, 96)
    r = rnd(x, y, 1)
    if r < 0.12:
        return shade(base, 0.82)
    if r > 0.9:
        return shade(base, 1.22)
    if rnd(x // 2, y // 2, 9) > 0.93:
        return (110, 150, 108)
    return base


def f_roca(x, y):
    base = (116, 100, 94)
    patch = rnd(x // 4, y // 4, 3)
    c = shade(base, 0.85 if patch < 0.35 else (1.1 if patch > 0.75 else 1.0))
    r = rnd(x, y, 4)
    if r < 0.1:
        return shade(c, 0.75)
    if r > 0.93:
        return shade(c, 1.25)
    return c


def f_hielo(x, y):
    base = (150, 190, 212)
    if ((x + y) // 3) % 6 == 0 and rnd(x, y, 5) > 0.3:
        return (206, 232, 244)
    r = rnd(x, y, 6)
    if r < 0.1:
        return (118, 160, 190)
    return base


def f_crater(x, y):
    base = f_roca(x, y)
    dx, dy = x - 16, y - 19
    d = (dx * dx + dy * dy) ** 0.5
    if d < 6.5:
        return (52, 38, 42) if (dx + dy) > -3 else (74, 54, 58)
    if d < 9.0:
        return (152, 124, 112) if (dx + dy) < 0 else (86, 66, 64)
    return shade(base, 0.92)


CRACK = [(8, 6), (13, 12), (11, 17), (18, 21), (16, 27), (23, 31)]


def f_grieta(x, y):
    base = (26, 16, 34)
    if rnd(x, y, 7) > 0.92:
        base = (40, 24, 52)
    for (ax, ay), (bx, by) in zip(CRACK, CRACK[1:]):
        steps = max(abs(bx - ax), abs(by - ay))
        for i in range(steps + 1):
            px_ = ax + (bx - ax) * i / steps
            py_ = ay + (by - ay) * i / steps
            dist = ((x - px_) ** 2 + (y - py_) ** 2) ** 0.5
            if dist < 0.8:
                return (6, 4, 10)
            if dist < 1.7:
                return (92, 44, 124)
    return base


def f_fog(x, y):
    r = rnd(x, y, 8)
    if r > 0.985:
        return (58, 70, 108)
    return (24, 30, 52)


def make_ring(color, width):
    px = []
    for y in range(HH):
        row = []
        for x in range(HW):
            dx, dy = x + 0.5 - HW / 2, y + 0.5 - HH / 2
            if hex_inside(dx, dy, 0.6) and not hex_inside(dx, dy, 0.6 + width):
                row.append(rgb(color))
            else:
                row.append(CLEAR)
        px.append(row)
    return px


# ------------------------------------------------------------------ sprites
PAL = {
    ".": CLEAR, "k": (12, 14, 22), "g": (200, 208, 220), "G": (130, 140, 160),
    "w": (255, 255, 255), "c": (90, 220, 255), "b": (40, 90, 200), "B": (20, 40, 110),
    "r": (220, 70, 70), "y": (255, 214, 102), "o": (255, 150, 60),
    "p": (150, 110, 200), "P": (90, 60, 130), "n": (110, 220, 120), "N": (50, 130, 70),
    "d": (70, 52, 44),
}


def make_sprite(rows, extra=None):
    pal = dict(PAL)
    pal.update(extra or {})
    assert len(rows) == 16, "sprite con %d filas" % len(rows)
    px = []
    for i, r in enumerate(rows):
        assert len(r) == 16, "fila %d con %d columnas: %r" % (i, len(r), r)
        px.append([rgb(pal[ch]) if ch != "." else CLEAR for ch in r])
    return px


ASTRONAUT = [
    "................",
    ".....kkkkkk.....",
    "....kggggggk....",
    "...kgkkkkkkgk...",
    "...kgkccwckgk...",
    "...kgkcccckgk...",
    "....kggggggk....",
    ".....kkkkkk.....",
    "...kkaaaaaakk...",
    "..kkgaaaaaagkk..",
    "..kkgaakkaagkk..",
    "..kkgGGGGGGgkk..",
    "...kkGGGGGGkk...",
    "....kGGkkGGk....",
    "....kggkkggk....",
    "....kkkkkkkk....",
]

SHIP = [
    "................",
    ".......kk.......",
    "......kggk......",
    ".....kgggGk.....",
    ".....kgccGk.....",
    ".....kgggGk.....",
    "....kkgggGkk....",
    "...kggggggGGk...",
    "..kgggkkkkggGk..",
    "..kkkkkkkkkkkk..",
    "..k.k......k.k..",
    ".kk.k......k.kk.",
    "................",
    "................",
    "................",
    "................",
]

SIGNAL = [
    "................",
    "...y...oo...y...",
    "..y..y.oo.y..y..",
    "..y.y..oo..y.y..",
    "..y..y.oo.y..y..",
    "...y...oo...y...",
    ".......kk.......",
    "......kggk......",
    ".......kk.......",
    "......kggk......",
    ".......kk.......",
    ".....kggggk.....",
    "....kggggggk....",
    "....kkkkkkkk....",
    "................",
    "................",
]

RUINS = [
    "................",
    "................",
    "................",
    "..kkkkkkkkkkkk..",
    ".kppppppppppppk.",
    ".kPPPPPPPPPPPPk.",
    "..kkppkkkkppkk..",
    "...kppk..kppk...",
    "...kPPk..kPpk...",
    "...kppk..kppk...",
    "...kPPk...kk....",
    "...kppk.........",
    ".kkkkkkkkkkkkkk.",
    "................",
    "................",
    "................",
]

WRECK = [
    "................",
    "................",
    "..G....G........",
    "...G..G.G.......",
    "....G...G.......",
    "...kkkkkkk......",
    "..kggggggGkk....",
    ".kgggkkkgggGk...",
    ".kggkccckggGGk..",
    "kkgggkkkkGGkk...",
    ".kkkkkGGGkk.o...",
    "...kkkkkkk.oyo..",
    "..........ooo...",
    "................",
    "................",
    "................",
]

LIFE = [
    "................",
    "................",
    "....y.....y.....",
    "...yny...yny....",
    "....n.....n.....",
    "....N..y..N.....",
    ".....N.yny.N....",
    ".....N..n..N....",
    "......N.n.N.....",
    ".......NnN......",
    "...nn..NnN..nn..",
    "..nNNnnNNNnnNn..",
    ".dddddddddddddd.",
    "................",
    "................",
    "................",
]

BEACON = [
    "................",
    ".......yy.......",
    "......kppk......",
    "......kpck......",
    ".....kPpcbk.....",
    ".....kPpcbk.....",
    ".....kPpcbk.....",
    ".....kPpcbk.....",
    "....kkPpcbkk....",
    "....kPPpcbbk....",
    "...kkkkkkkkkk...",
    "..kGGGGGGGGGGk..",
    "..kkkkkkkkkkkk..",
    "................",
    "................",
    "................",
]


def make_stars(w=640, h=360):
    px = []
    for y in range(h):
        row = []
        for x in range(w):
            g = int(9 + 9 * y / h)
            c = (g, g + 2, g + 12)
            # nebulosa tenue con tramado
            neb = rnd(x // 24, y // 24, 21) * 0.6 + rnd(x // 9, y // 9, 22) * 0.4
            if neb > 0.72 and (x + y) % 2 == 0:
                c = (g + 6, g + 6, g + 26)
            r = rnd(x, y, 23)
            if r > 0.9985:
                c = (235, 240, 255)
            elif r > 0.996:
                c = (140, 156, 200)
            elif r > 0.992:
                c = (68, 78, 116)
            row.append(rgb(c))
        px.append(row)
    return px


def main():
    for name, fill in [("llanura", f_llanura), ("roca", f_roca), ("hielo", f_hielo),
                       ("crater", f_crater), ("grieta", f_grieta), ("fog", f_fog)]:
        write_png("tile_" + name, make_hex(fill))
    write_png("hl_hover", make_ring((255, 255, 255), 1.6))
    write_png("hl_reach", make_ring((255, 214, 102), 1.6))
    write_png("avatar_vance", make_sprite(ASTRONAUT, {"a": (60, 180, 170)}))
    write_png("avatar_okafor", make_sprite(ASTRONAUT, {"a": (236, 140, 60), "c": (255, 214, 102)}))
    write_png("ship", make_sprite(SHIP))
    write_png("poi_signal", make_sprite(SIGNAL))
    write_png("poi_ruins", make_sprite(RUINS))
    write_png("poi_wreck", make_sprite(WRECK))
    write_png("poi_life", make_sprite(LIFE))
    write_png("poi_beacon", make_sprite(BEACON))
    write_png("bg_stars", make_stars())
    print("Arte generado en", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
