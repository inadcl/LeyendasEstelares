class_name PixelBar
extends Control
## Barra segmentada pixel art con brillo superior y animación suave del valor.

var color := Color("5cc8e8")
var max_value := 10.0
var seg_units := 1.0  # unidades que representa cada segmento
var value := 0.0:
	set(v):
		value = v
		set_process(true)
var _shown := -1.0


func _init(bar_color := Color("5cc8e8"), height := 14) -> void:
	color = bar_color
	custom_minimum_size = Vector2(0, height)
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func snap() -> void:
	_shown = value
	queue_redraw()


func _process(delta: float) -> void:
	if _shown < 0.0:
		_shown = value
	_shown = move_toward(_shown, value, maxf(max_value * 1.2 * delta, 0.01))
	queue_redraw()
	if is_equal_approx(_shown, value):
		set_process(false)


func _draw() -> void:
	var w := int(size.x)
	var h := int(size.y)
	draw_rect(Rect2(0, 0, w, h), Color("060810"))
	draw_rect(Rect2(1, 1, w - 2, h - 2), Color("0b1020"))
	draw_rect(Rect2(1, 1, w - 2, 1), Color("1c2748"))
	var inner_w := w - 4
	var frac := clampf((_shown if _shown >= 0.0 else value) / maxf(max_value, 0.001), 0.0, 1.0)
	var fill_w := int(roundf(inner_w * frac))
	if fill_w > 0:
		draw_rect(Rect2(2, 2, fill_w, h - 4), color)
		draw_rect(Rect2(2, 2, fill_w, 2), color.lightened(0.4))
		draw_rect(Rect2(2, h - 4, fill_w, 2), color.darkened(0.4))
	# separadores de segmento
	var segs := int(ceil(max_value / seg_units))
	for i in range(1, segs):
		var x := 2 + int(roundf(inner_w * float(i) / segs))
		draw_rect(Rect2(x, 2, 1, h - 4), Color(0.02, 0.03, 0.08, 0.8))
