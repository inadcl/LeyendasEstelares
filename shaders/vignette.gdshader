shader_type canvas_item;
// Viñeta suave sobre toda la pantalla.
void fragment() {
	vec2 d = (UV - 0.5) * vec2(1.0, 0.85);
	float v = smoothstep(0.32, 0.85, length(d));
	COLOR = vec4(0.0, 0.0, 0.03, v * 0.5);
}
