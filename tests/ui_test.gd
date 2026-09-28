extends Node
## Prueba de interfaz con eventos de entrada reales: clic y teclado deben mover al jugador.
## godot --headless --path . res://tests/ui_test.tscn

var _failures := 0


func _ready() -> void:
	var main: Control = load("res://scenes/main.tscn").instantiate()
	add_child(main)
	await get_tree().process_frame
	main._show_avatars()
	await get_tree().process_frame
	GameState.start_run(Content.avatar_by_id("vance"), Content.factions)
	main._start_planet()
	await get_tree().process_frame
	var screen: MapScreen = main._current
	var ex := screen.expedition
	var view: PlanetMapView = screen._view
	_check(not view.enabled, "el mapa está bloqueado durante el briefing")
	screen._close_overlay()
	await get_tree().process_frame
	_check(view.enabled, "el mapa se activa al descender")

	# Clic real sobre un hexágono adyacente transitable.
	var target := _adjacent(ex)
	var start := ex.player
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	click.pressed = true
	click.position = view.global_position + HexGrid.center(target)
	click.global_position = click.position
	get_viewport().push_input(click)
	await get_tree().process_frame
	_check(ex.player == target, "un clic sobre un hexágono adyacente mueve al jugador (%s → %s)" % [start, ex.player])

	# Teclado: cada tecla corresponde a un vecino; alguna debe poder moverse.
	var before := ex.player
	for key in [KEY_D, KEY_E, KEY_C, KEY_A, KEY_Q, KEY_Z]:
		if ex.player != before or not screen._view.enabled:
			break
		var ev := InputEventKey.new()
		ev.keycode = key
		ev.pressed = true
		get_viewport().push_input(ev)
		await get_tree().process_frame
	_check(ex.player != before or not screen._view.enabled, "el teclado mueve al jugador (o abre un evento)")

	print("\n%s (%d fallos)" % ["UI OK" if _failures == 0 else "FALLOS", _failures])
	get_tree().quit(0 if _failures == 0 else 1)


func _adjacent(ex: Expedition) -> Vector2i:
	for n in HexGrid.neighbors(ex.player):
		if ex.can_move(n) and ex.map.poi_at(n).is_empty():
			return n
	return ex.player


func _check(cond: bool, msg: String) -> void:
	print(("  ok: " if cond else "  FALLO: ") + msg)
	if not cond:
		_failures += 1
