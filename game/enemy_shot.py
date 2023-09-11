import pygame, os, math

class EnemyShot(pygame.sprite.Sprite):
    #This class handles the movement of all enemy shots. Enemy position (x, y), shot angle,
    #shot damage, range, and velocity are passed for each instance.
    def __init__(self, image, x, y, angle, damage, range, vel):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load(
            os.path.join('Sprites', image)).convert_alpha(), angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.x, self.y, self.angle = x, y, angle
        self.damage = damage
        self.range = range
        self.vel = vel

    def handle_movement(self):
        self.rect.x += self.vel * math.cos(math.radians(self.angle))
        self.rect.y += -1 * self.vel * math.sin(math.radians(self.angle))
        #Limit range
        if math.sqrt((self.rect.x - self.x) ** 2 + (self.rect.y - self.y) ** 2) > self.range:
            self.kill()

    def update(self):
        self.handle_movement()
