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
        "points": {"name": "+1 материи", "color": (250, 200, 50), "desc": "Получить 1 материи"},
        "house": {"name": "Дом", "color": (200, 100, 50), "desc": "Построить на равнине", "required_tag": "plain"},
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
        self.visible = False
        self.font_name = pygame.font.Font(None, 20)
        self.font_desc = pygame.font.Font(None, 16)
        self.font_index = pygame.font.Font(None, 24)
        
        # Картинки карт (сохраняем оригинал + уменьшенную)
        self.card_images = {}       # оригинальный размер
        self.card_images_small = {} # для руки
        image_map = {
            "fisher_hut": "Prefabs/Pictures/card_fisher_hut.png",
            "quarry": "Prefabs/Pictures/card_quarry.png",
            "sawmill": "Prefabs/Pictures/card_sawmill.png",
            "farm": "Prefabs/Pictures/card_farm.png",
            "house": "Prefabs/Pictures/card_house.png",
            "canyon": "Prefabs/Pictures/card_canyon.png",
            "teleport": "Prefabs/Pictures/card_teleport.png",
            "points": "Prefabs/Pictures/card_1_matter.png",
        }
        for card_type, path in image_map.items():
            try:
                img = pygame.image.load(path)
                self.card_images[card_type] = img  # оригинал
                small = pygame.transform.scale(img, (80, 120))
                self.card_images_small[card_type] = small
            except:
                self.card_images[card_type] = None
                self.card_images_small[card_type] = None
    
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
        """Отрисовка руки карт — при наведении оригинальный размер"""
        if not self.visible or not self.cards:
            return
        
        small_w, small_h = 80, 120
        spacing = 15
        
        total_width = len(self.cards) * small_w + (len(self.cards) - 1) * spacing
        start_x = screen_width // 2 - total_width // 2
        y = screen_height - small_h - 40
        
        # Затемнение
        overlay = pygame.Surface((screen_width, small_h + 80))
        overlay.set_alpha(100)
        overlay.fill((20, 20, 40))
        screen.blit(overlay, (0, y - 30))
        
        # Счётчик
        count_text = f"Карты: {self.count()}/{self.max_cards}"
        count_render = pygame.font.Font(None, 32).render(count_text, True, GOLD)
        count_rect = count_render.get_rect(center=(screen_width // 2, y - 15))
        screen.blit(count_render, count_rect)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for i, card in enumerate(self.cards):
            cx = start_x + i * (small_w + spacing)
            cy = y
            
            card_rect = pygame.Rect(cx, cy, small_w, small_h)
            hovered = card_rect.collidepoint(mouse_x, mouse_y)
            
            if hovered:
                img = self.card_images.get(card.type)
                if img:
                    scale = 2
                    ow, oh = int(img.get_width() * scale), int(img.get_height() * scale)
                    scaled_img = pygame.transform.scale(img, (ow, oh))
                    
                    # По центру экрана
                    ox = (screen_width - ow) // 2
                    oy = (screen_height - oh) // 2
                    
                    # Затемнение фона посильнее
                    dark = pygame.Surface((screen_width, screen_height))
                    dark.set_alpha(150)
                    dark.fill((0, 0, 0))
                    screen.blit(dark, (0, 0))
                    
                    screen.blit(scaled_img, (ox, oy))
                    big_rect = pygame.Rect(ox, oy, ow, oh)
                    pygame.draw.rect(screen, GOLD, big_rect, 4, border_radius=8)
                    
                    # Не рисуем остальные карты
                    return
            else:
                # Уменьшенная
                img = self.card_images_small.get(card.type)
                if img:
                    screen.blit(img, (cx, cy))
    
    def get_clicked_card(self, mouse_pos, screen_width, screen_height):
        if not self.visible or not self.cards:
            return None
        
        small_w, small_h = 80, 120
        spacing = 15
        total_width = len(self.cards) * small_w + (len(self.cards) - 1) * spacing
        start_x = screen_width // 2 - total_width // 2
        y = screen_height - small_h - 40
        
        mx, my = mouse_pos
        
        for i in range(len(self.cards)):
            cx = start_x + i * (small_w + spacing)
            card_rect = pygame.Rect(cx, y, small_w, small_h)
            if card_rect.collidepoint(mx, my):
                return i
        
        return None