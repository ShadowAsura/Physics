import math
import pygame

class Spring:
    def __init__(self, anchor_x, anchor_y, length, k, screen_height, num_coils=10):
        self.anchor = (anchor_x, anchor_y)  # Fixed anchor point
        self.length = length  # Rest length
        self.k = k  # Spring constant
        self.end = [anchor_x, anchor_y + length]  # Initial position of the end point
        self.velocity = [0, -20]
        self.screen_height = screen_height
        self.num_coils = num_coils
        self.coil_length = length / num_coils
        self.dragging = False

    def update(self):
        if self.dragging:
            self.end[0], self.end[1] = pygame.mouse.get_pos()
            self.velocity = [0, 0]  # Reset velocity
        else:
            # ... (rest of the update method)
            # Calculate displacement from rest position
            displacement = (self.end[1] - self.anchor[1]) - self.length
                
            # Calculate net acceleration
            g = 0.2  # Gravity
            acceleration = -self.k * displacement + g

            # Predict the next position
            next_position = self.end[1] + self.velocity[1] + acceleration

            # Boundary check for the end point
            if next_position > self.screen_height - 20:
                self.end[1] = self.screen_height - 20
                self.velocity[1] *= -0.6  # Reflect collision damping
            else:
                # Update velocity and position
                self.velocity[1] += acceleration
                self.velocity[1] *= 0.95 # Damping
                self.end[1] += self.velocity[1]


    def draw(self, screen):
        coil_space = (self.end[1] - self.anchor[1]) / self.num_coils
        for i in range(self.num_coils):
            start_y = self.anchor[1] + i * coil_space
            end_y = start_y + coil_space
            pygame.draw.arc(screen, (0, 0, 0), (self.anchor[0]-10, start_y, 20, coil_space), 0, math.pi, 2)
            pygame.draw.arc(screen, (0, 0, 0), (self.anchor[0]-10, start_y + coil_space/2, 20, coil_space), math.pi, 2*math.pi, 2)
        
        # Draw the mass at the end
        pygame.draw.circle(screen, (0, 0, 255), (int(self.end[0]), int(self.end[1])), 10)
