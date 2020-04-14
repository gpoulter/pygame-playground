#!python3
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
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
PLAYER_WIN = pygame.USEREVENT+1
PLAYER_LOSE = pygame.USEREVENT+2


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super(Paddle, self).__init__()
        self.surf = pygame.Surface((100, 25))
        self.surf.fill(COLOR_GREEN)
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-self.surf.get_height()/2))

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(+10, 0)
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self, blocks, paddle):
        super(Ball, self).__init__()
        self.blocks = blocks
        self.paddle = paddle
        self.surf = pygame.Surface((10,10))
        self.surf.fill(COLOR_WHITE)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        self.velocity = (-3,3)

    def update(self):
        self.rect.move_ip(self.velocity)
        if self.rect.bottom > SCREEN_HEIGHT:
            pygame.event.post(PLAYER_LOSE)
        if self.rect.top < 0:
            pygame.event.post(PLAYER_WIN)

        dx, dy = self.velocity
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            dx = -dx
        else:
            block = pygame.sprite.spritecollideany(self, self.blocks)
            if block is not None:
                if block is not self.paddle:
                    block.kill()
                if self.rect.top < block.rect.bottom or self.rect.bottom > block.rect.top:
                    dy = -dy
                if ((self.rect.right > block.rect.left and self.rect.left < block.rect.left)
                    or
                    (self.rect.left < block.rect.right and self.rect.right > block.rect.right)):
                    dx = -dx
        self.velocity = (dx, dy)


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Brick, self).__init__()
        self.surf = pygame.Surface((60,30))
        self.surf.fill(COLOR_WHITE)
        self.rect = self.surf.get_rect(center=pos)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    blocks = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    for row in range(0, 11):
        for column in range(0, 5):
            brick = Brick((50+70*row,20+40*column))
            blocks.add(brick)
            sprites.add(brick)
    paddle = Paddle()
    blocks.add(paddle)
    sprites.add(paddle)
    ball = Ball(blocks, paddle)
    sprites.add(ball)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type = PLAYER_WIN:
                running = False
            if event.type = PLAYER_LOSE:
                running = False
        pressed_keys = pygame.key.get_pressed()
        paddle.update(pressed_keys)
        ball.update()
        screen.fill(COLOR_BLACK)
        for sprite in sprites:
            screen.blit(sprite.surf, sprite.rect)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
