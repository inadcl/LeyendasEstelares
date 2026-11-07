#!/usr/bin/env python3
"""Genera los efectos de sonido y la música ambiental de res://audio/ (solo stdlib, WAV 16 bit mono).

Uso: python3 tools/gen_audio.py [directorio_salida]
Son sonidos placeholder sintetizados; se pueden sustituir por audio propio con los mismos nombres.
"""
import math
import os
import random
import struct
import sys
import wave

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio")
os.makedirs(OUT, exist_ok=True)
RATE = 22050


def save(name, samples):
    peak = max(1e-9, max(abs(s) for s in samples))
    scale = 0.85 * 32767 / max(peak, 1.0) if peak > 1.0 else 0.85 * 32767
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * scale / 32767 * 32767)) for s in samples))


def env(i, n, attack=0.01, release=0.5):
    t = i / RATE
    dur = n / RATE
    a = min(1.0, t / attack) if attack > 0 else 1.0
    r = min(1.0, (dur - t) / (dur * release)) if release > 0 else 1.0
    return a * max(0.0, r)


def tone(freq, dur, vol=0.5, attack=0.005, release=0.8, harmonics=((1, 1.0),), sweep=0.0):
    n = int(RATE * dur)
    out = []
    phase = 0.0
    for i in range(n):
        f = freq + sweep * (i / n)
        phase += 2 * math.pi * f / RATE
        s = sum(a * math.sin(phase * h) for h, a in harmonics)
        out.append(s * vol * env(i, n, attack, release))
    return out


def mix(*tracks):
    n = max(len(t) for t in tracks)
    return [sum(t[i] if i < len(t) else 0.0 for t in tracks) for i in range(n)]


def concat(*tracks, gap=0.0):
    out = []
    pad = [0.0] * int(RATE * gap)
    for t in tracks:
        out += t + pad
    return out


def noise(dur, vol=0.3, release=0.8, lowpass=0.3, seed=1):
    rng = random.Random(seed)
    n = int(RATE * dur)
    out = []
    y = 0.0
    for i in range(n):
        y += lowpass * (rng.uniform(-1, 1) - y)
        out.append(y * vol * env(i, n, 0.003, release))
    return out


NOTE = {"A3": 220.0, "C4": 261.63, "E4": 329.63, "G4": 392.0, "A4": 440.0, "C5": 523.25, "E5": 659.25, "A5": 880.0, "D4": 293.66, "F4": 349.23}


def main():
    save("click", tone(1200, 0.045, 0.55, 0.001, 0.9, ((1, 1.0), (2, 0.3))))
    save("tick", tone(1800, 0.02, 0.4, 0.001, 0.9))
    save("step", mix(noise(0.07, 0.8, 0.9, 0.12), tone(110, 0.07, 0.5, 0.002, 0.9)))
    scan = tone(420, 0.45, 0.45, 0.02, 0.5, ((1, 1.0), (3, 0.2)), sweep=900)
    save("scan", mix(scan, [0.0] * 2000 + tone(1800, 0.12, 0.2, 0.005, 0.9)))
    jump = mix(noise(0.8, 0.5, 0.7, 0.05), tone(520, 0.8, 0.35, 0.03, 0.6, ((1, 1.0), (2, 0.4)), sweep=-420))
    save("jump", jump)
    save("blip", concat(tone(740, 0.06, 0.45, 0.003, 0.8), tone(988, 0.08, 0.45, 0.003, 0.9)))
    save("event", concat(tone(NOTE["E5"], 0.18, 0.4, 0.01, 0.9, ((1, 1.0), (2, 0.25))), tone(NOTE["A5"], 0.3, 0.35, 0.01, 0.9, ((1, 1.0), (2, 0.25)))))
    save("success", concat(*[tone(NOTE[n], 0.13, 0.45, 0.005, 0.7, ((1, 1.0), (2, 0.3))) for n in ("C5", "E5", "A5")]))
    save("setback", concat(tone(NOTE["E4"], 0.18, 0.5, 0.005, 0.7, ((1, 1.0), (2, 0.2))), tone(NOTE["C4"], 0.32, 0.5, 0.005, 0.9, ((1, 1.0), (2, 0.2)))))
    save("alert", mix(tone(140, 0.5, 0.5, 0.01, 0.6, ((1, 1.0), (2, 0.8), (3, 0.5))), tone(147, 0.5, 0.4, 0.01, 0.6, ((1, 1.0), (2, 0.8)))))
    save("victory", concat(*[tone(NOTE[n], 0.2, 0.45, 0.01, 0.6, ((1, 1.0), (2, 0.3), (3, 0.1))) for n in ("A3", "E4", "A4", "C5", "E5", "A5")], gap=0.02))
    save("defeat", mix(tone(110, 1.2, 0.5, 0.05, 0.8, ((1, 1.0), (2, 0.5))), tone(116.5, 1.2, 0.4, 0.05, 0.8, ((1, 1.0), (2, 0.4)))))

    # Música ambiental: pad lento que enlaza sin cortes (todas las frecuencias son ciclos enteros en la duración).
    dur = 16
    n = RATE * dur
    voices = [(110, 0.30), (165, 0.20), (220, 0.18), (329, 0.10), (440, 0.07)]
    rng = random.Random(3)
    drift = [rng.uniform(0, 6.28) for _ in voices]
    out = []
    for i in range(n):
        t = i / RATE
        s = 0.0
        for (f, a), d in zip(voices, drift):
            lfo = 0.65 + 0.35 * math.sin(2 * math.pi * (1 / dur) * (1 + voices.index((f, a))) * t + d)
            s += a * lfo * math.sin(2 * math.pi * f * t) + 0.35 * a * lfo * math.sin(2 * math.pi * (f + 0.25) * t * 1.0)
        out.append(s)
    save("ambient", out)
    print("Audio generado en", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
