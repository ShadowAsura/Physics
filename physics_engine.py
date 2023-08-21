import pygame
import pygame.gfxdraw
from pendulum import Pendulum
from Spring import Spring
import math

pygame.init()

# Constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create a window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Physics Engine")

spring = Spring(SCREEN_WIDTH // 2, 100, 100, 0.05, SCREEN_HEIGHT)







running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse position is near the spring's end
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if math.sqrt((mouse_x - spring.end[0])**2 + (mouse_y - spring.end[1])**2) < 20:
                spring.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            spring.dragging = False

    screen.fill((255, 255, 255))  # Fill the screen with white

    

    # In the main loop:
    spring.update()
    spring.draw(screen)



    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
