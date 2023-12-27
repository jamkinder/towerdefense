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

# константа turret
TURRET_LEVELS = 4
BUY_COST = 200
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
        'im': 'archer_level_1.png',
        'damage': 20,
        "range": 150,
        "cooldown": 1000,
        'cost': 100,
    },
    {
        # 2 level
        'im': 'archer_level_2.png',
        'damage': 40,
        "range": 170,
        "cooldown": 800,
        'cost': 250
    },
    {
        # 3 level
        'im': 'archer_level_3.png',
        'damage': 60,
        "range": 200,
        "cooldown": 900,
        'cost': 400
    },
    {
        # 4 level
        'im': 'archer_level_4.png',
        'damage': 65,
        "range": 210,
        "cooldown": 600,
        'cost': 600
    },
    {
        # 5 level
        'im': 'archer_level_5.png',
        'damage': 70,
        "range": 210,
        "cooldown": 300,
        'cost': 800
    }]
}