import pygame, os, random
from Asteroids.constants import *
from Asteroids.classes import Asteroid, Player

# Window Management
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_width // 2 - WIDTH // 2, screen_height // 2 - HEIGHT // 2)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids, By: Arjun Sahlot")


def create_asteroids(n):
    asteroids = []
    for _ in range(n):
        asteroids.append(Asteroid(random.randint(0, WIDTH-200), random.randint(0, HEIGHT-200)))

    return asteroids


def draw_window(win, width, height, asteroids, player, events, score, max_score):
    win.fill(BLACK)
    for asteroid in asteroids:
        asteroid.update(win)
    player.update(win, events)
    text1 = FONT.render(f"Max Score: {max_score}", 1, WHITE)
    text2 = FONT.render(f"Score: {score}", 1, WHITE)
    win.blit(text1, (WIDTH - text1.get_width() - 5, 5))
    win.blit(text2, (WIDTH - text2.get_width() - 5, 5 + 5 + text1.get_height()))
    text3 = FONT.render(f"Lives: {player.lives}", 1, WHITE)
    win.blit(text3, (5, 5))
    small_surf = pygame.transform.scale(player.surf, (50, 65))
    for i in range(player.lives):
        win.blit(small_surf, (80*i + 5, 5 + text3.get_height() + 5))
    if player.lives == 0:
        pygame.display.update()
        pygame.time.delay(2000)
        with open("max_score.txt", "w") as f:
            f.write(str(max_score))
        exit()


def check_collision(player, asteroids, score, n):
    for asteroid in asteroids:
        mesg = asteroid.collide(player)
        if mesg[0] == "hit":
            asteroids = asteroid.split(asteroids)
            if asteroid.size == 3:
                score += 100
            elif asteroid.size == 2:
                score += 50
            else:
                score += 20
            player.projectiles.remove(mesg[1])
        if mesg[0] == "crash":
            player.hit()
            if mesg[0] == "hit":
                asteroids = asteroid.split(asteroids)
                if asteroid.size == 3:
                    score += 100
                elif asteroid.size == 2:
                    score += 50
                else:
                    score += 20
            asteroids = asteroid.split(asteroids)

    return player, asteroids, score, n


def main(win, width, height):
    asteroids = []
    player = Player(WIDTH // 2, HEIGHT // 2)
    clock = pygame.time.Clock()
    score = n = 0

    try:
        with open("max_score.txt", "r") as f:
            max_score = int(f.readline())

    except FileNotFoundError:
        max_score = 0

    run = True
    while run:
        clock.tick(FPS)
        events = pygame.event.get()
        if len(asteroids) == 0:
            n += 1
            n = min(n, 7)
            player.make_invulnerable()
            asteroids = create_asteroids(n)
        draw_window(win, width, height, asteroids, player, events, score, max_score)
        player, asteroids, score, n = check_collision(player, asteroids, score, n)
        if score > max_score:
            max_score = score
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                with open("max_score.txt", "w") as f:
                    f.write(str(max_score))
                exit()
        pygame.display.update()


main(WINDOW, WIDTH, HEIGHT)
