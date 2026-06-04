"""
Punto de entrada principal.
Ejecutar desde la raíz del proyecto: python main.py
"""

import pygame

from settings import ALTO, ANCHO, FPS
from src.juego import jugar, pantalla_inicio


def main() -> None:
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Monkey Invaders v1.0")

    fuente = pygame.font.SysFont("DejaVu Sans Mono", 22, bold=True)
    fuente_grande = pygame.font.SysFont("DejaVu Sans Mono", 36, bold=True)

    pantalla_inicio(screen, fuente, fuente_grande)

    corriendo = True
    while corriendo:
        corriendo = jugar(screen)

    pygame.quit()


if __name__ == "__main__":
    main()
