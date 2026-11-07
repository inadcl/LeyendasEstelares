extends Node
## Revisa el layout de todas las pantallas, eventos y conversaciones en ambos idiomas y tamaños:
## detecta texto partido letra a letra (columna estrecha y alta) y controles que se salen de la pantalla.
## godot --headless --path . res://tests/layout_test.tscn

var _failures := 0
var _checked := 0
var _sizes: Array[Vector2i] = [Vector2i(640, 360)]


func _ready() -> void:
	if "--portrait" in OS.get_cmdline_user_args():
		_sizes = [Vector2i(360, 640), Vector2i(360, 800)]
	for lang in T.LANGUAGES:
		T.set_language(lang, false)
		for size in _sizes:
			await _audit_all(lang, size)
	print("\n%s (%d controles revisados, %d fallos)" % ["LAYOUT OK" if _failures == 0 else "FALLOS", _checked, _failures])
	get_tree().quit(0 if _failures == 0 else 1)


## Monta una pantalla dentro de un SubViewport del tamaño dado y devuelve [viewport, raíz].
func _stage(size: Vector2i) -> Array:
	var vp := SubViewport.new()
	vp.size = size
	vp.disable_3d = true
	vp.transparent_bg = false
	add_child(vp)
	var root := Control.new()
	root.theme = UITheme.build()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	vp.add_child(root)
	return [vp, root]


func _show(screen: Control, size: Vector2i, label: String, setup := Callable(), keep := false) -> void:
	var st := _stage(size)
	(st[1] as Control).add_child(screen)
	await get_tree().process_frame
	await get_tree().process_frame
	if setup.is_valid():
		setup.call()
		await get_tree().process_frame
		await get_tree().process_frame
	_audit(screen, size, label)
	if not keep:
		(st[0] as Node).queue_free()
		await get_tree().process_frame


func _audit_all(lang: String, size: Vector2i) -> void:
	var tag := "[%s %dx%d]" % [lang, size.x, size.y]
	Layout.portrait = size.y > size.x
	GameState.start_run(Content.avatar_by_id("vance"), Content.factions, Content.campaign)
	GameState.apply_effects({"set_flags": ["met_vael", "vael_contacto", "gremio_amigo", "draeth_respeto"]})
	await _show(TitleScreen.new(), size, tag + " título")
	await _show(AvatarScreen.new(), size, tag + " avatares")
	var camp := Campaign.new(GameState, Content.campaign, 12)
	for id in camp.sector.nodes:
		camp.sector.nodes[id]["scanned"] = true
	var sec := SectorScreen.new()
	sec.campaign = camp
	await _show(sec, size, tag + " mapa estelar", func(): sec._select(camp.sector.nodes[camp.current]["edges"][0]))

	for sp in Content.campaign["species"]:
		for avatar in ["vance", "okafor"]:
			GameState.start_run(Content.avatar_by_id(avatar), Content.factions, Content.campaign)
			GameState.apply_effects({"set_flags": ["met_vael", "vael_contacto", "gremio_amigo", "draeth_respeto"], "data": 5})
			var cs := ContactScreen.new()
			cs.species_id = sp
			await _show(cs, size, "%s contacto %s/%s" % [tag, sp, avatar], func():
				cs._finish_typing(), true)
			# Recorre todos los intercambios mostrando indicaciones y respuestas.
			var guard := 0
			while not cs.runner.finished() and guard < 8:
				guard += 1
				cs._show_prompt()
				cs._finish_typing()
				await get_tree().process_frame
				await get_tree().process_frame
				_audit(cs, size, "%s contacto %s/%s intercambio %d" % [tag, sp, avatar, cs.runner.index])
				var pick := 0
				for i in cs.runner.exchange()["options"].size():
					if cs.runner.lock_reason(i) == "":
						pick = i
				cs._on_choose(pick)
				cs._finish_typing()
				await get_tree().process_frame
				await get_tree().process_frame
				_audit(cs, size, "%s contacto %s/%s respuesta %d" % [tag, sp, avatar, cs.runner.index])
			cs._show_outcome()
			cs._finish_typing()
			await get_tree().process_frame
			await get_tree().process_frame
			_audit(cs, size, "%s contacto %s/%s desenlace" % [tag, sp, avatar])
			cs.get_parent().get_parent().queue_free()

	GameState.start_run(Content.avatar_by_id("vance"), Content.factions, Content.campaign)
	for planet in Content.planets:
		var ms := MapScreen.new()
		ms.planet = planet
		await _show(ms, size, "%s planeta %s briefing" % [tag, planet["id"]], Callable(), true)
		ms.get_parent().get_parent().queue_free()
	# Todos los eventos: presentación y resultado, con y sin opciones bloqueadas.
	var holder := MapScreen.new()
	holder.planet = Content.planets[2]
	var st := _stage(size)
	(st[1] as Control).add_child(holder)
	await get_tree().process_frame
	await get_tree().process_frame
	holder._overlay.close()
	for id in Content.events:
		for flagged in [false, true]:
			GameState.flags = {"vael_contacto": true, "mapa_vael": true, "gremio_amigo": true, "draeth_respeto": true} if flagged else {}
			GameState.data = 5
			holder._overlay.present_event(id, func(_i): return {"text": "x", "lines": [], "success": true}, func(): pass)
			await get_tree().process_frame
			await get_tree().process_frame
			_audit(holder, size, "%s evento %s (flags=%s)" % [tag, id, flagged])
		# resultado largo
		holder._overlay.present_event(id, func(i): return {"text": T.ev(id, "c0.%s" % ("ok" if Content.events[id]["choices"][0].has("risk") else "res")), "lines": ["Oxygen −3", "Reputation Concordat +1", "Data +2"], "success": true}, func(): pass)
		holder._overlay._on_pick(id, 0, func(_i): return {"text": T.ev(id, "c0.%s" % ("ok" if Content.events[id]["choices"][0].has("risk") else "res")), "lines": ["Oxygen −3", "Reputation Concordat +1", "Data +2"], "success": true}, func(): pass)
		await get_tree().process_frame
		await get_tree().process_frame
		_audit(holder, size, "%s resultado de %s" % [tag, id])
	(st[0] as Node).queue_free()
	await get_tree().process_frame

	for ending in ["victory", "abort", "fuel", "oxygen", "morale"]:
		GameState.start_run(Content.avatar_by_id("vance"), Content.factions, Content.campaign)
		GameState.apply_effects({"rep": {"concordato": 2, "vael": -1}, "set_flags": ["baliza_dialogo", "colonia_danada", "torre_reparada", "jardin_protegido", "respeto_vael"]})
		var es := EndScreen.new()
		es.ending = ending
		es.jumps = 7
		await _show(es, size, "%s final %s" % [tag, ending])
	var help := Overlay.new()
	var st2 := _stage(size)
	(st2[1] as Control).add_child(help)
	help.show_help()
	await get_tree().process_frame
	await get_tree().process_frame
	_audit(help, size, tag + " ayuda")
	(st2[0] as Node).queue_free()


func _audit(root: Node, size: Vector2i, label: String) -> void:
	var bounds := Rect2(Vector2.ZERO, Vector2(size))
	for n in root.find_children("*", "Overlay", true, false) + ([root] if root is Overlay else []):
		var o := n as Overlay
		if o.is_open():
			var want := minf(o._box.get_combined_minimum_size().y, size.y - 48.0)
			if absf(o._scroll.size.y - want) > 3.0:
				_fail("%s: el panel del diálogo mide %d y su contenido %d" % [label, int(o._scroll.size.y), int(want)])
	for n in root.find_children("*", "Control", true, false):
		var c := n as Control
		if not c.is_visible_in_tree():
			continue
		_checked += 1
		if c is Label:
			var l := c as Label
			if l.autowrap_mode != TextServer.AUTOWRAP_OFF and l.text.length() > 8 and l.get_line_count() > maxi(2, l.text.length() / 7):
				_fail("%s: texto en vertical (%d líneas, ancho %d): '%s'" % [label, l.get_line_count(), int(l.size.x), l.text.left(40)])
		if c is Label or c is Button or c is PanelContainer or c is PixelBar:
			if _inside_scroll(c):
				continue
			var r := c.get_global_rect()
			if r.end.x > bounds.end.x + 1.0 or r.end.y > bounds.end.y + 1.0 or r.position.x < -1.0 or r.position.y < -1.0:
				_fail("%s: %s se sale de la pantalla %s (%s)" % [label, c.get_class(), r, (c as Label).text.left(30) if c is Label else (c as Button).text.left(30) if c is Button else ""])


func _inside_scroll(c: Node) -> bool:
	var p := c.get_parent()
	while p != null:
		if p is ScrollContainer:
			return true
		p = p.get_parent()
	return false


func _fail(msg: String) -> void:
	_failures += 1
	if _failures <= 40:
		print("  FALLO: ", msg)
