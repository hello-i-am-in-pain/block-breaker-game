import pygame

from main import game_state


class Ball:
    def __init__(self, x, y, radius):
        self.position = pygame.Vector2(x, y)

        self.radius = radius

        # Velocity is measured in pixels per second.
        self.velocity = pygame.Vector2(0, 0)

        # Current speed of the ball.
        self.speed = 500.0

        self.launched = False

    def launch(self):
        if self.launched:
            return

        self.launched = True

        # Initial direction.
        #
        # The ball starts travelling upward,
        # with a slight horizontal component.
        direction = pygame.Vector2(0.35, -1)

        direction = direction.normalize()

        self.velocity = direction * self.speed
        
    def update(self, dt):
        if not self.launched:
            return

        self.position += self.velocity * dt

    def get_rect(self):
        return pygame.Rect(
            int(self.position.x - self.radius),
            int(self.position.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                int(self.position.x),
                int(self.position.y)
            ),
            self.radius
        )