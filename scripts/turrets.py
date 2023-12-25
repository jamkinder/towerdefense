import pygame
from math import sqrt
from scripts import constants as const
from scripts import missile
from scripts import visual


class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y, image):  # пока он принемает только одно изображение, а не несколько
        pygame.sprite.Sprite.__init__(self)
        self.upgrade_level = 3

        self.range = const.STATS[self.upgrade_level - 1].get("range")
        self.cooldown = const.STATS[self.upgrade_level - 1].get("cooldown")
        self.target = None

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.missile_group = pygame.sprite.Group()

        self.update_time = pygame.time.get_ticks()

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
        self.target = self.pick_target(enemy_group)
        if self.target:  # если враг находится в диапазоне
            # если прошло достаточно времени с предыдущего  выстрела
            if pygame.time.get_ticks() - self.update_time > self.cooldown:
                # воспроизводим анимацию атаки и создаём снаряд
                self.missile_group.add(self.attack())

            self.missile_group.draw(surface)
            self.missile_group.update()

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
                return enemy
            else:
                return None

    def attack(self):
        # анимация атаки

        # создаёт снаряд
        self.update_time = pygame.time.get_ticks()
        missil = missile.Missile(visual.load_image('arrow.png', colorkey=-1), self.target,
                                 (self.rect.x, self.rect.y), 5)
        return missil