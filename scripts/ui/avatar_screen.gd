class_name AvatarScreen
extends Control

signal avatar_chosen(avatar_id: String)


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(UITheme.background())
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(center)
	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 12)
	center.add_child(col)
	var head := UITheme.label(T.t("ui.choose_traveler"), UITheme.ACCENT, 20)
	head.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	col.add_child(head)

	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 12)
	col.add_child(row)
	for a in Content.avatars:
		row.add_child(_card(a))


func _card(a: Dictionary) -> Control:
	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(260, 0)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 6)
	panel.add_child(v)

	var portrait := TextureRect.new()
	portrait.texture = Art.tex(a["sprite"])
	portrait.custom_minimum_size = Vector2(80, 80)
	portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	v.add_child(portrait)
	var id: String = a["id"]
	v.add_child(UITheme.label(T.t("avatar.%s.name" % id), UITheme.TEXT, 14))
	v.add_child(UITheme.label(T.t("avatar.%s.role" % id), UITheme.ACCENT, 11))
	var desc := UITheme.label(T.t("avatar.%s.desc" % id), UITheme.DIM, 11)
	desc.custom_minimum_size = Vector2(240, 60)
	v.add_child(desc)
	v.add_child(UITheme.label(T.t("ui.avatar_stats", {"oxygen": a["max_oxygen"], "morale": a["max_morale"]}), UITheme.TEXT, 11))
	v.add_child(UITheme.label(T.t("avatar.%s.perk" % id), UITheme.GOOD, 11))
	var pick := UITheme.button(T.t("ui.choose"))
	pick.alignment = HORIZONTAL_ALIGNMENT_CENTER
	pick.pressed.connect(func(): avatar_chosen.emit(a["id"]))
	v.add_child(pick)
	return panel
