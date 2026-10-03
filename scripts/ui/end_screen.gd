class_name EndScreen
extends Control
## Cierre de la campaña. `ending`: victory | abort | fuel | oxygen | morale.

signal continue_pressed

var ending := "victory"
var jumps := 0


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(UITheme.background("bg_title" if ending == "victory" else "bg_space", 0.0 if ending == "victory" else 0.2))
	Sfx.play("victory" if ending == "victory" else "defeat")
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(center)
	var good := ending == "victory"
	var panel := UITheme.framed("panel_accent" if good else ("panel_amber" if ending == "abort" else "panel"), Vector2i(16, 12))
	panel.custom_minimum_size = Vector2(520, 0)
	center.add_child(panel)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 8)
	panel.add_child(v)

	var color := UITheme.GOOD if good else (UITheme.WARN if ending == "abort" else UITheme.BAD)
	var title := UITheme.label(T.t("ending.%s.title" % ending), color, UITheme.SIZE_BIG, true)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	v.add_child(title)
	v.add_child(HSeparator.new())
	v.add_child(UITheme.label(T.t("ending.%s.body" % ending), UITheme.TEXT))
	var notes := false
	for p in Content.planets:
		for flag in p.get("epilogues", []):
			if GameState.has_flag(flag):
				if not notes:
					v.add_child(HSeparator.new())
					notes = true
				v.add_child(UITheme.label("◆ " + T.t("planet.%s.epilogue.%s" % [p["id"], flag]), UITheme.DIM))
	v.add_child(HSeparator.new())
	var stats := HBoxContainer.new()
	stats.add_theme_constant_override("separation", 20)
	stats.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(stats)
	for pair in [["data", str(GameState.data)], ["fuel", "%d/%d" % [GameState.fuel, GameState.max_fuel]], ["morale", "%d/%d" % [GameState.morale, GameState.max_morale]]]:
		var chip := UITheme.chip(pair[0])
		(chip.get_meta("label") as Label).text = pair[1]
		stats.add_child(chip)
	v.add_child(UITheme.label(T.t("ending.jumps", {"jumps": jumps}), UITheme.DIM))
	for faction in GameState.rep:
		var n: int = GameState.rep[faction]
		v.add_child(UITheme.label(T.t("ending.rep", {"faction": T.t("faction." + faction), "value": ("+" if n > 0 else "") + str(n)}), UITheme.DIM))
	var btn := UITheme.button(T.t("ui.back_title"))
	btn.alignment = HORIZONTAL_ALIGNMENT_CENTER
	btn.pressed.connect(func(): continue_pressed.emit())
	v.add_child(btn)
	btn.grab_focus()
