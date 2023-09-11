import pygame, random, math, os
from .config import SIZE, BULLET_VEL

class PlayerShot(pygame.sprite.Sprite):
    def __init__(self, angle, player_x, player_y):
        # Spawn bullet at player position and process angle traj
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load(
            os.path.join('Sprites', 'Player_projectile.png')),
            angle).convert_alpha()
        self.rect = self.image.get_rect(center=(player_x, player_y))
        self.angle = angle
        self.damage = random.randint(110, 220)

    def handle_shot_movement(self):
        self.rect.x += BULLET_VEL * math.cos(math.radians(self.angle))
        self.rect.y += -1 * BULLET_VEL * math.sin(math.radians(self.angle))

    def update(self):
        self.handle_shot_movement()
        # Kill when offscreen
        if not 0 < self.rect.x < SIZE[0] or not 0 < self.rect.y < SIZE[1]:
            self.kill()
