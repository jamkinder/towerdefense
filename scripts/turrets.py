import pygame
from math import sqrt
from scripts import constants as const
from scripts import missile
from scripts import visual


class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y, name_turret):
        pygame.sprite.Sprite.__init__(self)
        self.name_turret = name_turret

        self.upgrade_level = self.cost_upgrade = 3
        self.image = visual.load_image(const.TURRER[self.name_turret][self.upgrade_level - 1].get('im'),
                                       transforms=(const.TILE_SIZE, const.TILE_SIZE))
        self.range = const.TURRER[self.name_turret][self.upgrade_level - 1].get("range")
        self.cooldown = const.TURRER[self.name_turret][self.upgrade_level - 1].get("cooldown")
        self.damage = const.TURRER[self.name_turret][self.upgrade_level - 1].get("damage")
        self.cost_upgrade = const.TURRER[self.name_turret][self.upgrade_level - 1].get("cost")

        self.target = None

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.missile_group = pygame.sprite.Group()

        self.update_time = pygame.time.get_ticks()

        # создание визуального радиуса башни
        self.range_image = self.range_rect = None
        self.radius()

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
        else:
            self.missile_group = pygame.sprite.Group()

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
                                 (self.rect.x, self.rect.y), self.damage)
        return missil

    def upgrade(self):
        if self.upgrade_level != 5:
            if const.MONEY >= self.cost_upgrade:
                const.MONEY -= self.cost_upgrade
                self.upgrade_level += 1
                self.image = visual.load_image(const.TURRER[self.name_turret][self.upgrade_level - 1].get('im'),
                                               transforms=(const.TILE_SIZE, const.TILE_SIZE))
                self.range = const.TURRER[self.name_turret][self.upgrade_level - 1].get("range")
                self.cooldown = const.TURRER[self.name_turret][self.upgrade_level - 1].get("cooldown")
                self.damage = const.TURRER[self.name_turret][self.upgrade_level - 1].get("damage")
                self.cost_upgrade = const.TURRER[self.name_turret][self.upgrade_level - 1].get("cost")

                self.radius()

    def radius(self):
        # создание визуального радиуса башни
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "grey", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
