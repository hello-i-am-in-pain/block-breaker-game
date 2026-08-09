import pygame


class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.destroyed = False

    def hit(self):
        self.destroyed = True

    def draw(self, screen):
        if self.destroyed:
            return

        pygame.draw.rect(
            screen,
            (70, 130, 180),
            self.rect,
            border_radius=5
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect,
            width=2,
            border_radius=5
        )


class BrickWall:
    def __init__(
        self,
        screen_width,
        start_y,
        rows,
        columns
    ):
        self.bricks = []

        gap = 10
        margin = 80

        brick_width = (
            screen_width
            - (margin * 2)
            - (gap * (columns - 1))
        ) / columns

        brick_height = 35

        for row in range(rows):
            for column in range(columns):

                x = (
                    margin
                    + column * (
                        brick_width + gap
                    )
                )

                y = (
                    start_y
                    + row * (
                        brick_height + gap
                    )
                )

                brick = Brick(
                    int(x),
                    int(y),
                    int(brick_width),
                    brick_height
                )

                self.bricks.append(brick)

    def draw(self, screen):
        for brick in self.bricks:
            brick.draw(screen)