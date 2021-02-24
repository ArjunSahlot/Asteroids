#
#  Asteroids
#  The asteroids game made in pygame
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import pygame, random, math
import numpy as np
from Asteroids.constants import *


class Asteroid:
    def __init__(self, x, y, size=1):
        # size: 1 - biggest, 3 - smallest
        self.x1, self.y1 = x - WIDTH, y - HEIGHT
        self.x2, self.y2 = x, y
        self.x3, self.y3 = x + WIDTH, y + HEIGHT
        self.direction = random.randint(0, 360)
        self.size = self.velocity = size
        self.velocity *= 4 * 30/FPS
        if self.size > 1:
            self.velocity /= 1.4
        if self.size > 2:
            self.velocity /= 1.3
        if self.size == 1:
            self.surf = pygame.Surface((200, 200), pygame.SRCALPHA)
        elif self.size == 2:
            self.surf = pygame.Surface((200*2//3, 200*2//3), pygame.SRCALPHA)
        else:
            self.surf = pygame.Surface((200//3, 200//3), pygame.SRCALPHA)
        self.pairs = []
        self._create_surf()

    def update(self, win):
        self.move()
        self.draw(win)

    def move(self):
        delta_x = self.velocity * math.sin(math.radians(self.direction))
        delta_y = -(self.velocity * math.cos(math.radians(self.direction)))
        self.x1 += delta_x
        self.x2 += delta_x
        self.x3 += delta_x
        self.y1 += delta_y
        self.y2 += delta_y
        self.y3 += delta_y

        if self.x1 + WIDTH < 0:
            self.x1 = self.x3 + WIDTH
        if self.x2 + WIDTH < 0:
            self.x2 = self.x1 + WIDTH
        if self.x3 + WIDTH < 0:
            self.x3 = self.x2 + WIDTH

        if self.x3 - WIDTH > WIDTH:
            self.x3 = self.x1 - WIDTH
        if self.x2 - WIDTH > WIDTH:
            self.x2 = self.x3 - WIDTH
        if self.x1 - WIDTH > WIDTH:
            self.x1 = self.x2 - WIDTH

        if self.y1 + HEIGHT < 0:
            self.y1 = self.y3 + HEIGHT
        if self.y2 + HEIGHT < 0:
            self.y2 = self.y1 + HEIGHT
        if self.y3 + HEIGHT < 0:
            self.y3 = self.y2 + HEIGHT

        if self.y3 - HEIGHT > HEIGHT:
            self.y3 = self.y1 - HEIGHT
        if self.y2 - HEIGHT > HEIGHT:
            self.y2 = self.y3 - HEIGHT
        if self.y1 - HEIGHT > HEIGHT:
            self.y1 = self.y2 - HEIGHT

        self._update_pairs()

    def draw(self, win):
        for x, y in self.pairs:
            win.blit(self.surf, (x, y))

    def split(self, asteroids):
        if self.size != 3:
            asteroids.append(Asteroid(self.x2, self.y2, self.size + 1))
            asteroids.append(Asteroid(self.x2, self.y2, self.size + 1))
        asteroids.remove(self)
        return asteroids

    def collide(self, player):
        player_mask = player.get_mask()
        mask = pygame.mask.from_surface(self.surf)
        if not player.invulnerable:
            for px, py in player.pairs:
                for ax, ay in self.pairs:
                    offset = (round(ax) - round(px), round(ay) - round(py))
                    point = player_mask.overlap(mask, offset)

                    if point:
                        return "crash", None

        for projectile in player.projectiles:
            for px, py in projectile.pairs:
                for ax, ay in self.pairs:
                    projectile_mask = projectile.get_mask()
                    offset = (round(ax) - round(px), round(ay) - round(py))
                    point = projectile_mask.overlap(mask, offset)

                    if point:
                        return "hit", projectile

        return False, None

    def _update_pairs(self):
        xs, ys = sorted([self.x1, self.x2, self.x3]), sorted([self.y1, self.y2, self.y3])
        self.pairs = [(xs[0], ys[1]), (xs[1], ys[0]), (xs[1], ys[1]), (xs[1], ys[2]), (xs[2], ys[2])]

    def _create_surf(self):
        self.surf.fill((0, 0, 0, 0))
        ranges = (
            np.array((0, 0, 20, 20)) * self.surf.get_width() // 100,
            np.array((25, 5, 20, 20)) * self.surf.get_width() // 100,
            np.array((50, 2, 22, 22)) * self.surf.get_width() // 100,
            np.array((75, 20, 25, 25)) * self.surf.get_width() // 100,
            np.array((63, 37, 15, 15)) * self.surf.get_width() // 100,
            np.array((63, 60, 23, 28)) * self.surf.get_width() // 100,
            np.array((50, 80, 10, 15)) * self.surf.get_width() // 100,
            np.array((0, 70, 20, 23)) * self.surf.get_width() // 100,
            np.array((4, 34, 25, 21)) * self.surf.get_width() // 100
        )
        pygame.draw.polygon(self.surf, WHITE, list((random.randint(x, x + w), random.randint(y, y + h)) for x, y, w, h in ranges), 5)


class Player:
    def __init__(self, x=WIDTH//2, y=HEIGHT//2, sensitivity=3, lives=3):
        self.x1, self.y1 = x - WIDTH, y - HEIGHT
        self.x2, self.y2 = x, y
        self.x3, self.y3 = x + WIDTH, y + HEIGHT
        self.width, self.height = 80, 100
        self.lives = lives
        self.direction = 0
        self.turn_speed = 10 * 3/sensitivity * 30/FPS
        self.velocity = 0
        self.acceleration = 2 * 3/sensitivity * 30/FPS
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.move_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._create_surfs()
        self.pairs = []
        self.projectiles = []
        self.moving = False
        self.time = 0
        self.invulnerable = True

    def update(self, win, events):
        self.time += 1
        if self.invulnerable:
            self.invulnerable = False if self.time == 150 else True
        self.move()
        self._update_projectiles(win, events)
        self.draw(win)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction -= 1 * self.turn_speed
        if keys[pygame.K_RIGHT]:
            self.direction += 1 * self.turn_speed
        if keys[pygame.K_UP]:
            self.velocity += 0.2*self.acceleration
            self.velocity = min(self.velocity, 10)
            self.moving = True
        else:
            self.moving = False

        delta_x = self.velocity * math.sin(math.radians(self.direction))
        delta_y = -(self.velocity * math.cos(math.radians(self.direction)))
        self.x1 += delta_x
        self.x2 += delta_x
        self.x3 += delta_x
        self.y1 += delta_y
        self.y2 += delta_y
        self.y3 += delta_y

        if self.x1 + WIDTH < 0:
            self.x1 = self.x3 + WIDTH
        if self.x2 + WIDTH < 0:
            self.x2 = self.x1 + WIDTH
        if self.x3 + WIDTH < 0:
            self.x3 = self.x2 + WIDTH

        if self.x3 - WIDTH > WIDTH:
            self.x3 = self.x1 - WIDTH
        if self.x2 - WIDTH > WIDTH:
            self.x2 = self.x3 - WIDTH
        if self.x1 - WIDTH > WIDTH:
            self.x1 = self.x2 - WIDTH

        if self.y1 + HEIGHT < 0:
            self.y1 = self.y3 + HEIGHT
        if self.y2 + HEIGHT < 0:
            self.y2 = self.y1 + HEIGHT
        if self.y3 + HEIGHT < 0:
            self.y3 = self.y2 + HEIGHT

        if self.y3 - HEIGHT > HEIGHT:
            self.y3 = self.y1 - HEIGHT
        if self.y2 - HEIGHT > HEIGHT:
            self.y2 = self.y3 - HEIGHT
        if self.y1 - HEIGHT > HEIGHT:
            self.y1 = self.y2 - HEIGHT

        self._update_pairs()

        if not self.moving:
            # self.velocity /= 1.03
            self.velocity -= 0.06
            self.velocity = max(self.velocity, 0)

    def draw(self, win):
        surf = pygame.transform.rotate(self.surf, -self.direction)
        move_surf = pygame.transform.rotate(self.move_surf, -self.direction)
        rect = surf.get_rect(center=self.surf.get_rect().center)
        if not self.invulnerable:
            if not self.moving:
                for x, y in self.pairs:
                    win.blit(surf, (x + rect.x, y + rect.y))
            else:
                for x, y in self.pairs:
                    win.blit(move_surf, (x + rect.x, y + rect.y))
        else:
            pygame.display.update()
            win.blit(surf, (self.x2 + rect.x, self.y2 + rect.y))

    def make_invulnerable(self):
        self.invulnerable = True
        self.time = 0

    def hit(self):
        self._reset()

    def get_mask(self):
        return pygame.mask.from_surface(self.surf)

    def _add_projectiles(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and len(self.projectiles) < 10 and self.time % 25 == 0:
            self.projectiles.append(Projectile(self))
        for event in events:
            if event.type == pygame.KEYDOWN and len(self.projectiles) < 10:
                if event.key == pygame.K_SPACE:
                    self.projectiles.append(Projectile(self))

    def _update_projectiles(self, win, events):
        self._add_projectiles(events)
        rem = []
        for projectile in self.projectiles:
            projectile.update(win)
            if projectile.time == 150:
                rem.append(projectile)

        for projectile in rem:
            self.projectiles.remove(projectile)

    def _update_pairs(self):
        xs, ys = sorted([self.x1, self.x2, self.x3]), sorted([self.y1, self.y2, self.y3])
        self.pairs = [(xs[0], ys[1]), (xs[1], ys[0]), (xs[1], ys[1]), (xs[1], ys[2]), (xs[2], ys[2])]

    def _create_surfs(self):
        pygame.draw.line(self.surf, WHITE, (0 * self.width//100, 100 * self.height//100), (50 * self.width//100, 0 * self.height//100), 5)
        pygame.draw.line(self.surf, WHITE, (50 * self.width//100, 0 * self.height//100), (100 * self.width//100, 100 * self.height//100), 5)
        pygame.draw.line(self.surf, WHITE, (15 * self.width//100, 70 * self.height//100), (85 * self.width//100, 70 * self.height//100), 5)
        self.move_surf.blit(self.surf, (0, 0))
        pygame.draw.polygon(self.move_surf, WHITE, ((32 * self.width//100, 70 * self.height//100), (50 * self.width//100, 100 * self.height//100), (68 * self.width//100, 70 * self.height//100)), 5)

    def _reset(self):
        self.__init__(lives=self.lives-1)


class Projectile:
    def __init__(self, player):
        self.player = player
        self.x1, self.y1 = player.x1 + player.surf.get_width()//2, player.y1 + player.surf.get_height()//2
        self.x2, self.y2 = player.x2 + player.surf.get_width()//2, player.y2 + player.surf.get_height()//2
        self.x3, self.y3 = player.x3 + player.surf.get_width()//2, player.y3 + player.surf.get_height()//2
        self.direction = player.direction
        self.velocity = 5
        self.velocity *= 7 * 30/FPS
        self.surf = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, WHITE, (3, 3), 3)
        self.pairs = []
        self.time = 0
        for _ in range(2):
            self.move()

    def update(self, win):
        self.move()
        self.draw(win)

    def move(self):
        self.time += 1
        delta_x = self.velocity * math.sin(math.radians(self.direction))
        delta_y = -(self.velocity * math.cos(math.radians(self.direction)))
        self.x1 += delta_x
        self.x2 += delta_x
        self.x3 += delta_x
        self.y1 += delta_y
        self.y2 += delta_y
        self.y3 += delta_y

        if self.x1 + WIDTH < 0:
            self.x1 = self.x3 + WIDTH
        if self.x2 + WIDTH < 0:
            self.x2 = self.x1 + WIDTH
        if self.x3 + WIDTH < 0:
            self.x3 = self.x2 + WIDTH

        if self.x3 - WIDTH > WIDTH:
            self.x3 = self.x1 - WIDTH
        if self.x2 - WIDTH > WIDTH:
            self.x2 = self.x3 - WIDTH
        if self.x1 - WIDTH > WIDTH:
            self.x1 = self.x2 - WIDTH

        if self.y1 + HEIGHT < 0:
            self.y1 = self.y3 + HEIGHT
        if self.y2 + HEIGHT < 0:
            self.y2 = self.y1 + HEIGHT
        if self.y3 + HEIGHT < 0:
            self.y3 = self.y2 + HEIGHT

        if self.y3 - HEIGHT > HEIGHT:
            self.y3 = self.y1 - HEIGHT
        if self.y2 - HEIGHT > HEIGHT:
            self.y2 = self.y3 - HEIGHT
        if self.y1 - HEIGHT > HEIGHT:
            self.y1 = self.y2 - HEIGHT

        self._update_pairs()

    def draw(self, win):
        for x, y in self.pairs:
            win.blit(self.surf, (x, y))

    def get_mask(self):
        return pygame.mask.from_surface(self.surf)

    def _update_pairs(self):
        xs, ys = sorted([self.x1, self.x2, self.x3]), sorted([self.y1, self.y2, self.y3])
        self.pairs = [(xs[0], ys[1]), (xs[1], ys[0]), (xs[1], ys[1]), (xs[1], ys[2]), (xs[2], ys[2])]
