extends Node
## Captura pantallas del juego real (requiere display, p. ej. xvfb-run).
## xvfb-run -a godot --path . res://tests/screenshot.tscn -- <directorio_salida>

var _out := "/tmp"


func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	if not args.is_empty():
		_out = args[0]
	var main: Control = load("res://scenes/main.tscn").instantiate()
	add_child(main)
	await _shot("1_title")
	main._show_avatars()
	await _shot("2_avatars")
	GameState.start_run(Content.avatar_by_id("vance"), Content.factions)
	main._start_planet()
	await _shot("3_briefing")
	var screen: MapScreen = main._current
	screen._close_overlay()
	# Avanza por la mejor ruta hacia el primer punto de interés para ver niebla y eventos.
	var ex := screen.expedition
	var target: Dictionary = ex.map.pois[0]
	var steps := ex.map.find_path(ex.player, target["cell"])
	for i in steps.size():
		var res := ex.move(steps[i])
		screen._refresh_hud()
		if not res["poi"].is_empty():
			break
	await _shot("4_map")
	screen._open_event(ex.map.poi_at(ex.player))
	await _shot("5_event")
	get_tree().quit()


func _shot(name: String) -> void:
	await get_tree().process_frame
	await get_tree().process_frame
	await get_tree().process_frame
	get_viewport().get_texture().get_image().save_png("%s/%s.png" % [_out, name])
