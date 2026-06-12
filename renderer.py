import pygame
from settings import *
from ui import Button

class Renderer:
    """Отвечает за всю отрисовку игрового мира"""
    
    def __init__(self, screen_width, screen_height, map_x, map_y):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # КАРТА НА КООРДИНАТАХ 688, 96
        self.map_x = 688
        self.map_y = 96
        
        # Шрифты
        self.font = pygame.font.Font(None, 28)
        self.font_title = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 20)
        
        # Изображения карты
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
        
        # ЗАДНИЙ ФОН (1920x1080) - вместо чёрного экрана
        try:
            self.background = pygame.image.load("Prefabs/Pictures/game_background.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = None
    
    def draw(self, screen, game_world):
        """Главный метод отрисовки всего игрового мира"""
        
        # РИСУЕМ ЗАДНИЙ ФОН (на весь экран)
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Слой 1: Карта
        self.draw_map(screen)
        
        # Слой 2: Путь
        self.draw_steps(screen)

        # Слой 2.5: Ландшафт и здания
        self.draw_landscape_and_buildings(screen)
        
        # Слой 3: Сетка и выделение
        self.draw_grid(screen, game_world.selected_cell)
        
        # Слой 4: Игроки
        self.draw_players(screen, game_world.players)
        
        # Слой 5: Стрелки развилок
        self.draw_fork_arrows(screen, game_world)
        
        # Интерфейс
        self.draw_turn_panel(screen, game_world.current_player, game_world.turn_count, game_world.total_turns)
        self.draw_dice_area(screen, game_world)
        self.draw_hand_button(screen, game_world)
        self.draw_hand(screen, game_world)
        self.draw_card_hint(screen, game_world)
        self.draw_players_panel(screen, game_world)
        
        if game_world.selected_cell is not None:
            self.draw_cell_info(screen, game_world.selected_cell, game_world.players)
    
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
            
            arrow_size = 45
            tip_x = ax + adx * arrow_size
            tip_y = ay + ady * arrow_size
            
            wing_x = -ady * 15
            wing_y = adx * 15
            
            points = [
                (tip_x, tip_y),
                (ax + wing_x, ay + wing_y),
                (ax - wing_x, ay - wing_y)
            ]
            pygame.draw.polygon(screen, GOLD, points)
            pygame.draw.polygon(screen, WHITE, points, 2)
    
    # === Панели интерфейса ===
    
    def draw_turn_panel(self, screen, current_player, turn_count=0, total_turns=0):
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
        screen.blit(turn_text, (panel_x + 10, panel_y + 10))

        # Счётчик раундов
        round_text = self.font.render(f"Раунд: {turn_count}/{total_turns}", True, GOLD)
        screen.blit(round_text, (panel_x + 10, panel_y + 38))
    
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
    
    def draw_cell_info(self, screen, selected_cell, players=None):
        cell = BOARD_CELLS[selected_cell]
    
        panel_width = 300
        panel_height = 170
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
    
        # Теги
        tags_text = ", ".join(cell['tags'])
        type_text = self.font.render(f"Теги: {tags_text}", True, WHITE)
        screen.blit(type_text, (panel_x + 10, y_offset))
        y_offset += 25

        # Ландшафт
        landscape = LANDSCAPES.get(selected_cell)
        if landscape:
            landscape_name = "Каньон" if landscape == "canyon" else landscape
            land_text = self.font.render(f"Ландшафт: {landscape_name}", True, (200, 150, 100))
            screen.blit(land_text, (panel_x + 10, y_offset))
            y_offset += 25
    
        # Постройка
        building = BUILDINGS.get(selected_cell)
        if building:
            bname = BUILDING_TYPES[building['building']]['name']
            build_text = self.font.render(f"Постройка: {bname}", True, WHITE)
            screen.blit(build_text, (panel_x + 10, y_offset))
            y_offset += 25
        
            if building['owner'] is not None:
                owner_name = players[building['owner']].name if players else f"Игрок {building['owner'] + 1}"
                owner_text = self.font.render(f"Владелец: {owner_name}", True, WHITE)
            else:
                owner_text = self.font.render("Общее здание", True, WHITE)
            screen.blit(owner_text, (panel_x + 10, y_offset))
            y_offset += 25
    
        # Связи
        connections = [str(p) for p in cell['PATH'] if p != -1]
        conn_text = self.font.render(f"Связи: {', '.join(connections) if connections else 'нет'}", True, WHITE)
        screen.blit(conn_text, (panel_x + 10, y_offset))
    
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
    
    def draw_landscape_and_buildings(self, screen):
        for cell_id, cell in BOARD_CELLS.items():
            cell_x = self.map_x + cell['x']
            cell_y = self.map_y + cell['y']
            cx = cell_x + CELL_SIZE // 2
            cy = cell_y + CELL_SIZE // 2
        
            # Ландшафт (каньон)
            landscape = LANDSCAPES.get(cell_id)
            if landscape == "canyon":
                rect = pygame.Rect(cell_x + 20, cell_y + 20, CELL_SIZE - 40, CELL_SIZE - 40)
                pygame.draw.rect(screen, (139, 90, 43), rect, border_radius=5)
                pygame.draw.rect(screen, (100, 60, 20), rect, 3, border_radius=5)
                label = self.font_small.render("⛔", True, WHITE)
                label_rect = label.get_rect(center=(cx, cy))
                screen.blit(label, label_rect)
        
            # Постройки
            building = BUILDINGS.get(cell_id)
            if building:
                btype = building['building']
                bcolor = BUILDING_TYPES[btype]['color']
            
                rect = pygame.Rect(cell_x + 15, cell_y + 15, CELL_SIZE - 30, CELL_SIZE - 30)
                pygame.draw.rect(screen, bcolor, rect, border_radius=8)
            
                if building['owner'] is not None:
                    owner_color = PLAYER_COLORS[building['owner']]
                    pygame.draw.rect(screen, owner_color, rect, 3, border_radius=8)
                    label = self.font_small.render("Ч", True, WHITE)
                else:
                    pygame.draw.rect(screen, GOLD, rect, 2, border_radius=8)
                    label = self.font_small.render("О", True, BLACK)
            
                label_rect = label.get_rect(center=(cx, cy))
                screen.blit(label, label_rect)
    
    def draw_game_over_screen(self, screen, rating_table, winners=None):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
    
        font_title = pygame.font.Font(None, 72)
        font_winner = pygame.font.Font(None, 48)
        font_record = pygame.font.Font(None, 36)
        font_hint = pygame.font.Font(None, 28)
    
        title = font_title.render("ИГРА ОКОНЧЕНА", True, GOLD)
        title_rect = title.get_rect(center=(self.screen_width // 2, 40))
        screen.blit(title, title_rect)
    
        # Победители
        if winners:
            if len(winners) == len(rating_table.records) and len(winners) > 1:
                winner_text = "НИЧЬЯ!"
                winner_color = WHITE
            elif len(winners) == 1:
                winner_text = f"Победитель: {winners[0].name} ({winners[0].points} очк.)"
                winner_color = winners[0].color
            else:
                names = ", ".join(w.name for w in winners)
                winner_text = f"Победители: {names} ({winners[0].points} очк.)"
                winner_color = GOLD
        
            winner_render = font_winner.render(winner_text, True, winner_color)
            winner_rect = winner_render.get_rect(center=(self.screen_width // 2, 100))
            screen.blit(winner_render, winner_rect)
    
        subtitle = font_record.render("Таблица рекордов:", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(subtitle, subtitle_rect)
    
        records = rating_table.get_records()
        start_y = 190
        
        header_name = font_record.render("Игрок", True, GOLD)
        header_points = font_record.render("Очки", True, GOLD)
        screen.blit(header_name, (self.screen_width // 2 - 150, start_y))
        screen.blit(header_points, (self.screen_width // 2 + 50, start_y))
        pygame.draw.line(screen, GOLD,
                        (self.screen_width // 2 - 180, start_y + 35),
                        (self.screen_width // 2 + 180, start_y + 35), 2)
        
        for i, record in enumerate(records):
            y = start_y + 50 + i * 40
            color = PLAYER_COLORS[i % 4] if i < 4 else WHITE
            
            num_text = font_record.render(f"{i + 1}.", True, color)
            name_text = font_record.render(record["name"], True, color)
            points_text = font_record.render(str(record["points"]), True, GOLD)
            
            screen.blit(num_text, (self.screen_width // 2 - 200, y))
            screen.blit(name_text, (self.screen_width // 2 - 150, y))
            screen.blit(points_text, (self.screen_width // 2 + 50, y))
        
        if not records:
            empty_text = font_record.render("Нет рекордов", True, GRAY)
            empty_rect = empty_text.get_rect(center=(self.screen_width // 2, start_y + 40))
            screen.blit(empty_text, empty_rect)
        
        hint = font_hint.render("Кликните или нажмите любую клавишу для выхода в меню", True, GRAY)
        hint_rect = hint.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        screen.blit(hint, hint_rect)