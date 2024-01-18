import pygame
from math import sqrt
from scripts import constants as const
from scripts import missile
from scripts import visual


class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y, name_turret):
        pygame.sprite.Sprite.__init__(self)
        self.name_turret = name_turret

        # записываем начальные характеристики башни
        self.upgrade_level = 1
        self.image = visual.load_image(const.TURRER[self.name_turret][self.upgrade_level - 1].get('im'),
                                       transforms=(const.TILE_SIZE, const.TILE_SIZE))
        self.range = const.TURRER[self.name_turret][self.upgrade_level - 1].get("range")
        self.cooldown = const.TURRER[self.name_turret][self.upgrade_level - 1].get("cooldown")
        self.damage = const.TURRER[self.name_turret][self.upgrade_level - 1].get("damage")
        self.cost_upgrade = const.TURRER[self.name_turret][self.upgrade_level - 1].get("cost")

        self.hints_upgrade = visual.font_time.render('upgrade ' + str(self.cost_upgrade), 1,
                                                     pygame.Color((0, 0, 0)))

        self.additional_damage = 1

        # цель башни
        self.target = None

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.missile_group = pygame.sprite.Group()

        self.update_time = -self.cooldown
        self.update_time_money = pygame.time.get_ticks()

        # создание визуального радиуса башни
        self.range_image = self.range_rect = None
        self.radius()

        # True, если башня выбрана
        self.selected = False

    def update(self, enemy_group, surface):
        # если прошло достаточно времени с предыдущего выстрела
        if pygame.time.get_ticks() - self.update_time > self.cooldown:
            self.target = self.pick_target(enemy_group)
            if self.target:  # если враг находится в диапазоне
                # воспроизводим анимацию атаки и создаём снаряд
                self.update_time = pygame.time.get_ticks()
                self.attack()
        if pygame.time.get_ticks() - self.update_time_money > const.TIME_MONEY:
            const.MONEY += 1
            self.update_time_money = pygame.time.get_ticks()
        self.missile_group.draw(surface)
        self.missile_group.update()

    def draw(self, screen):
        # рисуем башню
        screen.blit(self.image, self.rect)

        # если выбрана, показываем радиус и стоимость улучшения
        if self.selected:
            screen.blit(self.range_image, self.range_rect)
            if self.upgrade_level != 5:
                screen.blit(self.hints_upgrade, (self.rect.x - 10, self.rect.y - 20))

    def radius(self):
        # создание визуального радиуса башни
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "grey", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def pick_target(self, enemy_group):  # найти координаты цели
        # проверяем находится ли враг в диапазоне
        for enemy in enemy_group:
            x_dist = enemy.rect.x - self.rect.x
            y_dist = enemy.rect.y - self.rect.y
            dist = sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range and enemy.rect.y > 0:
                return enemy
        return None

    def attack(self):
        # создаёт снаряд
        missil = missile.Missile(visual.load_image('arrow.png', colorkey=-1), self.target,
                                 (self.rect.x, self.rect.y), self.damage * self.additional_damage)
        self.missile_group.add(missil)

    def upgrade(self):
        # улучшает характеристики башни

        # проверяем не максимальный ли сейчас уровень и хватает ли денег на улучшение

        if self.upgrade_level != 5:
            if const.MONEY >= self.cost_upgrade:
                visual.music_up.play()

                const.MONEY -= self.cost_upgrade

                # повышаем характеристики башни
                self.upgrade_level += 1
                self.image = visual.load_image(const.TURRER[self.name_turret][self.upgrade_level - 1].get('im'),
                                               transforms=(const.TILE_SIZE, const.TILE_SIZE))
                self.range = const.TURRER[self.name_turret][self.upgrade_level - 1].get("range")
                self.cooldown = const.TURRER[self.name_turret][self.upgrade_level - 1].get("cooldown")
                self.damage = const.TURRER[self.name_turret][self.upgrade_level - 1].get("damage")
                self.cost_upgrade = const.TURRER[self.name_turret][self.upgrade_level - 1].get("cost")

                # изменяем визуальный радиус
                self.radius()


# башня, которая уничтожает врагов, находящихся в радиусе действия башни
class Darkturret(Turret):
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.selected:
            screen.blit(self.range_image, self.range_rect)
            if self.upgrade_level != 3:
                screen.blit(self.hints_upgrade, (self.rect.x - 10, self.rect.y - 20))

    def pick_target(self, enemy_group):  # найти координаты цели
        # проверяем находится ли враг в диапазоне
        enem_gr = pygame.sprite.Group()
        for enemy in enemy_group:
            x_dist = enemy.rect.x - self.rect.x
            y_dist = enemy.rect.y - self.rect.y
            dist = sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range and enemy.rect.y > 0:
                enem_gr.add(enemy)
        return enem_gr

    def upgrade(self):
        if self.upgrade_level != 3:
            if const.MONEY >= self.cost_upgrade:
                visual.music_up.play()

                const.MONEY -= self.cost_upgrade
                self.upgrade_level += 1

                self.cost_upgrade = const.TURRER[self.name_turret][self.upgrade_level - 1].get("cost")
                self.cooldown = const.TURRER[self.name_turret][self.upgrade_level - 1].get("cooldown")
                self.image = visual.load_image(const.TURRER[self.name_turret][self.upgrade_level - 1].get('im'),
                                               transforms=(const.TILE_SIZE, const.TILE_SIZE))
                self.hints_upgrade = visual.font_time.render('upgrade ' + str(self.cost_upgrade), 1,
                                                             pygame.Color((255, 0, 0)))
        self.hints_upgrade = visual.font_time.render('upgrade ' + str(self.cost_upgrade), 1,
                                                     pygame.Color((0, 0, 0)))

    def attack(self):
        for target in self.target:
            missil = missile.Missile(
                visual.load_image('Daco.png', colorkey=-1, transforms=(const.TILE_SIZE // 2, const.TILE_SIZE // 2)),
                target, (self.rect.x, self.rect.y), self.damage)
            self.missile_group.add(missil)
