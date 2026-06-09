import pygame
from settings import *

class Card:
    """Карта действия"""
    
    TYPES = {
        "building": {"name": "Постройка", "color": (100, 200, 100), "desc": "Построить здание на клетке"},
        "teleport": {"name": "Телепорт", "color": (100, 150, 250), "desc": "Переместиться на выбранную клетку"},
        "points":   {"name": "+100 очков", "color": (250, 200, 50), "desc": "Получить 100 очков"},
    }
    
    def __init__(self, card_type):
        self.type = card_type
        self.name = Card.TYPES[card_type]["name"]
        self.color = Card.TYPES[card_type]["color"]
        self.desc = Card.TYPES[card_type]["desc"]
    
    def get_name(self):
        return self.name
    
    def get_color(self):
        return self.color


class CardHand:
    """Рука карт игрока"""
    def __init__(self, max_cards=5):
        self.cards = []
        self.max_cards = max_cards
        self.visible = False  # показывать ли руку
    
    def add_card(self, card):
        """Добавить карту в руку"""
        if len(self.cards) < self.max_cards:
            self.cards.append(card)
            return True
        return False  # рука полна
    
    def remove_card(self, index):
        """Убрать карту по индексу"""
        if 0 <= index < len(self.cards):
            return self.cards.pop(index)
        return None
    
    def play_card(self, index):
        """Сыграть карту (удаляет и возвращает её)"""
        return self.remove_card(index)
    
    def get_cards(self):
        return self.cards
    
    def count(self):
        return len(self.cards)
    
    def toggle_visible(self):
        self.visible = not self.visible
    
    def draw(self, screen, screen_width, screen_height):
        """Отрисовка руки карт внизу экрана"""
        if not self.visible or not self.cards:
            return
        
        card_width = 150
        card_height = 200
        spacing = 20
        total_width = len(self.cards) * card_width + (len(self.cards) - 1) * spacing
        start_x = screen_width // 2 - total_width // 2
        y = screen_height - card_height - 40
        
        # Полупрозрачный фон для всей руки
        panel = pygame.Surface((screen_width, card_height + 60))
        panel.set_alpha(180)
        panel.fill((20, 20, 40))
        screen.blit(panel, (0, y - 20))
        
        font_name = pygame.font.Font(None, 20)
        font_desc = pygame.font.Font(None, 16)
        font_index = pygame.font.Font(None, 24)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for i, card in enumerate(self.cards):
            cx = start_x + i * (card_width + spacing)
            cy = y
            
            card_rect = pygame.Rect(cx, cy, card_width, card_height)
            
            # Подсветка при наведении
            hovered = card_rect.collidepoint(mouse_x, mouse_y)
            
            # Фон карты
            bg_color = card.color if not hovered else tuple(min(c + 50, 255) for c in card.color)
            pygame.draw.rect(screen, bg_color, card_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, card_rect, 2, border_radius=12)
            
            # Номер карты
            idx_text = font_index.render(str(i + 1), True, WHITE)
            screen.blit(idx_text, (cx + 10, cy + 8))
            
            # Название
            name_text = font_name.render(card.name, True, WHITE)
            name_rect = name_text.get_rect(center=(cx + card_width // 2, cy + 50))
            screen.blit(name_text, name_rect)
            
            # Описание (перенос строк)
            desc_words = card.desc.split()
            line1 = ""
            line2 = ""
            for word in desc_words:
                if len(line1) < 15:
                    line1 += word + " "
                else:
                    line2 += word + " "
            
            desc1 = font_desc.render(line1.strip(), True, WHITE)
            desc1_rect = desc1.get_rect(center=(cx + card_width // 2, cy + 100))
            screen.blit(desc1, desc1_rect)
            
            if line2:
                desc2 = font_desc.render(line2.strip(), True, WHITE)
                desc2_rect = desc2.get_rect(center=(cx + card_width // 2, cy + 120))
                screen.blit(desc2, desc2_rect)
            
            # Иконка-плейсхолдер
            icon_rect = pygame.Rect(cx + card_width // 2 - 25, cy + 140, 50, 50)
            pygame.draw.rect(screen, WHITE, icon_rect, 2, border_radius=8)
            icon_label = font_name.render("?", True, WHITE)
            icon_label_rect = icon_label.get_rect(center=icon_rect.center)
            screen.blit(icon_label, icon_label_rect)
    
    def get_clicked_card(self, mouse_pos, screen_width, screen_height):
        """Возвращает индекс карты, по которой кликнули, или None"""
        if not self.visible or not self.cards:
            return None
        
        card_width = 150
        card_height = 200
        spacing = 20
        total_width = len(self.cards) * card_width + (len(self.cards) - 1) * spacing
        start_x = screen_width // 2 - total_width // 2
        y = screen_height - card_height - 40
        
        mx, my = mouse_pos
        
        for i in range(len(self.cards)):
            cx = start_x + i * (card_width + spacing)
            card_rect = pygame.Rect(cx, y, card_width, card_height)
            if card_rect.collidepoint(mx, my):
                return i
        
        return None