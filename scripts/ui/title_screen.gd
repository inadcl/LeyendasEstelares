class_name TitleScreen
extends Control
## Portada: ilustración pixel art, logo y menú.

signal start_pressed
signal quit_pressed
signal language_changed
signal help_pressed

var _ship: TextureRect
var _time := 0.0


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(UITheme.background("bg_title"))

	_ship = TextureRect.new()
	_ship.texture = UITheme.tex("title_ship")
	_ship.position = Vector2(262, 196)
	_ship.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_ship)

	var logo := UITheme.logo(T.t("ui.title"), UITheme.ACCENT_L, 50)
	logo.position = Vector2(0, 8)
	logo.size = Vector2(640, 56)
	add_child(logo)
	var sub := UITheme.label(T.t("ui.subtitle"), Color("c8b8f0"), UITheme.SIZE_HEAD, true)
	sub.autowrap_mode = TextServer.AUTOWRAP_OFF
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub.position = Vector2(0, 62)
	sub.size = Vector2(640, 24)
	add_child(sub)

	var menu := UITheme.framed("panel", Vector2i(12, 10))
	menu.position = Vector2(22, 128)
	add_child(menu)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	box.custom_minimum_size = Vector2(196, 0)
	menu.add_child(box)

	var start := UITheme.button(T.t("ui.new_expedition"))
	start.alignment = HORIZONTAL_ALIGNMENT_CENTER
	start.pressed.connect(func(): start_pressed.emit())
	box.add_child(start)
	var help := UITheme.button(T.t("ui.how_to_play"))
	help.alignment = HORIZONTAL_ALIGNMENT_CENTER
	help.pressed.connect(func(): help_pressed.emit())
	box.add_child(help)
	var sound := UITheme.button(T.t("ui.sound_off" if Sfx.muted else "ui.sound_on"))
	sound.alignment = HORIZONTAL_ALIGNMENT_CENTER
	sound.pressed.connect(func():
		Sfx.toggle_mute()
		language_changed.emit())  # reconstruye el título con el texto actualizado
	box.add_child(sound)
	if not OS.has_feature("web"):
		var quit := UITheme.button(T.t("ui.quit"))
		quit.alignment = HORIZONTAL_ALIGNMENT_CENTER
		quit.pressed.connect(func(): quit_pressed.emit())
		box.add_child(quit)
	box.add_child(HSeparator.new())
	# Selector de idioma: un botón por idioma disponible.
	var langs := HBoxContainer.new()
	langs.alignment = BoxContainer.ALIGNMENT_CENTER
	langs.add_theme_constant_override("separation", 4)
	for code in T.LANGUAGES:
		var b := UITheme.button(T.LANGUAGES[code], false)
		b.alignment = HORIZONTAL_ALIGNMENT_CENTER
		b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		b.disabled = code == T.language()
		b.pressed.connect(func():
			T.set_language(code)
			language_changed.emit())
		langs.add_child(b)
	box.add_child(langs)
	start.grab_focus()


func _process(delta: float) -> void:
	_time += delta
	_ship.position = Vector2(262 + roundf(sin(_time * 0.7) * 6.0), 196 + roundf(sin(_time * 1.3) * 3.0))
