extends Node
## Prueba de interfaz con entradas reales: recorre título → avatar → mapa estelar → planeta / contacto / anomalía.
## godot --headless --path . res://tests/ui_test.tscn

var _failures := 0
var _main: Control


func _ready() -> void:
	T.set_language("en", false)
	_main = load("res://scenes/main.tscn").instantiate()
	add_child(_main)
	await _frames()

	# Título e idioma
	_check(_main._current is TitleScreen, "arranca en el título")
	var lang_buttons := _buttons(_main._current, "Español")
	_check(not lang_buttons.is_empty(), "hay selector de idioma")
	lang_buttons[0].pressed.emit()
	await _frames()
	_check(T.language() == "es", "el botón cambia el idioma a español")
	_check(not _buttons(_main._current, "Nueva expedición").is_empty(), "el título se retraduce")
	_buttons(_main._current, "English")[0].pressed.emit()
	await _frames()
	_check(T.language() == "en", "vuelve a inglés")
	_buttons(_main._current, "New expedition")[0].pressed.emit()
	await _frames()

	# Avatar → mapa estelar
	_check(_main._current is AvatarScreen, "pantalla de avatar")
	_buttons(_main._current, "Choose")[0].pressed.emit()
	await _frames()
	_check(_main._current is SectorScreen, "mapa estelar tras elegir avatar")
	var sector: SectorScreen = _main._current
	var camp: Campaign = _main._campaign
	var fuel0: int = GameState.fuel

	# Seleccionar un nodo alcanzable, escanear y saltar con los botones reales
	var target: String = camp.sector.nodes[camp.current]["edges"][0]
	sector._buttons[target].pressed.emit()
	await _frames()
	var scan_btn := _buttons(sector, "Scan")
	_check(not scan_btn.is_empty() and not scan_btn[0].disabled, "botón de escanear disponible")
	scan_btn[0].pressed.emit()
	await _frames()
	_check(camp.node(target)["scanned"], "el escaneo revela el nodo")
	var jump_btn := _buttons(sector, "Jump")
	_check(not jump_btn.is_empty() and not jump_btn[0].disabled, "botón de saltar disponible")
	jump_btn[0].pressed.emit()
	await _frames()
	_check(camp.current == target and GameState.fuel < fuel0, "el salto mueve la nave y gasta combustible")
	_check(not (_main._current is SectorScreen), "se abre la pantalla del nodo (%s)" % camp.node(target)["type"])

	# Planeta: clic y teclado reales sobre el mapa hexagonal
	var planet_id := _find_node(camp, "planet", false)
	_main._on_jumped(planet_id)
	await _frames()
	_check(_main._current is MapScreen, "pantalla de planeta")
	var screen: MapScreen = _main._current
	var view: PlanetMapView = screen._view
	_check(not view.enabled, "el mapa está bloqueado durante el briefing")
	_check(not _buttons(screen, "Do not descend").is_empty(), "en un planeta intermedio se puede no descender")
	_buttons(screen, "Descend")[0].pressed.emit()
	await _frames()
	_check(view.enabled, "el mapa se activa al descender")
	var ex := screen.expedition
	var adj := _adjacent(ex)
	var start := ex.player
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	click.pressed = true
	click.position = view.global_position + HexGrid.center(adj)
	click.global_position = click.position
	get_viewport().push_input(click)
	await _frames()
	_check(ex.player == adj, "un clic sobre un hexágono adyacente mueve al jugador (%s → %s)" % [start, ex.player])
	var before := ex.player
	for key in [KEY_D, KEY_E, KEY_C, KEY_A, KEY_Q, KEY_Z]:
		if ex.player != before or not screen._view.enabled:
			break
		var ev := InputEventKey.new()
		ev.keycode = key
		ev.pressed = true
		get_viewport().push_input(ev)
		await _frames()
	_check(ex.player != before or not screen._view.enabled, "el teclado mueve al jugador (o abre un evento)")
	screen.finished.emit({"result": "abort", "reason": ""})
	await _frames()
	_check(_main._current is SectorScreen, "tras abortar se vuelve al mapa estelar")

	# Contacto: recorre la conversación pulsando botones
	for sp in Content.campaign["species"]:
		var cid := _find_node(camp, "contact", false, sp)
		_main._on_jumped(cid)
		await _frames()
		_check(_main._current is ContactScreen, "pantalla de contacto (%s)" % sp)
		var guard := 0
		while _main._current is ContactScreen and guard < 20:
			guard += 1
			var btns := _enabled_buttons(_main._current)
			_check(not btns.is_empty(), "siempre hay un botón pulsable en el contacto")
			if btns.is_empty():
				break
			btns[0].pressed.emit()
			await _frames()
		_check(_main._current is SectorScreen, "el contacto %s termina y vuelve al mapa" % sp)

	# Anomalía
	var aid := _find_node(camp, "anomaly", false)
	_main._on_jumped(aid)
	await _frames()
	_check(_main._current is AnomalyScreen, "pantalla de anomalía")
	var guard2 := 0
	while _main._current is AnomalyScreen and guard2 < 5:
		guard2 += 1
		_enabled_buttons(_main._current)[0].pressed.emit()
		await _frames()
	_check(_main._current is SectorScreen, "la anomalía termina y vuelve al mapa")

	# Final: el planeta final aparece sin opción de saltarlo y da la victoria
	_main._on_jumped(camp.sector.final_id)
	await _frames()
	_check(_buttons(_main._current, "Do not descend").is_empty(), "el planeta final no se puede saltar")
	_main._current.finished.emit({"result": "success", "reason": ""})
	await _frames()
	_check(_main._current is EndScreen and _main._current.ending == "victory", "final de victoria")
	_buttons(_main._current, "Back to title")[0].pressed.emit()
	await _frames()
	_check(_main._current is TitleScreen, "vuelve al título")

	print("\n%s (%d fallos)" % ["UI OK" if _failures == 0 else "FALLOS", _failures])
	get_tree().quit(0 if _failures == 0 else 1)


func _frames(n := 3) -> void:
	for i in n:
		await get_tree().process_frame


func _find_node(camp: Campaign, type: String, done: bool, ref := "") -> String:
	for id in camp.sector.nodes:
		var n: Dictionary = camp.sector.nodes[id]
		if n["type"] == type and n["done"] == done and not n["final"] and (ref == "" or n["ref"] == ref):
			return id
	return ""


func _buttons(root: Node, starts_with: String) -> Array[Button]:
	var out: Array[Button] = []
	for n in root.find_children("*", "Button", true, false):
		if (n as Button).text.begins_with(starts_with):
			out.append(n)
	return out


func _enabled_buttons(root: Node) -> Array[Button]:
	var out: Array[Button] = []
	for n in root.find_children("*", "Button", true, false):
		var b := n as Button
		if b.visible and not b.disabled and b.text != "":
			out.append(b)
	return out


func _adjacent(ex: Expedition) -> Vector2i:
	for n in HexGrid.neighbors(ex.player):
		if ex.can_move(n) and ex.map.poi_at(n).is_empty():
			return n
	return ex.player


func _check(cond: bool, msg: String) -> void:
	print(("  ok: " if cond else "  FALLO: ") + msg)
	if not cond:
		_failures += 1
