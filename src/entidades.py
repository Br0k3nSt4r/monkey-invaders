import random

import pygame

from settings import (
    ALTO,
    AMARILLO,
    ANCHO,
    GRIS,
    MARRON,
    RUTA_IMAGEN_BANANA,
    RUTA_IMAGEN_METEORO,
    RUTA_IMAGEN_MONO,
    RUTA_IMAGEN_PALMERA,
    VERDE,
)


class Mono(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(RUTA_IMAGEN_MONO).convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 20
        self.velocidad = 7
        self.vidas = 3

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad


class Meteorito(pygame.sprite.Sprite):
    def __init__(self, velocidad_extra=0):
        super().__init__()
        self.image = pygame.image.load(RUTA_IMAGEN_METEORO).convert_alpha()
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - 35)
        self.rect.y = random.randint(-300, -50)
        self.velocidad = random.randint(3, 6) + velocidad_extra

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - 35)
            self.rect.y = random.randint(-200, -40)


class Banana(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(RUTA_IMAGEN_BANANA).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - 25)
        self.rect.y = random.randint(-400, -50)
        self.velocidad = 4

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - 25)
            self.rect.y = random.randint(-400, -40)


class Palmera(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(RUTA_IMAGEN_PALMERA).convert_alpha()
        self.image = pygame.transform.scale(self.image, (72, 92))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vida = 3
