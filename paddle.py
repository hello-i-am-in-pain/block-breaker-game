import pygame


class Paddle:
    def __init__(self, x, y, width, height, screen_width, keymap=None):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.screen_width = screen_width

        # Paddle movement
        self.speed = 800.0

        # Defaults preserve current single-player controls (arrows + A/D).
        # A future second paddle can pass its own keymap, e.g.
        # {"left": (pygame.K_a,), "right": (pygame.K_d,)}, without the
        # two players fighting over the same keys.
        self.keymap = keymap or {
            "left": (pygame.K_LEFT, pygame.K_a),
            "right": (pygame.K_RIGHT, pygame.K_d),
        }

    def update(self, dt):
        keys = pygame.key.get_pressed()

        movement = 0

        if any(keys[key] for key in self.keymap["left"]):
            movement -= 1

        if any(keys[key] for key in self.keymap["right"]):
            movement += 1

        self.rect.x += movement * self.speed * dt

        # Prevent the paddle from leaving the screen
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect,
            border_radius=8
        )