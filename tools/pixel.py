"""Utilidades mínimas de pixel art (solo stdlib): PNG, ruido determinista, formas y contornos."""
import os
import struct
import zlib

CLEAR = (0, 0, 0, 0)


def write_png(path, px):
    h, w = len(px), len(px[0])
    raw = b"".join(b"\x00" + bytes(c for p in row for c in p) for row in px)

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def hexc(s, a=255):
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)


def rnd(x, y, seed=0):
    n = (x * 374761393 + y * 668265263 + seed * 2147483647) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65536.0


def vnoise(x, y, scale, seed=0):
    """Ruido de valor suave en [0,1)."""
    fx, fy = x / scale, y / scale
    x0, y0 = int(fx // 1), int(fy // 1)
    tx, ty = fx - x0, fy - y0
    tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
    seed = int(seed * 1000)
    a = rnd(x0, y0, seed)
    b = rnd(x0 + 1, y0, seed)
    c = rnd(x0, y0 + 1, seed)
    d = rnd(x0 + 1, y0 + 1, seed)
    return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty


BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def bayer(x, y):
    return (BAYER[y % 4][x % 4] + 0.5) / 16.0


def canvas(w, h, color=CLEAR):
    return [[color for _ in range(w)] for _ in range(h)]


def put(px, x, y, c):
    if 0 <= y < len(px) and 0 <= x < len(px[0]):
        px[y][x] = c if len(c) == 4 else (c[0], c[1], c[2], 255)


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


def fill_poly(px, pts, color):
    for y in range(len(px)):
        for x in range(len(px[0])):
            if in_poly(x + 0.5, y + 0.5, pts):
                put(px, x, y, color(x, y) if callable(color) else color)


def fill_ellipse(px, cx, cy, rx, ry, color):
    for y in range(len(px)):
        for x in range(len(px[0])):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                put(px, x, y, color(x, y) if callable(color) else color)


def fill_rect(px, x0, y0, x1, y1, color):
    for y in range(y0, y1):
        for x in range(x0, x1):
            put(px, x, y, color(x, y) if callable(color) else color)


def outline(px, color):
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
        px[y][x] = color if len(color) == 4 else (color[0], color[1], color[2], 255)


def sprite(rows, pal, size=None):
    """Convierte filas ASCII en píxeles; si `size` se da, centra el dibujo en un lienzo size x size."""
    w = max(len(r) for r in rows)
    h = len(rows)
    sw, sh = (size, size) if size else (w, h)
    px = canvas(sw, sh)
    ox, oy = (sw - w) // 2, (sh - h) // 2
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != "." and ch != " ":
                put(px, ox + x, oy + y, pal[ch])
    return px


def scale(px, k):
    return [[p for p in row for _ in range(k)] for row in px for _ in range(k)]
