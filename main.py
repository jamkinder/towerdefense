import pygame
from scripts import turrets as t
from scripts import constants as const
from scripts import visual
from scripts import enemycontrols

money = const.MONEY


def create_turret(x, y):
    # определяем, можно ли там поставить турель
    if visual.load_level('map.txt')[y // const.TILE_SIZE][x // const.TILE_SIZE] == 'p':
        # проверяем нет ли там уже турели
        space_is_free = True
        for turret in turret_group:
            if (x // const.TILE_SIZE * const.TILE_SIZE, y // const.TILE_SIZE * const.TILE_SIZE) == (
                    turret.rect.x, turret.rect.y):
                space_is_free = False
        # есть свободное место или его нет
        return space_is_free
    return False


def select_turret(x, y):
    for turret in turret_group:
        if (x // const.TILE_SIZE * const.TILE_SIZE, y // const.TILE_SIZE * const.TILE_SIZE) == (
                turret.rect.x, turret.rect.y):
            if turret.selected:
                return None
            return turret


def clear_selected_turret():
    for turret in turret_group:
        turret.selected = False


pygame.init()
size = WIDTH, HEIGHT = const.SCREEN_WIDTH, const.SCREEN_HEIGHT
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
FPS = const.FPS

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
all_sprites, tiles_group, turret_group = visual.generate_visual()

update_time = pygame.time.get_ticks()

for i in range(0, -10 * const.TILE_SIZE, -const.TILE_SIZE):
    enemy = enemycontrols.Enemy(360, i, 'mar.png', tiles_group,visual.castle_group)
    enemy_group.add(enemy)
    all_sprites.add(enemy)

selected_turret = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # при закрытии окна
            running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = event.pos
            if create_turret(x, y) and visual.can_place_turr and (money - const.BUY_COST) >= 0:
                # ровно ставим турель
                const.MONEY -= const.BUY_COST
                new_turret = t.Turret(x // const.TILE_SIZE * const.TILE_SIZE,
                                      y // const.TILE_SIZE * const.TILE_SIZE,
                                      visual.load_image('archer_level_1.png', colorkey=(0, 0, 0),
                                                        transforms=(const.TILE_SIZE, const.TILE_SIZE)))
                turret_group.add(new_turret)
                all_sprites.add(new_turret)
            else:  # показываем радиус
                selected_turret = select_turret(x, y)

    # отрисовка и изменение свойств объектов
    screen.fill('Black')

    # tiles_group.draw(screen)
    all_sprites.draw(screen)
    #visual.castle_group.draw(screen)
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
    visual.shop_btn.draw()
    if visual.clicked:
        visual.buytowerbutton.draw()
        visual.exit_btn.draw()
    if visual.can_place_turr:
        visual.cancelbutton.draw()
    visual.img = visual.font.render(str(money), True, 'gray')
    visual.imgcastle = visual.font2.render(str(visual.castle.hp), True, 'red')
    visual.screen.blit(visual.img,(100,15))
    visual.screen.blit(visual.imgcastle, (460, 425))
    money = const.MONEY
    pygame.display.flip()
    pygame.display.update()

    clock.tick(FPS)
pygame.quit()