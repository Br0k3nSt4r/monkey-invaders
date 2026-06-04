import os

# ── Colores ──────────────────────────────────────────────
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (34, 139, 34)
MARRON = (139, 69, 19)
AMARILLO = (255, 255, 0)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0)

# ── Dimensiones ───────────────────────────────────────────
ANCHO = 450
ALTO = 600
FPS = 60

# ── Rutas de recursos ────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
RUTA_IMAGEN_MONO = os.path.join(BASE_DIR, "assets", "images", "mono.png")
RUTA_IMAGEN_METEORO = os.path.join(BASE_DIR, "assets", "images", "meteoro.png")
RUTA_IMAGEN_BANANA = os.path.join(BASE_DIR, "assets", "images", "banana.png")
RUTA_IMAGEN_PALMERA = os.path.join(BASE_DIR, "assets", "images", "palmera.png")
RUTA_FONDO = os.path.join(BASE_DIR, "assets", "images", "fondo.png")

RUTA_SFX_BANANA = os.path.join(BASE_DIR, "assets", "sound", "monkey.mp3")
RUTA_SFX_CHOQUE = os.path.join(BASE_DIR, "assets", "sound", "death.mp3")
RUTA_MUSICA = os.path.join(BASE_DIR, "assets", "music", "music.mp3")
