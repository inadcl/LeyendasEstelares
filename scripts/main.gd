extends Control
## Raíz del juego: gestiona el flujo título → avatar → exploración → resumen.

var _current: Control


func _ready() -> void:
	theme = UITheme.build()
	_show_title()


func _swap(screen: Control) -> void:
	if _current != null:
		_current.queue_free()
	_current = screen
	add_child(screen)


func _show_title() -> void:
	var s := TitleScreen.new()
	s.start_pressed.connect(_show_avatars)
	s.quit_pressed.connect(func(): get_tree().quit())
	_swap(s)


func _show_avatars() -> void:
	var s := AvatarScreen.new()
	s.avatar_chosen.connect(func(id: String):
		GameState.start_run(Content.avatar_by_id(id), Content.factions)
		_start_planet())
	_swap(s)


func _start_planet() -> void:
	GameState.begin_planet()
	var planet: Dictionary = Content.planets[GameState.planet_index]
	var s := MapScreen.new()
	s.planet = planet
	s.finished.connect(func(outcome: Dictionary): _show_summary(planet, outcome))
	_swap(s)


func _show_summary(planet: Dictionary, outcome: Dictionary) -> void:
	var s := SummaryScreen.new()
	s.planet = planet
	s.outcome = outcome
	s.continue_pressed.connect(_show_title)
	_swap(s)
