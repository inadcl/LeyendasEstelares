class_name Overlay
extends Control
## Panel modal reutilizable (briefings, eventos, resultados). Contiene la lógica de presentar un evento.

signal opened
signal closed

const EVENT_ICONS := {
	"signal": "poi_signal", "ruins": "poi_ruins", "wreck": "poi_wreck",
	"life": "poi_life", "beacon": "poi_beacon", "anomaly": "node_anomaly",
}

var _dim: ColorRect
var _panel: PanelContainer
var _scroll: ScrollContainer
var _box: VBoxContainer
var _w := 512.0  # ancho útil del contenido


func _init() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	visible = false
	_dim = ColorRect.new()
	_dim.color = Color(0.01, 0.02, 0.06, 0.62)
	_dim.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	_dim.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_dim)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)
	_panel = UITheme.framed("panel_accent", Vector2i(14, 12))
	center.add_child(_panel)
	_scroll = ScrollContainer.new()
	_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	_panel.add_child(_scroll)
	_box = VBoxContainer.new()
	_box.add_theme_constant_override("separation", 8)
	_scroll.add_child(_box)
	# El alto del panel sigue al contenido (los textos largos cambian su altura al ajustarse el ancho).
	_box.minimum_size_changed.connect(_fit)


func is_open() -> bool:
	return visible


func open() -> void:
	for c in _box.get_children():
		_box.remove_child(c)
		c.queue_free()
	var vs := get_viewport_rect().size
	_w = minf(512.0, vs.x - 24.0 - 28.0)
	_box.custom_minimum_size = Vector2(_w, 0)
	_scroll.custom_minimum_size = Vector2(_w, 0)
	visible = true
	_fit.call_deferred()
	opened.emit()


## Altura del panel: la del contenido, con tope en la pantalla (si no cabe, se desplaza).
func _fit() -> void:
	UITheme.fit_scroll(_scroll, _box, get_viewport_rect().size.y - 24.0 - 24.0)


func close() -> void:
	visible = false
	closed.emit()


## Título con icono opcional (textura 16x16 ampliada al doble).
func title(text: String, color := UITheme.ACCENT, icon_tex: Texture2D = null) -> void:
	var l := UITheme.label(text, color, UITheme.SIZE_HEAD, true)
	if icon_tex == null:
		_box.add_child(l)
		_box.add_child(HSeparator.new())
		return
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 10)
	var ic := TextureRect.new()
	ic.texture = icon_tex
	ic.custom_minimum_size = Vector2(32, 32)
	ic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	ic.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	row.add_child(ic)
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	l.size_flags_horizontal = Control.SIZE_EXPAND_FILL  # sin esto el autowrap parte el título letra a letra
	l.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	row.add_child(l)
	_box.add_child(row)
	_box.add_child(HSeparator.new())


func body(text: String) -> void:
	var l := UITheme.label(text, UITheme.TEXT)
	l.custom_minimum_size = Vector2(_w, 0)
	_box.add_child(l)


func note(text: String, color := UITheme.WARN) -> void:
	var l := UITheme.label(text, color)
	l.custom_minimum_size = Vector2(_w, 0)
	_box.add_child(l)


func separator() -> void:
	_box.add_child(HSeparator.new())


func button(text: String, cb: Callable, disabled := false) -> Button:
	var b := UITheme.button(text)
	b.custom_minimum_size = Vector2(_w, 0)
	b.disabled = disabled
	b.pressed.connect(cb)
	_box.add_child(b)
	return b


## Contenido de «Cómo se juega» (con el interruptor de sonido, útil sin teclado).
func show_help() -> void:
	open()
	title(T.t("ui.help.title"))
	body(T.t("ui.help.sector"))
	body(T.t("ui.help.contact"))
	body(T.t("ui.help.planet"))
	note(T.t("ui.help.keys"), UITheme.DIM)
	var sound := button(T.t("ui.sound_off" if Sfx.muted else "ui.sound_on"), func(): pass)
	sound.alignment = HORIZONTAL_ALIGNMENT_CENTER
	sound.pressed.connect(func():
		Sfx.toggle_mute()
		sound.text = T.t("ui.sound_off" if Sfx.muted else "ui.sound_on"))
	var close_btn := button(T.t("ui.help.close"), close)
	close_btn.alignment = HORIZONTAL_ALIGNMENT_CENTER
	close_btn.grab_focus()


## Presenta un evento y resuelve la elección con `resolve(index) -> {text, lines, success}`;
## al pulsar Continuar llama a `on_done`.
func present_event(event_id: String, resolve: Callable, on_done: Callable) -> void:
	var ev: Dictionary = Content.events[event_id]
	open()
	Sfx.play("event")
	title(T.ev(event_id, "title"), UITheme.ACCENT, UITheme.tex_icon(EVENT_ICONS.get(ev["type"], "poi_signal")))
	body(T.ev(event_id, "text"))
	separator()
	var first: Button = null
	for i in ev["choices"].size():
		var choice: Dictionary = ev["choices"][i]
		var hint := T.ev(event_id, "c%d.hint" % i) if choice.has("requires") else ""
		var lock := EventRunner.lock_reason(choice, GameState, hint)
		var label := T.ev(event_id, "c%d.text" % i)
		if lock != "":
			label += "   [%s]" % lock
		elif choice.has("risk"):
			label += "   (%s)" % _chance_text(choice)
		var b := button(label, _on_pick.bind(event_id, i, resolve, on_done), lock != "")
		if first == null and lock == "":
			first = b
	if first != null:
		first.grab_focus()


func _chance_text(choice: Dictionary) -> String:
	var pct := roundi(EventRunner.success_chance(choice, GameState) * 100.0)
	if choice.has("tag") and GameState.has_trait(choice["tag"]):
		return T.t("ui.choice.chance_bonus", {"pct": pct, "trait": T.t("trait." + choice["tag"])})
	return T.t("ui.choice.chance", {"pct": pct})


func _on_pick(event_id: String, index: int, resolve: Callable, on_done: Callable) -> void:
	var choice: Dictionary = Content.events[event_id]["choices"][index]
	var result: Dictionary = resolve.call(index)
	open()
	Sfx.play(("success" if result["success"] else "setback") if choice.has("risk") else "blip")
	var headline := T.ev(event_id, "title")
	var tint := UITheme.ACCENT
	if choice.has("risk"):
		headline += " — " + T.t("ui.event.success" if result["success"] else "ui.event.setback")
		tint = UITheme.GOOD if result["success"] else UITheme.BAD
	title(headline, tint, UITheme.tex_icon(EVENT_ICONS.get(Content.events[event_id]["type"], "poi_signal")))
	body(result["text"])
	if not result["lines"].is_empty():
		note("  ·  ".join(result["lines"]))
	button(T.t("ui.continue"), on_done).grab_focus()
