import json
import os

import pygame


SCORE_FILE = "highscore.json"

total = 40


def save_high_score(score):
    with open(SCORE_FILE, "w", encoding="utf-8") as file:
        json.dump({"highscore": score}, file)


def load_high_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("highscore", 0)
    return 0


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
        global total
        self.destroyed = True
        total -= 1
        return 10


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
        self.screen_width = screen_width
        self.start_y = start_y
        self.rows = rows
        self.columns = columns
        self.bricks = []
        self.reset(screen_width, start_y, rows, columns)

    def reset(self, screen_width=None, start_y=None, rows=None, columns=None):
        global total
        if screen_width is not None:
            self.screen_width = screen_width
        if start_y is not None:
            self.start_y = start_y
        if rows is not None:
            self.rows = rows
        if columns is not None:
            self.columns = columns

        self.bricks = []
        total = self.rows * self.columns

        gap = 10
        margin = 80

        brick_width = (
            self.screen_width
            - (margin * 2)
            - (gap * (self.columns - 1))
        ) / self.columns

        brick_height = 35

        for row in range(self.rows):
            for column in range(self.columns):
                x = margin + column * (brick_width + gap)
                y = self.start_y + row * (brick_height + gap)

                brick = Brick(
                    int(x),
                    int(y),
                    int(brick_width),
                    brick_height
                )

                self.bricks.append(brick)

    def is_cleared(self):
        return all(brick.destroyed for brick in self.bricks)

    def draw(self, screen):
        for brick in self.bricks:
            brick.draw(screen)