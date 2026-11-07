#!/usr/bin/env python3
"""Genera el kit de interfaz pixel art de res://ui/ (marcos 9-slice, botones, iconos, insignias, fondos, cursor).

Uso: python3 tools/gen_ui.py [directorio_salida]
Todo está dibujado por código con una paleta fija; se puede sustituir por arte propio con los mismos nombres.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixel import *  # noqa: E402,F401,F403

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ui")

# --------------------------------------------------------------------------- paleta
BK = hexc("060810")
NAVY0, NAVY1, NAVY2, NAVY3 = hexc("0b1020"), hexc("141b33"), hexc("1c2748"), hexc("26356a")
MID, LIGHT = hexc("2e3f73"), hexc("4f6bb5")
CYAN, CYAN_L, CYAN_D = hexc("5cc8e8"), hexc("a8ecff"), hexc("2a7ea0")
AMBER, AMBER_L, AMBER_D = hexc("e8b45c"), hexc("ffe0a0"), hexc("a8742c")
GREEN, GREEN_D = hexc("74d68b"), hexc("3a8c52")
RED, RED_D = hexc("e0605c"), hexc("98342f")
PURPLE, PURPLE_D = hexc("a07ae0"), hexc("5e3f98")
WHITE, GRAY, GRAY_D = hexc("f4f8ff"), hexc("8393b8"), hexc("4a5678")


def save(name, px):
    write_png(os.path.join(OUT, name + ".png"), px)


def shade(c, f):
    return (max(0, min(255, int(c[0] * f))), max(0, min(255, int(c[1] * f))), max(0, min(255, int(c[2] * f))), c[3])


# ------------------------------------------------------------- marcos 9-slice
def frame(w, h, ring, hi, lo, fill, cut=3, rivet=None):
    """Marco con esquinas achaflanadas: contorno oscuro, anillo, bisel claro/oscuro y relleno."""
    opaque = [[True] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if x + y < cut or (w - 1 - x) + y < cut or x + (h - 1 - y) < cut or (w - 1 - x) + (h - 1 - y) < cut:
                opaque[y][x] = False

    def solid(x, y):
        return 0 <= x < w and 0 <= y < h and opaque[y][x]

    def near(x, y, pred):
        return any(pred(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))

    edge = {(x, y) for y in range(h) for x in range(w) if opaque[y][x] and near(x, y, lambda a, b: not solid(a, b))}
    ring1 = {(x, y) for y in range(h) for x in range(w) if opaque[y][x] and (x, y) not in edge and near(x, y, lambda a, b: (a, b) in edge)}
    px = canvas(w, h)
    for y in range(h):
        for x in range(w):
            if not opaque[y][x]:
                continue
            if (x, y) in edge:
                c = BK
            elif (x, y) in ring1:
                c = ring
            elif near(x, y, lambda a, b: (a, b) in ring1):
                top_left = ((x - 1, y) in ring1) or ((x, y - 1) in ring1)
                bottom_right = ((x + 1, y) in ring1) or ((x, y + 1) in ring1)
                c = hi if top_left and not bottom_right else (lo if bottom_right else fill(x, y))
            else:
                c = fill(x, y)
            px[y][x] = c
    if rivet:
        m = max(4, cut + 1)
        for rx, ry in ((m, m), (w - 1 - m, m), (m, h - 1 - m), (w - 1 - m, h - 1 - m)):
            if solid(rx, ry) and (rx, ry) not in edge:
                px[ry][rx] = rivet
    return px


def dither_fill(a, b):
    return lambda x, y: a if (x + y) % 2 == 0 else b


def banded_fill(top, bottom, h):
    def f(x, y):
        mid = h // 2
        if y < mid - 1:
            return top
        if y > mid:
            return bottom
        return top if (x + y) % 2 == 0 else bottom
    return f


def make_panels():
    save("panel", frame(24, 24, MID, LIGHT, hexc("0a0f20"), dither_fill(NAVY1, hexc("161e3a")), rivet=hexc("6f8bd5")))
    save("panel_dark", frame(24, 24, hexc("1c2748"), hexc("070b16"), hexc("1a2440"), lambda x, y: NAVY0))
    save("panel_accent", frame(24, 24, CYAN_D, CYAN_L, hexc("0a1830"), dither_fill(NAVY1, hexc("161e3a")), rivet=CYAN))
    save("panel_amber", frame(24, 24, AMBER_D, AMBER_L, hexc("1c1408"), dither_fill(hexc("1a1626"), hexc("1e1a2c")), rivet=AMBER))
    for name, ring, hi, lo, top, bot in [
        ("btn_normal", hexc("3a4d8a"), hexc("5671c0"), hexc("141c3a"), NAVY3, hexc("1b2750")),
        ("btn_hover", CYAN, CYAN_L, hexc("163048"), hexc("31438a"), hexc("243468")),
        ("btn_pressed", hexc("3a4d8a"), hexc("0e1430"), hexc("4a63ad"), hexc("18224a"), hexc("131b3c")),
        ("btn_disabled", hexc("1e2740"), hexc("1e2740"), hexc("0e1322"), hexc("121828"), hexc("121828")),
    ]:
        save(name, frame(24, 24, ring, hi, lo, banded_fill(top, bot, 24), cut=3))
    # Anillo de foco (centro transparente)
    f = frame(24, 24, CYAN, CYAN_L, CYAN, lambda x, y: CLEAR, cut=3)
    ringed = canvas(24, 24)
    for y in range(24):
        for x in range(24):
            if f[y][x][3] and f[y][x] != CLEAR and (f[y][x] in (CYAN, CYAN_L) or f[y][x] == BK):
                ringed[y][x] = CYAN if f[y][x] != BK else CLEAR
    save("btn_focus", ringed)
    # Separador punteado
    sep = canvas(8, 2)
    for x in range(8):
        if x % 4 < 2:
            sep[0][x] = MID
            sep[1][x] = hexc("0a0f20")
    save("separator", sep)


# ------------------------------------------------------------- bisel de monitor
def make_bezel():
    w = h = 32
    px = frame(w, h, hexc("5a6688"), hexc("a4b0d0"), hexc("2a3350"), lambda x, y: hexc("3a4468") if (x + y) % 2 == 0 else hexc("424d74"), cut=4, rivet=hexc("c8d2ee"))
    # Recorte interior (pantalla)
    m = 8
    for y in range(m, h - m):
        for x in range(m, w - m):
            px[y][x] = hexc("04060c")
    for x in range(m - 1, w - m + 1):
        px[m - 1][x] = hexc("141a30")
        px[h - m][x] = hexc("6b789c")
    for y in range(m - 1, h - m + 1):
        px[y][m - 1] = hexc("141a30")
        px[y][w - m] = hexc("6b789c")
    save("bezel", px)


# ---------------------------------------------------------------------- iconos
def icon_canvas():
    return canvas(12, 12)


def icon_fuel():
    px = icon_canvas()
    fill_poly(px, [(6, 0.5), (10.5, 6), (10.5, 8), (8.5, 11.5), (3.5, 11.5), (1.5, 8), (1.5, 6)], lambda x, y: AMBER if x >= 5 else AMBER_D)
    fill_poly(px, [(5, 6), (7, 6), (7, 9), (5, 9)], AMBER_L)
    outline(px, BK)
    return px


def icon_scan():
    px = icon_canvas()
    fill_ellipse(px, 5, 5, 4.2, 4.2, CYAN_D)
    fill_ellipse(px, 5, 5, 3.0, 3.0, hexc("0b2a40"))
    put(px, 3, 3, CYAN_L)
    put(px, 4, 3, CYAN_L)
    put(px, 3, 4, CYAN_L)
    fill_poly(px, [(8, 7.5), (9, 6.5), (11.5, 9), (10.5, 10)], GRAY)
    outline(px, BK)
    return px


def icon_data():
    px = icon_canvas()
    fill_poly(px, [(6, 0.5), (10.5, 5), (6, 11.5), (1.5, 5)], lambda x, y: CYAN if x >= 6 else CYAN_D)
    fill_poly(px, [(6, 1.5), (9, 5), (6, 5)], CYAN_L)
    outline(px, BK)
    return px


HEART = [
    ".kk...kk.",
    "krrk.krrk",
    "krwrkrrrk",
    "krrrrrrrk",
    ".krrrrrk.",
    "..krrrk..",
    "...krk...",
    "....k....",
]


def icon_morale():
    px = sprite(HEART, {"k": BK, "r": RED, "w": hexc("ffb0a8")}, 12)
    return px


def icon_oxygen():
    px = icon_canvas()
    fill_ellipse(px, 6, 6, 5, 5, hexc("2a7ea0"))
    fill_ellipse(px, 6, 6, 3.8, 3.8, CYAN)
    fill_ellipse(px, 4.5, 4.5, 1.4, 1.4, WHITE)
    outline(px, BK)
    return px


def icon_open():  # sol: franqueza
    px = icon_canvas()
    fill_ellipse(px, 6, 6, 3.2, 3.2, AMBER_L)
    for x, y in [(6, 0), (6, 11), (0, 6), (11, 6), (2, 2), (9, 2), (2, 9), (9, 9)]:
        put(px, x, y, AMBER)
    outline(px, hexc("2a1c08"))
    return px


def icon_careful():  # escudo: cautela
    px = icon_canvas()
    fill_poly(px, [(1.5, 1), (10.5, 1), (10.5, 6), (6, 11.5), (1.5, 6)], lambda x, y: CYAN if x >= 6 else CYAN_D)
    fill_poly(px, [(3, 2.5), (6, 2.5), (6, 8)], CYAN_L)
    outline(px, BK)
    return px


def icon_firm():  # puño/bloque: firmeza
    px = icon_canvas()
    fill_rect(px, 2, 3, 10, 10, lambda x, y: RED if y < 7 else RED_D)
    fill_rect(px, 3, 4, 9, 5, hexc("ffb0a8"))
    for x in (4, 6, 8):
        put(px, x, 8, hexc("5a1a18"))
    fill_rect(px, 4, 1, 8, 3, RED_D)
    outline(px, BK)
    return px


def icon_deceive():  # ojo/máscara: engaño
    px = icon_canvas()
    fill_poly(px, [(0.5, 6), (3, 3), (9, 3), (11.5, 6), (9, 9), (3, 9)], lambda x, y: PURPLE if y < 6 else PURPLE_D)
    fill_ellipse(px, 6, 6, 2.0, 2.0, WHITE)
    fill_ellipse(px, 6, 6, 1.0, 1.0, BK)
    outline(px, BK)
    return px


def make_icons():
    for name, fn in [("fuel", icon_fuel), ("scan", icon_scan), ("data", icon_data), ("morale", icon_morale),
                     ("oxygen", icon_oxygen), ("stance_open", icon_open), ("stance_careful", icon_careful),
                     ("stance_firm", icon_firm), ("stance_deceive", icon_deceive)]:
        save("icon_" + name, fn())


# ------------------------------------------------------- insignias de nodo (36x36)
def make_badges():
    size = 36
    c = (size - 1) / 2
    specs = {
        "idle": (MID, hexc("141b33"), None),
        "reach": (AMBER, hexc("1a1626"), AMBER_D),
        "current": (CYAN, hexc("0e2236"), CYAN_D),
        "done": (hexc("232c4a"), hexc("0c1120"), None),
        "selected": (WHITE, hexc("1c2748"), GRAY),
    }
    for name, (ring, fill, inner) in specs.items():
        px = canvas(size, size)
        for y in range(size):
            for x in range(size):
                r = math.hypot(x - c, y - c)
                if r > 17.6:
                    continue
                if r > 16.2:
                    col = BK
                elif r > 14.0:
                    col = ring
                elif inner is not None and r > 13.0:
                    col = inner
                else:
                    col = fill if (x + y) % 2 == 0 else shade(fill, 1.12)
                px[y][x] = col
        save("badge_" + name, px)


# ------------------------------------------------------------------- cursor
CURSOR = [
    "k.........",
    "kk........",
    "kwk.......",
    "kwwk......",
    "kwwwk.....",
    "kwwwwk....",
    "kwwwwwk...",
    "kwwwwwwk..",
    "kwwwwwwwk.",
    "kwwwwwkkkk",
    "kwwkwwk...",
    "kwk.kwwk..",
    "kk..kwwk..",
    "k....kwwk.",
    ".....kwwk.",
    "......kk..",
]


def make_cursor():
    pal = {"k": hexc("0b1020"), "w": hexc("f4f8ff")}
    px = sprite(CURSOR, pal)
    # sombra de cian sutil en el borde derecho/inferior para que destaque sobre fondos oscuros
    save("cursor", scale(px, 2))


# ----------------------------------------------------------------- fondos
def sky_color(t):
    stops = [(0.0, (8, 8, 28)), (0.45, (22, 18, 58)), (0.7, (58, 34, 96)), (0.88, (110, 62, 120)), (1.0, (170, 98, 120))]
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t0 <= t <= t1:
            k = (t - t0) / (t1 - t0)
            return tuple(c0[i] + (c1[i] - c0[i]) * k for i in range(3))
    return stops[-1][1]


def dither_to_ramp(v, ramp, x, y):
    """Cuantiza v en [0,1] a una rampa con tramado ordenado."""
    pos = v * (len(ramp) - 1)
    lo = int(pos)
    frac = pos - lo
    return ramp[min(len(ramp) - 1, lo + (1 if frac > bayer(x, y) else 0))]


def make_title_bg(W=640, H=360, name="bg_title", planet=(470, 128, 66), ring=(118, 26), moon=(150, 92, 15), mount=(268, 300)):
    px = canvas(W, H, (0, 0, 0, 255))
    ramp_sky = [tuple(int(v) for v in sky_color(i / 11)) + (255,) for i in range(12)]
    for y in range(H):
        for x in range(W):
            t = min(1.0, y / (H * 0.78))
            px[y][x] = dither_to_ramp(t, ramp_sky, x, y)
    # estrellas
    for y in range(int(H * 0.72)):
        for x in range(W):
            r = rnd(x, y, 5)
            fade = 1.0 - y / (H * 0.72)
            if r > 0.9975 - 0.0015 * fade:
                px[y][x] = (240, 245, 255, 255) if r > 0.9992 else (150, 160, 210, 255)
    for sx, sy in ((90, 40), (300, 70), (560, 30), (40, 120), (410, 24), (200, 150)):
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            put(px, sx + dx, sy + dy, (255, 255, 255, 255) if (dx, dy) == (0, 0) else (150, 170, 230, 255))
    # planeta anillado
    cx, cy, R = planet
    ring_cx, ring_cy, rx, ry = cx, cy + 6, ring[0], ring[1]

    def ring_pix(x, y):
        e = ((x + 0.5 - ring_cx) / rx) ** 2 + ((y + 0.5 - ring_cy) / ry) ** 2
        return 0.64 <= e <= 1.0, e

    def ring_color(x, y, e):
        v = 0.35 + 0.5 * vnoise(int(e * 40), 0, 3, 11)
        base = [(88, 70, 60), (140, 112, 84), (196, 164, 118), (230, 204, 160)]
        return dither_to_ramp(min(1.0, v), [c + (255,) for c in base], x, y)

    for y in range(H):  # anillo trasero
        for x in range(W):
            ok, e = ring_pix(x, y)
            if ok and y < ring_cy:
                px[y][x] = ring_color(x, y, e)
    light = (-0.55, -0.6, 0.58)
    ln = math.sqrt(sum(v * v for v in light))
    light = tuple(v / ln for v in light)
    planet_ramp = [(20, 16, 50, 255), (38, 30, 88, 255), (66, 50, 130, 255), (104, 80, 170, 255), (150, 118, 206, 255), (200, 172, 238, 255)]
    for y in range(cy - R, cy + R + 1):
        for x in range(cx - R, cx + R + 1):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            d2 = (dx * dx + dy * dy) / (R * R)
            if d2 <= 1:
                nz = math.sqrt(1 - d2)
                lam = max(0.0, (dx / R) * light[0] + (dy / R) * light[1] + nz * light[2])
                band = 0.08 * math.sin(dy * 0.33 + 3 * vnoise(x, y, 14, 2)) + 0.05 * (vnoise(x, y, 5, 7) - 0.5)
                v = max(0.0, min(1.0, lam * 0.95 + band))
                if d2 > 0.93:
                    v *= 0.85
                px[y][x] = dither_to_ramp(v, planet_ramp, x, y)
    for y in range(H):  # anillo delantero
        for x in range(W):
            ok, e = ring_pix(x, y)
            if ok and y >= ring_cy:
                px[y][x] = ring_color(x, y, e)
    # luna
    mx, my, mr = moon
    moon_ramp = [(60, 54, 80, 255), (104, 98, 124, 255), (150, 144, 164, 255), (204, 198, 214, 255)]
    for y in range(my - mr, my + mr + 1):
        for x in range(mx - mr, mx + mr + 1):
            dx, dy = x + 0.5 - mx, y + 0.5 - my
            if dx * dx + dy * dy <= mr * mr:
                nz = math.sqrt(max(0.0, 1 - (dx * dx + dy * dy) / (mr * mr)))
                lam = max(0.0, (dx / mr) * -0.5 + (dy / mr) * -0.6 + nz * 0.62)
                for ccx, ccy, cr in ((mx - 5, my + 3, 3), (mx + 5, my - 4, 2.2), (mx + 3, my + 7, 2)):
                    if (x + 0.5 - ccx) ** 2 + (y + 0.5 - ccy) ** 2 <= cr * cr:
                        lam *= 0.55
                px[y][x] = dither_to_ramp(min(1.0, lam), moon_ramp, x, y)
    # montañas (dos capas)
    def mountains(base, amp, seed, color, detail):
        for x in range(W):
            hgt = base + amp * math.sin(x / 41.0 + seed) + (amp * 0.55) * math.sin(x / 17.0 + seed * 2) + detail * (vnoise(x, 0, 5, seed) - 0.5)
            for y in range(int(hgt), H):
                px[y][x] = color
    mountains(mount[0], 20, 1.3, (30, 24, 68, 255), 12)
    mountains(mount[1], 15, 4.1, (14, 12, 36, 255), 10)
    # haces de luz del horizonte sobre la capa lejana: tramado cálido
    for y in range(mount[0] - 13, mount[0] + 12):
        for x in range(W):
            if px[y][x] == (30, 24, 68, 255) and rnd(x, y, 3) > 0.7 and y < mount[0] + 8:
                px[y][x] = (44, 32, 84, 255)
    save(name, px)


def make_space_bg(W=640, H=360, name="bg_space"):
    px = canvas(W, H, (0, 0, 0, 255))
    neb = [(8, 9, 24), (12, 14, 36), (22, 18, 56), (40, 26, 84), (62, 40, 112)]
    neb2 = [(8, 9, 24), (10, 22, 40), (14, 40, 64), (22, 64, 92)]
    for y in range(H):
        for x in range(W):
            n = 0.55 * vnoise(x, y, 90, 1) + 0.3 * vnoise(x, y, 38, 2) + 0.15 * vnoise(x, y, 14, 3)
            v = max(0.0, (n - 0.42) * 2.3)
            n2 = 0.6 * vnoise(x + 300, y, 110, 4) + 0.4 * vnoise(x, y, 30, 5)
            w2 = max(0.0, (n2 - 0.5) * 1.8)
            c = dither_to_ramp(min(1.0, v), [c + (255,) for c in neb], x, y)
            if w2 > 0.05 and v < 0.25:
                c = dither_to_ramp(min(1.0, w2), [c + (255,) for c in neb2], x, y)
            px[y][x] = c
    for y in range(H):
        for x in range(W):
            r = rnd(x, y, 9)
            if r > 0.9985:
                px[y][x] = (240, 245, 255, 255)
            elif r > 0.996:
                px[y][x] = (150, 160, 210, 255)
            elif r > 0.9915:
                px[y][x] = (70, 80, 120, 255)
    save(name, px)


def make_title_ship():
    w, h = 56, 24
    px = canvas(w, h)
    fill_poly(px, [(4, 12), (14, 7), (40, 7), (52, 12), (40, 17), (14, 17)], lambda x, y: hexc("9aa8c8") if y < 12 else hexc("5a6688"))
    fill_poly(px, [(14, 7), (22, 2), (30, 2), (34, 7)], hexc("7a88aa"))
    fill_poly(px, [(14, 17), (22, 22), (30, 22), (34, 17)], hexc("3e4868"))
    fill_poly(px, [(40, 9), (50, 12), (40, 13)], CYAN)
    fill_poly(px, [(44, 10), (49, 12), (44, 12)], CYAN_L)
    fill_rect(px, 18, 11, 36, 13, hexc("2e3a5e"))
    for x in range(20, 34, 3):
        put(px, x, 12, AMBER_L)
    outline(px, BK)
    # motor
    for i in range(6):
        put(px, 3 - i // 2, 11 + (i % 2), AMBER if i < 4 else AMBER_D)
    save("title_ship", px)


def main():
    make_panels()
    make_bezel()
    make_icons()
    make_badges()
    make_cursor()
    make_title_bg()
    make_space_bg()
    # Variantes verticales (360x800; el juego recorta el centro si la pantalla es más baja)
    make_title_bg(360, 800, "bg_title_portrait", planet=(210, 250, 80), ring=(150, 30), moon=(70, 120, 16), mount=(640, 690))
    make_space_bg(360, 800, "bg_space_portrait")
    make_title_ship()
    print("Kit de interfaz generado en", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
