import math
import pygame
from engine.Spring import Spring



class SpringChain:
    def __init__(self, anchor_x, anchor_y, num_springs, length, k, screen_height):
        self.springs = [Spring(anchor_x, anchor_y + i * length, length, k, screen_height) for i in range(num_springs)]
        self.dragging = False
        self.dragged_spring = None
    def update(self):
        for i, spring in enumerate(self.springs):
            spring.update()
            
            # If it's not the first spring, hook it to the one above
            if i > 0:
                spring.anchor[0] = self.springs[i-1].end[0]
                spring.anchor[1] = self.springs[i-1].end[1]
            
            # See if the spring is getting stretched too far
            if math.dist(spring.anchor, spring.end) > 1.5 * spring.rest_length and i > 0:
                # Pull the spring above a bit to help out
                self.springs[i-1].end[0] += (spring.end[0] - spring.anchor[0]) * 0.1
                self.springs[i-1].end[1] += (spring.end[1] - spring.anchor[1]) * 0.1





    def draw(self, screen):
        for spring in self.springs:
            spring.draw(screen)
