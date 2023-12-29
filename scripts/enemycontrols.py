import pygame
from scripts import visual
from scripts import enemyspawnerData as spawner
from scripts import constants as const


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, columns, rows, tiles_group, castle_group, lvl, rect):
        self.font = pygame.font.SysFont(None, 24)
        self.healt_img = self.font.render('', True, 'BLUE')

        pygame.sprite.Sprite.__init__(self)
        self.frames = []

        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0

        self.image = self.frames[self.cur_frame]
        self.rect = rect
        self.rect.x = x
        self.rect.y = y

        self.castle = castle_group
        self.tiles_group = tiles_group

        self.upgrade_level = lvl

        self.healt = spawner.DATA[self.upgrade_level - 1].get("health")
        speed = spawner.DATA[self.upgrade_level - 1].get("speed")
        self.damage = spawner.DATA[self.upgrade_level - 1].get('damage')

        self.vx, self.vy = -speed, speed

        self.update_time = pygame.time.get_ticks()

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
        if self.healt <= 0:
            const.MONEY += const.KILL_REWARD
            self.kill()
        else:
            # показываем здоровье врагов
            self.healt_img = self.font.render(str(self.healt), True, 'red')
            visual.screen.blit(self.healt_img, (self.rect.x + 5, self.rect.y - 10))

        if self.trajectory % 2 == 0:
            self.rect = self.rect.move(0, self.vy)
        else:
            self.rect = self.rect.move(self.vx, 0)

        if pygame.time.get_ticks() - self.update_time > const.ANIM_ENEMY // abs(self.vx):
            self.update_time = pygame.time.get_ticks()

            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if pygame.sprite.spritecollideany(self, self.tiles_group):
            self.rotate()

    def rotate(self):
        if self.trajectory % 2 == 0:
            self.rect = self.rect.move(self.vx * (50 // abs(self.vx)), self.vy * -(5 // abs(self.vy)))
            if pygame.sprite.spritecollideany(self, self.tiles_group):
                self.vx *= -1
                self.rect = self.rect.move(self.vx * (50 // abs(self.vx)), 0)
            else:
                self.rect = self.rect.move(-self.vx * (50 // abs(self.vx)), 0)
        else:
            self.rect = self.rect.move(self.vx * -(5 // abs(self.vy)), self.vy * (50 // abs(self.vy)))
            if pygame.sprite.spritecollideany(self, self.tiles_group):
                self.vy *= -1
                self.rect = self.rect.move(0, self.vy * (50 // abs(self.vy)))
            else:
                self.rect = self.rect.move(0, -self.vy * (50 // abs(self.vy)))

        if pygame.sprite.spritecollideany(self, self.castle):
            visual.castle.take_damage(self.damage)
            self.kill()

        self.trajectory += 1