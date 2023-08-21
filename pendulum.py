import math
import pygame

class Pendulum:
    def __init__(self, x, y, length, angle):
        self.origin = (x, y)
        self.length = length
        self.angle = angle
        self.angular_velocity = 0
        self.angular_acceleration = 0
        self.GRAVITY = 0.4

    def update(self):
        # Calculate angular acceleration (simplified formula)
        self.angular_acceleration = (-self.GRAVITY / self.length) * math.sin(self.angle)
        
        # Update angular velocity and angle
        self.angular_velocity += self.angular_acceleration
        self.angular_velocity *= 0.99  # Damping
        self.angle += self.angular_velocity

    def draw(self, screen):
        end_x = self.origin[0] + self.length * math.sin(self.angle)
        end_y = self.origin[1] + self.length * math.cos(self.angle)
        
        # Use aaline for anti-aliased lines
        pygame.draw.aaline(screen, (0, 0, 0), self.origin, (end_x, end_y))
        
        # Use gfxdraw's aacircle and filled_circle for smoother circles
        pygame.gfxdraw.aacircle(screen, int(end_x), int(end_y), 10, (0, 0, 255))
        pygame.gfxdraw.filled_circle(screen, int(end_x), int(end_y), 10, (0, 0, 255))