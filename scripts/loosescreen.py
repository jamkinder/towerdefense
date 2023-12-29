import pygame
import sys
import os
clock = pygame.time.Clock()
pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
thislevel = []
restart = False
FPS = 50
def load_image(name, colorkey=None, transforms=None):
    fullname = os.path.join('data/im', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    if transforms:
        image = pygame.transform.scale(image, transforms)
    return image


def terminate():
    pygame.quit()
    sys.exit()



def start_screen():
    intro_text = ["                  Press any button to start game"]

    fon = pygame.transform.scale(load_image('losescreen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 450
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                global restart
                restart = True
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)