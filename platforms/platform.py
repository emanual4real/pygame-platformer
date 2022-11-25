import random

import pygame

from constants import *


def check(platform, group):
    if pygame.sprite.spritecollide(platform, group, False):
        return True
    else:
        for entity in group:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 50) and (
                    abs(platform.rect.bottom - entity.rect.top) < 50):
                return True
        return False


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30)))
        self.point = True
        self.speed = random.randint(-1, 1)
        self.moving = True

    def move(self):
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
