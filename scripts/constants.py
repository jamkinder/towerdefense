ROWS = 10
COLS = 10
TILE_SIZE = 50
SIDE_PANEL = 300
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS
FPS = 60
HEALTH = 100
MONEY = 500
TOTAL_LEVELS = 15

# константа enemy
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
        'damage': 5,
        "range": 100,
        "cooldown": 1500,
        'cost': 200,
    },
    {
        # 2 level
        'im': 'archer_level_2.png',
        'damage': 6.5,
        "range": 110,
        "cooldown": 1200,
        'cost': 300
    },
    {
        # 3 level
        'im': 'archer_level_3.png',
        'damage': 8,
        "range": 120,
        "cooldown": 900,
        'cost': 500
    },
    {
        # 4 level
        'im': 'archer_level_1.png',
        'damage': 9.5,
        "range": 130,
        "cooldown": 600,
        'cost': 600
    },
    {
        # 5 level
        'im': 'archer_level_2.png',
        'damage': 11,
        "range": 140,
        "cooldown": 300,
        'cost': '-'
    }]
}
