import pygame

BACKGROUND = (30, 30, 40)

def draw_death_screen(screen, width, height, score, high_score):
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(text, text_rect)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(width // 2, height // 2))
    screen.blit(score_text, score_rect)

    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    high_score_rect = high_score_text.get_rect(center=(width // 2, height // 2 + 50))
    screen.blit(high_score_text, high_score_rect)

    restart_text = font.render("Press Space to Restart or Q to Quit", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 100))
    screen.blit(restart_text, restart_rect)