extends Control
## Raíz del juego: título → avatar → mapa estelar → (planeta | contacto | anomalía) → … → final.
## Atajos globales: F1 ayuda, M sonido, F11 pantalla completa.
## Se adapta a la orientación: apaisado (640x360) o vertical (360x640+); ver Layout.

var _current: Control
var _campaign: Campaign
var _vignette: ColorRect
var _help: Overlay
var _rebuild := Callable()  # reconstruye la pantalla actual si no tiene estado propio (título, mapa estelar...)
var _stateful := false  # pantallas con partida en curso (planeta, contacto, anomalía): cambian de orientación al terminar


func _ready() -> void:
	T.load_language()
	# Pruebas en escritorio: `godot --path . -- --portrait` abre una ventana con forma de móvil.
	var args := OS.get_cmdline_user_args()
	if "--portrait" in args and DisplayServer.get_name() != "headless":
		get_window().size = Vector2i(540, 960)
		get_window().move_to_center()
	Layout.apply(get_window(), Layout.wants_portrait(get_window()))
	get_window().size_changed.connect(_on_window_resized)
	theme = UITheme.build()
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_vignette = ColorRect.new()
	_vignette.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	_vignette.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var mat := ShaderMaterial.new()
	mat.shader = load("res://shaders/vignette.gdshader")
	_vignette.material = mat
	add_child(_vignette)
	if DisplayServer.get_name() != "headless":
		Input.set_custom_mouse_cursor(load("res://ui/cursor.png"), Input.CURSOR_ARROW, Vector2(2, 2))
	# Todos los botones suenan al pulsarse y al pasar el ratón por encima.
	get_tree().node_added.connect(func(n: Node):
		if n is BaseButton:
			var b := n as BaseButton
			b.pressed.connect(func(): Sfx.play("click", -6.0))
			b.mouse_entered.connect(func():
				if not b.disabled:
					Sfx.play("tick", -12.0)))
	Sfx.start_music()
	_show_title()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_F1:
				_toggle_help()
			KEY_M:
				Sfx.toggle_mute()
			KEY_F11:
				var full := DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN
				DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED if full else DisplayServer.WINDOW_MODE_FULLSCREEN)


## La orientación solo cambia entre pantallas con estado propio; en las demás se reconstruye al instante.
func _on_window_resized() -> void:
	var want := Layout.wants_portrait(get_window())
	if want == Layout.portrait or _stateful or not _rebuild.is_valid():
		return
	Layout.apply(get_window(), want)
	_rebuild.call()


func _swap(screen: Control) -> void:
	var want := Layout.wants_portrait(get_window())
	if want != Layout.portrait:
		Layout.apply(get_window(), want)
	if _current != null:
		_current.queue_free()
	_current = screen
	add_child(screen)
	move_child(_vignette, -1)  # la viñeta siempre por encima
	if _help != null:
		move_child(_help, -1)
	screen.modulate.a = 0.0
	create_tween().tween_property(screen, "modulate:a", 1.0, 0.25)


func _toggle_help() -> void:
	if _help != null and _help.is_open():
		_help.close()
		return
	if _help == null:
		_help = Overlay.new()
		add_child(_help)
	_help.show_help()
	move_child(_help, -1)


func _show_title() -> void:
	_stateful = false
	_rebuild = _show_title
	var s := TitleScreen.new()
	s.start_pressed.connect(_show_avatars)
	s.quit_pressed.connect(func(): get_tree().quit())
	s.language_changed.connect(_show_title)
	s.help_pressed.connect(_toggle_help)
	_swap(s)


func _show_avatars() -> void:
	_stateful = false
	_rebuild = _show_avatars
	var s := AvatarScreen.new()
	s.avatar_chosen.connect(func(id: String):
		GameState.start_run(Content.avatar_by_id(id), Content.factions, Content.campaign)
		_campaign = Campaign.new(GameState, Content.campaign, randi())
		_show_sector()
		# La primera vez se muestra la ayuda (después, con F1 o desde el título).
		if not bool(Settings.get_value("game", "help_seen", false)):
			Settings.set_value("game", "help_seen", true)
			_toggle_help())
	_swap(s)


func _show_sector() -> void:
	_stateful = false
	_rebuild = _show_sector
	var s := SectorScreen.new()
	s.campaign = _campaign
	s.jumped.connect(_on_jumped)
	_swap(s)


func _on_jumped(id: String) -> void:
	_stateful = true
	var node := _campaign.node(id)
	match node["type"]:
		"planet":
			GameState.begin_planet()
			var s := MapScreen.new()
			s.planet = node["planet"]
			s.finished.connect(func(outcome: Dictionary): _after_planet(id, outcome))
			_swap(s)
		"contact":
			var s := ContactScreen.new()
			s.species_id = node["ref"]
			s.finished.connect(func(_outcome: Dictionary): _after_node(id))
			_swap(s)
		_:
			var s := AnomalyScreen.new()
			s.event_id = node["ref"]
			s.finished.connect(func(): _after_node(id))
			_swap(s)


func _after_planet(id: String, outcome: Dictionary) -> void:
	if outcome["result"] == "fail":
		_end(outcome["reason"])
		return
	if _campaign.is_final(id):
		_end("victory" if outcome["result"] == "success" else "abort")
		return
	_after_node(id)


func _after_node(id: String) -> void:
	_campaign.finish_node(id)
	var reason := _campaign.end_reason()
	if reason != "":
		_end(reason)
	else:
		_show_sector()


func _end(ending: String) -> void:
	_stateful = false
	_rebuild = func(): _end(ending)
	var s := EndScreen.new()
	s.ending = ending
	s.jumps = _campaign.jumps
	s.continue_pressed.connect(_show_title)
	_swap(s)
