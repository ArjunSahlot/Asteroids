import pygame, os, random
from Asteroids.constants import *
from Asteroids.classes import Asteroid, Player


# Window Management
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_width//2-WIDTH//2, screen_height//2-HEIGHT//2)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids, By: Arjun Sahlot")


def draw_window(win, width, height, asteroids, player, events):
    win.fill(BLACK)
    for asteroid in asteroids:
        asteroid.update(win)
    player.update(win, events)


def main(win, width, height):
    run = True
    asteroids = [Asteroid(100, 100)]
    player = Player(WIDTH//2, HEIGHT//2)
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        events = pygame.event.get()
        draw_window(win, width, height, asteroids, player, events)
        for asteroid in asteroids:
            if asteroid.player_collide(player):
                player.hit()
                asteroids = asteroid.split(asteroids)
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                exit()
        pygame.display.update()


main(WINDOW, WIDTH, HEIGHT)
