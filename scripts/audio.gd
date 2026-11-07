extends Node
## Sonido del juego (autoload "Sfx"): efectos puntuales y música ambiental. Archivos en res://audio/ (tools/gen_audio.py).

const VOICES := 6

var muted := false
var _players: Array[AudioStreamPlayer] = []
var _next := 0
var _streams := {}
var _music: AudioStreamPlayer


func _ready() -> void:
	muted = bool(Settings.get_value("audio", "muted", false))
	for i in VOICES:
		var p := AudioStreamPlayer.new()
		add_child(p)
		_players.append(p)
	_music = AudioStreamPlayer.new()
	_music.volume_db = -13.0
	add_child(_music)
	AudioServer.set_bus_mute(0, muted)


func play(sound: String, volume_db := 0.0) -> void:
	var stream := _stream(sound)
	if stream == null:
		return
	var p := _players[_next]
	_next = (_next + 1) % VOICES
	p.stream = stream
	p.volume_db = volume_db
	p.play()


func start_music() -> void:
	if _music.playing:
		return
	var stream := _stream("ambient")
	if stream is AudioStreamWAV:
		var wav := stream as AudioStreamWAV
		wav.loop_mode = AudioStreamWAV.LOOP_FORWARD
		wav.loop_begin = 0
		wav.loop_end = wav.data.size() / 2  # 16 bit mono
	_music.stream = stream
	_music.play()


func set_muted(value: bool) -> void:
	muted = value
	AudioServer.set_bus_mute(0, muted)
	Settings.set_value("audio", "muted", muted)


func toggle_mute() -> void:
	set_muted(not muted)


func _stream(sound: String) -> AudioStream:
	if not _streams.has(sound):
		var path := "res://audio/%s.wav" % sound
		_streams[sound] = load(path) if ResourceLoader.exists(path) else null
		if _streams[sound] == null:
			push_warning("Sonido ausente: %s" % path)
	return _streams[sound]
