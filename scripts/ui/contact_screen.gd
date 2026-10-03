class_name ContactScreen
extends Control
## Comunicación de primer contacto: monitor con el retrato de la especie, barras de confianza/tensión y
## respuestas por postura, con texto que se escribe poco a poco. Termina con finished({result}).

signal finished(outcome: Dictionary)

const TYPE_SPEED := 70.0  # caracteres por segundo
const STANCE_COLORS := {"open": Color("ffe0a0"), "careful": Color("a8ecff"), "firm": Color("ff9a94"), "deceive": Color("c8a8ff")}

var species_id := ""
var runner: ContactRunner

var _species: Dictionary
var _color := Color.WHITE
var _trust_bar: PixelBar
var _tension_bar: PixelBar
var _trust_label: Label
var _tension_label: Label
var _speech: Label
var _extra: Label
var _options: VBoxContainer
var _tween: Tween


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	_species = Content.species_by_id(species_id)
	_color = Color(_species["color"])
	runner = ContactRunner.new(GameState, _species, Content.encounter_for(species_id))
	add_child(UITheme.background("bg_space", 0.35))
	_build_left()
	_build_right()
	_refresh_bars()
	_bars_snap()
	_show_intro()


func _unhandled_input(event: InputEvent) -> void:
	# Un clic o Enter completa el texto que se está escribiendo.
	if _tween != null and _tween.is_running():
		if (event is InputEventMouseButton and event.pressed) or (event is InputEventKey and event.pressed and event.keycode in [KEY_ENTER, KEY_SPACE]):
			_finish_typing()
			get_viewport().set_input_as_handled()


func _build_left() -> void:
	var panel := UITheme.framed("panel", Vector2i(10, 8))
	panel.position = Vector2(8, 8)
	panel.custom_minimum_size = Vector2(204, 344)
	panel.size = Vector2(204, 344)
	add_child(panel)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 6)
	panel.add_child(v)
	var bezel := PanelContainer.new()
	bezel.add_theme_stylebox_override("panel", UITheme.tex_box("bezel", 10, Vector2i(10, 10)))
	bezel.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	var portrait := TextureRect.new()
	portrait.texture = UITheme.tex_icon(_species["portrait"])
	portrait.custom_minimum_size = Vector2(96, 96)
	portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	var mat := ShaderMaterial.new()
	mat.shader = load("res://shaders/comm.gdshader")
	mat.set_shader_parameter("tint", _color)
	portrait.material = mat
	bezel.add_child(portrait)
	v.add_child(bezel)
	v.add_child(UITheme.label(T.t("species.%s.name" % species_id), _color, UITheme.SIZE_HEAD, true))
	v.add_child(UITheme.label(T.t("species.%s.desc" % species_id), UITheme.DIM))
	var hint := _hint_text()
	if hint != "":
		v.add_child(HSeparator.new())
		v.add_child(UITheme.label(hint, UITheme.WARN))


func _hint_text() -> String:
	var value := T.t("ui.value." + runner.best_stance())
	if GameState.has_trait("ciencia"):
		return T.t("ui.contact.analysis", {"value": value})
	if GameState.has_flag("met_" + species_id):
		return T.t("ui.contact.experience", {"value": value})
	return ""


func _build_right() -> void:
	var panel := UITheme.framed("panel_accent", Vector2i(12, 8))
	panel.position = Vector2(220, 8)
	panel.custom_minimum_size = Vector2(412, 344)
	panel.size = Vector2(412, 344)
	add_child(panel)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 6)
	panel.add_child(v)

	var bars := HBoxContainer.new()
	bars.add_theme_constant_override("separation", 14)
	v.add_child(bars)
	var trust := _meter(UITheme.GOOD)
	_trust_label = trust[0]
	_trust_bar = trust[1]
	bars.add_child(trust[2])
	var tension := _meter(UITheme.BAD)
	_tension_label = tension[0]
	_tension_bar = tension[1]
	bars.add_child(tension[2])

	_speech = UITheme.label("", _color)
	_speech.custom_minimum_size = Vector2(386, 58)
	v.add_child(_speech)
	_extra = UITheme.label("", UITheme.WARN)
	_extra.autowrap_mode = TextServer.AUTOWRAP_OFF
	v.add_child(_extra)
	v.add_child(HSeparator.new())
	_options = VBoxContainer.new()
	_options.add_theme_constant_override("separation", 4)
	v.add_child(_options)


## Medidor con etiqueta y barra: devuelve [label, bar, contenedor].
func _meter(color: Color) -> Array:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 2)
	box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var label := UITheme.label("", UITheme.TEXT)
	label.autowrap_mode = TextServer.AUTOWRAP_OFF
	box.add_child(label)
	var bar := PixelBar.new(color, 14)
	bar.max_value = ContactRunner.MAX_METER
	bar.seg_units = 1.0
	box.add_child(bar)
	return [label, bar, box]


func _bars_snap() -> void:
	_trust_bar.snap()
	_tension_bar.snap()


func _refresh_bars() -> void:
	_trust_bar.value = runner.trust
	_tension_bar.value = runner.tension
	_trust_label.text = "%s  %d/%d" % [T.t("ui.contact.trust"), runner.trust, ContactRunner.MAX_METER]
	_tension_label.text = "%s  %d/%d" % [T.t("ui.contact.tension"), runner.tension, ContactRunner.MAX_METER]


# ----------------------------------------------------------------- texto
func _say(text: String, color: Color) -> void:
	if _tween != null:
		_tween.kill()
	_speech.text = text
	_speech.add_theme_color_override("font_color", color)
	_speech.visible_characters = 0
	_options.visible = false
	var chars := text.length()
	_tween = create_tween()
	_tween.tween_property(_speech, "visible_characters", chars, float(chars) / TYPE_SPEED)
	_tween.finished.connect(_typing_done)


func _finish_typing() -> void:
	if _tween != null:
		_tween.kill()
	_speech.visible_characters = -1
	_typing_done()


func _typing_done() -> void:
	_speech.visible_characters = -1
	_options.visible = true
	for c in _options.get_children():
		var b: Button = c.find_children("*", "Button", true, false)[0] if c is HBoxContainer else null
		if b != null and not b.disabled:
			b.grab_focus()
			break


func _clear_options() -> void:
	for c in _options.get_children():
		_options.remove_child(c)
		c.queue_free()


func _add_option(text: String, cb: Callable, disabled := false, stance := "") -> Button:
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 6)
	if stance != "":
		var ic := UITheme.icon("stance_" + stance, 2)
		ic.tooltip_text = T.t("ui.stance." + stance)
		ic.self_modulate = Color.WHITE if not disabled else Color(1, 1, 1, 0.4)
		row.add_child(ic)
	var b := UITheme.button(text)
	b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	b.disabled = disabled
	b.pressed.connect(cb)
	row.add_child(b)
	_options.add_child(row)
	return b


func _show_intro() -> void:
	_clear_options()
	_say(T.t("contact.%s.intro" % runner.encounter["id"]), UITheme.TEXT)
	_extra.text = ""
	_add_option(T.t("ui.continue"), _show_prompt)


func _show_prompt() -> void:
	_clear_options()
	var eid: String = runner.encounter["id"]
	var x := runner.index
	_say(T.t("contact.%s.x%d.prompt" % [eid, x]), _color)
	_extra.text = ""
	var opts: Array = runner.exchange()["options"]
	for i in opts.size():
		var hint := T.t("contact.%s.x%d.o%d.hint" % [eid, x, i]) if opts[i].has("requires") else ""
		var lock := runner.lock_reason(i, hint)
		var label := "%s: %s" % [T.t("ui.stance." + opts[i]["stance"]), T.t("contact.%s.x%d.o%d" % [eid, x, i])]
		if lock != "":
			label += "   [%s]" % lock
		_add_option(label, _on_choose.bind(i), lock != "", opts[i]["stance"])


func _on_choose(i: int) -> void:
	var res := runner.choose(i)
	Sfx.play("blip")
	_refresh_bars()
	_clear_options()
	_say(T.t(res["key"]), _color)
	_extra.text = "  ·  ".join(res["lines"])
	_add_option(T.t("ui.continue"), _after_reply)


func _after_reply() -> void:
	if runner.finished():
		_show_outcome()
	else:
		_show_prompt()


func _show_outcome() -> void:
	_clear_options()
	var out := runner.apply_outcome()
	Sfx.play({"alliance": "victory", "deal": "success", "wary": "event", "hostile": "alert"}[out["id"]])
	var colors := {"alliance": UITheme.GOOD, "deal": UITheme.ACCENT, "wary": UITheme.DIM, "hostile": UITheme.BAD}
	_say("%s\n%s" % [T.t("ui.contact.result." + out["id"]).to_upper(), T.t(out["key"])], colors[out["id"]])
	_extra.text = "  ·  ".join(out["lines"])
	_add_option(T.t("ui.contact.close"), func(): finished.emit({"result": out["id"]}))
