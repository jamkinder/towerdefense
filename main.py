import pygame
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
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False

        # отрисовка и изменение свойств объектов
        screen.fill('Black')

        tiles_group.draw(screen)
        all_sprites.update(event)

        # обновление экрана
        pygame.display.flip()
        pygame.display.update()
pygame.quit()
