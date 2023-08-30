import pygame
import math
from Spring import Spring


class SpringUI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(None, 24)
        self.addButton = self.font.render("Add Spring", True, (0, 0, 0))
        self.removeButton = self.font.render("Remove Spring", True, (0, 0, 0))
        self.k = 0.05  # Initial value of spring constant
        self.slider_x = self.x + 50  # Initial position of the slider handle
        self.dragging_slider = False


    def draw(self, screen):
        # Draw Add Spring button
        add_button_rect = pygame.Rect(self.x, self.y, 100, 40)
        pygame.draw.rect(screen, (200, 200, 200), add_button_rect)
        add_text_rect = self.addButton.get_rect(center=add_button_rect.center)
        screen.blit(self.addButton, add_text_rect)

        # Draw Remove Spring button (New)
        remove_button_rect = pygame.Rect(self.x, self.y + 50, 140, 40)
        pygame.draw.rect(screen, (200, 200, 200), remove_button_rect)
        remove_text_rect = self.removeButton.get_rect(center=remove_button_rect.center)
        screen.blit(self.removeButton, remove_text_rect)
        # Draw slider track
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y + 100), (self.x + 100, self.y + 100), 2)

        # Draw slider handle
        pygame.draw.circle(screen, (0, 0, 255), (int(self.slider_x), self.y + 100), 5)

    def handle_event(self, event, spring_chain):
        print("handle_event called")  # Debugging print statement
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Handle Add Spring button
            if pygame.Rect(self.x, self.y, 100, 40).collidepoint(mouse_x, mouse_y):
                new_spring = Spring(spring_chain.springs[-1].end[0], spring_chain.springs[-1].end[1], 100, 0.05, 600)
                spring_chain.springs.append(new_spring)

            # Handle Remove Spring button
            if pygame.Rect(self.x, self.y + 50, 140, 40).collidepoint(mouse_x, mouse_y):
                if len(spring_chain.springs) > 1:
                    spring_chain.springs.pop()

            if math.sqrt((mouse_x - self.slider_x)**2 + (mouse_y - (self.y + 100))**2) < 10:
                    print("Setting dragging_slider to True")  # Debugging
                    self.dragging_slider = True

        elif event.type == pygame.MOUSEBUTTONUP:
            print("Setting dragging_slider to False")  # Debugging
            self.dragging_slider = False


        elif event.type == pygame.MOUSEMOTION:
            print("Mouse motion detected")  # Debugging
            if self.dragging_slider:
                print("Dragging slider")  # Debugging
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.slider_x = min(max(self.x, mouse_x), self.x + 100)
                print("Slider X:", self.slider_x)  # Debugging


