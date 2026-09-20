import pygame

from classes.brick import BrickWall
from classes.heart import draw_heart

BACKGROUND = (30, 30, 40)


class RemoteGameView:
    """A read-only stand-in for the other player's board.

    This is never simulated - it has no physics, no update(dt) that
    moves anything on its own. Every frame it's simply told the latest
    snapshot received over the network (via apply_snapshot) and draws
    exactly that. If the network stalls for a moment, it just keeps
    showing the last snapshot it had rather than freezing or guessing.

    The brick wall geometry (rows/columns/screen size/start_y) has to
    match what the real Game on the other machine was built with, since
    only which bricks are destroyed is transmitted - not their
    positions. That's why both players need to be on the same
    difficulty/settings for now.
    """

    def __init__(self, width, height, rows=5, columns=8, start_y=100):
        self.width = width
        self.height = height

        # Built with include_heart=False since its random powerup
        # layout is meaningless here - every brick's powerup_type gets
        # overwritten from the snapshot each time one arrives, and this
        # wall is only ever drawn, never played, so what it starts with
        # doesn't matter.
        self.brick_wall = BrickWall(
            screen_width=width,
            start_y=start_y,
            rows=rows,
            columns=columns,
            include_heart=False,
        )

        self.paddle_width = 200
        self.paddle_height = 25
        self.paddle_x = width // 2
        self.paddle_y = height - 100

        self.balls = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.connected = False

    def apply_snapshot(self, snapshot):
        """Feed in the latest dict from NetworkPeer.get_latest_remote_state().
        Safe to call with None (e.g. before anything has arrived yet) -
        just does nothing that frame."""
        if snapshot is None:
            return

        self.connected = True
        self.score = snapshot.get("score", self.score)
        self.lives = snapshot.get("lives", self.lives)
        self.game_over = snapshot.get("game_over", self.game_over)
        self.paddle_x = snapshot.get("paddle_x", self.paddle_x)
        self.paddle_width = snapshot.get("paddle_width", self.paddle_width)
        self.balls = snapshot.get("balls", self.balls)

        destroyed = snapshot.get("destroyed_bricks")
        powerup_types = snapshot.get("powerup_types")
        if destroyed is not None:
            for index, brick in enumerate(self.brick_wall.bricks):
                if index < len(destroyed):
                    brick.destroyed = destroyed[index]
                if powerup_types is not None and index < len(powerup_types):
                    brick.powerup_type = powerup_types[index]

    def draw(self, screen):
        screen.fill(BACKGROUND)

        if not self.connected:
            font = pygame.font.Font(None, 36)
            waiting_text = font.render("Waiting for opponent...", True, (200, 200, 200))
            screen.blit(
                waiting_text,
                waiting_text.get_rect(center=(self.width // 2, self.height // 2)),
            )
            return

        self.brick_wall.draw(screen)

        paddle_rect = pygame.Rect(0, 0, self.paddle_width, self.paddle_height)
        paddle_rect.centerx = self.paddle_x
        paddle_rect.y = self.paddle_y
        pygame.draw.rect(screen, (255, 255, 255), paddle_rect, border_radius=8)

        for ball in self.balls:
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (int(ball["x"]), int(ball["y"])),
                int(ball["radius"]),
            )

        font = pygame.font.Font(None, 32)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (35, 25))

        heart_size = 22
        heart_spacing = 30
        heart_center_y = 60
        for i in range(self.lives):
            heart_center_x = 35 + heart_size // 2 + i * heart_spacing
            draw_heart(screen, (heart_center_x, heart_center_y), heart_size, (255, 255, 255))

        if self.game_over:
            over_font = pygame.font.Font(None, 48)
            over_text = over_font.render("OUT!", True, (255, 60, 60))
            screen.blit(
                over_text,
                over_text.get_rect(center=(self.width // 2, self.height // 2)),
            )