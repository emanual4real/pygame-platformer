import random
import sys
import time

import pygame
from pygame import QUIT

from constants import *
from platforms.platform import Platform, check
from players.player import Player


def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50, 100)
        p = Platform()
        c = True

        while c:
            p = Platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            c = check(p, platforms)

        platforms.add(p)
        all_sprites.add(p)


pygame.init()

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

P1 = Player()
PT1 = Platform()
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
PT1.moving = False
PT1.point = False

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
platforms.add(PT1)
all_sprites.add(PT1)
all_sprites.add(P1)

for x in range(random.randint(4, 5)):
    p1 = Platform()
    platforms.add(p1)
    all_sprites.add(p1)
    p1.move()

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump(platforms)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
    # game over
    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill((255, 0, 0))
            f = pygame.font.SysFont("Verdana", 20)
            g = f.render('Game Over', True, (123, 255, 0))
            displaysurface.blit(g, (WIDTH / 2, HEIGHT / 2))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()

    # refresh screen with all black
    displaysurface.fill((0, 0, 0))

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    plat_gen()
    P1.update(platforms)

    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(P1.score), True, (123, 255, 0))
    displaysurface.blit(g, (WIDTH / 2, 10))

    # loop through and display sprites
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    # update display
    pygame.display.update()
    # limits game loop to FPS=60
    FramePerSec.tick(FPS)
