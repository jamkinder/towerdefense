import pygame
from scripts import visual
from scripts import enemyspawnerData
from scripts import constants as const


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, columns, rows, tiles_group, castle_group, lvl, rect):
        self.healt_img = visual.font_healt_enemy.render('', True, 'BLUE')

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

        self.healt = enemyspawnerData.DATA[self.upgrade_level - 1].get("health")
        speed = enemyspawnerData.DATA[self.upgrade_level - 1].get("speed")
        self.damage = enemyspawnerData.DATA[self.upgrade_level - 1].get('damage')

        self.vx, self.vy = -speed, speed

        self.update_time = pygame.time.get_ticks()

        # если trajectory кратна 2, то движемся по y, наоборот по x
        self.trajectory = 0

    def cut_sheet(self, sheet, columns, rows):
        # создание спрайт листа

        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        # если у enemy сняли все жизни
        if self.healt <= 0:
            death_sound = pygame.mixer.Sound('data/music/death.wav')
            const.MONEY += const.KILL_REWARD
            death_sound.play()
            self.kill()
        else:
            # показываем здоровье врагов
            self.healt_img = visual.font_healt_enemy.render(str(round(self.healt)), True, 'red')
            visual.screen.blit(self.healt_img, (self.rect.x + 5, self.rect.y - 10))

        # передвигаем enemy по заданной траектории
        if self.trajectory % 2 == 0:
            self.rect = self.rect.move(0, self.vy)
        else:
            self.rect = self.rect.move(self.vx, 0)

        # меняем кадр
        if pygame.time.get_ticks() - self.update_time > const.ANIM_ENEMY // abs(self.vx):
            self.update_time = pygame.time.get_ticks()

            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        # проверяем enemy на касание стенки

        # если enemy движется по x
        if self.trajectory % 2 != 0:
            # передвигаем enemy на 10 пикселей, если он касается стенки, меняем его траекторию
            self.rect = self.rect.move(10 * (self.vx // abs(self.vx)), 0)
            if pygame.sprite.spritecollideany(self, self.tiles_group):
                self.rotate()
            # передвигаем enemy обратно на 10 пикселей
            self.rect = self.rect.move(-10 * (self.vx // abs(self.vx)), 0)
        # если enemy движется по y
        else:
            if pygame.sprite.spritecollideany(self, self.tiles_group):
                self.rotate()

    def rotate(self):  # изменяет путь enemy

        # если коснулся главной башни
        if pygame.sprite.spritecollideany(self, self.castle):
            visual.castle.take_damage(self.damage)
            self.kill()

        if self.trajectory % 2 == 0:
            # передвигаем enemy на одну клетку по y
            self.rect = self.rect.move(self.vx * (const.TILE_SIZE // abs(self.vx)), self.vy * -(5 // abs(self.vy)))
            # если enemy коснулся клетки, то изменяем его скорость на противоположную
            if pygame.sprite.spritecollideany(self, self.tiles_group):
                self.vx *= -1
                # передвигаем enemy назад, на одну клетку
                self.rect = self.rect.move(self.vx * (const.TILE_SIZE // abs(self.vx)), 0)
            else:
                # передвигаем enemy назад, на одну клетку
                self.rect = self.rect.move(-self.vx * (const.TILE_SIZE // abs(self.vx)), 0)
        else:
            # передвигаем enemy на одну клетку по x
            self.rect = self.rect.move(self.vx * -(5 // abs(self.vy)), self.vy * (const.TILE_SIZE // abs(self.vy)))
            # если enemy коснулся клетки, то изменяем его скорость на противоположную
            if pygame.sprite.spritecollideany(self, self.tiles_group):
                self.vy *= -1
                # передвигаем enemy назад, на одну клетку
                self.rect = self.rect.move(0, self.vy * (const.TILE_SIZE // abs(self.vy)))
            else:
                # передвигаем enemy назад, на одну клетку
                self.rect = self.rect.move(0, -self.vy * (const.TILE_SIZE // abs(self.vy)))

        # меняем траекторию
        self.trajectory += 1
