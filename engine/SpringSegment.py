import pygame
import math


class SpringSegment:
    def __init__(self, x, y, length, k):
        self.x = x
        self.y = y
        self.length = length
        self.k = k
        self.vx = 0
        self.vy = 0

    def apply_force_from(self, other):
        # Compute force due to another segment
        distance = math.dist((self.x, self.y), (other.x, other.y))
        force = self.k * (distance - self.length)
        angle = math.atan2(other.y - self.y, other.x - self.x)

        force_x = force * math.cos(angle)
        force_y = force * math.sin(angle)

        # Update velocities based on the force
        self.vx += force_x
        self.vy += force_y

    def update(self):
        # Simple Euler integration
        self.x += self.vx
        self.y += self.vy
