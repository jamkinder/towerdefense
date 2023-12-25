import pygame
from scripts import constants as const


class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y, image):  # пока он принемает только одно изображение, а не несколько
        pygame.sprite.Sprite.__init__(self)
        self.upgrade_level = 1

        self.range = const.STATS[self.upgrade_level - 1].get("range")
        self.cooldown = const.STATS[self.upgrade_level - 1].get("cooldown")

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
