import pygame
import sys
from settings import *
from menu import MainMenu, PauseMenu, PlayerSetupMenu
from gameworld import GameWorld
from player import Player
from rating import RatingTable

class Game:
    def __init__(self):
        pygame.init()
        
        info = pygame.display.Info()
        self.SCREEN_WIDTH = info.current_w
        self.SCREEN_HEIGHT = info.current_h
        
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            pygame.FULLSCREEN
        )
        pygame.display.set_caption("Междуземье")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # КАРТА НА КООРДИНАТАХ 688, 96
        self.map_x = 688
        self.map_y = 96
        
        self.state = "menu"
        
        self.main_menu = MainMenu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.player_setup = PlayerSetupMenu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.pause_menu = PauseMenu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        self.game_world = None

        self.rating_table = RatingTable()
        
        try:
            self.menu_background = pygame.image.load(BACKGROUND_IMAGE)
            self.menu_background = pygame.transform.scale(
                self.menu_background, 
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            )
        except:
            self.menu_background = None
    
    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.state == "player_setup":
                    self.player_setup.handle_event(event)
                
                # === Обработка по состояниям ===
                if self.state == "menu":
                    action = self.main_menu.handle_click(mouse_pos, event)
                    if action == "new_game":
                        self.state = "player_setup"
                    elif action == "exit":
                        self.running = False
                
                elif self.state == "player_setup":
                    action = self.player_setup.handle_click(mouse_pos, event)
                    if action == "start_game":
                        names = self.player_setup.get_player_names()
                        self.start_new_game(names)
                        self.state = "game"
                    elif action == "back":
                        self.state = "menu"
                
                elif self.state == "game":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # Если рука открыта — проверяем клик по карте
                        if self.game_world.current_player.hand.visible:
                            card_idx = self.game_world.current_player.hand.get_clicked_card(
                                mouse_pos, self.SCREEN_WIDTH, self.SCREEN_HEIGHT
                            )
                            if card_idx is not None:
                                result = self.game_world.play_card(card_idx)
                                if result == "teleport_pending":
                                    pass
                                elif result == "building_pending":
                                    pass
                                elif result == "landscape_pending":
                                    pass
                                continue
                        
                        # Если ждём телепорт или постройку — клик по карте
                        if self.game_world.selected_card_index is not None:
                            cell_id = self.game_world.get_cell_at_mouse(mouse_pos)
                            if cell_id is not None:
                                hand = self.game_world.current_player.hand
                                if self.game_world.selected_card_index < hand.count():
                                    card = hand.get_cards()[self.game_world.selected_card_index]
                                    if card.type == "teleport":
                                        self.game_world.confirm_teleport(cell_id)
                                    elif card.required_tag is not None:
                                        self.game_world.confirm_building(cell_id)
                                    elif card.is_landscape:
                                        self.game_world.confirm_landscape(cell_id)
                                continue
                        
                        # Кнопка просмотра руки
                        if self.game_world.hand_button.is_clicked(mouse_pos, event):
                            self.game_world.toggle_hand()
                            continue
                        
                        # Кнопка броска
                        if self.game_world.phase == "roll" and self.game_world.roll_button.is_clicked(mouse_pos, event):
                            self.game_world.roll_dice()
                            continue
                        
                        # Кнопка "Идти"
                        if self.game_world.phase == "wait_move" and self.game_world.move_button.is_clicked(mouse_pos, event):
                            self.game_world.start_movement()
                            continue
                        
                        # Стрелки развилок
                        if self.game_world.phase == "fork_wait":
                            target = self.game_world.get_fork_click(mouse_pos)
                            if target is not None:
                                self.game_world.choose_fork(target)
                            continue
                        
                        # Обычный клик по карте
                        cell_id = self.game_world.get_cell_at_mouse(mouse_pos)
                        if cell_id is not None:
                            self.game_world.select_cell(cell_id)
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_world.next_turn()
                            if self.game_world.is_game_over():
                                self.end_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "pause"
                        elif event.key == pygame.K_TAB:
                            self.game_world.toggle_hand()
                
                elif self.state == "pause":
                    action = self.pause_menu.handle_click(mouse_pos, event)
                    if action == "resume":
                        self.state = "game"
                    elif action == "main_menu":
                        self.end_game()
                    elif action == "exit":
                        self.running = False
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "game"
                
                elif self.state == "game_over":
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        self.state = "menu"
            
            # === Обновление ===
            if self.state == "menu":
                self.main_menu.update(mouse_pos)
            elif self.state == "player_setup":
                self.player_setup.update(mouse_pos)
            elif self.state == "game":
                self.game_world.update()
            elif self.state == "pause":
                self.pause_menu.update(mouse_pos)
            
            # === Отрисовка ===
            self.screen.fill(BLACK)
            
            if self.state == "menu":
                self.main_menu.draw(self.screen, self.menu_background)
            elif self.state == "player_setup":
                self.player_setup.draw(self.screen, self.menu_background)
            elif self.state == "game":
                self.game_world.draw(self.screen, self.map_x, self.map_y)
            elif self.state == "pause":
                self.game_world.draw(self.screen, self.map_x, self.map_y)
                self.pause_menu.draw(self.screen)
            elif self.state == "game_over":
                self.draw_game_over_screen()
            
            pygame.display.flip()
            self.clock.tick(60)

            fps = self.clock.get_fps()
            if int(fps) < 50:
                print(f"FPS: {fps:.0f}")
        
        pygame.quit()
        sys.exit()

    def end_game(self):
        """Завершение игры — сохранить результаты и показать таблицу"""
        if not self.game_world:
            return
    
        for player in self.game_world.players:
            self.rating_table.add_result(player.name, player.points)
    
        self.winners = self.game_world.get_winners()
        self.state = "game_over"
    
    def start_new_game(self, names):
        players = []
        for i, name in enumerate(names):
            player = Player(name, PLAYER_COLORS[i], i)
            players.append(player)
        
        self.game_world = GameWorld(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 
                                     self.map_x, self.map_y, players)
        self.game_world.give_starting_cards()
    
    def draw_game_over_screen(self):
        if self.game_world:
            winners = getattr(self, 'winners', None)
            self.game_world.renderer.draw_game_over_screen(self.screen, self.rating_table, winners)