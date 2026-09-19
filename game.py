import pygame

try:
    from classes.paddle import Paddle
    from classes.ball import Ball
    from classes.brick import BrickWall, MAX_LIVES, load_high_score, save_high_score
    from classes.heart import FallingHeart, draw_heart
except ImportError:  # pragma: no cover - package-style fallback
    from .classes.paddle import Paddle
    from .classes.ball import Ball
    from .classes.brick import BrickWall, MAX_LIVES, load_high_score, save_high_score
    from .classes.heart import FallingHeart, draw_heart

BACKGROUND = (30, 30, 40)


class Game:
    def __init__(self, width, height, difficulty="normal"):
        self.width = width
        self.height = height
        self.difficulty = difficulty

        difficulty_settings = {
            "easy": {"paddle_width": 260, "ball_speed": 400.0},
            "normal": {"paddle_width": 200, "ball_speed": 500.0},
            "hard": {"paddle_width": 150, "ball_speed": 700.0},
        }
        settings = difficulty_settings[difficulty]
        self.points_per_brick = {
            "easy": 10,
            "normal": 30,
            "hard": 50,
        }[difficulty]

        # How many full wall resets pass between heart-powerup spawns.
        # Lower difficulties get one more often since everything else
        # about the round is also easier to manage alongside chasing it.
        self.heart_interval = {
            "easy": 2,
            "normal": 3,
            "hard": 4,
        }[difficulty]
        self.round_number = 1

        self.paddle = Paddle(
            x=width // 2 - settings["paddle_width"] // 2,
            y=height - 100,
            width=settings["paddle_width"],
            height=25,
            screen_width=width,
        )
        self.base_paddle_width = settings["paddle_width"]
        self.paddle_powerup_time = 0.0

        self.ball = Ball(x=width // 2, y=height - 130, radius=10)
        self.ball.speed = settings["ball_speed"]
        self.balls = [self.ball]

        self.brick_wall = BrickWall(
            screen_width=width,
            start_y=100,
            rows=5,
            columns=8,
            include_heart=self._should_spawn_heart(),
        )

        self.high_score = load_high_score()
        self.current_score = 0
        self.lives = 3
        self.game_over = False
        self.falling_hearts = []

    def _should_spawn_heart(self):
        return self.round_number % self.heart_interval == 0

    def reset_ball(self):
        self.balls = [self._new_ball()]
        self.ball = self.balls[0]

    def _new_ball(self, position=None, velocity=None):
        ball = Ball(
            x=self.paddle.rect.centerx if position is None else position.x,
            y=self.paddle.rect.top - 12 if position is None else position.y,
            radius=10,
        )
        ball.speed = self.ball.speed
        if position is not None:
            ball.launched = True
            ball.velocity = velocity or pygame.Vector2(0, -ball.speed)
        return ball

    def launch_balls(self):
        for ball in self.balls:
            ball.launch()

    def reset_round(self):
        self.reset_ball()
        self.round_number += 1
        self.brick_wall.reset(
            screen_width=self.width,
            start_y=100,
            rows=self.brick_wall.rows,
            columns=self.brick_wall.columns,
            include_heart=self._should_spawn_heart(),
        )

    def lose_life(self):
        self.lives -= 1
        self._clear_powerups()
        # A heart caught mid-fall doesn't carry over into the next life -
        # losing the ball while it's in play costs you the attempt.
        self.falling_hearts = []
        self.reset_ball()
        if self.lives <= 0:
            self.game_over = True
            return False
        return True

    def _clear_powerups(self):
        self.paddle_powerup_time = 0.0
        self.paddle.rect.width = self.base_paddle_width
        self.paddle.rect.centerx = min(
            max(self.paddle.rect.centerx, self.paddle.rect.width // 2),
            self.width - self.paddle.rect.width // 2
        )

    def _update_powerups(self, dt):
        if self.paddle_powerup_time <= 0:
            return

        self.paddle_powerup_time = max(0, self.paddle_powerup_time - dt)
        if self.paddle_powerup_time == 0:
            self.paddle.rect.width = self.base_paddle_width
            self.paddle.rect.centerx = min(
                max(self.paddle.rect.centerx, self.paddle.rect.width // 2),
                self.width - self.paddle.rect.width // 2
            )

    def _update_falling_hearts(self, dt):
        for heart in self.falling_hearts:
            heart.update(dt, self.width, self.height)

            if (
                heart.can_be_caught
                and heart.velocity.y > 0
                and heart.get_rect().colliderect(self.paddle.rect)
            ):
                heart.bounce_off_paddle(self.paddle.rect)
                if heart.collected:
                    self.lives = min(self.lives + 1, MAX_LIVES)

        self.falling_hearts = [
            heart for heart in self.falling_hearts
            if not (heart.collected or heart.missed)
        ]

    def update(self, dt):
        if self.game_over:
            return False

        if self.brick_wall.is_cleared():
            self.reset_round()
            return True

        self.paddle.update(dt)
        self._update_powerups(dt)
        self._update_falling_hearts(dt)

        if not self.ball.launched:
            self.reset_ball()

        for ball in self.balls[:]:
            ball.update(dt)
            self._handle_collisions(ball)

            if ball.position.y - ball.radius > self.height:
                self.balls.remove(ball)

        if not self.balls:
            return self.lose_life()

        if self.current_score > self.high_score:
            self.high_score = self.current_score
            save_high_score(self.high_score)

        return True

    def _handle_collisions(self, ball):
        ball_rect = ball.get_rect()

        if ball.position.x - ball.radius <= 0:
            ball.position.x = ball.radius
            ball.velocity.x *= -1

        if ball.position.x + ball.radius >= self.width:
            ball.position.x = self.width - ball.radius
            ball.velocity.x *= -1

        if ball.position.y - ball.radius <= 0:
            ball.position.y = ball.radius
            ball.velocity.y *= -1

        if ball_rect.colliderect(self.paddle.rect) and ball.velocity.y > 0:
            ball.position.y = self.paddle.rect.top - ball.radius - 1
            ball.velocity.y *= -1
            offset = (ball.position.x - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            ball.velocity.x += offset * 200
            if ball.velocity.length_squared() > 0:
                ball.velocity = ball.velocity.normalize() * ball.speed

        for brick in self.brick_wall.bricks:
            if not brick.destroyed and ball_rect.colliderect(brick.rect):
                self.current_score += brick.hit(self.points_per_brick)
                ball.velocity.y *= -1
                self._apply_powerup(brick.powerup_type, ball, brick)
                break

    def _apply_powerup(self, powerup_type, source_ball, brick=None):
        if powerup_type == "paddle":
            self.paddle.rect.width = self.base_paddle_width + 30
            self.paddle.rect.width = min(self.paddle.rect.width, self.width)
            self.paddle_powerup_time = 30.0
            self.paddle.rect.centerx = min(
                max(self.paddle.rect.centerx, self.paddle.rect.width // 2),
                self.width - self.paddle.rect.width // 2
            )
        elif powerup_type == "extra_ball":
            velocity = source_ball.velocity.rotate(25)
            self.balls.append(self._new_ball(source_ball.position, velocity))
        elif powerup_type == "heart" and brick is not None:
            # Breaking the brick doesn't grant the life outright - it just
            # releases the heart, which now has to be bounced off the
            # paddle a few times before it turns into an actual life.
            self.falling_hearts.append(
                FallingHeart(
                    brick.rect.centerx,
                    brick.rect.centery,
                    speed=source_ball.speed * 1.3,
                )
            )

    def draw(self, screen):
        screen.fill(BACKGROUND)
        self.brick_wall.draw(screen)
        self.paddle.draw(screen)
        for ball in self.balls:
            ball.draw(screen)
        for heart in self.falling_hearts:
            heart.draw(screen)

        font = pygame.font.Font(None, 32)
        score_text = font.render(f"Score: {self.current_score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        screen.blit(score_text, (35, 25))
        screen.blit(high_score_text, (35, 50))

        heart_size = 22
        heart_spacing = 30
        heart_center_y = 88
        for i in range(self.lives):
            heart_center_x = 35 + heart_size // 2 + i * heart_spacing
            draw_heart(screen, (heart_center_x, heart_center_y), heart_size, (255, 255, 255))