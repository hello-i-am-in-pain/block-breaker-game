import pygame

from paddle import Paddle
from ball import Ball
from brick import BrickWall

BACKGROUND = (30, 30, 40)


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.paddle = Paddle(
            x=width // 2 - 100,
            y=height - 100,
            width=200,
            height=25,
            screen_width=width,
        )

        self.ball = Ball(x=width // 2, y=height - 130, radius=10)

        self.brick_wall = BrickWall(
            screen_width=width,
            start_y=100,
            rows=5,
            columns=10,
        )

    def update(self, dt):
        self.paddle.update(dt)

        if not self.ball.launched:
            self.ball.position.x = self.paddle.rect.centerx
            self.ball.position.y = self.paddle.rect.top - self.ball.radius - 2

        self.ball.update(dt)
        self._handle_collisions()

    def _handle_collisions(self):
        ball_rect = self.ball.get_rect()

        if self.ball.position.x - self.ball.radius <= 0:
            self.ball.position.x = self.ball.radius
            self.ball.velocity.x *= -1

        if self.ball.position.x + self.ball.radius >= self.width:
            self.ball.position.x = self.width - self.ball.radius
            self.ball.velocity.x *= -1

        if self.ball.position.y - self.ball.radius <= 0:
            self.ball.position.y = self.ball.radius
            self.ball.velocity.y *= -1

        if ball_rect.colliderect(self.paddle.rect) and self.ball.velocity.y > 0:
            self.ball.position.y = self.paddle.rect.top - self.ball.radius - 1
            self.ball.velocity.y *= -1
            offset = (self.ball.position.x - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            self.ball.velocity.x += offset * 200
            if self.ball.velocity.length_squared() > 0:
                self.ball.velocity = self.ball.velocity.normalize() * self.ball.speed

        for brick in self.brick_wall.bricks:
            if not brick.destroyed and ball_rect.colliderect(brick.rect):
                brick.hit()
                self.ball.velocity.y *= -1
                break

    def draw(self, screen):
        screen.fill(BACKGROUND)
        self.brick_wall.draw(screen)
        self.paddle.draw(screen)
        self.ball.draw(screen)