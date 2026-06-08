import pygame
from settings import *

class Button:
    """Класс кнопки"""
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        text = self.font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        
    def update(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class MainMenu:
    """Главное меню"""
    def __init__(self):
        button_width = 200
        button_height = 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.buttons = [
            Button(center_x, 300, button_width, button_height, "Новая игра", BLUE, LIGHT_BLUE),
            Button(center_x, 380, button_width, button_height, "Настройки", BLUE, LIGHT_BLUE),
            Button(center_x, 460, button_width, button_height, "Выход", BLUE, LIGHT_BLUE)
        ]
        
    def draw(self, screen, background=None):
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Заголовок
        font = pygame.font.Font(None, 72)
        title = font.render("МЕЖДУЗЕМЬЕ", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        for button in self.buttons:
            button.draw(screen)
            
    def update(self, pos):
        for button in self.buttons:
            button.update(pos)
            
    def handle_click(self, pos, event):
        if self.buttons[0].is_clicked(pos, event):
            return "new_game"
        elif self.buttons[1].is_clicked(pos, event):
            return "settings"
        elif self.buttons[2].is_clicked(pos, event):
            return "exit"
        return None

class PauseMenu:
    """Меню паузы"""
    def __init__(self):
        button_width = 200
        button_height = 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.buttons = [
            Button(center_x, 300, button_width, button_height, "Продолжить", BLUE, LIGHT_BLUE),
            Button(center_x, 380, button_width, button_height, "Главное меню", BLUE, LIGHT_BLUE),
            Button(center_x, 460, button_width, button_height, "Выход", BLUE, LIGHT_BLUE)
        ]
        
    def draw(self, screen, background=None):
        # Затемнение
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        title = font.render("ПАУЗА", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        for button in self.buttons:
            button.draw(screen)
            
    def update(self, pos):
        for button in self.buttons:
            button.update(pos)
            
    def handle_click(self, pos, event):
        if self.buttons[0].is_clicked(pos, event):
            return "resume"
        elif self.buttons[1].is_clicked(pos, event):
            return "main_menu"
        elif self.buttons[2].is_clicked(pos, event):
            return "exit"
        return None