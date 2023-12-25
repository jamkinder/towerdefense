import pygame
from scripts import turrets as t
from scripts import constants as const
from scripts import visual
from scripts import enemycontrols

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
FPS = const.FPS

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

all_sprites, tiles_group, turret_group = visual.generate_visual()

enemy = enemycontrols.Enemy(360, 0, 'mar.png', tiles_group)

enemy_group.add(enemy)
all_sprites.add(enemy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # при закрытии окна
            running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = event.pos
            # определяем, можно ли там поставить турель
            if visual.load_level('map.txt')[y // const.TILE_SIZE][x // const.TILE_SIZE] == 'p':
                # проверяем нет ли там уже турели
                space_is_free = True
                for turret in turret_group:
                    if (x // const.TILE_SIZE * const.TILE_SIZE, y // const.TILE_SIZE * const.TILE_SIZE) == (
                            turret.rect.x, turret.rect.y):
                        space_is_free = False
                # если есть свободное место
                if space_is_free:
                    # ровно ставим турель
                    new_turret = t.Turret(x // const.TILE_SIZE * const.TILE_SIZE,
                                          y // const.TILE_SIZE * const.TILE_SIZE,
                                          visual.load_image('archer_level_1.png',
                                                            transforms=(const.TILE_SIZE, const.TILE_SIZE)))
                    turret_group.add(new_turret)
                    all_sprites.add(new_turret)
    # отрисовка и изменение свойств объектов
    screen.fill('Black')

    # tiles_group.draw(screen)
    all_sprites.draw(screen)
    enemy_group.update()
# обновление экрана
    pygame.display.flip()
    pygame.display.update()

    clock.tick(FPS)
pygame.quit()
