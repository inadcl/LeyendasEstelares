class_name EndScreen
extends Control
## Cierre de la campaña. `ending`: victory | abort | fuel | oxygen | morale.

signal continue_pressed

var ending := "victory"
var jumps := 0

var _scroll: ScrollContainer
var _content: VBoxContainer


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(UITheme.background("bg_title" if ending == "victory" else "bg_space", 0.0 if ending == "victory" else 0.2))
	Sfx.play("victory" if ending == "victory" else "defeat")
	var vs := get_viewport_rect().size
	var w := minf(520.0, vs.x - 24.0)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(center)
	var good := ending == "victory"
	var panel := UITheme.framed("panel_accent" if good else ("panel_amber" if ending == "abort" else "panel"), Vector2i(16, 12))
	center.add_child(panel)
	var outer := VBoxContainer.new()
	outer.add_theme_constant_override("separation", 8)
	panel.add_child(outer)

	var color := UITheme.GOOD if good else (UITheme.WARN if ending == "abort" else UITheme.BAD)
	var title := UITheme.label(T.t("ending.%s.title" % ending), color, UITheme.SIZE_BIG if not Layout.portrait else UITheme.SIZE_HEAD + 4, true)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	outer.add_child(title)
	outer.add_child(HSeparator.new())

	# El cuerpo se desplaza si no cabe (muchos epílogos o pantalla baja); el botón queda siempre visible.
	_scroll = ScrollContainer.new()
	_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	outer.add_child(_scroll)
	_content = VBoxContainer.new()
	_content.custom_minimum_size = Vector2(w - 32.0, 0)
	_content.add_theme_constant_override("separation", 8)
	_scroll.add_child(_content)
	_scroll.custom_minimum_size = Vector2(w - 32.0, 0)
	_content.add_child(UITheme.label(T.t("ending.%s.body" % ending), UITheme.TEXT))
	var notes := false
	for p in Content.planets:
		for flag in p.get("epilogues", []):
			if GameState.has_flag(flag):
				if not notes:
					_content.add_child(HSeparator.new())
					notes = true
				_content.add_child(UITheme.label("◆ " + T.t("planet.%s.epilogue.%s" % [p["id"], flag]), UITheme.DIM))
	_content.add_child(HSeparator.new())
	var stats := HFlowContainer.new()
	stats.add_theme_constant_override("h_separation", 20)
	stats.alignment = FlowContainer.ALIGNMENT_CENTER
	_content.add_child(stats)
	for pair in [["data", str(GameState.data)], ["fuel", "%d/%d" % [GameState.fuel, GameState.max_fuel]], ["morale", "%d/%d" % [GameState.morale, GameState.max_morale]]]:
		var chip := UITheme.chip(pair[0])
		(chip.get_meta("label") as Label).text = pair[1]
		stats.add_child(chip)
	_content.add_child(UITheme.label(T.t("ending.jumps", {"jumps": jumps}), UITheme.DIM))
	var reps: Array[String] = []
	for faction in GameState.rep:
		var n: int = GameState.rep[faction]
		reps.append("%s %s%d" % [T.t("faction." + faction), "+" if n > 0 else "", n])
	if not reps.is_empty():
		_content.add_child(UITheme.label(T.t("ui.hud.rep", {"list": ", ".join(reps)}), UITheme.DIM))

	var btn := UITheme.button(T.t("ui.back_title"))
	btn.alignment = HORIZONTAL_ALIGNMENT_CENTER
	btn.pressed.connect(func(): continue_pressed.emit())
	outer.add_child(btn)
	btn.grab_focus()
	_content.minimum_size_changed.connect(func(): UITheme.fit_scroll(_scroll, _content, vs.y - 24.0 - 120.0))
	(func(): UITheme.fit_scroll(_scroll, _content, vs.y - 24.0 - 120.0)).call_deferred()
