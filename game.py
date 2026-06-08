import pygame
from settings import *
from player import Player
from dice import Dice
from menu import Button

class GameWorld:
    def __init__(self, screen_width, screen_height, map_x, map_y, players):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_x = map_x
        self.map_y = map_y
        
        self.selected_cell = None
        self.players = players
        self.current_player_index = 0
        self.current_player = players[0]
        
        self.phase = "roll"
        self.dice = Dice()
        self.steps = 0
        self.rolled = False
        
        button_width = 200
        button_height = 50
        self.roll_button = Button(
            30,
            self.screen_height // 2 + 50,
            button_width, button_height,
            "Бросить кубики", BLUE, LIGHT_BLUE
        )
        
        try:
            self.map_image = pygame.image.load(BACKGROUND_IMAGE)
            self.map_image = pygame.transform.scale(self.map_image, (MAP_WIDTH, MAP_HEIGHT))
        except:
            self.map_image = None
        
        try:
            self.steps_image = pygame.image.load("ancient_map_steps.png")
            self.steps_image = pygame.transform.scale(self.steps_image, (MAP_WIDTH, MAP_HEIGHT))
        except:
            self.steps_image = None
        
        self.font = pygame.font.Font(None, 28)
        self.font_title = pygame.font.Font(None, 36)


        print("=== ИГРОКИ СОЗДАНЫ ===")
        for p in self.players:
            cell = BOARD_CELLS[p.position]
            print(f"  {p.name} (id={p.id}) на клетке {p.position}: {cell['name']} x={cell['x']} y={cell['y']}")
        print("=======================")
    
    def select_cell(self, cell_id):
        self.selected_cell = cell_id
    
    def get_cell_at_mouse(self, mouse_pos):
        mx, my = mouse_pos
        map_mx = mx - self.map_x
        map_my = my - self.map_y
        
        if 0 <= map_mx < MAP_WIDTH and 0 <= map_my < MAP_HEIGHT:
            col = map_mx // CELL_SIZE  # 0-8
            row_from_top = map_my // CELL_SIZE  # 0-6 (0 = верх)
            row_from_bottom = 6 - row_from_top  # инвертируем: 6 = низ
            cell_id = row_from_bottom * 9 + col
            if cell_id in BOARD_CELLS:
                return cell_id
        return None
    
    def update(self, keys):
        self.dice.update()
        
        for player in self.players:
            player.update_move()
        
        if self.dice.result_shown and self.phase == "roll":
            self.steps = self.dice.get_total()
            self.current_player.move(self.steps)
            self.phase = "moved"
    
    def roll_dice(self):
        if self.phase == "roll" and not self.rolled:
            self.dice.roll()
            self.rolled = True
    
    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        self.phase = "roll"
        self.rolled = False
        self.dice.result_shown = False
        self.steps = 0
    
    def draw(self, screen, map_x, map_y):
        # Слой 1: Карта
        if self.map_image:
            screen.blit(self.map_image, (map_x, map_y))
        else:
            map_rect = pygame.Rect(map_x, map_y, MAP_WIDTH, MAP_HEIGHT)
            pygame.draw.rect(screen, DARK_GREEN, map_rect)
        
        # Слой 2: Путь
        if self.steps_image:
            screen.blit(self.steps_image, (map_x, map_y))
        
        # Рамка
        frame_rect = pygame.Rect(map_x - 3, map_y - 3, MAP_WIDTH + 6, MAP_HEIGHT + 6)
        pygame.draw.rect(screen, GOLD, frame_rect, 3)
        
        # Сетка
        for cell_id, cell in BOARD_CELLS.items():
            cell_x = map_x + cell['x']
            cell_y = map_y + cell['y']
            cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
            
            if cell_id == self.selected_cell:
                pygame.draw.rect(screen, GOLD, cell_rect, 3)
            
            pygame.draw.rect(screen, (255, 255, 255, 30), cell_rect, 1)
        




        print("--- ОТРИСОВКА ИГРОКОВ ---")
        print(f"map_x={map_x}, map_y={map_y}")
        for player in self.players:
            cell = BOARD_CELLS[player.position]
            print(f"  {player.name}: клетка {player.position} ({cell['name']}) x={cell['x']} y={cell['y']}")




        # === Жетоны игроков (исправлено!) ===
        for player in self.players:
            offset = PLAYER_OFFSETS[player.id]
            
            if player.moving and player.draw_x is not None:
                # Анимация — используем координаты анимации
                px = map_x + player.draw_x + offset[0]
                py = map_y + player.draw_y + offset[1]
            else:
                # Статичная позиция
                cell = BOARD_CELLS[player.position]
                px = map_x + cell['x'] + CELL_SIZE // 2 + offset[0]
                py = map_y + cell['y'] + CELL_SIZE // 2 + offset[1]
            
            # Тень
            pygame.draw.circle(screen, (0, 0, 0), (px + 2, py + 2), 14)
            # Жетон
            pygame.draw.circle(screen, player.color, (px, py), 14)
            pygame.draw.circle(screen, WHITE, (px, py), 14, 2)
            
            # Номер
            font_small = pygame.font.Font(None, 20)
            text = font_small.render(str(player.id + 1), True, WHITE)
            text_rect = text.get_rect(center=(px, py))
            screen.blit(text, text_rect)
        
        # Панели
        self.draw_turn_panel(screen)
        self.draw_dice_area(screen)
        self.draw_players_panel(screen)
        
        if self.selected_cell is not None:
            self.draw_cell_info(screen)
    
    def draw_turn_panel(self, screen):
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
            f"Ход: {self.current_player.name}",
            True, self.current_player.color
        )
        screen.blit(turn_text, (panel_x + 10, panel_y + 15))
    
    def draw_dice_area(self, screen):
        dice_x = 30
        dice_y = self.map_y + 100
        
        self.dice.draw(screen, dice_x, dice_y)
        
        mouse_pos = pygame.mouse.get_pos()
        self.roll_button.update(mouse_pos)
        self.roll_button.draw(screen)
        
        if self.phase == "moved":
            hint = self.font.render("ПРОБЕЛ — следующий ход", True, GOLD)
            screen.blit(hint, (dice_x, self.roll_button.rect.y + 60))
    
    def draw_cell_info(self, screen):
        cell = BOARD_CELLS[self.selected_cell]
        
        panel_width = 300
        panel_height = 180
        panel_x = 20
        panel_y = self.screen_height - 420
        
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
    
    def draw_players_panel(self, screen):
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
        for player in self.players:
            pygame.draw.circle(screen, player.color, (panel_x + 25, y_offset + 8), 10)
            pygame.draw.circle(screen, WHITE, (panel_x + 25, y_offset + 8), 10, 1)
            
            if player == self.current_player:
                status = " (идёт...)" if player.moving else ""
                text = self.font.render(f"▶ {player.name}: {player.points} очк.{status}", True, GOLD)
            else:
                text = self.font.render(f"  {player.name}: {player.points} очк.", True, WHITE)
            screen.blit(text, (panel_x + 45, y_offset))
            y_offset += 28