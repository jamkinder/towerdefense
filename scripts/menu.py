import pygame
from scripts import visual
from scripts import constants as const
from webbrowser import open


def menu(surface):
    # создаём рамку кнопок

    visual.music_fon_menu.play(-1)

    size_button = const.SIZE_BUTTON
    indent_x = 70
    kooficent_indent_y = 0.35

    image_button = visual.load_image('fon/cantbuy.png', transforms=size_button)
    # создаём фон
    fon = pygame.transform.scale(visual.load_image('fon/logo.png'), (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    # записываем текст кнопок
    text_button = [visual.font.render('Играть', 1, pygame.Color('black')),
                   visual.font.render('Выйти', 1, pygame.Color('black')),
                   visual.font_text.render('Справка', 1, pygame.Color('black'))]
    active_text_button = [visual.font_text.render('Играть', 1, pygame.Color('black')),
                          visual.font_text.render('Выйти', 1, pygame.Color('black')),
                          visual.font_text_min.render('Справка', 1, pygame.Color('black'))]

    hooked = False  # если навелись на кнопку
    # settingsmenu = False
    running = True
    while running:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                # если кликнули по кнопке начать, начинаем игру
                if ((const.SCREEN_WIDTH // 2 - indent_x <= x <= const.SCREEN_WIDTH // 2 - indent_x + size_button[0]
                     and const.SCREEN_HEIGHT // 2 <= y <= const.SCREEN_HEIGHT // 2 + size_button[1])):
                    visual.music_click.play()
                    return True
                # если кликнули по кнопке выйти, заканчиваем игру
                elif ((const.SCREEN_WIDTH // 2 - indent_x <= x <= const.SCREEN_WIDTH // 2 - indent_x + size_button[0]
                       and const.SCREEN_HEIGHT // 2 * (1 + kooficent_indent_y) <= y <= const.SCREEN_HEIGHT // 2 * (
                               1 + kooficent_indent_y) + size_button[1])):
                    return False
                # если кликнули по кнопке, то открываем меню настроек
                elif ((const.SCREEN_WIDTH // 2 - indent_x <= x <= const.SCREEN_WIDTH // 2 - indent_x + size_button[0]
                       and const.SCREEN_HEIGHT // 2 * (1 + kooficent_indent_y * 2) <= y <= const.SCREEN_HEIGHT // 2 * (
                               1 + kooficent_indent_y * 2) + size_button[1])):
                    open('https://github.com/jamkinder/towerdefense/blob/test/README.md')
                    # surface.fill('white')
                    # settingsmenu = True
                # elif (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                #       and (const.SCREEN_HEIGHT // 2 - 5) * 1.6 <= y <= (
                #               const.SCREEN_HEIGHT // 2 - 5) * 1.8 + 75) and settingsmenu:
                #     settingsmenu = False
                #     visual.music_fon_menu.stop()
                #     running = menu(surface)

        # показываем фон
        surface.blit(fon, (0, 0))
        # отдельная отрисовка меню настроек
        # if settingsmenu:
        #     surface.fill('white')
        #     myimage = pygame.image.load("data/im/guide/guide2.png")
        #     imagerect = myimage.get_rect()
        #     surface.blit(myimage, (0, 0, 400, 300))
        #     text_ = [visual.font.render('Back', 1, pygame.Color('black'))]
        #     for i in range(len(text_)):
        #         x, y = pygame.mouse.get_pos()
        #         surface.blit(image_button, (const.SCREEN_WIDTH // 2 - indent_x, 400 * (1 + i * 0.5)))
        #
        #         # если навелись на кнопку, то изменяем её размер
        #         if (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
        #                 and (const.SCREEN_HEIGHT // 1.25 - 1) <= y <= (const.SCREEN_HEIGHT // 2 - 20) + 255):
        #             surface.blit(text_[i],
        #                          (const.SCREEN_WIDTH // 2 - 30, const.SCREEN_WIDTH // 1.15 * (1 + i * 0.45) + 5))
        #
        #             if not hooked:
        #                 visual.music_hooked.play()
        #                 hooked = True
        #         else:
        #             surface.blit(text_[i], (const.SCREEN_WIDTH // 2 - 35, const.SCREEN_WIDTH // 1.2 * (1 + i * 0.45)))
        #
        #             if (not (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
        #                      and (const.SCREEN_HEIGHT // 2 - 20) <= y <= (const.SCREEN_HEIGHT // 2 - 20) + 75)):
        #                 hooked = False

        # показываем кнопки и все остальное
        # if not settingsmenu:
        for i in range(len(text_button)):
            x, y = pygame.mouse.get_pos()
            surface.blit(image_button,
                         (const.SCREEN_WIDTH // 2 - indent_x,
                          const.SCREEN_WIDTH // 2 * (1 + i * kooficent_indent_y)))

            # если навелись на кнопку, то изменяем её размер
            if (const.SCREEN_WIDTH // 2 - indent_x <= x <= const.SCREEN_WIDTH // 2 - indent_x + size_button[0]
                    and (const.SCREEN_HEIGHT // 2) * (1 + i * kooficent_indent_y) <= y <= (
                            const.SCREEN_HEIGHT // 2) * (1 + i * kooficent_indent_y) + size_button[1]):
                surface.blit(active_text_button[i],
                             (const.SCREEN_WIDTH // 2 - indent_x // 2 + 5,
                              (const.SCREEN_HEIGHT // 2 + 15) * (1 + i * kooficent_indent_y)))

                if not hooked:
                    visual.music_hooked.play()
                    hooked = True
            else:
                surface.blit(text_button[i],
                             (const.SCREEN_WIDTH // 2 - indent_x // 2,
                              (const.SCREEN_HEIGHT // 2 + 10) * (1 + i * kooficent_indent_y)))

                if not (const.SCREEN_WIDTH // 2 - indent_x <= x <= const.SCREEN_WIDTH // 2 - indent_x + size_button[
                    0] and
                        (((const.SCREEN_HEIGHT // 2) * 1 + kooficent_indent_y <= y <= (
                                const.SCREEN_HEIGHT // 2) * 1 + size_button[1]) or
                         ((const.SCREEN_HEIGHT // 2) * 1 + kooficent_indent_y <= y <= (
                                 const.SCREEN_HEIGHT // 2) * (1 + kooficent_indent_y) + kooficent_indent_y +
                          size_button[1]) or
                         ((const.SCREEN_HEIGHT // 2) * 1 + kooficent_indent_y <= y <= (
                                 const.SCREEN_HEIGHT // 2) * (1 + kooficent_indent_y * 2) + size_button[1]))):
                    hooked = False
        pygame.display.flip()
