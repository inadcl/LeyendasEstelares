extends Node
## Estado de la expedición en curso. Persiste entre planetas (autoload "GameState").

signal changed

var avatar: Dictionary = {}
var oxygen := 0
var max_oxygen := 0
var morale := 0
var max_morale := 0
var data := 0
var rep := {}  # facción -> int
var flags := {}  # String -> true
var planet_index := 0
var faction_names := {}


func start_run(avatar_dict: Dictionary, factions: Dictionary = {}) -> void:
	avatar = avatar_dict
	max_oxygen = int(avatar.get("max_oxygen", 40))
	max_morale = int(avatar.get("max_morale", 10))
	oxygen = max_oxygen
	morale = max_morale
	data = 0
	rep = {}
	flags = {}
	planet_index = 0
	faction_names = {}
	for id in factions:
		faction_names[id] = factions[id].get("name", id)
	changed.emit()


## Reabastece oxígeno al iniciar un nuevo planeta; moral, datos y reputación se conservan.
func begin_planet() -> void:
	oxygen = max_oxygen
	changed.emit()


func has_trait(t: String) -> bool:
	return t in avatar.get("traits", [])


func has_flag(f: String) -> bool:
	return flags.has(f)


func spend_oxygen(n: int) -> void:
	oxygen = maxi(oxygen - n, 0)
	changed.emit()


## "oxygen", "morale" o "" si la expedición sigue viva.
func failure_reason() -> String:
	if oxygen <= 0:
		return "oxygen"
	if morale <= 0:
		return "morale"
	return ""


## Aplica efectos y devuelve líneas legibles de lo que cambió realmente.
func apply_effects(effects: Dictionary) -> Array[String]:
	var lines: Array[String] = []
	if effects.has("oxygen"):
		var before := oxygen
		oxygen = clampi(oxygen + int(effects["oxygen"]), 0, max_oxygen)
		if oxygen != before:
			lines.append("Oxígeno %s" % _signed(oxygen - before))
	if effects.has("morale"):
		var before := morale
		morale = clampi(morale + int(effects["morale"]), 0, max_morale)
		if morale != before:
			lines.append("Moral %s" % _signed(morale - before))
	if effects.has("data"):
		var before := data
		data = maxi(data + int(effects["data"]), 0)
		if data != before:
			lines.append("Datos %s" % _signed(data - before))
	for faction in effects.get("rep", {}):
		var delta := int(effects["rep"][faction])
		rep[faction] = int(rep.get(faction, 0)) + delta
		lines.append("Reputación %s %s" % [faction_names.get(faction, faction), _signed(delta)])
	for f in effects.get("set_flags", []):
		flags[f] = true
	changed.emit()
	return lines


func _signed(n: int) -> String:
	return ("+%d" % n) if n > 0 else ("−%d" % absi(n))
