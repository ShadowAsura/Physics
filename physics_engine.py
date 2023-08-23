import pygame
import pygame.gfxdraw
from pendulum import Pendulum
from Spring import Spring
from SpringChain import SpringChain
import math

pygame.init()

# Constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create a window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Physics Engine")

# Create a chain of 3 springs, each of length 100
spring_chain = SpringChain(SCREEN_WIDTH // 2, 100, 3, 100, 0.05, SCREEN_HEIGHT)








running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check if the mouse is near the end of any spring in the chain
            for spring in spring_chain.springs:
                if math.sqrt((mouse_x - spring.end[0])**2 + (mouse_y - spring.end[1])**2) < 20:
                    spring.dragging = True
                    break  # Break out of the loop once a spring is being dragged
        elif event.type == pygame.MOUSEBUTTONUP:
            # Set dragging to False for all springs in the chain
            for spring in spring_chain.springs:
                spring.dragging = False

    screen.fill((255, 255, 255))  # Fill the screen with white

    

    # In the main loop:
    spring_chain.update()
    spring_chain.draw(screen)



    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
