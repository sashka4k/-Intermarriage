import pygame
import sys
from settings import *
from menu import MainMenu, PauseMenu
from game import GameWorld

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Междуземье")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Состояния игры
        self.state = "menu"  # menu, game, pause, game_over
        
        # Инициализация меню
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
        
        # Загрузка фона для меню
        try:
            self.menu_background = pygame.image.load(BACKGROUND_IMAGE)
            self.menu_background = pygame.transform.scale(self.menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.menu_background = None
            
        self.game_world = None
        
    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                # Обработка событий в зависимости от состояния
                if self.state == "menu":
                    action = self.main_menu.handle_click(mouse_pos, event)
                    if action == "new_game":
                        self.start_new_game()
                        self.state = "game"
                    elif action == "exit":
                        self.running = False
                        
                elif self.state == "game":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "pause"
                            
                elif self.state == "pause":
                    action = self.pause_menu.handle_click(mouse_pos, event)
                    if action == "resume":
                        self.state = "game"
                    elif action == "main_menu":
                        self.state = "menu"
                    elif action == "exit":
                        self.running = False
                        
                elif self.state == "game_over":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.start_new_game()
                            self.state = "game"
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "menu"
            
            # Обновление в зависимости от состояния
            if self.state == "menu":
                self.main_menu.update(mouse_pos)
                
            elif self.state == "game":
                keys = pygame.key.get_pressed()
                game_running = self.game_world.update(keys)
                if not game_running:
                    self.state = "game_over"
                    
            elif self.state == "pause":
                self.pause_menu.update(mouse_pos)
            
            # Отрисовка
            if self.state == "menu":
                self.main_menu.draw(self.screen, self.menu_background)
                
            elif self.state == "game":
                self.game_world.draw(self.screen)
                
            elif self.state == "pause":
                self.game_world.draw(self.screen)  # Фон игры
                self.pause_menu.draw(self.screen)   # Меню паузы поверх
                
            elif self.state == "game_over":
                self.game_world.draw(self.screen)
                # Рисуем экран Game Over
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))
                
                font = pygame.font.Font(None, 72)
                game_over = font.render("GAME OVER", True, (255, 0, 0))
                game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                self.screen.blit(game_over, game_over_rect)
                
                font_small = pygame.font.Font(None, 36)
                restart = font_small.render("Нажми ENTER для новой игры или ESC для выхода в меню", True, WHITE)
                restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                self.screen.blit(restart, restart_rect)
                
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()
        
    def start_new_game(self):
        """Начинает новую игру"""
        self.game_world = GameWorld()

if __name__ == "__main__":
    game = Game()
    game.run()