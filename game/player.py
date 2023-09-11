import pygame
from .config import SIZE, SPEED
import os
from .player_shot import PlayerShot
from .damage_indicator import DamageIndicator
from .health_bar import HealthBar

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(
            'Sprites', 'Wizard_skin1.png')).convert_alpha()
        self.animations = [pygame.image.load(os.path.join(
            'Sprites', 'Wizard_skin1.png')).convert_alpha(),
            pygame.image.load(os.path.join(
                'Sprites', 'Wizard_skin2.png')).convert_alpha()]
        self.flipped_animations = [pygame.transform.flip(image, True, False)
                              for image in self.animations]
        self.animation_state = 0
        self.rect = self.image.get_rect(midbottom=(SIZE[0] // 2, SIZE[1] - 50))
        self.player_left = False
        self.max_health = 1000
        self.health = self.max_health

    def move_player(self, speed):
        keys_pressed = pygame.key.get_pressed()
        # Animate player walking while moving or shooting
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d] \
                or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s] \
                or pygame.mouse.get_pressed()[0]:
            #When moving or shooting left, flip all image animations
            if not self.player_left:
                self.image = self.animations[int(self.animation_state) % 2]
                self.animation_state += 0.1
            else: 
                self.image = self.flipped_animations[int(self.animation_state) % 2]
                self.animation_state += 0.1
        #Move self.rect within frame
        if keys_pressed[pygame.K_w] and self.rect.y - speed > 0:
            self.rect.y -= speed
        if keys_pressed[pygame.K_a] and self.rect.x - speed > 0:
            self.rect.x -= speed
            self.player_left = True
        if keys_pressed[pygame.K_s] and self.rect.y + self.rect.height + speed < SIZE[1]:
            self.rect.y += speed
        if keys_pressed[pygame.K_d] and self.rect.x + self.rect.width + speed < SIZE[0]:
            self.rect.x += speed
            self.player_left = False

    def shoot(self, mouse_pos):
        player_to_mouse_vector = pygame.math.Vector2(
            x=(mouse_pos[0] - self.rect.x - 20), y=(mouse_pos[1] - self.rect.y + 10))
        mouse_angle_from_player = player_to_mouse_vector.angle_to((1, 0))
        # Rotate player to face shooting direction
        if -90 < mouse_angle_from_player < 90:
            self.player_left = False
        else:
            self.player_left = True
        return PlayerShot(mouse_angle_from_player, self.rect.x + 50, self.rect.y + 20)

    def check_hit(self, enemy_bullets, damage_indicator_group):
        for bullet in enemy_bullets:
            if pygame.sprite.collide_rect(self, bullet):
                self.health -= bullet.damage
                bullet.kill()
                damage_indicator = DamageIndicator(
                    bullet.damage, self.rect.x + self.rect.width // 2, self.rect.y - 20)
                damage_indicator_group.add(damage_indicator)

    def update(self, enemy_bullets, damage_indicator_group):
        self.move_player(SPEED)
        self.check_hit(enemy_bullets, damage_indicator_group)
        HealthBar(10, 10, self.max_health, self.health, 700, 40).update()
        if self.health < 0: 
            pygame.quit()
