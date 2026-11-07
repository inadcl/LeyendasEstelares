class_name HexGrid
extends RefCounted
## Geometría hexagonal (pointy-top, coordenadas "odd-r": las filas impares se desplazan media casilla).

const W := 32
const H := 36
const ROW_H := 27

const _DIRS_EVEN: Array[Vector2i] = [
	Vector2i(1, 0), Vector2i(0, -1), Vector2i(-1, -1),
	Vector2i(-1, 0), Vector2i(-1, 1), Vector2i(0, 1),
]
const _DIRS_ODD: Array[Vector2i] = [
	Vector2i(1, 0), Vector2i(1, -1), Vector2i(0, -1),
	Vector2i(-1, 0), Vector2i(0, 1), Vector2i(1, 1),
]


static func center(c: Vector2i) -> Vector2:
	return Vector2(c.x * W + (c.y & 1) * W * 0.5 + W * 0.5, c.y * ROW_H + H * 0.5)


static func neighbors(c: Vector2i) -> Array[Vector2i]:
	var out: Array[Vector2i] = []
	var dirs: Array[Vector2i] = _DIRS_ODD if (c.y & 1) == 1 else _DIRS_EVEN
	for d in dirs:
		out.append(c + d)
	return out


static func to_cube(c: Vector2i) -> Vector3i:
	var q: int = c.x - (c.y - (c.y & 1)) / 2
	return Vector3i(q, c.y, -q - c.y)


static func distance(a: Vector2i, b: Vector2i) -> int:
	var ca := to_cube(a)
	var cb := to_cube(b)
	return maxi(maxi(absi(ca.x - cb.x), absi(ca.y - cb.y)), absi(ca.z - cb.z))
