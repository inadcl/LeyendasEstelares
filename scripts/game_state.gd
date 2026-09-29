extends Node
## Estado de la expedición en curso. Persiste entre planetas (autoload "GameState").

signal changed

var avatar: Dictionary = {}
var oxygen := 0
var max_oxygen := 0
var morale := 0
var max_morale := 0
var data := 0
var fuel := 0
var max_fuel := 0
var scans := 0
var max_scans := 0
var rep := {}  # facción -> int
var flags := {}  # String -> true
var faction_ids: Array = []


func start_run(avatar_dict: Dictionary, factions: Dictionary = {}, campaign_cfg: Dictionary = {}) -> void:
	avatar = avatar_dict
	max_oxygen = int(avatar.get("max_oxygen", 40))
	max_morale = int(avatar.get("max_morale", 10))
	max_fuel = int(campaign_cfg.get("max_fuel", 10))
	max_scans = int(campaign_cfg.get("max_scans", 6))
	oxygen = max_oxygen
	morale = max_morale
	fuel = int(campaign_cfg.get("start_fuel", 8))
	scans = int(campaign_cfg.get("start_scans", 4))
	data = 0
	rep = {}
	flags = {}
	faction_ids = factions.keys()
	changed.emit()


## Reabastece oxígeno al descender; moral, datos, combustible y reputación se conservan.
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


func spend_fuel(n: int) -> void:
	fuel = maxi(fuel - n, 0)
	changed.emit()


func spend_scan() -> void:
	scans = maxi(scans - 1, 0)
	changed.emit()


## "oxygen", "morale" o "" si la expedición sigue viva (oxígeno solo cuenta en superficie).
func failure_reason() -> String:
	if oxygen <= 0:
		return "oxygen"
	if morale <= 0:
		return "morale"
	return ""


## Aplica efectos y devuelve líneas legibles (ya traducidas) de lo que cambió realmente.
func apply_effects(effects: Dictionary) -> Array[String]:
	var lines: Array[String] = []
	_apply_stat(effects, "oxygen", "max_oxygen", lines)
	_apply_stat(effects, "morale", "max_morale", lines)
	_apply_stat(effects, "fuel", "max_fuel", lines)
	_apply_stat(effects, "scans", "max_scans", lines)
	if effects.has("data"):
		var before := data
		data = maxi(data + int(effects["data"]), 0)
		if data != before:
			lines.append(T.t("fx.data", {"delta": _signed(data - before)}))
	for faction in effects.get("rep", {}):
		var delta := int(effects["rep"][faction])
		rep[faction] = int(rep.get(faction, 0)) + delta
		lines.append(T.t("fx.rep", {"faction": T.t("faction." + faction), "delta": _signed(delta)}))
	for f in effects.get("set_flags", []):
		flags[f] = true
	changed.emit()
	return lines


func _apply_stat(effects: Dictionary, stat: String, max_stat: String, lines: Array[String]) -> void:
	if not effects.has(stat):
		return
	var before: int = get(stat)
	var after := clampi(before + int(effects[stat]), 0, int(get(max_stat)))
	set(stat, after)
	if after != before:
		lines.append(T.t("fx." + stat, {"delta": _signed(after - before)}))


func _signed(n: int) -> String:
	return ("+%d" % n) if n > 0 else ("−%d" % absi(n))
