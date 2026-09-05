import pygame

from menu import Menu
from game import Game
from death_screen import draw_death_screen

pygame.init()

info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
FPS = 60
lives = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Block Breaker Game")
clock = pygame.time.Clock()


menu = Menu(WIDTH, HEIGHT)
game = None
game_state = "menu"
difficulty = "normal"
death_score = 0
death_high_score = 0

running = True

while running:
    dt = clock.tick(FPS) / 1000.0
    dt = min(dt, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if menu.start_button.is_clicked(event):
                game_state = "difficulty"
            elif menu.quit_button.is_clicked(event):
                running = False
        elif game_state == "difficulty":
            if menu.easy_button.is_clicked(event):
                difficulty = "easy"
                game = Game(WIDTH, HEIGHT, difficulty)
                game_state = "playing"
            elif menu.medium_button.is_clicked(event):
                difficulty = "normal"
                game = Game(WIDTH, HEIGHT, difficulty)
                game_state = "playing"
            elif menu.hard_button.is_clicked(event):
                difficulty = "hard"
                game = Game(WIDTH, HEIGHT, difficulty)
                game_state = "playing"
            elif menu.back_button.is_clicked(event):
                game_state = "menu"
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
                    death_score = game.current_score
                    death_high_score = game.high_score
                    game = None
                    game_state = "death_screen"
                else:
                    game.reset_ball()
        elif game_state == "death_screen":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lives = 3
                    game = Game(WIDTH, HEIGHT, difficulty)
                    game_state = "playing"
                elif event.key == pygame.K_q:
                    game = None
                    game_state = "menu"

    if game_state == "menu":
        screen.fill((30, 30, 40))
        menu.draw(screen)
    elif game_state == "difficulty":
        menu.draw_difficulty(screen)
    elif game_state == "playing" and game is not None:
        if not game.update(dt):
            death_score = game.current_score
            death_high_score = game.high_score
            game = None
            game_state = "death_screen"
        else:
            game.draw(screen)
    elif game_state == "death_screen":
        screen.fill((30, 30, 40))
        draw_death_screen(screen, WIDTH, HEIGHT, death_score, death_high_score)

    pygame.display.flip()

pygame.quit()