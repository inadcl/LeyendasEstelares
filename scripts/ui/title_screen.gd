class_name TitleScreen
extends Control

signal start_pressed
signal quit_pressed
signal language_changed
signal help_pressed


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(UITheme.background())
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(center)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	box.custom_minimum_size = Vector2(300, 0)
	center.add_child(box)

	var title := UITheme.label(T.t("ui.title"), UITheme.ACCENT, 28)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(title)
	var sub := UITheme.label(T.t("ui.subtitle"), UITheme.DIM, 12)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(sub)
	box.add_child(Control.new())

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

	# Selector de idioma: un botón por idioma disponible.
	var langs := HBoxContainer.new()
	langs.alignment = BoxContainer.ALIGNMENT_CENTER
	langs.add_theme_constant_override("separation", 6)
	var lang_label := UITheme.label(T.t("ui.language") + ":", UITheme.DIM, 11)
	lang_label.autowrap_mode = TextServer.AUTOWRAP_OFF
	langs.add_child(lang_label)
	for code in T.LANGUAGES:
		var b := UITheme.button(T.LANGUAGES[code], false)
		b.disabled = code == T.language()
		b.pressed.connect(func():
			T.set_language(code)
			language_changed.emit())
		langs.add_child(b)
	box.add_child(langs)
	start.grab_focus()
