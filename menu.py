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


class TextInputBox:
    """A minimal single-line text field for typing in an IP address.

    Pygame has no built-in text input widget, so this just accumulates
    characters from KEYDOWN events. Returns "submit" when Enter is
    pressed and "cancel" when Escape is pressed, so the caller can react
    without this class needing to know anything about game states.
    """

    def __init__(self, x, y, width, height, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("arial", 32)
        self.placeholder = placeholder
        self.text = ""

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_RETURN:
            return "submit"

        if event.key == pygame.K_ESCAPE:
            return "cancel"

        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            return None

        # Only accept characters that can legally appear in an IPv4
        # address, and cap the length at "255.255.255.255".
        if event.unicode and (event.unicode.isdigit() or event.unicode == "."):
            if len(self.text) < 15:
                self.text += event.unicode

        return None

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, width=2, border_radius=8)

        display_text = self.text if self.text else self.placeholder
        color = WHITE if self.text else (150, 150, 150)
        text_surface = self.font.render(display_text, True, color)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 15, self.rect.centery))
        screen.blit(text_surface, text_rect)

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
            "Solo"
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
            "Versus"
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

        self.host_button = Button(
            x, 260,
            button_width,
            button_height,
            "Host Game"
        )

        self.join_button = Button(
            x, 355,
            button_width,
            button_height,
            "Join Game"
        )

        self.ip_input = TextInputBox(
            x, 300,
            button_width,
            60,
            placeholder="Host IP address"
        )

        self.connect_button = Button(
            x, 400,
            button_width,
            button_height,
            "Connect"
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

    def draw_versus_mode_select(self, screen):
        screen.fill(BACKGROUND)

        title = self.title_font.render("Versus Mode", True, WHITE)
        title_rect = title.get_rect(center=(self.width // 2, 120))
        screen.blit(title, title_rect)

        self.host_button.draw(screen)
        self.join_button.draw(screen)
        self.back_button.draw(screen)

    def draw_host_waiting(self, screen, local_ip, status_message):
        screen.fill(BACKGROUND)

        title = self.title_font.render("Hosting...", True, WHITE)
        screen.blit(title, title.get_rect(center=(self.width // 2, 120)))

        info_font = pygame.font.SysFont("arial", 32)

        ip_text = info_font.render(f"Your IP: {local_ip}", True, WHITE)
        screen.blit(ip_text, ip_text.get_rect(center=(self.width // 2, 280)))

        status_text = info_font.render(status_message, True, (200, 200, 200))
        screen.blit(status_text, status_text.get_rect(center=(self.width // 2, 340)))

        hint_font = pygame.font.SysFont("arial", 26)
        hint_text = hint_font.render("Press Esc to cancel", True, (150, 150, 150))
        screen.blit(hint_text, hint_text.get_rect(center=(self.width // 2, 500)))

    def draw_join_ip_entry(self, screen, error_message=None):
        screen.fill(BACKGROUND)

        title = self.title_font.render("Join Game", True, WHITE)
        screen.blit(title, title.get_rect(center=(self.width // 2, 120)))

        label_font = pygame.font.SysFont("arial", 28)
        label = label_font.render("Host IP address:", True, WHITE)
        screen.blit(label, (self.ip_input.rect.x, self.ip_input.rect.y - 40))

        self.ip_input.draw(screen)
        self.connect_button.draw(screen)
        self.back_button.draw(screen)

        if error_message:
            error_font = pygame.font.SysFont("arial", 26)
            error_text = error_font.render(error_message, True, (220, 80, 80))
            screen.blit(error_text, error_text.get_rect(center=(self.width // 2, 500)))

    def draw_join_connecting(self, screen, host_ip, status_message):
        screen.fill(BACKGROUND)

        title = self.title_font.render("Connecting...", True, WHITE)
        screen.blit(title, title.get_rect(center=(self.width // 2, 120)))

        info_font = pygame.font.SysFont("arial", 32)

        ip_text = info_font.render(f"Connecting to {host_ip}", True, WHITE)
        screen.blit(ip_text, ip_text.get_rect(center=(self.width // 2, 280)))

        status_text = info_font.render(status_message, True, (200, 200, 200))
        screen.blit(status_text, status_text.get_rect(center=(self.width // 2, 340)))

        hint_font = pygame.font.SysFont("arial", 26)
        hint_text = hint_font.render("Press Esc to cancel", True, (150, 150, 150))
        screen.blit(hint_text, hint_text.get_rect(center=(self.width // 2, 500)))