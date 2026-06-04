import math
import struct

import pygame


SAMPLE_RATE = 22050


def _generar_onda(freqs, duracion_ms, volumen=0.18, waveform="sine"):
    frames = int(SAMPLE_RATE * duracion_ms / 1000.0)
    buffer = bytearray()

    for i in range(frames):
        t = i / SAMPLE_RATE
        sample = 0.0

        for freq in freqs:
            if waveform == "square":
                sample += 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
            else:
                sample += math.sin(2 * math.pi * freq * t)

        sample *= volumen
        sample = max(-1.0, min(1.0, sample))
        buffer += struct.pack("<h", int(sample * 32767))

    return bytes(buffer)


def crear_sfx_banana():
    raw = _generar_onda([880, 1320], 65, volumen=0.12, waveform="sine")
    return pygame.mixer.Sound(buffer=raw)


def crear_sfx_choque():
    raw = _generar_onda([220, 180], 110, volumen=0.08, waveform="square")
    return pygame.mixer.Sound(buffer=raw)


def crear_musica_arcade():
    notas = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63]
    duracion_ms = 180
    frames = int(SAMPLE_RATE * 2.0)
    buffer = bytearray()

    for i in range(frames):
        t = i / SAMPLE_RATE
        nota = notas[int((i // (SAMPLE_RATE // 4)) % len(notas))]
        sample = 0.0
        sample += math.sin(2 * math.pi * nota * t)
        sample += 0.35 * math.sin(2 * math.pi * (nota * 2) * t)
        sample *= 0.08
        sample = max(-1.0, min(1.0, sample))
        buffer += struct.pack("<h", int(sample * 32767))

    return pygame.mixer.Sound(buffer=bytes(buffer))
