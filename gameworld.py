import pygame
import random
import math
from settings import *
from ui import ImageButton
from card import Card
from renderer import Renderer
from dice import Dice

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
        self.can_move = False
        
        self.fork_cell = None
        self.fork_options = []
        self.fork_arrows = []
        self.steps_remaining = 0
        self.pending_path = []
        
        self.selected_card_index = None
        self.card_played_this_turn = False
        self.canyon_players = {}

        button_width = 260
        button_height = 65
        button_x = 30
        button_y = self.map_y + 170
        
        # Кнопка "Бросить кубики" с изображением
        self.roll_button = ImageButton(
            button_x, button_y,
            button_width, button_height,
            "Prefabs/Pictures/button_roll.png",
            "Prefabs/Pictures/button_roll_hover.png"
        )
        
        # Кнопка "Идти" с изображением
        self.move_button = ImageButton(
            button_x, button_y,
            button_width, button_height,
            "Prefabs/Pictures/button_move.png",
            "Prefabs/Pictures/button_move_hover.png"
        )
        
        # Кнопка "Карты" с изображением
        self.hand_button = ImageButton(
            30,
            self.map_y + 250,
            260, 55,
            "Prefabs/Pictures/button_hand.png",
            "Prefabs/Pictures/button_hand_hover.png"
        )
        
        self.renderer = Renderer(screen_width, screen_height, map_x, map_y)
        
        self.font = pygame.font.Font(None, 28)
    
    # === Игровой цикл ===
    
    def update(self):
        self.dice.update()
        
        for player in self.players:
            player.update_move()
        
        if self.dice.result_shown and self.phase == "roll":
            self.steps = self.dice.get_total()
            self.phase = "wait_move"
        
        if self.phase == "moving":
            all_stopped = all(not p.is_moving() for p in self.players)
            if all_stopped:
                self.phase = "moved"
                self.apply_cell_effect()
                if self.current_player.position in CARD_CELLS:
                    self.give_random_card()

        if self.phase == "step_moving":
            all_stopped = all(not p.is_moving() for p in self.players)
            if all_stopped:
                # Один шаг завершён — пробуем следующий
                self.do_step()
    
    # === Карта и клетки ===
    
    def select_cell(self, cell_id):
        self.selected_cell = cell_id
    
    def get_cell_at_mouse(self, mouse_pos):
        mx, my = mouse_pos
        map_mx = mx - self.map_x
        map_my = my - self.map_y
        
        if 0 <= map_mx < MAP_WIDTH and 0 <= map_my < MAP_HEIGHT:
            col = map_mx // CELL_SIZE
            row_from_top = map_my // CELL_SIZE
            row_from_bottom = 6 - row_from_top
            cell_id = row_from_bottom * 9 + col
            if cell_id in BOARD_CELLS:
                return cell_id
        return None
    
    def is_fork(self, cell_id):
        cell = BOARD_CELLS[cell_id]
        paths = [p for p in cell['PATH'] if p != -1]
        return len(paths) >= 2
    
    # === Кубики и ход ===
    
    def roll_dice(self):
        if self.phase == "roll" and not self.rolled:
            self.dice.roll()
            self.rolled = True
    
    def start_movement(self):
        if self.phase != "wait_move":
            return
    
        self.steps_remaining = self.steps
        self.do_step()

    def do_step(self):
        """Сделать один шаг. Если развилка — остановиться и ждать выбора."""
        if self.steps_remaining <= 0:
            self.phase = "moving"
            return
    
        current = self.current_player.position
        cell = BOARD_CELLS[current]
        valid_paths = [p for p in cell['PATH'] if p != -1]
        
        if len(valid_paths) == 0:
            self.phase = "moving"
            return
        
        if len(valid_paths) == 1:
            # Один путь — идём сразу
            target = valid_paths[0]
            self.current_player.start_move([current, target])
            self.steps_remaining -= 1
            self.phase = "step_moving"
        else:
            # Развилка — ждём выбора
            self.fork_cell = current
            self.fork_options = valid_paths
            self.calculate_fork_arrows()
            self.phase = "fork_wait"
 
    def next_turn(self):
        if any(p.is_moving() for p in self.players):
            return
        if self.phase != "moved":
            return
    
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
    
        if self.canyon_players.get(self.current_player.id, False):
            self.canyon_players[self.current_player.id] = False
            self.phase = "moved"
            self.rolled = False
            self.dice.reset()
            self.steps = 0
            self.card_played_this_turn = False
            self.selected_card_index = None
            self.current_player.hand.visible = False
            self.update_hand_button_text()
            return
    
        self.phase = "roll"
        self.rolled = False
        self.dice.reset()
        self.steps = 0
        self.card_played_this_turn = False
        self.selected_card_index = None
        self.current_player.hand.visible = False
        self.update_hand_button_text()
    
    # === Развилки ===
    
    def calculate_fork_arrows(self):
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
            
            dx = tx - cx
            dy = ty - cy
            
            length = math.sqrt(dx * dx + dy * dy)
            if length > 0:
                dx /= length
                dy /= length
            
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
        if self.phase != "fork_wait":
            return
    
        if target_id not in self.fork_options:
            return
    
        # Делаем шаг в выбранном направлении
        self.current_player.start_move([self.fork_cell, target_id])
        self.steps_remaining -= 1
        
        self.fork_cell = None
        self.fork_options = []
        self.fork_arrows = []
        
        self.phase = "step_moving"
        
    def get_fork_click(self, mouse_pos):
        mx, my = mouse_pos
        
        for arrow in self.fork_arrows:
            ax = self.map_x + arrow['x']
            ay = self.map_y + arrow['y']
            
            dist = ((mx - ax) ** 2 + (my - ay) ** 2) ** 0.5
            if dist < 50:
                return arrow['target']
        
        return None
    
    # === Карты ===
    
    def toggle_hand(self):
        self.current_player.hand.toggle_visible()
        self.selected_card_index = None
        self.update_hand_button_text()
    
    def update_hand_button_text(self):
        count = self.current_player.hand.count()
        #Саня: пока что уберу потому что не отображается на кнопках кошличаество карт 
        #self.hand_button.text = f"Карты ({count})" 
    
    def play_card(self, index):
        if self.card_played_this_turn:
            return False
    
        hand = self.current_player.hand
        if index < 0 or index >= hand.count():
            return False
    
        card = hand.get_cards()[index]
    
        if card.type == "points":
            self.current_player.points += 100
            hand.remove_card(index)
            self.card_played_this_turn = True
            self.selected_card_index = None
            self.update_hand_button_text()
            return True
    
        elif card.type == "teleport":
            self.selected_card_index = index
            return "teleport_pending"
    
        elif card.required_tag is not None:
            self.selected_card_index = index
            return "building_pending"

        elif card.is_landscape:
            self.selected_card_index = index
            return "landscape_pending"
    
        return False
    
    def confirm_teleport(self, cell_id):
        if self.selected_card_index is None:
            return False
    
        hand = self.current_player.hand
        card = hand.get_cards()[self.selected_card_index]
    
        if card.type != "teleport":
            return False
    
        cell = BOARD_CELLS[cell_id]
        if cell['PATH'] == [-1]:
            return False
    
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
        if self.selected_card_index is None:
            return False
    
        hand = self.current_player.hand
        card = hand.get_cards()[self.selected_card_index]
    
        if card.required_tag is None:
            return False
    
        cell = BOARD_CELLS[cell_id]
    
        if card.required_tag not in cell['tags']:
            return False
    
        if cell_id in BUILDINGS:
            return False
    
        if cell_id == self.current_player.position:
            BUILDINGS[cell_id] = {"building": card.type, "owner": self.current_player.id}
        else:
            BUILDINGS[cell_id] = {"building": card.type, "owner": None}
    
        hand.remove_card(self.selected_card_index)
        self.card_played_this_turn = True
        self.selected_card_index = None
        self.update_hand_button_text()
        return True
    
    def confirm_landscape(self, cell_id):
        if self.selected_card_index is None:
            return False
    
        hand = self.current_player.hand
        card = hand.get_cards()[self.selected_card_index]
    
        if not card.is_landscape:
            return False
    
        cell = BOARD_CELLS[cell_id]
    
        if cell_id in LANDSCAPES:
            return False
        if cell_id in BUILDINGS:
            return False
    
        LANDSCAPES[cell_id] = card.type
    
        hand.remove_card(self.selected_card_index)
        self.card_played_this_turn = True
        self.selected_card_index = None
        self.update_hand_button_text()
        return True
    
    def give_random_card(self):
        building_types = ["fisher_hut", "quarry", "sawmill", "farm", "canyon"]
        card_type = random.choice(["teleport", "points"] + building_types)
        card = Card(card_type)
        self.current_player.hand.add_card(card)
        self.update_hand_button_text()

    def give_starting_cards(self):
        building_types = ["fisher_hut", "quarry", "sawmill", "farm", "canyon"]
        for player in self.players:
            for _ in range(2):
                card_type = random.choice(["teleport", "points"] + building_types)
                card = Card(card_type)
                player.hand.add_card(card)
        self.update_hand_button_text()
    
    def apply_cell_effect(self):
        cell = BOARD_CELLS[self.current_player.position]
        tags = cell['tags']
    
        landscape = LANDSCAPES.get(self.current_player.position)

        if landscape == "canyon":
            self.canyon_players[self.current_player.id] = True
            return
    
        building = BUILDINGS.get(self.current_player.position)
        if building:
            if building['owner'] is not None:
                self.players[building['owner']].points += BUILDING_TYPES[building['building']]['profit']
            else:
                for p in self.players:
                    p.points += 20
    
    # === Отрисовка ===
    
    def draw(self, screen, map_x, map_y):
        self.renderer.draw(screen, self)