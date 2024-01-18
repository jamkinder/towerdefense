import pygame
import math
import random
from scripts import constants as const

pygame.mixer.init()
music_damage = pygame.mixer.Sound("data/music/damage_m.wav")
music_damage.set_volume(0.1)


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
        self.angle = 0

        self.rotate()
        self.pos = pos

        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.target)

        # определяем направление к точке, в которой находится враг
        self.vx, self.vy = (self.target.rect.x - self.rect.x) / 15 * abs(target.vx), (
                self.target.rect.y - self.rect.y) / 15 * abs(target.vy)

    def update(self):
        # перемешает стрелу
        self.rect = self.rect.move(self.vx, self.vy)
        # если стрела коснулась врага или вышла за пределы экрана, удаляем её
        if (pygame.sprite.spritecollideany(self, self.enemy_group)
            or not 0 <= self.rect.y <= const.SCREEN_HEIGHT or not 0 <= self.rect.x <= const.SCREEN_WIDTH) or not (
                (self.target.rect.y - self.pos[1] > 0 and self.target.rect.y - self.rect.y + self.rect[3] > 0) or (
                (self.target.rect.y - self.pos[1] < 0 and self.target.rect.y - self.rect.y - self.rect[
                    3] < 0))) or not (
                (self.target.rect.x - self.pos[0] > 0 and self.target.rect.x - self.rect.x - self.rect[2] > 0) or (
                (self.target.rect.x - self.pos[0] < 0 and self.target.rect.x - self.rect.x + self.rect[2] < 0))):

            music_damage.play()
            # шанс крита
            if random.randint(0, 50) % 10 == 0:
                self.target.healt -= self.damage
            self.target.healt -= self.damage
            self.kill()

    def rotate(self):
        # поворачивает стрелу
        dist_x = self.target.rect.x - self.rect.x
        dist_y = self.target.rect.y - self.rect.y

        if dist_y > 0:
            self.angle = 180
        if dist_y != 0:
            self.angle += math.degrees(math.atan((dist_x / dist_y)))
            self.image = pygame.transform.rotate(self.image, self.angle)