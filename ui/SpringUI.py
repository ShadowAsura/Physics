import pygame
import math
from engine.FluidParticle import FluidParticle
from engine.Spring import Spring


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
        self.gravity = 9.81  # Initial value of gravity
        self.gravity_slider_x = self.x + 50  # Initial position of the gravity slider handle
        self.dragging_gravity_slider = False  # To track if the gravity slider is being dragged


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

        # Draw k value label
        k_value_label = self.font.render(f"k Value: {self.k:.2f} N/m", True, (0, 0, 0))
        screen.blit(k_value_label, (self.x, self.y + 120))
        # Draw gravity slider track
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y + 150), (self.x + 100, self.y + 150), 2)

        # Draw gravity slider handle
        pygame.draw.circle(screen, (255, 0, 0), (int(self.gravity_slider_x), self.y + 150), 5)

        # Draw label for gravity
        gravity_label = self.font.render(f"Gravity: {self.gravity:.2f} m/s^2", True, (0, 0, 0))
        screen.blit(gravity_label, (self.x, self.y + 160))


    def handle_event(self, event, spring_chain, scene_manager):
        # Define mouse_x and mouse_y at the beginning of the method
        mouse_x, mouse_y = pygame.mouse.get_pos()

        print("handle_event called")  # Debugging print statement

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle gravity slider
            if math.sqrt((mouse_x - self.gravity_slider_x)**2 + (mouse_y - (self.y + 150))**2) < 10:
                self.dragging_gravity_slider = True

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
            self.dragging_gravity_slider = False  # Add this line

        elif event.type == pygame.MOUSEMOTION:
            print("Mouse motion detected")  # Debugging
            if self.dragging_slider:
                print("Dragging slider")  # Debugging
                self.slider_x = min(max(self.x, mouse_x), self.x + 100)
                print("Slider X:", self.slider_x)  # Debugging

                # Update the k value based on the new slider_x position
                self.k = 0.01 + 0.19 * (self.slider_x - self.x) / 100.0  # Update k value between 0.01 and 0.2 N/m
                print(f"Current k value: {self.k}")  # Debugging

            elif self.dragging_gravity_slider:
                self.gravity_slider_x = min(max(self.x, mouse_x), self.x + 100)
                self.gravity = 0 + 20 * (self.gravity_slider_x - self.x) / 100.0  # Update gravity value between 0 and 20

        # Update k value and gravity for all springs in the chain
        for spring in spring_chain.springs:
            spring.k = self.k
            spring.GRAVITY = self.gravity


