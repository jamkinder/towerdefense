import pygame
from scripts import turrets as t
from scripts import constants as const
from scripts import visual
from scripts import enemycontrols
from scripts import enemyspawnerData
from scripts import menu


def create_turret(x_pos, y_pos):
    # определяем, можно ли там поставить турель
    for places in place_group:
        if places.rect.collidepoint((x_pos, y_pos)):
            # проверяем нет ли там уже турели
            space_is_free = True
            for tower in turret_group:
                if (x_pos // const.TILE_SIZE * const.TILE_SIZE, y_pos // const.TILE_SIZE * const.TILE_SIZE) == (
                        tower.rect.x, tower.rect.y):
                    space_is_free = False
            # есть свободное место или его нет
            return space_is_free
    return False


def select_turret(x_pos, y_pos):  # проверяет наличие турели на клетке
    for tower in turret_group:
        if tower.rect.collidepoint((x_pos, y_pos)):
            if tower.selected:
                return None
            return tower


def clear_selected_turret():  # скрывает все радиусы башен
    for tower in turret_group:
        tower.selected = False


def spawn_enemyes():  # функция спавна врагов
    for i in range(0, -sum(enemyspawnerData.WAVES.get(str(1))) * const.TILE_SIZE, -const.TILE_SIZE):
        enemys = enemycontrols.Enemy(360 - camera.coord, i,
                                     visual.load_image(r"enemies\s_walk.png", transforms=(320, 50)), 6, 1,
                                     tiles_group, visual.castle_group, 1, visual.load_image('mar.png').get_rect())
        enemy_group.add(enemys)
        all_sprites.add(enemys)

    for j in range(20, -sum(enemyspawnerData.WAVES.get(str(1))) // 2 * const.TILE_SIZE, -const.TILE_SIZE):
        enemys = enemycontrols.Enemy(360 - camera.coord, j,
                                     visual.load_image(r"enemies\s_walk_blue.png", transforms=(300, 50)), 6, 1,
                                     tiles_group, visual.castle_group, 2, visual.load_image('mar.png').get_rect())
        enemy_group.add(enemys)
        all_sprites.add(enemys)


def new_wave(totalwav):  # создаёт новую волну
    enemyspawnerData.WAVES.update(
        {str(1): [round(enemyspawnerData.WAVES.get(str(1))[0] * 1.5),
                  round(enemyspawnerData.WAVES.get(str(1))[1] * 1.5)]})
    const.total_wave = totalwav
    const.enemies_alive = sum(enemyspawnerData.WAVES.get('1'))
    spawn_enemyes()


def show_store():  # показывает магазин
    screen.blit(visual.shop_menu_image, (0, 0))

    visual.button_sprites = pygame.sprite.Group()

    iteration = 0
    for tower in const.TURRER:
        screen.blit(visual.load_image(const.TURRER[tower][0].get('im'), transforms=(50, 50)),
                    (15, 60 + 65 * iteration))
        visual.Button(83, 60 + 60 * iteration, visual.buy_tower_image, 1, 'buy', products=tower)
        iteration += 1
    visual.Button(visual.tile_width * 4 + 8, 60 + 60 * iteration, visual.exit_image, 1, 'exit')

    iteration = 0
    for hints in const.HINTS:
        screen.blit(visual.load_image(hints, transforms=(97, 60)),
                    (190, 50 + 65 * iteration))
        iteration += 1


def start_game():  # начало игры
    all_g, tiles_g, turret_g, place_g = visual.generate_visual()
    const.MONEY = 600
    camera.coord = 0
    enemyspawnerData.WAVES = {'1': [1, 0]}
    return all_g, tiles_g, turret_g, place_g, pygame.sprite.Group(), 0, -1, 20


pygame.init()
size = WIDTH, HEIGHT = const.SCREEN_WIDTH, const.SCREEN_HEIGHT
screen = pygame.display.set_mode(size)

camera = visual.Camera(15)

running = menu.menu(screen)

clock = pygame.time.Clock()
FPS = const.FPS
counter = 30
timer_event = pygame.USEREVENT+1
if running:
    all_sprites, tiles_group, turret_group, place_group, \
        enemy_group, totalwave, time_the_next_wave, pluscoof = start_game()

selected_turret = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # при закрытии окна
            running = False

        # ----------------------------
        #           Клики
        # ----------------------------
        elif event.type == timer_event:
            counter -= 1
            print(counter)
            if counter == 0:
                print('1')
                pygame.time.set_timer(timer_event, 0)
                for elem in const.TURRER:
                    for j in const.TURRER.get(elem):
                        if j.get('damage') != None:
                            print(j['damage'], 'before')
                            j['damage'] /= 1.5
                            print(j['damage'], 'affter')

        if event.type == pygame.MOUSEBUTTONUP and not visual.flag_pause:
            x, y = event.pos

            # Смотрим если кликнули по магазину
            if not create_turret(x, y) and visual.product == 'alpha' and const.MONEY - const.TURRER[visual.product][0].get('buy_cost') >= 0 and event.button == 1:
                not_turret = True
                if not_turret:
                    visual.button_sprites = pygame.sprite.Group()
                    visual.Button(0, 0, visual.shop_image, 1, 'shop')

                    const.MONEY -= const.TURRER[visual.product][0].get('buy_cost')
                    visual.product = None
            if (not create_turret(x, y) and visual.product == 'axe'
                    and const.MONEY - const.TURRER[visual.product][0].get('buy_cost') >= 0 and event.button == 1):

                # покупка топора
                not_turret = True

                # проверяем можно ли там поставить зону для турелей
                for sprite in visual.dirt_group:
                    if sprite.rect.collidepoint((x, y)):
                        not_turret = False
                if visual.castle.rect.collidepoint((x - 25, y)):
                    not_turret = False
                if (x <= const.TILE_SIZE * 3 and y >= const.TILE_SIZE * 9) or (
                        x <= const.TILE_SIZE * 2 and y <= const.TILE_SIZE):
                    not_turret = False

                if not_turret:
                    visual.button_sprites = pygame.sprite.Group()
                    visual.Button(0, 0, visual.shop_image, 1, 'shop')

                    const.MONEY -= const.TURRER[visual.product][0].get('buy_cost')
                    visual.product = None

                    # проверяем стоит ли там турель, если да, то удаляем её
                    for towers in turret_group:
                        if towers.rect.collidepoint((x, y)):
                            towers.kill()
                            not_turret = False

                    # ставим зону для турелей
                    if not_turret:
                        place = visual.Tile('gun', x // const.TILE_SIZE,
                                            y // const.TILE_SIZE, place_group, all_sprites)

            # покупка турели
            elif create_turret(x, y) and visual.product and visual.product != 'axe' and visual.product != 'alpha' and const.MONEY - \
                    const.TURRER[visual.product][0].get(
                        'buy_cost') >= 0 and event.button == 1:
                visual.button_sprites = pygame.sprite.Group()
                visual.Button(0, 0, visual.shop_image, 1, 'shop')
                const.MONEY -= const.TURRER[visual.product][0].get('buy_cost')

                # ровно ставим турель
                if visual.product == 'slowing':
                    new_turret = t.Darkturret(x // const.TILE_SIZE * const.TILE_SIZE,
                                              y // const.TILE_SIZE * const.TILE_SIZE,
                                              visual.product)
                else:
                    new_turret = t.Turret(x // const.TILE_SIZE * const.TILE_SIZE,
                                          y // const.TILE_SIZE * const.TILE_SIZE,
                                          visual.product)

                # добавляем турель в группу
                turret_group.add(new_turret)
                all_sprites.add(new_turret)

                visual.product = None

            # Если кликнули по башне, показываем радиус
            else:
                selected_turret = select_turret(x, y)
                if event.button == 3 and selected_turret:
                    selected_turret.upgrade()
                    selected_turret = None

            visual.button_sprites.update()

        # отслеживание кликов в паузе
        if event.type == pygame.MOUSEBUTTONUP and visual.flag_pause:
            x, y = event.pos
            if 160 <= x <= 360 and 275 <= y <= 350:
                visual.music_click.play()
                visual.flag_pause = False
                running = menu.menu(screen)
                if running:
                    (all_sprites, tiles_group, turret_group,
                     place_group, enemy_group, totalwave, time_the_next_wave, pluscoof) = start_game()
                if visual.losed:
                    visual.losed = False

        # ----------------------------
        #      Кнопки клавиатуры
        # ----------------------------

        if event.type == pygame.KEYDOWN:

            # Чит на деньги

            if event.key == pygame.K_UP and event.mod & pygame.KMOD_SHIFT and not visual.flag_pause:
                const.MONEY += 1000

            # Рестарт

            elif event.key == pygame.K_DOWN and not visual.flag_pause and visual.losed:
                running = menu.menu(screen)
                if running:
                    (all_sprites, tiles_group, turret_group,
                     place_group, enemy_group, totalwave, time_the_next_wave, pluscoof) = start_game()
                if visual.losed:
                    visual.losed = False

            # Движение камеры

            elif event.key == pygame.K_LEFT and not visual.flag_pause:
                if 0 <= camera.coord - const.TILE_SIZE <= camera.field_size_x:
                    visual.castle.rect.x += const.TILE_SIZE
                    camera.coord -= const.TILE_SIZE
                    for sprite in all_sprites:
                        camera.apply(sprite, 1)
                    for turret in turret_group:
                        turret.range_rect.x += 50
                        for missile in turret.missile_group:
                            missile.rect.x += 50

            elif event.key == pygame.K_RIGHT and not visual.flag_pause:
                if 0 <= camera.coord + const.TILE_SIZE <= camera.field_size_x:
                    visual.castle.rect.x -= const.TILE_SIZE
                    camera.coord += const.TILE_SIZE
                    for sprite in all_sprites:
                        camera.apply(sprite, -1)
                    for turret in turret_group:
                        turret.range_rect.x -= 50
                        for missile in turret.missile_group:
                            missile.rect.x -= 50

            # Пауза

            elif event.key == pygame.K_ESCAPE:
                # меняем флаг паузы на противоположный
                visual.flag_pause = not visual.flag_pause
                # создаём меню паузы
                screen.blit(visual.pause_image, (0, 0))
                screen.blit(visual.pause_text,
                            (const.SCREEN_WIDTH // 2 - const.TILE_SIZE, const.SCREEN_HEIGHT // 2 - const.TILE_SIZE))
                screen.blit(visual.load_image('fon/cantbuy.png', transforms=(200, 75)), (160, 275))
                screen.blit(visual.font_min.render('Выйти в меню', 1, pygame.Color('black')), (190, 300))

    # если сейчас не пауза
    if not visual.flag_pause:
        # отрисовка объектов
        screen.fill('Black')
        all_sprites.draw(screen)
        place_group.draw(screen)
        # скроем диапазоны каждой башни
        clear_selected_turret()

        if selected_turret:
            # показываем диапазон
            selected_turret.selected = True

        # показываем башни
        for turrets in turret_group:
            turrets.draw(screen)

        # обновляем врагов и башни
        enemy_group.update()
        turret_group.update(enemy_group, screen)

        # обновление экрана
        if visual.clicked:
            show_store()

        # если пользователь выбрал товар, рисуем его около курсора
        if visual.product:
            if visual.product == 'alpha':
                visual.button_sprites = pygame.sprite.Group()
                visual.Button(0, 0, visual.shop_image, 1, 'shop')

                const.MONEY -= const.TURRER[visual.product][0].get('buy_cost')

                visual.product = None
                for elem in const.TURRER:
                    for j in const.TURRER.get(elem):
                        if j.get('damage') != None:
                            print(j['damage'],'before')
                            j['damage'] *= 1.5
                            print(j['damage'],'affter')
                pygame.time.set_timer(timer_event, 1000)
            mouse_pos = pygame.mouse.get_pos()
            if visual.product:
                screen.blit(visual.load_image(const.TURRER[visual.product][0].get('im'), transforms=(50, 50)),
                            (mouse_pos[0] - const.TILE_SIZE // 2, mouse_pos[1] - const.TILE_SIZE // 2))

        # показываем кнопки
        visual.button_sprites.draw(screen)

        # создаём отображение волны, денег, и здоровья главной башни
        visual.img = visual.font.render('Money: ' + str(const.MONEY), True, (255, 36, 0))
        visual.imgcastle = visual.font.render(str(visual.castle.hp), True, (203, 40, 33))
        visual.wavetext = visual.font_min.render('ВОЛНА: ' + str(totalwave), True, (203, 40, 33))

        # показываем волну, деньги, и здоровье главной башни
        screen.blit(visual.load_image('fon/cantbuy.png', transforms=(170, const.TILE_SIZE)),
                    (0, const.SCREEN_HEIGHT - const.TILE_SIZE))
        visual.screen.blit(visual.img, (105, 15))
        visual.screen.blit(visual.imgcastle,
                           (visual.castle.rect.x + const.TILE_SIZE // 1.5, visual.castle.rect.y - const.TILE_SIZE // 2))
        visual.screen.blit(visual.wavetext,
                           (33 - len(str(totalwave)) * 5, const.SCREEN_HEIGHT - const.TILE_SIZE // 1.4))

        # проверка на то, закончилась ли волна каким либо образом и если это так, то вызываем следующую волну.
        if len(enemy_group) == 0:
            # если time_the_next_wave содержит в себя время
            if time_the_next_wave:
                # получаем время, через сколько будет волна и выводим его
                str_time = round(2 - float(str(abs(time_the_next_wave - pygame.time.get_ticks()) / 1000)[:3]), 1)
                time = visual.font_time.render(f'Следующая волна через: {str_time}s', True, (0, 0, 0))
                screen.blit(time, (200, const.SCREEN_HEIGHT - 20))

                # елси прошло достаточно времени с предыдущей волны
                if (time_the_next_wave == -1 or pygame.time.get_ticks() - time_the_next_wave >=
                        const.TIME_UNTIL_THE_NEXT_WAVE):
                    time_the_next_wave = None

                    totalwave += 1

                    if totalwave % 2 == 0:
                        enemyspawnerData.DATA[0].update({'health': enemyspawnerData.DATA[0].get('health') + pluscoof})
                        enemyspawnerData.DATA[1].update({'health': enemyspawnerData.DATA[1].get('health') + pluscoof})

                    if totalwave % 10 == 0:
                        enemy = enemycontrols.Enemy(360, 5,
                                                    visual.load_image(r"enemies\s_walk.png", transforms=(320, 50)),
                                                    6, 1,
                                                    tiles_group, visual.castle_group, 3,
                                                    visual.load_image('mar.png').get_rect())
                        enemy_group.add(enemy)
                        all_sprites.add(enemy)
                        enemyspawnerData.WAVES.update(
                            {str(1): [
                                round(
                                    enemyspawnerData.WAVES.get(str(1))[0] / enemyspawnerData.WAVES.get(str(1))[0]) + 1,
                                round(enemyspawnerData.WAVES.get(str(1))[1] * 0)]})
                    if totalwave % 15 == 0:
                        pluscoof *= 5
                    new_wave(totalwave)
            else:
                time_the_next_wave = pygame.time.get_ticks()

        if visual.losed:
            visual.lose_screen()

    # обновляем экран
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()