import pygame
from .config import SCREEN

class HealthBar():
    # Basic health bar below each sprite. Will change color based on health
    def __init__(self, x, y, max_health, current_health, width, height=10):
        self.x, self.y = x, y
        self.current_health = current_health
        self.health_percent = current_health / max_health \
            if current_health / max_health > 0 else -0.0001
        self.width = width * self.health_percent
        self.height = height
        # Healthbar color changes from green to red based on percent health
        self.color = (46 + (1-self.health_percent) * 154,
                      127 - (1-self.health_percent) * 90,
                      24 + (1-self.health_percent) * 32)

    def update(self):
        pygame.draw.rect(SCREEN, self.color,
                         (self.x, self.y, self.width, self.height))
