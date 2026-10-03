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


BIOMES = {
    "frost": {"llanura": (78, 118, 96), "roca": (116, 100, 94), "hielo": (150, 190, 212),
              "crater_in": (52, 38, 42), "crater_rim": (152, 124, 112), "grieta_crack": (92, 44, 124),
              "grieta_base": (26, 16, 34), "tuft": (110, 150, 108)},
    "dust": {"llanura": (196, 160, 104), "roca": (150, 84, 60), "hielo": (228, 214, 186),
             "crater_in": (70, 34, 26), "crater_rim": (208, 140, 84), "grieta_crack": (255, 128, 40),
             "grieta_base": (40, 20, 16), "tuft": (216, 184, 124)},
    "verdant": {"llanura": (58, 118, 66), "roca": (84, 96, 84), "hielo": (56, 122, 164),
                "crater_in": (24, 56, 50), "crater_rim": (96, 168, 120), "grieta_crack": (80, 220, 200),
                "grieta_base": (10, 24, 30), "tuft": (96, 170, 96)},
}


def f_llanura(pal):
    base = pal["llanura"]

    def f(x, y):
        r = rnd(x, y, 1)
        if r < 0.12:
            return shade(base, 0.82)
        if r > 0.9:
            return shade(base, 1.22)
        if rnd(x // 2, y // 2, 9) > 0.93:
            return pal["tuft"]
        return base
    return f


def f_roca(pal):
    base = pal["roca"]

    def f(x, y):
        patch = rnd(x // 4, y // 4, 3)
        c = shade(base, 0.85 if patch < 0.35 else (1.1 if patch > 0.75 else 1.0))
        r = rnd(x, y, 4)
        if r < 0.1:
            return shade(c, 0.75)
        if r > 0.93:
            return shade(c, 1.25)
        return c
    return f


def f_hielo(pal):
    base = pal["hielo"]

    def f(x, y):
        if ((x + y) // 3) % 6 == 0 and rnd(x, y, 5) > 0.3:
            return shade(base, 1.28)
        if rnd(x, y, 6) < 0.1:
            return shade(base, 0.78)
        return base
    return f


def f_crater(pal):
    rock = f_roca(pal)

    def f(x, y):
        dx, dy = x - 16, y - 19
        d = (dx * dx + dy * dy) ** 0.5
        if d < 6.5:
            return pal["crater_in"] if (dx + dy) > -3 else shade(pal["crater_in"], 1.4)
        if d < 9.0:
            return pal["crater_rim"] if (dx + dy) < 0 else shade(pal["crater_rim"], 0.55)
        return shade(rock(x, y), 0.92)
    return f


CRACK = [(8, 6), (13, 12), (11, 17), (18, 21), (16, 27), (23, 31)]


def f_grieta(pal):
    def f(x, y):
        base = pal["grieta_base"]
        if rnd(x, y, 7) > 0.92:
            base = shade(base, 1.5)
        for (ax, ay), (bx, by) in zip(CRACK, CRACK[1:]):
            steps = max(abs(bx - ax), abs(by - ay))
            for i in range(steps + 1):
                px_ = ax + (bx - ax) * i / steps
                py_ = ay + (by - ay) * i / steps
                dist = ((x - px_) ** 2 + (y - py_) ** 2) ** 0.5
                if dist < 0.8:
                    return (6, 4, 10)
                if dist < 1.7:
                    return pal["grieta_crack"]
        return base
    return f


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



# ---------------------------------------------------------- iconos del mapa estelar
NODE_START = [
    "................", "................", "......gggg......", ".....gGGGGg.....",
    "....gGccccGg....", "....gGcwwcGg....", "....gGccccGg....", ".....gGGGGg.....",
    "......gggg......", ".....kkkkkk.....", "....kGGGGGGk....", "....kGkkkkGk....",
    "................", "................", "................", "................",
]
NODE_PLANET = [
    "................", "................", "......kkkk......", "....kkbbbbkk....",
    "...kbbcbbbbbk...", "..kbcccbbBBBbk..", "..kbccbbbBBBbk..", ".yyyyyyyyyyyyyy.",
    "..kbbbbbBBBBbk..", "..kbbbbBBBBBbk..", "...kbbBBBBBbk...", "....kkBBBBkk....",
    "......kkkk......", "................", "................", "................",
]
NODE_CONTACT = [
    "................", "................", ".......oo.......", "......oooo......",
    ".....oo..oo.....", "....oo.yy.oo....", "...oo.y..y.oo...", "....oo.yy.oo....",
    ".....oo..oo.....", "......oooo......", ".......oo.......", "................",
    "......kkkk......", ".....kggggk.....", "................", "................",
]
NODE_ANOMALY = [
    "................", "................", "......pppp......", "....pppPPppp....",
    "...ppP....Ppp...", "..ppP..cc..Pp...", "..pP..cwwc..Pp..", "..pP..cwwc..Pp..",
    "..ppP..cc..Ppp..", "...pppP...Ppp...", "....ppppPppp....", "......pppp......",
    "................", "................", "................", "................",
]
NODE_UNKNOWN = [
    "................", "................", ".....GGGGGG.....", "....GwwwwwwG....",
    "...GwG....GwG...", "..........GwG...", ".........GwG....", "........GwG.....",
    ".......GwG......", ".......GwG......", "................", ".......GwG......",
    ".......GwG......", "................", "................", "................",
]
NODE_FINAL = [
    "................", ".......yy.......", "......yccy......", ".....yccccy.....",
    "....yycwwcyy....", ".....yccccy.....", "......yccy......", ".......yy.......",
    "......kppk......", "......kppk......", ".....kPppbk.....", "....kkkkkkkk....",
    "...kGGGGGGGGk...", "................", "................", "................",
]
SECTOR_SHIP = [
    "................", "................", "................", "........g.......",
    ".......ggg......", "......ggcgg.....", ".....gggggGG....", "....gggggggGG...",
    "...kkgggggGkk...", "...k.kkggkk.k...", "..oo..kkkk..oo..", "..oy...oo...yo..",
    "................", "................", "................", "................",
]

# -------------------------------------------------------- retratos (32x32) procedurales


def canvas(w=32, h=32):
    return [[CLEAR for _ in range(w)] for _ in range(h)]


def put_px(px, x, y, c):
    if 0 <= y < len(px) and 0 <= x < len(px[0]):
        px[y][x] = rgb(c) if len(c) == 3 else c


def in_poly(x, y, pts):
    inside = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def fill_poly(px, pts, color, noise=0.0, seed=0):
    for y in range(len(px)):
        for x in range(len(px[0])):
            if in_poly(x + 0.5, y + 0.5, pts):
                c = color(x, y) if callable(color) else color
                if noise:
                    c = shade(c, 1 + (rnd(x, y, seed) - 0.5) * noise)
                put_px(px, x, y, c)


def fill_ellipse(px, cx, cy, rx, ry, color, noise=0.0, seed=0):
    for y in range(len(px)):
        for x in range(len(px[0])):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                c = color(x, y) if callable(color) else color
                if noise:
                    c = shade(c, 1 + (rnd(x, y, seed) - 0.5) * noise)
                put_px(px, x, y, c)


def outline(px, color=(10, 12, 20)):
    h, w = len(px), len(px[0])
    edge = []
    for y in range(h):
        for x in range(w):
            if px[y][x][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and px[ny][nx][3] != 0:
                        edge.append((x, y))
                        break
    for x, y in edge:
        px[y][x] = rgb(color)


def paint_vael():
    px = canvas()
    # halo de luz
    for y in range(32):
        for x in range(32):
            d = ((x - 16) ** 2 + (y - 15) ** 2) ** 0.5
            if 13 < d < 15.5:
                put_px(px, x, y, (60, 130, 170, 90))
    diamond = [(16, 2), (26, 13), (16, 30), (6, 13)]
    fill_poly(px, diamond, lambda x, y: (140, 226, 255) if x >= 16 else (70, 160, 214), noise=0.12, seed=31)
    # facetas
    fill_poly(px, [(16, 2), (26, 13), (16, 13)], (200, 244, 255))
    fill_poly(px, [(16, 2), (6, 13), (16, 13)], (110, 196, 240))
    fill_poly(px, [(16, 13), (26, 13), (16, 30)], (90, 178, 232))
    fill_poly(px, [(16, 13), (6, 13), (16, 30)], (50, 120, 190))
    # ojos: dos rendijas luminosas
    for x in (11, 12, 13, 19, 20, 21):
        put_px(px, x, 12, (255, 255, 255))
        put_px(px, x, 13, (170, 240, 255))
    # núcleo
    fill_ellipse(px, 16, 21, 2.2, 3.2, (235, 250, 255))
    outline(px, (16, 40, 80))
    return px


def paint_hallen():
    px = canvas()
    coat = (212, 132, 56)
    fill_poly(px, [(3, 31), (6, 23), (26, 23), (29, 31)], coat, noise=0.14, seed=5)
    fill_poly(px, [(12, 23), (20, 23), (16, 29)], (250, 220, 150))
    for bx, by in ((9, 27), (23, 27), (16, 30)):
        fill_ellipse(px, bx, by, 1.3, 1.3, (255, 220, 90))
    skin = (150, 176, 92)
    fill_ellipse(px, 16, 14, 10, 9, skin, noise=0.12, seed=9)
    fill_ellipse(px, 12, 9, 5, 3, (176, 200, 116))
    # gafas grandes
    for cx in (11, 21):
        fill_ellipse(px, cx, 13, 4.4, 4.4, (40, 36, 30))
        fill_ellipse(px, cx, 13, 3.2, 3.2, (255, 214, 102))
        fill_ellipse(px, cx - 1, 12, 1.1, 1.1, (255, 250, 220))
    fill_poly(px, [(14, 13), (18, 13), (18, 14), (14, 14)], (40, 36, 30))
    # boca ancha con dientes
    for x in range(11, 22):
        put_px(px, x, 19, (60, 40, 30))
    for x in range(12, 21, 2):
        put_px(px, x, 20, (250, 250, 240))
    outline(px, (24, 20, 14))
    return px


def paint_draeth():
    px = canvas()
    steel = (96, 108, 132)
    # hombreras con pinchos
    fill_poly(px, [(1, 31), (4, 22), (11, 24), (11, 31)], (70, 74, 90), noise=0.12, seed=13)
    fill_poly(px, [(31, 31), (28, 22), (21, 24), (21, 31)], (70, 74, 90), noise=0.12, seed=14)
    for pts in ([(3, 22), (2, 17), (6, 22)], [(29, 22), (30, 17), (26, 22)]):
        fill_poly(px, pts, (214, 70, 60))
    fill_poly(px, [(11, 31), (11, 24), (21, 24), (21, 31)], (46, 50, 66))
    # cresta
    fill_poly(px, [(16, 0), (12, 8), (20, 8)], (214, 70, 60))
    # cabeza / casco
    head = [(9, 8), (23, 8), (26, 17), (21, 26), (11, 26), (6, 17)]
    fill_poly(px, head, lambda x, y: steel if x >= 16 else shade(steel, 0.8), noise=0.12, seed=17)
    fill_poly(px, [(9, 8), (23, 8), (22, 12), (10, 12)], (128, 142, 168))
    # visera roja
    fill_poly(px, [(9, 14), (23, 14), (22, 17), (10, 17)], (24, 10, 14))
    for x in range(11, 22):
        put_px(px, x, 15, (255, 70, 60))
        put_px(px, x, 16, (190, 30, 30))
    # mandíbulas
    fill_poly(px, [(11, 22), (14, 22), (14, 27), (12, 26)], (200, 200, 190))
    fill_poly(px, [(21, 22), (18, 22), (18, 27), (20, 26)], (200, 200, 190))
    for x in (15, 16, 17):
        put_px(px, x, 21, (30, 34, 46))
    outline(px, (12, 14, 22))
    return px


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
    for biome, pal in BIOMES.items():
        for name, maker in [("llanura", f_llanura), ("roca", f_roca), ("hielo", f_hielo),
                            ("crater", f_crater), ("grieta", f_grieta)]:
            write_png("tile_%s_%s" % (biome, name), make_hex(maker(pal)))
    write_png("tile_fog", make_hex(f_fog))
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
    for biome, extra in [("frost", {}),
                         ("dust", {"b": (214, 150, 70), "B": (140, 80, 40), "c": (255, 214, 140)}),
                         ("verdant", {"b": (70, 170, 90), "B": (30, 100, 60), "c": (170, 240, 150)})]:
        write_png("node_planet_" + biome, make_sprite(NODE_PLANET, extra))
    for name, rows in [("node_start", NODE_START), ("node_contact", NODE_CONTACT),
                       ("node_anomaly", NODE_ANOMALY), ("node_unknown", NODE_UNKNOWN), ("node_final", NODE_FINAL),
                       ("sector_ship", SECTOR_SHIP)]:
        write_png(name, make_sprite(rows))
    for name, painter in [("vael", paint_vael), ("hallen", paint_hallen), ("draeth", paint_draeth)]:
        write_png("portrait_" + name, painter())
    print("Arte generado en", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
