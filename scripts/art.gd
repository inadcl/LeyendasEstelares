class_name Art
extends RefCounted
## Acceso cacheado a las texturas de res://art (generadas por tools/gen_art.py).

static var _cache := {}


static func tex(tex_name: String) -> Texture2D:
	if not _cache.has(tex_name):
		_cache[tex_name] = load("res://art/%s.png" % tex_name)
	return _cache[tex_name]
