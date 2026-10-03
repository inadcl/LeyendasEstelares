class_name UITheme
extends RefCounted
## Tema visual compartido: paleta oscura, paneles planos y botones sobrios.

const BG := Color("0b0e17")
const PANEL := Color("141a2b")
const PANEL_BORDER := Color("2c3a5c")
const TEXT := Color("d7e2f2")
const DIM := Color("7f8fab")
const ACCENT := Color("5cc8e8")
const WARN := Color("e8a95c")
const BAD := Color("e0605c")
const GOOD := Color("74d68b")


static func box(bg: Color, border: Color, pad := 6, border_w := 1) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.set_content_margin_all(pad)
	return sb


static func build() -> Theme:
	var t := Theme.new()
	t.default_font_size = 12
	t.set_color("font_color", "Label", TEXT)
	t.set_color("default_color", "RichTextLabel", TEXT)
	t.set_font_size("normal_font_size", "RichTextLabel", 12)
	t.set_stylebox("panel", "PanelContainer", box(PANEL, PANEL_BORDER, 8))
	t.set_stylebox("normal", "Button", box(Color("1b2440"), PANEL_BORDER, 6))
	t.set_stylebox("hover", "Button", box(Color("25325a"), ACCENT, 6))
	t.set_stylebox("pressed", "Button", box(Color("31427a"), ACCENT, 6))
	t.set_stylebox("disabled", "Button", box(Color("10141f"), Color("1e2638"), 6))
	t.set_stylebox("focus", "Button", StyleBoxEmpty.new())
	t.set_color("font_color", "Button", TEXT)
	t.set_color("font_hover_color", "Button", Color.WHITE)
	t.set_color("font_disabled_color", "Button", Color("4a566e"))
	t.set_stylebox("background", "ProgressBar", box(Color("0d1220"), PANEL_BORDER, 0))
	return t


static func label(text: String, color := TEXT, size := 12) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_color_override("font_color", color)
	l.add_theme_font_size_override("font_size", size)
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return l


static func bar(color: Color) -> ProgressBar:
	var b := ProgressBar.new()
	b.show_percentage = false
	b.custom_minimum_size = Vector2(0, 8)
	b.add_theme_stylebox_override("fill", box(color, color, 0, 0))
	return b


## `wrap` = false para botones en filas horizontales (con autowrap el texto se partiría letra a letra).
static func button(text: String, wrap := true) -> Button:
	var b := Button.new()
	b.text = text
	b.alignment = HORIZONTAL_ALIGNMENT_LEFT
	b.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART if wrap else TextServer.AUTOWRAP_OFF
	return b


static func background() -> TextureRect:
	var bg := TextureRect.new()
	bg.texture = Art.tex("bg_stars")
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return bg
