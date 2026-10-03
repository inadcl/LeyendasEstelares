class_name Layout
extends RefCounted
## Orientación de la interfaz: apaisada (640x360, bandas laterales si sobra) o vertical (360x640 que se
## amplía a lo alto para llenar la pantalla). Las pantallas leen `Layout.portrait` al construirse.

const LANDSCAPE := Vector2i(640, 360)
const PORTRAIT := Vector2i(360, 640)

static var portrait := false
## -1 = automático (según la ventana), 0 = forzar apaisado, 1 = forzar vertical (pruebas en escritorio, tecla F10).
static var override := -1
## Margen superior en píxeles lógicos para muescas/barras del sistema (solo en móvil vertical).
static var safe_top := 0


static func wants_portrait(window: Window) -> bool:
	if override >= 0:
		return override == 1
	return window.size.y > window.size.x


static func apply(window: Window, want_portrait: bool) -> void:
	portrait = want_portrait
	window.content_scale_size = PORTRAIT if portrait else LANDSCAPE
	window.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_EXPAND if portrait else Window.CONTENT_SCALE_ASPECT_KEEP
	safe_top = 0
	if portrait and OS.has_feature("mobile"):
		var area := DisplayServer.get_display_safe_area()
		var screen := DisplayServer.screen_get_size()
		if screen.x > 0:
			safe_top = int(ceil(float(area.position.y) * PORTRAIT.x / screen.x))
