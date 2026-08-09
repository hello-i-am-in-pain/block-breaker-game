import pygame

from paddle import Paddle
from ball import Ball
from brick import BrickWall, load_high_score, save_high_score

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

        self.high_score = load_high_score()
        self.current_score = 0
        self.lives = 3
        self.game_over = False

    def reset_ball(self):
        self.ball.launched = False
        self.ball.velocity = pygame.Vector2(0, 0)
        self.ball.position.x = self.paddle.rect.centerx
        self.ball.position.y = self.paddle.rect.top - self.ball.radius - 2

    def reset_round(self):
        self.reset_ball()
        self.brick_wall.reset(
            screen_width=self.width,
            start_y=100,
            rows=5,
            columns=10,
        )

    def lose_life(self):
        self.lives -= 1
        self.reset_ball()
        if self.lives <= 0:
            self.game_over = True
            return False
        return True

    def update(self, dt):
        if self.game_over:
            return False

        if self.brick_wall.is_cleared():
            self.reset_round()
            return True

        self.paddle.update(dt)

        if not self.ball.launched:
            self.reset_ball()

        self.ball.update(dt)
        self._handle_collisions()

        if self.ball.position.y - self.ball.radius > self.height:
            return self.lose_life()

        if self.current_score > self.high_score:
            self.high_score = self.current_score
            save_high_score(self.high_score)

        return True

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
                self.current_score += brick.hit()
                self.ball.velocity.y *= -1
                break

    def draw(self, screen):
        screen.fill(BACKGROUND)
        self.brick_wall.draw(screen)
        self.paddle.draw(screen)
        self.ball.draw(screen)

        font = pygame.font.Font(None, 32)
        score_text = font.render(f"Score: {self.current_score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(score_text, (35, 25))
        screen.blit(high_score_text, (35, 50))
        screen.blit(lives_text, (35, 75))