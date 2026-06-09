import pygame
from settings import *
from card import CardHand

class Player:
    def __init__(self, name, color, player_id):
        self.name = name
        self.color = color
        self.id = player_id
        self.position = START_CELL  # все начинают со старта
        self.money = 0
        self.points = 0
        self.hand = None
        
        # Анимация
        self.moving = False
        self.move_path = []
        self.move_progress = 0
        self.move_speed = 0.08
        self.draw_x = None  # текущая X для отрисовки
        self.draw_y = None  # текущая Y для отрисовки

        self.hand = CardHand(max_cards=5)
    
    def start_move(self, path):
        """Начать движение по пути"""
        if len(path) < 2:
            self.position = path[-1] if path else self.position
            return
        
        self.move_path = path
        self.move_progress = 0
        self.moving = True
        
        # Начальная позиция
        start_cell = BOARD_CELLS[path[0]]
        self.draw_x = start_cell['x'] + CELL_SIZE // 2
        self.draw_y = start_cell['y'] + CELL_SIZE // 2
    
    def update_move(self):
        """Обновление анимации"""
        if not self.moving or len(self.move_path) < 2:
            return
        
        self.move_progress += self.move_speed
        
        # Текущий отрезок пути
        total_segments = len(self.move_path) - 1
        progress_total = self.move_progress  # от 0 до total_segments
        
        if progress_total >= total_segments:
            # Конец пути
            self.position = self.move_path[-1]
            self.moving = False
            self.move_path = []
            self.draw_x = None
            self.draw_y = None
            return
        
        # Между какими клетками сейчас идём
        idx = int(progress_total)
        t = progress_total - idx  # 0.0 до 1.0
        
        cell_from = BOARD_CELLS[self.move_path[idx]]
        cell_to = BOARD_CELLS[self.move_path[idx + 1]]
        
        x1 = cell_from['x'] + CELL_SIZE // 2
        y1 = cell_from['y'] + CELL_SIZE // 2
        x2 = cell_to['x'] + CELL_SIZE // 2
        y2 = cell_to['y'] + CELL_SIZE // 2
        
        self.draw_x = x1 + (x2 - x1) * t
        self.draw_y = y1 + (y2 - y1) * t
    
    def move(self, steps, force_path=None):
        """
        Вычисляет путь на steps шагов вперёд.
        Если force_path передан — идём по принудительному пути (после выбора на развилке).
        """
        if force_path is not None:
            self.start_move(force_path)
            return force_path[-1]
    
        path = [self.position]
        current = self.position
    
        for _ in range(steps):
            cell = BOARD_CELLS[current]
            # Берём первый доступный путь
            valid_paths = [p for p in cell['PATH'] if p != -1]
            if valid_paths:
                current = valid_paths[0]
                path.append(current)
            else:
                break
    
        self.start_move(path)
        return current
    
    def is_moving(self):
        return self.moving
    
    def draw(self, screen, map_x, map_y, offset):
        """Рисует жетон игрока — единый метод отрисовки"""
        if self.moving and self.draw_x is not None:
            cx = map_x + self.draw_x
            cy = map_y + self.draw_y
        else:
            cell = BOARD_CELLS[self.position]
            cx = map_x + cell['x'] + CELL_SIZE // 2
            cy = map_y + cell['y'] + CELL_SIZE // 2
    
        px = cx + offset[0]
        py = cy + offset[1]
    
        # Тень
        pygame.draw.circle(screen, (0, 0, 0), (px + 2, py + 2), 14)
        # Жетон
        pygame.draw.circle(screen, self.color, (px, py), 14)
        pygame.draw.circle(screen, WHITE, (px, py), 14, 2)
    
        # Номер игрока
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.id + 1), True, WHITE)
        text_rect = text.get_rect(center=(px, py))
        screen.blit(text, text_rect)