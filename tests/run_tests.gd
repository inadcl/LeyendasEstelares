extends Node
## Pruebas headless: godot --headless --path . res://tests/run_tests.tscn
## Sale con código 0 si todo pasa. Con "-- --balance" imprime además estadísticas de equilibrio.

var _failures := 0


func _ready() -> void:
	_test_hex()
	_test_content()
	_test_generation()
	_test_event_rules()
	_test_bot_playthroughs("vance")
	_test_bot_playthroughs("okafor")
	print("\n%s (%d fallos)" % ["TODO OK" if _failures == 0 else "FALLOS", _failures])
	get_tree().quit(0 if _failures == 0 else 1)


func _check(cond: bool, msg: String) -> void:
	if not cond:
		_failures += 1
		print("  FALLO: ", msg)


func _test_hex() -> void:
	print("hex")
	for y in 6:
		for x in 6:
			var c := Vector2i(x, y)
			for n in HexGrid.neighbors(c):
				_check(HexGrid.distance(c, n) == 1, "vecino a distancia 1 %s→%s" % [c, n])
				_check(HexGrid.neighbors(n).has(c), "vecindad simétrica %s↔%s" % [c, n])
	_check(HexGrid.distance(Vector2i(0, 0), Vector2i(3, 0)) == 3, "distancia en línea")


func _test_content() -> void:
	print("contenido")
	var errors := Content.validate()
	for e in errors:
		_check(false, e)
	_check(Content.avatars.size() >= 2, "al menos 2 avatares")
	_check(not Content.planets.is_empty(), "al menos 1 planeta")


func _test_generation() -> void:
	print("generación de mapas")
	var planet: Dictionary = Content.planets[0]
	var counts := {}
	for s in 300:
		var m := PlanetData.new()
		m.generate(planet, Content.events, s)
		var costs := m.path_costs(m.ship_cell)
		_check(m.pois.size() == int(planet["poi_count"]) + 1, "nº de POIs semilla %d" % s)
		for p in m.pois:
			_check(costs.has(p["cell"]), "POI alcanzable semilla %d" % s)
		_check(costs[m.beacon_cell] >= 8, "baliza no demasiado cerca semilla %d" % s)
		for t in m.terrain.values():
			counts[t] = int(counts.get(t, 0)) + 1
		var again := PlanetData.new()
		again.generate(planet, Content.events, s)
		_check(again.terrain == m.terrain and again.ship_cell == m.ship_cell, "determinista semilla %d" % s)
	print("  terrenos: ", counts)


func _test_event_rules() -> void:
	print("reglas de eventos")
	var gs = load("res://scripts/game_state.gd").new()
	gs.start_run(Content.avatar_by_id("vance"), Content.factions)
	var rng := RandomNumberGenerator.new()
	rng.seed = 1
	var sci := {"tag": "ciencia", "risk": {"chance": 0.5, "success": {"text": "ok", "effects": {"data": 2}}, "fail": {"text": "no", "effects": {"oxygen": -3}}}}
	_check(is_equal_approx(EventRunner.success_chance(sci, gs), 0.7), "bonus de rasgo +20%")
	gs.start_run(Content.avatar_by_id("okafor"), Content.factions)
	_check(is_equal_approx(EventRunner.success_chance(sci, gs), 0.5), "sin rasgo, sin bonus")
	var locked := {"requires": {"flag": "x", "hint": "falta x"}, "result": {"text": "", "effects": {}}}
	_check(EventRunner.lock_reason(locked, gs) == "falta x", "opción bloqueada por flag")
	gs.apply_effects({"set_flags": ["x"]})
	_check(EventRunner.lock_reason(locked, gs) == "", "opción desbloqueada tras flag")
	var before: int = gs.oxygen
	gs.apply_effects({"oxygen": -5, "morale": -1, "data": 3, "rep": {"vael": 2}})
	_check(gs.oxygen == before - 5 and gs.data == 3 and gs.rep["vael"] == 2, "efectos aplicados")
	gs.apply_effects({"oxygen": 999})
	_check(gs.oxygen == gs.max_oxygen, "oxígeno acotado al máximo")
	gs.apply_effects({"oxygen": -999})
	_check(gs.failure_reason() == "oxygen", "fallo por oxígeno")
	gs.free()


## Un bot recorre el juego completo con el mismo motor que la UI.
func _test_bot_playthroughs(avatar_id: String) -> void:
	print("bot (%s)" % avatar_id)
	var gs = load("res://scripts/game_state.gd").new()
	var planet: Dictionary = Content.planets[0]
	var results := {"success": 0, "fail": 0, "abort": 0}
	var runs := 400
	for s in runs:
		var rng := RandomNumberGenerator.new()
		rng.seed = s * 31 + 7
		gs.start_run(Content.avatar_by_id(avatar_id), Content.factions)
		gs.begin_planet()
		var ex := Expedition.new(gs, planet, Content.events, s)
		results[_bot_run(ex, gs, rng)] += 1
	print("  ", results)
	var win_rate := float(results["success"]) / runs
	_check(win_rate > 0.25 and win_rate < 0.95, "tasa de éxito razonable (%.2f)" % win_rate)
	gs.free()


func _bot_run(ex: Expedition, gs, rng: RandomNumberGenerator) -> String:
	var visits := rng.randi_range(1, 5)
	var targets: Array[Dictionary] = []
	for p in ex.map.pois:
		if not p["objective"]:
			targets.append(p)
	targets.sort_custom(func(a, b): return HexGrid.distance(a["cell"], ex.map.ship_cell) < HexGrid.distance(b["cell"], ex.map.ship_cell))
	var beacon: Dictionary = ex.map.poi_at(ex.map.beacon_cell)
	var plan: Array[Dictionary] = targets.slice(0, visits)
	plan.append(beacon)
	for target in plan:
		var costs := ex.map.path_costs(ex.player)
		var home_costs := ex.map.path_costs(ex.map.ship_cell)
		# Solo va si le queda aire para llegar y volver a la nave (con margen).
		var need: int = costs[target["cell"]] + home_costs[target["cell"]] + 2
		if not target["objective"] and need > gs.oxygen:
			continue
		var outcome := _walk_and_resolve(ex, gs, rng, target)
		if outcome != "":
			return outcome
	if not ex.objective_done:
		return "abort"
	var path := ex.map.find_path(ex.player, ex.map.ship_cell)
	for c in path:
		var res := ex.move(c)
		if res["home"]:
			return "success"
		if res["failure"] != "":
			return "fail"
		if not res["poi"].is_empty():
			var o := _resolve_random(ex, gs, rng, res["poi"])
			if o != "":
				return o
	return "fail"


func _walk_and_resolve(ex: Expedition, gs, rng: RandomNumberGenerator, target: Dictionary) -> String:
	for c in ex.map.find_path(ex.player, target["cell"]):
		var res := ex.move(c)
		if res["failure"] != "":
			return "fail"
		if not res["poi"].is_empty():
			var o := _resolve_random(ex, gs, rng, res["poi"])
			if o != "":
				return o
	return ""


func _resolve_random(ex: Expedition, gs, rng: RandomNumberGenerator, poi: Dictionary) -> String:
	var options: Array = []
	for c in ex.event_of(poi)["choices"]:
		if EventRunner.lock_reason(c, gs) == "":
			options.append(c)
	_check(not options.is_empty(), "siempre hay una opción disponible en %s" % poi["event_id"])
	ex.resolve_choice(poi, options[rng.randi() % options.size()], rng)
	return "fail" if gs.failure_reason() != "" else ""
