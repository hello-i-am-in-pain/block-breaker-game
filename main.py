import pygame
from menu import WHITE, Menu

pygame.init()

#Window settings - subject to change
WIDTH = 1280
HEIGHT = 720
FPS = 60
game_state = "menu"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker Game")

clock = pygame.time.Clock()

#Menu creation
menu = Menu(WIDTH, HEIGHT)

def draw_main(self, screen):
    screen.fill((30, 30, 40))

    title = self.title_font.render("Select Difficulty", True, (255, 255, 255))
    
    title_rect = title.get_rect(center=(self.width // 2, 120))
    screen.blit(title, title_rect)

    self.easy_button.draw(screen)
    self.medium_button.draw(screen)
    self.hard_button.draw(screen)

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        menu.handle_event(event)

    menu.draw(screen)

    if game_state == "menu":
        if menu.quit_button.is_clicked(event):
            running = False
        if menu.start_button.is_clicked(event):
            game_state = "game"
        if menu.settings_button.is_clicked(event):
            pass
        if menu.multiplayer_button.is_clicked(event):
            pass

    if game_state == "game":
        draw_main(menu, screen)

    pygame.display.flip()

pygame.quit()