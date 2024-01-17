import pygame
from scripts import visual
from scripts import constants as const


def menu(surface):
    # создаём рамку кнопок
    image_button = visual.load_image('fon/cantbuy.png', transforms=(150, 75))
    # создаём фон
    fon = pygame.transform.scale(visual.load_image('fon/logo.png'), (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    # записываем текст кнопок
    text_button = [visual.font.render('Играть', 1, pygame.Color('black')),
                   visual.font.render('Выйти', 1, pygame.Color('black'))]
    active_text_button = [visual.font_min.render('Играть', 1, pygame.Color('black')),
                          visual.font_min.render('Выйти', 1, pygame.Color('black'))]

    hooked = False  # если навелись на кнопку

    running = True
    while running:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                # если кликнули по кнопке начать, начинаем игру
                if (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                        and const.SCREEN_HEIGHT // 2 - 20 <= y <= const.SCREEN_HEIGHT // 2 + 55):
                    visual.music_click.play()
                    return True
                # если кликнули по кнопке выйти, заканчиваем игру
                elif (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                      and (const.SCREEN_HEIGHT // 2 - 20) * 1.5 <= y <= (const.SCREEN_HEIGHT // 2 - 20) * 1.5 + 75):
                    return False
        # показываем фон
        surface.blit(fon, (0, 0))
        # показываем кнопки
        for i in range(len(text_button)):
            x, y = pygame.mouse.get_pos()
            surface.blit(image_button, (const.SCREEN_WIDTH // 2 - 70, 230 * (1 + i * 0.5)))

            # если навелись на кнопку, то изменяем её размер
            if (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                    and (const.SCREEN_HEIGHT // 2 - 20) * (1 + i * 0.5) <= y <= (
                            const.SCREEN_HEIGHT // 2 - 20) * (1 + i * 0.5) + 75):
                surface.blit(active_text_button[i],
                             (const.SCREEN_WIDTH // 2 - 30, const.SCREEN_WIDTH // 2 * (1 + i * 0.45) + 5))

                if not hooked:
                    visual.music_hooked.play()
                    hooked = True
            else:
                surface.blit(text_button[i], (const.SCREEN_WIDTH // 2 - 35, const.SCREEN_WIDTH // 2 * (1 + i * 0.45)))

                if (not (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                         and (const.SCREEN_HEIGHT // 2 - 20) <= y <= (const.SCREEN_HEIGHT // 2 - 20) + 75)
                        and not (
                                const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150 and
                                (const.SCREEN_HEIGHT // 2 - 20) * 1.5 <= y <= (
                                        const.SCREEN_HEIGHT // 2 - 20) * 1.5 + 75)):
                    hooked = False
        pygame.display.flip()
