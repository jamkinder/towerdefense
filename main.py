import pygame
from scripts import turrets as t
from scripts import constants as const
from scripts import visual
from scripts import enemycontrols
from scripts import enemyspawnerData as enemydata

money = const.MONEY
totalwave = 0
time_the_next_wave = -1
pluscoof = 20


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


def select_turret(x_pos, y_pos):
    for tower in turret_group:
        if tower.rect.collidepoint((x_pos, y_pos)):
            if tower.selected:
                return None
            return tower


def clear_selected_turret():  # скрывает все радиусы башен
    for tower in turret_group:
        tower.selected = False


def spawn_enemyes():  # функция спавна врагов
    for i in range(0, -sum(enemydata.WAVES.get(str(1))) * const.TILE_SIZE, -const.TILE_SIZE):
        enemy = enemycontrols.Enemy(360, i, visual.load_image("enemies\S_Walk.png", transforms=(320, 50)), 6, 1,
                                    tiles_group, visual.castle_group, 1, visual.load_image('mar.png').get_rect())
        # enemy = enemycontrols.Enemy(360, i, 'mar.png', tiles_group, visual.castle_group, 1)
        enemy_group.add(enemy)
        all_sprites.add(enemy)

    for i in range(0, -sum(enemydata.WAVES.get(str(1))) // 2 * const.TILE_SIZE, -const.TILE_SIZE):
        enemy = enemycontrols.Enemy(360, i, visual.load_image("enemies\S_walk_Blue.png", transforms=(320, 50)), 6, 1,
                                    tiles_group, visual.castle_group, 1, visual.load_image('mar.png').get_rect())
        # enemy = enemycontrols.Enemy(360, i, 'mar.png', tiles_group, visual.castle_group, 1)
        enemy_group.add(enemy)
        all_sprites.add(enemy)


def new_wave(totalwav):  # создаёт новую волну
    totalwav += 1
    enemydata.WAVES.update(
        {str(1): [round(enemydata.WAVES.get(str(1))[0] * 1.5), round(enemydata.WAVES.get(str(1))[1] * 1.5)]})
    const.total_wave += totalwav
    const.enemies_alive = sum(enemydata.WAVES.get('1'))
    spawn_enemyes()


def show_store():  # показывает магазин
    screen.blit(visual.shop_menu_image, (0, 0))
    iteration = 0
    for tower in const.TURRER:
        screen.blit(visual.load_image(const.TURRER[tower][0].get('im'), transforms=(50, 50)),
                    (15, 60 + 60 * iteration))
        visual.Button(83, 60 + 60 * iteration, visual.buy_tower_image, 1, 'buy', products=tower)
        iteration += 1


pygame.init()
size = WIDTH, HEIGHT = const.SCREEN_WIDTH, const.SCREEN_HEIGHT
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
FPS = const.FPS

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
place_group = pygame.sprite.Group()
all_sprites, tiles_group, turret_group, place_group = visual.generate_visual()

update_time = pygame.time.get_ticks()

selected_turret = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # при закрытии окна
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos

            if not create_turret(x, y) and visual.product == 'axe' and const.MONEY - const.TURRER[visual.product][0].get(
                    'buy_cost') >= 0 and event.button == 1:

                visual.button_sprites = pygame.sprite.Group()
                visual.Button(0, 0, visual.shop_image, 1, 'shop')

                not_turret = True
                for towers in turret_group:
                    if towers.rect.collidepoint((x, y)):
                        towers.kill()
                        not_turret = False
                if not_turret:
                    place = visual.Tile('gun', x // const.TILE_SIZE,
                                        y // const.TILE_SIZE, place_group)

                const.MONEY -= const.TURRER[visual.product][0].get('buy_cost')
                visual.product = None

            elif create_turret(x, y) and visual.product and const.MONEY - const.TURRER[visual.product][0].get(
                    'buy_cost') >= 0 and event.button == 1:

                visual.button_sprites = pygame.sprite.Group()
                visual.Button(0, 0, visual.shop_image, 1, 'shop')
                const.MONEY -= const.TURRER[visual.product][0].get('buy_cost')

                if visual.product != 'axe':
                    # ровно ставим турель
                    new_turret = t.Turret(x // const.TILE_SIZE * const.TILE_SIZE,
                                          y // const.TILE_SIZE * const.TILE_SIZE,
                                          visual.product)
                    turret_group.add(new_turret)
                    all_sprites.add(new_turret)

                visual.product = None
            # показываем радиус
            else:
                selected_turret = select_turret(x, y)
                if event.button == 3 and selected_turret:
                    selected_turret.upgrade()
                    selected_turret = None

            visual.button_sprites.update()

        # чит на деньги
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                const.MONEY += 1000

    # отрисовка объектов
    screen.fill('Black')
    all_sprites.draw(screen)
    place_group.draw(screen)
    # скроем диапазоны каждой башни
    clear_selected_turret()

    if selected_turret:
        selected_turret.selected = True  # показываем диапазон
    # отрисовываем башни
    for turrets in turret_group:
        turrets.draw(screen)

    enemy_group.update()
    turret_group.update(enemy_group, screen)

    # обновление экрана
    if visual.clicked:
        show_store()

    # если пользователь выбрал товар, рисуем его около курсора
    if visual.product:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(visual.load_image(const.TURRER[visual.product][0].get('im'), transforms=(50, 50)),
                    (mouse_pos[0] - const.TILE_SIZE // 2, mouse_pos[1] - const.TILE_SIZE // 2))

    visual.button_sprites.draw(screen)

    visual.img = visual.font.render(str(const.MONEY), True, (255, 215, 0))
    visual.imgcastle = visual.font.render(str(visual.castle.hp), True, 'red')
    visual.wavetext = visual.font.render('ВОЛНА: ' + str(totalwave), True, 'red')

    visual.screen.blit(visual.img, (100, 15))
    visual.screen.blit(visual.imgcastle, (460, 425))
    visual.screen.blit(visual.wavetext, (WIDTH // 2.5, 10))

    # проверка на то, закончилась ли волна каким либо образом и если это так, то вызываем следующую волну.
    if len(enemy_group) == 0:
        # если time_the_next_wave содержит в себя время
        if time_the_next_wave:
            # получаем время, через сколько будет волна и выводим его
            str_time = round(2 - float(str(abs(time_the_next_wave - pygame.time.get_ticks()) / 1000)[:3]), 1)
            time = visual.font_time.render(f'Следующая волна через: {str_time}s', True, 'red')
            screen.blit(time, (200, const.SCREEN_HEIGHT - 20))

            # елси прошло достаточно времени с предыдущей волны
            if (time_the_next_wave == -1 or pygame.time.get_ticks() - time_the_next_wave >=
                    const.TIME_UNTIL_THE_NEXT_WAVE):
                time_the_next_wave = None

                totalwave += 1

                if totalwave % 2 == 0:
                    enemydata.DATA[0].update({'health': enemydata.DATA[0].get('health') + pluscoof})

                # if totalwave % 10 == 0:
                #     enemy = enemycontrols.Enemy(360, 1, visual.load_image("enemies\S_Walk.png", transforms=(320, 50)),
                #                                 6, 1,
                #                                 tiles_group, visual.castle_group, 3, visual.load_image('mar.png'))
                #     enemy_group.add(enemy)
                #     all_sprites.add(enemy)
                #     enemydata.WAVES.update(
                #         {str(1): [round(enemydata.WAVES.get(str(1))[0] / enemydata.WAVES.get(str(1))[0]) + 1,
                #                   round(enemydata.WAVES.get(str(1))[1] * 0)]})
                if totalwave % 15 == 0:
                    pluscoof *= 5
                new_wave(totalwave)
        else:
            time_the_next_wave = pygame.time.get_ticks()

    # screen.blit(visual.load_image('defaulttower.png', transforms=(130, 70)), (170, 120))
    # R

    pygame.display.flip()
    pygame.display.update()

    clock.tick(FPS)
pygame.quit()
