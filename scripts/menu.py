import pygame
from scripts import visual
from scripts import constants as const

def menu(surface):

    # создаём рамку кнопок

    visual.music_fon_menu.play(-1)
    image_button = visual.load_image('fon/cantbuy.png', transforms=(150, 75))
    # создаём фон
    fon = pygame.transform.scale(visual.load_image('fon/logo.png'), (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    # записываем текст кнопок
    text_button = [visual.font.render('Играть', 1, pygame.Color('black')),
                   visual.font.render('Выйти', 1, pygame.Color('black')),
                   visual.font.render('Настройки', 1, pygame.Color('black'))]
    active_text_button = [visual.font_min.render('Играть', 1, pygame.Color('black')),
                          visual.font_min.render('Выйти', 1, pygame.Color('black')),
                          visual.font_min.render('Настройки ', 1, pygame.Color('black'))]

    hooked = False  # если навелись на кнопку
    settingsmenu = False
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
                        and const.SCREEN_HEIGHT // 2 - 35 <= y <= const.SCREEN_HEIGHT // 2 + 55) and settingsmenu == False:
                    visual.music_click.play()
                    return True
                # если кликнули по кнопке выйти, заканчиваем игру
                elif (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                      and (const.SCREEN_HEIGHT // 2 - 25) * 1.5 <= y <= (const.SCREEN_HEIGHT // 2 - 20) * 1.5 + 75) and settingsmenu == False:
                    return False
                # если кликнули по кнопке то открываем меню настроек
                elif (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                        and (const.SCREEN_HEIGHT // 2 - 5) * 1.8 <= y <= (const.SCREEN_HEIGHT // 2 - 5) * 1.8 + 75) and settingsmenu == False:
                    surface.fill('white')
                    settingsmenu = True
                elif (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                        and (const.SCREEN_HEIGHT // 2 - 5) * 1.6 <= y <= (
                                    const.SCREEN_HEIGHT // 2 - 5) * 1.8 + 75) and settingsmenu:
                    settingsmenu = False
                    visual.music_fon_menu.stop()
                    running = menu(surface)


        # показываем фон
        surface.blit(fon, (0, 0))
        # отдельная отрисовка меню настроек
        if settingsmenu:
            surface.fill('white')
            myimage = pygame.image.load("data/im/guide/guide2.png")
            imagerect = myimage.get_rect()
            surface.blit(myimage, (0,0,400,300))
            text_ = [visual.font.render('Back', 1, pygame.Color('black'))]
            for i in range(len(text_)):
                x, y = pygame.mouse.get_pos()
                surface.blit(image_button, (const.SCREEN_WIDTH // 2 - 70, 400 * (1 + i * 0.5)))

                # если навелись на кнопку, то изменяем её размер
                if (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                        and (const.SCREEN_HEIGHT // 1.25 - 1) <= y <= (const.SCREEN_HEIGHT // 2 - 20) + 255):
                    surface.blit(text_[i],
                                 (const.SCREEN_WIDTH // 2 - 30, const.SCREEN_WIDTH // 1.15 * (1 + i * 0.45) + 5))

                    if not hooked:
                        visual.music_hooked.play()
                        hooked = True
                else:
                    surface.blit(text_[i], (const.SCREEN_WIDTH // 2 - 35, const.SCREEN_WIDTH // 1.2 * (1 + i * 0.45)))

                    if (not (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                             and (const.SCREEN_HEIGHT // 2 - 20) <= y <= (const.SCREEN_HEIGHT // 2 - 20) + 75)):
                        hooked = False



        # показываем кнопки и все остальное
        if not settingsmenu:
            for i in range(len(text_button)):
                x, y = pygame.mouse.get_pos()
                surface.blit(image_button, (const.SCREEN_WIDTH // 2 - 70, 218 * (1 + i * 0.5)))

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
                    surface.blit(text_button[i], (const.SCREEN_WIDTH // 2 - 35, const.SCREEN_WIDTH // 2.1 * (1 + i * 0.45)))

                    if (not (const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150
                             and (const.SCREEN_HEIGHT // 2 - 20) <= y <= (const.SCREEN_HEIGHT // 2 - 20) + 75)
                            and not (
                                    const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150 and
                                    (const.SCREEN_HEIGHT // 2 - 20) * 1.5 <= y <= (
                                            const.SCREEN_HEIGHT // 2 - 20) * 1.5 + 75)\
                            and not (
                                    const.SCREEN_WIDTH // 2 - 70 <= x <= const.SCREEN_WIDTH // 2 - 70 + 150 and
                                    (const.SCREEN_HEIGHT // 2 - 10) * 1.8 <= y <= (
                                            const.SCREEN_HEIGHT // 2 - 10) * 1.8 + 75)):
                        hooked = False
        pygame.display.flip()