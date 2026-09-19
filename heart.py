import random

import pygame


def draw_heart(screen, center, size, color):
    """Draw a simple filled heart shape centered at `center`.

    `size` is roughly the heart's total width/height in pixels. Used both
    for the lives HUD and for the falling heart powerup itself.
    """
    x, y = center
    lobe_radius = size / 4

    pygame.draw.circle(
        screen, color, (int(x - lobe_radius), int(y - lobe_radius * 0.4)), int(lobe_radius)
    )
    pygame.draw.circle(
        screen, color, (int(x + lobe_radius), int(y - lobe_radius * 0.4)), int(lobe_radius)
    )

    points = [
        (x - size / 2, y - lobe_radius * 0.2),
        (x, y + size / 2),
        (x + size / 2, y - lobe_radius * 0.2),
    ]
    pygame.draw.polygon(screen, color, points)


class FallingHeart:
    """A rare extra-life powerup.

    When its brick is destroyed, the heart drops out like a ball - only
    faster - and bounces off the paddle instead of the paddle simply
    catching it. Each bounce sends it off at a random angle, so the
    player has to keep tracking and repositioning under it. It takes
    `hits_required` paddle bounces to turn into an actual life, and after
    each bounce it has to climb back to at least `RECATCH_HEIGHT` pixels
    above the paddle before the next bounce is allowed to count, so it
    can't just be rattled against the paddle in place. Let it fall past
    the paddle without enough bounces and it's lost for the round.
    """

    RECATCH_HEIGHT = 100

    def __init__(self, x, y, hits_required=3, speed=600.0, radius=16):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, speed)
        self.radius = radius
        self.speed = speed
        self.hits_required = hits_required
        self.hits_taken = 0
        self.collected = False
        self.missed = False
        self.can_be_caught = True
        self._recatch_y = None

    def update(self, dt, screen_width, screen_height):
        if self.collected or self.missed:
            return

        self.position += self.velocity * dt

        if self.position.x - self.radius <= 0:
            self.position.x = self.radius
            self.velocity.x *= -1

        if self.position.x + self.radius >= screen_width:
            self.position.x = screen_width - self.radius
            self.velocity.x *= -1

        if self.position.y - self.radius <= 0:
            self.position.y = self.radius
            self.velocity.y *= -1

        if not self.can_be_caught and self.position.y <= self._recatch_y:
            self.can_be_caught = True

        if self.position.y - self.radius > screen_height:
            self.missed = True

    def get_rect(self):
        return pygame.Rect(
            int(self.position.x - self.radius),
            int(self.position.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def bounce_off_paddle(self, paddle_rect):
        if not self.can_be_caught:
            return

        self.position.y = paddle_rect.top - self.radius - 1

        # A random angle every time, not one based on where it landed on
        # the paddle - that unpredictability is the actual challenge here.
        angle = random.uniform(-60, 60)
        direction = pygame.Vector2(0, -1).rotate(angle)
        self.velocity = direction * self.speed

        self.hits_taken += 1
        self.can_be_caught = False
        self._recatch_y = paddle_rect.top - self.RECATCH_HEIGHT

        if self.hits_taken >= self.hits_required:
            self.collected = True

    def draw(self, screen):
        if self.collected or self.missed:
            return

        # Brightens from a dim red toward white-hot pink with each bounce,
        # so the player gets clear feedback on how close it is.
        progress = self.hits_taken / self.hits_required
        start = pygame.Vector3(150, 30, 60)
        end = pygame.Vector3(255, 255, 255)
        current = start.lerp(end, progress)
        color = (int(current.x), int(current.y), int(current.z))

        draw_heart(screen, (self.position.x, self.position.y), self.radius * 2, color)

        # Small pips above the heart show bounces landed vs. still needed.
        pip_radius = 4
        spacing = 12
        start_x = self.position.x - (spacing * (self.hits_required - 1)) / 2
        pip_y = self.position.y - self.radius - 14
        for i in range(self.hits_required):
            pip_color = (255, 255, 255) if i < self.hits_taken else (90, 90, 100)
            pygame.draw.circle(
                screen,
                pip_color,
                (int(start_x + i * spacing), int(pip_y)),
                pip_radius,
            )