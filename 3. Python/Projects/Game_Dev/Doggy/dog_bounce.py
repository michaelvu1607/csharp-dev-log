import pygame as pygame
from random import randint
import time
from os.path import join
# setup
pygame.init()

WIDTH = 1920
HEIGHT = 1080
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# plain surface
surf = pygame.Surface((100, 200))
surf.fill("orange")

# importing images
player_surf = pygame.image.load(join("PythonProjects", "Game_Dev", "Doggy", "5100114.png")).convert_alpha()

# rect
player_rect =  player_surf.get_frect(center = (WIDTH/2,HEIGHT/2))

player_dir = pygame.math.Vector2(10, 10)

running = True
clock = pygame.time.Clock()
k = 50

while running:
    # clock
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill('darkgray')

    #mvnt
    player_rect.center += player_dir * k * dt

    if round(player_rect.top) <= 0:
        player_dir.y *= -1
        player_rect.top = 0
    if round(player_rect.bottom) >= HEIGHT:
        player_dir.y *= -1
        player_rect.bottom = HEIGHT
    if round(player_rect.left) <= 0:
        player_dir.x *= -1
        player_rect.left = 0

    if round(player_rect.right) >= WIDTH:
        player_dir.x *= -1
        player_rect.right = WIDTH



    # draw game
    display_surface.blit(player_surf, player_rect)

    pygame.display.update()
 
pygame.quit()