class_name EventRunner
extends RefCounted
## Reglas de las decisiones de un evento. `state` es GameState (o algo con su misma interfaz).

const TAG_BONUS := 0.2


## "" si la opción se puede elegir; si no, el motivo (texto para el jugador).
static func lock_reason(choice: Dictionary, state) -> String:
	var req: Dictionary = choice.get("requires", {})
	var hint: String = req.get("hint", "No disponible")
	if req.has("trait") and not state.has_trait(req["trait"]):
		return hint
	if req.has("flag") and not state.has_flag(req["flag"]):
		return hint
	if req.has("any_flag"):
		var ok := false
		for f in req["any_flag"]:
			ok = ok or state.has_flag(f)
		if not ok:
			return hint
	if req.has("not_flag") and state.has_flag(req["not_flag"]):
		return hint
	return ""


static func success_chance(choice: Dictionary, state) -> float:
	if not choice.has("risk"):
		return 1.0
	var chance: float = choice["risk"]["chance"]
	if choice.has("tag") and state.has_trait(choice["tag"]):
		chance += TAG_BONUS
	return clampf(chance, 0.05, 0.95)


## Resuelve la opción: aplica efectos y devuelve {text, lines, success}.
static func resolve(choice: Dictionary, state, rng: RandomNumberGenerator) -> Dictionary:
	var branch: Dictionary
	var success := true
	if choice.has("risk"):
		success = rng.randf() < success_chance(choice, state)
		branch = choice["risk"]["success"] if success else choice["risk"]["fail"]
	else:
		branch = choice["result"]
	var lines: Array[String] = state.apply_effects(branch.get("effects", {}))
	return {"text": branch.get("text", ""), "lines": lines, "success": success}
