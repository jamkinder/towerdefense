import pygame
from scripts import visual
from scripts import constants as const


def menu(surface):
    image_button = visual.load_image('fon/cantbuy.png', transforms=(150, 75))
    fon = pygame.transform.scale(visual.load_image('fon/logo.png'), (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    text_button = [visual.font.render('Играть', 1, pygame.Color('black')),
                   visual.font.render('Выйти', 1, pygame.Color('black'))]
    active_text_button = [visual.font_min.render('Играть', 1, pygame.Color('black')),
                          visual.font_min.render('Выйти', 1, pygame.Color('black'))]
    hooked = False

    running = True
    while running:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if 180 <= x <= 180 + 150 and 230 <= y <= 305:
                    visual.music_click.play()
                    return True
                elif 180 <= x <= 180 + 150 and 230 * 1.5 <= y <= 305 * 1.5:
                    return False
        surface.blit(fon, (0, 0))

        for i in range(len(text_button)):
            x, y = pygame.mouse.get_pos()
            surface.blit(image_button, (180, 230 * (1 + i * 0.5)))
            if 180 <= x <= 180 + 150 and 230 * (1 + i * 0.5) <= y <= 305 * (1 + i * 0.5):
                surface.blit(active_text_button[i], (215 + 5, 250 * (1 + i * 0.45) + 5))
                if not hooked:
                    visual.music_hooked.play()
                    hooked = True
            else:
                surface.blit(text_button[i], (215, 250 * (1 + i * 0.45)))
                if not (180 <= x <= 180 + 150 and 230 <= y <= 305) and not (
                        180 <= x <= 180 + 150 and 230 * 1.5 <= y <= 305 * 1.5):
                    hooked = False
        pygame.display.flip()
