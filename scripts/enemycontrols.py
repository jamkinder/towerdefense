import pygame
from scripts import visual


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, tiles_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = visual.load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.tiles_group = tiles_group

        self.vx, self.vy = -1, 1

        self.trajectory = 0  # если trajectory кратна 2, то движемся по y, наоборот x

    def update(self):
        if self.trajectory % 2 == 0:
            self.rect = self.rect.move(0, self.vy)
        else:
            self.rect = self.rect.move(self.vx, 0)
        if pygame.sprite.spritecollideany(self, self.tiles_group):
            self.trajectory += 1
            if self.trajectory % 2 == 0:
                self.rect = self.rect.move(self.vx * -10, 0)
            else:
                self.rect = self.rect.move(0, self.vy * -10)
                self.vx *= -1