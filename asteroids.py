#!python3

import pygame
import math
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
PLAYER_WIN = pygame.USEREVENT+1
PLAYER_LOSE = pygame.USEREVENT+2
TURN_SPEED = math.pi / 60
ACCELERATION = 0.5
BULLET_SPEED = 5
BULLET_TTL = 30
ASTEROID_COUNT = 3

def wrap(rect):
    if rect.centery > SCREEN_HEIGHT:
        rect.centery = 1
    elif rect.centery < 0:
        rect.centery = SCREEN_HEIGHT-1
    elif rect.centerx > SCREEN_WIDTH:
        rect.centerx = 1
    elif rect.centerx < 0:
        rect.centerx = SCREEN_WIDTH-1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, center, direction, ship_speed):
        super(Bullet, self).__init__()
        BULLET_LENGTH = 10
        BULLET_WIDTH = 2
        self.ttl = BULLET_TTL
        speed = ship_speed + BULLET_SPEED
        self.velocity = (speed * math.cos(direction),
                         speed* math.sin(direction))
        base_surf = pygame.Surface((BULLET_LENGTH, BULLET_WIDTH))
        base_surf.fill(COLOR_RED)
        self.surf = pygame.transform.rotate(
            base_surf, -direction*180/math.pi)
        self.rect = self.surf.get_rect(center=center)

    def update(self):
        self.ttl -= 1
        if self.ttl <= 0:
            self.kill()
        self.rect.move_ip(self.velocity)
        wrap(self.rect)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, center):
        super(Player, self).__init__()
        SHIP_WIDTH = 50
        SHIP_HEIGHT = 30
        self.img = pygame.Surface((SHIP_WIDTH,SHIP_HEIGHT))
        self.surf = self.img
        self.surf.set_colorkey((0,0,0))
        pygame.draw.polygon(self.surf, COLOR_YELLOW,
        ((0,0), (SHIP_WIDTH,SHIP_HEIGHT//2), (0,SHIP_HEIGHT)), 0)
        self.rect = self.surf.get_rect(center=center)
        self.direction = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.bullets = pygame.sprite.Group()

    def update(self, pressed_keys):
        # Direction update
        if pressed_keys[K_LEFT]:
            self.direction -= TURN_SPEED
        if pressed_keys[K_RIGHT]:
            self.direction += TURN_SPEED
        self.surf = pygame.transform.rotate(
            self.img, -self.direction*180/math.pi)
        center = self.rect.center
        self.rect = self.surf.get_rect(center=center)
        # Acceleration Update
        accel_abs = 0.0
        if pressed_keys[K_UP]:
            accel_x = ACCELERATION * math.cos(self.direction)
            accel_y = ACCELERATION * math.sin(self.direction)
            self.vel_x += accel_x
            self.vel_y += accel_y
        # Breaking effect
        if pressed_keys[K_DOWN]:
            speed = math.hypot(self.vel_x, self.vel_y)
            if speed > 0:
                accel_x = -ACCELERATION * self.vel_x/speed
                accel_y = -ACCELERATION * self.vel_y/speed
                if abs(self.vel_x) > abs(accel_x):
                    self.vel_x += accel_x
                else:
                    self.vel_x = 0
                if abs(self.vel_y) > abs(accel_y):
                    self.vel_y += accel_y
                else:
                    self.vel_y = 0
        # Shooting Update
        if pressed_keys[K_SPACE]:
            self.bullets.add(Bullet(
                self.rect.center, self.direction,
                math.hypot(self.vel_x, self.vel_y)))
        # Velocity and Position update
        self.rect.move_ip((self.vel_x, self.vel_y))
        wrap(self.rect)
        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super(Asteroid, self).__init__()
        self.diameter = random.randint(20,50)
        self.center_x = random.random() * SCREEN_WIDTH
        self.center_y = random.random() * SCREEN_HEIGHT
        self.velocity_x = random.random() * 3
        self.velocity_y = random.random() * 3
        self.surf = pygame.Surface((self.diameter, self.diameter))
        pygame.draw.circle(self.surf, COLOR_WHITE,
            (self.diameter//2, self.diameter//2), self.diameter//2)
        self.rect = self.surf.get_rect(center=(self.center_x, self.center_y))

    def update(self):
        self.center_x += self.velocity_x
        self.center_y += self.velocity_y
        self.rect.center = (self.center_x, self.center_y)
        wrap(self.rect)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player((SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    asteroids = pygame.sprite.Group()
    for i in range(ASTEROID_COUNT):
        asteroids.add(Asteroid())
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pressed_keys = pygame.key.get_pressed()
        screen.fill(COLOR_BLACK)
        player.update(pressed_keys)
        if pygame.sprite.spritecollideany(player, asteroids):
            running = False
        for asteroid in asteroids:
            asteroid.update()
        for bullet in player.bullets:
            pygame.sprite.spritecollide(bullet, asteroids, True)
        for sprite in [player] + player.bullets.sprites() + asteroids.sprites():
            sprite.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
