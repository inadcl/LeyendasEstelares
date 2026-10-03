class_name MapScreen
extends Control
## Exploración de un planeta: mapa a la izquierda, HUD a la derecha, eventos como panel superpuesto.
## Termina con finished({result: "success"|"abort"|"fail"|"skip", reason}).

signal finished(outcome: Dictionary)

var planet: Dictionary = {}
var expedition: Expedition

var _view: PlanetMapView
var _log: RichTextLabel
var _o2_row: HBoxContainer
var _morale_row: HBoxContainer
var _data_chip: HBoxContainer
var _rep_label: Label
var _goal_label: Label
var _overlay: Overlay
var _rng := RandomNumberGenerator.new()


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE  # si no, este Control se come los clics del mapa
	_rng.randomize()
	expedition = Expedition.new(GameState, planet, Content.events, int(planet.get("seed", 1)))

	add_child(UITheme.background("bg_space", 0.3))
	var frame := UITheme.framed("panel_dark", Vector2i(0, 0), false)
	frame.position = Vector2(4, 4)
	frame.custom_minimum_size = Vector2(380, 260)
	frame.size = Vector2(380, 260)
	frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(frame)
	_view = PlanetMapView.new()
	_view.position = Vector2(8, 8)
	_view.expedition = expedition
	_view.cell_clicked.connect(_on_cell_clicked)
	add_child(_view)
	_build_hud()
	_overlay = Overlay.new()
	_overlay.opened.connect(func(): _view.enabled = false)
	_overlay.closed.connect(func(): _view.enabled = true)
	add_child(_overlay)
	GameState.changed.connect(_refresh_hud)
	_refresh_hud()
	(_o2_row.get_meta("bar") as PixelBar).snap()
	(_morale_row.get_meta("bar") as PixelBar).snap()
	_view.enabled = false
	_show_briefing()


func _build_hud() -> void:
	var logbox := UITheme.framed("panel_dark", Vector2i(8, 4))
	logbox.position = Vector2(4, 268)
	logbox.custom_minimum_size = Vector2(380, 88)
	logbox.size = Vector2(380, 88)
	add_child(logbox)
	_log = RichTextLabel.new()
	_log.bbcode_enabled = true
	_log.scroll_following = true
	_log.fit_content = false
	_log.custom_minimum_size = Vector2(360, 76)
	_log.add_theme_stylebox_override("normal", StyleBoxEmpty.new())
	logbox.add_child(_log)

	var panel := UITheme.framed("panel", Vector2i(10, 8))
	panel.position = Vector2(392, 4)
	panel.custom_minimum_size = Vector2(244, 352)
	panel.size = Vector2(244, 352)
	add_child(panel)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 5)
	panel.add_child(v)
	v.add_child(UITheme.label(T.t("planet.%s.name" % planet["id"]), UITheme.ACCENT_L, UITheme.SIZE_HEAD, true))
	v.add_child(UITheme.label(T.t("avatar.%s.name" % GameState.avatar["id"]), UITheme.TEXT))
	v.add_child(HSeparator.new())

	_o2_row = UITheme.meter_row("oxygen", Color("4fc3e8"), UITheme.ACCENT, 2.0)
	v.add_child(_o2_row)
	_morale_row = UITheme.meter_row("morale", Color("e0605c"), Color("ff9a94"))
	v.add_child(_morale_row)
	_data_chip = UITheme.chip("data", UITheme.ACCENT_L)
	v.add_child(_data_chip)
	_rep_label = UITheme.label("", UITheme.DIM)
	v.add_child(_rep_label)
	v.add_child(HSeparator.new())
	_goal_label = UITheme.label("", UITheme.WARN)
	v.add_child(_goal_label)
	var spacer := Control.new()
	spacer.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(spacer)
	v.add_child(UITheme.label(T.t("ui.map.hint"), UITheme.DIM))
	var abort := UITheme.button(T.t("ui.map.abort"))
	abort.alignment = HORIZONTAL_ALIGNMENT_CENTER
	abort.pressed.connect(_confirm_abort)
	v.add_child(abort)


func _refresh_hud() -> void:
	(_o2_row.get_meta("label") as Label).text = "%d/%d" % [GameState.oxygen, GameState.max_oxygen]
	var o2: PixelBar = _o2_row.get_meta("bar")
	o2.max_value = GameState.max_oxygen
	o2.value = GameState.oxygen
	(_morale_row.get_meta("label") as Label).text = "%d/%d" % [GameState.morale, GameState.max_morale]
	var mo: PixelBar = _morale_row.get_meta("bar")
	mo.max_value = GameState.max_morale
	mo.value = GameState.morale
	(_data_chip.get_meta("label") as Label).text = str(GameState.data)
	var parts: Array[String] = []
	for f in GameState.rep:
		parts.append("%s %+d" % [T.t("faction." + f), GameState.rep[f]])
	_rep_label.text = T.t("ui.hud.rep", {"list": ", ".join(parts) if not parts.is_empty() else "—"})
	_goal_label.text = T.t("ui.map.goal_done" if expedition.objective_done else "ui.map.goal_pending")


func _say(text: String, color := UITheme.TEXT) -> void:
	_log.append_text("[color=#%s]%s[/color]\n" % [color.to_html(false), text])


# ---------------------------------------------------------------- movimiento
func _on_cell_clicked(cell: Vector2i) -> void:
	if not expedition.can_move(cell):
		return
	var cost := expedition.map.move_cost(cell)
	var res := expedition.move(cell)
	Sfx.play("step", -4.0)
	_say(T.t("ui.log.move", {"cost": cost}), UITheme.DIM)
	if res["failure"] != "":
		_fail(res["failure"])
	elif not res["poi"].is_empty():
		_open_event(res["poi"])
	elif res["home"]:
		_conclude("success")


# ------------------------------------------------------------------- diálogos
func _show_briefing() -> void:
	var pid: String = planet["id"]
	_overlay.open()
	_overlay.title(T.t("ui.briefing.title", {"planet": T.t("planet.%s.name" % pid)}), UITheme.ACCENT, UITheme.tex_icon("node_planet_" + planet.get("biome", "frost")))
	_overlay.body(T.t("planet.%s.intro" % pid))
	_overlay.button(T.t("ui.descend"), func():
		_overlay.close()
		_say(T.t("ui.log.descend"), UITheme.ACCENT)
	).grab_focus()
	if not planet.get("final", false):
		_overlay.button(T.t("ui.skip_planet"), func(): finished.emit({"result": "skip", "reason": ""}))


func _open_event(poi: Dictionary) -> void:
	_overlay.present_event(
		poi["event_id"],
		func(i: int): return expedition.resolve_choice(poi, i, _rng),
		func(): _after_event(poi))


func _after_event(poi: Dictionary) -> void:
	_say("%s" % T.ev(poi["event_id"], "title"), UITheme.TEXT)
	if poi["objective"]:
		_say(T.t("ui.map.goal_done"), UITheme.GOOD)
	var reason := GameState.failure_reason()
	if reason != "":
		_fail(reason)
		return
	_overlay.close()


func _fail(reason: String) -> void:
	Sfx.play("defeat")
	_overlay.open()
	_overlay.title(T.t("ui.fail.title"), UITheme.BAD)
	_overlay.body(T.t("ui.fail.oxygen" if reason == "oxygen" else "ui.fail.morale"))
	_overlay.button(T.t("ui.continue"), func(): finished.emit({"result": "fail", "reason": reason})).grab_focus()


func _confirm_abort() -> void:
	if _overlay.is_open():
		return
	_overlay.open()
	_overlay.title(T.t("ui.abort.title"), UITheme.WARN)
	_overlay.body(T.t("ui.abort.body"))
	_overlay.button(T.t("ui.abort.yes"), func(): _conclude("abort")).grab_focus()
	_overlay.button(T.t("ui.abort.no"), _overlay.close)


## Cierra la salida con un pequeño epílogo del planeta.
func _conclude(result: String) -> void:
	var pid: String = planet["id"]
	_overlay.open()
	Sfx.play("success" if result == "success" else "setback")
	if result == "success":
		_overlay.title(T.t("ui.planet.done"), UITheme.GOOD)
		_overlay.body(T.t("planet.%s.outro_success" % pid))
	else:
		_overlay.title(T.t("ui.planet.aborted"), UITheme.WARN)
		_overlay.body(T.t("planet.%s.outro_abort" % pid))
	_overlay.button(T.t("ui.continue"), func(): finished.emit({"result": result, "reason": ""})).grab_focus()
