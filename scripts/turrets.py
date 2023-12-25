import pygame
from math import sqrt
from scripts import constants as const
from scripts import missile
from scripts import visual


class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y, image):  # пока он принемает только одно изображение, а не несколько
        pygame.sprite.Sprite.__init__(self)
        self.upgrade_level = 1

        self.range = const.STATS[self.upgrade_level - 1].get("range")
        self.cooldown = const.STATS[self.upgrade_level - 1].get("cooldown")
        self.target = None

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # создание визуального радиуса башни
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "grey", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

        self.selected = False

    def update(self, enemy_group, surface):
        self.pick_target(enemy_group)
        if self.target:
            missil = missile.Missile(visual.load_image('arrow.png', colorkey=-1), self.target,
                                     (self.rect.x, self.rect.y), 5)
            missil.update(surface)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.selected:
            screen.blit(self.range_image, self.range_rect)

    def pick_target(self, enemy_group):  # найти координаты цели
        # проверяем находится ли враг в диапазоне
        for enemy in enemy_group:
            x_dist = enemy.rect.x - self.rect.x
            y_dist = enemy.rect.y - self.rect.y
            dist = sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range:
                self.target = enemy
            else:
                self.target = None