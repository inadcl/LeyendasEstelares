class_name TitleScreen
extends Control

signal start_pressed
signal quit_pressed


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(UITheme.background())
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(center)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 10)
	box.custom_minimum_size = Vector2(300, 0)
	center.add_child(box)

	var title := UITheme.label("LEYENDAS ESTELARES", UITheme.ACCENT, 28)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(title)
	var sub := UITheme.label("Exploración, criterio y consecuencias", UITheme.DIM, 12)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(sub)
	box.add_child(Control.new())

	var start := UITheme.button("Nueva expedición")
	start.alignment = HORIZONTAL_ALIGNMENT_CENTER
	start.pressed.connect(func(): start_pressed.emit())
	box.add_child(start)
	if not OS.has_feature("web"):
		var quit := UITheme.button("Salir")
		quit.alignment = HORIZONTAL_ALIGNMENT_CENTER
		quit.pressed.connect(func(): quit_pressed.emit())
		box.add_child(quit)
	start.grab_focus()
