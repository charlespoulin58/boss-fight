import pygame
import os
import math
import random
from game.boss import Boss
from game.player import Player
from game.config import SCREEN, SCREEN_IMG, MAX_FPS, ATK_SPEED

#Handles drawing the background as well as all sprites. Parameters are the 
#sprite groups
def draw_window(player, player_shots, boss_group, damage_indicator_group,
                boss_minion_group, enemy_shot_group):
    SCREEN.blit(SCREEN_IMG, (0, 0))

    player.draw(SCREEN)
    player.update(enemy_shot_group, damage_indicator_group)

    player_shots.draw(SCREEN)
    player_shots.update()

    boss_group.draw(SCREEN)
    boss_group.update(player_shots, damage_indicator_group,
                      player, enemy_shot_group, boss_minion_group)

    damage_indicator_group.draw(SCREEN)
    damage_indicator_group.update()

    boss_minion_group.draw(SCREEN)
    boss_minion_group.update(
        player_shots, damage_indicator_group, player, enemy_shot_group)

    enemy_shot_group.draw(SCREEN)
    enemy_shot_group.update()

    pygame.display.update()

#Main game loop. Sprite groups are initialized here. 
def main():
    pygame.init()

    player = Player()
    player_group_single = pygame.sprite.GroupSingle()
    player_group_single.add(player)
    player_shots = pygame.sprite.Group()

    boss = Boss(player)
    boss_group = pygame.sprite.Group()
    boss_group.add(boss)

    boss_minion_group = pygame.sprite.Group()
    enemy_shot_group = pygame.sprite.Group()

    damage_indicator_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True
    last_shot_time = 0
    while running:
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player shoot on click with cooldown
        if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - last_shot_time > ATK_SPEED:
            last_shot_time = pygame.time.get_ticks()
            player_shots.add(player.shoot(pygame.mouse.get_pos()))

        draw_window(player_group_single, player_shots, boss_group,
                    damage_indicator_group, boss_minion_group, enemy_shot_group)

    pygame.quit()


if __name__ == '__main__':
    main()
