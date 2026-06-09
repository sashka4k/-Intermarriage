import pygame
import random
from settings import *

class Dice:
    """Класс двух кубиков"""
    def __init__(self):
        self.die1 = 1
        self.die2 = 1
        self.final_die1 = 1
        self.final_die2 = 1
        self.rolling = False
        self.roll_time = 0
        self.roll_duration = 30  # кадров анимации
        self.result_shown = False
    
    def roll(self):
        """Бросок кубиков — финальный результат определяется сразу"""
        self.final_die1 = random.randint(1, 6)
        self.final_die2 = random.randint(1, 6)
        self.die1 = 1
        self.die2 = 1
        self.rolling = True
        self.roll_time = 0
        self.result_shown = False
    
    def update(self):
        """Анимация броска"""
        if self.rolling:
            self.roll_time += 1
            if self.roll_time < self.roll_duration:
                # Пока крутятся — меняем значения случайно
                self.die1 = random.randint(1, 6)
                self.die2 = random.randint(1, 6)
            else:
                # Показываем сохранённый финальный результат
                self.die1 = self.final_die1
                self.die2 = self.final_die2
                self.rolling = False
                self.result_shown = True
    
    def get_total(self):
        """Сумма на кубиках"""
        return self.die1 + self.die2
    
    def is_double(self):
        """Дубль?"""
        return self.die1 == self.die2
    
    def reset(self):
        """Сброс для нового хода"""
        self.rolling = False
        self.result_shown = False
        self.die1 = 1
        self.die2 = 1
    
    def draw(self, screen, x, y):
        """Отрисовка кубиков"""
        dice_size = 60
        spacing = 15
        
        # Кубик 1
        self.draw_die(screen, x, y, self.die1, dice_size)
        # Кубик 2
        self.draw_die(screen, x + dice_size + spacing, y, self.die2, dice_size)
        
        # Сумма — показываем только когда бросок завершён
        if self.result_shown and not self.rolling:
            font = pygame.font.Font(None, 48)
            total_text = font.render(f"= {self.get_total()}", True, GOLD)
            screen.blit(total_text, (x + dice_size * 2 + spacing + 10, y + 10))
    
    def draw_die(self, screen, x, y, value, size):
        """Рисует один кубик с точками"""
        dice_rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(screen, WHITE, dice_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, dice_rect, 2, border_radius=10)
        
        dot_color = BLACK
        dot_radius = 7
        
        cx = x + size // 2
        cy = y + size // 2
        offset = size // 4
        
        positions = {
            1: [(cx, cy)],
            2: [(cx - offset, cy - offset), (cx + offset, cy + offset)],
            3: [(cx - offset, cy - offset), (cx, cy), (cx + offset, cy + offset)],
            4: [(cx - offset, cy - offset), (cx + offset, cy - offset),
                (cx - offset, cy + offset), (cx + offset, cy + offset)],
            5: [(cx - offset, cy - offset), (cx + offset, cy - offset),
                (cx, cy),
                (cx - offset, cy + offset), (cx + offset, cy + offset)],
            6: [(cx - offset, cy - offset), (cx + offset, cy - offset),
                (cx - offset, cy), (cx + offset, cy),
                (cx - offset, cy + offset), (cx + offset, cy + offset)]
        }
        
        for pos in positions.get(value, []):
            pygame.draw.circle(screen, dot_color, pos, dot_radius)