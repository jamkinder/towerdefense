ROWS = 10
COLS = 10
TILE_SIZE = 50
SIDE_PANEL = 300
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS
FPS = 30
HEALTH = 100
MONEY = 500
TOTAL_LEVELS = 15

# константа enemy
TIME_UNTIL_THE_NEXT_WAVE = 2000  # 5 секунд
SPAWN_COOLDOWN = 400
ANIM_ENEMY = 50

# константа turret
TURRET_LEVELS = 4
KILL_REWARD = 25
LEVEL_COMPLETE_REWARD = 100
ANIMATION_STEPS = 8
ANIMATION_DELAY = 100
total_wave = 1
enemies_alive = 4

# характеристики уровней turret
TURRER = {'usual': [
    {
        # 1 level
        'im': 'blue_turret/archer_level_1.png',
        'damage': 20,
        "range": 110,
        "cooldown": 1000,
        'cost': 300,
        'buy_cost': 200
    },
    {
        # 2 level
        'im': 'blue_turret/archer_level_2.png',
        'damage': 40,
        "range": 125,
        "cooldown": 900,
        'cost': 400
    },
    {
        # 3 level
        'im': 'blue_turret/archer_level_3.png',
        'damage': 60,
        "range": 150,
        "cooldown": 800,
        'cost': 500
    },
    {
        # 4 level
        'im': 'blue_turret/archer_level_4.png',
        'damage': 65,
        "range": 165,
        "cooldown": 700,
        'cost': 600
    },
    {
        # 5 level
        'im': 'blue_turret/archer_level_5.png',
        'damage': 70,
        "range": 180,
        "cooldown": 600,
        'cost': 800
    }],
    'green': [  # башня с большой скоростью
        {
            # 1 level
            'im': 'green_turret/archer_level_1_green.png',
            'damage': 20,
            "range": 80,
            "cooldown": 600,
            'cost': 400,
            'buy_cost': 300
        },
        {
            # 2 level
            'im': 'green_turret/archer_level_2_green.png',
            'damage': 20,
            "range": 90,
            "cooldown": 500,
            'cost': 600
        },
        {
            # 3 level
            'im': 'green_turret/archer_level_3_green.png',
            'damage': 25,
            "range": 100,
            "cooldown": 400,
            'cost': 700
        },
        {
            # 4 level
            'im': 'green_turret/archer_level_4_green.png',
            'damage': 30,
            "range": 110,
            "cooldown": 300,
            'cost': 700
        },
        {
            # 5 level
            'im': 'green_turret/archer_level_5_green.png',
            'damage': 35,
            "range": 120,
            "cooldown": 200,
            'cost': 800
        }],
    'red': [   # башня с большим уроном
        {
            # 1 level
            'im': 'red_turret/archer_level_1_red.png',
            'damage': 100,
            "range": 120,
            "cooldown": 7000,
            'cost': 600,
            'buy_cost': 400
        },
        {
            # 2 level
            'im': 'red_turret/archer_level_2_red.png',
            'damage': 150,
            "range": 140,
            "cooldown": 6000,
            'cost': 800
        },
        {
            # 3 level
            'im': 'red_turret/archer_level_3_red.png',
            'damage': 200,
            "range": 160,
            "cooldown": 5000,
            'cost': 1000
        },
        {
            # 4 level
            'im': 'red_turret/archer_level_4_red.png',
            'damage': 250,
            "range": 180,
            "cooldown": 4000,
            'cost': 1250
        },
        {
            # 5 level
            'im': 'red_turret/archer_level_5_red.png',
            'damage': 315,
            "range": 200,
            "cooldown": 3000,
            'cost': 1500
        }],
    'slowing': [  # башня, которая поглашает врагов
        {
            # 1 level
            'im': 'slowing_turret/archer_level_1_black.png',
            'damage': 100 ** 100,
            "range": 75,
            "cooldown": 20000,
            'cost': 100,
            'buy_cost': 500
        },
        {
            # 2 level
            'im': 'slowing_turret/archer_level_2_black.png',
            "cooldown": 15000,
            'cost': 250
        },
        {
            # 3 level
            'im': 'slowing_turret/archer_level_3_black.png',
            "cooldown": 10000,
            'cost': 400
        }],
    'axe': [{'im': 'axe.png',
             'buy_cost': 100}]
}

HINTS = ['hints/defaulttower.png',
         'hints/green1tower.png',
         'hints/redtower1.png',
         'hints/blacktower1.png']