import pygame
from menu import Menu

pygame.init()

#Window settings - subject to change
WIDTH = 1280
HEIGHT = 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker Game")

clock = pygame.time.Clock()

#Menu creation
menu = Menu(WIDTH, HEIGHT)

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        menu.handle_event(event)

    menu.draw(screen)

    if menu.quit_button.is_clicked(event):
        running = False

    pygame.display.flip()

pygame.quit()