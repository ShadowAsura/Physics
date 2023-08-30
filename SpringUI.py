import pygame
import math
from Spring import Spring


class SpringUI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(None, 24)
        self.addButton = self.font.render("Add Spring", True, (0, 0, 0))
        self.addButtonRect = self.addButton.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, 100, 40))
        screen.blit(self.addButton, (self.x, self.y))

    def handle_event(self, event, spring_chain):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.addButtonRect.collidepoint(mouse_x, mouse_y):
                # Logic to add a new spring to the chain
                new_spring = Spring(spring_chain.springs[-1].end[0], spring_chain.springs[-1].end[1], 100, 0.05, 600)
                spring_chain.springs.append(new_spring)
