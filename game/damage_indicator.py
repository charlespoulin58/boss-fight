import pygame

class DamageIndicator(pygame.sprite.Sprite):
    def __init__(self, damage, x, y):
        # Collect damage done by shot, and location of target hit.
        #  Damage will float above affected sprite and last for a second
        super().__init__()
        self.damage = damage
        self.font = pygame.font.SysFont('Arial', 30, bold=True)
        self.image = self.font.render(str(self.damage), False, (200, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 60  # Display time in frames

    def update(self):
        self.timer -= 1
        self.rect.y -= 1.5
        if self.timer <= 0:
            self.kill()

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
