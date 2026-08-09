import pygame


class Paddle:
    def __init__(self, x, y, width, height, screen_width):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.screen_width = screen_width

        # Paddle movement
        self.speed = 800.0

    def update(self, dt):
        keys = pygame.key.get_pressed()

        movement = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            movement -= 1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
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