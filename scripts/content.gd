extends Node
## Carga los datos del juego (res://data/*.json) y los valida (autoload "Content").

const VALID_EFFECTS := ["oxygen", "morale", "data", "rep", "set_flags"]
const VALID_REQUIRES := ["trait", "flag", "any_flag", "not_flag", "hint"]
const VALID_TYPES := ["signal", "ruins", "wreck", "life", "beacon"]

var avatars: Array = []
var planets: Array = []
var events := {}  # id -> evento
var factions := {}


func _init() -> void:
	avatars = _read("res://data/avatars.json")
	planets = _read("res://data/planets.json")
	factions = _read("res://data/factions.json")
	for e in _read("res://data/events.json"):
		events[e["id"]] = e


func avatar_by_id(id: String) -> Dictionary:
	for a in avatars:
		if a["id"] == id:
			return a
	return {}


func _read(path: String) -> Variant:
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if parsed == null:
		push_error("JSON inválido o ausente: %s" % path)
	return parsed


## Lista de problemas de coherencia en los datos (vacía si todo está bien).
func validate() -> Array[String]:
	var errors: Array[String] = []
	var set_flags := {}
	for id in events:
		var e: Dictionary = events[id]
		if not (e.get("type", "") in VALID_TYPES):
			errors.append("%s: tipo inválido" % id)
		if e.get("choices", []).size() < 2:
			errors.append("%s: necesita al menos 2 opciones" % id)
		for i in e.get("choices", []).size():
			var c: Dictionary = e["choices"][i]
			var where := "%s[%d]" % [id, i]
			if not c.has("text"):
				errors.append("%s: sin texto" % where)
			if c.has("risk") == c.has("result"):
				errors.append("%s: debe tener exactamente uno de risk/result" % where)
			var branches: Array = []
			if c.has("risk"):
				var chance: float = c["risk"].get("chance", -1.0)
				if chance < 0.0 or chance > 1.0:
					errors.append("%s: chance fuera de rango" % where)
				branches = [c["risk"].get("success", {}), c["risk"].get("fail", {})]
			elif c.has("result"):
				branches = [c["result"]]
			for b in branches:
				if not b.has("text"):
					errors.append("%s: rama sin texto" % where)
				for k in b.get("effects", {}):
					if not (k in VALID_EFFECTS):
						errors.append("%s: efecto desconocido '%s'" % [where, k])
				for f in b.get("effects", {}).get("set_flags", []):
					set_flags[f] = true
				for fac in b.get("effects", {}).get("rep", {}):
					if not factions.has(fac):
						errors.append("%s: facción desconocida '%s'" % [where, fac])
			for k in c.get("requires", {}):
				if not (k in VALID_REQUIRES):
					errors.append("%s: requisito desconocido '%s'" % [where, k])
			if c.has("tag") and not _any_avatar_has_trait(c["tag"]):
				errors.append("%s: ningún avatar tiene el rasgo '%s'" % [where, c["tag"]])
	# Los flags exigidos deben poder activarse en algún sitio.
	for id in events:
		for c in events[id].get("choices", []):
			var req: Dictionary = c.get("requires", {})
			var needed: Array = req.get("any_flag", []).duplicate()
			if req.has("flag"):
				needed.append(req["flag"])
			for f in needed:
				if not set_flags.has(f):
					errors.append("%s: el flag '%s' nunca se activa" % [id, f])
	for p in planets:
		for id in p.get("event_pool", []) + [p.get("beacon_event", "")]:
			if not events.has(id):
				errors.append("planeta %s: evento inexistente '%s'" % [p.get("id", "?"), id])
		if p.get("event_pool", []).size() < int(p.get("poi_count", 6)):
			errors.append("planeta %s: el pool tiene menos eventos que poi_count" % p.get("id", "?"))
	return errors


func _any_avatar_has_trait(t: String) -> bool:
	for a in avatars:
		if t in a.get("traits", []):
			return true
	return false
