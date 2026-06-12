import pygame
from settings import *
from ui import InputBox

class ImageButton:
    """Кнопка с изображением вместо фона (без текста)"""
    def __init__(self, x, y, width, height, image_path, hover_image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        
        # Загружаем обычное изображение
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            self.image = None
        
        # Загружаем изображение при наведении
        if hover_image_path:
            try:
                self.hover_image = pygame.image.load(hover_image_path)
                self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
            except:
                self.hover_image = None
        else:
            self.hover_image = None
    
    def draw(self, screen):
        # Выбираем какое изображение рисовать
        if self.is_hovered and self.hover_image:
            current_image = self.hover_image
        elif self.image:
            current_image = self.image
        else:
            # Если изображений нет - рисуем обычную кнопку
            color = (100, 100, 200) if self.is_hovered else (50, 50, 100)
            pygame.draw.rect(screen, color, self.rect, border_radius=10)
            pygame.draw.rect(screen, GOLD, self.rect, 2, border_radius=10)
            current_image = None
        
        if current_image:
            screen.blit(current_image, (self.rect.x, self.rect.y))
    
    def update(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        button_width = 320
        button_height = 80
        button_spacing = 40
        
        center_x = screen_width // 2 - button_width // 2
        
        total_buttons_height = button_height * 2 + button_spacing
        start_y = screen_height // 2 - total_buttons_height // 2
        
        self.buttons = [
            ImageButton(center_x, start_y, button_width, button_height, 
                       "Prefabs/Pictures/button_new_game.png",
                       "Prefabs/Pictures/button_new_game_hover.png"),
            ImageButton(center_x, start_y + button_height + button_spacing, 
                       button_width, button_height, 
                       "Prefabs/Pictures/button_exit.png",
                       "Prefabs/Pictures/button_exit_hover.png")
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
        
        input_width = 380
        input_height = 55
        start_y = screen_height // 2 - 80
        spacing = 90
        
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
        
        button_width = 320
        button_height = 80
        button_center_x = screen_width // 2 - button_width // 2
        
        self.start_button = ImageButton(
            button_center_x,
            start_y + 4 * spacing + 30,
            button_width, button_height,
            #ПОменял с button_start.png на button_new_game.png
            "Prefabs/Pictures/button_new_game.png",
            "Prefabs/Pictures/button_new_game_hover.png"
        )
        
        self.back_button = ImageButton(
            button_center_x,
            start_y + 4 * spacing + 120,
            button_width, button_height,
            "Prefabs/Pictures/button_back.png",
            "Prefabs/Pictures/button_back_hover.png"
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
        
        button_width = 320
        button_height = 80
        button_spacing = 30
        
        center_x = screen_width // 2 - button_width // 2
        
        total_buttons_height = button_height * 3 + button_spacing * 2
        start_y = screen_height // 2 - total_buttons_height // 2
        
        self.buttons = [
            ImageButton(center_x, start_y, button_width, button_height,
                       "Prefabs/Pictures/button_resume.png",
                       "Prefabs/Pictures/button_resume_hover.png"),
            ImageButton(center_x, start_y + button_height + button_spacing, 
                       button_width, button_height,
                       "Prefabs/Pictures/button_menu.png",
                       "Prefabs/Pictures/button_menu_hover.png"),
            ImageButton(center_x, start_y + (button_height + button_spacing) * 2, 
                       button_width, button_height,
                       "Prefabs/Pictures/button_exit.png",
                       "Prefabs/Pictures/button_exit_hover.png")
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