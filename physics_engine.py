import pygame
import pygame.gfxdraw
from pendulum import Pendulum
import math

pygame.init()

# Constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create a window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Physics Engine")

pendulum = Pendulum(SCREEN_WIDTH // 2, 100, 200, 0.5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Fill the screen with white

    pendulum.update()
    pendulum.draw(screen)

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
