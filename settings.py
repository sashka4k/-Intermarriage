import pygame

# Размеры карты
MAP_WIDTH = 1152   # 9 клеток × 128
MAP_HEIGHT = 896   # 7 клеток × 128
CELL_SIZE = 128

# Отступы карты от краёв экрана
MAP_MARGIN_TOP = 60
MAP_MARGIN_RIGHT = 40

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
DARK_GREEN = (30, 60, 30)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BLUE = (50, 100, 200)
LIGHT_BLUE = (100, 150, 250)
RED = (200, 50, 50)
PANEL_BG = (40, 40, 60, 200)  # с альфа-каналом

# Пути к файлам
BACKGROUND_IMAGE = "Prefabs/Pictures/main_menu.png"
MAP_WITHOUT_STEPS = "Prefabs/Pictures/ancient_map_without_steps.png"
MAP_STEPS = "Prefabs/Pictures/ancient_map_steps.png"



# Игроки
PLAYER_COUNT = 4
PLAYER_COLORS = [
    (50, 100, 200),   # синий
    (200, 50, 50),    # красный
    (50, 180, 50),    # зелёный
    (200, 180, 50),   # жёлтый
]

# Смещение жетонов игроков внутри клетки (относительно центра)
PLAYER_OFFSETS = [
    (-20, -20),  # верхний-левый
    (20, -20),   # верхний-правый
    (-20, 20),   # нижний-левый
    (20, 20),    # нижний-правый
]

BOARD_CELLS = {
    # Ряд 1 (нижний): y = 768
    0: {"name": "1 : 1", "type": "none", "x": 0, "y": 768, "PATH": [9]},
    1: {"name": "2 : 1", "type": "none", "x": 128, "y": 768, "PATH": [0]},
    2: {"name": "3 : 1", "type": "none", "x": 256, "y": 768, "PATH": [11]},
    3: {"name": "4 : 1", "type": "none", "x": 384, "y": 768, "PATH": [2]},
    4: {"name": "5 : 1", "type": "none", "x": 512, "y": 768, "PATH": [-1]},
    5: {"name": "6 : 1", "type": "none", "x": 640, "y": 768, "PATH": [13]},
    6: {"name": "7 : 1", "type": "none", "x": 768, "y": 768, "PATH": [5]},
    7: {"name": "8 : 1", "type": "none", "x": 896, "y": 768, "PATH": [-1]},
    8: {"name": "9 : 1", "type": "none", "x": 1024, "y": 768, "PATH": [-1]},
    # Ряд 2: y = 640
    9: {"name": "1 : 2", "type": "none", "x": 0, "y": 640, "PATH": [18]},
    10: {"name": "2 : 2", "type": "none", "x": 128, "y": 640, "PATH": [1]},
    11: {"name": "3 : 2", "type": "none", "x": 256, "y": 640, "PATH": [10]},
    12: {"name": "4 : 2", "type": "none", "x": 384, "y": 640, "PATH": [3]},
    13: {"name": "5 : 2", "type": "none", "x": 512, "y": 640, "PATH": [12]},
    14: {"name": "6 : 2", "type": "none", "x": 640, "y": 640, "PATH": [6]},
    15: {"name": "7 : 2", "type": "none", "x": 768, "y": 640, "PATH": [14]},
    16: {"name": "8 : 2", "type": "none", "x": 896, "y": 640, "PATH": [24]},
    17: {"name": "9 : 2", "type": "none", "x": 1024, "y": 640, "PATH": [-1]},
    # Ряд 3: y = 512
    18: {"name": "1 : 3", "type": "none", "x": 0, "y": 512, "PATH": [19]},
    19: {"name": "2 : 3", "type": "none", "x": 128, "y": 512, "PATH": [20]},
    20: {"name": "3 : 3", "type": "none", "x": 256, "y": 512, "PATH": [21]},
    21: {"name": "4 : 3", "type": "none", "x": 384, "y": 512, "PATH": [30]},
    22: {"name": "5 : 3", "type": "none", "x": 512, "y": 512, "PATH": [13]},
    23: {"name": "6 : 3", "type": "none", "x": 640, "y": 512, "PATH": [22]},
    24: {"name": "7 : 3", "type": "none", "x": 768, "y": 512, "PATH": [15]},
    25: {"name": "8 : 3", "type": "none", "x": 896, "y": 512, "PATH": [-1]},
    26: {"name": "9 : 3", "type": "none", "x": 1024, "y": 512, "PATH": [16]},
    # Ряд 4: y = 384
    27: {"name": "1 : 4", "type": "none", "x": 0, "y": 384, "PATH": [36]},
    28: {"name": "2 : 4", "type": "none", "x": 128, "y": 384, "PATH": [27]},
    29: {"name": "3 : 4", "type": "none", "x": 256, "y": 384, "PATH": [28]},
    30: {"name": "4 : 4", "type": "none", "x": 384, "y": 384, "PATH": [29]},
    31: {"name": "5 : 4", "type": "none", "x": 512, "y": 384, "PATH": [23]},
    32: {"name": "6 : 4", "type": "none", "x": 640, "y": 384, "PATH": [-1]},
    33: {"name": "7 : 4", "type": "none", "x": 768, "y": 384, "PATH": [24]},
    34: {"name": "8 : 4", "type": "none", "x": 896, "y": 384, "PATH": [-1]},
    35: {"name": "9 : 4", "type": "none", "x": 1024, "y": 384, "PATH": [26]},
    # Ряд 5: y = 256
    36: {"name": "1 : 5", "type": "none", "x": 0, "y": 256, "PATH": [46]},
    37: {"name": "2 : 5", "type": "none", "x": 128, "y": 256, "PATH": [-1]},
    38: {"name": "3 : 5", "type": "none", "x": 256, "y": 256, "PATH": [-1]},
    39: {"name": "4 : 5", "type": "none", "x": 384, "y": 256, "PATH": [-1]},
    40: {"name": "5 : 5", "type": "none", "x": 512, "y": 256, "PATH": [31]},
    41: {"name": "6 : 5", "type": "none", "x": 640, "y": 256, "PATH": [42]},
    42: {"name": "7 : 5", "type": "none", "x": 768, "y": 256, "PATH": [43]},
    43: {"name": "8 : 5", "type": "none", "x": 896, "y": 256, "PATH": [33]},
    44: {"name": "9 : 5", "type": "none", "x": 1024, "y": 256, "PATH": [35]},
    # Ряд 6: y = 128
    45: {"name": "1 : 6", "type": "none", "x": 0, "y": 128, "PATH": [-1]},
    46: {"name": "2 : 6", "type": "none", "x": 128, "y": 128, "PATH": [55]},
    47: {"name": "3 : 6", "type": "none", "x": 256, "y": 128, "PATH": [56]},
    48: {"name": "4 : 6", "type": "none", "x": 384, "y": 128, "PATH": [58]},
    49: {"name": "5 : 6", "type": "none", "x": 512, "y": 128, "PATH": [40]},
    50: {"name": "6 : 6", "type": "none", "x": 640, "y": 128, "PATH": [-1]},
    51: {"name": "7 : 6", "type": "none", "x": 768, "y": 128, "PATH": [41]},
    52: {"name": "8 : 6", "type": "none", "x": 896, "y": 128, "PATH": [51]},
    53: {"name": "9 : 6", "type": "none", "x": 1024, "y": 128, "PATH": [44, 52]},
    # Ряд 7 (верхний): y = 0
    54: {"name": "1 : 7", "type": "none", "x": 0, "y": 0, "PATH": [-1]},
    55: {"name": "2 : 7", "type": "none", "x": 128, "y": 0, "PATH": [47]},
    56: {"name": "3 : 7", "type": "none", "x": 256, "y": 0, "PATH": [48]},
    57: {"name": "4 : 7", "type": "none", "x": 384, "y": 0, "PATH": [-1]},
    58: {"name": "5 : 7", "type": "none", "x": 512, "y": 0, "PATH": [59, 49]},
    59: {"name": "6 : 7", "type": "none", "x": 640, "y": 0, "PATH": [60]},
    60: {"name": "7 : 7", "type": "none", "x": 768, "y": 0, "PATH": [61]},
    61: {"name": "8 : 7", "type": "none", "x": 896, "y": 0, "PATH": [62]},
    62: {"name": "9 : 7", "type": "none", "x": 1024, "y": 0, "PATH": [53]},
}

# Клетки, на которых выдаются карты
CARD_CELLS = [9, 18, 27, 26, 35, 44, 54, 58, 62]

# Стартовая клетка
START_CELL = 0