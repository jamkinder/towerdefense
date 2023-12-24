import pygame
from scripts import turrets as t
from scripts import constants as const
from scripts import visual

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)

FPS = const.FPS

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

all_sprites, tiles_group = visual.generate_visual()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # при закрытии окна
            running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = event.pos
            # определяем, можно ли там поставить турель
            if visual.load_level('map.txt')[y // const.TILE_SIZE][x // const.TILE_SIZE] == 'p':
                # ровно ставим турель
                turret = t.Turret(x // const.TILE_SIZE * const.TILE_SIZE, y // const.TILE_SIZE * const.TILE_SIZE,
                                  'archer_level_1.png')
                tiles_group.add(turret)
        # отрисовка и изменение свойств объектов
        screen.fill('Black')

        tiles_group.draw(screen)
        all_sprites.update(event)

        # обновление экрана
        pygame.display.flip()
        pygame.display.update()
pygame.quit()
