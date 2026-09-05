import pygame

BACKGROUND = (30, 30, 40)
WHITE = (255, 255, 255)

BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 220)



class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("arial", 36)
    
    def draw(self, screen):
        mouse = pygame.mouse.get_pos()

        color = BUTTON_HOVER if self.rect.collidepoint(mouse) else BUTTON_COLOR

        pygame.draw.rect(screen, color, self.rect, border_radius=12)

        text = self.font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)

        screen.blit(text, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

#Menu code
class Menu:
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.title_font = pygame.font.SysFont("arial", 64, bold=True)

        button_width = 300
        button_height = 70
        spacing = 25

        x = width // 2 - button_width // 2

        self.start_button = Button(
            x, 260,
            button_width,
            button_height,
            "Start"
        )

        self.settings_button = Button(
            x, 355,
            button_width,
            button_height,
            "Settings"
        )

        self.multiplayer_button = Button(
            x, 450,
            button_width,
            button_height,
            "Multiplayer"
        )

        self.quit_button = Button(
            x, 545,
            button_width,
            button_height,
            "Quit"
        )

        self.easy_button = Button(
            x, 260,
            button_width,
            button_height,
            "Easy"
        )

        self.medium_button = Button(
            x, 355,
            button_width,
            button_height,
            "Normal"
        )

        self.hard_button = Button(
            x, 450,
            button_width,
            button_height,
            "Hard"
        )

        self.back_button = Button(
            x, 545,
            button_width,
            button_height,
            "Back"
        )

#Event handling for the buttons
    def handle_event(self, event):

        if self.start_button.is_clicked(event):
            print("Start clicked")

        elif self.settings_button.is_clicked(event):
            print("Settings clicked")

        elif self.multiplayer_button.is_clicked(event):
            print("Multiplayer clicked")

    def draw(self, screen):

        screen.fill(BACKGROUND)

        title = self.title_font.render(
            "Block Breaker Game",
            True,
            WHITE
        )

        title_rect = title.get_rect(center=(self.width // 2, 120))
        screen.blit(title, title_rect)

        self.start_button.draw(screen)
        self.settings_button.draw(screen)
        self.multiplayer_button.draw(screen)
        self.quit_button.draw(screen)

    def draw_difficulty(self, screen):
        screen.fill(BACKGROUND)

        title = self.title_font.render(
            "Select Difficulty",
            True,
            WHITE
        )

        title_rect = title.get_rect(center=(self.width // 2, 120))
        screen.blit(title, title_rect)

        self.easy_button.draw(screen)
        self.medium_button.draw(screen)
        self.hard_button.draw(screen)
        self.back_button.draw(screen)