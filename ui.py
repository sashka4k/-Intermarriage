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
            elif len(self.text) < 12:
                self.text += event.unicode
    
    def draw(self, screen):
        label_text = self.label_font.render(self.label, True, GOLD)
        screen.blit(label_text, (self.rect.x, self.rect.y - 25))
        
        color = LIGHT_BLUE if self.active else GRAY
        pygame.draw.rect(screen, (30, 30, 50), self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 8))
        
        if self.active:
            cursor_x = self.rect.x + 10 + text_surface.get_width() + 2
            pygame.draw.line(screen, WHITE, 
                           (cursor_x, self.rect.y + 8),
                           (cursor_x, self.rect.y + self.rect.height - 8), 2)