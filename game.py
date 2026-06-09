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
        self.can_move = False  # можно ли начать движение

        self.fork_cell = None        # клетка развилки (ждёт выбора)
        self.fork_options = []       # варианты путей [cell_id, cell_id]
        self.fork_arrows = []        # координаты стрелок [(x, y, dx, dy), ...]
        self.steps_remaining = 0     # оставшиеся шаги после выбора
        self.pending_path = []       # путь, который ждёт завершения

        # Карты
        self.selected_card_index = None  # выбранная карта в руке
        self.card_played_this_turn = False  # одну карту за ход

        # Кнопка просмотра руки
        self.hand_button = Button(
            30,
            self.map_y + 230,
            200, 40,
            "Карты (0)", BLUE, LIGHT_BLUE
        )

        button_width = 200
        button_height = 50
        button_x = 30
        button_y = self.map_y + 170  # единая позиция для обеих кнопок

        self.roll_button = Button(
            button_x, button_y,
            button_width, button_height,
            "Бросить кубики", BLUE, LIGHT_BLUE
        )

        # Кнопка "Идти" — на том же месте, появляется после броска
        self.move_button = Button(
            button_x, button_y,
            button_width, button_height,
            "Идти", BLUE, LIGHT_BLUE
        )
        
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
        
        self.font = pygame.font.Font(None, 28)
        self.font_title = pygame.font.Font(None, 36)
    
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
    
    def is_fork(self, cell_id):
        """Проверяет, есть ли в клетке развилка (больше одного пути)"""
        cell = BOARD_CELLS[cell_id]
        paths = [p for p in cell['PATH'] if p != -1]
        return len(paths) >= 2

    def update(self, keys=None):
        """Обновление игрового мира"""
        self.dice.update()
    
        for player in self.players:
            player.update_move()
    
        # Проверяем завершение броска и окончание анимации движения
        if self.dice.result_shown and self.phase == "roll":
            self.steps = self.dice.get_total()
            self.phase = "wait_move"  # ждём нажатия кнопки "Идти"
    
        # Ждём окончания анимации (обычное движение)
        if self.phase == "moving":
            all_stopped = all(not p.is_moving() for p in self.players)
            if all_stopped:
                self.phase = "moved"
                # Проверка: попал ли игрок на клетку с картой
                if self.current_player.position in CARD_CELLS:
                    self.give_random_card()

        # Ждём прибытия на развилку
        if self.phase == "fork_wait" and self.fork_arrows == []:
            all_stopped = all(not p.is_moving() for p in self.players)
            if all_stopped:
                self.calculate_fork_arrows()
    
    def roll_dice(self):
        """Бросок кубиков — можно только в фазе roll и если ещё не бросали"""
        if self.phase == "roll" and not self.rolled:
            self.dice.roll()
            self.rolled = True
    
    def start_movement(self):
        """Начать движение — проверяет развилки по пути"""
        if self.phase != "wait_move":
            return
    
        # Строим путь по шагам
        path = [self.current_player.position]
        current = self.current_player.position
        steps_left = self.steps
    
        for _ in range(steps_left):
            cell = BOARD_CELLS[current]
            valid_paths = [p for p in cell['PATH'] if p != -1]
        
            if len(valid_paths) == 1:
                # Один путь — идём сразу
                current = valid_paths[0]
                path.append(current)
            elif len(valid_paths) >= 2:
                # Развилка! Запоминаем и останавливаемся
                self.fork_cell = current
                self.fork_options = valid_paths
                self.steps_remaining = steps_left - len(path) + 1
                # Путь до развилки (включая саму развилку)
                self.pending_path = path
                # Запускаем движение до развилки
                self.current_player.start_move(path)
                self.phase = "fork_wait"
                return
            else:
                # Тупик
                break
    
        # Если развилок нет — идём до конца
        self.current_player.start_move(path)
        self.phase = "moving"

    def next_turn(self):
        """Переход хода — только если никто не двигается"""
        # Защита: нельзя сменить ход во время анимации
        if any(player.is_moving() for player in self.players):
            return
    
        if self.phase not in ("moved", "wait_move"):
            return
    
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        self.phase = "roll"
        self.rolled = False
        self.dice.reset()  # используем новый метод reset()
        self.steps = 0

        self.card_played_this_turn = False
        self.selected_card_index = None
        self.current_player.hand.visible = False
        self.update_hand_button_text()
    
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

        # === Жетоны игроков (исправлено!) ===
        for player in self.players:
            offset = PLAYER_OFFSETS[player.id]
            player.draw(screen, map_x, map_y, offset)
        
        # Слой 5: Стрелки развилок
        if self.phase == "fork_wait" and self.fork_arrows:
            for arrow in self.fork_arrows:
                ax = map_x + arrow['x']
                ay = map_y + arrow['y']
                adx = arrow['dx']
                ady = arrow['dy']
        
                # Основание стрелки
                arrow_size = 30
                tip_x = ax + adx * arrow_size
                tip_y = ay + ady * arrow_size
        
                # Перпендикуляр для крыльев стрелки
                wing_x = -ady * 10
                wing_y = adx * 10
        
                # Рисуем стрелку
                points = [
                    (tip_x, tip_y),
                    (ax + wing_x, ay + wing_y),
                    (ax - wing_x, ay - wing_y)
                ]
                pygame.draw.polygon(screen, GOLD, points)
                pygame.draw.polygon(screen, WHITE, points, 2)

        # Панели
        self.draw_turn_panel(screen)
        self.draw_dice_area(screen)

        # Кнопка просмотра карт
        mouse_pos = pygame.mouse.get_pos()
        self.hand_button.update(mouse_pos)
        self.hand_button.draw(screen)

        # Рука карт (если открыта)
        self.current_player.hand.draw(screen, self.screen_width, self.screen_height)

        # Подсказка при ожидании телепорта/постройки
        if self.selected_card_index is not None:
            hand = self.current_player.hand
            if hand.count() > self.selected_card_index:
                card = hand.get_cards()[self.selected_card_index]
                if card.type == "teleport":
                    hint = self.font.render("Кликните по клетке для телепорта", True, GOLD)
                    hint_rect = hint.get_rect(center=(self.screen_width // 2, self.screen_height - 270))
                    screen.blit(hint, hint_rect)
                elif card.type == "building":
                    hint = self.font.render("Кликните по клетке для постройки", True, GOLD)
                    hint_rect = hint.get_rect(center=(self.screen_width // 2, self.screen_height - 270))
                    screen.blit(hint, hint_rect)

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
    
        # Кнопка "Бросить кубики" или "Идти" — на одном месте
        if self.phase == "roll" and not self.rolled:
            self.roll_button.update(mouse_pos)
            self.roll_button.draw(screen)
        elif self.phase == "wait_move":
            self.move_button.update(mouse_pos)
            self.move_button.draw(screen)
        elif self.phase == "moved":
            hint = self.font.render("ПРОБЕЛ — следующий ход", True, GOLD)
            hint_x = self.move_button.rect.x
            hint_y = self.move_button.rect.y
            screen.blit(hint, (hint_x, hint_y))
    
    def draw_cell_info(self, screen):
        cell = BOARD_CELLS[self.selected_cell]
        
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
                text = self.font.render(f"> {player.name}: {player.points} очк.{status}", True, GOLD)
            else:
                text = self.font.render(f"  {player.name}: {player.points} очк.", True, WHITE)
            screen.blit(text, (panel_x + 45, y_offset))
            y_offset += 28
    
    def calculate_fork_arrows(self):
        """Вычисляет позиции стрелок для выбора направления на развилке"""
        self.fork_arrows = []
    
        if self.fork_cell is None:
            return
    
        cell_from = BOARD_CELLS[self.fork_cell]
        cx = cell_from['x'] + CELL_SIZE // 2
        cy = cell_from['y'] + CELL_SIZE // 2
    
        for target_id in self.fork_options:
            cell_to = BOARD_CELLS[target_id]
            tx = cell_to['x'] + CELL_SIZE // 2
            ty = cell_to['y'] + CELL_SIZE // 2
        
            # Направление вектора
            dx = tx - cx
            dy = ty - cy
        
            # Длина вектора
            import math
            length = math.sqrt(dx * dx + dy * dy)
            if length > 0:
                dx /= length
                dy /= length
        
            # Стрелка на середине между центрами клеток
            arrow_x = cx + dx * CELL_SIZE * 0.55
            arrow_y = cy + dy * CELL_SIZE * 0.55
        
            self.fork_arrows.append({
                'x': arrow_x,
                'y': arrow_y,
                'dx': dx,
                'dy': dy,
                'target': target_id
            })
    
    def choose_fork(self, target_id):
        """Игрок выбрал направление на развилке"""
        if self.phase != "fork_wait":
            return
    
        if target_id not in self.fork_options:
            return
    
        # Строим оставшийся путь от выбранной клетки
        current = target_id
        remaining_path = [current]
        steps_left = self.steps_remaining - 1  # минус один шаг на переход с развилки
    
        for _ in range(steps_left):
            cell = BOARD_CELLS[current]
            valid_paths = [p for p in cell['PATH'] if p != -1]
            if valid_paths:
                # Берём первый доступный (дальше без развилок)
                current = valid_paths[0]
                remaining_path.append(current)
            else:
                break
    
        # Полный путь: pending_path (уже прошли) + remaining_path
        # Но pending_path уже анимирован, начинаем с текущей позиции
        full_path = [self.fork_cell] + remaining_path
    
        self.current_player.start_move(full_path)
        self.fork_cell = None
        self.fork_options = []
        self.fork_arrows = []
        self.steps_remaining = 0
        self.pending_path = []
        self.phase = "moving"
    
    def get_fork_click(self, mouse_pos):
        """Проверяет, попал ли клик по одной из стрелок развилки"""
        mx, my = mouse_pos
    
        for arrow in self.fork_arrows:
            ax = self.map_x + arrow['x']
            ay = self.map_y + arrow['y']
        
            # Проверяем расстояние от клика до центра стрелки
            dist = ((mx - ax) ** 2 + (my - ay) ** 2) ** 0.5
            if dist < 35:  # радиус попадания
                return arrow['target']
    
        return None
    
    def toggle_hand(self):
        """Показать/скрыть руку карт"""
        self.current_player.hand.toggle_visible()
        self.selected_card_index = None
        self.update_hand_button_text()

    def update_hand_button_text(self):
        """Обновить текст на кнопке руки"""
        count = self.current_player.hand.count()
        self.hand_button.text = f"Карты ({count})"

    def play_card(self, index):
        """Сыграть карту из руки"""
        if self.card_played_this_turn:
            return False
    
        hand = self.current_player.hand
        if index < 0 or index >= hand.count():
            return False
    
        card = hand.get_cards()[index]
    
        # Применяем эффект карты
        if card.type == "points":
            self.current_player.points += 100
            self.current_player.hand.remove_card(index)
            self.card_played_this_turn = True
            self.selected_card_index = None
            self.update_hand_button_text()
            return True
    
        elif card.type == "teleport":
            # Телепорт — ждём клика по карте
            self.selected_card_index = index
            return "teleport_pending"
    
        elif card.type == "building":
            # Постройка — ждём клика по карте
            self.selected_card_index = index
            return "building_pending"
    
        return False

    def confirm_teleport(self, cell_id):
        """Подтвердить телепорт на клетку"""
        if self.selected_card_index is None:
            return False
    
        hand = self.current_player.hand
        card = hand.get_cards()[self.selected_card_index]
    
        if card.type != "teleport":
            return False
    
        # Перемещаем игрока
        self.current_player.position = cell_id
        self.current_player.draw_x = None
        self.current_player.draw_y = None
        self.current_player.moving = False
    
        hand.remove_card(self.selected_card_index)
        self.card_played_this_turn = True
        self.selected_card_index = None
        self.update_hand_button_text()
        return True

    def confirm_building(self, cell_id):
        """Подтвердить постройку на клетке"""
        if self.selected_card_index is None:
            return False
    
        hand = self.current_player.hand
        card = hand.get_cards()[self.selected_card_index]
    
        if card.type != "building":
            return False
    
        # Здесь будет логика постройки (пока просто заглушка)
        print(f"Постройка на клетке {cell_id}!")
    
        hand.remove_card(self.selected_card_index)
        self.card_played_this_turn = True
        self.selected_card_index = None
        self.update_hand_button_text()
        return True

    def give_random_card(self):
        """Выдать случайную карту текущему игроку"""
        import random
        card_type = random.choice(["building", "teleport", "points"])
        from card import Card
        card = Card(card_type)
        self.current_player.hand.add_card(card)
        self.update_hand_button_text()

    def give_starting_cards(self):
        """Выдать стартовые карты всем игрокам"""
        import random
        from card import Card
    
        for player in self.players:
            for _ in range(2):
                card_type = random.choice(["building", "teleport", "points"])
                card = Card(card_type)
                player.hand.add_card(card)
    
        self.update_hand_button_text()