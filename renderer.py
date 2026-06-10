import pygame
from settings import *
from ui import Button

class Renderer:
    """Отвечает за всю отрисовку игрового мира"""
    
    def __init__(self, screen_width, screen_height, map_x, map_y):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_x = map_x
        self.map_y = map_y
        
        # Шрифты
        self.font = pygame.font.Font(None, 28)
        self.font_title = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 20)
        
        # Изображения
        try:
            self.map_image = pygame.image.load(MAP_WITHOUT_STEPS)
            self.map_image = pygame.transform.scale(self.map_image, (MAP_WIDTH, MAP_HEIGHT))
        except:
            self.map_image = None
        
        try:
            self.steps_image = pygame.image.load(MAP_STEPS)
            self.steps_image = pygame.transform.scale(self.steps_image, (MAP_WIDTH, MAP_HEIGHT))
        except:
            self.steps_image = None
    
    def draw(self, screen, game_world):
        """Главный метод отрисовки всего игрового мира"""
        # Слой 1: Карта
        self.draw_map(screen)
        
        # Слой 2: Путь
        self.draw_steps(screen)
        
        # Слой 3: Сетка и выделение
        self.draw_grid(screen, game_world.selected_cell)
        
        # Слой 4: Игроки
        self.draw_players(screen, game_world.players)
        
        # Слой 5: Стрелки развилок
        self.draw_fork_arrows(screen, game_world)
        
        # Интерфейс
        self.draw_turn_panel(screen, game_world.current_player)
        self.draw_dice_area(screen, game_world)
        self.draw_hand_button(screen, game_world)
        self.draw_hand(screen, game_world)
        self.draw_card_hint(screen, game_world)
        self.draw_players_panel(screen, game_world)
        
        if game_world.selected_cell is not None:
            self.draw_cell_info(screen, game_world.selected_cell)
    
    # === Слои ===
    
    def draw_map(self, screen):
        if self.map_image:
            screen.blit(self.map_image, (self.map_x, self.map_y))
        else:
            map_rect = pygame.Rect(self.map_x, self.map_y, MAP_WIDTH, MAP_HEIGHT)
            pygame.draw.rect(screen, DARK_GREEN, map_rect)
    
    def draw_steps(self, screen):
        if self.steps_image:
            screen.blit(self.steps_image, (self.map_x, self.map_y))
        
        # Рамка карты
        frame_rect = pygame.Rect(self.map_x - 3, self.map_y - 3, MAP_WIDTH + 6, MAP_HEIGHT + 6)
        pygame.draw.rect(screen, GOLD, frame_rect, 3)
    
    def draw_grid(self, screen, selected_cell):
        for cell_id, cell in BOARD_CELLS.items():
            cell_x = self.map_x + cell['x']
            cell_y = self.map_y + cell['y']
            cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
            
            if cell_id == selected_cell:
                pygame.draw.rect(screen, GOLD, cell_rect, 3)
            
            pygame.draw.rect(screen, (255, 255, 255, 30), cell_rect, 1)
    
    def draw_players(self, screen, players):
        for player in players:
            offset = PLAYER_OFFSETS[player.id]
            player.draw(screen, self.map_x, self.map_y, offset)
    
    def draw_fork_arrows(self, screen, game_world):
        if game_world.phase != "fork_wait" or not game_world.fork_arrows:
            return
        
        for arrow in game_world.fork_arrows:
            ax = self.map_x + arrow['x']
            ay = self.map_y + arrow['y']
            adx = arrow['dx']
            ady = arrow['dy']
            
            arrow_size = 30
            tip_x = ax + adx * arrow_size
            tip_y = ay + ady * arrow_size
            
            wing_x = -ady * 10
            wing_y = adx * 10
            
            points = [
                (tip_x, tip_y),
                (ax + wing_x, ay + wing_y),
                (ax - wing_x, ay - wing_y)
            ]
            pygame.draw.polygon(screen, GOLD, points)
            pygame.draw.polygon(screen, WHITE, points, 2)
    
    # === Панели интерфейса ===
    
    def draw_turn_panel(self, screen, current_player):
        panel_width = 300
        panel_height = 60
        panel_x = 20
        panel_y = self.map_y
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(200)
        panel_surface.fill((40, 40, 60))
        screen.blit(panel_surface, (panel_x, panel_y))
        pygame.draw.rect(screen, GOLD, (panel_x, panel_y, panel_width, panel_height), 2)
        
        turn_text = self.font_title.render(
            f"Ход: {current_player.name}",
            True, current_player.color
        )
        screen.blit(turn_text, (panel_x + 10, panel_y + 15))
    
    def draw_dice_area(self, screen, game_world):
        dice_x = 30
        dice_y = self.map_y + 100
        
        game_world.dice.draw(screen, dice_x, dice_y)
        
        mouse_pos = pygame.mouse.get_pos()
        
        if game_world.phase == "roll" and not game_world.rolled:
            game_world.roll_button.update(mouse_pos)
            game_world.roll_button.draw(screen)
        elif game_world.phase == "wait_move":
            game_world.move_button.update(mouse_pos)
            game_world.move_button.draw(screen)
        elif game_world.phase == "moved":
            hint = self.font.render("ПРОБЕЛ — следующий ход", True, GOLD)
            hint_x = game_world.move_button.rect.x
            hint_y = game_world.move_button.rect.y
            screen.blit(hint, (hint_x, hint_y))
    
    def draw_hand_button(self, screen, game_world):
        mouse_pos = pygame.mouse.get_pos()
        game_world.hand_button.update(mouse_pos)
        game_world.hand_button.draw(screen)
    
    def draw_hand(self, screen, game_world):
        game_world.current_player.hand.draw(screen, self.screen_width, self.screen_height)
    
    def draw_card_hint(self, screen, game_world):
        if game_world.selected_card_index is None:
            return
        
        hand = game_world.current_player.hand
        if game_world.selected_card_index >= hand.count():
            return
        
        card = hand.get_cards()[game_world.selected_card_index]
        hint_text = ""
        
        if card.type == "teleport":
            hint_text = "Кликните по клетке для телепорта"
        elif card.type == "building":
            hint_text = "Кликните по клетке для постройки"
        
        if hint_text:
            hint = self.font.render(hint_text, True, GOLD)
            hint_rect = hint.get_rect(center=(self.screen_width // 2, self.screen_height - 270))
            screen.blit(hint, hint_rect)
    
    def draw_cell_info(self, screen, selected_cell):
        cell = BOARD_CELLS[selected_cell]
        
        panel_width = 300
        panel_height = 150
        panel_x = 20
        panel_y = self.screen_height - 430
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(220)
        panel_surface.fill((30, 30, 50))
        screen.blit(panel_surface, (panel_x, panel_y))
        pygame.draw.rect(screen, GOLD, (panel_x, panel_y, panel_width, panel_height), 2)
        
        y_offset = panel_y + 10
        title = self.font_title.render(f"Клетка: {cell['name']}", True, GOLD)
        screen.blit(title, (panel_x + 10, y_offset))
        
        y_offset += 40
        for line in [f"Тип: {cell['type']}", f"Связи: {cell['PATH']}"]:
            text = self.font.render(line, True, WHITE)
            screen.blit(text, (panel_x + 10, y_offset))
            y_offset += 25
    
    def draw_players_panel(self, screen, game_world):
        panel_width = 300
        panel_height = 160
        panel_x = 20
        panel_y = self.screen_height - 220
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(200)
        panel_surface.fill((40, 40, 60))
        screen.blit(panel_surface, (panel_x, panel_y))
        pygame.draw.rect(screen, GOLD, (panel_x, panel_y, panel_width, panel_height), 2)
        
        y_offset = panel_y + 10
        title = self.font_title.render("Игроки", True, GOLD)
        screen.blit(title, (panel_x + 10, y_offset))
        
        y_offset += 35
        for player in game_world.players:
            pygame.draw.circle(screen, player.color, (panel_x + 25, y_offset + 8), 10)
            pygame.draw.circle(screen, WHITE, (panel_x + 25, y_offset + 8), 10, 1)
            
            if player == game_world.current_player:
                status = " (идёт...)" if player.moving else ""
                text = self.font.render(f"> {player.name}: {player.points} очк.{status}", True, GOLD)
            else:
                text = self.font.render(f"  {player.name}: {player.points} очк.", True, WHITE)
            screen.blit(text, (panel_x + 45, y_offset))
            y_offset += 28