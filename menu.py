import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, GOLD, self.rect, 2, border_radius=10)
        
        text = self.font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def update(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


class InputBox:
    """Поле ввода текста"""
    def __init__(self, x, y, width, height, label, default_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.text = default_text
        self.active = False
        self.font = pygame.font.Font(None, 36)
        self.label_font = pygame.font.Font(None, 28)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif len(self.text) < 12:  # макс длина имени
                self.text += event.unicode
    
    def draw(self, screen):
        # Подпись
        label_text = self.label_font.render(self.label, True, GOLD)
        screen.blit(label_text, (self.rect.x, self.rect.y - 25))
        
        # Поле ввода
        color = LIGHT_BLUE if self.active else GRAY
        pygame.draw.rect(screen, (30, 30, 50), self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        
        # Текст
        text_surface = self.font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 8))
        
        # Курсор если активно
        if self.active:
            cursor_x = self.rect.x + 10 + text_surface.get_width() + 2
            pygame.draw.line(screen, WHITE, 
                           (cursor_x, self.rect.y + 8),
                           (cursor_x, self.rect.y + self.rect.height - 8), 2)


class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        button_width = 250
        button_height = 60
        center_x = screen_width // 2 - button_width // 2
        
        self.buttons = [
            Button(center_x, screen_height // 2 - 60, button_width, button_height, 
                   "Новая игра", BLUE, LIGHT_BLUE),
            Button(center_x, screen_height // 2 + 20, button_width, button_height, 
                   "Выход", RED, (250, 100, 100))
        ]
    
    def draw(self, screen, background=None):
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)
        
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(100)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 96)
        title = font.render("МЕЖДУЗЕМЬЕ", True, GOLD)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
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
            return "exit"
        return None


class PlayerSetupMenu:
    """Экран ввода имён 4 игроков"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Поля ввода для 4 игроков
        input_width = 300
        input_height = 40
        start_y = screen_height // 2 - 120
        spacing = 70
        
        player_labels = [
            "Игрок 1 (синий)",
            "Игрок 2 (красный)", 
            "Игрок 3 (зелёный)",
            "Игрок 4 (жёлтый)"
        ]
        default_names = ["", "", "", ""]
        
        self.inputs = []
        center_x = screen_width // 2 - input_width // 2
        
        for i in range(4):
            y = start_y + i * spacing
            self.inputs.append(
                InputBox(center_x, y, input_width, input_height, 
                        player_labels[i], default_names[i])
            )
        
        # Кнопка "Начать игру"
        button_width = 250
        button_height = 60
        self.start_button = Button(
            screen_width // 2 - button_width // 2,
            start_y + 4 * spacing + 20,
            button_width, button_height,
            "Начать игру", BLUE, LIGHT_BLUE
        )
        
        # Кнопка "Назад"
        self.back_button = Button(
            screen_width // 2 - button_width // 2,
            start_y + 4 * spacing + 90,
            button_width, button_height,
            "Назад", RED, (250, 100, 100)
        )
    
    def handle_event(self, event):
        for input_box in self.inputs:
            input_box.handle_event(event)
    
    def update(self, pos):
        self.start_button.update(pos)
        self.back_button.update(pos)
    
    def handle_click(self, pos, event):
        if self.start_button.is_clicked(pos, event):
            return "start_game"
        elif self.back_button.is_clicked(pos, event):
            return "back"
        return None
    
    def get_player_names(self):
        """Возвращает список имён (пустые заменяет на Игрок 1-4)"""
        names = []
        for i, inp in enumerate(self.inputs):
            name = inp.text.strip()
            if not name:
                name = f"Игрок {i + 1}"
            names.append(name)
        return names
    
    def draw(self, screen, background=None):
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)
        
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(100)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        title = font.render("ВВЕДИТЕ ИМЕНА ИГРОКОВ", True, GOLD)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 3 - 40))
        screen.blit(title, title_rect)
        
        for input_box in self.inputs:
            input_box.draw(screen)
        
        self.start_button.draw(screen)
        self.back_button.draw(screen)


class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        button_width = 250
        button_height = 60
        center_x = screen_width // 2 - button_width // 2
        
        self.buttons = [
            Button(center_x, screen_height // 2 - 80, button_width, button_height,
                   "Продолжить", BLUE, LIGHT_BLUE),
            Button(center_x, screen_height // 2, button_width, button_height,
                   "Главное меню", BLUE, LIGHT_BLUE),
            Button(center_x, screen_height // 2 + 80, button_width, button_height,
                   "Выход", RED, (250, 100, 100))
        ]
    
    def draw(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(160)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        title = font.render("ПАУЗА", True, GOLD)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
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