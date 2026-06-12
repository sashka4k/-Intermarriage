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
    0: {"name": "1 : 1", "tags": ["forest"], "x": 0, "y": 768, "PATH": [9]},
    1: {"name": "2 : 1", "tags": ["forest"], "x": 128, "y": 768, "PATH": [0]},
    2: {"name": "3 : 1", "tags": ["water"], "x": 256, "y": 768, "PATH": [11]},
    3: {"name": "4 : 1", "tags": ["forest"], "x": 384, "y": 768, "PATH": [2]},
    4: {"name": "5 : 1", "tags": ["forest"], "x": 512, "y": 768, "PATH": [-1]},
    5: {"name": "6 : 1", "tags": ["forest"], "x": 640, "y": 768, "PATH": [13]},
    6: {"name": "7 : 1", "tags": ["forest"], "x": 768, "y": 768, "PATH": [5]},
    7: {"name": "8 : 1", "tags": ["mountain"], "x": 896, "y": 768, "PATH": [-1]},
    8: {"name": "9 : 1", "tags": ["mountain"], "x": 1024, "y": 768, "PATH": [-1]},
    # Ряд 2: y = 640
    9: {"name": "1 : 2", "tags": ["water"], "x": 0, "y": 640, "PATH": [18]},
    10: {"name": "2 : 2", "tags": ["water"], "x": 128, "y": 640, "PATH": [1]},
    11: {"name": "3 : 2", "tags": ["water"], "x": 256, "y": 640, "PATH": [10]},
    12: {"name": "4 : 2", "tags": ["water"], "x": 384, "y": 640, "PATH": [3]},
    13: {"name": "5 : 2", "tags": ["forest"], "x": 512, "y": 640, "PATH": [12]},
    14: {"name": "6 : 2", "tags": ["plain"], "x": 640, "y": 640, "PATH": [6]},
    15: {"name": "7 : 2", "tags": ["forest"], "x": 768, "y": 640, "PATH": [14]},
    16: {"name": "8 : 2", "tags": ["plain"], "x": 896, "y": 640, "PATH": [24]},
    17: {"name": "9 : 2", "tags": ["forest"], "x": 1024, "y": 640, "PATH": [-1]},
    # Ряд 3: y = 512
    18: {"name": "1 : 3", "tags": ["water"], "x": 0, "y": 512, "PATH": [19]},
    19: {"name": "2 : 3", "tags": ["water"], "x": 128, "y": 512, "PATH": [20]},
    20: {"name": "3 : 3", "tags": ["water"], "x": 256, "y": 512, "PATH": [21]},
    21: {"name": "4 : 3", "tags": ["plain"], "x": 384, "y": 512, "PATH": [30]},
    22: {"name": "5 : 3", "tags": ["water"], "x": 512, "y": 512, "PATH": [13]},
    23: {"name": "6 : 3", "tags": ["water"], "x": 640, "y": 512, "PATH": [22]},
    24: {"name": "7 : 3", "tags": ["water"], "x": 768, "y": 512, "PATH": [15]},
    25: {"name": "8 : 3", "tags": ["forest"], "x": 896, "y": 512, "PATH": [-1]},
    26: {"name": "9 : 3", "tags": ["mountain"], "x": 1024, "y": 512, "PATH": [16]},
    # Ряд 4: y = 384
    27: {"name": "1 : 4", "tags": ["water"], "x": 0, "y": 384, "PATH": [36]},
    28: {"name": "2 : 4", "tags": ["plain"], "x": 128, "y": 384, "PATH": [27]},
    29: {"name": "3 : 4", "tags": ["plain"], "x": 256, "y": 384, "PATH": [28]},
    30: {"name": "4 : 4", "tags": ["plain"], "x": 384, "y": 384, "PATH": [29]},
    31: {"name": "5 : 4", "tags": ["plain"], "x": 512, "y": 384, "PATH": [23]},
    32: {"name": "6 : 4", "tags": ["forest"], "x": 640, "y": 384, "PATH": [-1]},
    33: {"name": "7 : 4", "tags": ["water"], "x": 768, "y": 384, "PATH": [24]},
    34: {"name": "8 : 4", "tags": ["water"], "x": 896, "y": 384, "PATH": [-1]},
    35: {"name": "9 : 4", "tags": ["mountain"], "x": 1024, "y": 384, "PATH": [26]},
    # Ряд 5: y = 256
    36: {"name": "1 : 5", "tags": ["water"], "x": 0, "y": 256, "PATH": [46]},
    37: {"name": "2 : 5", "tags": ["forest"], "x": 128, "y": 256, "PATH": [-1]},
    38: {"name": "3 : 5", "tags": ["forest"], "x": 256, "y": 256, "PATH": [-1]},
    39: {"name": "4 : 5", "tags": ["plain"], "x": 384, "y": 256, "PATH": [-1]},
    40: {"name": "5 : 5", "tags": ["forest"], "x": 512, "y": 256, "PATH": [31]},
    41: {"name": "6 : 5", "tags": ["plain"], "x": 640, "y": 256, "PATH": [42]},
    42: {"name": "7 : 5", "tags": ["forest"], "x": 768, "y": 256, "PATH": [43]},
    43: {"name": "8 : 5", "tags": ["plain"], "x": 896, "y": 256, "PATH": [33]},
    44: {"name": "9 : 5", "tags": ["water"], "x": 1024, "y": 256, "PATH": [35]},
    # Ряд 6: y = 128
    45: {"name": "1 : 6", "tags": ["forest"], "x": 0, "y": 128, "PATH": [-1]},
    46: {"name": "2 : 6", "tags": ["plain"], "x": 128, "y": 128, "PATH": [55]},
    47: {"name": "3 : 6", "tags": ["plain"], "x": 256, "y": 128, "PATH": [56]},
    48: {"name": "4 : 6", "tags": ["plain"], "x": 384, "y": 128, "PATH": [58]},
    49: {"name": "5 : 6", "tags": ["forest"], "x": 512, "y": 128, "PATH": [40]},
    50: {"name": "6 : 6", "tags": ["water"], "x": 640, "y": 128, "PATH": [-1]},
    51: {"name": "7 : 6", "tags": ["forest"], "x": 768, "y": 128, "PATH": [41]},
    52: {"name": "8 : 6", "tags": ["plain"], "x": 896, "y": 128, "PATH": [51]},
    53: {"name": "9 : 6", "tags": ["mountain"], "x": 1024, "y": 128, "PATH": [44, 52]},
    # Ряд 7 (верхний): y = 0
    54: {"name": "1 : 7", "tags": ["forest"], "x": 0, "y": 0, "PATH": [-1]},
    55: {"name": "2 : 7", "tags": ["forest"], "x": 128, "y": 0, "PATH": [47]},
    56: {"name": "3 : 7", "tags": ["forest"], "x": 256, "y": 0, "PATH": [48]},
    57: {"name": "4 : 7", "tags": ["forest"], "x": 384, "y": 0, "PATH": [-1]},
    58: {"name": "5 : 7", "tags": ["plain"], "x": 512, "y": 0, "PATH": [59, 49]},
    59: {"name": "6 : 7", "tags": ["forest"], "x": 640, "y": 0, "PATH": [60]},
    60: {"name": "7 : 7", "tags": ["mountain"], "x": 768, "y": 0, "PATH": [61]},
    61: {"name": "8 : 7", "tags": ["mountain"], "x": 896, "y": 0, "PATH": [62]},
    62: {"name": "9 : 7", "tags": ["mountain"], "x": 1024, "y": 0, "PATH": [53]},
}

# Постройки на карте: key = cell_id, value = {"building": "fisher_hut"/..., "owner": player_id или None}
BUILDINGS = {}

# Типы зданий
BUILDING_TYPES = {
    "fisher_hut": {
        "name": "Хижина рыбака",
        "required_tag": "water",
        "color": (70, 130, 180),
        "owner_matter": 4,      # владелец при попадании любого
        "visitor_matter": 2,    # гость при попадании
    },
    "quarry": {
        "name": "Карьер",
        "required_tag": "mountain",
        "color": (160, 140, 100),
        "owner_matter": 5,      # владелец каждый круг
        "visitor_matter": 0,    # гости ничего
    },
    "sawmill": {
        "name": "Лесопилка",
        "required_tag": "forest",
        "color": (34, 139, 34),
        "owner_matter": 2,      # владелец при попадании
        "visitor_matter": 2,    # гость при попадании (всем поровну)
    },
    "farm": {
        "name": "Ферма",
        "required_tag": "plain",
        "color": (218, 165, 32),
        "owner_matter": 1.5,    # владелец при своём попадании
        "visitor_matter": 1,    # гость при попадании
        "owner_passive": 0.5,   # владелец когда гость попадает
    },
}

# Клетки, на которых выдаются карты
CARD_CELLS = [8, 17, 26, 35, 44, 54, 62]

# Стартовая клетка
START_CELL = 0

# Ландшафт на клетках: key = cell_id, value = "canyon" (пока только каньон)
LANDSCAPES = {}

# Каньон — параметры
CANYON_STOP_TURNS = 1  # сколько ходов пропускает игрок

MAX_TURNS = 10