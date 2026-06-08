import pygame
import random
from settings import *

class Player:
    """Класс игрока"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 5
        self.color = BLUE
        
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
            
        # Границы
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Enemy:
    """Класс врага"""
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(0, SCREEN_HEIGHT - self.height)
        self.speed = 2
        self.color = (255, 0, 0)
        
    def update(self, player_x, player_y):
        # Движение к игроку
        if self.x < player_x:
            self.x += self.speed
        elif self.x > player_x:
            self.x -= self.speed
            
        if self.y < player_y:
            self.y += self.speed
        elif self.y > player_y:
            self.y -= self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class GameWorld:
    """Основной игровой мир"""
    def __init__(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = [Enemy() for _ in range(5)]
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
        # Загрузка фона
        try:
            self.background = pygame.image.load(BACKGROUND_IMAGE)
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
            
    def update(self, keys):
        self.player.update(keys)
        
        for enemy in self.enemies:
            enemy.update(self.player.x, self.player.y)
            
            # Проверка столкновения
            if self.player.get_rect().colliderect(enemy.get_rect()):
                return False  # Игра окончена
                
        return True  # Игра продолжается
        
    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(DARK_GREEN)
            
        self.player.draw(screen)
        
        for enemy in self.enemies:
            enemy.draw(screen)
            
        # Отображение счёта
        score_text = self.font.render(f"Счёт: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
    def add_score(self):
        self.score += 1