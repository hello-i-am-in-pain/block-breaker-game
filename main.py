import pygame

from menu import Menu
from game import Game

pygame.init()

WIDTH = 1600
HEIGHT = 900
FPS = 60
lives = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker Game")
clock = pygame.time.Clock()

menu = Menu(WIDTH, HEIGHT)
game = None
game_state = "menu"

running = True

while running:
    dt = clock.tick(FPS) / 1000.0
    dt = min(dt, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if menu.start_button.is_clicked(event):
                game = Game(WIDTH, HEIGHT)
                game_state = "playing"
            elif menu.quit_button.is_clicked(event):
                running = False
        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = None
                    game_state = "menu"
                elif event.key == pygame.K_SPACE and game is not None:
                    game.ball.launch()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and game is not None:
                    game.ball.launch()
            if game is not None and (
                game.ball.position.x - game.ball.radius < 0 or         # Left Edge
                game.ball.position.x + game.ball.radius > WIDTH or     # Right Edge
                game.ball.position.y - game.ball.radius < 0 or         # Top Edge
                game.ball.position.y + game.ball.radius > HEIGHT       # Bottom Edge
            ):
                lives -= 1
                if lives <= 0:
                    game = None
                    game_state = "menu"
                else:
                    game.reset_ball()

    if game_state == "menu":
        screen.fill((30, 30, 40))
        menu.draw(screen)
    elif game_state == "playing" and game is not None:
        if not game.update(dt):
            game = None
            game_state = "menu"
        else:
            game.draw(screen)

    pygame.display.flip()

pygame.quit()