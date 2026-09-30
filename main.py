import sys

import pygame

from menu import Menu
from game import Game
from network import Host, Client
from remote_view import RemoteGameView
from classes.death_screen import draw_death_screen

pygame.init()

# Pass --windowed on the command line to run in a small window instead
# of fullscreen - handy for testing two instances side by side on one
# machine, since two exclusive-fullscreen windows fighting for the same
# monitor doesn't work reliably. Normal play (no flag) is untouched.
WINDOWED_TEST_MODE = "--windowed" in sys.argv

if WINDOWED_TEST_MODE:
    WIDTH, HEIGHT = 960, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
else:
    info = pygame.display.Info()
    WIDTH = info.current_w
    HEIGHT = info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

HALF_WIDTH = WIDTH // 2
FPS = 60
lives = 3

pygame.display.set_caption("Block Breaker Game")
clock = pygame.time.Clock()


menu = Menu(WIDTH, HEIGHT)
game = None
game_state = "menu"
mode = "solo"
difficulty = "normal"
death_score = 0
death_high_score = 0

# Versus-mode networking state. network_peer is a Host or Client from
# network.py once a connection attempt has started; versus_role tracks
# which one so we know how to draw/react in shared states.
network_peer = None
versus_role = None
versus_error = None

# Versus-mode match state, built once the connection succeeds.
remote_view = None
local_surface = None
remote_surface = None


def _abandon_connection():
    """Tear down whatever connection attempt is in progress and drop
    back to the versus mode-select screen. Used any time the player
    backs out or cancels."""
    global network_peer, versus_role, versus_error
    if network_peer is not None:
        network_peer.close()
    network_peer = None
    versus_role = None
    versus_error = None

running = True

while running:
    dt = clock.tick(FPS) / 1000.0
    dt = min(dt, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if menu.start_button.is_clicked(event):
                mode = "solo"
                game_state = "difficulty"
            elif menu.multiplayer_button.is_clicked(event):
                mode = "versus"
                game_state = "difficulty"
            elif menu.quit_button.is_clicked(event):
                running = False
        elif game_state == "difficulty":
            selected_difficulty = None
            if menu.easy_button.is_clicked(event):
                selected_difficulty = "easy"
            elif menu.medium_button.is_clicked(event):
                selected_difficulty = "normal"
            elif menu.hard_button.is_clicked(event):
                selected_difficulty = "hard"
            elif menu.back_button.is_clicked(event):
                game_state = "menu"

            if selected_difficulty is not None:
                difficulty = selected_difficulty
                if mode == "solo":
                    game = Game(WIDTH, HEIGHT, difficulty)
                    game_state = "playing"
                else:
                    game_state = "versus_mode_select"
        elif game_state == "versus_mode_select":
            if menu.host_button.is_clicked(event):
                versus_role = "host"
                versus_error = None
                network_peer = Host()
                network_peer.start_hosting()
                game_state = "versus_hosting"
            elif menu.join_button.is_clicked(event):
                versus_role = "client"
                versus_error = None
                menu.ip_input.text = ""
                game_state = "versus_ip_entry"
            elif menu.back_button.is_clicked(event):
                game_state = "menu"
        elif game_state == "versus_hosting":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                _abandon_connection()
                game_state = "versus_mode_select"
        elif game_state == "versus_ip_entry":
            result = menu.ip_input.handle_event(event)
            if result == "submit":
                host_ip = menu.ip_input.text.strip()
                if host_ip:
                    versus_error = None
                    network_peer = Client()
                    network_peer.connect(host_ip)
                    game_state = "versus_connecting"
            elif result == "cancel":
                game_state = "versus_mode_select"
            elif menu.connect_button.is_clicked(event):
                host_ip = menu.ip_input.text.strip()
                if host_ip:
                    versus_error = None
                    network_peer = Client()
                    network_peer.connect(host_ip)
                    game_state = "versus_connecting"
            elif menu.back_button.is_clicked(event):
                game_state = "versus_mode_select"
        elif game_state == "versus_connecting":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                _abandon_connection()
                game_state = "versus_mode_select"
        elif game_state == "versus_playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    _abandon_connection()
                    game = None
                    remote_view = None
                    game_state = "menu"
                elif event.key == pygame.K_SPACE and game is not None:
                    game.launch_balls()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and game is not None:
                    game.launch_balls()
        elif game_state == "versus_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "menu"
        elif game_state == "versus_disconnected":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "menu"
        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = None
                    game_state = "menu"
                elif event.key == pygame.K_SPACE and game is not None:
                    game.launch_balls()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and game is not None:
                    game.launch_balls()
        elif game_state == "death_screen":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lives = 3
                    game = Game(WIDTH, HEIGHT, difficulty)
                    game_state = "playing"
                elif event.key == pygame.K_q:
                    game = None
                    game_state = "menu"

    # Connecting/hosting happens on a background thread (see network.py),
    # so this checks in on it every frame rather than waiting for an
    # event - there's no user input involved while it's in progress.
    if game_state == "versus_hosting" and network_peer is not None:
        if network_peer.connected:
            game = Game(HALF_WIDTH, HEIGHT, difficulty)
            remote_view = RemoteGameView(HALF_WIDTH, HEIGHT)
            local_surface = pygame.Surface((HALF_WIDTH, HEIGHT))
            remote_surface = pygame.Surface((HALF_WIDTH, HEIGHT))
            game_state = "versus_playing"
        elif network_peer.error:
            versus_error = network_peer.error
    elif game_state == "versus_connecting" and network_peer is not None:
        if network_peer.connected:
            game = Game(HALF_WIDTH, HEIGHT, difficulty)
            remote_view = RemoteGameView(HALF_WIDTH, HEIGHT)
            local_surface = pygame.Surface((HALF_WIDTH, HEIGHT))
            remote_surface = pygame.Surface((HALF_WIDTH, HEIGHT))
            game_state = "versus_playing"
        elif network_peer.error:
            versus_error = network_peer.error
            game_state = "versus_ip_entry"

    if game_state == "menu":
        screen.fill((30, 30, 40))
        menu.draw(screen)
    elif game_state == "difficulty":
        menu.draw_difficulty(screen)
    elif game_state == "versus_mode_select":
        menu.draw_versus_mode_select(screen)
    elif game_state == "versus_hosting":
        status = "Waiting for opponent..." if versus_error is None else versus_error
        menu.draw_host_waiting(screen, network_peer.local_ip, status)
    elif game_state == "versus_ip_entry":
        menu.draw_join_ip_entry(screen, versus_error)
    elif game_state == "versus_connecting":
        menu.draw_join_connecting(screen, menu.ip_input.text, "Connecting...")
    elif game_state == "versus_playing" and game is not None:
        still_alive = game.update(dt)

        # Send our state and pull in theirs regardless of whether we
        # just lost this frame - the opponent still needs to see our
        # final position/game-over flag.
        if network_peer is not None:
            network_peer.send_state(game.get_network_snapshot())
            remote_view.apply_snapshot(network_peer.get_latest_remote_state())

        game.draw(local_surface)
        remote_view.draw(remote_surface)
        screen.blit(local_surface, (0, 0))
        screen.blit(remote_surface, (HALF_WIDTH, 0))
        pygame.draw.line(screen, (255, 255, 255), (HALF_WIDTH, 0), (HALF_WIDTH, HEIGHT), 2)

        # Left half is always "you" - label it so it's obvious which
        # window/role you're looking at, especially useful when testing
        # two windowed instances side by side on one machine.
        role_font = pygame.font.Font(None, 28)
        role_text = role_font.render(
            f"You: {versus_role.capitalize()}", True, (255, 255, 0)
        )
        screen.blit(role_text, (20, HEIGHT - 40))

        if network_peer is not None and not network_peer.connected:
            # Opponent dropped mid-match. A cleaner reconnect/notice flow
            # is a later step - for now, stop the match and say so.
            versus_error = network_peer.error or "Opponent disconnected."
            game = None
            remote_view = None
            game_state = "versus_disconnected"
        elif not still_alive:
            # Local game over. A proper win/loss screen (using
            # remote_view.game_over to tell who actually won) is next -
            # this just reports your own result for now.
            death_score = game.current_score
            death_high_score = game.high_score
            game = None
            remote_view = None
            _abandon_connection()
            game_state = "versus_over"
    elif game_state == "versus_over":
        screen.fill((30, 30, 40))
        font = pygame.font.Font(None, 48)
        text = font.render("Match Over", True, (255, 60, 60))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))

        info_font = pygame.font.Font(None, 36)
        score_text = info_font.render(f"Your score: {death_score}", True, (255, 255, 255))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

        hint_text = info_font.render("Press Esc to return to menu", True, (200, 200, 200))
        screen.blit(hint_text, hint_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80)))
    elif game_state == "versus_disconnected":
        screen.fill((30, 30, 40))
        font = pygame.font.Font(None, 48)
        text = font.render("Connection Lost", True, (255, 60, 60))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))

        info_font = pygame.font.Font(None, 32)
        detail_text = info_font.render(versus_error or "", True, (200, 200, 200))
        screen.blit(detail_text, detail_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))

        hint_text = info_font.render("Press Esc to return to menu", True, (200, 200, 200))
        screen.blit(hint_text, hint_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))
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