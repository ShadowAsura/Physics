import math
import pygame

class Pendulum:
    def __init__(self, x, y, length, angle, child_length=None, child_angle=None):
        self.origin = (x, y)
        self.length = length
        self.angle = angle
        self.angular_velocity = 0
        self.angular_acceleration = 0
        self.GRAVITY = 0.4

        # If child_length and child_angle are provided, create a child pendulum
        self.child = None
        if child_length and child_angle:
            end_x = self.origin[0] + self.length * math.sin(self.angle)
            end_y = self.origin[1] + self.length * math.cos(self.angle)
            self.child = Pendulum(end_x, end_y, child_length, child_angle)

    def update(self):
        # Update the child pendulum first (if it exists)
        if self.child:
            self.child.update()

        # Calculate angular acceleration (simplified formula)
        self.angular_acceleration = (-self.GRAVITY / self.length) * math.sin(self.angle)
        
        # Update angular velocity and angle
        self.angular_velocity += self.angular_acceleration
        self.angular_velocity *= 0.99  # Damping
        self.angle += self.angular_velocity

        # Update the position of the child pendulum (if it exists)
        if self.child:
            self.child.origin = (self.origin[0] + self.length * math.sin(self.angle),
                                 self.origin[1] + self.length * math.cos(self.angle))

    def draw(self, screen):
        end_x = self.origin[0] + self.length * math.sin(self.angle)
        end_y = self.origin[1] + self.length * math.cos(self.angle)
        pygame.draw.aaline(screen, (0, 0, 0), self.origin, (end_x, end_y))
        pygame.draw.circle(screen, (0, 0, 255), (int(end_x), int(end_y)), 10)

        # Draw the child pendulum (if it exists)
        if self.child:
            self.child.draw(screen)
