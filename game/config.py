import pygame, os

# Intiialize window
SIZE = (1000, 700)
SCREEN_IMG = pygame.image.load(os.path.join('Sprites', 'Dungeon_floor.png'))
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Boss Battle')

MAX_FPS = 60

# Player Stats
SPEED = 5
BULLET_VEL = 10
ATK_SPEED = 200