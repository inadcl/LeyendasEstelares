class_name AnomalyScreen
extends Control
## Anomalía espacial: un evento breve resuelto desde la nave, sin mapa de superficie.

signal finished

var event_id := ""

var _overlay: Overlay
var _rng := RandomNumberGenerator.new()


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_rng.randomize()
	add_child(UITheme.background())
	_overlay = Overlay.new()
	add_child(_overlay)
	_overlay.present_event(
		event_id,
		func(i: int): return EventRunner.resolve(event_id, i, Content.events[event_id]["choices"][i], GameState, _rng),
		func(): finished.emit())
