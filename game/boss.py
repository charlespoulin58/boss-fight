import pygame, os, math, random
from .enemy_shot import EnemyShot
from.damage_indicator import DamageIndicator
from .health_bar import HealthBar
from .config import SIZE

#Handles boss and minnion movement and attack patterns. 
class Boss(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        BOSS_IDLE_1 = pygame.image.load(
            os.path.join('Sprites', 'Boss_idle_1.png')).convert_alpha()
        BOSS_IDLE_2 = pygame.image.load(
            os.path.join('Sprites', 'Boss_idle_2.png')).convert_alpha()
        self.boss_idleing = [BOSS_IDLE_1, BOSS_IDLE_2]
        self.image = BOSS_IDLE_1
        self.animation_state = 0
        self.rect = self.image.get_rect(
            center=(SIZE[0] // 2, SIZE[1] // 2 - 50))
        self.speed = 4
        self.max_health = 10_000
        self.health = self.max_health
        self.target = player
        self.last_attack = 0

    def animate(self):
        #Animate between two movement images.
        self.image = self.boss_idleing[int(self.animation_state) % 2]
        self.animation_state += 0.01
    

    def random_movement(self, left_bound, right_bound, up_bound, down_bound):
        # For every frame, boss will chose to move verticle and/or horizontally at random
        # Contain boss in center region of screen
        move = random.randint(0, 8)
        up_down_move = random.randint(0, 1)
        side_move = random.randint(0, 1)
        if move == 1:
            if up_down_move and up_bound < self.rect.y + random.choice((-self.speed, self.speed)) < down_bound:
                self.rect.y += random.choice((-self.speed, self.speed))
            if side_move and left_bound < self.rect.x + random.choice((-self.speed, self.speed)) < right_bound:
                self.rect.x += random.choice((-self.speed, self.speed))

    def charge(self, players):
        #Boss will charge at the players current location
        for player in players:
            player_x, player_y = player.rect.x, player.rect.y
            player_to_self_vector = pygame.math.Vector2(
                x=(player_x - self.rect.x), y=(player_y - self.rect.y))
            angle = player_to_self_vector.angle_to((1, 0))
        self.rect.x += self.speed * \
                math.cos(math.radians(angle)) + random.randint(-2, 2)
        self.rect.y += -1 * self.speed * \
                math.sin(math.radians(angle)) + random.randint(-2, 2)

    def attack(self, bullet_group, image, angle, damage, range, vel):
        bullet_group.add(EnemyShot(image, self.rect.centerx,
                         self.rect.centery, angle, damage, range, vel))

    def check_hit(self, player_shot, damage_indicator_group):
        # If collides with player shot, decrement health and create a damage_indicator object
        for shot in player_shot:
            if pygame.sprite.collide_rect(self, shot):
                self.health -= shot.damage  # - ATK
                damage_indicator = DamageIndicator(
                    shot.damage, self.rect.x + self.rect.width // 2, self.rect.y - 20)
                damage_indicator_group.add(damage_indicator)
                shot.kill()

    def summon_minnion(self, minion_group):
        #Summon a minion near current location
        summon_x = self.rect.x + random.randint(-50, 50)
        summon_y = self.rect.y + random.randint(0, 50)
        minion_group.add(BossSummons(summon_x, summon_y, self.target))
    
    def passive_summon_phase(self, minion_group, bullet_group): 
    #First phase: Boss will idle in center of screen and summon minnions periodically
        self.random_movement(300, 700, 100, 600)
        if pygame.time.get_ticks() - self.last_attack > 1200:
            self.last_attack = pygame.time.get_ticks()
            for angle in range(0, 360, 60):
                self.attack(bullet_group, 'Fire_bolt.png',
                        angle, 100, 500, 3)
            self.summon_minnion(minion_group)
    
    def targeted_shotgun(self, bullet_group):
        #Move back to center
        self.player_to_self_vector = pygame.math.Vector2(
                x=(self.target.rect.x - self.rect.x), y=(self.target.rect.y - self.rect.y))
        self.attack_angle = self.player_to_self_vector.angle_to((1, 0))
        if pygame.time.get_ticks() - self.last_attack > 1800:
            self.last_attack = pygame.time.get_ticks()
            for angle in [self.attack_angle + 30 * i for i in [-1, 0, 1]]:
                self.attack(bullet_group, "Large_fireball.png", angle, 150, 700, 10)

    def update(self, player_shot, damage_indicator_group, player,  bullet_group, minion_group):
        self.animate()
        self.check_hit(player_shot, damage_indicator_group)
        HealthBar(self.rect.x, self.rect.y + self.rect.height,
                  self.max_health, self.health, self.rect.width).update()
        
        if self.health / self.max_health > 0.75:
            self.random_movement(300, 700, 100, 600)
            self.passive_summon_phase(minion_group, bullet_group) #Phase 1
        elif self.health / self.max_health > 0.25:
            self.random_movement(300, 700, 100, 600)
            self.targeted_shotgun(bullet_group)
        else: 
            self.charge(player)
        

        if self.health <= 0:
            self.kill()

class BossSummons(Boss):
    '''This class handles the logic of the minnions that the boss summons. 
    Minions charge at the player while repeatedly firing short-range and low damage shots. 
    Charge behavior is inherited from the Boss class.'''
    def __init__(self, spawn_x, spawn_y, player):
        super().__init__(player)
        MINION_IDLE_1 = pygame.image.load(
            os.path.join('Sprites', 'Minion_idle1.png')).convert_alpha()
        MINION_IDLE_2 = pygame.image.load(
            os.path.join('Sprites', 'Minion_idle2.png')).convert_alpha()
        self.image = MINION_IDLE_1
        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
        self.idleing = [MINION_IDLE_1, MINION_IDLE_2]
        self.animation_state = 0
        self.max_health = 300
        self.health = self.max_health
        self.speed = 3

    def animate(self):
        self.animation_state -= .012
        self.image = self.idleing[int(self.animation_state) % 2]

    def update(self, player_shot, damage_indicator_group, player, bullet_group):
        self.animate()
        self.check_hit(player_shot, damage_indicator_group)
        self.charge(player)
        HealthBar(self.rect.x, self.rect.y + self.rect.height,
                  self.max_health, self.health, self.rect.width).update()

        # Short range, single shot attack pattern. Shoots directly at player
        player_to_self_vector = pygame.math.Vector2(
            x=(self.target.rect.x - self.rect.x), y=(self.target.rect.y - self.rect.y))
        attack_angle = player_to_self_vector.angle_to((1, 0))
        if pygame.time.get_ticks() - self.last_attack > 300:
            self.last_attack = pygame.time.get_ticks()
            self.attack(bullet_group, 'Fire_bolt.png',
                        attack_angle, random.randint(30, 70), 150, 10)

        if self.health <= 0:
            self.kill()