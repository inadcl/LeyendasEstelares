class_name SummaryScreen
extends Control
## Cierre de una salida: {result: "success"|"abort"|"fail", reason: String}.

signal continue_pressed

var planet: Dictionary = {}
var outcome: Dictionary = {}


func _ready() -> void:
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(UITheme.background())
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	add_child(center)
	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(460, 0)
	center.add_child(panel)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 8)
	panel.add_child(v)

	var result: String = outcome.get("result", "abort")
	var title := "Misión cumplida"
	var color := UITheme.GOOD
	var body: String = planet.get("outro_success", "")
	if result == "abort":
		title = "Misión abortada"
		color = UITheme.WARN
		body = planet.get("outro_abort", "")
	elif result == "fail":
		title = "Expedición perdida"
		color = UITheme.BAD
		body = _fail_text(outcome.get("reason", ""))
	v.add_child(UITheme.label("%s — %s" % [planet.get("name", ""), title], color, 18))
	v.add_child(UITheme.label(body, UITheme.TEXT, 12))

	if result == "success":
		for e in planet.get("epilogues", []):
			if GameState.has_flag(e["flag"]):
				v.add_child(UITheme.label("· " + e["text"], UITheme.DIM, 11))
	v.add_child(HSeparator.new())
	v.add_child(UITheme.label("Datos reunidos: %d   ·   Moral: %d/%d" % [GameState.data, GameState.morale, GameState.max_morale], UITheme.ACCENT, 12))
	for faction in GameState.rep:
		var n: int = GameState.rep[faction]
		v.add_child(UITheme.label("Reputación %s: %s%d" % [GameState.faction_names.get(faction, faction), "+" if n > 0 else "", n], UITheme.DIM, 11))
	var btn := UITheme.button("Volver al título")
	btn.alignment = HORIZONTAL_ALIGNMENT_CENTER
	btn.pressed.connect(func(): continue_pressed.emit())
	v.add_child(btn)
	btn.grab_focus()


func _fail_text(reason: String) -> String:
	if reason == "oxygen":
		return "Las reservas de oxígeno se agotaron lejos de la nave. La Meridiana registra la pérdida y suspende las operaciones en la superficie."
	return "La moral de la expedición se quebró. Sin cohesión ni confianza, la operación no pudo continuar."
