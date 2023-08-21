import math
import pygame

class Spring:
    def __init__(self, anchor_x, anchor_y, length, k=0.1, num_coils=10):
        self.anchor = (anchor_x, anchor_y)
        self.length = length  # Rest length
        self.k = k  # Spring constant
        self.end = [anchor_x, anchor_y + length]  # Initial position of the end point
        self.velocity = [0, 0]
        self.num_coils = num_coils
        self.coil_length = length / num_coils

    def update(self):
        # Calculate displacement from rest position
        displacement = math.sqrt((self.end[0] - self.anchor[0])**2 + (self.end[1] - self.anchor[1])**2) - self.length
        
        # Limit the maximum stretch
        MAX_STRETCH = self.length * 0.5
        if displacement > MAX_STRETCH:
            displacement = MAX_STRETCH
        
        # Calculate force based on Hooke's law
        force = self.k * displacement

        # Update velocity and position (simple Euler integration for demonstration)
        self.velocity[1] += force - 0.2  # Adding gravity effect
        self.velocity[1] *= 0.92  # Increased damping
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

