class_name SectorScreen
extends Control
## Mapa estelar tipo FTL: elige a dónde saltar, escanea para reducir la incertidumbre y gestiona el combustible.

signal jumped(node_id: String)

const MAP_X0 := 62.0
const MAP_X1 := 578.0
const MAP_Y0 := 74.0
const MAP_H := 186.0
const NODE_SIZE := Vector2(36, 36)
const BADGES := ["idle", "reach", "current", "done", "selected"]

var campaign: Campaign

var _buttons := {}  # id -> Button
var _selected := ""
var _lines: _Lines
var _ship: TextureRect
var _fuel_chip: HBoxContainer
var _fuel_bar: PixelBar
var _scan_chip: HBoxContainer
var _data_chip: HBoxContainer
var _morale_chip: HBoxContainer
var _morale_bar: PixelBar
var _info_title: Label
var _info_body: Label
var _jump_btn: Button
var _scan_btn: Button
var _time := 0.0


class _Lines extends Control:
	var screen: SectorScreen

	func _process(_d: float) -> void:
		queue_redraw()

	func _draw() -> void:
		var c := screen.campaign
		var t := Time.get_ticks_msec() / 1000.0
		for id in c.sector.nodes:
			var a: Dictionary = c.sector.nodes[id]
			for to in a["edges"]:
				var reachable: bool = id == c.current and c.can_jump(to)
				var a_pos := screen.node_pos(id)
				var b_pos := screen.node_pos(to)
				var dir := (b_pos - a_pos)
				var length := dir.length()
				dir = dir / length
				var col := Color("e8b45c") if reachable else Color("3a4670")
				var step := 6.0
				var shift := fposmod(t * 10.0, step) if reachable else 0.0
				var d := 20.0 + shift  # empieza fuera de la insignia
				while d < length - 20.0:
					var p := (a_pos + dir * d).round()
					draw_rect(Rect2(p - Vector2.ONE, Vector2(2, 2)) if not reachable else Rect2(p - Vector2(1, 1), Vector2(3, 3)), col)
					d += step
				var cost: int = a["costs"][to]
				if cost > 1:
					var mid := ((a_pos + b_pos) * 0.5).round()
					draw_rect(Rect2(mid - Vector2(10, 10), Vector2(20, 20)), Color("060810"))
					draw_rect(Rect2(mid - Vector2(9, 9), Vector2(18, 18)), Color("141b33"))
					draw_rect(Rect2(mid - Vector2(9, 9), Vector2(18, 1)), col)
					draw_rect(Rect2(mid - Vector2(9, -8), Vector2(18, 1)), col)
					draw_string(UITheme.font(), mid + Vector2(-4, 5), str(cost), HORIZONTAL_ALIGNMENT_CENTER, 8, 16, col)


class _Stars extends Control:
	var _pts: Array = []

	func _init() -> void:
		var rng := RandomNumberGenerator.new()
		rng.seed = 77
		for i in 70:
			_pts.append([rng.randf() * 640.0, rng.randf() * 360.0, rng.randi_range(1, 3), rng.randf() * 6.28])

	func _process(_d: float) -> void:
		queue_redraw()

	func _draw() -> void:
		var t := Time.get_ticks_msec() / 1000.0
		for p in _pts:
			var layer: int = p[2]
			var x := fposmod(p[0] - t * 2.5 * layer, 640.0)
			var a := 0.3 + 0.25 * layer / 3.0 + 0.2 * sin(t * 1.5 + p[3])
			draw_rect(Rect2(floorf(x), floorf(p[1]), 1 if layer < 3 else 2, 1 if layer < 3 else 2), Color(0.85, 0.92, 1.0, a))


func node_pos(id: String) -> Vector2:
	var n: Dictionary = campaign.sector.nodes[id]
	var cols: int = campaign.sector.columns.size()
	return Vector2(lerpf(MAP_X0, MAP_X1, float(n["col"]) / (cols - 1)), MAP_Y0 + float(n["y"]) * MAP_H).round()


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(UITheme.background("bg_space", 0.2))
	var stars := _Stars.new()
	stars.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	stars.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(stars)

	# Marco del mapa
	var frame := UITheme.framed("panel_dark", Vector2i(0, 0), false)
	frame.position = Vector2(8, 44)
	frame.custom_minimum_size = Vector2(624, 238)
	frame.size = Vector2(624, 238)
	frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(frame)

	_lines = _Lines.new()
	_lines.screen = self
	_lines.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	_lines.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_lines)

	for id in campaign.sector.nodes:
		var b := Button.new()
		b.custom_minimum_size = NODE_SIZE
		b.size = NODE_SIZE
		b.position = node_pos(id) - NODE_SIZE / 2.0
		b.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
		b.vertical_icon_alignment = VERTICAL_ALIGNMENT_CENTER
		b.expand_icon = false
		b.focus_mode = Control.FOCUS_ALL
		b.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		b.pressed.connect(_select.bind(id))
		b.focus_entered.connect(_select.bind(id))
		add_child(b)
		_buttons[id] = b

	_ship = TextureRect.new()
	_ship.texture = UITheme.tex_icon("sector_ship")
	_ship.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_ship.size = Vector2(16, 16)
	add_child(_ship)

	_build_hud()
	_build_info()
	GameState.changed.connect(_refresh)
	_select(campaign.current)
	_refresh()
	_fuel_bar.snap()
	_morale_bar.snap()
	# Foco inicial en un nodo alcanzable para poder jugar solo con teclado.
	for to in campaign.sector.nodes[campaign.current]["edges"]:
		if campaign.can_jump(to):
			_buttons[to].grab_focus()
			break


func _process(delta: float) -> void:
	_time += delta
	var base := node_pos(campaign.current) + Vector2(-8, -38)
	_ship.position = base + Vector2(0, roundf(sin(_time * 2.2) * 2.0))


func _build_hud() -> void:
	var bar := UITheme.framed("panel_dark", Vector2i(10, 4))
	bar.position = Vector2(8, 6)
	bar.custom_minimum_size = Vector2(624, 34)
	bar.size = Vector2(624, 34)
	add_child(bar)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 22)
	bar.add_child(row)

	_fuel_chip = UITheme.chip("fuel", UITheme.WARN)
	_fuel_bar = PixelBar.new(Color("e8b45c"), 14)
	_fuel_bar.custom_minimum_size = Vector2(84, 14)
	_fuel_bar.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_fuel_chip.add_child(_fuel_bar)
	row.add_child(_fuel_chip)
	_scan_chip = UITheme.chip("scan", UITheme.ACCENT)
	row.add_child(_scan_chip)
	_data_chip = UITheme.chip("data", UITheme.ACCENT_L)
	row.add_child(_data_chip)
	_morale_chip = UITheme.chip("morale", Color("ff9a94"))
	_morale_bar = PixelBar.new(Color("e0605c"), 14)
	_morale_bar.custom_minimum_size = Vector2(84, 14)
	_morale_bar.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_morale_chip.add_child(_morale_bar)
	row.add_child(_morale_chip)


func _build_info() -> void:
	var panel := UITheme.framed("panel", Vector2i(12, 8))
	panel.position = Vector2(8, 288)
	panel.custom_minimum_size = Vector2(624, 66)
	panel.size = Vector2(624, 66)
	add_child(panel)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 12)
	panel.add_child(row)
	var col := VBoxContainer.new()
	col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	col.add_theme_constant_override("separation", 0)
	row.add_child(col)
	_info_title = UITheme.label("", UITheme.ACCENT, UITheme.SIZE_HEAD)
	col.add_child(_info_title)
	_info_body = UITheme.label("", UITheme.DIM)
	col.add_child(_info_body)
	var btns := VBoxContainer.new()
	btns.add_theme_constant_override("separation", 4)
	row.add_child(btns)
	_jump_btn = UITheme.button("", false)
	_jump_btn.alignment = HORIZONTAL_ALIGNMENT_CENTER
	_jump_btn.custom_minimum_size = Vector2(190, 0)
	_jump_btn.pressed.connect(_on_jump)
	btns.add_child(_jump_btn)
	_scan_btn = UITheme.button("", false)
	_scan_btn.alignment = HORIZONTAL_ALIGNMENT_CENTER
	_scan_btn.custom_minimum_size = Vector2(190, 0)
	_scan_btn.pressed.connect(_on_scan)
	btns.add_child(_scan_btn)


func _set_chip(chip: HBoxContainer, text: String) -> void:
	(chip.get_meta("label") as Label).text = text


func _refresh() -> void:
	_set_chip(_fuel_chip, "%d/%d" % [GameState.fuel, GameState.max_fuel])
	_fuel_bar.max_value = GameState.max_fuel
	_fuel_bar.seg_units = 1.0
	_fuel_bar.value = GameState.fuel
	_set_chip(_scan_chip, str(GameState.scans))
	_set_chip(_data_chip, str(GameState.data))
	_set_chip(_morale_chip, "%d/%d" % [GameState.morale, GameState.max_morale])
	_morale_bar.max_value = GameState.max_morale
	_morale_bar.value = GameState.morale
	for id in _buttons:
		_style_node(id)
	_update_info()


func _icon_for(id: String) -> String:
	var n: Dictionary = campaign.node(id)
	if n["type"] == "start":
		return "node_start"
	if n["final"]:
		return "node_final"
	if not n["scanned"]:
		return "node_unknown"
	if n["type"] == "planet":
		return "node_planet_" + n["planet"]["biome"]  # el color anticipa el bioma
	return "node_" + n["type"]


func _badge_for(id: String) -> String:
	var n: Dictionary = campaign.node(id)
	if id == _selected:
		return "selected"
	if id == campaign.current:
		return "current"
	if campaign.node(campaign.current)["edges"].has(id) and not n["done"]:
		return "reach"
	if n["done"]:
		return "done"
	return "idle"


func _style_node(id: String) -> void:
	var b: Button = _buttons[id]
	var n: Dictionary = campaign.node(id)
	b.icon = UITheme.tex_icon(_icon_for(id))
	var badge := _badge_for(id)
	for state in ["normal", "hover", "pressed", "focus", "disabled"]:
		var sb := UITheme.tex_box("badge_" + (("selected" if state == "hover" else badge)), 0, Vector2i(0, 0))
		sb.axis_stretch_horizontal = StyleBoxTexture.AXIS_STRETCH_MODE_STRETCH
		sb.axis_stretch_vertical = StyleBoxTexture.AXIS_STRETCH_MODE_STRETCH
		b.add_theme_stylebox_override(state, sb)
	b.self_modulate = Color(1, 1, 1, 0.5 if n["done"] and id != campaign.current else 1.0)


func _select(id: String) -> void:
	_selected = id
	for other in _buttons:
		_style_node(other)
	_update_info()


func _update_info() -> void:
	if _selected == "":
		_info_title.text = T.t("ui.sector.select")
		return
	var n: Dictionary = campaign.node(_selected)
	var here := _selected == campaign.current
	_info_title.text = _title_for(n)
	var body := ""
	if here:
		body = T.t("ui.sector.here")
	elif n["done"]:
		body = T.t("ui.sector.visited")
	elif not campaign.node(campaign.current)["edges"].has(_selected):
		body = T.t("ui.sector.unreachable")
	elif GameState.fuel < campaign.edge_cost(campaign.current, _selected):
		body = T.t("ui.sector.no_fuel")
	if not n["scanned"]:
		body = (body + "  " if body != "" else "") + T.t("ui.sector.unknown_body")
	elif n["type"] == "planet":
		var tags: Array[String] = []
		for tag in campaign.sector.scan_tags(_selected):
			tags.append(T.t("ui.scan.tag." + tag))
		if not tags.is_empty():
			body = (body + "  " if body != "" else "") + T.t("ui.sector.tags", {"list": ", ".join(tags)})
	_info_body.text = body
	var cost := campaign.edge_cost(campaign.current, _selected) if campaign.node(campaign.current)["edges"].has(_selected) else 1
	_jump_btn.text = T.t("ui.sector.jump", {"n": cost})
	_jump_btn.disabled = not campaign.can_jump(_selected)
	_scan_btn.text = T.t("ui.sector.scan", {"n": GameState.scans})
	_scan_btn.disabled = not campaign.can_scan(_selected)


func _title_for(n: Dictionary) -> String:
	if n["type"] == "start":
		return T.t("ui.sector.type.start")
	if not n["scanned"]:
		return T.t("ui.sector.unknown_title")
	match n["type"]:
		"planet":
			var name := T.t("planet.%s.name" % n["ref"])
			return T.t("ui.sector.type.final" if n["final"] else "ui.sector.type.planet", {"name": name})
		"contact":
			return T.t("ui.sector.type.contact", {"species": T.t("species.%s.name" % n["ref"])})
	return T.t("ui.sector.type.anomaly")


func _on_jump() -> void:
	if campaign.can_jump(_selected):
		var id := _selected
		Sfx.play("jump")
		campaign.jump(id)
		jumped.emit(id)


func _on_scan() -> void:
	if campaign.can_scan(_selected):
		Sfx.play("scan")
		campaign.scan(_selected)
		_refresh()
