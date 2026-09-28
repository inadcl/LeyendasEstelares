# Leyendas Estelares

Mini juego open source de **exploración espacial narrativa**, hecho con [Godot 4.3](https://godotengine.org) (multiplataforma).

Eliges a un viajero espacial, aterrizas en un planeta y exploras su superficie casilla a casilla
(mapa hexagonal con niebla, al estilo *The Curious Expedition*). Cada punto de interés plantea una situación
breve con 2–4 decisiones concretas: algunas arriesgadas, otras bloqueadas según tu perfil o tus actos
anteriores. Tono serio, de ciencia ficción exploratoria: primer contacto, dilemas éticos, prudencia.

## Cómo se juega

- **Recursos:** oxígeno (cada paso cuesta según el terreno), moral y datos científicos.
- **Objetivo:** llegar a la baliza del planeta y **volver a la nave** antes de quedarte sin aire.
- **Decisiones:** las opciones muestran su probabilidad de éxito; el rasgo de tu avatar da +20% en su especialidad.
- **Consecuencias:** tus actos activan banderas y cambian tu reputación con las facciones (Concordato, Vael),
  lo que abre o cierra opciones más adelante y cambia el epílogo.

## Ejecutar

1. Abre la carpeta con Godot 4.3+ y pulsa *Play*, o desde terminal: `godot --path .`
2. El arte ya está generado en `art/`. Para regenerarlo: `python3 tools/gen_art.py`

## Pruebas

```
godot --headless --path . --import          # solo la primera vez
godot --headless --path . res://tests/run_tests.tscn
```

Valida los datos, la geometría hexagonal, la generación de mapas (300 semillas) y simula partidas
completas con un bot usando el mismo motor que la interfaz.

Capturas de pantalla (requiere display, p. ej. `xvfb-run`):
`godot --path . res://tests/screenshot.tscn -- /ruta/salida`

## Estructura

| Ruta | Contenido |
|---|---|
| `data/` | Avatares, facciones, planetas y **eventos** en JSON (añadir contenido no requiere tocar código) |
| `scripts/` | Lógica pura (`planet_data`, `expedition`, `event_runner`, `game_state`) y UI (`scripts/ui/`) |
| `art/` | Pixel art placeholder generado por `tools/gen_art.py`; se puede sustituir por arte propio |
| `tests/` | Pruebas headless y capturas |

### Añadir un evento

Edita `data/events.json` y añade su id al `event_pool` del planeta en `data/planets.json`.
Cada opción tiene o bien `result` (determinista) o bien `risk` (`chance`, `success`, `fail`), y opcionalmente
`tag` (rasgo que da ventaja) y `requires` (`trait`, `flag`, `any_flag`, `not_flag`, `hint`).
Efectos: `oxygen`, `morale`, `data`, `rep`, `set_flags`. Las pruebas detectan errores de coherencia.

## Hoja de ruta

- [x] Fase 1: núcleo (mapa hexagonal, recursos, niebla, eventos con decisiones, 2 avatares, 1 planeta)
- [ ] Fase 2: más eventos, encuentros con facciones, objetos
- [ ] Fase 3: campaña con varios planetas y mapa estelar; estado persistente entre ellos
- [ ] Fase 4: arte propio, sonido y pulido; exportaciones (PC, móvil, web)

## Licencia

GPL v2 (ver `LICENSE`).
