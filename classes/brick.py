import json
import os
import random

import pygame


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCORE_DIR = os.path.join(PROJECT_ROOT, "score")
SCORE_FILE = os.path.join(SCORE_DIR, "highscore.json")

MAX_LIVES = 5


def save_high_score(score):
    os.makedirs(SCORE_DIR, exist_ok=True)
    with open(SCORE_FILE, "w", encoding="utf-8") as file:
        json.dump({"highscore": score}, file)


def load_high_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("highscore", 0)
    return 0


class Brick:
    def __init__(self, x, y, width, height, powerup_type=None):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.destroyed = False
        self.powerup_type = powerup_type

    def hit(self, points=10):
        self.destroyed = True
        return points


    def draw(self, screen):
        if self.destroyed:
            return

        color = (70, 130, 180)
        if self.powerup_type == "extra_ball":
            color = (220, 170, 60)
        elif self.powerup_type == "paddle":
            color = (80, 190, 110)
        elif self.powerup_type == "heart":
            color = (230, 40, 90)

        pygame.draw.rect(screen, color, self.rect, border_radius=5)

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
        columns,
        include_heart=False
    ):
        self.screen_width = screen_width
        self.start_y = start_y
        self.rows = rows
        self.columns = columns
        self.bricks = []
        self.reset(screen_width, start_y, rows, columns, include_heart=include_heart)

    def reset(self, screen_width=None, start_y=None, rows=None, columns=None, include_heart=False):
        if screen_width is not None:
            self.screen_width = screen_width
        if start_y is not None:
            self.start_y = start_y
        if rows is not None:
            self.rows = rows
        if columns is not None:
            self.columns = columns

        self.bricks = []
        self.total = self.rows * self.columns

        powerup_positions = set(random.sample(
            range(self.total),
            min(5, self.total)
        ))

        # The heart is not part of the regular powerup pool above - it's
        # placed in exactly one brick, and only on rounds Game decides
        # should have one (see difficulty-based intervals in game.py).
        heart_index = None
        if include_heart:
            available = list(set(range(self.total)) - powerup_positions)
            if available:
                heart_index = random.choice(available)

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

                brick_index = row * self.columns + column
                powerup_type = None
                if brick_index == heart_index:
                    powerup_type = "heart"
                elif brick_index in powerup_positions:
                    powerup_type = random.choice(("extra_ball", "paddle"))

                brick = Brick(
                    int(x),
                    int(y),
                    int(brick_width),
                    brick_height,
                    powerup_type
                )

                self.bricks.append(brick)

    def is_cleared(self):
        return all(brick.destroyed for brick in self.bricks)

    def draw(self, screen):
        for brick in self.bricks:
            brick.draw(screen)