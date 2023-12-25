import pygame
import math
from scripts import constants as const


class Missile(pygame.sprite.Sprite):
    def __init__(self, image, target, pos, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.update_time = pygame.time.get_ticks()

        self.target = target
        self.damage = damage
        self.angle = 90

        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.target)
        # определяем направление к точке, в которой находится враг
        self.vx, self.vy = (self.target.rect.x - self.rect.x) / 20 * abs(target.vx), (
                self.target.rect.y - self.rect.y) / 20 * abs(target.vy)

    def update(self):
        # если прошло время поворачивает стрелу
        if pygame.time.get_ticks() - self.update_time > const.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.rotate()
        # перемешает стрелу
        self.rect = self.rect.move(self.vx, self.vy)
        # если стрела каснулась врага или вышла за пределы экрана, удаляем её
        if (pygame.sprite.spritecollideany(self, self.enemy_group)
                or not 0 <= self.rect.y <= const.SCREEN_HEIGHT or not 0 <= self.rect.x <= const.SCREEN_WIDTH):
            self.target.healt -= self.damage
            self.kill()

    def rotate(self):  # поварачивает стрелу
        dist_x = self.target.rect.x - self.rect.x
        dist_y = self.target.rect.y - self.rect.y
        self.angle = math.degrees(math.atan2(dist_y, dist_x))
        self.image = pygame.transform.rotate(self.image, self.angle)
