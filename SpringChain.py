import math
import pygame
from Spring import Spring


class SpringChain:
    def __init__(self, anchor_x, anchor_y, num_springs, length, k, screen_height):
        self.springs = [Spring(anchor_x, anchor_y + i * length, length, k, screen_height) for i in range(num_springs)]
        self.dragging = False
        self.dragged_spring = None
    def update(self):
        # If the last spring is being dragged, update its end position to the mouse position
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.springs[-1].end = [mouse_x, mouse_y]

        # Update each spring in the chain
        for i, spring in enumerate(self.springs):
            spring.update()
            # If it's not the last spring, set the anchor of the next spring to the end of the current spring
            if i < len(self.springs) - 1:
                self.springs[i + 1].anchor = spring.end.copy()




    def draw(self, screen):
        for spring in self.springs:
            spring.draw(screen)
