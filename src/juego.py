import os
import sys

import pygame

from settings import (
    ALTO,
    AMARILLO,
    ANCHO,
    BLANCO,
    FPS,
    GRIS,
    NEGRO,
    RUTA_FONDO,
    RUTA_MUSICA,
    ROJO,
    VERDE,
)
from src.audio_arcade import crear_sfx_banana, crear_sfx_choque
from src.entidades import Banana, Meteorito, Mono, Palmera


def pantalla_inicio(screen, fuente, fuente_grande):
    esperando = True
    while esperando:
        screen.fill(NEGRO)
        txt_titulo = fuente_grande.render("MONKEY INVADERS", True, AMARILLO)
        txt_jugar = fuente.render("Presiona ENTER", True, BLANCO)
        screen.blit(txt_titulo, (ANCHO // 2 - txt_titulo.get_width() // 2, 200))
        screen.blit(txt_jugar, (ANCHO // 2 - txt_jugar.get_width() // 2, 350))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False


def pantalla_game_over(screen, fuente, fuente_grande, puntos):
    nombre = ""
    ingresando = True
    while ingresando:
        screen.fill(NEGRO)
        txt_go = fuente_grande.render("GAME OVER", True, ROJO)
        txt_nom = fuente.render(f"Tu Nombre: {nombre}", True, BLANCO)
        screen.blit(txt_go, (ANCHO // 2 - txt_go.get_width() // 2, 100))
        screen.blit(txt_nom, (ANCHO // 2 - txt_nom.get_width() // 2, 250))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and len(nombre) > 0:
                    ingresando = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < 3 and evento.unicode.isalnum():
                    nombre += evento.unicode.upper()

    # Guardar puntaje simple
    with open("puntajes.txt", "a", encoding="utf-8") as f:
        f.write(f"{nombre},{puntos}\n")

    mostrando = True
    while mostrando:
        screen.fill(NEGRO)
        txt_lb = fuente_grande.render("TOP 5", True, AMARILLO)
        screen.blit(txt_lb, (ANCHO // 2 - txt_lb.get_width() // 2, 50))

        try:
            with open("puntajes.txt", "r", encoding="utf-8") as f:
                mejores = sorted((linea.strip().split(",") for linea in f if "," in linea), key=lambda x: int(x[1]), reverse=True)[:5]
        except FileNotFoundError:
            mejores = []

        y_offset = 150
        for nombre, puntos_txt in mejores:
            screen.blit(fuente.render(nombre, True, BLANCO), (80, y_offset))
            screen.blit(fuente.render(str(puntos_txt), True, BLANCO), (ANCHO - 150, y_offset))
            y_offset += 50

        screen.blit(fuente.render("ENTER: Reintentar", True, GRIS), (ANCHO // 2 - 100, 480))
        screen.blit(fuente.render("ESC: Salir", True, GRIS), (ANCHO // 2 - 70, 520))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False


def jugar(screen):
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("DejaVu Sans Mono", 22, bold=True)
    fuente_grande = pygame.font.SysFont("DejaVu Sans Mono", 36, bold=True)

    mono = Mono()
    sprites_todos = pygame.sprite.Group(mono)
    grupo_meteoritos = pygame.sprite.Group()
    grupo_bananas = pygame.sprite.Group()
    grupo_palmeras = pygame.sprite.Group()

    puntuacion = 0
    nivel = 1
    meta_nivel = 40

    for _ in range(3):
        m = Meteorito()
        sprites_todos.add(m)
        grupo_meteoritos.add(m)

    for _ in range(1):
        b = Banana()
        sprites_todos.add(b)
        grupo_bananas.add(b)

    for x in [60, 185, 310]:
        p = Palmera(x, ALTO - 140)
        sprites_todos.add(p)
        grupo_palmeras.add(p)

    fondo = None
    if os.path.exists(RUTA_FONDO):
        fondo = pygame.image.load(RUTA_FONDO).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    snd_banana = crear_sfx_banana()
    snd_choque = crear_sfx_choque()
    snd_banana.set_volume(0.28)
    snd_choque.set_volume(0.20)

    if os.path.exists(RUTA_MUSICA):
        pygame.mixer.music.load(RUTA_MUSICA)
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.music.play(-1)

    jugando = True
    invencible_timer = 0

    while jugando:
        reloj.tick(FPS)
        if invencible_timer > 0:
            invencible_timer -= 1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        sprites_todos.update()

        if puntuacion >= meta_nivel:
            nivel += 1
            meta_nivel += 40 * nivel
            m = Meteorito(velocidad_extra=nivel)
            sprites_todos.add(m)
            grupo_meteoritos.add(m)

        for banana in pygame.sprite.spritecollide(mono, grupo_bananas, True):
            puntuacion += 10
            if snd_banana:
                snd_banana.play()
            if mono.vidas < 3:
                mono.vidas += 1
            nueva_b = Banana()
            sprites_todos.add(nueva_b)
            grupo_bananas.add(nueva_b)

        for palmera in grupo_palmeras:
            for met in pygame.sprite.spritecollide(palmera, grupo_meteoritos, True):
                palmera.vida -= 1
                if snd_choque:
                    snd_choque.play()
                if palmera.vida <= 0:
                    palmera.kill()
                nuevo_m = Meteorito(velocidad_extra=nivel)
                sprites_todos.add(nuevo_m)
                grupo_meteoritos.add(nuevo_m)

        if invencible_timer == 0:
            for met in pygame.sprite.spritecollide(mono, grupo_meteoritos, True):
                mono.vidas -= 1
                if snd_choque:
                    snd_choque.play()
                invencible_timer = 60
                if mono.vidas <= 0:
                    jugando = False
                nuevo_m = Meteorito(velocidad_extra=nivel)
                sprites_todos.add(nuevo_m)
                grupo_meteoritos.add(nuevo_m)

        if fondo is not None:
            screen.blit(fondo, (0, 0))
        else:
            screen.fill((8, 10, 24))
            for y in range(0, ALTO, 8):
                color = (8 + (y * 2) % 40, 10 + (y * 1) % 35, 24 + (y * 1) % 50)
                pygame.draw.line(screen, color, (0, y), (ANCHO, y), 1)
            for _ in range(40):
                x = (pygame.time.get_ticks() * 0.02 + _ * 17) % ANCHO
                y = (_ * 37 + pygame.time.get_ticks() * 0.03) % ALTO
                pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 1)
        sprites_todos.draw(screen)
        screen.blit(fuente.render(f"PTS:{puntuacion}", True, BLANCO), (10, 10))
        screen.blit(fuente.render(f"V:{mono.vidas}", True, ROJO), (ANCHO - 60, 10))
        screen.blit(fuente.render(f"LVL:{nivel}", True, VERDE), (ANCHO // 2 - 30, 10))
        pygame.display.flip()

    return pantalla_game_over(screen, fuente, fuente_grande, puntuacion)
