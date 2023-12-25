ROWS = 14
COLS = 14
TILE_SIZE = 50
SIDE_PANEL = 300
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS
FPS = 30
HEALTH = 100
MONEY = 650
TOTAL_LEVELS = 15

# константа enemy
SPAWN_COOLDOWN = 400
#test
# константа turret
TURRET_LEVELS = 4
BUY_COST = 200
UPGRADE_COST = 100
KILL_REWARD = 1
LEVEL_COMPLETE_REWARD = 100
ANIMATION_STEPS = 8
ANIMATION_DELAY = 15
DAMAGE = 5

# характеристики уровней turret
STATS = [
    {
        # 1 level
        "range": 70,
        "cooldown": 2000,
    },
    {
        # 2 level
        "range": 140,
        "cooldown": 1700,
    },
    {
        # 3 level
        "range": 190,
        "cooldown": 1500,
    },
    {
        # 4 level
        "range": 235,
        "cooldown": 1200,
    }
]


