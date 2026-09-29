class_name Campaign
extends RefCounted
## Una campaña: el mapa estelar, la posición de la nave y las reglas de salto y escaneo.

const SCAN_RANGE := 2  # columnas por delante de la actual que se pueden escanear

var state
var sector := SectorData.new()
var current := ""
var jumps := 0


func _init(state_, cfg: Dictionary, seed_value: int) -> void:
	state = state_
	sector.generate(cfg, seed_value)
	current = sector.start_id


func node(id: String) -> Dictionary:
	return sector.nodes[id]


func is_final(id: String) -> bool:
	return sector.nodes[id]["final"]


func edge_cost(from: String, to: String) -> int:
	return int(sector.nodes[from]["costs"].get(to, 1))


func can_jump(id: String) -> bool:
	return sector.nodes[current]["edges"].has(id) and not sector.nodes[id]["done"] and state.fuel >= edge_cost(current, id)


func jump(id: String) -> void:
	state.spend_fuel(edge_cost(current, id))
	current = id
	jumps += 1


func can_scan(id: String) -> bool:
	var n: Dictionary = sector.nodes[id]
	var ahead: int = n["col"] - sector.nodes[current]["col"]
	return state.scans > 0 and not n["scanned"] and not n["done"] and ahead >= 1 and ahead <= SCAN_RANGE


func scan(id: String) -> void:
	state.spend_scan()
	sector.nodes[id]["scanned"] = true


func finish_node(id: String) -> void:
	sector.nodes[id]["done"] = true


## "fuel" si la nave no puede continuar; "morale" si la tripulación se niega; "" si sigue viva.
func end_reason() -> String:
	if state.morale <= 0:
		return "morale"
	if not is_final(current):
		for to in sector.nodes[current]["edges"]:
			if can_jump(to):
				return ""
		return "fuel"
	return ""
