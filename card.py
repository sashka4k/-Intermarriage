import pygame
from settings import *

class Card:
    """Карта действия"""
    
    TYPES = {
        "fisher_hut": {"name": "Хижина рыбака", "color": (70, 130, 180), "desc": "Построить на воде", "required_tag": "water"},
        "quarry": {"name": "Карьер", "color": (160, 140, 100), "desc": "Построить в горах", "required_tag": "mountain"},
        "sawmill": {"name": "Лесопилка", "color": (34, 139, 34), "desc": "Построить в лесу", "required_tag": "forest"},
        "farm": {"name": "Ферма", "color": (218, 165, 32), "desc": "Построить на равнине", "required_tag": "plain"},
        "teleport": {"name": "Телепорт", "color": (100, 150, 250), "desc": "Переместиться на клетку"},
        "points": {"name": "+100 очков", "color": (250, 200, 50), "desc": "Получить 100 очков"},
        "canyon": {"name": "Каньон", "color": (139, 90, 43), "desc": "Создать каньон на клетке", "is_landscape": True},
    }
    
    def __init__(self, card_type):
        self.type = card_type
        info = Card.TYPES[card_type]
        self.name = info["name"]
        self.color = info["color"]
        self.desc = info["desc"]
        self.required_tag = info.get("required_tag", None)
        self.is_landscape = info.get("is_landscape", False)
    
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
        self.font_name = pygame.font.Font(None, 20)
        self.font_desc = pygame.font.Font(None, 16)
        self.font_index = pygame.font.Font(None, 24)
    
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
        pygame.draw.rect(screen, (20, 20, 40), (0, y - 20, screen_width, card_height + 60))
        
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
            idx_text = self.font_index.render(str(i + 1), True, WHITE)
            screen.blit(idx_text, (cx + 10, cy + 8))
            
            # Название
            name_text = self.font_name.render(card.name, True, WHITE)
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
            
            desc1 = self.font_desc.render(line1.strip(), True, WHITE)
            desc1_rect = desc1.get_rect(center=(cx + card_width // 2, cy + 100))
            screen.blit(desc1, desc1_rect)
            
            if line2:
                desc2 = self.font_desc.render(line2.strip(), True, WHITE)
                desc2_rect = desc2.get_rect(center=(cx + card_width // 2, cy + 120))
                screen.blit(desc2, desc2_rect)
            
            # Иконка-плейсхолдер
            icon_rect = pygame.Rect(cx + card_width // 2 - 25, cy + 140, 50, 50)
            pygame.draw.rect(screen, WHITE, icon_rect, 2, border_radius=8)
            icon_label = self.font_name.render("?", True, WHITE)
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