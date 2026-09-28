class_name MapScreen
extends Control
## Pantalla de exploración: mapa a la izquierda, HUD a la derecha, eventos como panel superpuesto.

signal finished(outcome: Dictionary)

var planet: Dictionary = {}
var expedition: Expedition

var _view: PlanetMapView
var _log: RichTextLabel
var _o2_label: Label
var _o2_bar: ProgressBar
var _morale_label: Label
var _morale_bar: ProgressBar
var _data_label: Label
var _rep_label: Label
var _goal_label: Label
var _dim: ColorRect
var _overlay: PanelContainer
var _overlay_box: VBoxContainer
var _rng := RandomNumberGenerator.new()


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE  # si no, este Control se come los clics del mapa
	_rng.randomize()
	var seed_value := int(planet.get("seed", 1)) + _rng.randi() % 100000
	expedition = Expedition.new(GameState, planet, Content.events, seed_value)

	add_child(UITheme.background())
	_view = PlanetMapView.new()
	_view.position = Vector2(8, 8)
	_view.expedition = expedition
	_view.cell_clicked.connect(_on_cell_clicked)
	add_child(_view)
	_build_hud()
	_build_overlay()
	GameState.changed.connect(_refresh_hud)
	_refresh_hud()
	_view.enabled = false
	_show_briefing()


func _build_hud() -> void:
	_log = RichTextLabel.new()
	_log.position = Vector2(8, 258)
	_log.size = Vector2(354, 94)
	_log.bbcode_enabled = true
	_log.scroll_following = true
	_log.add_theme_font_size_override("normal_font_size", 11)
	_log.add_theme_stylebox_override("normal", UITheme.box(Color(0.04, 0.05, 0.09, 0.85), UITheme.PANEL_BORDER, 5))
	add_child(_log)

	var panel := PanelContainer.new()
	panel.position = Vector2(370, 8)
	panel.size = Vector2(262, 344)
	add_child(panel)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 5)
	panel.add_child(v)
	v.add_child(UITheme.label(planet.get("name", ""), UITheme.ACCENT, 16))
	v.add_child(UITheme.label(GameState.avatar.get("name", ""), UITheme.TEXT, 12))
	v.add_child(UITheme.label(GameState.avatar.get("role", ""), UITheme.DIM, 10))
	v.add_child(HSeparator.new())
	_o2_label = UITheme.label("", UITheme.TEXT, 11)
	v.add_child(_o2_label)
	_o2_bar = UITheme.bar(Color("4fc3e8"))
	v.add_child(_o2_bar)
	_morale_label = UITheme.label("", UITheme.TEXT, 11)
	v.add_child(_morale_label)
	_morale_bar = UITheme.bar(Color("e8b45c"))
	v.add_child(_morale_bar)
	_data_label = UITheme.label("", UITheme.ACCENT, 11)
	v.add_child(_data_label)
	_rep_label = UITheme.label("", UITheme.DIM, 10)
	v.add_child(_rep_label)
	v.add_child(HSeparator.new())
	_goal_label = UITheme.label("", UITheme.WARN, 11)
	v.add_child(_goal_label)
	var hint := UITheme.label("Clic en un hexágono resaltado para avanzar (o teclas Q E / A D / Z C). El número es el oxígeno que cuesta. Guarda aire para volver.", UITheme.DIM, 10)
	v.add_child(hint)
	var spacer := Control.new()
	spacer.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(spacer)
	var abort := UITheme.button("Abortar misión")
	abort.alignment = HORIZONTAL_ALIGNMENT_CENTER
	abort.pressed.connect(_confirm_abort)
	v.add_child(abort)


func _build_overlay() -> void:
	_dim = ColorRect.new()
	_dim.color = Color(0, 0, 0, 0.55)
	_dim.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	_dim.mouse_filter = Control.MOUSE_FILTER_STOP
	_dim.visible = false
	add_child(_dim)
	_overlay = PanelContainer.new()
	_overlay.position = Vector2(64, 28)
	_overlay.size = Vector2(512, 100)
	_overlay.visible = false
	add_child(_overlay)
	_overlay_box = VBoxContainer.new()
	_overlay_box.add_theme_constant_override("separation", 8)
	_overlay.add_child(_overlay_box)


func _refresh_hud() -> void:
	_o2_label.text = "OXÍGENO  %d / %d" % [GameState.oxygen, GameState.max_oxygen]
	_o2_bar.max_value = GameState.max_oxygen
	_o2_bar.value = GameState.oxygen
	_morale_label.text = "MORAL  %d / %d" % [GameState.morale, GameState.max_morale]
	_morale_bar.max_value = GameState.max_morale
	_morale_bar.value = GameState.morale
	_data_label.text = "DATOS  %d" % GameState.data
	var parts: Array[String] = []
	for f in GameState.rep:
		parts.append("%s %+d" % [GameState.faction_names.get(f, f), GameState.rep[f]])
	_rep_label.text = "Reputación: " + (", ".join(parts) if not parts.is_empty() else "—")
	if expedition.objective_done:
		_goal_label.text = "Objetivo cumplido. Regresa a la nave."
	else:
		_goal_label.text = "Objetivo: alcanzar la baliza (este) y volver a la nave."
	_view.queue_redraw()


func _say(text: String, color := UITheme.TEXT) -> void:
	_log.append_text("[color=#%s]%s[/color]\n" % [color.to_html(false), text])


# ---------------------------------------------------------------- movimiento
func _on_cell_clicked(cell: Vector2i) -> void:
	if not expedition.can_move(cell):
		return
	var cost := expedition.map.move_cost(cell)
	var res := expedition.move(cell)
	_say("Avanzas (−%d oxígeno)." % cost, UITheme.DIM)
	if res["failure"] != "":
		_fail(res["failure"])
	elif not res["poi"].is_empty():
		_open_event(res["poi"])
	elif res["home"]:
		_finish("success")


# ------------------------------------------------------------------- overlay
func _open_overlay() -> void:
	for c in _overlay_box.get_children():
		_overlay_box.remove_child(c)
		c.queue_free()
	_view.enabled = false
	_dim.visible = true
	_overlay.visible = true


func _close_overlay() -> void:
	_dim.visible = false
	_overlay.visible = false
	_view.enabled = true


func _add_body(text: String) -> void:
	var l := UITheme.label(text, UITheme.TEXT, 12)
	l.custom_minimum_size = Vector2(490, 0)
	_overlay_box.add_child(l)


func _add_button(text: String, cb: Callable, disabled := false) -> Button:
	var b := UITheme.button(text)
	b.custom_minimum_size = Vector2(490, 0)
	b.disabled = disabled
	b.pressed.connect(cb)
	_overlay_box.add_child(b)
	return b


func _show_briefing() -> void:
	_open_overlay()
	_overlay_box.add_child(UITheme.label("Descenso a " + planet.get("name", ""), UITheme.ACCENT, 16))
	_add_body(planet.get("intro", ""))
	_add_button("Descender", func():
		_close_overlay()
		_say("Desciendes a la superficie. Objetivo: la baliza, al este.", UITheme.ACCENT)
	).grab_focus()


func _open_event(poi: Dictionary) -> void:
	var ev := expedition.event_of(poi)
	_open_overlay()
	_overlay_box.add_child(UITheme.label(ev["title"], UITheme.ACCENT, 16))
	_add_body(ev["text"])
	_overlay_box.add_child(HSeparator.new())
	var first: Button = null
	for choice in ev["choices"]:
		var lock := EventRunner.lock_reason(choice, GameState)
		var label: String = choice["text"]
		if lock != "":
			label += "   [%s]" % lock
		elif choice.has("risk"):
			label += "   (%d%% de éxito%s)" % [roundi(EventRunner.success_chance(choice, GameState) * 100.0), _bonus_note(choice)]
		var b := _add_button(label, _on_choice.bind(poi, choice), lock != "")
		if first == null and lock == "":
			first = b
	if first != null:
		first.grab_focus()


func _bonus_note(choice: Dictionary) -> String:
	if choice.has("tag") and GameState.has_trait(choice["tag"]):
		return ", ventaja de " + choice["tag"]
	return ""


func _on_choice(poi: Dictionary, choice: Dictionary) -> void:
	var result := expedition.resolve_choice(poi, choice, _rng)
	var ev := expedition.event_of(poi)
	_open_overlay()
	var risky: bool = choice.has("risk")
	var headline: String = ev["title"]
	if risky:
		headline += " — " + ("éxito" if result["success"] else "revés")
	_overlay_box.add_child(UITheme.label(headline, UITheme.GOOD if result["success"] else UITheme.BAD, 16))
	_add_body(result["text"])
	if not result["lines"].is_empty():
		_overlay_box.add_child(UITheme.label("  ·  ".join(result["lines"]), UITheme.WARN, 12))
	_say("%s: %s" % [ev["title"], result["text"]], UITheme.TEXT)
	if poi["objective"]:
		_say("Objetivo cumplido. Regresa a la nave.", UITheme.GOOD)
	_add_button("Continuar", _after_event).grab_focus()


func _after_event() -> void:
	var reason := GameState.failure_reason()
	if reason != "":
		_fail(reason)
		return
	_close_overlay()


func _fail(reason: String) -> void:
	_open_overlay()
	_overlay_box.add_child(UITheme.label("Expedición perdida", UITheme.BAD, 16))
	_add_body("Se agotó el oxígeno lejos de la nave." if reason == "oxygen" else "La moral de la expedición se ha quebrado.")
	_add_button("Continuar", func(): _finish("fail", reason)).grab_focus()


func _confirm_abort() -> void:
	if _overlay.visible:
		return
	_open_overlay()
	_overlay_box.add_child(UITheme.label("¿Abortar la misión?", UITheme.WARN, 16))
	_add_body("Serás evacuado a la Meridiana. La misión quedará incompleta.")
	_add_button("Sí, abortar", func(): _finish("abort")).grab_focus()
	_add_button("Seguir explorando", _close_overlay)


func _finish(result: String, reason := "") -> void:
	finished.emit({"result": result, "reason": reason})
