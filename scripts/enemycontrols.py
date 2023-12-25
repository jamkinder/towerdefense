import pygame
from scripts import visual
from scripts import enemyspawnerData as spawner

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, tiles_group):
        pygame.sprite.Sprite.__init__(self)

        self.frames = []
        image_sheet = visual.load_image(sheet, transforms=(25, 35))
        self.cut_sheet(image_sheet, 1, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.tiles_group = tiles_group

        self.upgrade_level = 1
        self.healt = spawner.DATA[self.upgrade_level - 1].get("health")
        speed = spawner.DATA[self.upgrade_level - 1].get("speed")
        self.vx, self.vy = -speed, speed

        self.trajectory = 0  # если trajectory кратна 2, то движемся по y, наоборот x

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        # self.cur_frame = (self.cur_frame + 1) % 2
        # self.image = self.frames[self.cur_frame]
        if self.healt <= 0:
            self.kill()

        if self.trajectory % 2 == 0:
            self.rect = self.rect.move(0, self.vy)
        else:
            self.rect = self.rect.move(self.vx, 0)
        if pygame.sprite.spritecollideany(self, self.tiles_group):
            self.rotate()

    def rotate(self):
        if self.trajectory % 2 == 0:
            self.rect = self.rect.move(self.vx * (50 // abs(self.vx)), self.vy * -(10 // abs(self.vy)))
            if pygame.sprite.spritecollideany(self, self.tiles_group):
                self.vx *= -1
                self.rect = self.rect.move(self.vx * (50 // abs(self.vx)), 0)
            else:
                self.rect = self.rect.move(-self.vx * (50 // abs(self.vx)), 0)
        else:
            self.rect = self.rect.move(self.vx * -(10 // abs(self.vy)), self.vy * (50 // abs(self.vy)))
            if pygame.sprite.spritecollideany(self, self.tiles_group):
                self.vy *= -1
                self.rect = self.rect.move(0, self.vy * (50 // abs(self.vy)))
            else:
                self.rect = self.rect.move(0, -self.vy * (50 // abs(self.vy)))
        self.trajectory += 1
