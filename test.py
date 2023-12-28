for i in range(0, -sum(enemydata.WAVES.get(str(1))) // 2 * const.TILE_SIZE, -const.TILE_SIZE):
    enemy = enemycontrols.Enemy(360, i, visual.load_image("enemies\S_walk_Blue.png", transforms=(320, 50)), 6, 1,
                                tiles_group, visual.castle_group, 2, visual.load_image('mar.png'))
    enemy_group.add(enemy)
    all_sprites.add(enemy)




if totalwave % 10 == 0:

    enemy = enemycontrols.Enemy(360, 1, visual.load_image("enemies\S_Walk.png", transforms=(320, 50)), 6, 1,
                                tiles_group, visual.castle_group, 3, visual.load_image('mar.png'))