import pygame
import math


class Missile(pygame.sprite.Sprite):
    def __init__(self, image, target, pos, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

        self.target = target
        self.damage = damage

        self.vx, self.vy = 5, -5
        self.angle = 90

    def update(self, surface):
        dist_x = self.target.rect.x - self.rect.x
        dist_y = self.target.rect.y - self.rect.y
        self.angle = math.degrees(math.atan2(-dist_y, dist_x))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rect.move(self.vx, self.vy)
        surface.blit(self.image, self.rect)