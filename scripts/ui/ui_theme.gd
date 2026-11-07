class_name UITheme
extends RefCounted
## Tema pixel art: fuente Jersey 10, marcos 9-slice y botones de res://ui (generados por tools/gen_ui.py).

const TEXT := Color("dfe8ff")
const DIM := Color("8393b8")
const ACCENT := Color("5cc8e8")
const ACCENT_L := Color("a8ecff")
const WARN := Color("e8b45c")
const BAD := Color("e0605c")
const GOOD := Color("74d68b")
const PURPLE := Color("a07ae0")
const BLACK := Color("060810")
const NAVY := Color("0b1020")
const MID := Color("2e3f73")

const SIZE_BODY := 16
const SIZE_HEAD := 20
const SIZE_BIG := 32

static var _font: FontFile


static func font() -> FontFile:
	if _font == null:
		_font = load("res://fonts/Jersey10-Regular.ttf")
		_font.antialiasing = TextServer.FONT_ANTIALIASING_NONE
		_font.hinting = TextServer.HINTING_NONE
		_font.subpixel_positioning = TextServer.SUBPIXEL_POSITIONING_DISABLED
	return _font


static func tex(name: String) -> Texture2D:
	return load("res://ui/%s.png" % name)


## Textura de res://art (sprites del juego).
static func tex_icon(name: String) -> Texture2D:
	return load("res://art/%s.png" % name)


## Estilo 9-slice con textura de res://ui. `margin` = borde fijo del 9-slice (px del PNG).
static func tex_box(name: String, margin := 6, pad := Vector2i(8, 5), draw_center := true) -> StyleBoxTexture:
	var sb := StyleBoxTexture.new()
	sb.texture = tex(name)
	sb.set_texture_margin_all(margin)
	sb.content_margin_left = pad.x
	sb.content_margin_right = pad.x
	sb.content_margin_top = pad.y
	sb.content_margin_bottom = pad.y
	sb.draw_center = draw_center
	sb.axis_stretch_horizontal = StyleBoxTexture.AXIS_STRETCH_MODE_TILE
	sb.axis_stretch_vertical = StyleBoxTexture.AXIS_STRETCH_MODE_TILE
	return sb


static func build() -> Theme:
	var t := Theme.new()
	t.default_font = font()
	t.default_font_size = SIZE_BODY
	t.set_color("font_color", "Label", TEXT)
	t.set_color("default_color", "RichTextLabel", TEXT)
	t.set_font("normal_font", "RichTextLabel", font())
	t.set_font_size("normal_font_size", "RichTextLabel", SIZE_BODY)
	t.set_stylebox("panel", "PanelContainer", tex_box("panel", 6, Vector2i(10, 8)))
	var pad := Vector2i(10, 4)
	t.set_stylebox("normal", "Button", tex_box("btn_normal", 6, pad))
	t.set_stylebox("hover", "Button", tex_box("btn_hover", 6, pad))
	t.set_stylebox("pressed", "Button", tex_box("btn_pressed", 6, Vector2i(10, 5)))
	t.set_stylebox("disabled", "Button", tex_box("btn_disabled", 6, pad))
	t.set_stylebox("focus", "Button", tex_box("btn_focus", 6, pad, false))
	t.set_color("font_color", "Button", TEXT)
	t.set_color("font_hover_color", "Button", Color.WHITE)
	t.set_color("font_pressed_color", "Button", WARN)
	t.set_color("font_focus_color", "Button", Color.WHITE)
	t.set_color("font_disabled_color", "Button", Color("4a5678"))
	t.set_constant("h_separation", "Button", 6)
	var sep := StyleBoxTexture.new()
	sep.texture = tex("separator")
	sep.axis_stretch_horizontal = StyleBoxTexture.AXIS_STRETCH_MODE_TILE
	t.set_stylebox("separator", "HSeparator", sep)
	t.set_constant("separation", "HSeparator", 6)
	return t


static func label(text: String, color := TEXT, size := SIZE_BODY, shadow := false) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_color_override("font_color", color)
	l.add_theme_font_size_override("font_size", size)
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	if shadow:
		l.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.85))
		l.add_theme_constant_override("shadow_offset_x", 2)
		l.add_theme_constant_override("shadow_offset_y", 2)
	return l


## Título grande con contorno oscuro (para el logo).
static func logo(text: String, color: Color, size: int) -> Label:
	var l := label(text, color, size, true)
	l.autowrap_mode = TextServer.AUTOWRAP_OFF
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.add_theme_color_override("font_outline_color", BLACK)
	l.add_theme_constant_override("outline_size", 6)
	return l


## `wrap` = false para botones en filas horizontales (con autowrap el texto se partiría letra a letra).
static func button(text: String, wrap := true) -> Button:
	var b := Button.new()
	b.text = text
	b.alignment = HORIZONTAL_ALIGNMENT_LEFT
	b.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART if wrap else TextServer.AUTOWRAP_OFF
	b.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	return b


static func background(name := "bg_space", dim := 0.0) -> Control:
	var holder := Control.new()
	holder.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	holder.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var bg := TextureRect.new()
	bg.texture = tex(name + "_portrait" if Layout.portrait else name)
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	holder.add_child(bg)
	if dim > 0.0:
		var shade := ColorRect.new()
		shade.color = Color(0.02, 0.03, 0.08, dim)
		shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
		holder.add_child(shade)
	return holder


## Ajusta la altura de un ScrollContainer al contenido, con tope `max_h` (llamar tras añadir el contenido, diferido).
static func fit_scroll(scroll: ScrollContainer, content: Control, max_h: float) -> void:
	scroll.custom_minimum_size.y = minf(content.get_combined_minimum_size().y, max_h)


## Icono pixel (12x12) ampliado `k` veces con el filtro nearest del proyecto.
static func icon(name: String, k := 2) -> TextureRect:
	var r := TextureRect.new()
	r.texture = tex("icon_" + name)
	r.custom_minimum_size = Vector2(12 * k, 12 * k)
	r.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	r.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return r


## Contenedor con un marco: PanelContainer cuyo estilo es `style` ("panel", "panel_dark", "panel_accent"...).
static func framed(style := "panel", pad := Vector2i(10, 8), draw_center := true) -> PanelContainer:
	var p := PanelContainer.new()
	p.add_theme_stylebox_override("panel", tex_box(style, 6, pad, draw_center))
	return p


## Fila "icono + barra + valor": devuelve el HBox con metas "bar" (PixelBar) y "label" (Label).
static func meter_row(icon_name: String, bar_color: Color, text_color := TEXT, seg_units := 1.0) -> HBoxContainer:
	var box := HBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	box.add_child(icon(icon_name, 2))
	var bar := PixelBar.new(bar_color, 14)
	bar.seg_units = seg_units
	bar.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bar.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	box.add_child(bar)
	var l := label("", text_color)
	l.autowrap_mode = TextServer.AUTOWRAP_OFF
	l.custom_minimum_size = Vector2(46, 0)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	box.add_child(l)
	box.set_meta("bar", bar)
	box.set_meta("label", l)
	return box


## Fila "icono + etiqueta" para el HUD. Devuelve el HBox; la etiqueta es `box.get_meta("label")`.
static func chip(icon_name: String, color := TEXT, k := 2) -> HBoxContainer:
	var box := HBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	box.add_child(icon(icon_name, k))
	var l := label("", color, SIZE_BODY)
	l.autowrap_mode = TextServer.AUTOWRAP_OFF
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	box.add_child(l)
	box.set_meta("label", l)
	return box
