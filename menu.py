import pygame

pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker Game")

clock = pygame.time.Clock()

BACKGROUND = (30, 30, 40)
WHITE = (255, 255, 255)

BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 220)

title_font = pygame.font.SysFont("arial", 64, bold=True)
button_font = pygame.font.SysFont("arial", 36)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(surface, color, self.rect, border_radius=12)

        text_surface = button_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)

        surface.blit(text_surface, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

button_width = 300
button_height = 70
spacing = 25

start_button = Button(
    WIDTH // 2 - button_width // 2,
    260,
    button_width,
    button_height,
    "Start",
)

settings_button = Button(
    WIDTH // 2 - button_width // 2,
    260 + button_height + spacing,
    button_width,
    button_height,
    "Settings",
)

multiplayer_button = Button(
    WIDTH // 2 - button_width // 2,
    260 + (button_height + spacing) * 2,
    button_width,
    button_height,
    "Multiplayer",
)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND)

    title = title_font.render("Block Breaker Game", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 120))
    screen.blit(title, title_rect)

    start_button.draw(screen)
    settings_button.draw(screen)
    multiplayer_button.draw(screen)

    pygame.display.flip()

pygame.quit()