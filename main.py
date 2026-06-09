import pygame
import sys
from settings import *
from menu import MainMenu, PauseMenu, PlayerSetupMenu
from game import GameWorld
from player import Player

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
        
        self.map_x = self.SCREEN_WIDTH - MAP_WIDTH - MAP_MARGIN_RIGHT
        self.map_y = MAP_MARGIN_TOP
        
        self.state = "menu"
        
        self.main_menu = MainMenu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.player_setup = PlayerSetupMenu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.pause_menu = PauseMenu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        self.game_world = None
        
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

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                
                elif self.state == "game":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # Проверка кнопки броска
                        if self.game_world.phase == "roll" and self.game_world.roll_button.is_clicked(mouse_pos, event):
                            self.game_world.roll_dice()
                        # Проверка кнопки "Идти"
                        elif self.game_world.phase == "wait_move" and self.game_world.move_button.is_clicked(mouse_pos, event):
                            self.game_world.start_movement()
                        else:
                            # Клик по карте
                            cell_id = self.game_world.get_cell_at_mouse(mouse_pos)
                            if cell_id is not None:
                                self.game_world.select_cell(cell_id)
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                        # next_turn сам проверит, можно ли сменить ход
                            self.game_world.next_turn()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "pause"
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "pause"

                
                elif self.state == "pause":
                    action = self.pause_menu.handle_click(mouse_pos, event)
                    if action == "resume":
                        self.state = "game"
                    elif action == "main_menu":
                        self.state = "menu"
                    elif action == "exit":
                        self.running = False

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "game"
            
            # === Обновление ===
            if self.state == "menu":
                self.main_menu.update(mouse_pos)
            elif self.state == "player_setup":
                self.player_setup.update(mouse_pos)
            elif self.state == "game":
                keys = pygame.key.get_pressed()
                self.game_world.update(keys)
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
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def start_new_game(self, names):
        players = []
        for i, name in enumerate(names):
            player = Player(name, PLAYER_COLORS[i], i)
            players.append(player)
        
        self.game_world = GameWorld(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 
                                     self.map_x, self.map_y, players)

if __name__ == "__main__":
    game = Game()
    game.run()