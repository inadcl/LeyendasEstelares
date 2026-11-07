class_name AvatarScreen
extends Control

signal avatar_chosen(avatar_id: String)


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(UITheme.background("bg_space", 0.25))
	var vs := get_viewport_rect().size
	var portrait := Layout.portrait
	var head := UITheme.logo(T.t("ui.choose_traveler"), UITheme.ACCENT_L, UITheme.SIZE_BIG if not portrait else UITheme.SIZE_HEAD + 4)
	head.position = Vector2(0, 8 + Layout.safe_top)
	head.size = Vector2(vs.x, 36)
	add_child(head)

	# Las tarjetas van una junto a otra (apaisado) o apiladas con desplazamiento (vertical).
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.position = Vector2(0, 52 + Layout.safe_top)
	scroll.size = Vector2(vs.x, vs.y - 52 - Layout.safe_top)
	add_child(scroll)
	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 12 if portrait else 14)
	margin.add_theme_constant_override("margin_right", 12 if portrait else 14)
	margin.add_theme_constant_override("margin_bottom", 12)
	scroll.add_child(margin)
	var row := BoxContainer.new()
	row.vertical = portrait
	row.add_theme_constant_override("separation", 14)
	margin.add_child(row)
	var card_w := (vs.x - 24.0) if portrait else 300.0
	for a in Content.avatars:
		row.add_child(_card(a, card_w))
	var first := row.find_children("*", "Button", true, false)
	if not first.is_empty():
		(first[0] as Button).grab_focus()


func _card(a: Dictionary, card_w: float) -> Control:
	var id: String = a["id"]
	var panel := UITheme.framed("panel", Vector2i(12, 10))
	panel.custom_minimum_size = Vector2(card_w, 0)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 8)
	panel.add_child(v)

	var top := HBoxContainer.new()
	top.add_theme_constant_override("separation", 12)
	v.add_child(top)
	var bezel := PanelContainer.new()
	bezel.add_theme_stylebox_override("panel", UITheme.tex_box("bezel", 10, Vector2i(10, 10)))
	var portrait := TextureRect.new()
	portrait.texture = Art.tex(a["sprite"])
	portrait.custom_minimum_size = Vector2(80, 80)
	portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	bezel.add_child(portrait)
	top.add_child(bezel)
	var names := VBoxContainer.new()
	names.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	names.add_theme_constant_override("separation", 2)
	top.add_child(names)
	names.add_child(UITheme.label(T.t("avatar.%s.name" % id), UITheme.TEXT, UITheme.SIZE_HEAD))
	names.add_child(UITheme.label(T.t("avatar.%s.role" % id), UITheme.ACCENT))
	names.add_child(UITheme.label(T.t("avatar.%s.perk" % id), UITheme.GOOD))

	var desc := UITheme.label(T.t("avatar.%s.desc" % id), UITheme.DIM)
	desc.custom_minimum_size = Vector2(card_w - 24.0, 0)
	v.add_child(desc)

	var stats := HBoxContainer.new()
	stats.add_theme_constant_override("separation", 18)
	v.add_child(stats)
	var o2 := UITheme.chip("oxygen", UITheme.TEXT)
	(o2.get_meta("label") as Label).text = str(a["max_oxygen"])
	stats.add_child(o2)
	var mo := UITheme.chip("morale", UITheme.TEXT)
	(mo.get_meta("label") as Label).text = str(a["max_morale"])
	stats.add_child(mo)

	var pick := UITheme.button(T.t("ui.choose"))
	pick.alignment = HORIZONTAL_ALIGNMENT_CENTER
	pick.pressed.connect(func(): avatar_chosen.emit(id))
	v.add_child(pick)
	return panel
