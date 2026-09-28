class_name PlanetMapView
extends Node2D
## Dibuja el mapa hexagonal de una Expedition y emite los clics sobre casillas.

signal cell_clicked(cell: Vector2i)

var expedition: Expedition
var enabled := true
var _hover := Vector2i(-1, -1)

const _HEX_OFFSET := Vector2(HexGrid.W / 2.0, HexGrid.H / 2.0)


func size_px() -> Vector2:
	return Vector2(PlanetData.COLS * HexGrid.W + HexGrid.W / 2.0, (PlanetData.ROWS - 1) * HexGrid.ROW_H + HexGrid.H)


func cell_at(local: Vector2) -> Vector2i:
	var best := Vector2i(-1, -1)
	var best_d := 19.0
	for c in expedition.map.terrain:
		var d := local.distance_to(HexGrid.center(c))
		if d < best_d:
			best_d = d
			best = c
	return best


func _process(_delta: float) -> void:
	var c := cell_at(get_local_mouse_position()) if enabled else Vector2i(-1, -1)
	if c != _hover:
		_hover = c
		queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	if not enabled or expedition == null:
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var c := cell_at(get_local_mouse_position())
		if c != Vector2i(-1, -1):
			cell_clicked.emit(c)


func _draw() -> void:
	if expedition == null:
		return
	var map := expedition.map
	for c in map.terrain:
		var tile: String = "tile_fog" if not map.revealed.has(c) else "tile_" + map.terrain[c]
		draw_texture(Art.tex(tile), HexGrid.center(c) - _HEX_OFFSET)

	for p in map.pois:
		if map.revealed.has(p["cell"]):
			var tint := Color(1, 1, 1, 0.35) if p["resolved"] else Color.WHITE
			draw_texture(Art.tex("poi_" + p["type"]), HexGrid.center(p["cell"]) - Vector2(8, 12), tint)
	draw_texture(Art.tex("ship"), HexGrid.center(map.ship_cell) - Vector2(8, 12))

	var font := ThemeDB.fallback_font
	for n in HexGrid.neighbors(expedition.player):
		if expedition.can_move(n):
			var pos := HexGrid.center(n)
			draw_texture(Art.tex("hl_reach"), pos - _HEX_OFFSET)
			if not map.poi_at(n).is_empty() and map.revealed.has(n):
				continue
			draw_string_outline(font, pos + Vector2(-8, 22), str(map.move_cost(n)), HORIZONTAL_ALIGNMENT_CENTER, 16, 10, 3, Color.BLACK)
			draw_string(font, pos + Vector2(-8, 22), str(map.move_cost(n)), HORIZONTAL_ALIGNMENT_CENTER, 16, 10, UITheme.WARN)
	if enabled and _hover != Vector2i(-1, -1):
		draw_texture(Art.tex("hl_hover"), HexGrid.center(_hover) - _HEX_OFFSET)

	var avatar_tex := Art.tex(GameState.avatar.get("sprite", "avatar_vance"))
	draw_texture(avatar_tex, HexGrid.center(expedition.player) - Vector2(8, 13))
