import pygame
from settings import *
from ui import Button, InputBox

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
        
        button_width = 250
        button_height = 60
        self.start_button = Button(
            screen_width // 2 - button_width // 2,
            start_y + 4 * spacing + 20,
            button_width, button_height,
            "Начать игру", BLUE, LIGHT_BLUE
        )
        
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