# Leyendas Estelares / Stellar Legends

Mini juego open source de **exploración espacial narrativa** hecho con [Godot](https://godotengine.org) 4 (multiplataforma).
Disponible en **español e inglés** (cambio de idioma desde el título).

Capitanea la nave *Meridiana* a través de un sector desconocido, siguiendo un pulso de tres tonos hasta su origen.
Decides a dónde saltar, hablas con otras formas de vida y exploras la superficie de los planetas.
Tono serio, de ciencia ficción exploratoria: primer contacto, dilemas éticos, prudencia.

## Cómo se juega

El juego tiene tres capas:

1. **Mapa estelar (estilo *FTL*).** Cada salto gasta **combustible** (las rutas largas cuestan 2). Los nodos
   aparecen como «?» hasta que los **escaneas**: un escaneo revela el tipo de nodo y qué hay en un planeta
   (ruinas, señales, restos, vida, combustible). Si te quedas sin combustible lejos del destino, la campaña termina.
2. **Comunicaciones de primer contacto.** Tres especies con valores distintos: los **Vael** (franqueza),
   el **Gremio de Hallen** (cautela) y el **Dominio Draeth** (firmeza). Cada respuesta es una *postura*
   (abierta, cauta, firme, engañosa) que sube o baja **confianza** y **tensión**. Según las barras
   terminas en alianza, acuerdo, distancia prudente u hostilidad. La Dra. Vance analiza qué valora cada especie;
   el Cmdte. Okafor templa la tensión.
3. **Exploración de planetas** (estilo *The Curious Expedition*). Mapa hexagonal con niebla, oxígeno que se
   gasta según el terreno, puntos de interés con decisiones (a veces arriesgadas) y un objetivo que alcanzar
   antes de volver a la nave.

Lo que haces en una capa afecta a las otras: banderas y reputación (Concordato, Vael) abren o cierran opciones
más adelante y cambian el epílogo. Por ejemplo, ser amigo del Gremio o ganarte el respeto de los Draeth desbloquea
opciones exclusivas en anomalías posteriores (por eso importa el orden en que los encuentras).

**Controles:** ratón (clic) en todo; en el mapa de superficie también teclado: `Q` `E` (arriba), `A` `D` (lados),
`Z` `C` (abajo). En los menús, las flechas y Enter. Atajos globales: `F1` ayuda («Cómo se juega», se muestra solo
la primera vez), `M` sonido, `F11` pantalla completa.

## Ejecutar

Necesitas Godot 4.3 o superior (probado en 4.3 y 4.7).

```
godot --path . --import      # solo la primera vez (o abre el proyecto una vez en el editor)
godot --path .
```

Desde el editor: abre `project.godot` y pulsa *Play* (F5).

## Traducciones

Todos los textos están en **`translations/strings.csv`** (formato estándar de Godot: `keys,en,es`).
Los JSON de `data/` solo contienen mecánica; el texto se busca por claves con nombre convencional:

| Texto | Clave |
|---|---|
| Evento | `event.<id>.title`, `.text`, `.c<i>.text`, `.c<i>.ok` / `.fail` / `.res`, `.c<i>.hint` |
| Encuentro | `contact.<id>.intro`, `.x<n>.prompt`, `.x<n>.o<i>`, `.x<n>.o<i>.reply`, `.out.<desenlace>` |
| Planeta, avatar, especie | `planet.<id>.name/intro/...`, `avatar.<id>.name/...`, `species.<id>.name/desc` |
| Interfaz | `ui.*`, `fx.*`, `ending.*` |

Los parámetros se escriben `{nombre}`. En el código se usa `T.t("clave", {"nombre": valor})`.

**Añadir un idioma:** añade una columna con su código (p. ej. `fr`) al CSV y una entrada en `T.LANGUAGES`
(`scripts/t.gd`). Las pruebas avisan de cualquier clave sin traducir, parámetros que no coinciden entre idiomas
y claves sin uso.

## Pruebas

```
godot --headless --path . res://tests/run_tests.tscn   # lógica, datos, traducciones y bots de campaña
godot --headless --path . res://tests/ui_test.tscn      # recorre la interfaz con clics y teclas reales
```

`run_tests` valida datos y traducciones, genera cientos de mapas y sectores, comprueba las conversaciones y
simula campañas completas con un bot usando el mismo motor que la interfaz.
Capturas (requiere display, p. ej. `xvfb-run`): `godot --path . res://tests/screenshot.tscn -- /ruta [en|es]`.

## Estructura

| Ruta | Contenido |
|---|---|
| `data/` | Mecánica en JSON: avatares, facciones, planetas, eventos, especies, encuentros, campaña |
| `translations/` | `strings.csv`: todos los textos (en, es) |
| `scripts/` | Lógica pura (`sector_data`, `campaign`, `planet_data`, `expedition`, `event_runner`, `contact_runner`, `game_state`) y UI (`scripts/ui/`) |
| `shaders/` | Viñeta y efecto de comunicación |
| `ui/` | Kit de interfaz pixel art (marcos 9-slice, botones, iconos, insignias, fondos, cursor) generado por `tools/gen_ui.py` |
| `fonts/` | Fuente pixel *Jersey 10* (SIL Open Font License, ver `fonts/OFL-Jersey10.txt`) |
| `audio/` | Efectos y música ambiental sintetizados por `tools/gen_audio.py` (se pueden sustituir por audio propio) |
| `art/` | Pixel art placeholder generado por `tools/gen_art.py` (se puede sustituir por arte propio) |
| `tests/` | Pruebas headless, prueba de UI y capturas |

### Añadir contenido

- **Evento:** añádelo a `data/events.json` (cada opción tiene `result` o `risk`; opcional `tag` y `requires`),
  escribe sus textos en el CSV y añade su id al `event_pool` de un planeta o a `anomaly_pool` en `data/campaign.json`.
- **Encuentro:** añádelo a `data/encounters.json` con su especie, intercambios y desenlaces (`data/species.json`
  define cómo reacciona cada especie a cada postura).
- Regenerar el arte: `python3 tools/gen_art.py` (sprites), `python3 tools/gen_ui.py` (interfaz) y `python3 tools/gen_audio.py` (sonido).

## Hoja de ruta

- [x] Fase 1: exploración de planetas (mapa hexagonal, recursos, eventos con decisiones)
- [x] Fase 2: mapa estelar con combustible y escaneos, 3 especies con comunicaciones, 3 planetas con biomas, español/inglés
- [ ] Fase 3: tripulación (los avatares como equipo), objetos y comercio con las especies
- [ ] Fase 4: arte propio, sonido y pulido; exportaciones (PC, móvil, web)

## Licencia

Código y arte: GPL v2 (ver `LICENSE`). La fuente *Jersey 10* (© The Soft Type Project Authors) se distribuye con la
SIL Open Font License 1.1 (`fonts/OFL-Jersey10.txt`).
