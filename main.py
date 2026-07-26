import pygame
from menu import Menu

pygame.init()

#Window settings - subject to change
WIDTH = 1600
HEIGHT = 900
FPS = 60
game_state = "menu"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker Game")

clock = pygame.time.Clock()

#Menu creation
menu = Menu(WIDTH, HEIGHT)

class ImageButton:
    def __init__(self, x, y, image_path, size=None):
        self.image = pygame.image.load(image_path).convert_alpha()
        if size:
            self.image = pygame.transform.smoothscale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def draw_main(menu, screen):
    screen.fill((30, 30, 40))

    title = menu.title_font.render("Select Difficulty", True, (255, 255, 255))
    title_rect = title.get_rect(center=(menu.width // 2, 120))
    screen.blit(title, title_rect)

    menu.easy_button.draw(screen)
    menu.medium_button.draw(screen)
    menu.hard_button.draw(screen)
    menu.menu_back_button.draw(screen)


arrow_size = (90, 70)
arrow_margin = 60
arrow_x = WIDTH - arrow_size[0] - arrow_margin
arrow_y = arrow_margin
menu_back_button = ImageButton(arrow_x, arrow_y, "./images/image.png", size=arrow_size)
menu.menu_back_button = menu_back_button

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if menu.start_button.is_clicked(event):
                game_state = "game"
            elif menu.quit_button.is_clicked(event):
                running = False
            elif menu.settings_button.is_clicked(event):
                pass
            elif menu.multiplayer_button.is_clicked(event):
                pass
        elif game_state == "game":
            if menu_back_button.is_clicked(event):
                game_state = "menu"

    if game_state == "menu":
        menu.draw(screen)
    elif game_state == "game":
        draw_main(menu, screen)

    pygame.display.flip()

pygame.quit()